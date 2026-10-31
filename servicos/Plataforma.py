from modelos.Disciplina import Disciplina
from modelos.MetaEstudo import MetaEstudo
from modelos.Relacionamentos import TrilhaEstudo
from modelos.Sessoes import SessaoHistorica
from modelos.Usuarios import Administrador, Discente, Responsavel


class Plataforma:
    """Coordena os objetos e a persistência sem colocar regras dentro da tela."""

    def __init__(self, repositorio, nome="Lucas Silva", nomeResponsavel="Carlos Silva"):
        self.repositorio = repositorio
        # Perfis de demonstração: a API do material não oferece login de usuários.
        self.discente = Discente("1", nome, "discente@fecap.br", "demo", "RA-101")
        self.responsavel = Responsavel("2", nomeResponsavel, "responsavel@exemplo.com", "demo", "Tutor")
        self.administrador = Administrador("3", "Coordenação PI", "admin@fecap.br", "demo", "Mentoria")
        self.meta = MetaEstudo(180)
        self.responsavel.DefinirMeta(self.discente, self.meta)
        self.trilha = TrilhaEstudo("Trilha do semestre", self.administrador)
        # Mesmas matérias usadas no seu script. Os objetos são criados fora da trilha.
        ins = Disciplina("ADS02", "Full Stack", "Programação", 4)
        ins2 = Disciplina("CCOMP02", "POO", "Programação", 0)
        ins3 = Disciplina("ADS04", "Design de Interface", "Design", 9)
        for disciplina in (ins, ins2, ins3):
            self.trilha.AdicionarDisciplina(disciplina)
        self.registros = []

    def CarregarHistorico(self):
        nome = self.discente.GetNome()
        registros = self.repositorio.ListarSessoes(nome)
        metas = self.repositorio.ListarMetas(nome)
        discente = Discente("1", nome, self.discente.GetEmail(), "demo", self.discente.ra)
        meta = MetaEstudo(metas[0]["metaMinutosSemana"] if metas else 180)
        # Reconstrói um objeto novo a cada GET para não duplicar o XP ao recarregar.
        for registro in registros:
            sessao = SessaoHistorica(registro)
            discente.RegistrarEstudo(sessao)
            meta.RegistrarAvanco(sessao.GetDuracaoMinutos())
        responsavel = Responsavel("2", self.responsavel.GetNome(), self.responsavel.GetEmail(), "demo", "Tutor")
        responsavel.DefinirMeta(discente, meta)
        # Só substitui o estado atual depois de validar todo o histórico.
        self.discente, self.meta, self.responsavel = discente, meta, responsavel
        self.registros = registros

    def RegistrarEstudo(self, sessao):
        # A gravação vem primeiro: uma falha HTTP não cria XP somente na memória.
        salvo = self.repositorio.SalvarSessao(self.discente.GetNome(), sessao)
        self.discente.RegistrarEstudo(sessao)
        self.meta.RegistrarAvanco(sessao.GetDuracaoMinutos())
        self.registros.append(salvo)

    def DefinirMeta(self, minutos):
        self.repositorio.SalvarMeta(self.discente.GetNome(), self.responsavel.GetNome(), minutos)
        self.meta.RedefinirMeta(minutos)
