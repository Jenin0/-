from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional


class ModuleStatus(Enum):
    """Можливі стани модуля станції."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    EMERGENCY = "emergency"


class Module(ABC):
    """
    Абстрактний базовий клас для всіх модулів космічної станції.
    """

    def __init__(self, name: str, power_consumption: float) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Назва модуля не може бути порожньою")
        if not isinstance(power_consumption, (int, float)) or power_consumption < 0:
            raise ValueError("Споживання енергії має бути >= 0")

        self._name: str = name
        self._status: ModuleStatus = ModuleStatus.INACTIVE
        self._power_consumption: float = float(power_consumption)

    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> ModuleStatus:
        return self._status

    @property
    def power_consumption(self) -> float:
        return self._power_consumption

    def activate(self) -> None:
        """Вмикає модуль."""
        self._status = ModuleStatus.ACTIVE
        print(f"[{self._name}] Модуль увімкнено ✅")

    def deactivate(self) -> None:
        """Вимикає модуль."""
        self._status = ModuleStatus.INACTIVE
        print(f"[{self._name}] Модуль вимкнено 🔴")

    @abstractmethod
    def status_report(self) -> str:
        """Звіт про стан модуля (реалізується в підкласах)."""
        ...

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Module):
            return self._name == other._name
        return NotImplemented

    def __lt__(self, other: "Module") -> bool:
        if isinstance(other, Module):
            return self._name < other._name
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name!r}, status={self._status.value})"

    def __str__(self) -> str:
        return f"Модуль «{self._name}» [{self._status.value}] | {self._power_consumption} Вт"
class LifeSupportModule(Module):
    """
    Модуль життєзабезпечення — контролює кисень і температуру.
    """

    def __init__(self, name: str, power_consumption: float,
                 oxygen_level: float = 21.0, temperature: float = 22.0) -> None:
        super().__init__(name, power_consumption)
        if not (0 <= oxygen_level <= 100):
            raise ValueError("Рівень кисню має бути від 0 до 100%")
        if not (-50 <= temperature <= 50):
            raise ValueError("Температура має бути від -50 до +50°C")
        self._oxygen_level: float = oxygen_level
        self._temperature: float = temperature

    def regulate_oxygen(self, target: float) -> None:
        """Регулює рівень кисню."""
        if not (0 <= target <= 100):
            raise ValueError("Рівень кисню має бути від 0 до 100%")
        self._oxygen_level = target
        print(f"[{self._name}] Кисень встановлено: {target}%")

    def regulate_temperature(self, target: float) -> None:
        """Регулює температуру."""
        if not (-50 <= target <= 50):
            raise ValueError("Температура має бути від -50 до +50°C")
        self._temperature = target
        print(f"[{self._name}] Температура встановлена: {target}°C")

    def status_report(self) -> str:
        return (f"[LifeSupport] {self._name} | "
                f"O₂: {self._oxygen_level}% | "
                f"Temp: {self._temperature}°C | "
                f"Статус: {self._status.value}")


class PowerModule(Module):
    """
    Енергетичний модуль — генерує електрику.
    """

    def __init__(self, name: str, power_consumption: float,
                 power_type: str, output: float) -> None:
        super().__init__(name, power_consumption)
        if power_type not in ("solar", "nuclear"):
            raise ValueError("Тип джерела: 'solar' або 'nuclear'")
        if output <= 0:
            raise ValueError("Потужність має бути > 0")
        self._power_type: str = power_type
        self._output: float = output

    def generate(self) -> float:
        """Генерує енергію якщо модуль активний."""
        if self._status == ModuleStatus.ACTIVE:
            print(f"[{self._name}] Генерація: {self._output} Вт ⚡")
            return self._output
        print(f"[{self._name}] Модуль неактивний, енергія не генерується")
        return 0.0

    def status_report(self) -> str:
        return (f"[Power] {self._name} | "
                f"Тип: {self._power_type} | "
                f"Вихід: {self._output} Вт | "
                f"Статус: {self._status.value}")


class CommunicationModule(Module):
    """
    Модуль зв'язку — відправляє повідомлення.
    """

    def __init__(self, name: str, power_consumption: float,
                 frequency: float, signal_strength: float) -> None:
        super().__init__(name, power_consumption)
        if frequency <= 0:
            raise ValueError("Частота має бути > 0")
        if signal_strength <= 0:
            raise ValueError("Потужність сигналу має бути > 0")
        self._frequency: float = frequency
        self._signal_strength: float = signal_strength

    def send_message(self, msg: str) -> None:
        """Відправляє повідомлення якщо модуль активний."""
        if self._status != ModuleStatus.ACTIVE:
            print(f"[{self._name}] Неможливо відправити — модуль неактивний")
            return
        print(f"[{self._name}] 📡 Відправлено: '{msg}'")

    def status_report(self) -> str:
        return (f"[Comm] {self._name} | "
                f"Частота: {self._frequency} МГц | "
                f"Сигнал: {self._signal_strength} дБ | "
                f"Статус: {self._status.value}")


class ResearchModule(Module):
    """
    Дослідницький модуль — проводить експерименти.
    """

    def __init__(self, name: str, power_consumption: float) -> None:
        super().__init__(name, power_consumption)
        self._experiments: list[str] = []

    def run_experiment(self, experiment_name: str) -> None:
        """Запускає експеримент якщо модуль активний."""
        if self._status != ModuleStatus.ACTIVE:
            print(f"[{self._name}] Неможливо запустити — модуль неактивний")
            return
        self._experiments.append(experiment_name)
        print(f"[{self._name}] 🔬 Експеримент '{experiment_name}' запущено")

    def status_report(self) -> str:
        exps = ", ".join(self._experiments) if self._experiments else "немає"
        return (f"[Research] {self._name} | "
                f"Експерименти: {exps} | "
                f"Статус: {self._status.value}")\

class SpaceStation:
    """
    Космічна станція — керує всіма модулями.
    """

    def __init__(self, name: str) -> None:
        if not name or not isinstance(name, str):
            raise ValueError("Назва станції не може бути порожньою")
        self._name: str = name
        self._modules: list[Module] = []

    def add_module(self, module: Module) -> None:
        """Додає модуль на станцію."""
        if module in self._modules:
            raise ValueError(f"Модуль «{module.name}» вже існує на станції")
        self._modules.append(module)
        print(f"[{self._name}] Модуль «{module.name}» додано ✅")

    def remove_module(self, name: str) -> None:
        """Видаляє модуль зі станції за назвою."""
        for module in self._modules:
            if module.name == name:
                self._modules.remove(module)
                print(f"[{self._name}] Модуль «{name}» видалено 🗑️")
                return
        raise ValueError(f"Модуль «{name}» не знайдено")

    def total_power_consumption(self) -> float:
        """Повертає загальне споживання енергії всіх модулів."""
        return sum(m.power_consumption for m in self._modules)

    def __len__(self) -> int:
        """Повертає кількість модулів на станції."""
        return len(self._modules)

    def __str__(self) -> str:
        """Загальний статус станції."""
        return (f"🚀 Станція «{self._name}» | "
                f"Модулів: {len(self)} | "
                f"Споживання: {self.total_power_consumption()} Вт")