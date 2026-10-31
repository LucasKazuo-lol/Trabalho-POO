# Regras pequenas compartilhadas pelas classes para evitar repetir validações.
def ValidarInteiro(valor, nome, minimo=0, maximo=None):
    # type(... ) is int também recusa True/False, que Python considera números.
    if type(valor) is not int or valor < minimo:
        raise ValueError(f"{nome} deve ser um número inteiro maior ou igual a {minimo}.")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{nome} deve ser menor ou igual a {maximo}.")
    return valor


def ValidarTexto(valor, nome):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"Preencha {nome}.")
    return valor.strip()
