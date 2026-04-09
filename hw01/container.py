"""Контейнерный тип (задание 1.2).

Реализуй контейнер согласно своему варианту.
Вариант определяется автоматически по ФИО в STUDENT.md.

Варианты:
  0 — SortedList: автоматически сортируемый список (Sequence)
  1 — LimitedDict: словарь с макс. N ключей, LRU-вытеснение (MutableMapping)
  2 — TypedList: список с проверкой типа при вставке (Sequence)
  3 — FrozenDict: неизменяемый словарь, hashable (Mapping)
  4 — ChainList: ленивая конкатенация нескольких списков (Sequence)
  5 — BiDict: двунаправленный словарь key <-> value (MutableMapping)
  6 — RingBuffer: кольцевой буфер фиксированного размера (Sequence)
  7 — DefaultList: defaultdict-подобный, но для списка (Sequence)

Обязательные методы:
  __len__, __getitem__, __setitem__ (где применимо), __delitem__ (где применимо),
  __iter__, __reversed__, __contains__, __repr__, __str__

Используй ABC из collections.abc (Sequence, MutableSequence, Mapping, MutableMapping).
"""

# TODO: Реализуй свой контейнерный тип здесь
