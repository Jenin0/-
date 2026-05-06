import unittest
from space_station import (
    SpaceStation,
    LifeSupportModule,
    PowerModule,
    CommunicationModule,
    ResearchModule,
    ModuleStatus
)


class TestLifeSupportModule(unittest.TestCase):

    def setUp(self):
        self.module = LifeSupportModule("Кисень", power_consumption=100)

    def test_initial_status(self):
        self.assertEqual(self.module.status, ModuleStatus.INACTIVE)

    def test_activate(self):
        self.module.activate()
        self.assertEqual(self.module.status, ModuleStatus.ACTIVE)

    def test_regulate_oxygen(self):
        self.module.regulate_oxygen(25.0)
        self.assertIn("25.0", self.module.status_report())

    def test_invalid_oxygen(self):
        with self.assertRaises(ValueError):
            self.module.regulate_oxygen(150)

    def test_invalid_temperature(self):
        with self.assertRaises(ValueError):
            self.module.regulate_temperature(100)


class TestPowerModule(unittest.TestCase):

    def setUp(self):
        self.module = PowerModule("Сонячні панелі", 50, "solar", 500)

    def test_generate_when_active(self):
        self.module.activate()
        self.assertEqual(self.module.generate(), 500)

    def test_generate_when_inactive(self):
        self.assertEqual(self.module.generate(), 0.0)

    def test_invalid_power_type(self):
        with self.assertRaises(ValueError):
            PowerModule("Тест", 50, "gas", 100)

    def test_invalid_output(self):
        with self.assertRaises(ValueError):
            PowerModule("Тест", 50, "solar", -10)


class TestCommunicationModule(unittest.TestCase):

    def setUp(self):
        self.module = CommunicationModule("Антена", 30, 145.8, 25)

    def test_send_message_inactive(self, ):
        # не має відправляти якщо неактивний
        self.module.send_message("Тест")
        self.assertEqual(self.module.status, ModuleStatus.INACTIVE)

    def test_send_message_active(self):
        self.module.activate()
        self.module.send_message("Houston!")
        self.assertEqual(self.module.status, ModuleStatus.ACTIVE)


class TestResearchModule(unittest.TestCase):

    def setUp(self):
        self.module = ResearchModule("Лабораторія", 80)

    def test_experiment_when_active(self):
        self.module.activate()
        self.module.run_experiment("Помідори")
        self.assertIn("Помідори", self.module.status_report())

    def test_experiment_when_inactive(self):
        self.module.run_experiment("Помідори")
        self.assertNotIn("Помідори", self.module.status_report())


class TestSpaceStation(unittest.TestCase):

    def setUp(self):
        self.station = SpaceStation("Зоря-1")
        self.module = LifeSupportModule("Кисень", 100)

    def test_add_module(self):
        self.station.add_module(self.module)
        self.assertEqual(len(self.station), 1)

    def test_remove_module(self):
        self.station.add_module(self.module)
        self.station.remove_module("Кисень")
        self.assertEqual(len(self.station), 0)

    def test_duplicate_module(self):
        self.station.add_module(self.module)
        with self.assertRaises(ValueError):
            self.station.add_module(self.module)

    def test_total_power(self):
        self.station.add_module(self.module)
        self.assertEqual(self.station.total_power_consumption(), 100)

    def test_invalid_station_name(self):
        with self.assertRaises(ValueError):
            SpaceStation("")


if __name__ == "__main__":
    unittest.main()