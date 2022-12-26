import json
import os
from typing import IO

from classes.Definicoes import Definicoes
from classes.Jogador import Jogador
from classes.Jogo import Jogo
from classes.ListaDeJogadores import ListaDeJogadores
from tools import utilitarios as utils


class Model:
    def __init__(self):
        self.jogo = Jogo()
        self.lista = ListaDeJogadores()
        self.definicoes = Definicoes()

    def salvar(self, nome_ficheiro: str) -> str:
        if not os.path.exists(nome_ficheiro):
            return 'Ocorreu um erro na gravação.'

        if not utils.verificar_se_e_json(nome_ficheiro):
            return 'Ocorreu um erro na gravação.'

        try:
            ficheiro: IO = open(nome_ficheiro, 'w')
            jogadores: list[any] = []
            jogo: list[list[int]] = self.jogo.grelha
            definicoes: Definicoes.__dict__ = self.definicoes.__dict__

            jogador: Jogador
            for jogador in self.lista.dados:
                jogadores.append(jogador.__dict__)

            dados = {
                "jogadores": jogadores,
                "jogo": jogo,
                "definicoes": definicoes,
            }

            ficheiro.write(json.dumps(dados))
            ficheiro.close()
            return 'Jogo gravado.'
        except FileNotFoundError:
            return 'Ocorreu um erro na gravação.'

    def ler(self, nome_ficheiro: str) -> str:
        if not os.path.exists(nome_ficheiro):
            return 'Ocorreu um erro no carregamento.'

        if not utils.verificar_se_e_json(nome_ficheiro):
            return 'Ocorreu um erro no carregamento.'

        try:
            ficheiro: IO = open(nome_ficheiro, 'r')
            dados: any = json.load(ficheiro)
            self.jogo.grelha = dados['jogo']
            self.lista.limpar()

            jogadores: list[dict] = dados['jogadores']
            definicoes: dict = dados['definicoes']

            for jogador in jogadores:
                jogador_guardado: Jogador = Jogador()
                for key in jogador.keys():
                    jogador_guardado.__dict__[key] = jogador[key]
                self.lista.adicionar(jogador_guardado)

            for key in definicoes.keys():
                self.definicoes.__dict__[key] = definicoes[key]

            ficheiro.close()
            return 'Jogo carregado.'
        except FileNotFoundError:
            return 'Ocorreu um erro no carregamento.'
