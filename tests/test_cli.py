"""Tests for CLI utilities (task 1.3).

CLI variant depends on container variant:
  Variants 0, 3, 6 -> wc (count lines, words, bytes)
  Variants 1, 4, 7 -> nl (number lines)
  Variants 2, 5    -> tail (last N lines)
"""

import re
import subprocess
import sys
from pathlib import Path

import pytest


def _run_cli(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    """Run hw01 CLI via `python -m hw01`."""
    return subprocess.run(
        [sys.executable, "-m", "hw01", *args],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
        cwd=Path(__file__).resolve().parent.parent,
    )


@pytest.fixture()
def sample_file(tmp_path: Path) -> Path:
    """Create a sample text file for testing."""
    p = tmp_path / "sample.txt"
    p.write_text("hello world\nfoo bar baz\nqux\n", encoding="utf-8", newline="")
    return p


@pytest.fixture()
def multi_line_file(tmp_path: Path) -> Path:
    """Create a file with many lines for tail testing."""
    p = tmp_path / "lines.txt"
    lines = [f"line {i}" for i in range(1, 21)]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="")
    return p


@pytest.fixture()
def empty_file(tmp_path: Path) -> Path:
    """Create an empty file."""
    p = tmp_path / "empty.txt"
    p.write_text("", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# wc tests (variants 0, 3, 6)
# ---------------------------------------------------------------------------
class TestWc:
    """Tests for wc CLI utility."""

    @pytest.fixture(autouse=True)
    def skip_unless_wc(self, variant: int) -> None:
        if variant not in (0, 3, 6):
            pytest.skip("Not a wc variant")

    def test_line_count(self, sample_file: Path) -> None:
        result = _run_cli(str(sample_file))
        assert result.returncode == 0
        # "hello world\nfoo bar baz\nqux\n" = 3 lines
        assert re.search(r"\b3\b", result.stdout)

    def test_word_count(self, sample_file: Path) -> None:
        result = _run_cli(str(sample_file))
        assert result.returncode == 0
        # 2 + 3 + 1 = 6 words
        assert re.search(r"\b6\b", result.stdout)

    def test_byte_count(self, sample_file: Path) -> None:
        result = _run_cli(str(sample_file))
        assert result.returncode == 0
        content = "hello world\nfoo bar baz\nqux\n"
        expected_bytes = len(content.encode("utf-8"))
        assert str(expected_bytes) in result.stdout

    def test_stdin(self) -> None:
        result = _run_cli(stdin="one two\nthree\n")
        assert result.returncode == 0
        assert "2" in result.stdout  # 2 lines

    def test_empty_file(self, empty_file: Path) -> None:
        result = _run_cli(str(empty_file))
        assert result.returncode == 0
        assert "0" in result.stdout

    def test_missing_file(self) -> None:
        result = _run_cli("/nonexistent/file.txt")
        assert result.returncode != 0

    def test_multiple_files(self, sample_file: Path, tmp_path: Path) -> None:
        f2 = tmp_path / "second.txt"
        f2.write_text("a b c\n", encoding="utf-8", newline="")
        result = _run_cli(str(sample_file), str(f2))
        assert result.returncode == 0
        # Should have output for both files
        out = result.stdout
        assert re.search(r"\b3\b", out)  # lines from sample
        assert re.search(r"\b1\b", out)  # lines from second

    def test_lines_only_flag(self, sample_file: Path) -> None:
        """Test -l flag for line count only."""
        result = _run_cli("-l", str(sample_file))
        assert result.returncode == 0
        assert "3" in result.stdout


# ---------------------------------------------------------------------------
# nl tests (variants 1, 4, 7)
# ---------------------------------------------------------------------------
class TestNl:
    """Tests for nl CLI utility."""

    @pytest.fixture(autouse=True)
    def skip_unless_nl(self, variant: int) -> None:
        if variant not in (1, 4, 7):
            pytest.skip("Not an nl variant")

    def test_basic_numbering(self, sample_file: Path) -> None:
        result = _run_cli(str(sample_file))
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 3
        # First line should contain "1" and "hello world"
        assert "1" in lines[0]
        assert "hello world" in lines[0]

    def test_sequential_numbers(self, sample_file: Path) -> None:
        result = _run_cli(str(sample_file))
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        for i, line in enumerate(lines, start=1):
            assert str(i) in line

    def test_stdin(self) -> None:
        result = _run_cli(stdin="alpha\nbeta\ngamma\n")
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 3
        assert "1" in lines[0]
        assert "alpha" in lines[0]
        assert "3" in lines[2]
        assert "gamma" in lines[2]

    def test_empty_file(self, empty_file: Path) -> None:
        result = _run_cli(str(empty_file))
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_missing_file(self) -> None:
        result = _run_cli("/nonexistent/file.txt")
        assert result.returncode != 0

    def test_single_line(self, tmp_path: Path) -> None:
        f = tmp_path / "one.txt"
        f.write_text("only line\n", encoding="utf-8", newline="")
        result = _run_cli(str(f))
        assert result.returncode == 0
        assert "1" in result.stdout
        assert "only line" in result.stdout

    def test_preserves_content(self, sample_file: Path) -> None:
        result = _run_cli(str(sample_file))
        assert result.returncode == 0
        assert "hello world" in result.stdout
        assert "foo bar baz" in result.stdout
        assert "qux" in result.stdout

    def test_multiple_files(self, sample_file: Path, tmp_path: Path) -> None:
        f2 = tmp_path / "extra.txt"
        f2.write_text("line a\nline b\n", encoding="utf-8", newline="")
        result = _run_cli(str(sample_file), str(f2))
        assert result.returncode == 0
        # Should number lines from both files
        assert "hello world" in result.stdout
        assert "line a" in result.stdout


# ---------------------------------------------------------------------------
# tail tests (variants 2, 5)
# ---------------------------------------------------------------------------
class TestTail:
    """Tests for tail CLI utility."""

    @pytest.fixture(autouse=True)
    def skip_unless_tail(self, variant: int) -> None:
        if variant not in (2, 5):
            pytest.skip("Not a tail variant")

    def test_default_last_10(self, multi_line_file: Path) -> None:
        result = _run_cli(str(multi_line_file))
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        # Default: last 10 lines of a 20-line file
        assert len(lines) == 10
        assert "line 11" in lines[0]
        assert "line 20" in lines[-1]

    def test_custom_n(self, multi_line_file: Path) -> None:
        result = _run_cli("-n", "3", str(multi_line_file))
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 3
        assert "line 18" in lines[0]
        assert "line 20" in lines[-1]

    def test_n_greater_than_file(self, sample_file: Path) -> None:
        result = _run_cli("-n", "100", str(sample_file))
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 3  # file only has 3 lines

    def test_stdin(self) -> None:
        input_text = "\n".join(f"row {i}" for i in range(1, 11)) + "\n"
        result = _run_cli("-n", "3", stdin=input_text)
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 3
        assert "row 8" in lines[0]
        assert "row 10" in lines[-1]

    def test_empty_file(self, empty_file: Path) -> None:
        result = _run_cli(str(empty_file))
        assert result.returncode == 0
        assert result.stdout.strip() == ""

    def test_missing_file(self) -> None:
        result = _run_cli("/nonexistent/file.txt")
        assert result.returncode != 0

    def test_single_line_file(self, tmp_path: Path) -> None:
        f = tmp_path / "single.txt"
        f.write_text("only\n", encoding="utf-8", newline="")
        result = _run_cli("-n", "5", str(f))
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 1
        assert "only" in lines[0]

    def test_n_one(self, multi_line_file: Path) -> None:
        result = _run_cli("-n", "1", str(multi_line_file))
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 1
        assert "line 20" in lines[0]
