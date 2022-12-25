import json
from json.decoder import JSONDecodeError
import os
from tipos.matriz import *
from prettytable import PrettyTable
from Informador import *
from ListaDeJogadores import *
from Jogador import *


class Utilitarios:
    def __init__(self):
        self.informador: Informador = Informador()

    @staticmethod
    def criar_matriz(altura: int, comprimento: int) -> MatrizDeNumerosInterios:
        matriz: MatrizDeNumerosInterios = []
        h: int
        for h in range(altura):
            matriz.append([])
            w: int
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

    def prettytable_matriz(self, matriz, altura, comprimento) -> bool:
        try:
            cabecalho = ['']
            linhas = []
            x: int
            for x in range(comprimento):
                cabecalho.append(x + 1)
            y: int
            for y in range(altura):
                linha = []
                for x in range(comprimento):
                    match matriz[y][x]:
                        # Circulo Vermelho
                        case 1:
                            linha.append("\U0001F534")
                        # Circulo Amarelo
                        case 2:
                            linha.append("\U0001F7E1")
                        # Circulo Verde
                        case 3:
                            linha.append("\U0001F7E2")
                        # Circulo Preto
                        case default:
                            linha.append("\U000026AB")
                linha.insert(0, y + 1)
                linhas.append(linha)
            tab = PrettyTable(cabecalho)
            tab.add_rows(linhas)
            self.informador.predefinicao(tab)
        except TypeError:
            return False
        except IndexError:
            return False
        return True

    @staticmethod
    def verificar_se_e_json(nome_ficheiro: str) -> bool:
        try:
            ficheiro = open(nome_ficheiro, 'r')
            json.load(ficheiro)
            return True
        except JSONDecodeError:
            return False

    @staticmethod
    def adicionar_jogador_a_lista_de_jogadores(lista_de_jogadores: ListaDeJogadores, jogador: Jogador) -> bool:
        if lista_de_jogadores.obter_por_nome(jogador.nome):
            return False
        lista_de_jogadores.adicionar_jogador(jogador)
        return True

    def finalizar_instrucao(self) -> None:
        """Esta função será executada no final de cada instrução"""
        input('\nClique ENTER para continuar e limpar o ecran.')
        self.limpar_ecran()

    def inicializar_instrucao(self) -> None:
        """Esta função será executada antes de cada instrução"""
        self.limpar_ecran()

    def imprimir_menu(self) -> None:
        self.informador.predefinicao('--------------------------------------------')
        self.informador.predefinicao('Jogo do N em Linha:')
        self.informador.predefinicao('---Jogadores--------------------------------')
        self.informador.predefinicao('EJ - Eliminar')
        self.informador.predefinicao('LJ - Lista')
        self.informador.predefinicao('RJ - Registar')
        self.informador.predefinicao('---Jogo-------------------------------------')
        self.informador.predefinicao('CP - Colocar Peca')
        self.informador.predefinicao('D  - Desitir')
        self.informador.predefinicao('DJ - Detalhes')
        self.informador.predefinicao('IJ - Iniciar')
        self.informador.predefinicao('V  - Visualizar')
        self.informador.predefinicao('---Dados------------------------------------')
        self.informador.predefinicao('G  - Guardar')
        self.informador.predefinicao('L  - Ler')
        self.informador.predefinicao('---Outros--Comandos-------------------------')
        self.informador.predefinicao('AJUDA - Guia de como usar os comandos')
        self.informador.predefinicao('SAIR - Sair do Jogo')
        self.informador.predefinicao('--------------------------------------------')
