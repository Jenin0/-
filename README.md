# 🚀 Космічна станція

Симулятор системи управління космічною станцією на Python.

## Структура класів
- `Module` — абстрактний базовий клас
- `LifeSupportModule` — система кисню та температури
- `PowerModule` — генерація енергії
- `CommunicationModule` — модуль зв'язку
- `ResearchModule` — дослідницький модуль
- `SpaceStation` — керує всіма модулями

## Запуск
```bash
python main.py
```

## Тести
```bash
python -m unittest tests.py -v
```
