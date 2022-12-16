import json
import os

from tipos.definicoes import *
from tipos.jogador import *
from tipos.matriz import *


class Model:
    def __init__(self):
        """A classe Model vai ser inicializada com 3 variaveis:\n
        - **jogadores**: Lista com todos os jogadores registados.\n
        - **jogo**: Matriz de inteiros com os valores correspondentes a cada jogada: 0, 1, 2.\n
        - **definicoes**: Todas as definições relativas ao jogo, em baixo encontram se os valores das definições:
            - jogadores: Lista dos jogadores a jogar
            - tamanho_sequencia: Quantidade de peças necessárias para vencer o jogo
            - altura: Altura da matriz do jogo
            - comprimento: Comprimento da matriz do jogo
            - pecas_especiais: Lista de peças especiais
        """
        self.jogadores: list[Jogador] = []
        self.jogo: MatrizDeNumerosInteiros = []
        self.definicoes: Definicoes = {
            "jogadores": [],
            "tamanho_sequencia": 0,
            "altura": 0,
            "comprimento": 0,
            "pecas_especiais": [],
        }

    def atualizar_jogo(self, jogo: MatrizDeNumerosInteiros) -> None:
        """Esta função serve para atualizar o Jogo, recebe uma matriz de numeros interios que substituirá a matriz atual"""
        self.jogo = jogo

    def obter_jogo(self) -> MatrizDeNumerosInteiros:
        """Esta função serve para obter o jogo atual"""
        return self.jogo

    def atualizar_lista_de_jogadores(self, lista_de_jogadores: list[Jogador]) -> None:
        """Esta função serve para atualizar todos os dados da variavel jogadores"""
        self.jogadores = lista_de_jogadores

    def obter_lista_de_jogadores(self) -> list[Jogador]:
        """Esta função serve para obter todos os jogadores registados"""
        return self.jogadores

    def obter_jogador_pelo_nome(self, nome_do_jogador: str) -> Jogador:
        """Esta função obtem o jogador através do nome do Jogador"""
        for jogador in self.jogadores:
            if jogador['nome'] == nome_do_jogador and not jogador['eliminado']:
                return jogador
        return False

    def atualizar_definicoes_do_jogo(self, novas_definicoes: Definicoes) -> None:
        """Esta função serve para atualizar as definicoes do jogo"""
        self.definicoes = novas_definicoes

    def obter_definicoes_do_jogo(self) -> Definicoes:
        """Esta função serve para obter as definicoes do jogo"""
        return self.definicoes

    def obter_jogadores_em_jogo(self) -> list[Jogador]:
        """Retorna a lista de todos os jogadores em jogo"""
        return [jogador for jogador in self.obter_lista_de_jogadores() if
                jogador['em_jogo'] and not jogador['eliminado']]

    def salvar_dados_em_ficheiro(self, nome_ficheiro: str) -> bool:
        """Esta função serve para salvar os jogos e os jogadores num ficheiro .json"""
        if not os.path.exists(nome_ficheiro):
            return False
        try:
            ficheiro = open(nome_ficheiro, 'w')
            dados = {
                "jogadores": self.obter_lista_de_jogadores(),
                "jogo": self.obter_jogo(),
                "definicoes": self.obter_definicoes_do_jogo()
            }
            ficheiro.write(json.dumps(dados))
            ficheiro.close()
            return True
        except FileNotFoundError:
            return False

    def ler_dados_de_um_ficheiro(self, nome_ficheiro: str) -> bool:
        """Esta função serve para atribuir às variaveis jogos e jogadores os valores de um determinado ficheiro .json"""
        if not os.path.exists(nome_ficheiro):
            return False
        try:
            ficheiro = open(nome_ficheiro, 'r')
            dados = json.load(ficheiro)
            self.atualizar_jogo(dados['jogo'])
            self.atualizar_lista_de_jogadores(dados['jogadores'])
            self.atualizar_definicoes_do_jogo(dados['definicoes'])
            ficheiro.close()
            return True
        except FileNotFoundError:
            return False
