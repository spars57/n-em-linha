import os
from tipos.matriz import *
from prettytable import PrettyTable


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
    def verificar_se_e_possivel_converter_para_inteiro(value: any) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def verificar_se_index_existe_na_matriz(matriz, y, x):
        try:
            matriz[y][x] = 1
            return True
        except IndexError:
            return False

    @staticmethod
    def prettytable_matriz(matriz, altura, comprimento) -> bool:
        cabecalho = ['']
        linhas = []
        for x in range(comprimento):
            cabecalho.append(x + 1)
        for y in range(altura):
            linha = []
            for x in range(comprimento):
                match matriz[y][x]:
                    case 1:
                        linha.append("\U0001F534")
                    case 2:
                        linha.append("\U0001F7E1")
                    case 3:
                        linha.append("\U0001F7E2")
                    case default:
                        linha.append("\U000026AB")
            linha.insert(0, y + 1)
            linhas.append(linha)
        tab = PrettyTable(cabecalho)
        tab.add_rows(linhas)
        print(tab)
        return True
