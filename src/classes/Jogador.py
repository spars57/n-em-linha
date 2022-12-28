import json


class Jogador:
    def __init__(self):
        self.nome: str = ''
        self.vitorias: int = 0
        self.derrotas: int = 0
        self.empates: int = 0
        self.em_jogo: bool = False
        self.pecas_especiais: list[int] = []

    def json(self) -> str:
        return json.dumps(self.__dict__)
