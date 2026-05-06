from space_station import (
    SpaceStation,
    LifeSupportModule,
    PowerModule,
    CommunicationModule,
    ResearchModule
)

# Створюємо станцію
station = SpaceStation("Зоря-1")

# Створюємо модулі
life_support = LifeSupportModule("Система кисню", power_consumption=100)
power = PowerModule("Сонячні панелі", power_consumption=50, power_type="solar", output=500)
comm = CommunicationModule("Антена", power_consumption=30, frequency=145.8, signal_strength=25)
research = ResearchModule("Лабораторія", power_consumption=80)

# Додаємо на станцію
station.add_module(life_support)
station.add_module(power)
station.add_module(comm)
station.add_module(research)

print("\n--- Статус станції ---")
print(station)

print("\n--- Вмикаємо модулі ---")
life_support.activate()
power.activate()
comm.activate()
research.activate()

print("\n--- Тестуємо функції ---")
life_support.regulate_oxygen(23.0)
life_support.regulate_temperature(24.0)
power.generate()
comm.send_message("Houston, все добре!")
research.run_experiment("Вирощування помідорів")

print("\n--- Звіти ---")
print(life_support.status_report())
print(power.status_report())
print(comm.status_report())
print(research.status_report())

print("\n--- Фінальний статус ---")
print(station)