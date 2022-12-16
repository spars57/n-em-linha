import os

from prettytable import PrettyTable
from Informador import *
from Model import *


class Controller:
    def __init__(self, model: Model):
        self.model = model
        self.informador = Informador()

    def adicionar_jogador_a_lista_de_jogadores(self, jogador: Jogador) -> bool:
        if self.verificar_se_jogador_existe_pelo_nome(jogador['nome']):
            return False

        lista_de_jogadores = self.model.obter_lista_de_jogadores()
        lista_de_jogadores.append(jogador)

        self.model.atualizar_lista_de_jogadores(lista_de_jogadores)
        return True

    @staticmethod
    def criar_matriz(altura: int, comprimento: int) -> MatrizDeNumerosInteiros:
        matriz: MatrizDeNumerosInteiros = []

        for h in range(altura):
            matriz.append([])
            for w in range(comprimento):
                matriz[h].append(0)

        return matriz

    @staticmethod
    def criar_novo_jogador(nome_do_jogador: str) -> Jogador:
        return {
            "nome": nome_do_jogador,
            "vitorias": 0,
            "derrotas": 0,
            "empates": 0,
            "em_jogo": False,
            "eliminado": False
        }

    def eliminar_jogador_pelo_nome(self, nome_do_jogador: str) -> bool:
        if not self.verificar_se_jogador_existe_pelo_nome(nome_do_jogador):
            return False
        lista_de_jogadores = self.model.obter_lista_de_jogadores()

        for jogador in lista_de_jogadores:
            if jogador['nome'] == nome_do_jogador:
                jogador['eliminado'] = True
        self.model.atualizar_lista_de_jogadores(lista_de_jogadores)
        return True

    def finalizar_instrucao(self) -> None:
        """Esta função será executada no final de cada instrução"""
        self.informador.info('Clique ENTER para continuar e limpar o ecran')
        input()
        self.limpar_ecran()

    def inicializar_instrucao(self) -> None:
        """Esta função será executada antes de cada instrução"""
        self.limpar_ecran()

    def iniciar_jogo(self, lista_de_parametros: list[str]) -> bool:
        # Verificar se foram passados no minimo 6 parametros se não for temos um erro
        if len(lista_de_parametros) < 6:
            self.informador.predefinicao('O Comando IJ necessita de receber no minimo 6 parametros.')
            return False

        parametros: dict = {
            "nome_1": lista_de_parametros[0],
            "nome_2": lista_de_parametros[1],
            "comprimento": lista_de_parametros[2],
            "altura": lista_de_parametros[3],
            "tamanho_sequencia": lista_de_parametros[4],
            # No caso de haverem mais de 6 parametros, todos os restantes são guardados no tamanho_peca
            "tamanho_peca": [i for i in range(len(lista_de_parametros)) if i > 6]
        }

        # Validar se os dois primeiros parametros são válidos
        # Verificar se os jogadores existem e se não estão em jogo.
        nomes_dos_jogadores: list[str] = [parametros['nome_1'], parametros['nome_2']]

        # Para cada nome vamos validar se o jogador existe e pode jogar
        for nome in nomes_dos_jogadores:
            if not self.model.obter_jogador_pelo_nome(nome):
                self.informador.erro(f'Jogador "{nome}" não registado')
                return False

        # Validar se o comprimento, altura e tamanho sequencia são válidos
        # Isto é se podem ser convertidos para número inteiro
        if not self.verificar_se_e_possivel_converter_para_inteiro(parametros['comprimento']):
            self.informador.erro(f'O valor <comprimento> deve ser inteiro."')
            return False

        if not self.verificar_se_e_possivel_converter_para_inteiro(parametros['altura']):
            self.informador.erro(f'O valor <altura> deve ser inteiro.')
            return False

        if not self.verificar_se_e_possivel_converter_para_inteiro(parametros['tamanho_sequencia']):
            self.informador.erro(
                f'O valor <tamanho_sequencia> deve ser inteiro."')
            return False

        # Converter valores para inteiro
        parametros['comprimento'], parametros['altura'], parametros['tamanho_sequencia'] = int(
            parametros['comprimento']), int(
            parametros['altura']), int(parametros['tamanho_sequencia'])

        # Validar se o tamanho da sequencia é válido
        if not parametros['tamanho_sequencia'] >= 0:
            self.informador.erro(f'O valor <tamanho_sequencia> deve ser um valor entre 0 e +infinito.')
            return False

        # Validar se o comprimento é maior ou ígual que o tamanho da sequencia
        if not parametros['tamanho_sequencia'] <= parametros['comprimento']:
            self.informador.erro(f'O valor <tamanho_sequencia> deve ser menor que o <comprimento>')
            return False

        # Validar se o comprimento é maior ou ígual que o tamanho da sequencia
        if not parametros['tamanho_sequencia'] <= parametros['comprimento']:
            self.informador.erro(f'O valor <tamanho_sequencia> deve ser menor que o <comprimento>')
            return False

        # Validar se a altura está dentro dos limites aceites
        if not parametros['comprimento'] // 2 <= parametros['altura'] <= parametros['comprimento']:
            self.informador.erro(f'O valor <altura> deve estar entre <comprimento / 2> e <comprimento>')
            return False

        # Validar se as peças especiais existem
        if not len(parametros['tamanho_peca']) == 0:
            # Validar se as peças especiais são válidas em termos de tamanho
            if not len(parametros['tamanho_peca']) < parametros['tamanho_sequencia']:
                self.informador.erro(
                    f'O número de peças especiais ultrapassa o limite de {parametros["tamanho_sequencia"] - 1}.')

            # Validar se todos os valores das peças especiais são positivos e inteiros e maiores que zero
            for peca_especial in parametros['tamanho_peca']:
                if not isinstance(peca_especial, int):
                    self.informador.erro(f'Valor {peca_especial} não é inteiro')
                    return False
                if not peca_especial > 0:
                    self.informador.erro(f'Valor {peca_especial} não é maior que 0')
                    return False

        if len(self.model.obter_jogadores_em_jogo()) > 0:
            self.informador.erro('Existe um jogo em curso')
            return False

        # Esta matriz.py terá que ser salva nos dados do jogo:
        self.model.atualizar_jogo(self.criar_matriz(parametros['altura'], parametros['comprimento']))

        jogador1 = self.model.obter_jogador_pelo_nome(parametros["nome_1"])
        jogador2 = self.model.obter_jogador_pelo_nome(parametros["nome_2"])

        jogador1['em_jogo'], jogador2['em_jogo'] = True, True

        definicoes = {
            "jogadores": [jogador1, jogador2],
            "tamanho_sequencia": parametros['tamanho_sequencia'],
            "altura": parametros['altura'],
            "comprimento": parametros['comprimento'],
            "tamanho_peca": parametros['tamanho_peca'],
            "vez": 1,
        }

        self.model.atualizar_definicoes_do_jogo(definicoes)
        self.model.atualizar_jogo(self.criar_matriz(parametros['altura'], parametros['comprimento']))

        return True

    def imprimir_menu(self) -> None:
        self.informador.predefinicao('Jogo do N em Linha:')
        self.informador.predefinicao('IJ - Iniciar Jogo')
        self.informador.predefinicao('RJ - Registar Jogador')
        self.informador.predefinicao('EJ - Eliminar Jogador')
        self.informador.predefinicao('LJ - Lista de Jogadores')
        self.informador.predefinicao('D - Desitir de Jogo')
        self.informador.predefinicao('DJ - Detalhes do Jogo')
        self.informador.predefinicao('G - Guardar num ficheiro')
        self.informador.predefinicao('L - Ler dados de um ficheiro')
        self.informador.predefinicao('V - Visualizar Jogo')
        self.informador.predefinicao('sair - Sair do Jogo')

    @staticmethod
    def limpar_ecran() -> None:
        os.system('clear')

    def validar_vitoria(self) -> bool:
        jogo_atual = self.model.obter_jogo()

        def vertical() -> bool:
            definicoes = self.model.obter_definicoes_do_jogo()
            altura = definicoes['altura']
            comprimento = definicoes['comprimento']
            tamanho_sequencia = definicoes['tamanho_sequencia']
            peca_atual = 0
            sequencia_atual = 0
            for y in range(altura - 1, -1, -1):
                for x in range(comprimento):
                    if jogo_atual[y][x] == 0:
                        sequencia_atual = 0

                    if peca_atual != jogo_atual[y][x]:
                        peca_atual = jogo_atual[y][x]
                        sequencia_atual = 1
                    else:
                        sequencia_atual += 1

                    if sequencia_atual >= tamanho_sequencia:
                        return True
            return False

        def horizontal() -> bool:
            definicoes = self.model.obter_definicoes_do_jogo()
            altura = definicoes['altura']
            comprimento = definicoes['comprimento']
            tamanho_sequencia = definicoes['tamanho_sequencia']
            peca_atual = 0
            sequencia_atual = 0
            for x in range(comprimento):
                for y in range(altura - 1, -1, -1):
                    if jogo_atual[y][x] == 0:
                        sequencia_atual = 0

                    if peca_atual != jogo_atual[y][x]:
                        peca_atual = jogo_atual[y][x]
                        sequencia_atual = 1
                    else:
                        sequencia_atual += 1

                    if sequencia_atual >= tamanho_sequencia:
                        return True
            return False

        def diagonal_esquerda_direita() -> bool:
            definicoes = self.model.obter_definicoes_do_jogo()
            altura = definicoes['altura']
            comprimento = definicoes['comprimento']
            tamanho_sequencia = definicoes['tamanho_sequencia']

            for y in range(altura - 1, -1, -1):
                for x in range(comprimento - 1):
                    valor_atual = jogo_atual[y][x]
                    sequencia_atual = 1

                    for z in range(tamanho_sequencia, -1, -1):
                        if sequencia_atual == tamanho_sequencia:
                            return True

                        if y - tamanho_sequencia < 0 or x + tamanho_sequencia > comprimento - 1:
                            continue

                        if jogo_atual[y - z][x + z] == 0:
                            sequencia_atual = 1
                            valor_atual = jogo_atual[y - z][x + z]

                        if jogo_atual[y - z][x + z] == valor_atual:
                            sequencia_atual += 1
                        else:
                            sequencia_atual = 1
                            valor_atual = jogo_atual[y - z][x + z]

            return False

        def diagonal_direita_esquerda() -> bool:
            definicoes = self.model.obter_definicoes_do_jogo()
            altura = definicoes['altura']
            comprimento = definicoes['comprimento']
            tamanho_sequencia = definicoes['tamanho_sequencia']

            for y in range(altura - 1, -1, -1):
                for x in range(comprimento - 1, -1, - 1):
                    valor_atual = jogo_atual[y][x]
                    sequencia_atual = 1

                    for z in range(tamanho_sequencia):
                        if sequencia_atual == tamanho_sequencia:
                            return True

                        if y - tamanho_sequencia < -1 or x - tamanho_sequencia < -1:
                            continue

                        valor_posicao = jogo_atual[y - z][x - z]

                        if valor_posicao == 0:
                            sequencia_atual = 1
                            valor_atual = valor_posicao

                        if valor_posicao == valor_atual:
                            sequencia_atual += 1
                        else:
                            sequencia_atual = 1
                            valor_atual = valor_posicao

            return False

        return vertical() or horizontal() or diagonal_esquerda_direita() or diagonal_direita_esquerda()

    def validar_empate(self) -> bool:
        definicoes = self.model.obter_definicoes_do_jogo()
        total_jogadas = definicoes['comprimento'] * definicoes['altura']
        jogo_atual = self.model.obter_jogo()
        total_jogadas_do_jogo = 0

        for y in range(definicoes['altura']):
            total_jogadas_do_jogo += jogo_atual[y].count(1)
            total_jogadas_do_jogo += jogo_atual[y].count(2)

        return total_jogadas_do_jogo == total_jogadas

    @staticmethod
    def verificar_se_e_possivel_converter_para_inteiro(string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False

    def verificar_se_jogador_existe_pelo_nome(self, nome_do_jogador: str) -> bool:
        for jogador in self.model.obter_lista_de_jogadores():
            if jogador['nome'] == nome_do_jogador:
                return True
        return False

    def visualizar_jogo(self) -> bool:
        jogo_atual = self.model.obter_jogo()
        definicoes = self.model.obter_definicoes_do_jogo()
        altura = definicoes['altura']
        comprimento = definicoes['comprimento']

        if not len(self.model.obter_jogadores_em_jogo()):
            return False

        cabecalho = ['']
        linhas = []
        for x in range(comprimento):
            cabecalho.append(x + 1)

        for y in range(altura):
            linha = []
            for x in range(comprimento):
                match jogo_atual[y][x]:
                    case 1:
                        linha.append("\U0001F534")
                    case 2:
                        linha.append("\U0001F7E1")
                    case default:
                        linha.append("\U000026AB")
            linha.insert(0, y + 1)
            linhas.append(linha)

        tab = PrettyTable(cabecalho)
        tab.add_rows(linhas)

        self.informador.info(tab)
        return True
