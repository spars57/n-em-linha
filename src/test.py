from tests.colocar_peca import TestesColocarPeca
from tests.desistir import TestesDesistir
from tests.eliminar_jogador import TestesEliminarJogador
from tests.iniciar_jogo import TestesIniciarJogo
from tests.lista_jogadores import TestesListaDeJogadores
from tests.registar_jogador import TestesRegistarJogador
from tools.utilitarios import limpar_ecran

limpar_ecran()

TestesRegistarJogador().start()
TestesEliminarJogador().start()
TestesIniciarJogo().start()
TestesListaDeJogadores().start()
TestesDesistir().start()
TestesColocarPeca().start()
