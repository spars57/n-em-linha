import os
from json.decoder import JSONDecodeError
from prettytable import PrettyTable
from classes.ListaDeJogadores import ListaDeJogadores
from classes.Jogador import Jogador


def criar_matriz(altura: int, comprimento: int) -> list[list[int]]:
    matriz: list[list[int]] = []
    h: int
    for h in range(altura):
        matriz.append([])
        for _ in range(comprimento):
            matriz[h].append(0)
    return matriz


def limpar_ecran() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def verificar_se_e_possivel_converter_para_inteiro(value: any) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def verificar_se_index_existe_na_matriz(matriz, y, x):
    try:
        matriz[y][x] = 1
        return True
    except IndexError:
        return False


def prettytable_matriz(matriz, altura, comprimento) -> bool:
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
                    case 0:
                        linha.append("\U000026AB")
            linha.insert(0, y + 1)
            linhas.append(linha)
        tab = PrettyTable(cabecalho)
        tab.add_rows(linhas)
        print(tab)
    except TypeError:
        return False
    except IndexError:
        return False
    return True


def verificar_se_e_json(nome_ficheiro: str) -> bool:
    try:
        ficheiro = open(nome_ficheiro, 'r')
        json.load(ficheiro)
        return True
    except JSONDecodeError:
        return False


def adicionar_jogador_a_lista_de_jogadores(lista_de_jogadores: ListaDeJogadores, jogador: Jogador) -> bool:
    if lista_de_jogadores.obter(jogador.nome):
        return False
    lista_de_jogadores.adicionar(jogador)
    return True


def finalizar_instrucao() -> None:
    """Esta função será executada no final de cada instrução"""
    input('\nClique ENTER para continuar e limpar o ecran.')
    limpar_ecran()


def inicializar_instrucao() -> None:
    """Esta função será executada antes de cada instrução"""
    limpar_ecran()


def imprimir_menu() -> None:
    print('--------------------------------------------')
    print('Jogo do N em Linha:')
    print('---Jogadores--------------------------------')
    print('EJ - Eliminar')
    print('LJ - Lista')
    print('RJ - Registar')
    print('---Jogo-------------------------------------')
    print('CP - Colocar Peca')
    print('D  - Desitir')
    print('DJ - Detalhes')
    print('IJ - Iniciar')
    print('V  - Visualizar')
    print('---Dados------------------------------------')
    print('G  - Guardar')
    print('L  - Ler')
    print('---Outros--Comandos-------------------------')
    print('AJUDA - Guia de como usar os comandos')
    print('SAIR - Sair do Jogo')
    print('--------------------------------------------')


def imprimir_ajuda() -> None:
    print("RJ Nome")
    print("EJ Nome")
    print("LJ")
    print(
        "IJ Nome Nome Comprimento Altura TamanhoSequência[ TamanhoPeça TamanhoPeça TamanhoPeça ...]")
    print("DJ")
    print("D Nome[ Nome]")
    print("CP Nome TamanhoPeça Posição[ Sentido]")
    print("V")
    print("G NomeFicheiro")
    print("L NomeFicheiro")
