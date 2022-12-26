from classes.Jogador import Jogador


class ListaDeJogadores:
    def __init__(self) -> None:
        self.dados: list[Jogador] = []

    def limpar(self) -> None:
        self.dados = []

    def adicionar(self, jogador: Jogador) -> None:
        self.dados.append(jogador)

    def remover(self, nome_jogador: str) -> None:
        jogador: Jogador
        self.dados = [jogador for jogador in self.dados if jogador.nome != nome_jogador]

    def obter(self, nome_do_jogador: str) -> Jogador | None:
        try:
            jogador: Jogador
            return [jogador for jogador in self.dados if jogador.nome == nome_do_jogador][0]
        except IndexError:
            return None

    def obter_jogadores_em_jogo(self) -> list[Jogador]:
        jogador: Jogador
        return [jogador for jogador in self.dados if jogador.em_jogo]
