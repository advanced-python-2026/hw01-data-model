# ДЗ 1 — Модель данных, CLI, пакетирование

Полный текст задания: https://advanced-python.ru/advanced-python/homework/hw01

## Быстрый старт

1. **Заполни `STUDENT.md`** — впиши ФИО точно как в ведомости (от этого зависит вариант).
2. **Установи зависимости:**
   ```bash
   uv sync
   ```
3. **Посмотри свой вариант:**
   ```bash
   uv run pytest -v --co
   ```
4. **Реализуй задания** в `hw01/container.py` и `hw01/cli.py`.
5. **Добавь entry point** в `pyproject.toml` секцию `[project.scripts]`.
6. **Проверь локально:**
   ```bash
   uv run ruff check .
   uv run ruff format --check .
   uv run pytest -v
   ```
7. **Запуш в main** — CI проверит автоматически.

## Структура

```
hw01/
  __init__.py      — пакет
  container.py     — контейнерный тип (задание 1.2)
  cli.py           — CLI-утилита (задание 1.3)
  __main__.py      — python -m hw01
tests/
  conftest.py      — определение варианта по ФИО
  test_container.py — тесты контейнера
  test_cli.py      — тесты CLI
```
