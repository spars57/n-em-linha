import json
import time

import utilitarios as utils
from classes.Jogador import Jogador
from classes.Model import Model

# FPS = secs / frames
FPS = 1 / 60


class Controller:
    def __init__(self, model: Model):
        self.model = model

    def colocar_peca_na_grelha_do_jogo(self, coluna: int, valor: int, grelha: list[list[int]]) -> bool:
        y: int
        for y in range(self.model.definicoes.altura - 1, -1, -1):
            if grelha[y][coluna] == 0:
                grelha[y][coluna] = valor
                # Caso estejamos a usar esta função apenas para validar se existe espaço.
                if valor == 0:
                    return True

                if y < self.model.definicoes.altura_maxima_ocupada:
                    self.model.definicoes.altura_maxima_ocupada = y
                if coluna > self.model.definicoes.comprimento_maximo_ocupado:
                    self.model.definicoes.comprimento_maximo_ocupado = coluna

                self.model.jogo.grelha[y][coluna] = grelha[y][coluna]
                return True
        return False

    def colocar_peca(self, parametros: list[any]) -> str:
        return ''

    def desistir_do_jogo(self, nomes_dos_jogadores: list[str]) -> str:

        nome: str
        for nome in nomes_dos_jogadores:
            jogador_analisado: Jogador = self.model.lista.obter(nome)
            if jogador_analisado is None:
                return 'Jogador não registado.'
            if not self.model.definicoes.em_curso:
                return 'Não existe jogo em curso.'
            if not jogador_analisado.em_jogo:
                return 'Jogador não participa no jogo em curso'

        # Obter nomes dos jogadores em jogo.
        nomes_dos_jogadores_em_jogo: list[str] = self.model.definicoes.nomes_dos_jogadores

        # Obter dicionarios jogadores através do nome
        jogador1: Jogador = self.model.lista.obter(nomes_dos_jogadores_em_jogo[0])
        jogador2: Jogador = self.model.lista.obter(nomes_dos_jogadores_em_jogo[1])

        # Lista que armazena o número de desistencias:
        # [0] = jogador1
        # [1] = jogador2
        numero_de_desistencias = [False, False]

        # Contar numero de desistencias para saber ser ambos desistiram
        i: int
        for i in range(len(nomes_dos_jogadores)):
            jogador: Jogador = self.model.lista.obter(nomes_dos_jogadores[i])

            if jogador.nome == jogador1.nome and jogador1.em_jogo:
                numero_de_desistencias[0] = True

            if jogador.nome == jogador2.nome and jogador2.em_jogo:
                numero_de_desistencias[1] = True

        # Ambos os jogadores desistem
        if numero_de_desistencias == [True, True]:
            jogador1.empates += 1
            jogador2.empates += 1

        # Jogador 2 desiste
        if numero_de_desistencias == [False, True]:
            jogador1.vitorias += 1
            jogador2.derrotas += 1
        # Jogador 1 desiste
        if numero_de_desistencias == [True, False]:
            jogador1.derrotas += 1
            jogador2.vitorias += 1

        # Atualizar o estado dos jogadores para "não joga"
        jogador1.em_jogo = False
        jogador2.em_jogo = False

        # Finalizar jogo
        self.model.definicoes.reset()
        return 'Desistência com sucesso. Jogo terminado.'

    def eliminar_jogador(self, nome_do_jogador: str) -> str:
        jogador: Jogador
        for jogador in self.model.lista.dados:
            if jogador.nome == nome_do_jogador:
                if jogador.em_jogo:
                    return 'Jogador participa no jogo em curso.'
                else:
                    jogador.eliminado = True
                    self.model.lista.remover(jogador.nome)
                    return 'Jogador removido com sucesso.'
        return 'Jogador não existente.'

    def iniciar_jogo(self, lista_de_parametros: list[str]) -> str:
        # Verificar se foram passados no minimo 6 parametros se não for temos um erro
        if len(lista_de_parametros) < 5:
            return ''

        parametros: dict = {
            "nome_1": lista_de_parametros[0],
            "nome_2": lista_de_parametros[1],
            "comprimento": lista_de_parametros[2],
            "altura": lista_de_parametros[3],
            "tamanho_sequencia": lista_de_parametros[4],
            "tamanho_peca": []
        }

        # Validar se existe um jogo em curso
        if self.model.definicoes.em_curso:
            return 'Existe um jogo em curso.'

        if parametros['nome_1'] == parametros['nome_2']:
            return 'Não foi possível iniciar o jogo.'

        # Verificar se os jogadores existem e se não estão em jogo.
        nomes_dos_jogadores: list[str] = [parametros['nome_1'], parametros['nome_2']]

        # Para cada nome vamos validar se o jogador existe e pode jogar
        for nome in nomes_dos_jogadores:
            if not self.model.lista.obter(nome):
                return 'Jogador não registado.'
            if self.model.lista.obter(nome).em_jogo:
                return 'Jogador não registado.'

        # Obter jogadores pelo nome
        jogador1: Jogador = self.model.lista.obter(parametros['nome_1'])
        jogador2: Jogador = self.model.lista.obter(parametros['nome_2'])

        # Validar se os jogadores não foram eliminados
        if jogador1.eliminado:
            return 'Jogador não registado.'
        if jogador2.eliminado:
            return 'Jogador não registado.'

        # Validar se o comprimento e altura são inteiros
        if not utils.verificar_se_e_possivel_converter_para_inteiro(parametros['comprimento']):
            return 'Dimensões de grelha invalidas.'
        if not utils.verificar_se_e_possivel_converter_para_inteiro(parametros['altura']):
            return 'Dimensões de grelha invalidas.'

        # Converter Altura e Comprimento para Inteiro:
        parametros['comprimento'] = int(parametros['comprimento'])
        parametros['altura'] = int(parametros['altura'])

        # Validar se são números positivos
        if not parametros['altura'] >= 0:
            return 'Dimensões de grelha invalidas.'

        if not parametros['comprimento'] >= 0:
            return 'Dimensões de grelha invalidas.'

        # Validar se a altura está dentro dos limites aceites
        if not parametros['comprimento'] // 2 <= parametros['altura'] <= parametros['comprimento']:
            return 'Dimensões de grelha invalidas.'

        # Validar se o tamanho sequencia é inteiro.
        if not utils.verificar_se_e_possivel_converter_para_inteiro(parametros['tamanho_sequencia']):
            return 'Tamanho de sequência invalido.'

        # Converter tamanho sequencia para inteiro
        parametros['tamanho_sequencia'] = int(parametros['tamanho_sequencia'])

        # Validar se o tamanho da sequência é válido
        if not parametros['tamanho_sequencia'] >= 0:
            return 'Tamanho de sequência invalido.'

        # Validar se o comprimento é maior ou ígual que o tamanho da sequência
        if not parametros['tamanho_sequencia'] <= parametros['comprimento']:
            return 'Tamanho de sequência invalido.'

        # Validar se o comprimento é maior ou ígual que o tamanho da sequência
        if not parametros['tamanho_sequencia'] <= parametros['comprimento']:
            return 'Tamanho de sequência invalido.'

        # No caso de haverem mais de 6 parametros, os restantes são guardados no tamanho_peca se forem numeros inteiros
        for i in range(len(lista_de_parametros)):
            if i >= 5:
                # Validar se são numeros inteiros
                if not utils.verificar_se_e_possivel_converter_para_inteiro(lista_de_parametros[i]):
                    return 'Dimensões de peças especiais invalidas.'
                # se TODOS os números forem inteiros então TODOS são adicionados às peças especiais.
                parametros['tamanho_peca'].append(int(lista_de_parametros[i]))

        # Atualizar jogadores para os colocar em jogo.
        jogador1.em_jogo = True
        jogador2.em_jogo = True

        # Atualizar pecas especiais dos jogadores
        jogador1.pecas_especiais = parametros['tamanho_peca']
        jogador2.pecas_especiais = parametros['tamanho_peca']

        # Atualizar as definicoes do jogo.
        self.model.definicoes.nomes_dos_jogadores = [parametros['nome_1'], parametros['nome_2']]
        self.model.definicoes.tamanho_sequencia = parametros['tamanho_sequencia']
        self.model.definicoes.altura = parametros['altura']
        self.model.definicoes.comprimento = parametros['comprimento']
        self.model.definicoes.pecas_especiais = parametros['tamanho_peca']
        self.model.definicoes.vez = 1
        self.model.definicoes.em_curso = True
        self.model.definicoes.altura_maxima_ocupada = parametros['altura']
        self.model.definicoes.comprimento_maximo_ocupado = 0

        # Atualizar numero de espacos livres na matriz
        self.model.definicoes.espacos_livres = parametros['altura'] * parametros['comprimento']
        # Atualizar numero de espacos ocupados na matriz
        self.model.definicoes.espacos_ocupados = 0
        # Atualizar Jogo.
        self.model.jogo.grelha = utils.criar_matriz(parametros['altura'], parametros['comprimento'])

        return f'Jogo iniciado entre {jogador1.nome} e {jogador2.nome}.'

    def registar_jogador(self, nome_do_jogador) -> str:
        # Verificar se jogador existe.
        if self.model.lista.obter(nome_do_jogador) is not None:
            return 'Jogador existente.'
        # Criar Jogador.
        novo_jogador = Jogador()
        # Alterar o nome do novo jogador para o nome pretendido.
        novo_jogador.nome = nome_do_jogador
        # Adicionar jogador à lista de jogadores.
        self.model.lista.adicionar(novo_jogador)
        return 'Jogador registado com sucesso.'

    def validar_vitoria(self) -> bool:

        jogo_atual = self.model.jogo.grelha
        altura = self.model.definicoes.altura
        comprimento = self.model.definicoes.comprimento
        y_minimo = self.model.definicoes.altura_maxima_ocupada
        x_maximo = self.model.definicoes.comprimento_maximo_ocupado + 1
        tamanho_sequencia = self.model.definicoes.tamanho_sequencia
        maximo_ciclos = altura * comprimento * 4

        def horizontal() -> bool:

            contador_de_ciclos = 0

            peca_atual = 0
            sequencia_atual = 0

            y_inicial = altura - 1
            y_final = -1
            y_passo = -1

            x_inicial = 0
            x_final = comprimento
            x_passo = 1

            matriz_teste = utils.criar_matriz(altura, comprimento)

            if x_maximo < tamanho_sequencia:
                return False

            y: int
            for y in range(y_inicial, y_final, y_passo):

                if y < y_minimo:
                    continue

                x: int
                for x in range(x_inicial, x_final, x_passo):
                    if x >= x_maximo:
                        continue

                    if sequencia_atual == tamanho_sequencia:
                        return True

                    sequencia_atual = 1 if jogo_atual[y][x] == 0 else sequencia_atual
                    sequencia_atual = 1 if peca_atual != jogo_atual[y][x] else sequencia_atual + 1
                    peca_atual = jogo_atual[y][x] if peca_atual != jogo_atual[y][x] else peca_atual
                    matriz_teste[y][x] = 3

                    contador_de_ciclos += 1
                    time.sleep(FPS)
                    utils.limpar_ecran()
                    print(
                        f'A verificar vitória na horizontal ({round((contador_de_ciclos / maximo_ciclos) * 100)}%)')
                    # utils.prettytable_matriz(matriz_teste, altura, comprimento)
            utils.limpar_ecran()
            return False

        def vertical() -> bool:

            contador_de_ciclos = 0

            peca_atual = 0
            sequencia_atual = 0

            y_inicial = altura - 1
            y_final = -1
            y_passo = -1

            x_inicial = 0
            x_final = comprimento
            x_passo = 1

            matriz_teste = utils.criar_matriz(altura, comprimento)

            if y_minimo > altura - tamanho_sequencia:
                return False

            x: int
            for x in range(x_inicial, x_final, x_passo):
                if x >= x_maximo:
                    continue

                y: int
                for y in range(y_inicial, y_final, y_passo):
                    if y < y_minimo:
                        continue

                    if sequencia_atual >= tamanho_sequencia:
                        return True

                    sequencia_atual = 0 if jogo_atual[y][x] == 0 else sequencia_atual
                    sequencia_atual = 1 if peca_atual != jogo_atual[y][x] else sequencia_atual + 1
                    peca_atual = jogo_atual[y][x] if peca_atual != jogo_atual[y][x] else peca_atual

                    contador_de_ciclos += 1
                    matriz_teste[y][x] = 3

                    time.sleep(FPS)
                    utils.limpar_ecran()
                    print(
                        f'A verificar vitória na vertical ({round((contador_de_ciclos / maximo_ciclos) * 100) + 25}%)')

                    # utils.prettytable_matriz(matriz_teste, altura, comprimento)
            utils.limpar_ecran()
            return False

        def diagonal_esquerda_direita() -> bool:

            contador_de_ciclos = 0

            processados = []
            peca_atual = 0
            sequencia_atual = 0

            y_inicial = altura - 1
            y_final = tamanho_sequencia - 2
            y_passo = -1

            x_inicial = 0
            x_final = comprimento - tamanho_sequencia + 1
            x_passo = 1

            incremento_inicial = 0
            incremento_final = altura
            incremento_passo = 1

            if y_minimo > altura - tamanho_sequencia:
                return False

            if x_maximo < tamanho_sequencia:
                return False

            matriz_teste = utils.criar_matriz(altura, comprimento)

            y: int
            for y in range(y_inicial, y_final, y_passo):
                x: int
                for x in range(x_inicial, x_final, x_passo):
                    incremento: int
                    for incremento in range(incremento_inicial, incremento_final, incremento_passo):
                        if sequencia_atual == tamanho_sequencia:
                            return True

                        # Restrições do dominio da função f(x,y,z)
                        if x + incremento >= comprimento:
                            continue
                        if y - incremento < 0:
                            continue
                        if y - incremento < y_minimo:
                            continue
                        if x + incremento >= x_maximo:
                            continue

                        # Se o valor já tiver sido processado não será processado novamente, isto é para evitar repetições.
                        if (y - incremento, x + incremento) in processados:
                            continue
                        else:
                            # Adicionar valor aos processados
                            processados.append((y - incremento, x + incremento))

                        if peca_atual == 0:
                            sequencia_atual = 0
                        if peca_atual == jogo_atual[y - incremento][x + incremento]:
                            sequencia_atual += 1
                        else:
                            sequencia_atual = 1

                        peca_atual = jogo_atual[y - incremento][x + incremento]

                        contador_de_ciclos += 1
                        matriz_teste[y - incremento][x + incremento] = 3

                        time.sleep(FPS)
                        utils.limpar_ecran()
                        print(
                            f'A verificar vitória na diagonal ({round((contador_de_ciclos / maximo_ciclos) * 100) + 50}%)')

                        # utils.prettytable_matriz(matriz_teste, altura, comprimento)
            utils.limpar_ecran()
            return False

        def diagonal_direita_esquerda() -> bool:

            contador_de_ciclos = 0

            processados = []
            peca_atual = 0
            sequencia_atual = 0

            y_inicial = altura - 1
            y_final = tamanho_sequencia - 2
            y_passo = -1

            x_inicial = comprimento - 1
            x_final = tamanho_sequencia - 2
            x_passo = - 1

            incremento_inicial = 0
            incremento_final = altura
            incremento_passo = 1

            matriz_teste = utils.criar_matriz(altura, comprimento)

            if y_minimo > altura - tamanho_sequencia:
                return False

            if x_maximo < tamanho_sequencia:
                return False

            y: int
            for y in range(y_inicial, y_final, y_passo):
                x: int
                for x in range(x_inicial, x_final, x_passo):
                    incremento: int
                    for incremento in range(incremento_inicial, incremento_final, incremento_passo):
                        if sequencia_atual == tamanho_sequencia:
                            return True

                        # Restrições do dominio da função f(x,y,z)
                        if x - incremento < 0:
                            continue
                        if y - incremento < 0:
                            continue
                        if x - incremento >= x_maximo:
                            continue
                        if y - incremento < y_minimo:
                            continue

                        # Se o valor já tiver sido processado não será processado novamente, isto é para evitar repetições.
                        if (y - incremento, x - incremento) in processados:
                            continue
                        else:
                            # Adicionar valor aos processados
                            processados.append((y - incremento, x - incremento))

                        if peca_atual == 0:
                            sequencia_atual = 0
                        if peca_atual == jogo_atual[y - incremento][x - incremento]:
                            sequencia_atual += 1
                        else:
                            sequencia_atual = 1

                        peca_atual = jogo_atual[y - incremento][x - incremento]

                        contador_de_ciclos += 1
                        matriz_teste[y - incremento][x - incremento] = 3

                        time.sleep(FPS)
                        utils.limpar_ecran()
                        print(
                            f'A verificar vitória na diagonal ({round((contador_de_ciclos / maximo_ciclos) * 100) + 75}%)')
                        # utils.prettytable_matriz(matriz_teste, altura, comprimento)
            utils.limpar_ecran()
            return False

        return horizontal() or vertical() or diagonal_esquerda_direita() or diagonal_direita_esquerda()

    def validar_empate(self) -> bool:
        return self.model.definicoes.espacos_livres - \
               self.model.definicoes.espacos_ocupados == 0

    def visualizar_jogo(self) -> str:
        if not self.model.definicoes.em_curso:
            return 'Não existe jogo em curso'

    def mostrar_lista_de_jogadores(self) -> str:
        if len(self.model.lista.dados) == 0:
            return 'Não existem jogadores registados.'
        return json.dumps([jogador.__dict__ for jogador in self.model.lista.dados], indent=2)
