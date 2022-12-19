import time

from prettytable import PrettyTable
from Informador import *
from Model import *
from Utilitarios import *


class Controller:
    def __init__(self, model: Model):
        self.model = model
        self.informador = Informador()
        self.utilitarios = Utilitarios()

    def adicionar_jogador_a_lista_de_jogadores(self, jogador: Jogador) -> bool:
        if self.model.lista_de_jogadores.obter_por_nome(jogador.obter_nome()):
            return False
        self.model.lista_de_jogadores.adicionar_jogador(jogador)
        return True

    def colocar_peca_na_matriz(self, coluna: int, valor: int) -> bool:
        j = self.model.jogo.obter()
        for y_ in range(self.model.definicoes_do_jogo.obter_altura() - 1, -1, -1):
            if j[y_][coluna] == 0:
                j[y_][coluna] = valor
                self.model.jogo.atualizar(j)
                return True
        return False

    def colocar_peca(self, parametros: list[any]) -> bool:

        # Validar se os parametros tem o comprimento minimo
        if not len(parametros) >= 3:
            self.informador.erro('O comando CP necessita de pelo menos 3 parametros.')
            return False

        jogador = self.model.lista_de_jogadores.obter_por_nome(parametros[0])

        # Validar se o nome do jogador é valido e se o jogador existe:
        if jogador is None:
            self.informador.erro(f'Jogador "{parametros[0]}" não existe.')
            return False

        # Validar existe algum jogo em curso:
        if not self.model.definicoes_do_jogo.obter_em_curso():
            self.informador.erro(f'Não existe jogo em curso.')
            return False

        # Validar se o jogador joga:
        if not jogador.obter_em_jogo():
            self.informador.erro(f'Jogador "{jogador.obter_nome()}" não participa no jogo em curso.')
            return False

        # Validar se a posição pode ser convertida para inteiro
        if not self.utilitarios.verificar_se_e_possivel_converter_para_inteiro(parametros[2]):
            self.informador.erro(f'O valor <posicao> deve ser inteiro.')
            return False

        # Validar se o tamanho_peca_que_vai_ser_colocada pode ser convertido para interio
        if not self.utilitarios.verificar_se_e_possivel_converter_para_inteiro(parametros[1]):
            self.informador.erro(f'O valor <tamanho_peca> deve ser inteiro.')
            return False

        coluna = int(parametros[2]) - 1
        tamanho_peca_que_vai_ser_colocada = int(parametros[1])

        # Validar se a posição está nos limites
        if not coluna >= 0 and coluna <= self.model.definicoes_do_jogo.obter_comprimento():
            self.informador.erro(f'Posição irregular.')
            return False

        # validar se é a vez do jogador
        nomes_dos_jogadores: list[Jogador] = self.model.lista_de_jogadores.obter_jogadores_em_jogo()

        # Se o nome do jogador corresponder ao nome do jogador 1 a vez atual é 1 senão é 2
        vez_atual = 1 if jogador.obter_nome() == nomes_dos_jogadores[0].obter_nome() else 2

        # Validar se é a vez do jogador em questão.
        if not vez_atual == self.model.definicoes_do_jogo.obter_vez():
            self.informador.erro(f'Não é a vez do jogador "{jogador.obter_nome()}"')
            return False

        # Caso exista sentido significa que se trata de uma peça especial
        if len(parametros) >= 4 and tamanho_peca_que_vai_ser_colocada > 1:
            sentido: str = parametros[3]
            # Verificar se o parametro sentido é válido:
            if not sentido.upper() == 'D' and not sentido.upper() == "E":
                self.informador.erro(f'O valor <sentido> deve "D" ou "E".')
                return False

            # Validar se o jogador pode utilizar a peça especial
            if tamanho_peca_que_vai_ser_colocada not in jogador.obter_pecas_especiais():
                self.informador.erro(
                    f'Peça com tamanho {tamanho_peca_que_vai_ser_colocada} não disponivel.\nPeças disponiveis: {jogador.obter_pecas_especiais()}')
                return False

            # Verificar se é possível colocar essa peça nas colunas pretendidas.

            for x in range(coluna,
                           coluna + tamanho_peca_que_vai_ser_colocada if sentido == 'D' else coluna - tamanho_peca_que_vai_ser_colocada,
                           1 if sentido == 'D' else -1):
                if x < 0 or x > self.model.definicoes_do_jogo.obter_comprimento() - 1:
                    self.informador.erro('O valor ultrapassa os limites laterais do jogo.')
                    return False

                if not self.colocar_peca_na_matriz(x, 0):
                    self.informador.erro('Uma das colunas já se encontra completa.')
                    return False

            # Caso seja possivel introduzimos os valores nas colunas:
            for x in range(coluna,
                           coluna + tamanho_peca_que_vai_ser_colocada if sentido == 'D' else coluna - tamanho_peca_que_vai_ser_colocada,
                           1 if sentido == 'D' else -1):
                self.colocar_peca_na_matriz(x, vez_atual)
            # Trocar a vez do jogador.
            self.model.definicoes_do_jogo.atualizar_vez(1 if vez_atual == 2 else 2)
            # Remover peça especial ao jogador.
            removido = False
            nova_lista_de_pecas = []
            for peca in jogador.obter_pecas_especiais():
                if not removido and peca == tamanho_peca_que_vai_ser_colocada:
                    removido = True
                else:
                    nova_lista_de_pecas.append(peca)
            jogador.atualizar_pecas_especiais(nova_lista_de_pecas)
            return True

        if tamanho_peca_que_vai_ser_colocada == 1:
            # Colocar a peca na matriz
            if self.colocar_peca_na_matriz(coluna, valor=vez_atual):
                # Trocar a vez do jogador.
                self.model.definicoes_do_jogo.atualizar_vez(1 if vez_atual == 2 else 2)
                return True
            else:
                self.informador.erro('Não foi possivel colocar a peça porque a coluna encontra-se cheia')
                return False

        self.informador.erro('Tamanho da peça inválido.')
        return False

    def desistir_do_jogo(self, nomes_dos_jogadores: list[str]) -> bool:
        def validacoes() -> bool:
            # Validar se existe um jogo em curso.
            if not self.model.definicoes_do_jogo.obter_em_curso():
                self.informador.erro('Não existe jogo em curso.')
                return False

            # Para cada um dos Jogadores são feitas as seguintes validações:
            for nome in nomes_dos_jogadores:
                jogador_analisado = self.model.lista_de_jogadores.obter_por_nome(nome)
                # Validar se jogador existe.
                if jogador_analisado is None:
                    self.informador.erro(f'Jogador "{nome}" não registado.')
                    return False
                # Validar se o jogador joga.
                if not jogador_analisado.obter_em_jogo():
                    self.informador.erro(f'Jogador "{nome}" não participa no jogo em curso')
                    return False
            return True

        # Verificar se as validações passaram
        if not validacoes():
            return False

        # Obter nomes dos jogadores em jogo.
        nomes_dos_jogadores_em_jogo: list[str] = self.model.definicoes_do_jogo.obter_jogadores()

        # Obter dicionarios jogadores através do nome
        jogador1: Jogador = self.model.lista_de_jogadores.obter_por_nome(nomes_dos_jogadores_em_jogo[0])
        jogador2: Jogador = self.model.lista_de_jogadores.obter_por_nome(nomes_dos_jogadores_em_jogo[1])

        numero_de_desistencias = [False, False]

        # Contar numero de desistencias para saber ser ambos desistiram
        for i in range(len(nomes_dos_jogadores_em_jogo)):
            jogador = self.model.lista_de_jogadores.obter_por_nome(nomes_dos_jogadores_em_jogo[i])
            if not jogador.obter_em_jogo():
                numero_de_desistencias[i] = True

        # Ambos os jogadores desistem
        if numero_de_desistencias == [True, True]:
            self.informador.aviso('Ambos os jogadores desistiram do jogo')
            jogador1.atualizar_numero_de_empates(jogador1.obter_numero_de_empates() + 1)
            jogador2.atualizar_numero_de_empates(jogador2.obter_numero_de_empates() + 1)

        # Jogador 2 desiste
        if numero_de_desistencias == [False, True]:
            jogador1.atualizar_numero_de_vitorias(jogador1.obter_numero_de_vitorias() + 1)
            jogador2.atualizar_numero_de_derrotas(jogador2.obter_numero_de_derrotas() + 1)

        # Jogador 1 desiste
        if numero_de_desistencias == [True, False]:
            jogador2.atualizar_numero_de_vitorias(jogador2.obter_numero_de_vitorias() + 1)
            jogador1.atualizar_numero_de_derrotas(jogador1.obter_numero_de_derrotas() + 1)

        # Atualizar o estado dos jogadores para "não joga"
        jogador2.atualizar_em_jogo(False)
        jogador1.atualizar_em_jogo(False)

        # Finalizar jogo
        self.model.definicoes_do_jogo.resetar()
        return True

    def eliminar_jogador_pelo_nome(self, nome_do_jogador: str) -> bool:
        # Verificar se o jogador existe pelo nome.
        if not self.model.lista_de_jogadores.verificar_se_jogador_existe_pelo_nome(nome_do_jogador):
            return False

        # Atualizar o estado de eliminado do jogador para True.
        for jogador in self.model.lista_de_jogadores.obter():
            if jogador.obter_nome() == nome_do_jogador:
                jogador.atualizar_eliminado(True)

        return True

    def finalizar_instrucao(self) -> None:
        """Esta função será executada no final de cada instrução"""
        self.informador.predefinicao('Clique ENTER para continuar e limpar o ecran.')
        input()
        self.utilitarios.limpar_ecran()

    def inicializar_instrucao(self) -> None:
        """Esta função será executada antes de cada instrução"""
        self.utilitarios.limpar_ecran()

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
            # No caso de haverem mais de 6 parametros, os restantes são guardados no tamanho_peca
            "tamanho_peca": []
        }

        for i in range(len(lista_de_parametros)):
            if i > 6:
                parametros['tamanho_peca'].append(lista_de_parametros[i])

        print('Lista de Parametros:', lista_de_parametros)
        print('Tamanho Peça:', parametros['tamanho_peca'])

        # Validar se os dois primeiros parametros são válidos
        # Verificar se os jogadores existem e se não estão em jogo.
        nomes_dos_jogadores: list[str] = [parametros['nome_1'], parametros['nome_2']]

        # Para cada nome vamos validar se o jogador existe e pode jogar
        for nome in nomes_dos_jogadores:
            if not self.model.lista_de_jogadores.obter_por_nome(nome):
                self.informador.erro(f'Jogador "{nome}" não registado')
                return False
            if self.model.lista_de_jogadores.obter_por_nome(nome).obter_em_jogo():
                self.informador.erro(f'Jogador "{nome}" encontra-se a jogar outro jogo.')
                return False

        # Validar se o comprimento, altura e tamanho sequencia são válidos
        if not self.utilitarios.verificar_se_e_possivel_converter_para_inteiro(parametros['comprimento']):
            self.informador.erro(f'O valor <comprimento> deve ser inteiro.')
            return False
        if not self.utilitarios.verificar_se_e_possivel_converter_para_inteiro(parametros['altura']):
            self.informador.erro(f'O valor <altura> deve ser inteiro.')
            return False
        if not self.utilitarios.verificar_se_e_possivel_converter_para_inteiro(parametros['tamanho_sequencia']):
            self.informador.erro(
                f'O valor <tamanho_sequencia> deve ser inteiro."')
            return False

        # Converter valores para inteiro
        parametros['comprimento'], parametros['altura'], parametros['tamanho_sequencia'] = int(
            parametros['comprimento']), int(
            parametros['altura']), int(parametros['tamanho_sequencia'])

        # Validar se o tamanho da sequência é válido
        if not parametros['tamanho_sequencia'] >= 0:
            self.informador.erro(f'O valor <tamanho_sequencia> deve ser um valor entre 0 e +infinito.')
            return False
        # Validar se o comprimento é maior ou ígual que o tamanho da sequência
        if not parametros['tamanho_sequencia'] <= parametros['comprimento']:
            self.informador.erro(f'O valor <tamanho_sequencia> deve ser menor que o <comprimento>')
            return False
        # Validar se o comprimento é maior ou ígual que o tamanho da sequência
        if not parametros['tamanho_sequencia'] <= parametros['comprimento']:
            self.informador.erro(f'O valor <tamanho_sequencia> deve ser menor que o <comprimento>')
            return False
        # Validar se a altura está dentro dos limites aceites
        if not parametros['comprimento'] // 2 <= parametros['altura'] <= parametros['comprimento']:
            self.informador.erro(f'O valor <altura> deve estar entre <comprimento / 2> e <comprimento>')
            return False

        # Validar se as peças especiais existem
        if not len(parametros['tamanho_peca']) == 0:
            # Validar se as peças especiais são válidas em tamanho
            if not len(parametros['tamanho_peca']) < parametros['tamanho_sequencia']:
                self.informador.erro(
                    f'O número de peças especiais ultrapassa o limite de {parametros["tamanho_sequencia"] - 1}.')
            # Validar se todos os valores das peças especiais são positivos, inteiros e maiores que zero
            for peca_especial in parametros['tamanho_peca']:
                if not isinstance(peca_especial, int):
                    self.informador.erro(f'Valor {peca_especial} não é inteiro')
                    return False
                if not peca_especial > 0:
                    self.informador.erro(f'Valor {peca_especial} não é maior que 0')
                    return False
        if self.model.definicoes_do_jogo.obter_em_curso():
            self.informador.erro('Existe um jogo em curso')
            return False
        # Obter jogadores pelo nome
        jogador1: Jogador = self.model.lista_de_jogadores.obter_por_nome(parametros['nome_1'])
        jogador2: Jogador = self.model.lista_de_jogadores.obter_por_nome(parametros['nome_2'])
        # Validar se os jogadores não foram eliminados
        if jogador1.obter_eliminado():
            self.informador.erro(f'Jogador "{jogador1.obter_nome()}" encontra-se eliminado e não pode jogar mais.')
            return False
        if jogador2.obter_eliminado():
            self.informador.erro(f'Jogador "{jogador2.obter_nome()}" encontra-se eliminado e não pode jogar mais.')
            return False
        # Atualizar jogadores para os colocar em jogo.
        jogador1.atualizar_em_jogo(True)
        jogador2.atualizar_em_jogo(True)

        # Atualizar as definicoes do jogo.
        self.model.definicoes_do_jogo.atualizar_jogadores([parametros['nome_1'], parametros['nome_2']])
        self.model.definicoes_do_jogo.atualizar_tamanho_sequencia(parametros['tamanho_sequencia']),
        self.model.definicoes_do_jogo.atualizar_altura(parametros['altura'])
        self.model.definicoes_do_jogo.atualizar_comprimento(parametros['comprimento'])
        self.model.definicoes_do_jogo.atualizar_pecas_especiais(parametros['tamanho_peca'])
        self.model.definicoes_do_jogo.atualizar_vez(1)
        self.model.definicoes_do_jogo.atualizar_em_curso(True)

        # Criar Matriz
        matriz = self.utilitarios.criar_matriz(parametros['altura'], parametros['comprimento'])
        self.model.jogo.atualizar(matriz)
        return True

    def imprimir_menu(self) -> None:
        self.informador.predefinicao('Jogo do N em Linha:')
        self.informador.predefinicao('IJ - Iniciar Jogo')
        self.informador.predefinicao('RJ - Registar Jogador')
        self.informador.predefinicao('EJ - Eliminar Jogador')
        self.informador.predefinicao('LJ - Lista de Jogadores')
        self.informador.predefinicao('CP - Colocar Peca')
        self.informador.predefinicao('D - Desitir de Jogo')
        self.informador.predefinicao('DJ - Detalhes do Jogo')
        self.informador.predefinicao('G - Guardar num ficheiro')
        self.informador.predefinicao('L - Ler dados de um ficheiro')
        self.informador.predefinicao('V - Visualizar Jogo')
        self.informador.predefinicao('sair - Sair do Jogo')

    def registar_jogador(self, nome_do_jogador) -> bool:
        # Verificar se jogador existe.
        if self.model.lista_de_jogadores.obter_por_nome(nome_do_jogador) is not None:
            return False
        # Criar Jogador.
        novo_jogador = Jogador()
        # Alterar o nome do novo jogador para o nome pretendido.
        novo_jogador.atualizar_nome(nome_do_jogador)
        # Adicionar jogador à lista de jogadores.
        self.model.lista_de_jogadores.adicionar_jogador(novo_jogador)
        return True

    def mostrar_lista_de_jogadores(self) -> None:
        for jogador in self.model.lista_de_jogadores.obter():
            # O json é usado aqui para imprimir os dicionarios bonitos.
            self.informador.predefinicao(json.dumps(jogador.obter(), indent=2))

    def validar_vitoria(self) -> bool:
        jogo_atual = self.model.jogo.obter()

        altura = self.model.definicoes_do_jogo.obter_altura()
        comprimento = self.model.definicoes_do_jogo.obter_comprimento()
        tamanho_sequencia = self.model.definicoes_do_jogo.obter_tamanho_sequencia()

        def vertical() -> bool:
            peca_atual = 0
            sequencia_atual = 0
            for y in range(altura - 1, -1, -1):
                for x in range(comprimento):
                    if sequencia_atual >= tamanho_sequencia:
                        return True

                    sequencia_atual = 0 if jogo_atual[y][x] == 0 else sequencia_atual
                    sequencia_atual = 1 if peca_atual != jogo_atual[y][x] else sequencia_atual + 1
                    peca_atual = jogo_atual[y][x] if peca_atual != jogo_atual[y][x] else peca_atual
            return False

        def horizontal() -> bool:
            peca_atual = 0
            sequencia_atual = 0
            for x in range(comprimento):
                for y in range(altura - 1, -1, -1):
                    if sequencia_atual >= tamanho_sequencia:
                        return True

                    sequencia_atual = 0 if jogo_atual[y][x] == 0 else sequencia_atual
                    sequencia_atual = 1 if peca_atual != jogo_atual[y][x] else sequencia_atual + 1
                    peca_atual = jogo_atual[y][x] if peca_atual != jogo_atual[y][x] else peca_atual
            return False

        def diagonal_esquerda_direita() -> bool:
            total_ciclos = 0
            processados = []

            y_inicial = altura - 1
            y_final = tamanho_sequencia - 2
            y_passo = -1

            x_inicial = 0
            x_final = comprimento - tamanho_sequencia + 1
            x_passo = 1

            z_inicial = 0
            z_final = altura
            z_passo = 1

            peca_atual = 0
            sequencia_atual = 0

            matriz_teste = self.utilitarios.criar_matriz(altura, comprimento)

            for y in range(y_inicial, y_final, y_passo):
                for x in range(x_inicial, x_final, x_passo):
                    for z in range(z_inicial, z_final, z_passo):
                        if sequencia_atual == tamanho_sequencia:
                            return True

                        if x + z >= comprimento:
                            continue
                        if y - z < 0:
                            continue
                        if (y - z, x + z) in processados:
                            continue

                        if peca_atual == 0:
                            sequencia_atual = 0

                        if peca_atual == jogo_atual[y - z][x + z]:
                            sequencia_atual += 1
                        else:
                            sequencia_atual = 1

                        peca_atual = jogo_atual[y - z][x + z]

                        processados.append((y - z, x + z))

                        total_ciclos += 1
                        matriz_teste[y - z][x + z] = 3
                        time.sleep(0.016)
                        self.utilitarios.limpar_ecran()
                        self.utilitarios.prettytable_matriz(matriz_teste, altura, comprimento)
                        self.informador.predefinicao(f'Total Ciclos: {total_ciclos}')
            return False

        def diagonal_direita_esquerda() -> bool:
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

        if vertical():
            self.informador.sucesso('Sequencia conseguida na vertical!')

        if horizontal():
            self.informador.sucesso('Sequencia conseguida na horizontal!')

        if diagonal_direita_esquerda():
            self.informador.sucesso('Sequencia conseguida na diagonal sentido direita -> esquerda!')
        if diagonal_esquerda_direita():
            self.informador.sucesso('Sequencia conseguida na diagonal sentido esquerda -> direita!')

        return vertical() or horizontal() or diagonal_esquerda_direita() or diagonal_direita_esquerda()

    def validar_empate(self) -> bool:
        definicoes = self.model.definicoes_do_jogo.obter()
        total_jogadas = definicoes['comprimento'] * definicoes['altura']
        jogo_atual = self.model.definicoes_do_jogo.obter()
        total_jogadas_do_jogo = 0

        for y in range(definicoes['altura']):
            total_jogadas_do_jogo += jogo_atual[y].count(1)
            total_jogadas_do_jogo += jogo_atual[y].count(2)

        return total_jogadas_do_jogo == total_jogadas

    def visualizar_jogo(self) -> bool:

        if not self.model.definicoes_do_jogo.obter_em_curso():
            return False

        jogo = self.model.jogo.obter()
        altura = self.model.definicoes_do_jogo.obter_altura()
        comprimento = self.model.definicoes_do_jogo.obter_comprimento()

        self.utilitarios.prettytable_matriz(jogo, altura, comprimento)

        return True
