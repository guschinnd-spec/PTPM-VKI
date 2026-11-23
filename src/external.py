from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        raise NotImplementedError


class EmailNotifier(Notifier):
    def send(self, message: str) -> bool:
        print(f"[EMAIL] Отправлено: {message}")
        return True