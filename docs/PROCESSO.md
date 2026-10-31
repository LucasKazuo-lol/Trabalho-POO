# Processo do desenvolvimento — Trabalho POO

## Material e estilo utilizados

Li a seção da Aula 9 no `index.html`, incluindo cenário, arquitetura, dez missões, endpoints e checklist final. Consultei os DTOs e as rotas reais em `Backend/Source/Program.cs` para conferir os campos JSON.

Usei o script enviado como referência de escrita: construtores explícitos, atributos com nomes em português, métodos como `ExibirResumo`, comentários explicativos, f-strings, três objetos, laço de impressão, Rich, Panel e documentação da classe. As classes foram separadas por assunto para facilitar a leitura do projeto inteiro.

## Missão 1 — Disciplina

Mantive as matérias Full Stack, POO e Design de Interface. `Disciplina` recebe código, nome, categoria e carga semanal. Cargas menores ou iguais a zero assumem 2. `CalcularCargaEmMinutos` retorna horas × 60 e `ExibirResumo` retorna a string do enunciado.

O arquivo continua executável sozinho com `python -m modelos.Disciplina`. O Rich usa `Text` para preservar os colchetes do código e destacar nome e minutos antes de envolver o resultado em `Panel`.

## Missão 2 — MetaEstudo

Os minutos cumpridos e o alvo ficam privados. O construtor chama `RedefinirMeta`, que limita o alvo a 30–3000 minutos. `RegistrarAvanco` aceita apenas inteiros de 1–480 e retorna falso sem alterar o estado em casos recusados. O percentual fica limitado a 100%.

O teste de mesa do material foi incluído: -20 e 900 não somam minutos; 60 minutos em uma meta de 100 produzem 60%.

## Missão 3 — Usuario e perfis

`Usuario` usa `ABC` e não pode ser instanciado diretamente. Administrador, Responsavel e Discente implementam os métodos abstratos de perfil e resumo. Os dados comuns são privados e têm getters, exceto a senha.

A autenticação do objeto compara uma derivação PBKDF2 da senha com sal aleatório. O recurso é didático no domínio, pois a API fornecida não oferece login de servidor.

## Missão 4 — Polimorfismo das sessões

`SessaoEstudo` é abstrata e guarda a disciplina e os minutos. As três subclasses calculam seu próprio XP e feedback. Um mesmo laço percorre as sessões e chama os métodos sem testar a modalidade para calcular os pontos.

As fórmulas foram mantidas: Pomodoro usa minutos × 2 + ciclos × 15; Exercícios usa minutos + acertos × 10; Leitura usa minutos + páginas × 3 + 25 quando há resumo. O exemplo resulta em 65 + 120 + 85 = 270 XP.

## Missão 5 — Três formas de registrar

`RegistrarEstudo` recebe uma sessão pronta; disciplina e minutos; ou disciplina, hora inicial, final e páginas. Nos dois atalhos, cria a subclasse pedida e executa a mesma etapa de registro e soma de XP.

Em Python, uma única implementação reconhece os argumentos em execução. Isso adapta a intenção da sobrecarga; não representa resolução de métodos em compilação como no C#.

## Missão 6 — Interfaces

`INotificador` exige canal e envio de alerta. Painel e e-mail simulado cumprem esse contrato. Os alertas podem aparecer em um painel Rich ou em uma mensagem da interface.

`IExportavelJson` exige `ParaJson`. Metas e sessões exportam seus dados usando a biblioteca padrão `json`. A sessão usa as chaves exigidas pelo backend.

## Missão 7 — Associação e agregação

Responsavel recebe discentes criados fora dele e os guarda por identificador, sem duplicar. Também associa a meta ao discente.

TrilhaEstudo recebe disciplinas já existentes, permitindo compartilhar a mesma matéria entre trilhas. O administrador é uma associação da trilha. A soma da carga horária dos exemplos é 4 + 2 + 9 = 15 horas semanais.

## Missão 8 — Composição e dependência

PlanoEstudo cria ItemCronograma internamente. O acesso externo recebe cópias de dados, sem a lista ou as referências dos itens internos.

ServicoAlertaResponsavel recebe os objetos por parâmetro, calcula a situação da meta e usa INotificador. O serviço não guarda essas dependências em atributos.

## Missão 9 — Interface gráfica

Construí a janela Tkinter com os cabeçalhos dos perfis, formulário de estudo, campos específicos de cada modalidade, meta, barra de progresso, histórico, feedback e botão de notificação.

O botão instancia a modalidade e delega a regra aos objetos. O XP não é calculado dentro da tela. A segunda aba demonstra trilhas e cronograma. Operações de armazenamento rodam em uma thread de trabalho para manter a janela responsiva.

## Missão 10 — Backend e persistência

O modo padrão acessa o backend C# da aula. `ClienteBackendEstudo` envia POST para sessões/metas e consulta GET para status, sessões e metas. As consultas passam o parâmetro `discente` exigido pelo código real da API.

O cliente filtra o nome completo, seleciona a meta mais recente e monta o relatório com as sessões confirmadas. Isso evita misturar nomes semelhantes e compensa a possibilidade de várias metas no caminho MySQL original.

Antes de somar XP ou progresso em memória, a aplicação confirma a gravação. Para carregar, cria objetos novos a partir do histórico, impedindo duplicação de XP em GETs repetidos. `SessaoHistorica` preserva os valores gravados, porque os DTOs originais não guardam todos os parâmetros da modalidade.

Também há um modo SQLite opcional, com SQL parametrizado, para executar sem .NET ou MySQL. Esse modo não substitui a integração C# na apresentação da missão 10.

## Entrega e validação

Organizei os binários e o fonte do backend fornecido no ZIP local. A publicação no GitHub contém o código Python, documentação, inicializador e um exemplo de conexão sem senha pessoal; os arquivos recebidos do backend devem ser copiados localmente. A configuração pessoal de MySQL e os dados locais não foram publicados.

Verifiquei as regras das missões, entradas inválidas, autenticação no domínio, notificadores, JSON, relacionamentos, reabertura do SQLite e preservação do estado após falha de gravação.

O teste de interface cria uma janela Tkinter real, oculta durante a automação, executa os eventos das três modalidades e verifica histórico, XP e progresso. O teste de integração inicia uma cópia temporária do backend em outra porta, grava os estudos, encerra o processo e reinicia para confirmar a recuperação dos dados.

A integração foi testada com JSON local do backend, sem MySQL ativo. O resultado final da suíte está registrado em `VALIDACAO.json`.

## Como apresentar

1. Execute `python main.py --console` para percorrer as missões 1–8 com Rich.
2. Mostre os métodos e comentários dos arquivos relacionados a cada missão.
3. Execute `Backend/iniciar_backend.bat` e depois `python main.py`.
4. Use um nome de aluno novo para começar sem sessões anteriores e salve uma meta de 100 minutos.
5. Registre Pomodoro de 25 minutos/1 ciclo; Exercícios de 40 minutos/10 questões/8 acertos; Leitura de 30 minutos/10 páginas/com resumo.
6. Mostre 95 minutos, 270 XP e 95% da meta, consulte o feedback e notifique o responsável.
7. Exporte o relatório e feche/reabra a tela para demonstrar persistência.
8. Consulte o diagnóstico do backend e diferencie o teste em JSON da opção MySQL descrita no README.

## Organização em pacotes

As classes foram agrupadas em `modelos/`; a coordenação, comunicação HTTP e notificações em `servicos/`; a janela em `interface/`; e a demonstração Rich em `exemplos/`. A raiz mantém `main.py`, documentação e inicializadores. Os imports e o alvo de mock dos testes foram ajustados aos caminhos dos pacotes. Os caminhos do SQLite e do backend continuam ancorados na raiz do projeto.
