import unittest

from classes.Controller import Controller
from classes.Model import Model


class TestesDesistir(unittest.TestCase):

    def start(self):
        self.correto()
        self.jogador_nao_registado()
        self.nao_existe_jogo_em_curso()
        self.jogador_nao_participa()

    def correto(self):
        model = Model()
        controller = Controller()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 16
        altura = 12
        tamanho_sequencia = 4

        controller.registar_jogador(model, nome1)
        controller.registar_jogador(model, nome2)

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 3, 3, 3]

        player1 = model.lista.obter(nome1)
        player2 = model.lista.obter(nome2)

        self.assertEqual(0, player1.vitorias)
        self.assertEqual(0, player2.vitorias)

        self.assertEqual(0, player1.derrotas)
        self.assertEqual(0, player2.derrotas)

        controller.iniciar_jogo(model, parametros)

        resposta = controller.desistir_do_jogo(model, [nome1])

        self.assertEqual(0, player1.vitorias)
        self.assertEqual(1, player2.vitorias)

        self.assertEqual(1, player1.derrotas)
        self.assertEqual(0, player2.derrotas)

        self.assertEqual(resposta, 'Desistência com sucesso. Jogo terminado.')

    def jogador_nao_registado(self):
        model = Model()
        controller = Controller()

        resposta = controller.desistir_do_jogo(model, ['eu_nao_existo_'])
        self.assertEqual(resposta, 'Jogador não registado.')

    def nao_existe_jogo_em_curso(self):
        model = Model()
        controller = Controller()

        controller.registar_jogador(model, 'player1')

        resposta = controller.desistir_do_jogo(model, ['player1'])

        self.assertEqual(resposta, 'Não existe jogo em curso.')

    def jogador_nao_participa(self):
        model = Model()
        controller = Controller()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 16
        altura = 12
        tamanho_sequencia = 4

        controller.registar_jogador(model, nome1)
        controller.registar_jogador(model, nome2)
        controller.registar_jogador(model, 'player3')

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 3, 3, 3]

        player1 = model.lista.obter(nome1)
        player2 = model.lista.obter(nome2)

        self.assertEqual(0, player1.vitorias)
        self.assertEqual(0, player2.vitorias)

        self.assertEqual(0, player1.derrotas)
        self.assertEqual(0, player2.derrotas)

        controller.iniciar_jogo(model, parametros)

        resposta = controller.desistir_do_jogo(model, ['player3'])

        self.assertEqual(resposta, 'Jogador não participa no jogo em curso.')
