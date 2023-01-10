import unittest

from classes.Controller import Controller
from classes.Model import Model


class TestesListaDeJogadores(unittest.TestCase):

    def start(self):
        self.correto()

    def correto(self):
        model = Model()
        controller = Controller()

        controller.registar_jogador(model, 'player1')
        resposta = controller.mostrar_lista_de_jogadores(model)

        self.assertIsNot(resposta, 'Não existem jogadores registados.')

    def nao_existem_jogadores_registados(self):
        model = Model()
        controller = Controller()

        resposta = controller.mostrar_lista_de_jogadores(model)

        self.assertEqual(resposta, 'Não existem jogadores registados.')
