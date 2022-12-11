import json
import os
from utils.jogador import *
from utils.definicoes import *


class Model:
    def __init__(self):
        self.jogadores: list[Jogador] = []
        self.jogo: list[list[int]] = []
        self.definicoes: Definicoes = {"tamanho_sequencia": 0, "altura": 0, "comprimento": 0, "pecas_especiais": []}

    def atualizar_jogo(self, jogo: list[list[int]]) -> None:
        """Esta função serve para atualizar o Jogo"""
        self.jogo = jogo

    def obter_jogo(self) -> list[list[int]]:
        """Esta função serve para obter o jogo atual"""
        return self.jogo

    def atualizar_jogadores(self, jogadores: list[Jogador]) -> None:
        """Esta função serve para atualizar todos os dados da variavel jogadores"""
        self.jogadores = jogadores

    def obter_todos_os_jogadores(self) -> list[Jogador]:
        """Esta função serve para obter todos os jogadores registados"""
        return self.jogadores

    def obter_jogador_pelo_nome(self, nome: str) -> Jogador:
        """Esta função obtem o jogador através do nome do Jogador"""
        for jogador in self.jogadores:
            if jogador['nome'] == nome:
                return jogador
        return False

    def atualizar_definicoes_do_jogo(self, definicoes) -> None:
        """Esta função serve para atualizar as definicoes do jogo"""
        self.definicoes = definicoes

    def obter_definicoes_do_jogo(self) -> Definicoes:
        """Esta função serve para obter as definicoes do jogo"""
        return self.definicoes

    def salvar_dados_em_ficheiro(self, nome_ficheiro: str) -> bool:
        """Esta função serve para salvar os jogos e os jogadores num ficheiro .json"""
        if not os.path.exists(nome_ficheiro):
            return False
        try:
            ficheiro = open(nome_ficheiro, 'w')
            dados = {
                "jogadores": self.obter_todos_os_jogadores(),
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
            self.atualizar_jogadores(dados['jogadores'])
            self.atualizar_definicoes_do_jogo(dados['definicoes'])
            ficheiro.close()
            return True
        except FileNotFoundError:
            return False
