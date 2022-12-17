import json
import os
from ListaDeJogadores import *
from DefinicoesDoJogo import *
from Jogador import *
from Jogo import *


class Model:
    def __init__(self):
        self.jogo: Jogo = Jogo()
        self.lista_de_jogadores: ListaDeJogadores = ListaDeJogadores()
        self.definicoes_do_jogo: DefinicoesDoJogo = DefinicoesDoJogo()

    def salvar_dados_em_ficheiro(self, nome_ficheiro: str) -> bool:
        """Esta função serve para salvar os jogos e os jogadores num ficheiro .json"""
        if not os.path.exists(nome_ficheiro):
            return False
        try:
            ficheiro = open(nome_ficheiro, 'w')

            dados = {
                "jogadores": self.lista_de_jogadores.obter_como_lista_de_TJogador(),
                "jogo": self.jogo.obter(),
                "definicoes": self.definicoes_do_jogo.obter()
            }
            ficheiro.write(json.dumps(dados))
            ficheiro.close()
            return True
        except FileNotFoundError:
            return False

    def ler_dados_de_um_ficheiro(self, nome_ficheiro: str) -> bool:
        try:
            ficheiro = open(nome_ficheiro, 'r')
            dados = json.load(ficheiro)
            self.jogo.atualizar(dados['jogo'])
            self.lista_de_jogadores.limpar()
            for jogador in dados['jogadores']:
                jogador_transformado = Jogador()
                jogador_transformado.atualizar_nome(jogador['nome'])
                jogador_transformado.atualizar_numero_de_vitorias(jogador['vitorias'])
                jogador_transformado.atualizar_numero_de_derrotas(jogador['derrotas'])
                jogador_transformado.atualizar_numero_de_empates(jogador['empates'])
                jogador_transformado.atualizar_eliminado(jogador['eliminado'])
                jogador_transformado.atualizar_em_jogo(jogador['em_jogo'])
                self.lista_de_jogadores.adicionar_jogador(jogador_transformado)
            self.definicoes_do_jogo.atualizar(dados['definicoes'])
            ficheiro.close()
            return True
        except FileNotFoundError:
            print('FileNotFoundError')
            return False
