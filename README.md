# Python Task Manager (Middle Level)

CLI-приложение для управления задачами на Python.

## Возможности

- Добавление задач с приоритетом и описанием
- Список с фильтрацией (только невыполненные / по приоритету)
- Отметка выполненными и удаление
- Сохранение в JSON
- Красивый вывод с помощью [Rich](https://github.com/Textualize/rich)

## Структура

```
src/
├── models.py      # Модели данных (dataclass + Enum)
├── storage.py     # Работа с файлом
└── cli.py         # Командная строка (argparse)
```

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
# Добавить задачу
python -m src.cli add "Написать отчёт" -p high --due 2026-12-01

# Список всех задач
python -m src.cli list

# Только невыполненные
python -m src.cli list --pending

# Отметить выполненной
python -m src.cli done 1

# Удалить
python -m src.cli delete 1
```

## Что использовалось

- `dataclasses` + `Enum`
- Типизация
- `argparse` с подкомандами
- Сохранение в JSON
- Библиотека Rich для красивого вывода
- Разделение на модули (models / storage / cli)

---

Создано Grok
