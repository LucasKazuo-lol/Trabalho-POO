"""Regras das missões, recuperação de dados e proteção contra falhas de gravação."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tests.apoio import PastaTemporaria
from servicos.ClienteBackendEstudo import ClienteBackendEstudo, ErroBackend, RepositorioSQLite
from modelos.Disciplina import Disciplina
from modelos.MetaEstudo import MetaEstudo
from servicos.Notificadores import NotificadorEmail, NotificadorPainel
from servicos.Plataforma import Plataforma
from modelos.Relacionamentos import PlanoEstudo, ServicoAlertaResponsavel, TrilhaEstudo
from modelos.Sessoes import SessaoEstudo, SessaoPomodoro, SessaoExercicios, SessaoLeitura
from modelos.Usuarios import Usuario, Administrador, Responsavel, Discente


class TestPBL(unittest.TestCase):
    def setUp(self):
        self.disciplina = Disciplina("ADS201", "POO", "Computação", 4)

    def Aluno(self):
        return Discente("1", "Ana", "ana@exemplo.com", "segredo", "101")

    def test_disciplina_e_resumo_do_enunciado(self):
        self.assertEqual(self.disciplina.CalcularCargaEmMinutos(), 240)
        for carga in (0, -4):
            self.assertEqual(Disciplina("X", "Teste", "Computação", carga).CalcularCargaEmMinutos(), 120)
        self.assertEqual(self.disciplina.ExibirResumo(), "[ADS201] POO (Computação) — 4h/semana (240 min)")

    def test_meta_recusa_avancos_e_limita_percentual(self):
        meta = MetaEstudo(100)
        for minutos in (-20, 900, 0, True, 1.5):
            self.assertFalse(meta.RegistrarAvanco(minutos))
        self.assertEqual(meta.GetMinutosCumpridos(), 0)
        meta.RegistrarAvanco(60)
        self.assertEqual(meta.CalcularPercentual(), 60)
        meta.RegistrarAvanco(60)
        self.assertEqual(meta.CalcularPercentual(), 100)
        self.assertTrue(meta.EstaCumprida())
        meta.RedefinirMeta(-1)
        self.assertEqual(meta.GetMetaMinutosSemana(), 30)
        meta.RedefinirMeta(9999)
        self.assertEqual(meta.GetMetaMinutosSemana(), 3000)
        self.assertFalse(hasattr(meta, "SetMinutosCumpridos"))

    def test_classe_abstrata_perfis_e_senha_privada(self):
        with self.assertRaises(TypeError):
            Usuario("1", "Ana", "ana@exemplo.com", "x")
        aluno = self.Aluno()
        self.assertTrue(aluno.Autenticar("segredo"))
        self.assertFalse(aluno.Autenticar("erro"))
        self.assertFalse(hasattr(aluno, "GetSenha"))
        perfis = [aluno, Responsavel("2", "Bia", "bia@exemplo.com", "x", "Tutor"),
                  Administrador("3", "Caio", "caio@exemplo.com", "x", "Mentor")]
        self.assertEqual([p.ObterTipoPerfil() for p in perfis], ["Discente", "Responsavel", "Administrador"])

    def test_formulas_polimorficas_e_feedback(self):
        sessoes = [SessaoPomodoro(self.disciplina, 25, 1),
                   SessaoExercicios(self.disciplina, 40, 10, 8),
                   SessaoLeitura(self.disciplina, 30, 10, True)]
        self.assertEqual([s.CalcularXp() for s in sessoes], [65, 120, 85])
        self.assertIn("80%", sessoes[1].GerarFeedback())
        self.assertEqual(SessaoLeitura(self.disciplina, 30, 10, False).CalcularXp(), 60)
        with self.assertRaises(TypeError):
            SessaoEstudo(self.disciplina, 25)

    def test_sessoes_invalidas_nao_geram_estudos(self):
        for minutos in (-1, 0, 481, True):
            with self.assertRaises(ValueError):
                SessaoPomodoro(self.disciplina, minutos, 1)
        for total, acertos in ((0, 0), (10, -1), (10, 11)):
            with self.assertRaises(ValueError):
                SessaoExercicios(self.disciplina, 25, total, acertos)

    def test_tres_formas_de_registro(self):
        aluno = self.Aluno()
        aluno.RegistrarEstudo(SessaoPomodoro(self.disciplina, 25, 1))
        aluno.RegistrarEstudo(self.disciplina, 50)
        aluno.RegistrarEstudo(self.disciplina, 14, 15, 10)
        self.assertEqual(aluno.GetXpTotal(), 310)
        self.assertEqual(len(aluno.GetHistorico()), 3)
        with self.assertRaises(ValueError):
            aluno.RegistrarEstudo(self.disciplina, 15, 14, 10)
        self.assertEqual(aluno.GetXpTotal(), 310)

    def test_interfaces_json_e_alerta(self):
        meta = MetaEstudo(30)
        meta.RegistrarAvanco(30)
        self.assertEqual(json.loads(meta.ParaJson())["minutosCumpridos"], 30)
        sessao = SessaoPomodoro(self.disciplina, 25, 1)
        self.assertEqual(json.loads(sessao.ParaJson())["xpGanho"], 65)
        responsavel = Responsavel("2", "Bia", "bia@exemplo.com", "x", "Tutor")
        for canal in (NotificadorPainel(False), NotificadorEmail(False)):
            self.assertTrue(ServicoAlertaResponsavel().AvaliarDiscente(self.Aluno(), meta, responsavel, canal))
            self.assertIn("Parabéns", canal.GetMensagens()[-1])

    def test_associacao_e_agregacao_sem_duplicatas(self):
        aluno = self.Aluno()
        resp = Responsavel("2", "Bia", "bia@exemplo.com", "x", "Tutor")
        resp.VincularDiscente(aluno)
        resp.VincularDiscente(aluno)
        self.assertEqual(len(resp.GetDiscentes()), 1)
        admin = Administrador("3", "Caio", "caio@exemplo.com", "x", "Mentor")
        a, b = TrilhaEstudo("A", admin), TrilhaEstudo("B", admin)
        for trilha in (a, a, b):
            trilha.AdicionarDisciplina(self.disciplina)
        self.assertIs(a.GetDisciplinas()[0], b.GetDisciplinas()[0])
        self.assertEqual(a.CalcularCargaHorariaTotal(), 4)

    def test_composicao_devolve_copias(self):
        plano = PlanoEstudo()
        plano.AdicionarItem("Segunda", 60)
        copia = plano.ParaDados()
        copia[0]["minutosPlanejados"] = -1
        copia.clear()
        self.assertEqual(plano.ParaDados()[0]["minutosPlanejados"], 60)

    def test_sqlite_reabre_e_nao_duplica_xp_ao_recarregar(self):
        with PastaTemporaria() as pasta:
            caminho = Path(pasta) / "estudos.sqlite3"
            app = Plataforma(RepositorioSQLite(caminho), "Ana", "Bia")
            app.DefinirMeta(100)
            app.RegistrarEstudo(SessaoPomodoro(self.disciplina, 25, 1))
            novo = Plataforma(RepositorioSQLite(caminho), "Ana", "Bia")
            for _ in range(3):
                novo.CarregarHistorico()
                self.assertEqual(novo.discente.GetXpTotal(), 65)
                self.assertEqual(novo.meta.GetMinutosCumpridos(), 25)
                self.assertEqual(novo.meta.CalcularPercentual(), 25)
            novo.DefinirMeta(200)
            novo.CarregarHistorico()
            self.assertEqual(novo.meta.GetMinutosCumpridos(), 25)
            self.assertEqual(novo.meta.CalcularPercentual(), 12.5)

    def test_falha_de_gravacao_nao_altera_memoria(self):
        with PastaTemporaria() as pasta:
            repo = RepositorioSQLite(Path(pasta) / "estudos.sqlite3")
            app = Plataforma(repo, "Ana", "Bia")
            with patch.object(repo, "SalvarSessao", side_effect=ErroBackend("Offline")):
                with self.assertRaises(ErroBackend):
                    app.RegistrarEstudo(SessaoPomodoro(self.disciplina, 25, 1))
            self.assertEqual(app.discente.GetXpTotal(), 0)
            self.assertEqual(app.meta.GetMinutosCumpridos(), 0)

    def test_cliente_filtra_nome_exato_e_meta_mais_recente(self):
        cliente = ClienteBackendEstudo()
        with patch.object(cliente, "Requisitar", return_value=[
            {"discenteNome": "Ana", "id": 1}, {"discenteNome": "Ana Maria", "id": 2},
            {"discenteNome": "Ana", "id": 3}]):
            self.assertEqual(len(cliente.ListarSessoes("Ana")), 2)
            self.assertEqual(cliente.ListarMetas("Ana")[0]["id"], 3)


if __name__ == "__main__":
    unittest.main()
