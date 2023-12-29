from enum import StrEnum


class C6BankStatementColumns(StrEnum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    LAST_4_DIGITS = "Final do Cartão"
    NAME = "Nome no Cartão"
    DATE = "Data de Compra"
    CATEGORY = "Categoria"
    DESCRIPTION = "Descrição"
    INSTALLMENT = "Parcela"
    AMOUNT = "Valor (em R$)"
