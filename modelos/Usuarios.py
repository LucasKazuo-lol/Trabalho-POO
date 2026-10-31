from abc import ABC, abstractmethod
from hashlib import pbkdf2_hmac
from hmac import compare_digest
import secrets

from modelos.Disciplina import Disciplina
from modelos.Sessoes import SessaoEstudo, SessaoPomodoro, SessaoLeitura
from servicos.Validacoes import ValidarInteiro, ValidarTexto


class Usuario(ABC):
    """Classe abstrata comum aos três perfis — missão 3."""

    def __init__(self, id, nome, email, senha):
        self.__id = ValidarTexto(str(id), "identificador")
        self.__nome = ValidarTexto(nome, "nome")
        self.__email = ValidarTexto(email, "e-mail")
        if "@" not in self.__email:
            raise ValueError("E-mail inválido.")
        # A senha não tem getter. Guardamos uma derivação, e não o texto digitado.
        self.__sal = secrets.token_bytes(16)
        self.__senha = self.__GerarSenha(ValidarTexto(senha, "senha"))

    def __GerarSenha(self, senha):
        return pbkdf2_hmac("sha256", senha.encode("utf-8"), self.__sal, 100000)

    def GetId(self):
        return self.__id

    def GetNome(self):
        return self.__nome

    def GetEmail(self):
        return self.__email

    def Autenticar(self, senhaDigitada):
        return compare_digest(self.__senha, self.__GerarSenha(senhaDigitada))

    @abstractmethod
    def ObterTipoPerfil(self):
        pass

    @abstractmethod
    def GerarPainelResumo(self):
        pass


class Administrador(Usuario):
    def __init__(self, id, nome, email, senha, cargo):
        super().__init__(id, nome, email, senha)
        self.cargo = ValidarTexto(cargo, "cargo")

    def ObterTipoPerfil(self):
        return "Administrador"

    def GerarPainelResumo(self):
        return f"{self.GetNome()} | Administrador | {self.cargo}"


class Discente(Usuario):
    """Aluno com RA, XP e histórico — missões 3 e 5."""

    def __init__(self, id, nome, email, senha, ra):
        super().__init__(id, nome, email, senha)
        self.ra = ValidarTexto(ra, "RA")
        self.__xpTotal = 0
        self.__historico = []

    def GetXpTotal(self):
        return self.__xpTotal

    def GetHistorico(self):
        # A tupla protege a lista interna contra append/remove externos.
        return tuple(self.__historico)

    def AdicionarXp(self, pontos):
        self.__xpTotal += ValidarInteiro(pontos, "XP")

    def ObterTipoPerfil(self):
        return "Discente"

    def GerarPainelResumo(self):
        return f"{self.GetNome()} | RA {self.ra} | {self.__xpTotal} XP"

    def RegistrarEstudo(self, entrada, *argumentos):
        # Python não tem sobrecarga por assinatura como C#.
        # Uma implementação reconhece as três formas de chamada da missão 5.
        if isinstance(entrada, SessaoEstudo) and len(argumentos) == 0:
            sessao = entrada
        elif isinstance(entrada, Disciplina) and len(argumentos) == 1:
            minutos = ValidarInteiro(argumentos[0], "Duração", 1, 480)
            ciclos = max(1, minutos // 25)
            sessao = SessaoPomodoro(entrada, minutos, ciclos)
        elif isinstance(entrada, Disciplina) and len(argumentos) == 3:
            inicio, fim, paginas = argumentos
            ValidarInteiro(inicio, "Hora inicial", 0, 23)
            ValidarInteiro(fim, "Hora final", 1, 24)
            minutos = (fim - inicio) * 60
            sessao = SessaoLeitura(entrada, minutos, paginas, True)
        else:
            raise TypeError("Use sessão; disciplina/minutos; ou disciplina/início/fim/páginas.")

        self.__historico.append(sessao)
        self.AdicionarXp(sessao.CalcularXp())
        return sessao


class Responsavel(Usuario):
    """Associa discentes já existentes às suas metas — missões 3 e 7."""

    def __init__(self, id, nome, email, senha, parentesco):
        super().__init__(id, nome, email, senha)
        self.parentesco = ValidarTexto(parentesco, "parentesco")
        self.__discentes = {}
        self.__metas = {}

    def VincularDiscente(self, discente):
        # O dicionário impede cadastrar duas vezes o mesmo identificador.
        self.__discentes.setdefault(discente.GetId(), discente)

    def DefinirMeta(self, discente, meta):
        self.VincularDiscente(discente)
        self.__metas[discente.GetId()] = meta

    def GetMeta(self, discente):
        return self.__metas.get(discente.GetId())

    def GetDiscentes(self):
        return tuple(self.__discentes.values())

    def ObterTipoPerfil(self):
        return "Responsavel"

    def GerarPainelResumo(self):
        return (f"{self.GetNome()} | {self.parentesco} | "
                f"{len(self.__discentes)} discente(s) acompanhado(s)")
