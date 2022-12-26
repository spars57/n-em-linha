class Definicoes:
    def __init__(self):
        self.nomes_dos_jogadores: list = []
        self.tamanho_sequencia: int = 0
        self.altura: int = 0
        self.comprimento: int = 0
        self.pecas_especiais: list = []
        self.espacos_livres_total: int = 0
        self.espacos_ocupados: int = 0
        self.altura_maxima_ocupada: int = 0
        self.comprimento_maximo_ocupado: int = 0
        self.em_curso: bool = False
        self.vez: int = 0

    def reset(self) -> None:
        self.nomes_dos_jogadores = []
        self.tamanho_sequencia = 0
        self.altura = 0
        self.comprimento = 0
        self.pecas_especiais = []
        self.espacos_livres_total = 0
        self.espacos_ocupados = 0
        self.altura_maxima_ocupada = 0
        self.comprimento_maximo_ocupado = 0
        self.em_curso = False
        self.vez = 0
