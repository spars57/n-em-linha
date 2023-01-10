import unittest

from classes.Controller import Controller
from classes.Model import Model


class TestesIniciarJogo(unittest.TestCase):

    def start(self):
        self.correto()
        self.altura_incorreta()
        self.comprimento_incorreto()
        self.tamanho_sequencia_incorreto()
        self.tamanho_peca_incorreto()
        self.jogador_nao_existe()

    def correto(self):
        controller = Controller()
        model = Model()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 16
        altura = 12
        tamanho_sequencia = 4

        controller.registar_jogador(model, nome1)
        controller.registar_jogador(model, nome2)

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 3, 3, 3]

        resposta = controller.iniciar_jogo(model, parametros)

        self.assertEqual(resposta, 'Jogo iniciado entre a e b.')
        self.assertEqual(altura, model.definicoes.altura)
        self.assertEqual(comprimento, model.definicoes.comprimento)
        self.assertEqual(tamanho_sequencia, model.definicoes.tamanho_sequencia)
        self.assertIsNot([], model.definicoes.nomes_dos_jogadores)

    def altura_incorreta(self):
        controller = Controller()
        model = Model()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 16
        altura = -1
        tamanho_sequencia = 4

        controller.registar_jogador(model, nome1)
        controller.registar_jogador(model, nome2)

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 3, 3, 3]

        resposta = controller.iniciar_jogo(model, parametros)

        self.assertEqual(resposta, 'Dimensões de grelha invalidas.')

    def comprimento_incorreto(self):
        controller = Controller()
        model = Model()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 99
        altura = 12
        tamanho_sequencia = 4

        controller.registar_jogador(model, nome1)
        controller.registar_jogador(model, nome2)

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 3, 3, 3]

        resposta = controller.iniciar_jogo(model, parametros)

        self.assertEqual(resposta, 'Dimensões de grelha invalidas.')

    def tamanho_sequencia_incorreto(self):
        controller = Controller()
        model = Model()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 16
        altura = 12
        tamanho_sequencia = 99

        controller.registar_jogador(model, nome1)
        controller.registar_jogador(model, nome2)

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 3, 3, 3]

        resposta = controller.iniciar_jogo(model, parametros)

        self.assertEqual(resposta, 'Tamanho de sequência invalido.')

    def tamanho_peca_incorreto(self):
        controller = Controller()
        model = Model()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 16
        altura = 12
        tamanho_sequencia = 4

        controller.registar_jogador(model, nome1)
        controller.registar_jogador(model, nome2)

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 99]

        resposta = controller.iniciar_jogo(model, parametros)

        self.assertEqual(resposta, 'Dimensões de peças especiais invalidas.')

    def jogador_nao_existe(self):
        controller = Controller()
        model = Model()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 16
        altura = 12
        tamanho_sequencia = 4

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 3, 3, 3]

        resposta = controller.iniciar_jogo(model, parametros)

        self.assertEqual(resposta, 'Jogador não registado.')
