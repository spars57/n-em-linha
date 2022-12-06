from functions import *
from controller import Controller
from console import Console

file_name = 'data/players.json'


class View:
    def __init__(self):
        self.console = Console()
        self.controller = Controller()
        self.allowed_commands = ['rj', 'ej', 'lj', 'ij', 'dj', 'd', 'cp', 'v', 'g', 'l', 'exit']

    def create_new_player(self, name: str) -> bool:
        return self.controller.post_player(create_new_player_dict(name), file_name)

    def delete_player(self, name: str) -> bool:
        return self.controller.delete_player(name, file_name)

    def print_players_list(self) -> None:
        players = self.controller.get_players(file_name)
        for player in players:
            print(player)

    def loop(self) -> None:
        while True:
            inputs: list[str] = input('Introduza o seu comando: ').split(None, 1)
            command = inputs[0].lower()
            args = None

            if len(inputs) == 2:
                args = inputs[1]

            match command:
                case 'rj':
                    if self.create_new_player(args):
                        self.console.print_success(f'Jogador "{args}" registado com sucesso.')
                    else:
                        self.console.print_error(f'Jogador "{args}" já existe.')
                case 'lj':
                    self.print_players_list()
                case 'ej':
                    if self.delete_player(args):
                        self.console.print_success(f'Jogador "{args}" removido com sucesso.')
                    else:
                        self.console.print_error(f'Jogador "{args}" não existente.')
                case 'exit':
                    exit()
                case default:
                    self.console.print_error(f'Comando "{command}" não encontrado.')
