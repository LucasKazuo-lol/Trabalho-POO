# Trabalho POO — FecapStudy em Python

Projeto completo da **Aula 9 — Plataforma de Apoio ao Estudo**, adaptado para Python conforme o pedido. Mantém o estilo do script inicial: classes com construtores explícitos, nomes de métodos do enunciado, comentários em português, `from rich import print`, `Panel`, cores e documentação de classe.

A aplicação oferece **tela gráfica em Tkinter**, demonstração no terminal com **Rich** e integração HTTP com o **backend C# fornecido**. O modo padrão usa esse backend, conforme a missão 10. SQLite é uma opção adicional para executar sem servidor.

## As 10 missões

| Missão | Implementação | Onde encontrar |
|---|---|---|
| 1 — Classes e objetos | Disciplina, três matérias e conversão de horas para minutos | `Disciplina.py`, `Plataforma.py` |
| 2 — Encapsulamento | Meta privada, avanço controlado e validações | `MetaEstudo.py` |
| 3 — Abstração e herança | Usuario abstrato; Administrador, Responsavel e Discente | `Usuarios.py` |
| 4 — Polimorfismo dinâmico | Pomodoro, Exercícios e Leitura com XP e feedback próprios | `Sessoes.py` |
| 5 — Sobrecarga | Três formas de chamar RegistrarEstudo | `Usuarios.py`, `Demonstracao.py` |
| 6 — Interfaces | INotificador e IExportavelJson; painel e e-mail simulado | `Interfaces.py`, `Notificadores.py` |
| 7 — Associação e agregação | Responsável/discentes e trilha/disciplinas | `Usuarios.py`, `Relacionamentos.py` |
| 8 — Composição e dependência | Plano/itens e serviço de alerta | `Relacionamentos.py` |
| 9 — Tela gráfica | Formulário, perfis, histórico, XP e barra de progresso | `TelaEstudo.py` |
| 10 — Integração | POST de sessões/metas e GET do histórico no backend C# | `ClienteBackendEstudo.py`, `Backend/` |

## Dependências

- **Python 3.10 ou superior**, com `pip` e **Tkinter**. Validado com Python 3.14.6 e Tk 8.6 no Windows.
- **Rich 14.3.4**, única biblioteca Python externa usada diretamente. `Panel` e `Text` fazem parte do Rich.
- Para o backend fornecido: **ASP.NET Core Runtime 10 para Windows x64**, ou SDK .NET 10. O SDK é necessário somente para recompilar o C#.
- **MySQL**, se quiser persistência nesse banco. Sem MySQL, o backend da aula salva automaticamente em JSON local.

`json`, `sqlite3`, `urllib`, `tkinter`, `unittest` e os demais módulos usados já fazem parte do Python. No instalador do Python para Windows, mantenha a opção de Tcl/Tk instalada. Para conferir:

```powershell
python -m tkinter
```

Instale o Rich na pasta do projeto:

```powershell
python -m pip install -r requirements.txt
```

Referência do runtime do backend: [download oficial do .NET 10](https://dotnet.microsoft.com/download/dotnet/10.0). Para verificar se está disponível:

```powershell
dotnet --list-runtimes
```

A lista precisa conter `Microsoft.AspNetCore.App 10.x` para executar a API.

## Baixar e executar o projeto completo

```powershell
git clone https://github.com/LucasKazuo-lol/Trabalho-POO.git
cd Trabalho-POO
python -m pip install -r requirements.txt
```

1. Copie para `Backend/` os arquivos fornecidos: `BackendEstudoAPI.exe`, `BackendEstudoAPI.dll`, `BackendEstudoAPI.deps.json`, `BackendEstudoAPI.runtimeconfig.json`, `BackendEstudoAPI.staticwebassets.endpoints.json` e `MySqlConnector.dll`.
2. Dê dois cliques em `Backend/iniciar_backend.bat` e mantenha o servidor aberto.
3. Consulte `http://localhost:5080` para ver o diagnóstico do banco.
4. Em outro terminal, na raiz do projeto, execute:

```powershell
python main.py
```

Também existe `iniciar_projeto.bat`. Copie os arquivos do backend fornecidos no material para `Backend/` antes de iniciar. Os executáveis, bibliotecas e código C# do material não são versionados neste repositório. O ZIP local entregue nesta conversa já os contém.

## Configurar MySQL

Se o MySQL estiver ativo e usar usuário `root` com senha vazia, o backend já tenta essa configuração padrão. Para uma configuração diferente, copie o exemplo e edite **somente a cópia local**:

```powershell
Copy-Item Backend/mysql_config.exemplo.txt Backend/mysql_config.txt
notepad Backend/mysql_config.txt
```

Formato esperado:

```text
Server=localhost;Port=3306;Database=fecap_estudo;Uid=root;Pwd=;
```

Preencha as credenciais corretas da sua instalação. O backend cria o banco e as tabelas automaticamente se o usuário tiver permissão. `banco_estudo.sql`, disponível no material da aula, serve para consulta; não é necessário executá-lo manualmente no funcionamento normal.

O diagnóstico em `http://localhost:5080` informa se a persistência atual é MySQL ou JSON. O arquivo de configuração pessoal e os dados gerados são ignorados pelo Git. A configuração pessoal original do computador não foi publicada.

## Outras formas de executar

**Demonstração das missões 1 a 8 no terminal, no estilo do script inicial:**

```powershell
python main.py --console
```

Ou use `demonstrar.bat`. A demonstração não grava sessões e não precisa de backend.

**Tela com armazenamento SQLite, sem .NET ou MySQL:**

```powershell
python main.py --local
```

Ou use `iniciar_local.bat`. O arquivo `dados/estudos.sqlite3` será criado automaticamente. Esse modo é adicional; para demonstrar a integração da missão 10, execute o modo padrão com o backend C#.

**API em outro endereço:**

```powershell
python main.py --backend http://localhost:5080
```

Os modos SQLite e API usam armazenamentos independentes e não sincronizam dados entre si.

## Como usar a tela

1. Informe o discente e o responsável. Clique em **Carregar Histórico do Servidor / Relatório** para aplicar o perfil e recuperar o histórico.
2. Salve uma meta entre 30 e 3000 minutos. Números abaixo/acima são ajustados aos limites.
3. Escolha a disciplina e a modalidade: Pomodoro, Exercicios ou Leitura.
4. Informe de 1 a 480 minutos e os dados adicionais: ciclos; acertos e total de questões; ou páginas e indicação de resumo.
5. Clique em **Registrar Estudo**. A aplicação grava primeiro e depois atualiza o XP e o progresso na tela.
6. Selecione uma sessão no histórico para ver o feedback.
7. Clique em **Notificar responsável** para visualizar a mensagem no painel ou simular um e-mail.
8. Use **Exportar relatório JSON** para salvar os dados persistidos.
9. Na segunda aba, consulte a trilha e monte os horários do cronograma.
10. Feche e reabra, usando o mesmo armazenamento e nome, para recuperar sessões, meta e XP.

Editar o nome sem clicar em carregar não troca o perfil ativo. O cabeçalho mostra quem está sendo usado no registro.

## Estrutura de pastas

```text
Trabalho-POO/
├── main.py                     # Inicia a tela ou a demonstração
├── Disciplina.py               # Missão 1; também pode rodar sozinha
├── MetaEstudo.py               # Missão 2
├── Usuarios.py                 # Missões 3, 5 e associação da 7
├── Sessoes.py                  # Missões 4 e 6
├── Interfaces.py               # Contratos da missão 6
├── Notificadores.py            # Alertas com Rich / mensagem para a tela
├── Relacionamentos.py          # Trilhas, composição e serviço de alerta
├── Plataforma.py               # Coordena os objetos e a gravação
├── ClienteBackendEstudo.py     # Cliente HTTP e alternativa SQLite
├── TelaEstudo.py               # Interface Tkinter da missão 9
├── Demonstracao.py             # Exemplos das missões 1 a 8 com Rich
├── Validacoes.py               # Validações compartilhadas
├── iniciar_projeto.bat
├── iniciar_local.bat
├── demonstrar.bat
├── requirements.txt
├── README.md
├── .gitignore
├── Backend/
│   ├── iniciar_backend.bat         # Inicializador; requer os arquivos da aula
│   ├── mysql_config.exemplo.txt    # Exemplo sem senha pessoal
│   └── README.md                   # Quais arquivos copiar do material
├── docs/
│   ├── PROCESSO.md             # Explicação do desenvolvimento e conceitos
│   └── VALIDACAO.json          # Resultado da verificação
└── tests/
    ├── apoio.py
    ├── test_pbl.py
    ├── test_interface.py
    └── test_backend_real.py
```

`dados/`, ambientes virtuais, cache do Python, arquivos fornecidos do backend e configurações pessoais não entram no Git. O ZIP local completo inclui os binários e o fonte recebidos no material; o clone do GitHub precisa recebê-los separadamente na pasta `Backend/`.

## Fórmulas de XP e exemplo

| Modalidade | Fórmula | Exemplo |
|---|---|---|
| Pomodoro | minutos × 2 + ciclos × 15 | 25 min, 1 ciclo: 65 XP |
| Exercícios | minutos + acertos × 10 | 40 min, 8 acertos: 120 XP |
| Leitura | minutos + páginas × 3 + 25 se houver resumo | 30 min, 10 páginas e resumo: 85 XP |

Resultado do exemplo: **95 minutos, 270 XP e 95% de uma meta de 100 minutos**.

As matérias do seu script foram mantidas: Full Stack, POO e Design de Interface. As cargas dos exemplos são 4, 0 e 9; a carga zero de POO é ajustada para 2 horas.

## Adaptações para Python

- O material original permite C#/JavaScript. O domínio e a tela foram adaptados para **Python**, mantendo o backend C# fornecido.
- `ABC` e `abstractmethod` representam classes abstratas e contratos.
- Python não escolhe sobrecargas em compilação como C#. `RegistrarEstudo` reconhece três combinações de argumentos em execução, como a adaptação sugerida para JavaScript na aula.
- O resumo de uma disciplina continua sendo uma string. `Panel` e `Text` cuidam da apresentação sem misturar a regra da classe com a impressão.
- A tela não calcula XP: ela instancia a modalidade e chama os objetos de domínio.

## Escopo do exercício

A tela reúne estudo e acompanhamento; os três tipos de perfil existem no domínio e na demonstração. A API fornecida não tem autenticação de servidor: `Autenticar` demonstra a regra no objeto, sem criar um login remoto. As credenciais de demonstração não são enviadas à API.

As notificações são locais e o e-mail é simulado. O cronograma permanece na execução atual; a missão 8 exige demonstrar composição, e o backend não tem uma rota de cronograma. Sessões e metas são persistidas.

Como no backend da aula, a meta tem um alvo semanal, mas o acumulado vem do histórico completo; não há reinício automático da semana. O cliente usa os minutos das sessões como fonte para o progresso.

O backend original busca trechos de nomes e, no modo MySQL, pode criar várias metas do mesmo aluno. O cliente filtra nomes completos, considera a meta de maior ID e consolida o relatório pelas sessões confirmadas. Não faz reenvio automático de POST: em caso de perda de resposta, carregue o histórico antes de tentar registrar novamente.

## Testes e validação

Na raiz do projeto:

```powershell
python -m unittest discover -s tests -v
```

A suíte verifica regras das missões, recuperação do SQLite, falha de gravação, eventos de uma janela Tkinter real e integração HTTP com uma cópia temporária do backend C#. O teste do backend usa outra porta e não altera os dados originais.

O resultado registrado está em `docs/VALIDACAO.json`. A integração real foi testada com o fallback JSON do C#; **não foi validada gravação em um MySQL ativo**. O teste da tela verifica eventos e valores dos controles; não representa uma revisão visual por captura de tela.

Sem `dotnet` ou sem os arquivos do backend, o teste de integração é ignorado. A sessão gráfica é necessária para o teste Tkinter. Em ambientes que bloqueiam conexões locais, é necessário permitir HTTP em localhost.

## Rich no VS Code

Se aparecer `No module named rich`, pressione **Ctrl + Shift + P → Python: Select Interpreter** e escolha o mesmo Python usado na instalação:

```powershell
python -c "import sys; print(sys.executable)"
python -m pip show rich
```

Depois execute **Run Python File in Terminal**. Para isolar as dependências no Windows, também pode usar:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Selecione `.venv/Scripts/python.exe` no VS Code se utilizar esse ambiente.
