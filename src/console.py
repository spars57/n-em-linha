from colorama import Fore


# O objetivo desta classe é fazer prints coloridos.

class Console:
    @staticmethod
    def print_error(message: str):
        print(f'{Fore.RED}{message}{Fore.RESET}')

    @staticmethod
    def print_success(message: str):
        print(f'{Fore.GREEN}{message}{Fore.RESET}')

    @staticmethod
    def print_warning(message: str):
        print(f'{Fore.YELLOW}{message}{Fore.RESET}')

    @staticmethod
    def print_info(message: str):
        print(f'{Fore.BLUE}{message}{Fore.RESET}')
