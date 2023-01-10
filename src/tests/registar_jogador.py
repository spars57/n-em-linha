import unittest

from classes import Controller
from classes import Model


class TestesRegistarJogador(unittest.TestCase):

    def start(self):
        self.correto()
        self.duplicado()

    def correto(self):
        controller = Controller.Controller()
        model = Model.Model()
        resposta: str = controller.registar_jogador(model, 'jonh_doe')
        self.assertEqual(resposta, 'Jogador registado com sucesso.')
        self.assertIs(1, len(model.lista.dados))

    def duplicado(self):
        controller = Controller.Controller()
        model = Model.Model()

        resposta: str = controller.registar_jogador(model, 'jonh_doe')
        self.assertEqual(resposta, 'Jogador registado com sucesso.')
        self.assertIs(1, len(model.lista.dados))

        resposta: str = controller.registar_jogador(model, 'jonh_doe')
        self.assertEqual(resposta, 'Jogador existente.')
        self.assertIs(1, len(model.lista.dados))
