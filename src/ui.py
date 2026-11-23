from abc import ABC, abstractmethod


class UserIO(ABC):
    @abstractmethod
    def get_input(self):
        raise NotImplementedError


class ConsoleUserIO(UserIO):
    def get_input(self):
        a = float(input("Введите сторону a: "))
        b = float(input("Введите сторону b: "))
        c = float(input("Введите сторону c: "))
        return a, b, c