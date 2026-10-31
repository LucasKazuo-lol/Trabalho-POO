"""Interface Tkinter: captura dados e delega regras ao domínio."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# As regras ficam nas classes; os eventos apenas leem os campos e chamam métodos.
from servicos.Plataforma import Plataforma
from modelos.Relacionamentos import DIAS_SEMANA, PlanoEstudo, ServicoAlertaResponsavel
from servicos.Notificadores import NotificadorEmail, NotificadorPainel
from modelos.Sessoes import SessaoExercicios, SessaoLeitura, SessaoPomodoro


class TelaEstudo(tk.Tk):
    def __init__(self, repositorio):
        super().__init__()
        self.title("FecapStudy • Plataforma de Apoio ao Estudo")
        self.geometry("1100x800")
        self.minsize(900, 700)
        self.configure(background="#eef5f1")
        self.repositorio = repositorio
        self.plataforma = Plataforma(repositorio, "Lucas Silva", "Carlos Silva")
        self.plano = PlanoEstudo()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.ocupado = False
        self.botoes = []
        self.protocol("WM_DELETE_WINDOW", self.Fechar)
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#eef5f1")
        estilo.configure("TLabel", background="#eef5f1", foreground="#153e30", font=("Segoe UI", 10))
        estilo.configure("TLabelframe", background="#eef5f1")
        estilo.configure("TLabelframe.Label", background="#eef5f1", foreground="#153e30")
        estilo.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))
        estilo.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.configure("TProgressbar", background="#008754", troughcolor="#d4e4db")
        self.MontarTela()
        self.after(150, self.CarregarHistorico)

    def CriarBotao(self, pai, texto, comando):
        botao = ttk.Button(pai, text=texto, command=comando)
        self.botoes.append(botao)
        return botao

    def MontarTela(self):
        topo = tk.Frame(self, bg="#023327", padx=24, pady=15)
        topo.pack(fill="x")
        tk.Label(topo, text="FecapStudy", bg="#023327", fg="#00e387",
                 font=("Segoe UI", 25, "bold")).pack(anchor="w")
        tk.Label(topo, text="Seu estudo com foco, progresso e acompanhamento.",
                 bg="#023327", fg="white", font=("Segoe UI", 11)).pack(anchor="w")
        corpo = ttk.Frame(self, padding=18)
        corpo.pack(fill="both", expand=True)
        perfil = ttk.Frame(corpo)
        perfil.pack(fill="x", pady=(0, 12))
        self.nome = tk.StringVar(value="Lucas Silva")
        self.responsavel = tk.StringVar(value="Carlos Silva")
        ttk.Label(perfil, text="Discente").grid(row=0, column=0, sticky="w")
        ttk.Label(perfil, text="Responsável").grid(row=0, column=1, sticky="w", padx=10)
        self.nomeEntry = ttk.Entry(perfil, textvariable=self.nome, width=30)
        self.nomeEntry.grid(row=1, column=0)
        self.respEntry = ttk.Entry(perfil, textvariable=self.responsavel, width=30)
        self.respEntry.grid(row=1, column=1, padx=10)
        self.CriarBotao(perfil, "Carregar Histórico do Servidor / Relatório", self.CarregarHistorico).grid(row=1, column=2)
        self.painelDiscente = tk.StringVar()
        self.painelResponsavel = tk.StringVar()
        ttk.Label(corpo, textvariable=self.painelDiscente, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(corpo, textvariable=self.painelResponsavel).pack(anchor="w", pady=(2, 10))
        self.abas = ttk.Notebook(corpo)
        self.abas.pack(fill="both", expand=True)
        estudo = ttk.Frame(self.abas, padding=14)
        trilha = ttk.Frame(self.abas, padding=14)
        self.abas.add(estudo, text="Estudos e metas")
        self.abas.add(trilha, text="Trilha e cronograma")
        self.MontarEstudos(estudo)
        self.MontarTrilha(trilha)
        self.statusTexto = tk.StringVar(value="Iniciando…")
        ttk.Label(corpo, textvariable=self.statusTexto, wraplength=1000).pack(anchor="w", pady=(12, 0))
        self.AtualizarTela()

    # Formulário, meta, barra de progresso e histórico da missão 9.
    def MontarEstudos(self, pai):
        formulario = ttk.LabelFrame(pai, text="Nova sessão de estudo", padding=12)
        formulario.pack(fill="x")
        self.disciplina = tk.StringVar(value=self.plataforma.trilha.GetDisciplinas()[0].GetNome())
        self.modalidade = tk.StringVar(value="Pomodoro")
        self.duracao = tk.StringVar(value="25")
        self.extra = tk.StringVar(value="1")
        self.questoes = tk.StringVar(value="10")
        self.resumo = tk.BooleanVar(value=True)
        self.discCombo = ttk.Combobox(formulario, textvariable=self.disciplina, state="readonly",
            width=34, values=[d.GetNome() for d in self.plataforma.trilha.GetDisciplinas()])
        self.modalCombo = ttk.Combobox(formulario, textvariable=self.modalidade, state="readonly",
            width=16, values=("Pomodoro", "Exercicios", "Leitura"))
        self.extraLabel = ttk.Label(formulario, text="Ciclos completos")
        self.totalLabel = ttk.Label(formulario, text="Total de questões")
        self.totalEntry = ttk.Entry(formulario, textvariable=self.questoes, width=15)
        self.resumoCheck = ttk.Checkbutton(formulario, text="Fiz resumo", variable=self.resumo)
        campos = (("Disciplina", self.discCombo), ("Modalidade", self.modalCombo),
                  ("Duração (1–480 min)", ttk.Entry(formulario, textvariable=self.duracao, width=18)))
        for coluna, (rotulo, widget) in enumerate(campos):
            ttk.Label(formulario, text=rotulo).grid(row=0, column=coluna, sticky="w", padx=(0, 12))
            widget.grid(row=1, column=coluna, sticky="w", padx=(0, 12), pady=(4, 12))
        self.extraLabel.grid(row=2, column=0, sticky="w")
        ttk.Entry(formulario, textvariable=self.extra, width=18).grid(row=3, column=0, sticky="w")
        self.totalLabel.grid(row=2, column=1, sticky="w")
        self.totalEntry.grid(row=3, column=1, sticky="w")
        self.resumoCheck.grid(row=3, column=1, sticky="w")
        self.CriarBotao(formulario, "Registrar Estudo", self.RegistrarEstudo).grid(row=3, column=2, sticky="w")
        self.modalCombo.bind("<<ComboboxSelected>>", lambda _: self.TrocarModalidade())
        self.TrocarModalidade()
        metas = ttk.Frame(pai)
        metas.pack(fill="x", pady=14)
        self.metaValor = tk.StringVar(value="180")
        ttk.Label(metas, text="Meta semanal (30–3000 min)").pack(side="left")
        ttk.Entry(metas, textvariable=self.metaValor, width=8).pack(side="left", padx=8)
        self.CriarBotao(metas, "Salvar meta", self.SalvarMeta).pack(side="left")
        self.progressoTexto = tk.StringVar()
        ttk.Label(pai, textvariable=self.progressoTexto).pack(anchor="w")
        self.progresso = ttk.Progressbar(pai, maximum=100)
        self.progresso.pack(fill="x", pady=(5, 12))
        colunas = ("data", "modalidade", "minutos", "xp", "disciplina")
        tabela = ttk.Frame(pai)
        tabela.pack(fill="both", expand=True)
        self.historico = ttk.Treeview(tabela, columns=colunas, show="headings", height=6)
        for coluna, titulo, largura in zip(colunas,
            ("Data", "Modalidade", "Minutos", "XP", "Disciplina"), (165, 110, 70, 60, 300)):
            self.historico.heading(coluna, text=titulo)
            self.historico.column(coluna, width=largura, minwidth=50)
        barra = ttk.Scrollbar(tabela, orient="vertical", command=self.historico.yview)
        self.historico.configure(yscrollcommand=barra.set)
        self.historico.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        self.feedback = tk.StringVar(value="Selecione uma sessão para ver o feedback.")
        self.historico.bind("<<TreeviewSelect>>", self.SelecionarFeedback)
        ttk.Label(pai, textvariable=self.feedback, wraplength=940).pack(anchor="w", pady=8)
        acoes = ttk.Frame(pai)
        acoes.pack(fill="x")
        self.CriarBotao(acoes, "Notificar responsável", self.NotificarResponsavel).pack(side="left")
        self.canal = tk.StringVar(value="Painel")
        ttk.Combobox(acoes, textvariable=self.canal, state="readonly", width=19,
                     values=("Painel", "E-mail (simulado)")).pack(side="left", padx=8)
        self.CriarBotao(acoes, "Exportar relatório JSON", self.ExportarRelatorio).pack(side="right")

    def MontarTrilha(self, pai):
        ttk.Label(pai, text=self.plataforma.administrador.GerarPainelResumo(),
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 15))
        for disciplina in self.plataforma.trilha.GetDisciplinas():
            ttk.Label(pai, text=disciplina.ExibirResumo(), wraplength=900).pack(anchor="w", pady=6)
        ttk.Label(pai, text=f"Carga total da trilha: {self.plataforma.trilha.CalcularCargaHorariaTotal()} h/semana",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=12)
        ttk.Separator(pai).pack(fill="x", pady=12)
        ttk.Label(pai, text="Cronograma pessoal (mantido nesta execução)").pack(anchor="w")
        linha = ttk.Frame(pai)
        linha.pack(fill="x", pady=10)
        self.dia = tk.StringVar(value="Segunda")
        self.planejados = tk.StringVar(value="60")
        ttk.Combobox(linha, textvariable=self.dia, values=DIAS_SEMANA,
                     state="readonly", width=12).pack(side="left")
        ttk.Label(linha, text="Minutos").pack(side="left", padx=8)
        ttk.Entry(linha, textvariable=self.planejados, width=8).pack(side="left")
        self.CriarBotao(linha, "Adicionar horário", self.AdicionarHorario).pack(side="left", padx=8)
        self.listaPlano = tk.Listbox(pai, height=7, font=("Segoe UI", 11))
        self.listaPlano.pack(fill="both", expand=True)

    def TrocarModalidade(self):
        tipo = self.modalidade.get()
        self.extraLabel.configure(text={"Pomodoro": "Ciclos completos", "Exercicios": "Acertos",
                                         "Leitura": "Páginas lidas"}[tipo])
        for widget in (self.totalLabel, self.totalEntry, self.resumoCheck):
            widget.grid_remove()
        if tipo == "Exercicios":
            self.totalLabel.grid()
            self.totalEntry.grid()
        elif tipo == "Leitura":
            self.resumoCheck.grid()

    # I/O em outra thread mantém a janela responsiva enquanto a API responde.
    def Executar(self, operacao, sucesso):
        if self.ocupado:
            return
        self.ocupado = True
        for botao in self.botoes:
            botao.state(["disabled"])
        self.statusTexto.set("Aguarde, acessando o armazenamento…")
        tarefa = self.executor.submit(operacao)

        def verificar():
            if not tarefa.done():
                self.after(80, verificar)
                return
            self.ocupado = False
            for botao in self.botoes:
                botao.state(["!disabled"])
            try:
                sucesso(tarefa.result())
            except Exception as erro:
                self.statusTexto.set("Operação não concluída. Veja a mensagem de erro.")
                messagebox.showerror("FecapStudy", str(erro), parent=self)
        self.after(80, verificar)

    def CarregarHistorico(self):
        try:
            plataforma = Plataforma(self.repositorio, self.nome.get(), self.responsavel.get())
        except ValueError as erro:
            messagebox.showerror("Perfil inválido", str(erro), parent=self)
            return

        def ler():
            status = self.repositorio.Status()
            plataforma.CarregarHistorico()
            return plataforma, status

        def pronto(resultado):
            self.plataforma, status = resultado
            modo = status.get("modoBanco") or ("MySQL" if status.get("usandoMySql") else "JSON do backend C#")
            self.statusTexto.set(f"Histórico carregado • {modo}")
            self.AtualizarTela()
        self.Executar(ler, pronto)

    # O botão cria a subclasse escolhida; o domínio calcula o XP.
    def RegistrarEstudo(self):
        try:
            disciplina = next(d for d in self.plataforma.trilha.GetDisciplinas() if d.GetNome() == self.disciplina.get())
            duracao, extra = int(self.duracao.get()), int(self.extra.get())
            tipo = self.modalidade.get()
            if tipo == "Pomodoro":
                sessao = SessaoPomodoro(disciplina, duracao, extra)
            elif tipo == "Exercicios":
                sessao = SessaoExercicios(disciplina, duracao, int(self.questoes.get()), extra)
            else:
                sessao = SessaoLeitura(disciplina, duracao, extra, self.resumo.get())
        except (ValueError, StopIteration) as erro:
            messagebox.showerror("Confira os campos", str(erro) or "Selecione uma disciplina.", parent=self)
            return

        def pronto(_):
            self.AtualizarTela()
            self.feedback.set(sessao.GerarFeedback())
            self.statusTexto.set("Sessão gravada. XP e progresso atualizados.")
        self.Executar(lambda: self.plataforma.RegistrarEstudo(sessao), pronto)

    def SalvarMeta(self):
        try:
            minutos = int(self.metaValor.get())
        except ValueError:
            messagebox.showerror("Meta inválida", "Digite um número inteiro de minutos.", parent=self)
            return

        def pronto(_):
            self.AtualizarTela()
            self.statusTexto.set("Meta salva (valores ajustados para o intervalo de 30 a 3000 min).")
        self.Executar(lambda: self.plataforma.DefinirMeta(minutos), pronto)

    def AtualizarTela(self):
        p = self.plataforma
        self.painelDiscente.set(p.discente.GerarPainelResumo())
        self.painelResponsavel.set(p.responsavel.GerarPainelResumo())
        self.metaValor.set(str(p.meta.GetMetaMinutosSemana()))
        self.progresso["value"] = p.meta.CalcularPercentual()
        self.progressoTexto.set(f"{p.meta.GetMinutosCumpridos()} / {p.meta.GetMetaMinutosSemana()} minutos "
                                f"• {p.meta.CalcularPercentual():.1f}% da meta")
        self.historico.delete(*self.historico.get_children())
        for indice, r in enumerate(p.registros):
            self.historico.insert("", 0, iid=str(indice), values=(r.get("dataRegistro", ""),
                r["tipoModalidade"], r["duracaoMinutos"], r["xpGanho"], r["disciplina"]))

    def SelecionarFeedback(self, _):
        selecionado = self.historico.selection()
        if selecionado:
            self.feedback.set(self.plataforma.registros[int(selecionado[0])]["resumoFeedback"])

    def NotificarResponsavel(self):
        notificador = NotificadorPainel() if self.canal.get() == "Painel" else NotificadorEmail()
        p = self.plataforma
        ServicoAlertaResponsavel().AvaliarDiscente(p.discente, p.meta, p.responsavel, notificador)
        messagebox.showinfo(notificador.ObterCanal(), notificador.GetMensagens()[-1], parent=self)

    def AdicionarHorario(self):
        try:
            self.plano.AdicionarItem(self.dia.get(), int(self.planejados.get()))
        except ValueError as erro:
            messagebox.showerror("Horário inválido", str(erro), parent=self)
            return
        self.listaPlano.delete(0, "end")
        for item in self.plano.ParaDados():
            self.listaPlano.insert("end", f"{item['diaSemana']} • {item['minutosPlanejados']} minutos")

    def ExportarRelatorio(self):
        caminho = filedialog.asksaveasfilename(parent=self, title="Salvar relatório",
            defaultextension=".json", initialfile="relatorio_estudo.json",
            filetypes=[("JSON", "*.json")])
        if not caminho:
            return

        def pronto(relatorio):
            Path(caminho).write_text(json.dumps(relatorio, ensure_ascii=False, indent=2), encoding="utf-8")
            self.statusTexto.set(f"Relatório exportado: {caminho}")
        nome = self.plataforma.discente.GetNome()
        self.Executar(lambda: self.repositorio.GerarRelatorio(nome), pronto)

    def Fechar(self):
        if self.ocupado:
            messagebox.showinfo("Aguarde", "Aguarde a conclusão da operação antes de fechar.", parent=self)
            return
        self.executor.shutdown(wait=False, cancel_futures=True)
        self.destroy()
