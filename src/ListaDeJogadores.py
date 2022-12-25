import json

import Jogador


class ListaDeJogadores:
    def __init__(self) -> None:
        self.lista_de_jogadores: list[Jogador] = []

    def limpar(self) -> None:
        self.lista_de_jogadores = []

    def adicionar_jogador(self, jogador: Jogador) -> None:
        self.lista_de_jogadores.append(jogador)

    def remover_jogador_pelo_nome(self, nome_jogador: str) -> None:
        jogador: Jogador
        self.lista_de_jogadores = [jogador for jogador in self.lista_de_jogadores if jogador.nome != nome_jogador]

    def substituir_jogador_pelo_nome(self, nome_do_jogador: str, novo_jogador: Jogador) -> None:
        index: int
        for index in range(len(self.lista_de_jogadores)):
            jogador: Jogador = self.lista_de_jogadores[index]
            if jogador.nome == nome_do_jogador:
                self.lista_de_jogadores.pop(index)
                self.lista_de_jogadores.append(novo_jogador)

    def eliminar_jogador_pelo_nome(self, nome_jogador: str) -> None:
        jogador: Jogador
        for jogador in self.lista_de_jogadores:
            if jogador.nome == nome_jogador and not jogador.eliminado:
                jogador.eliminado = True

    def reativar_jogador_eliminado_pelo_nome(self, nome_jogador: str) -> None:
        jogador: Jogador
        for jogador in self.lista_de_jogadores:
            if jogador.nome == nome_jogador and jogador.eliminado:
                jogador.eliminado = False

    def obter_por_nome(self, nome_do_jogador: str) -> Jogador:
        try:
            jogador: Jogador
            return [jogador for jogador in self.lista_de_jogadores if jogador.nome == nome_do_jogador][0]
        except IndexError:
            return None

    def obter_jogadores_em_jogo(self) -> list[Jogador]:
        jogador: Jogador
        return [jogador for jogador in self.lista_de_jogadores if jogador.em_jogo and not jogador.eliminado]

    def verificar_se_jogador_existe_pelo_nome(self, nome_do_jogador: str) -> bool:
        jogador: Jogador
        for jogador in self.lista_de_jogadores:
            if jogador.nome == nome_do_jogador:
                return True
        return False
