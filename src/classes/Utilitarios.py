import os
from tipos.matriz import *


class Utilitarios:

    @staticmethod
    def criar_matriz(altura: int, comprimento: int) -> TMatrizDeNumerosInteiros:
        matriz: TMatrizDeNumerosInteiros = []
        for h in range(altura):
            matriz.append([])
            for w in range(comprimento):
                matriz[h].append(0)
        return matriz

    @staticmethod
    def limpar_ecran() -> None:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def verificar_se_e_possivel_converter_para_inteiro(string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False
