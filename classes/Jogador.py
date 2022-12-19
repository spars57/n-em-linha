from tipos.jogador import *


class Jogador:
    def __init__(self, nome=""):
        self.dados: TJogador = {
            "nome": nome,
            "vitorias": 0,
            "derrotas": 0,
            "empates": 0,
            "em_jogo": False,
            "eliminado": False,
            "pecas_especiais": [],
        }

    def obter_nome(self) -> str:
        return self.dados['nome']

    def obter_numero_de_vitorias(self) -> int:
        return self.dados['vitorias']

    def obter_numero_de_derrotas(self) -> int:
        return self.dados['derrotas']

    def obter_numero_de_empates(self) -> int:
        return self.dados['empates']

    def obter_em_jogo(self) -> bool:
        return self.dados['em_jogo']

    def obter_eliminado(self) -> bool:
        return self.dados['eliminado']

    def obter_pecas_especiais(self) -> list[int]:
        return self.dados['pecas_especiais']

    def obter(self) -> TJogador:
        return self.dados

    def atualizar_nome(self, nome_do_jogador: str) -> None:
        self.dados['nome'] = nome_do_jogador

    def atualizar_numero_de_vitorias(self, valor: int) -> None:
        self.dados['vitorias'] = valor

    def atualizar_numero_de_derrotas(self, valor: int) -> None:
        self.dados['derrotas'] = valor

    def atualizar_numero_de_empates(self, valor: int) -> None:
        self.dados['empates'] = valor

    def atualizar_em_jogo(self, valor: bool) -> None:
        self.dados['em_jogo'] = valor

    def atualizar_eliminado(self, valor: bool) -> None:
        self.dados['eliminado'] = valor

    def atualizar_pecas_especiais(self, valor: list[int]) -> None:
        self.dados['pecas_especiais'] = valor

    def atualizar(self, jogador: TJogador) -> None:
        self.dados = jogador
