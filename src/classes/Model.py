import os
import utilitarios as utils
import json

from typing import IO
from classes.ListaDeJogadores import ListaDeJogadores
from classes.Definicoes import Definicoes
from classes.Jogo import Jogo
from classes.Jogador import Jogador


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
            return 'Ocorreu um erro na gravação.'

        if not utils.verificar_se_e_json(nome_ficheiro):
            return 'Ocorreu um erro na gravação.'

        try:
            ficheiro: IO = open(nome_ficheiro, 'r')
            dados: any = json.load(ficheiro)
            self.jogo.grelha = dados['jogo']
            self.lista.limpar()

            jogadores: list[dict] = dados['jogadores']
            definicoes: dict = dados['definicoes']

            for jogador in jogadores:
                jogador_transformado = Jogador()
                jogador_transformado.nome = jogador['nome']
                jogador_transformado.vitorias = jogador['vitorias']
                jogador_transformado.derrotas = jogador['derrotas']
                jogador_transformado.empates = jogador['empates']
                jogador_transformado.eliminado = jogador['eliminado']
                jogador_transformado.em_jogo = jogador['em_jogo']
                jogador_transformado.pecas_especiais = jogador['pecas_especiais']
                self.lista.adicionar(jogador_transformado)

            self.definicoes.altura = definicoes['altura']
            self.definicoes.altura_maxima_ocupada = definicoes['altura_maxima_ocupada']
            self.definicoes.comprimento = definicoes['comprimento']
            self.definicoes.comprimento_maximo_ocupado = definicoes['comprimento_maximo_ocupado']
            self.definicoes.espacos_livres = definicoes['espacos_livres']
            self.definicoes.espacos_ocupados = definicoes['espacos_ocupados']
            self.definicoes.em_curso = definicoes['em_curso']
            self.definicoes.pecas_especiais = definicoes['pecas_especiais']
            self.definicoes.nomes_dos_jogadores = definicoes['nomes_dos_jogadores']
            self.definicoes.tamanho_sequencia = definicoes['tamanho_sequencia']
            self.definicoes.vez = definicoes['vez']

            ficheiro.close()
            return 'Jogo carregado.'
        except FileNotFoundError:
            return 'Ocorreu um erro na gravação.'
