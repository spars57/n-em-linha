import Jogador
from tipos.jogador import TJogador


class ListaDeJogadores:
    def __init__(self) -> None:
        self.lista_de_jogadores: list[Jogador] = []

    def limpar(self) -> None:
        self.lista_de_jogadores = []

    def adicionar_jogador(self, jogador: Jogador) -> None:
        self.lista_de_jogadores.append(jogador)

    def remover_jogador_pelo_nome(self, nome_jogador: str) -> None:
        self.atualizar([jogador for jogador in self.lista_de_jogadores if
                        jogador.obter_nome() != nome_jogador])

    def eliminar_jogador_pelo_nome(self, nome_jogador: str) -> None:
        for jogador in self.lista_de_jogadores:
            if jogador.obter_nome() == nome_jogador and not jogador.obter_eliminado():
                jogador.atualizar_eliminado(True)

    def reativar_jogador_eliminado_pelo_nome(self, nome_jogador: str) -> None:
        for jogador in self.lista_de_jogadores:
            if jogador.obter_nome() == nome_jogador and jogador.obter_eliminado():
                jogador.atualizar_eliminado(False)

    def obter(self) -> list[Jogador]:
        return self.lista_de_jogadores

    def obter_como_lista_de_TJogador(self) -> list[TJogador]:
        return [jogador.obter() for jogador in self.lista_de_jogadores]

    def obter_por_nome(self, nome_do_jogador: str) -> Jogador:
        for jogador in self.lista_de_jogadores:
            if jogador.obter_nome() == nome_do_jogador:
                return jogador

    def obter_jogadores_em_jogo(self) -> list[Jogador]:
        return [jogador for jogador in self.lista_de_jogadores if
                jogador.obter_em_jogo() and not jogador.obter_eliminado()]

    def atualizar(self, nova_lista_de_jogadores: list[Jogador]) -> None:
        self.lista_de_jogadores = nova_lista_de_jogadores

    def verificar_se_jogador_existe_pelo_nome(self, nome_do_jogador: str) -> bool:
        for jogador in self.lista_de_jogadores:
            if jogador.obter_nome() == nome_do_jogador:
                return True
        return False
