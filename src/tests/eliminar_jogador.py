import unittest

from classes import Controller
from classes import Model


class TestesEliminarJogador(unittest.TestCase):

    def start(self):
        self.correto()
        self.jogador_nao_existente()
        self.jogador_participa_no_jogo_em_curso()

    def correto(self):
        controller = Controller.Controller()
        model = Model.Model()
        controller.registar_jogador(model, 'jonh_doe')
        self.assertIs(1, len(model.lista.dados))

        resposta: str = controller.eliminar_jogador(model, 'jonh_doe')
        self.assertEqual(resposta, 'Jogador removido com sucesso.')
        self.assertIs(0, len(model.lista.dados))

    def jogador_nao_existente(self):
        controller = Controller.Controller()
        model = Model.Model()
        resposta: str = controller.eliminar_jogador(model, 'jonh_doe')
        self.assertEqual(resposta, 'Jogador não existente.')

    def jogador_participa_no_jogo_em_curso(self):
        controller = Controller.Controller()
        model = Model.Model()
        controller.registar_jogador(model, 'jonh_doe')
        self.assertIs(1, len(model.lista.dados))

        jogador = model.lista.dados[0]

        self.assertIsNot(None, jogador)
        self.assertEqual('jonh_doe', jogador.nome)

        jogador.em_jogo = True

        resposta: str = controller.eliminar_jogador(model, 'jonh_doe')
        self.assertEqual(resposta, 'Jogador participa no jogo em curso.')
