from tipos.definicoes import *


class DefinicoesDoJogo:
    def __init__(self):
        self.definicoes_do_jogo = {
            "nomes_dos_jogadores": [],
            "tamanho_sequencia": 0,
            "altura": 0,
            "comprimento": 0,
            "pecas_especiais": [],
            "em_curso": False,
            "vez": 0,
        }

    def resetar(self) -> None:
        self.definicoes_do_jogo = {
            "nomes_dos_jogadores": [],
            "tamanho_sequencia": 0,
            "altura": 0,
            "comprimento": 0,
            "pecas_especiais": [],
            "em_curso": False,
            "vez": 0,
        }

    def limpar(self) -> None:
        self.definicoes_do_jogo = {}

    def obter(self) -> TDefinicoes:
        return self.definicoes_do_jogo

    def atualizar(self, novas_definicoes: TDefinicoes) -> None:
        self.definicoes_do_jogo = novas_definicoes

    def obter_jogadores(self) -> list[str]:
        return self.definicoes_do_jogo['nomes_dos_jogadores']

    def obter_tamanho_sequencia(self) -> int:
        return self.definicoes_do_jogo['tamanho_sequencia']

    def obter_altura(self) -> int:
        return self.definicoes_do_jogo['altura']

    def obter_comprimento(self) -> int:
        return self.definicoes_do_jogo['comprimento']

    def obter_pecas_especiais(self) -> list[int]:
        return self.definicoes_do_jogo['pecas_especiais']

    def obter_em_curso(self) -> bool:
        return self.definicoes_do_jogo['em_curso']

    def obter_vez(self) -> int:
        return self.definicoes_do_jogo['vez']

    def atualizar_vez(self, vez: int) -> None:
        self.definicoes_do_jogo['vez'] = vez

    def atualizar_em_curso(self, valor: bool) -> None:
        self.definicoes_do_jogo['em_curso'] = valor

    def atualizar_jogadores(self, nomes_dos_jogadores: list[str]) -> None:
        self.definicoes_do_jogo['nomes_dos_jogadores'] = nomes_dos_jogadores

    def atualizar_tamanho_sequencia(self, tamanho_sequencia: int) -> None:
        self.definicoes_do_jogo['tamanho_sequencia'] = tamanho_sequencia

    def atualizar_altura(self, altura: int) -> None:
        self.definicoes_do_jogo['altura'] = altura

    def atualizar_comprimento(self, comprimento: int) -> None:
        self.definicoes_do_jogo['comprimento'] = comprimento

    def atualizar_pecas_especiais(self, pecas_especiais: list[int]) -> None:
        self.definicoes_do_jogo['pecas_especiais'] = pecas_especiais
