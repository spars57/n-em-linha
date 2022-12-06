from model import Model
from __types__ import Player


class Controller:
    def __init__(self):
        self.model = Model()
        pass

    def get_player(self, player_name: str, file_name: str) -> bool:
        return self.model.get_player(player_name, file_name) is not None

    def get_players(self, file_name: str) -> list[Player]:
        return self.model.get_all_players(file_name)

    def delete_player(self, name: str, file_name: str) -> bool:
        # TODO: Validar se o jogador em questão não está a participar noutro jogo
        return self.model.delete_player(name, file_name)

    def post_player(self, player: Player, file_name) -> bool:
        if not self.get_player(player['name'], file_name):
            self.model.post_player(player, file_name)
            return True
        else:
            return False
