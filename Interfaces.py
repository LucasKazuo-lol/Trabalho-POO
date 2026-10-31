# ABC e abstractmethod permitem representar contratos e classes abstratas em Python.
from abc import ABC, abstractmethod


class IExportavelJson(ABC):
    """Contrato das classes que sabem exportar seus dados para JSON — missão 6."""

    @abstractmethod
    def ParaJson(self):
        pass


class INotificador(ABC):
    """Contrato comum dos canais de notificação — missão 6."""

    @abstractmethod
    def ObterCanal(self):
        pass

    @abstractmethod
    def EnviarAlerta(self, destinatario, mensagem):
        pass
