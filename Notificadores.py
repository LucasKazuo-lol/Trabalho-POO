from rich import print
from rich.panel import Panel
from rich.text import Text

from Interfaces import INotificador
from Validacoes import ValidarTexto


class NotificadorPainel(INotificador):
    """Registra a mensagem para a tela e, opcionalmente, exibe um Panel no terminal."""

    def __init__(self, exibirNoTerminal=True):
        self.__mensagens = []
        self.exibirNoTerminal = exibirNoTerminal

    def ObterCanal(self):
        return "Painel"

    def GetMensagens(self):
        return tuple(self.__mensagens)

    def EnviarAlerta(self, destinatario, mensagem):
        mensagem = f"{ValidarTexto(destinatario, 'destinatário')}: {ValidarTexto(mensagem, 'mensagem')}"
        self.__mensagens.append(mensagem)
        if self.exibirNoTerminal:
            print(Panel(Text(mensagem, style="green"), title=self.ObterCanal(), border_style="blue"))
        return True


class NotificadorEmail(NotificadorPainel):
    """Simulação de e-mail do exercício; não envia mensagens reais."""

    def ObterCanal(self):
        return "E-mail (simulado)"
