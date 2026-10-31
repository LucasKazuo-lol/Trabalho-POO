import json

from Interfaces import IExportavelJson


class MetaEstudo(IExportavelJson):
    """Protege a meta e controla o avanço dos estudos — missão 2."""

    def __init__(self, metaMinutosSemana=180):
        # Dois sublinhados tornam os atributos privados à classe.
        self.__minutosCumpridos = 0
        self.RedefinirMeta(metaMinutosSemana)

    def GetMetaMinutosSemana(self):
        return self.__metaMinutosSemana

    def GetMinutosCumpridos(self):
        return self.__minutosCumpridos

    def RedefinirMeta(self, novaMeta):
        if type(novaMeta) is not int:
            raise ValueError("A meta deve ser um número inteiro.")
        # A mesma validação atende tanto o construtor quanto mudanças posteriores.
        self.__metaMinutosSemana = max(30, min(3000, novaMeta))

    def RegistrarAvanco(self, minutos):
        # Dados recusados retornam False sem alterar os minutos já cumpridos.
        if type(minutos) is not int or minutos <= 0 or minutos > 480:
            return False
        self.__minutosCumpridos += minutos
        return True

    def CalcularPercentual(self):
        return min(100.0, self.__minutosCumpridos / self.__metaMinutosSemana * 100)

    def EstaCumprida(self):
        return self.__minutosCumpridos >= self.__metaMinutosSemana

    def ParaJson(self):
        # O JSON expõe uma cópia dos valores, não o acesso direto ao estado privado.
        return json.dumps({"metaMinutosSemana": self.__metaMinutosSemana,
                           "minutosCumpridos": self.__minutosCumpridos}, ensure_ascii=False)
