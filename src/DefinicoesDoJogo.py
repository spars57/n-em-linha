import json


class DefinicoesDoJogo:
    def __init__(self):
        self.nomes_dos_jogadores: list = []
        self.tamanho_sequencia: int = 0
        self.altura: int = 0
        self.comprimento: int = 0
        self.pecas_especiais: list = []
        self.espacos_livres: int = 0
        self.espacos_ocupados: int = 0
        self.altura_maxima_ocupada: int = 0
        self.comprimento_maximo_ocupado: int = 0
        self.em_curso: bool = False
        self.vez: int = 0

    def resetar(self) -> None:
        self.nomes_dos_jogadores = []
        self.tamanho_sequencia = 0
        self.altura = 0
        self.comprimento = 0
        self.pecas_especiais = []
        self.espacos_livres = 0
        self.espacos_ocupados = 0
        self.altura_maxima_ocupada = 0
        self.comprimento_maximo_ocupado = 0
        self.em_curso = False
        self.vez = 0

    def json(self) -> str:
        jsondict: dict = {
            'nomes_dos_jogadores': self.nomes_dos_jogadores,
            'tamanho_sequencia': self.tamanho_sequencia,
            'altura': self.altura,
            'comprimento': self.comprimento,
            'pecas_especiais': self.pecas_especiais,
            'espacos_livres': self.espacos_livres,
            'espacos_ocupados': self.espacos_ocupados,
            'altura_maxima_ocupada': self.altura_maxima_ocupada,
            'comprimento_maximo_ocupado': self.comprimento_maximo_ocupado,
            'em_curso': self.em_curso,
            'vez': self.vez
        }
        return json.dumps(jsondict, indent=2)
