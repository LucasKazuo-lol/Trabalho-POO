"""SQLite independente e cliente HTTP compatível com o backend da aula."""
from __future__ import annotations

from contextlib import closing
from datetime import datetime
import json
from pathlib import Path
import sqlite3
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import ProxyHandler, Request, build_opener, urlopen

from MetaEstudo import MetaEstudo
from Sessoes import SessaoEstudo
from Validacoes import ValidarTexto


class ErroBackend(RuntimeError):
    pass


class ClienteBackendEstudo:
    def __init__(self, url_base: str = "http://localhost:5080", timeout: float = 5):
        self.url_base = url_base.rstrip("/")
        self.timeout = timeout
        partes = urlsplit(self.url_base)
        if partes.scheme not in ("http", "https") or not partes.hostname:
            raise ValueError("Informe uma URL HTTP ou HTTPS válida para o backend.")
        # Não encaminha a API da própria máquina para proxies configurados no Windows.
        self._abrir = (build_opener(ProxyHandler({})).open
                       if partes.hostname in ("localhost", "127.0.0.1", "::1") else urlopen)

    def Requisitar(self, rota: str, dados: dict | None = None):
        corpo = None if dados is None else json.dumps(dados, ensure_ascii=False).encode("utf-8")
        pedido = Request(self.url_base + rota, data=corpo,
                         headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with self._abrir(pedido, timeout=self.timeout) as resposta:
                return json.load(resposta)
        except HTTPError as erro:
            detalhe = erro.read().decode("utf-8", errors="replace")[:300]
            raise ErroBackend(f"API respondeu HTTP {erro.code}: {detalhe}") from erro
        except (URLError, TimeoutError, OSError) as erro:
            raise ErroBackend(f"Não foi possível acessar {self.url_base}. Inicie o backend. {erro}") from erro
        except (ValueError, UnicodeError) as erro:
            raise ErroBackend("O servidor retornou uma resposta JSON inválida.") from erro

    def Status(self) -> dict:
        return self.Requisitar("/api/status")

    def ListarSessoes(self, nome: str) -> list[dict]:
        # O código C# exige o parâmetro discente nas rotas GET.
        registros = self.Requisitar("/api/sessoes?" + urlencode({"discente": nome}))
        return [r for r in registros if r["discenteNome"].casefold() == nome.casefold()]

    def ListarMetas(self, nome: str) -> list[dict]:
        registros = self.Requisitar("/api/metas?" + urlencode({"discente": nome}))
        return sorted((r for r in registros if r["discenteNome"].casefold() == nome.casefold()),
                      key=lambda r: r.get("id", 0), reverse=True)

    def SalvarSessao(self, nome: str, sessao: SessaoEstudo) -> dict:
        return self.Requisitar("/api/sessoes", {"discenteNome": ValidarTexto(nome, "Discente"),
                                               **json.loads(sessao.ParaJson())})

    def SalvarMeta(self, nome: str, responsavel: str, minutos: int) -> dict:
        meta = MetaEstudo(minutos)
        return self.Requisitar("/api/metas", {"discenteNome": ValidarTexto(nome, "Discente"),
            "responsavelNome": ValidarTexto(responsavel, "Responsável"),
            "metaMinutosSemana": meta.GetMetaMinutosSemana()})

    def GerarRelatorio(self, nome: str) -> dict:
        # Consolida os GETs exatos: a rota de relatório C# usa busca parcial por nome
        # e não trata corretamente nomes contendo uma barra no parâmetro da URL.
        sessoes, metas = self.ListarSessoes(nome), self.ListarMetas(nome)
        return {"discenteNome": nome, "totalSessoes": len(sessoes),
                "totalMinutos": sum(s["duracaoMinutos"] for s in sessoes),
                "xpTotal": sum(s["xpGanho"] for s in sessoes), "metas": metas, "sessoes": sessoes}


class RepositorioSQLite:
    def __init__(self, caminho: str | Path):
        self.caminho = Path(caminho)
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with closing(self.Conectar()) as banco, banco:
            banco.executescript("""
                CREATE TABLE IF NOT EXISTS metas (
                    nome TEXT PRIMARY KEY, responsavel TEXT NOT NULL,
                    minutos INTEGER NOT NULL CHECK(minutos BETWEEN 30 AND 3000)
                );
                CREATE TABLE IF NOT EXISTS sessoes (
                    id INTEGER PRIMARY KEY, nome TEXT NOT NULL, disciplina TEXT NOT NULL,
                    modalidade TEXT NOT NULL, duracao INTEGER NOT NULL CHECK(duracao BETWEEN 1 AND 480),
                    xp INTEGER NOT NULL CHECK(xp >= 0), feedback TEXT NOT NULL, data TEXT NOT NULL
                );
            """)

    def Conectar(self):
        banco = sqlite3.connect(self.caminho, timeout=5)
        banco.row_factory = sqlite3.Row
        return banco

    def Status(self) -> dict:
        return {"online": True, "modoBanco": "SQLite local", "usandoMySql": False}

    def ListarSessoes(self, nome: str) -> list[dict]:
        with closing(self.Conectar()) as banco:
            linhas = banco.execute("SELECT * FROM sessoes WHERE nome = ? ORDER BY id", (nome,)).fetchall()
        return [{"id": r["id"], "discenteNome": r["nome"], "disciplina": r["disciplina"],
                 "tipoModalidade": r["modalidade"], "duracaoMinutos": r["duracao"],
                 "xpGanho": r["xp"], "resumoFeedback": r["feedback"], "dataRegistro": r["data"]}
                for r in linhas]

    def ListarMetas(self, nome: str) -> list[dict]:
        with closing(self.Conectar()) as banco:
            linha = banco.execute("SELECT * FROM metas WHERE nome = ?", (nome,)).fetchone()
            minutos = banco.execute("SELECT COALESCE(SUM(duracao), 0) FROM sessoes WHERE nome = ?",
                                    (nome,)).fetchone()[0]
        if linha is None:
            return []
        return [{"discenteNome": nome, "responsavelNome": linha["responsavel"],
                 "metaMinutosSemana": linha["minutos"], "minutosCumpridos": minutos}]

    def SalvarMeta(self, nome: str, responsavel: str, minutos: int) -> dict:
        nome, responsavel = ValidarTexto(nome, "Discente"), ValidarTexto(responsavel, "Responsável")
        meta = MetaEstudo(minutos)
        with closing(self.Conectar()) as banco, banco:
            banco.execute("""INSERT INTO metas VALUES (?, ?, ?)
                ON CONFLICT(nome) DO UPDATE SET responsavel=excluded.responsavel, minutos=excluded.minutos""",
                (nome, responsavel, meta.GetMetaMinutosSemana()))
        return self.ListarMetas(nome)[0]

    def SalvarSessao(self, nome: str, sessao: SessaoEstudo) -> dict:
        nome = ValidarTexto(nome, "Discente")
        dados = json.loads(sessao.ParaJson())
        data = datetime.now().astimezone().isoformat(timespec="seconds")
        with closing(self.Conectar()) as banco, banco:
            cursor = banco.execute("""INSERT INTO sessoes
                (nome, disciplina, modalidade, duracao, xp, feedback, data) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (nome, dados["disciplina"], dados["tipoModalidade"], dados["duracaoMinutos"],
                 dados["xpGanho"], dados["resumoFeedback"], data))
            id_sessao = cursor.lastrowid
        return {"id": id_sessao, "discenteNome": nome, **dados, "dataRegistro": data}

    def GerarRelatorio(self, nome: str) -> dict:
        sessoes, metas = self.ListarSessoes(nome), self.ListarMetas(nome)
        return {"discenteNome": nome, "totalSessoes": len(sessoes),
                "totalMinutos": sum(s["duracaoMinutos"] for s in sessoes),
                "xpTotal": sum(s["xpGanho"] for s in sessoes), "metas": metas, "sessoes": sessoes}
