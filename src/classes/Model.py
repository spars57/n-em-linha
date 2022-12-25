from typing import IO

from DefinicoesDoJogo import *
from Jogo import *
from Utilitarios import *
from Informador import *


class Model:
    def __init__(self):
        self.jogo = Jogo()
        self.lista_de_jogadores = ListaDeJogadores()
        self.definicoes_do_jogo = DefinicoesDoJogo()
        self.utilitarios = Utilitarios()
        self.informador = Informador()

    def salvar_dados_em_ficheiro(self, nome_ficheiro: str) -> str:
        if not os.path.exists(nome_ficheiro):
            return 'Ocorreu um erro na gravação.'
        try:
            ficheiro: IO = open(nome_ficheiro, 'w')
            jogadores: list[any] = []
            jogo: MatrizDeNumerosInterios = self.jogo.grelha
            definicoes: DefinicoesDoJogo.__dict__ = self.definicoes_do_jogo.__dict__

            jogador: Jogador
            for jogador in self.lista_de_jogadores.lista_de_jogadores:
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

    def ler_dados_de_um_ficheiro(self, nome_ficheiro: str) -> str:
        if not os.path.exists(nome_ficheiro):
            return 'Ocorreu um erro na gravação.'

        if not self.utilitarios.verificar_se_e_json(nome_ficheiro):
            return 'Ocorreu um erro na gravação.'

        try:
            ficheiro: IO = open(nome_ficheiro, 'r')
            dados: any = json.load(ficheiro)
            self.jogo.grelha = dados['jogo']
            self.lista_de_jogadores.limpar()

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

                self.lista_de_jogadores.adicionar_jogador(jogador_transformado)

            self.definicoes_do_jogo.altura = definicoes['altura']
            self.definicoes_do_jogo.altura_maxima_ocupada = definicoes['altura_maxima_ocupada']
            self.definicoes_do_jogo.comprimento = definicoes['comprimento']
            self.definicoes_do_jogo.comprimento_maximo_ocupado = definicoes['comprimento_maximo_ocupado']
            self.definicoes_do_jogo.espacos_livres = definicoes['espacos_livres']
            self.definicoes_do_jogo.espacos_ocupados = definicoes['espacos_ocupados']
            self.definicoes_do_jogo.em_curso = definicoes['em_curso']
            self.definicoes_do_jogo.pecas_especiais = definicoes['pecas_especiais']
            self.definicoes_do_jogo.nomes_dos_jogadores = definicoes['nomes_dos_jogadores']
            self.definicoes_do_jogo.tamanho_sequencia = definicoes['tamanho_sequencia']
            self.definicoes_do_jogo.vez = definicoes['vez']

            ficheiro.close()
            return 'Jogo carregado.'
        except FileNotFoundError:
            return 'Ocorreu um erro na gravação.'
