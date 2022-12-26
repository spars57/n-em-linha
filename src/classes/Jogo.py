class Jogo:
    def __init__(self):
        self.grelha: list[list[int]] = []

    def reset(self) -> None:
        self.grelha: list[list[int]] = []
