# O print do Rich permite exibir objetos formatados no terminal.
from rich import print

# Panel cria a caixa com título e bordas ao redor do resumo.
from rich.panel import Panel

# Text preserva os colchetes do código da disciplina e permite aplicar cores.
from rich.text import Text


class Disciplina:
    """
    Representa uma disciplina com código, nome, categoria e carga horária semanal.

    O construtor usa 2 horas quando a carga informada é menor ou igual a zero.
    Os métodos convertem a carga para minutos e retornam um resumo em texto.
    """

    def __init__(self, codigo="", nome="", categoria="", hora=2):
        # self representa o objeto que está sendo criado. Cada objeto guarda
        # seus próprios valores, sem alterar os valores das outras disciplinas.
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria

        # A expressão condicional valida a carga horária no próprio construtor.
        # Por exemplo: 4 permanece 4, enquanto 0 ou -3 se tornam 2 horas.
        if type(hora) is not int:
            raise ValueError("A carga horária deve ser um número inteiro.")
        self.cargaHorariaSemanalHoras = hora if hora > 0 else 2

    def CalcularCargaEmMinutos(self):
        """Retorna a carga semanal em minutos: cada hora equivale a 60 minutos."""
        # Retornar o resultado permite reutilizá-lo sem criar um atributo minuto.
        return self.cargaHorariaSemanalHoras * 60

    # Getters usados pelas outras classes do projeto, como nas dicas da aula.
    def GetCodigo(self):
        return self.codigo

    def GetNome(self):
        return self.nome

    def GetCategoria(self):
        return self.categoria

    def GetCargaHorariaSemanalHoras(self):
        return self.cargaHorariaSemanalHoras

    def ExibirResumo(self):
        """Retorna uma string com os dados e a carga horária da disciplina."""
        # As f-strings inserem os valores do objeto dentro do texto.
        # O cálculo é chamado aqui, sem depender de uma chamada anterior no main.
        return (
            f"[{self.codigo}] {self.nome} ({self.categoria}) — "
            f"{self.cargaHorariaSemanalHoras}h/semana "
            f"({self.CalcularCargaEmMinutos()} min)"
        )


def main():
    """Cria três disciplinas e apresenta seus resumos em painéis coloridos."""
    # Cada chamada a Disciplina(...) cria um objeto independente.
    ins = Disciplina(
        "ADS02",
        "Full Stack",
        "Programação",
        4,
    )

    # A vírgula após "POO" separa nome e categoria.
    # A carga zero demonstra a aplicação do valor padrão de 2 horas.
    ins2 = Disciplina(
        "CCOMP02",
        "POO",
        "Programação",
        0,
    )

    ins3 = Disciplina(
        "ADS04",
        "Design de Interface",
        "Design",
        9,
    )

    # O laço percorre a tupla de objetos e evita repetir a impressão três vezes.
    for disciplina in (ins, ins2, ins3):
        # Text recebe o resumo como texto literal: [ADS02] não vira uma tag.
        resumo = Text(disciplina.ExibirResumo(), style="blue")

        # Destaca o nome em verde e a carga em minutos em vermelho.
        resumo.highlight_words([disciplina.nome], style="green")
        resumo.highlight_words(
            [f"{disciplina.CalcularCargaEmMinutos()} min"],
            style="red",
        )

        # Panel recebe o texto já estilizado e adiciona título e borda azul.
        print(Panel(resumo, title="Disciplina", border_style="blue"))

    # __doc__ contém a documentação escrita entre as aspas triplas da classe.
    print(Disciplina.__doc__)


# Executa o programa ao chamar python -m modelos.Disciplina.
# Importar a classe em outro arquivo não executa as impressões automaticamente.
if __name__ == "__main__":
    main()
