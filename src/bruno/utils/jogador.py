Jogador = {
    "nome": str,
    "vitorias": int,  # valor de inicialização: 0
    "derrotas": int,  # valor de inicialização: 0
    "empates": int,  # valor de inicialização: 0
    "em_jogo": bool,  # valor de inicialização: False
    "eliminado": bool,  # valor de inicialização: False
}


def criar_novo_jogador(nome: str) -> Jogador:
    # Retorna um dicionario com a mesma estrutura do que está em cima
    pass


def adicionar_jogador_a_lista_de_jogadores(jogador: Jogador) -> bool:
    # !! Isto implica uma função que valida se o jogador existe!
    # return True se adicionar
    # return False se não adicionar
    pass


def remover_jogador_da_lista(nome: str) -> bool:
    # !! Isto implica uma função que valida se o jogador existe!
    # return True se o jogador for removido
    # return False se o jogador não for
    pass


def verificar_se_jogador_existe(nome: str) -> bool:
    # return True se o jogador existir
    # return False se não existir
    pass
