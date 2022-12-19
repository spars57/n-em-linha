from colorama import Fore


class Informador:
    def __init__(self):
        """O Informador serve para imprimir mensagens coloridas"""

    @staticmethod
    def erro(valor: any) -> None:
        """Imprime Vermelho"""
        print(f'{Fore.RED}{valor}{Fore.RESET}')

    @staticmethod
    def sucesso(valor: any) -> None:
        """Imprime Verde"""
        print(f'{Fore.GREEN}{valor}{Fore.RESET}')

    @staticmethod
    def info(valor: any) -> None:
        """Imprime Azul"""
        print(f'{Fore.BLUE}{valor}{Fore.RESET}')

    @staticmethod
    def aviso(valor: any) -> None:
        """Imprime Amarelo"""
        print(f'{Fore.YELLOW}{valor}{Fore.RESET}')

    @staticmethod
    def predefinicao(valor: any) -> None:
        """Funciona exatamente como a função print()"""
        print(f'{Fore.WHITE}{valor}{Fore.RESET}')

    @staticmethod
    def transparente(valor: any) -> None:
        return None
