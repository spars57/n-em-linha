from __types__ import Player


def create_new_player_dict(name: str) -> Player:
    return {"name": name, "wins": 0, "losses": 0, "draws": 0}
