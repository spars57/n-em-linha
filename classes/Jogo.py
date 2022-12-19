from tipos.matriz import *


class Jogo:
    def __init__(self):
        self.jogo: TMatrizDeNumerosInteiros = []

    def obter(self) -> TMatrizDeNumerosInteiros:
        return self.jogo

    def atualizar(self, jogo: TMatrizDeNumerosInteiros) -> None:
        self.jogo = jogo
