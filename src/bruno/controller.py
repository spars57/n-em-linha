import os
from prettytable import PrettyTable


class Controller:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def verificar_se_e_possivel_converter_para_inteiro(string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def criar_matriz(altura: int, comprimento: int) -> list[list[int]]:
        matriz: list[list[int]] = []

        for h in range(altura):
            matriz.append([])
            for w in range(comprimento):
                matriz[h].append(0)

        return matriz

    @staticmethod
    def limpar_ecran() -> None:
        os.system('clear')

    def continuar_e_limpar_ecran(self) -> None:
        input('Clique ENTER para continuar e limpar o ecran')
        self.limpar_ecran()

    @staticmethod
    def imprimir_menu() -> None:
        print('Jogo do N em Linha:')
        print('IJ - Iniciar Jogo')
        print('RJ - Registar Jogador')
        print('EJ - Eliminar Jogador')
        print('LJ - Lista de Jogadores')
        print('D - Desitir de Jogo')
        print('DJ - Detalhes do Jogo')
        print('G - Guardar num ficheiro')
        print('L - Ler dados de um ficheiro')
        print('V - Visualizar Jogo')
        print('sair - Sair do Jogo')

    def iniciar_jogo(self, params: list[str]) -> bool:
        # Verificar se foram passados no minimo 6 parametros se não for temos um erro
        if len(params) < 6:
            print('Erro: O Comando IJ necessita de receber no minimo 6 parametros.')
            return False

        parametros: dict = {
            "nome_1": params[0],
            "nome_2": params[1],
            "comprimento": params[2],
            "altura": params[3],
            "tamanho_sequencia": params[4],
            # No caso de haverem mais de 6 parametros, todos os restantes são guardados no tamanho_peca
            "tamanho_peca": [i for i in range(len(params)) if i > 6]
        }

        # Validar se os dois primeiros parametros são válidos
        # Verificar se os jogadores existem e se não estão em jogo.
        nomes_dos_jogadores: list[str] = [parametros['nome_1'], parametros['nome_2']]

        # Para cada nome vamos validar se o jogador existe e pode jogar
        for nome in nomes_dos_jogadores:
            # Aqui fica a função que verifica se existe jogador
            # Aqui fica a função que verifica se existe um jogo em curso envolvendo os dois jogadores
            pass

        # Validar se o comprimento, altura e tamanho sequencia são válidos
        # Isto é se podem ser convertidos para número inteiro
        if not self.verificar_se_e_possivel_converter_para_inteiro(parametros['comprimento']):
            print(f'Erro: O valor <comprimento> deve ser inteiro."')
            return False

        if not self.verificar_se_e_possivel_converter_para_inteiro(parametros['altura']):
            print(f'Erro: O valor <altura> deve ser inteiro.')
            return False

        if not self.verificar_se_e_possivel_converter_para_inteiro(parametros['tamanho_sequencia']):
            print(
                f'Erro: O valor <tamanho_sequencia> deve ser inteiro."')
            return False

        # Converter valores para inteiro
        parametros['comprimento'], parametros['altura'], parametros['tamanho_sequencia'] = int(
            parametros['comprimento']), int(
            parametros['altura']), int(parametros['tamanho_sequencia'])

        # Validar se o tamanho da sequencia é válido
        if not parametros['tamanho_sequencia'] >= 0:
            print(f'Erro: O valor <tamanho_sequencia> deve ser um valor entre 0 e +infinito.')
            return False

        # Validar se o comprimento é maior ou ígual que o tamanho da sequencia
        if not parametros['tamanho_sequencia'] <= parametros['comprimento']:
            print(f'Erro: O valor <tamanho_sequencia> deve ser menor que o <comprimento>')
            return False

        # Validar se o comprimento é maior ou ígual que o tamanho da sequencia
        if not parametros['tamanho_sequencia'] <= parametros['comprimento']:
            print(f'Erro: O valor <tamanho_sequencia> deve ser menor que o <comprimento>')
            return False

        # Validar se a altura está dentro dos limites aceites
        if not parametros['comprimento'] // 2 <= parametros['altura'] <= parametros['comprimento']:
            print(f'Erro: O valor <altura> deve estar entre <comprimento / 2> e <comprimento>')
            return False

        # Validar se as peças especiais existem
        if not len(parametros['tamanho_peca']) == 0:
            # Validar se as peças especiais são válidas em termos de tamanho
            if not len(parametros['tamanho_peca']) < parametros['tamanho_sequencia']:
                print(
                    f'Erro: O número de peças especiais ultrapassa o limite de {parametros["tamanho_sequencia"] - 1}.')

            # Validar se todos os valores das peças especiais são positivos e inteiros e maiores que zero
            for peca_especial in parametros['tamanho_peca']:
                if not isinstance(peca_especial, int):
                    print(f'Erro: Valor {peca_especial} não é inteiro')
                if not peca_especial > 0:
                    print(f'Erro: Valor {peca_especial} não é maior que 0')

        # Esta matriz terá que ser salva nos dados do jogo:
        self.model.atualizar_jogo(self.criar_matriz(parametros['altura'], parametros['comprimento']))

        jogador1 = self.model.obter_jogador_pelo_nome(parametros["nome_1"])
        jogador2 = self.model.obter_jogador_pelo_nome(parametros["nome_2"])

        definicoes = {
            "jogadores": [jogador1, jogador2],
            "tamanho_sequencia": parametros['tamanho_sequencia'],
            "altura": parametros['altura'],
            "comprimento": parametros['comprimento'],
            "tamanho_peca": parametros['tamanho_peca'],
            "vez": 1,
        }

        self.model.atualizar_definicoes_do_jogo(definicoes)

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
                        print(sequencia_atual)
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

    def visualizar_jogo(self) -> None:
        jogo_atual = self.model.obter_jogo()
        definicoes = self.model.obter_definicoes_do_jogo()
        altura = definicoes['altura']
        comprimento = definicoes['comprimento']
        linha = ""

        cabecalho = ['']
        linhas = []
        for y in range(comprimento):
            cabecalho.append(y + 1)

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

        print(tab)
