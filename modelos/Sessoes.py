from abc import abstractmethod
import json

from modelos.Disciplina import Disciplina
from modelos.Interfaces import IExportavelJson
from servicos.Validacoes import ValidarInteiro


class SessaoEstudo(IExportavelJson):
    """Base abstrata das modalidades de estudo — missões 4 e 6."""

    def __init__(self, disciplina, duracaoMinutos):
        if not isinstance(disciplina, Disciplina):
            raise ValueError("Informe um objeto Disciplina.")
        self.__disciplina = disciplina
        self.__duracaoMinutos = ValidarInteiro(duracaoMinutos, "Duração", 1, 480)

    def GetDisciplina(self):
        return self.__disciplina

    def GetDuracaoMinutos(self):
        return self.__duracaoMinutos

    @abstractmethod
    def ObterModalidade(self):
        pass

    @abstractmethod
    def CalcularXp(self):
        pass

    def GerarFeedback(self):
        # A chamada a CalcularXp usa automaticamente a implementação da subclasse.
        return (f"{self.ObterModalidade()} em {self.__disciplina.GetNome()} "
                f"({self.__duracaoMinutos} min) -> +{self.CalcularXp()} XP")

    def ParaJson(self):
        # Nomes das chaves iguais aos DTOs do backend fornecido na aula.
        dados = {"disciplina": self.__disciplina.GetNome(),
                 "tipoModalidade": self.ObterModalidade(),
                 "duracaoMinutos": self.__duracaoMinutos,
                 "xpGanho": self.CalcularXp(), "resumoFeedback": self.GerarFeedback()}
        return json.dumps(dados, ensure_ascii=False)


class SessaoPomodoro(SessaoEstudo):
    """Estudo por ciclos de foco: minutos × 2 + ciclos × 15."""

    def __init__(self, disciplina, duracaoMinutos, ciclosCompletos=1):
        super().__init__(disciplina, duracaoMinutos)
        self.__ciclosCompletos = ValidarInteiro(ciclosCompletos, "Ciclos", 1)

    def ObterModalidade(self):
        return "Pomodoro"

    def CalcularXp(self):
        return self.GetDuracaoMinutos() * 2 + self.__ciclosCompletos * 15

    def GerarFeedback(self):
        # super reaproveita o texto da classe mãe e acrescenta o detalhe do ciclo.
        return f"{super().GerarFeedback()} | {self.__ciclosCompletos} ciclo(s) concluído(s)"


class SessaoExercicios(SessaoEstudo):
    """Listas de exercícios: minutos + acertos × 10."""

    def __init__(self, disciplina, duracaoMinutos, totalQuestoes, acertos):
        super().__init__(disciplina, duracaoMinutos)
        self.__totalQuestoes = ValidarInteiro(totalQuestoes, "Total de questões", 1)
        self.__acertos = ValidarInteiro(acertos, "Acertos", 0, self.__totalQuestoes)

    def ObterModalidade(self):
        return "Exercicios"

    def CalcularXp(self):
        return self.GetDuracaoMinutos() + self.__acertos * 10

    def GerarFeedback(self):
        percentual = self.__acertos / self.__totalQuestoes * 100
        return f"{super().GerarFeedback()} | {percentual:.0f}% de acerto"


class SessaoLeitura(SessaoEstudo):
    """Leitura: minutos + páginas × 3 + bônus de 25 quando existe resumo."""

    def __init__(self, disciplina, duracaoMinutos, paginasLidas, fezResumo=False):
        super().__init__(disciplina, duracaoMinutos)
        self.__paginasLidas = ValidarInteiro(paginasLidas, "Páginas", 1)
        if type(fezResumo) is not bool:
            raise ValueError("Fez resumo deve ser True ou False.")
        self.__fezResumo = fezResumo

    def ObterModalidade(self):
        return "Leitura"

    def CalcularXp(self):
        bonus = 25 if self.__fezResumo else 0
        return self.GetDuracaoMinutos() + self.__paginasLidas * 3 + bonus

    def GerarFeedback(self):
        resumo = "com resumo" if self.__fezResumo else "sem resumo"
        return f"{super().GerarFeedback()} | {self.__paginasLidas} página(s), {resumo}"


class SessaoHistorica(SessaoEstudo):
    """Restaura os valores já confirmados pelo servidor, sem recalcular o XP."""

    def __init__(self, dados):
        disciplina = Disciplina("HIST", dados["disciplina"], "Histórico", 2)
        super().__init__(disciplina, dados["duracaoMinutos"])
        self.__modalidade = dados["tipoModalidade"]
        self.__xp = ValidarInteiro(dados["xpGanho"], "XP do histórico")
        self.__feedback = dados["resumoFeedback"]

    def ObterModalidade(self):
        return self.__modalidade

    def CalcularXp(self):
        return self.__xp

    def GerarFeedback(self):
        return self.__feedback
