from __types__ import Player
import json


class Model:

    @staticmethod
    def get_player(name: str, file_path: str) -> Player:
        file = open(file_path, 'r')
        players: list[Player] = json.load(file)
        if len(players) == 0:
            return None
        for player in players:
            if player['name'] == name:
                file.close()
                return player
        return None

    @staticmethod
    def get_all_players(file_path: str) -> list[Player]:
        file = open(file_path, 'r')
        return json.load(file)

    def post_player(self, player: Player, file_path: str) -> bool:
        if self.get_player(player['name'], file_path) is not None:
            return False
        file = open(file_path, 'r')
        players: list[Player] = json.load(file)
        file.close()
        players.append(player)

        file = open(file_path, 'w')
        file.write(json.dumps(players))
        file.close()
        return True

    def put_player(self, name: str, new_player: Player, file_path: str) -> bool:
        if self.get_player(name, file_path) is None:
            return False
        file = open(file_path, 'r')
        players: list[Player] = json.load(file)
        new_list: list[Player] = []

        if len(players) == 0:
            return False

        for player in players:
            if player['name'] == name:
                player = new_player
            new_list.append(player)

        file = open(file_path, 'w')
        file.write(json.dumps(new_list))
        file.close()

        return True

    def delete_player(self, name: str, file_path: str) -> bool:
        if self.get_player(name, file_path) is None:
            return False
        file = open(file_path, 'r')
        players: list[Player] = json.load(file)
        new_list: list[Player] = []

        if len(players) == 0:
            return False

        for player in players:
            if player['name'] != name:
                new_list.append(player)

        file = open(file_path, 'w')
        file.write(json.dumps(new_list))
        file.close()

        return True
