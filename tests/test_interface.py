"""Smoke test da janela real Tkinter e dos eventos de registro/carregamento."""
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
from tests.apoio import PastaTemporaria

from interface.TelaEstudo import TelaEstudo
from servicos.ClienteBackendEstudo import RepositorioSQLite


class TestInterface(unittest.TestCase):
    def test_tela_registra_recarrega_e_atualiza_progresso(self):
        with PastaTemporaria() as pasta:
            janela = TelaEstudo(RepositorioSQLite(Path(pasta) / "ui.sqlite3"))
            janela.withdraw()
            erros = []
            try:
                with patch("interface.TelaEstudo.messagebox.showerror", side_effect=lambda *a, **k: erros.append(a)):
                    def aguardar():
                        limite = time.monotonic() + 10
                        while janela.ocupado and time.monotonic() < limite:
                            janela.update()
                            time.sleep(0.01)
                        self.assertFalse(janela.ocupado)

                    janela.update()
                    janela.CarregarHistorico()
                    aguardar()
                    # Processa também o carregamento inicial agendado pela janela.
                    limite = time.monotonic() + 0.25
                    while time.monotonic() < limite:
                        janela.update()
                        time.sleep(0.01)
                    aguardar()
                    janela.metaValor.set("100")
                    janela.SalvarMeta()
                    aguardar()
                    janela.RegistrarEstudo()
                    aguardar()
                    self.assertIn("65 XP", janela.painelDiscente.get())
                    self.assertEqual(float(janela.progresso["value"]), 25)
                    self.assertEqual(len(janela.historico.get_children()), 1)
                    janela.CarregarHistorico()
                    aguardar()
                    self.assertIn("65 XP", janela.painelDiscente.get())
                    janela.modalidade.set("Exercicios")
                    janela.TrocarModalidade()
                    janela.extra.set("8")
                    janela.duracao.set("40")
                    janela.RegistrarEstudo()
                    aguardar()
                    self.assertIn("185 XP", janela.painelDiscente.get())
                    janela.modalidade.set("Leitura")
                    janela.TrocarModalidade()
                    janela.extra.set("10")
                    janela.duracao.set("30")
                    janela.RegistrarEstudo()
                    aguardar()
                    self.assertIn("270 XP", janela.painelDiscente.get())
                    self.assertEqual(float(janela.progresso["value"]), 95)
                    self.assertEqual(len(janela.historico.get_children()), 3)
                    janela.AdicionarHorario()
                    self.assertEqual(janela.listaPlano.size(), 1)
                    self.assertEqual(erros, [])
            finally:
                janela.executor.shutdown(wait=True)
                janela.destroy()


if __name__ == "__main__":
    unittest.main()
