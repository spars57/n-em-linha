import unittest

from classes.Controller import Controller
from classes.Model import Model


class TestesColocarPeca(unittest.TestCase):

    def start(self):
        self.testes()

    def testes(self):
        controller = Controller()
        model = Model()

        nome1 = 'a'
        nome2 = 'b'
        comprimento = 16
        altura = 12
        tamanho_sequencia = 4

        controller.registar_jogador(model, nome1)
        controller.registar_jogador(model, nome2)

        parametros = [nome1, nome2, comprimento, altura, tamanho_sequencia, 3, 4]

        controller.iniciar_jogo(model, parametros)

        self.assertEqual(controller.colocar_peca(model, ['a', 1, 1]), 'Peça colocada.')
        self.assertEqual(controller.colocar_peca(model, ['a', 1, 1]), 'Não é a vez do jogador.')
        self.assertEqual(controller.colocar_peca(model, ['b', 1, 1]), 'Peça colocada.')
        self.assertEqual(controller.colocar_peca(model, ['a', 4, 1]), 'Tamanho da peça inválido.')
        self.assertEqual(controller.colocar_peca(model, ['a', 3, 1, 'F']), 'Posição irregular.')
        self.assertEqual(controller.colocar_peca(model, ['a', 3, 1, 'D']), 'Peça colocada.')
        controller.desistir_do_jogo(model, ['a'])

        self.assertEqual(controller.colocar_peca(model, ['a', 1, 1]), 'Não existe jogo em curso.')

        controller.iniciar_jogo(model, parametros)
        self.assertEqual(controller.colocar_peca(model, ['a', 1, 1]), 'Peça colocada.')
        self.assertEqual(controller.colocar_peca(model, ['b', 1, 2]), 'Peça colocada.')
        self.assertEqual(controller.colocar_peca(model, ['a', 1, 1]), 'Peça colocada.')
        self.assertEqual(controller.colocar_peca(model, ['b', 1, 2]), 'Peça colocada.')
        self.assertEqual(controller.colocar_peca(model, ['a', 1, 1]), 'Peça colocada.')
        self.assertEqual(controller.colocar_peca(model, ['b', 1, 2]), 'Peça colocada.')
        self.assertEqual(controller.colocar_peca(model, ['a', 1, 1]), 'Sequência conseguida. Jogo terminado.')
