from modelos.Interfaces import INotificador
from servicos.Validacoes import ValidarInteiro, ValidarTexto


DIAS_SEMANA = ("Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo")


class TrilhaEstudo:
    """Agrega disciplinas que também podem existir em outras trilhas — missão 7."""

    def __init__(self, titulo, administrador):
        self.titulo = ValidarTexto(titulo, "título")
        self.administrador = administrador
        self.__disciplinas = {}

    def AdicionarDisciplina(self, disciplina):
        # Recebe um objeto criado fora, em vez de criar uma nova disciplina aqui.
        self.__disciplinas.setdefault(disciplina.GetCodigo(), disciplina)

    def GetDisciplinas(self):
        return tuple(self.__disciplinas.values())

    def CalcularCargaHorariaTotal(self):
        return sum(d.GetCargaHorariaSemanalHoras() for d in self.__disciplinas.values())


class ItemCronograma:
    def __init__(self, diaSemana, minutosPlanejados):
        if diaSemana not in DIAS_SEMANA:
            raise ValueError("Selecione um dia válido.")
        self.__diaSemana = diaSemana
        self.__minutosPlanejados = ValidarInteiro(minutosPlanejados, "Minutos planejados", 1, 480)

    def ParaDados(self):
        return {"diaSemana": self.__diaSemana, "minutosPlanejados": self.__minutosPlanejados}


class PlanoEstudo:
    """É dono dos itens que cria internamente: composição — missão 8."""

    def __init__(self):
        self.__itens = []

    def AdicionarItem(self, diaSemana, minutos):
        self.__itens.append(ItemCronograma(diaSemana, minutos))

    def ParaDados(self):
        # Só devolve cópias de valores. Ninguém recebe os objetos internos.
        return [item.ParaDados() for item in self.__itens]


class ServicoAlertaResponsavel:
    """Usa os objetos por parâmetro, sem guardá-los: dependência — missão 8."""

    def AvaliarDiscente(self, discente, meta, responsavel, notificador: INotificador):
        status = "Parabéns, meta atingida!" if meta.EstaCumprida() else "Continue acompanhando."
        mensagem = f"{discente.GetNome()}: {meta.CalcularPercentual():.1f}% da meta. {status}"
        return notificador.EnviarAlerta(responsavel.GetEmail(), mensagem)
