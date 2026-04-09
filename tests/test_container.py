"""Tests for container types (task 1.2).

Each class tests a specific variant and auto-skips if the student's variant differs.
"""

import pytest


# ---------------------------------------------------------------------------
# Variant 0: SortedList
# ---------------------------------------------------------------------------
class TestSortedList:
    """Tests for variant 0 — SortedList (auto-sorted list on insert)."""

    @pytest.fixture(autouse=True)
    def skip_unless_variant(self, variant: int) -> None:
        if variant != 0:
            pytest.skip("Not variant 0")

    @pytest.fixture()
    def cls(self):
        from hw01.container import SortedList

        return SortedList

    # -- construction --
    def test_create_empty(self, cls):
        sl = cls()
        assert len(sl) == 0

    def test_create_from_iterable(self, cls):
        sl = cls([5, 2, 8, 1])
        assert list(sl) == [1, 2, 5, 8]

    # -- len --
    def test_len(self, cls):
        sl = cls([3, 1, 2])
        assert len(sl) == 3

    # -- maintains sort --
    def test_maintains_sort_on_init(self, cls):
        sl = cls([3, 1, 4, 1, 5, 9])
        assert list(sl) == [1, 1, 3, 4, 5, 9]

    def test_maintains_sort_on_add(self, cls):
        sl = cls([3, 1])
        sl.add(2)
        assert list(sl) == [1, 2, 3]

    def test_add_to_empty(self, cls):
        sl = cls()
        sl.add(42)
        assert list(sl) == [42]

    # -- getitem --
    def test_getitem_valid(self, cls):
        sl = cls([30, 10, 20])
        assert sl[0] == 10
        assert sl[1] == 20
        assert sl[2] == 30

    def test_getitem_negative(self, cls):
        sl = cls([30, 10, 20])
        assert sl[-1] == 30

    def test_getitem_out_of_range(self, cls):
        sl = cls([1])
        with pytest.raises(IndexError):
            sl[5]

    # -- delitem --
    def test_delitem(self, cls):
        sl = cls([3, 1, 2])
        del sl[0]  # removes smallest (1)
        assert list(sl) == [2, 3]

    def test_delitem_out_of_range(self, cls):
        sl = cls([1])
        with pytest.raises(IndexError):
            del sl[10]

    # -- iter / reversed --
    def test_iter(self, cls):
        sl = cls([3, 1, 2])
        assert list(iter(sl)) == [1, 2, 3]

    def test_reversed(self, cls):
        sl = cls([3, 1, 2])
        assert list(reversed(sl)) == [3, 2, 1]

    # -- contains --
    def test_contains_true(self, cls):
        sl = cls([3, 1, 2])
        assert 2 in sl

    def test_contains_false(self, cls):
        sl = cls([3, 1, 2])
        assert 99 not in sl

    # -- repr / str --
    def test_repr(self, cls):
        sl = cls([1, 2])
        r = repr(sl)
        assert isinstance(r, str)
        assert "1" in r and "2" in r

    def test_str(self, cls):
        sl = cls([1, 2])
        assert isinstance(str(sl), str)


# ---------------------------------------------------------------------------
# Variant 1: LimitedDict
# ---------------------------------------------------------------------------
class TestLimitedDict:
    """Tests for variant 1 — LimitedDict (dict with max N keys, LRU eviction)."""

    @pytest.fixture(autouse=True)
    def skip_unless_variant(self, variant: int) -> None:
        if variant != 1:
            pytest.skip("Not variant 1")

    @pytest.fixture()
    def cls(self):
        from hw01.container import LimitedDict

        return LimitedDict

    # -- construction --
    def test_create_empty(self, cls):
        ld = cls(maxsize=3)
        assert len(ld) == 0

    def test_create_with_items(self, cls):
        ld = cls(maxsize=5, items={"a": 1, "b": 2})
        assert len(ld) == 2

    # -- len --
    def test_len_after_set(self, cls):
        ld = cls(maxsize=3)
        ld["x"] = 1
        ld["y"] = 2
        assert len(ld) == 2

    # -- getitem / setitem --
    def test_getitem(self, cls):
        ld = cls(maxsize=3)
        ld["key"] = "value"
        assert ld["key"] == "value"

    def test_getitem_missing(self, cls):
        ld = cls(maxsize=3)
        with pytest.raises(KeyError):
            ld["missing"]

    def test_setitem_overwrite(self, cls):
        ld = cls(maxsize=3)
        ld["a"] = 1
        ld["a"] = 2
        assert ld["a"] == 2
        assert len(ld) == 1

    # -- LRU eviction --
    def test_eviction(self, cls):
        ld = cls(maxsize=2)
        ld["a"] = 1
        ld["b"] = 2
        ld["c"] = 3  # should evict "a"
        assert "a" not in ld
        assert "b" in ld
        assert "c" in ld
        assert len(ld) == 2

    def test_access_refreshes_lru(self, cls):
        ld = cls(maxsize=2)
        ld["a"] = 1
        ld["b"] = 2
        _ = ld["a"]  # refresh "a"
        ld["c"] = 3  # should evict "b" (least recently used)
        assert "a" in ld
        assert "b" not in ld
        assert "c" in ld

    # -- delitem --
    def test_delitem(self, cls):
        ld = cls(maxsize=3)
        ld["a"] = 1
        del ld["a"]
        assert "a" not in ld
        assert len(ld) == 0

    def test_delitem_missing(self, cls):
        ld = cls(maxsize=3)
        with pytest.raises(KeyError):
            del ld["missing"]

    # -- iter --
    def test_iter(self, cls):
        ld = cls(maxsize=5)
        ld["a"] = 1
        ld["b"] = 2
        keys = list(iter(ld))
        assert set(keys) == {"a", "b"}

    # -- reversed --
    def test_reversed(self, cls):
        ld = cls(maxsize=5)
        ld["a"] = 1
        ld["b"] = 2
        keys = list(reversed(ld))
        assert set(keys) == {"a", "b"}

    # -- contains --
    def test_contains(self, cls):
        ld = cls(maxsize=3)
        ld["x"] = 10
        assert "x" in ld
        assert "y" not in ld

    # -- repr / str --
    def test_repr(self, cls):
        ld = cls(maxsize=3)
        ld["a"] = 1
        assert isinstance(repr(ld), str)

    def test_str(self, cls):
        ld = cls(maxsize=3)
        assert isinstance(str(ld), str)


# ---------------------------------------------------------------------------
# Variant 2: TypedList
# ---------------------------------------------------------------------------
class TestTypedList:
    """Tests for variant 2 — TypedList (list with type checking on insert)."""

    @pytest.fixture(autouse=True)
    def skip_unless_variant(self, variant: int) -> None:
        if variant != 2:
            pytest.skip("Not variant 2")

    @pytest.fixture()
    def cls(self):
        from hw01.container import TypedList

        return TypedList

    # -- construction --
    def test_create_empty(self, cls):
        tl = cls(int)
        assert len(tl) == 0

    def test_create_from_iterable(self, cls):
        tl = cls(int, [1, 2, 3])
        assert list(tl) == [1, 2, 3]

    def test_create_wrong_type(self, cls):
        with pytest.raises(TypeError):
            cls(int, [1, "two", 3])

    # -- len --
    def test_len(self, cls):
        tl = cls(str, ["a", "b"])
        assert len(tl) == 2

    # -- type checking --
    def test_append_correct_type(self, cls):
        tl = cls(int)
        tl.append(42)
        assert list(tl) == [42]

    def test_append_wrong_type(self, cls):
        tl = cls(int)
        with pytest.raises(TypeError):
            tl.append("not an int")

    # -- getitem --
    def test_getitem(self, cls):
        tl = cls(int, [10, 20, 30])
        assert tl[1] == 20

    def test_getitem_negative(self, cls):
        tl = cls(int, [10, 20, 30])
        assert tl[-1] == 30

    def test_getitem_out_of_range(self, cls):
        tl = cls(int, [1])
        with pytest.raises(IndexError):
            tl[5]

    # -- setitem --
    def test_setitem_correct_type(self, cls):
        tl = cls(int, [1, 2, 3])
        tl[1] = 99
        assert tl[1] == 99

    def test_setitem_wrong_type(self, cls):
        tl = cls(int, [1, 2, 3])
        with pytest.raises(TypeError):
            tl[1] = "string"

    # -- delitem --
    def test_delitem(self, cls):
        tl = cls(int, [1, 2, 3])
        del tl[1]
        assert list(tl) == [1, 3]

    # -- iter / reversed --
    def test_iter(self, cls):
        tl = cls(int, [1, 2, 3])
        assert list(iter(tl)) == [1, 2, 3]

    def test_reversed(self, cls):
        tl = cls(int, [1, 2, 3])
        assert list(reversed(tl)) == [3, 2, 1]

    # -- contains --
    def test_contains(self, cls):
        tl = cls(str, ["hello", "world"])
        assert "hello" in tl
        assert "nope" not in tl

    # -- repr / str --
    def test_repr(self, cls):
        tl = cls(int, [1, 2])
        r = repr(tl)
        assert isinstance(r, str)
        assert "int" in r.lower() or "1" in r

    def test_str(self, cls):
        tl = cls(int, [1])
        assert isinstance(str(tl), str)


# ---------------------------------------------------------------------------
# Variant 3: FrozenDict
# ---------------------------------------------------------------------------
class TestFrozenDict:
    """Tests for variant 3 — FrozenDict (immutable dict, hashable)."""

    @pytest.fixture(autouse=True)
    def skip_unless_variant(self, variant: int) -> None:
        if variant != 3:
            pytest.skip("Not variant 3")

    @pytest.fixture()
    def cls(self):
        from hw01.container import FrozenDict

        return FrozenDict

    # -- construction --
    def test_create_empty(self, cls):
        fd = cls()
        assert len(fd) == 0

    def test_create_from_dict(self, cls):
        fd = cls({"a": 1, "b": 2})
        assert len(fd) == 2

    def test_create_from_kwargs(self, cls):
        fd = cls(x=10, y=20)
        assert fd["x"] == 10

    # -- immutability --
    def test_setitem_raises(self, cls):
        fd = cls({"a": 1})
        with pytest.raises(TypeError):
            fd["a"] = 2

    def test_delitem_raises(self, cls):
        fd = cls({"a": 1})
        with pytest.raises(TypeError):
            del fd["a"]

    # -- getitem --
    def test_getitem(self, cls):
        fd = cls({"key": "value"})
        assert fd["key"] == "value"

    def test_getitem_missing(self, cls):
        fd = cls({"a": 1})
        with pytest.raises(KeyError):
            fd["missing"]

    # -- len --
    def test_len(self, cls):
        fd = cls({"a": 1, "b": 2, "c": 3})
        assert len(fd) == 3

    # -- hashable --
    def test_hashable(self, cls):
        fd = cls({"a": 1, "b": 2})
        h = hash(fd)
        assert isinstance(h, int)

    def test_equality(self, cls):
        fd1 = cls({"a": 1, "b": 2})
        fd2 = cls({"b": 2, "a": 1})
        assert fd1 == fd2
        assert hash(fd1) == hash(fd2)

    def test_hash_consistent(self, cls):
        fd1 = cls({"a": 1, "b": 2})
        fd2 = cls({"a": 1, "b": 2})
        assert hash(fd1) == hash(fd2)

    def test_usable_as_dict_key(self, cls):
        fd = cls({"a": 1})
        d = {fd: "works"}
        assert d[fd] == "works"

    # -- iter / reversed --
    def test_iter(self, cls):
        fd = cls({"a": 1, "b": 2})
        keys = list(iter(fd))
        assert set(keys) == {"a", "b"}

    def test_reversed(self, cls):
        fd = cls({"a": 1, "b": 2})
        keys = list(reversed(fd))
        assert set(keys) == {"a", "b"}

    # -- contains --
    def test_contains(self, cls):
        fd = cls({"a": 1})
        assert "a" in fd
        assert "z" not in fd

    # -- repr / str --
    def test_repr(self, cls):
        fd = cls({"a": 1})
        assert isinstance(repr(fd), str)

    def test_str(self, cls):
        fd = cls({"a": 1})
        assert isinstance(str(fd), str)


# ---------------------------------------------------------------------------
# Variant 4: ChainList
# ---------------------------------------------------------------------------
class TestChainList:
    """Tests for variant 4 — ChainList (lazily concatenates multiple lists)."""

    @pytest.fixture(autouse=True)
    def skip_unless_variant(self, variant: int) -> None:
        if variant != 4:
            pytest.skip("Not variant 4")

    @pytest.fixture()
    def cls(self):
        from hw01.container import ChainList

        return ChainList

    # -- construction --
    def test_create_empty(self, cls):
        cl = cls()
        assert len(cl) == 0

    def test_create_from_lists(self, cls):
        cl = cls([1, 2], [3, 4])
        assert list(cl) == [1, 2, 3, 4]

    def test_create_single_list(self, cls):
        cl = cls([10, 20])
        assert list(cl) == [10, 20]

    # -- lazy: modifications to original lists reflect --
    def test_lazy_reflects_changes(self, cls):
        a = [1, 2]
        b = [3, 4]
        cl = cls(a, b)
        a.append(99)
        assert 99 in cl

    # -- len --
    def test_len(self, cls):
        cl = cls([1, 2], [3], [4, 5, 6])
        assert len(cl) == 6

    # -- getitem --
    def test_getitem_across_boundaries(self, cls):
        cl = cls([1, 2], [3, 4])
        assert cl[0] == 1
        assert cl[1] == 2
        assert cl[2] == 3
        assert cl[3] == 4

    def test_getitem_negative(self, cls):
        cl = cls([1, 2], [3, 4])
        assert cl[-1] == 4
        assert cl[-3] == 2

    def test_getitem_out_of_range(self, cls):
        cl = cls([1])
        with pytest.raises(IndexError):
            cl[10]

    # -- iter / reversed --
    def test_iter(self, cls):
        cl = cls([1, 2], [3])
        assert list(iter(cl)) == [1, 2, 3]

    def test_reversed(self, cls):
        cl = cls([1, 2], [3])
        assert list(reversed(cl)) == [3, 2, 1]

    # -- contains --
    def test_contains(self, cls):
        cl = cls([1, 2], [3, 4])
        assert 3 in cl
        assert 99 not in cl

    # -- repr / str --
    def test_repr(self, cls):
        cl = cls([1], [2])
        assert isinstance(repr(cl), str)

    def test_str(self, cls):
        cl = cls([1], [2])
        assert isinstance(str(cl), str)


# ---------------------------------------------------------------------------
# Variant 5: BiDict
# ---------------------------------------------------------------------------
class TestBiDict:
    """Tests for variant 5 — BiDict (bidirectional dict: key <-> value)."""

    @pytest.fixture(autouse=True)
    def skip_unless_variant(self, variant: int) -> None:
        if variant != 5:
            pytest.skip("Not variant 5")

    @pytest.fixture()
    def cls(self):
        from hw01.container import BiDict

        return BiDict

    # -- construction --
    def test_create_empty(self, cls):
        bd = cls()
        assert len(bd) == 0

    def test_create_from_dict(self, cls):
        bd = cls({"a": 1, "b": 2})
        assert bd["a"] == 1

    # -- bidirectional access --
    def test_inverse_lookup(self, cls):
        bd = cls({"a": 1, "b": 2})
        assert bd.inverse[1] == "a"
        assert bd.inverse[2] == "b"

    def test_setitem_updates_inverse(self, cls):
        bd = cls()
        bd["x"] = 10
        assert bd.inverse[10] == "x"

    def test_overwrite_cleans_old_inverse(self, cls):
        bd = cls()
        bd["a"] = 1
        bd["a"] = 2
        assert bd.inverse[2] == "a"
        assert 1 not in bd.inverse

    # -- duplicate values --
    def test_duplicate_value_raises_or_overwrites(self, cls):
        """BiDict must enforce value uniqueness: either raise or evict old key."""
        bd = cls()
        bd["a"] = 1
        bd["b"] = 1  # value 1 already mapped to "a"
        # After this, at most one key maps to 1
        count = sum(1 for k in bd if bd[k] == 1)
        assert count == 1

    # -- len --
    def test_len(self, cls):
        bd = cls({"a": 1, "b": 2})
        assert len(bd) == 2

    # -- getitem --
    def test_getitem(self, cls):
        bd = cls({"k": "v"})
        assert bd["k"] == "v"

    def test_getitem_missing(self, cls):
        bd = cls()
        with pytest.raises(KeyError):
            bd["nope"]

    # -- delitem --
    def test_delitem(self, cls):
        bd = cls({"a": 1})
        del bd["a"]
        assert "a" not in bd
        assert 1 not in bd.inverse

    def test_delitem_missing(self, cls):
        bd = cls()
        with pytest.raises(KeyError):
            del bd["nope"]

    # -- iter / reversed --
    def test_iter(self, cls):
        bd = cls({"a": 1, "b": 2})
        keys = list(iter(bd))
        assert set(keys) == {"a", "b"}

    def test_reversed(self, cls):
        bd = cls({"a": 1, "b": 2})
        keys = list(reversed(bd))
        assert set(keys) == {"a", "b"}

    # -- contains --
    def test_contains(self, cls):
        bd = cls({"a": 1})
        assert "a" in bd
        assert "z" not in bd

    # -- repr / str --
    def test_repr(self, cls):
        bd = cls({"a": 1})
        assert isinstance(repr(bd), str)

    def test_str(self, cls):
        bd = cls({"a": 1})
        assert isinstance(str(bd), str)


# ---------------------------------------------------------------------------
# Variant 6: RingBuffer
# ---------------------------------------------------------------------------
class TestRingBuffer:
    """Tests for variant 6 — RingBuffer (fixed-size circular buffer)."""

    @pytest.fixture(autouse=True)
    def skip_unless_variant(self, variant: int) -> None:
        if variant != 6:
            pytest.skip("Not variant 6")

    @pytest.fixture()
    def cls(self):
        from hw01.container import RingBuffer

        return RingBuffer

    # -- construction --
    def test_create_empty(self, cls):
        rb = cls(capacity=5)
        assert len(rb) == 0

    def test_create_from_iterable(self, cls):
        rb = cls(capacity=5, items=[1, 2, 3])
        assert list(rb) == [1, 2, 3]

    # -- fixed size: overflow wraps --
    def test_overflow_drops_oldest(self, cls):
        rb = cls(capacity=3)
        for i in range(5):
            rb.append(i)
        # capacity 3: should have [2, 3, 4]
        assert list(rb) == [2, 3, 4]
        assert len(rb) == 3

    def test_single_capacity(self, cls):
        rb = cls(capacity=1)
        rb.append(1)
        rb.append(2)
        assert list(rb) == [2]

    # -- len --
    def test_len_partial(self, cls):
        rb = cls(capacity=5)
        rb.append(1)
        rb.append(2)
        assert len(rb) == 2

    def test_len_full(self, cls):
        rb = cls(capacity=3)
        for i in range(10):
            rb.append(i)
        assert len(rb) == 3

    # -- getitem --
    def test_getitem(self, cls):
        rb = cls(capacity=5, items=[10, 20, 30])
        assert rb[0] == 10
        assert rb[2] == 30

    def test_getitem_negative(self, cls):
        rb = cls(capacity=5, items=[10, 20, 30])
        assert rb[-1] == 30

    def test_getitem_after_overflow(self, cls):
        rb = cls(capacity=3)
        for i in range(5):  # [2, 3, 4]
            rb.append(i)
        assert rb[0] == 2
        assert rb[2] == 4

    def test_getitem_out_of_range(self, cls):
        rb = cls(capacity=5, items=[1])
        with pytest.raises(IndexError):
            rb[5]

    # -- iter / reversed --
    def test_iter(self, cls):
        rb = cls(capacity=4, items=[1, 2, 3])
        assert list(iter(rb)) == [1, 2, 3]

    def test_reversed(self, cls):
        rb = cls(capacity=4, items=[1, 2, 3])
        assert list(reversed(rb)) == [3, 2, 1]

    def test_iter_after_overflow(self, cls):
        rb = cls(capacity=3)
        for i in range(5):
            rb.append(i)
        assert list(rb) == [2, 3, 4]

    # -- contains --
    def test_contains(self, cls):
        rb = cls(capacity=5, items=[1, 2, 3])
        assert 2 in rb
        assert 99 not in rb

    # -- repr / str --
    def test_repr(self, cls):
        rb = cls(capacity=3, items=[1, 2])
        assert isinstance(repr(rb), str)

    def test_str(self, cls):
        rb = cls(capacity=3)
        assert isinstance(str(rb), str)


# ---------------------------------------------------------------------------
# Variant 7: DefaultList
# ---------------------------------------------------------------------------
class TestDefaultList:
    """Tests for variant 7 — DefaultList (defaultdict-like but for list)."""

    @pytest.fixture(autouse=True)
    def skip_unless_variant(self, variant: int) -> None:
        if variant != 7:
            pytest.skip("Not variant 7")

    @pytest.fixture()
    def cls(self):
        from hw01.container import DefaultList

        return DefaultList

    # -- construction --
    def test_create_empty(self, cls):
        dl = cls(default=0)
        assert len(dl) == 0

    def test_create_from_iterable(self, cls):
        dl = cls(default=0, items=[1, 2, 3])
        assert list(dl) == [1, 2, 3]

    def test_create_with_callable_default(self, cls):
        dl = cls(default=lambda: "x")
        # Accessing out-of-range index returns default and extends
        val = dl[5]
        assert val == "x"

    # -- default on out-of-range access --
    def test_getitem_extends_with_default(self, cls):
        dl = cls(default=0)
        val = dl[3]
        assert val == 0
        # list should now have length >= 4
        assert len(dl) >= 4

    def test_getitem_fills_gaps(self, cls):
        dl = cls(default=-1, items=[10, 20])
        val = dl[5]
        assert val == -1
        # indices 2, 3, 4 should also be filled
        assert dl[2] == -1
        assert dl[4] == -1

    def test_getitem_valid_no_extend(self, cls):
        dl = cls(default=0, items=[10, 20, 30])
        assert dl[1] == 20
        assert len(dl) == 3

    def test_getitem_negative(self, cls):
        dl = cls(default=0, items=[10, 20, 30])
        assert dl[-1] == 30

    # -- len --
    def test_len(self, cls):
        dl = cls(default=0, items=[1, 2])
        assert len(dl) == 2

    # -- setitem --
    def test_setitem_within_range(self, cls):
        dl = cls(default=0, items=[1, 2, 3])
        dl[1] = 99
        assert dl[1] == 99

    def test_setitem_beyond_range(self, cls):
        dl = cls(default=0)
        dl[3] = 42
        assert dl[3] == 42
        assert len(dl) >= 4

    # -- delitem --
    def test_delitem(self, cls):
        dl = cls(default=0, items=[1, 2, 3])
        del dl[1]
        assert list(dl) == [1, 3]

    # -- iter / reversed --
    def test_iter(self, cls):
        dl = cls(default=0, items=[1, 2, 3])
        assert list(iter(dl)) == [1, 2, 3]

    def test_reversed(self, cls):
        dl = cls(default=0, items=[1, 2, 3])
        assert list(reversed(dl)) == [3, 2, 1]

    # -- contains --
    def test_contains(self, cls):
        dl = cls(default=0, items=[1, 2, 3])
        assert 2 in dl
        assert 99 not in dl

    # -- repr / str --
    def test_repr(self, cls):
        dl = cls(default=0, items=[1, 2])
        assert isinstance(repr(dl), str)

    def test_str(self, cls):
        dl = cls(default=0)
        assert isinstance(str(dl), str)
