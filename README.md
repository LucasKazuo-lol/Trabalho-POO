# Trabalho POO em Python — Classe Disciplina

Exercício de Programação Orientada a Objetos que representa disciplinas, converte a carga horária semanal de horas para minutos e exibe os resultados em painéis coloridos no terminal com **Rich**.

## Funcionalidades

- Classe `Disciplina` com código, nome, categoria e carga horária semanal.
- Construtor que recebe os quatro valores e assume **2 horas** se a carga for menor ou igual a zero.
- Método `CalcularCargaEmMinutos()` que retorna a carga horária multiplicada por 60.
- Método `ExibirResumo()` que retorna uma string com os dados da disciplina.
- Três objetos independentes: Full Stack, POO e Design de Interface.
- Exibição com `print` do Rich, caixas `Panel`, nome em verde e minutos em vermelho.
- Impressão da documentação da classe com `Disciplina.__doc__`.
- Código comentado em português para explicar cada parte.

## Requisitos e dependências

É necessário ter **Python 3.8 ou superior**, com `pip`. O código foi verificado com **Python 3.14.6** e **Rich 14.3.4**.

A única biblioteca externa usada diretamente pelo projeto é o **Rich**. `Panel` e `Text` fazem parte dela; não são instalações separadas. O `pip` instala automaticamente as dependências internas do Rich.

Instale a versão declarada no arquivo `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Usar `python -m pip` ajuda a instalar a biblioteca no mesmo Python utilizado para executar o programa.

Não é necessário instalar servidor, banco de dados ou extensão do VS Code para executar pelo terminal.

## Como executar

Com Git instalado, baixe o projeto:

```powershell
git clone https://github.com/LucasKazuo-lol/Trabalho-POO.git
cd Trabalho-POO
```

Também é possível baixar o ZIP pelo botão **Code → Download ZIP** no GitHub e abrir a pasta extraída no terminal.

Na pasta que contém `Disciplina.py`, execute:

```powershell
python -m pip install -r requirements.txt
python Disciplina.py
```

### Ambiente virtual no Windows — opcional

Para manter a dependência separada de outros projetos, execute na pasta do repositório:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe Disciplina.py
```

Esses comandos usam o Python do ambiente diretamente, sem precisar ativá-lo no PowerShell.

## Executar no VS Code

1. Abra a pasta `Trabalho-POO` no VS Code e abra `Disciplina.py`.
2. Com a extensão Python da Microsoft instalada, pressione **Ctrl + Shift + P** e execute **Python: Select Interpreter**.
3. Selecione o Python em que instalou o Rich. Se criou o ambiente virtual, escolha `.venv\Scripts\python.exe`.
4. Use **Run Python File in Terminal** para executar e visualizar os painéis.

Se aparecer `ModuleNotFoundError: No module named 'rich'`, o Python usado para executar o arquivo não encontrou a biblioteca. Confira o executável e a instalação:

```powershell
python -c "import sys; print(sys.executable)"
python -m pip show rich
```

Selecione esse mesmo interpretador no VS Code ou instale o `requirements.txt` usando o executável que o editor selecionou. Reinicie o terminal após trocar de ambiente.

## Estrutura de pastas e arquivos

```text
Trabalho-POO/
├── Disciplina.py     # Classe, métodos, três objetos e apresentação com Rich
├── README.md         # Explicação, dependências e instruções de execução
├── requirements.txt  # Versão do Rich utilizada pelo projeto
└── .gitignore        # Ignora ambientes virtuais e cache do Python
```

As pastas `.venv/` e `__pycache__/` podem surgir localmente durante o uso, mas são ignoradas pelo Git.

## Como o código funciona

### Classe e construtor

`Disciplina` reúne os dados de uma matéria. `__init__` recebe `codigo`, `nome`, `categoria` e `hora`. `self` representa o objeto atual. O valor de `hora` é guardado em `cargaHorariaSemanalHoras`, com correção de valores menores ou iguais a zero.

### Conversão e resumo

`CalcularCargaEmMinutos()` retorna `cargaHorariaSemanalHoras * 60`. `ExibirResumo()` chama esse cálculo e monta uma string usando f-strings. Não é preciso calcular os minutos manualmente antes de pedir o resumo.

Exemplo do texto retornado:

```text
[ADS02] Full Stack (Programação) — 4h/semana (240 min)
```

### Rich, Panel e Text

`from rich import print` fornece a impressão formatada. `Text` preserva os colchetes de `[ADS02]` como texto e aplica as cores. `Panel` desenha a caixa com título e borda azul ao redor do resumo.

`Panel` recebe um objeto `Text` já estilizado; não utiliza o argumento `markup=False`, que não faz parte da API de `Panel`.

### Programa principal

`main()` instancia os objetos `ins`, `ins2` e `ins3`. Um laço percorre a tupla de disciplinas e imprime um painel para cada uma. Ao final, `Disciplina.__doc__` apresenta a documentação da classe.

O bloco `if __name__ == "__main__":` chama `main()` somente quando o arquivo é executado diretamente. Assim, a classe pode ser importada por outros arquivos sem imprimir os exemplos.

## Resultados dos exemplos

| Objeto | Disciplina | Horas informadas | Horas utilizadas | Minutos |
|---|---|---:|---:|---:|
| `ins` | Full Stack | 4 | 4 | 240 |
| `ins2` | POO | 0 | 2 | 120 |
| `ins3` | Design de Interface | 9 | 9 | 540 |

Os resumos aparecem dentro de painéis no terminal. As cores dependem do suporte do terminal; em uma saída redirecionada para arquivo, o Rich pode removê-las automaticamente.

O exercício espera uma carga horária inteira. Os nomes, códigos e cargas dos exemplos podem ser ajustados para as disciplinas do semestre.
