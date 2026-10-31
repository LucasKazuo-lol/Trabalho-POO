"""Integração com cópia temporária do binário C#; não altera o backend original."""
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
import unittest
from tests.apoio import PastaTemporaria

from servicos.Plataforma import Plataforma
from modelos.Sessoes import SessaoExercicios, SessaoLeitura, SessaoPomodoro
from modelos.Disciplina import Disciplina
from servicos.ClienteBackendEstudo import ClienteBackendEstudo, ErroBackend


BACKEND = Path(os.environ.get("FECAP_BACKEND_DIR",
    str(Path(__file__).resolve().parents[1] / "Backend")))


@unittest.skipUnless((BACKEND / "BackendEstudoAPI.dll").exists() and shutil.which("dotnet"),
                     "Requer o backend C# da aula e .NET 10. Defina FECAP_BACKEND_DIR se necessário.")
class TestBackendReal(unittest.TestCase):
    def test_post_get_e_persistencia_apos_reiniciar(self):
        with PastaTemporaria() as pasta:
            pasta = Path(pasta)
            for arquivo in ("BackendEstudoAPI.dll", "BackendEstudoAPI.deps.json",
                            "BackendEstudoAPI.runtimeconfig.json", "MySqlConnector.dll"):
                shutil.copy2(BACKEND / arquivo, pasta / arquivo)
            with socket.socket() as porta:
                porta.bind(("127.0.0.1", 0))
                numero = porta.getsockname()[1]
            cliente = ClienteBackendEstudo(f"http://localhost:{numero}", timeout=1)
            ambiente = dict(os.environ, PORTA_BACKEND=str(numero))
            comando = ["dotnet", str(pasta / "BackendEstudoAPI.dll"), "--mysql",
                "Server=127.0.0.1;Port=1;Database=fecap_estudo;Uid=root;Pwd=;Connection Timeout=1;"]

            def iniciar(log):
                processo = subprocess.Popen(comando, cwd=pasta, env=ambiente,
                    stdout=log, stderr=subprocess.STDOUT,
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                limite = time.monotonic() + 20
                ultimo_erro = ""
                while time.monotonic() < limite:
                    try:
                        cliente.Status()
                        return processo
                    except ErroBackend as erro:
                        ultimo_erro = str(erro)
                        if processo.poll() is not None:
                            break
                        time.sleep(0.15)
                processo.terminate()
                processo.wait(timeout=5)
                self.fail("O backend C# não ficou acessível: " + ultimo_erro + "\n" +
                          (pasta / "servidor.log").read_text(errors="replace"))

            with (pasta / "servidor.log").open("w", encoding="utf-8") as log:
                processo = iniciar(log)
                try:
                    self.assertFalse(cliente.Status()["usandoMySql"])
                    nome = "Teste PBL Ágata / Python"
                    plataforma = Plataforma(cliente, nome, "Tutor Python")
                    plataforma.DefinirMeta(100)
                    disciplina = Disciplina("ADS201", "POO", "Computação", 4)
                    for sessao in (SessaoPomodoro(disciplina, 25, 1),
                                   SessaoExercicios(disciplina, 40, 10, 8),
                                   SessaoLeitura(disciplina, 30, 10, True)):
                        plataforma.RegistrarEstudo(sessao)
                    self.assertEqual(len(cliente.ListarSessoes(nome)), 3)
                    self.assertEqual(cliente.ListarMetas(nome)[0]["minutosCumpridos"], 95)
                    GerarRelatorio = cliente.GerarRelatorio(nome)
                    self.assertEqual(GerarRelatorio["xpTotal"], 270)
                    self.assertEqual(GerarRelatorio["totalMinutos"], 95)
                finally:
                    processo.terminate()
                    processo.wait(timeout=5)
                processo = iniciar(log)
                try:
                    restaurado = Plataforma(cliente, nome, "Tutor Python")
                    restaurado.CarregarHistorico()
                    restaurado.CarregarHistorico()
                    self.assertEqual(restaurado.discente.GetXpTotal(), 270)
                    self.assertEqual(restaurado.meta.GetMinutosCumpridos(), 95)
                    self.assertEqual(len(restaurado.registros), 3)
                finally:
                    processo.terminate()
                    processo.wait(timeout=5)


if __name__ == "__main__":
    unittest.main()
