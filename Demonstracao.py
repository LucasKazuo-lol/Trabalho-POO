"""Demonstração das missões 1 a 8 no seu estilo, com print e Panel do Rich."""
from rich import print
from rich.panel import Panel
from rich.text import Text

from MetaEstudo import MetaEstudo
from Notificadores import NotificadorEmail, NotificadorPainel
from Plataforma import Plataforma
from Relacionamentos import PlanoEstudo, ServicoAlertaResponsavel
from Sessoes import SessaoPomodoro, SessaoExercicios, SessaoLeitura
from Usuarios import Discente


def Demonstrar():
    # Nenhum banco é aberto: None indica que a demonstração usa só os objetos.
    plataforma = Plataforma(None)
    disciplinas = plataforma.trilha.GetDisciplinas()
    for disciplina in disciplinas:
        print(Panel(Text(disciplina.ExibirResumo(), style="green"), title="Missão 1 — Disciplina", border_style="blue"))

    # Teste de mesa obrigatório da missão 2.
    meta = MetaEstudo(100)
    for minutos in (-20, 900):
        aceito = meta.RegistrarAvanco(minutos)
        print(f"Avanço de {minutos} minutos: {aceito} | acumulado: {meta.GetMinutosCumpridos()}")
    meta.RegistrarAvanco(60)
    print(Panel(f"Meta de 100 minutos: {meta.CalcularPercentual():.0f}% após 60 minutos", title="Missão 2"))

    # Uma coleção de usuários diferentes responde ao mesmo método abstrato.
    for usuario in (plataforma.administrador, plataforma.responsavel, plataforma.discente):
        print(Panel(Text(usuario.GerarPainelResumo(), style="green"), title="Missão 3 — Perfil"))

    # As fórmulas estão nas subclasses; o laço não testa qual é a modalidade.
    sessoes = [SessaoPomodoro(disciplinas[0], 25, 1),
               SessaoExercicios(disciplinas[1], 40, 10, 8),
               SessaoLeitura(disciplinas[2], 30, 10, True)]
    meta = MetaEstudo(100)
    for sessao in sessoes:
        plataforma.discente.RegistrarEstudo(sessao)
        meta.RegistrarAvanco(sessao.GetDuracaoMinutos())
        print(Panel(Text(sessao.GerarFeedback(), style="green"), title="Missão 4 — Sessão"))

    # Três formas de chamada da missão 5, em outro aluno para não misturar os exemplos.
    aluno = Discente("4", "Exemplo de sobrecarga", "exemplo@fecap.br", "demo", "RA-102")
    aluno.RegistrarEstudo(sessoes[0])
    aluno.RegistrarEstudo(disciplinas[0], 50)
    aluno.RegistrarEstudo(disciplinas[0], 14, 15, 10)
    print(Panel(f"Três registros: {aluno.GetXpTotal()} XP", title="Missão 5 — Sobrecarga adaptada"))

    print(Panel(Text(meta.ParaJson()), title="Missão 6 — Exportação JSON"))
    print(Panel(f"Trilha: {plataforma.trilha.CalcularCargaHorariaTotal()}h/semana", title="Missão 7 — Agregação"))
    plano = PlanoEstudo()
    plano.AdicionarItem("Segunda", 25)
    plano.AdicionarItem("Quarta", 40)
    plano.AdicionarItem("Sexta", 30)
    print(Panel(Text(str(plano.ParaDados())), title="Missão 8 — Composição"))
    for notificador in (NotificadorPainel(), NotificadorEmail()):
        ServicoAlertaResponsavel().AvaliarDiscente(plataforma.discente, meta, plataforma.responsavel, notificador)

    print(Panel(f"{meta.GetMinutosCumpridos()} minutos | {plataforma.discente.GetXpTotal()} XP | "
                f"{meta.CalcularPercentual():.0f}% da meta", title="Resultado", border_style="green"))
    print(plataforma.discente.__class__.__doc__)


if __name__ == "__main__":
    Demonstrar()
