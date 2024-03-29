import time
from collections import OrderedDict

from prettytable import PrettyTable

from classes.Jogador import Jogador
from classes.Model import Model
from tools import utilitarios as utils

# FPS = secs / frames
FPS = 1 / 60


class Controller:

    @staticmethod
    def reset(model: Model) -> None:
        model.definicoes.reset()
        model.jogo.reset()

        jogador: Jogador
        for jogador in model.lista.obter_jogadores_em_jogo():
            jogador.em_jogo = False

    @staticmethod
    def colocar_peca_na_grelha_do_jogo(model: Model, coluna: int, valor: int, grelha: list[list[int]]) -> bool:
        # Esta função é auxiliar do comando CP, foi desenvolvida pelo Alexandre.
        y: int
        for y in range(model.definicoes.altura - 1, -1, -1):
            if grelha[y][coluna] == 0:
                grelha[y][coluna] = valor
                # Caso estejamos a usar esta função apenas para validar se existe espaço.
                if valor == 0:
                    return True

                if y < model.definicoes.altura_maxima_ocupada:
                    model.definicoes.altura_maxima_ocupada = y
                if coluna > model.definicoes.comprimento_maximo_ocupado:
                    model.definicoes.comprimento_maximo_ocupado = coluna

                model.jogo.grelha[y][coluna] = grelha[y][coluna]
                return True
        return False

    def colocar_peca(self, model: Model, parametros: list[any]) -> str:

        # Validar se os parametros tem o comprimento minimo
        if not len(parametros) >= 3:
            return 'Instrução Invalida.'

        # Validar existe algum jogo em curso:
        if not model.definicoes.em_curso:
            return 'Não existe jogo em curso.'

        jogador: Jogador = model.lista.obter(parametros[0])

        # Validar se o nome do jogador é valido e se o jogador existe:
        if jogador is None:
            return 'Jogador não registado.'

        # validar se é a vez do jogador
        nomes_dos_jogadores: list[Jogador] = model.lista.obter_jogadores_em_jogo(
        )

        vez_atual: int = 1 if jogador.nome == nomes_dos_jogadores[0].nome else 2

        # Validar se é a vez do jogador em questão.
        if not vez_atual == model.definicoes.vez:
            return 'Não é a vez do jogador.'

        # Validar se o jogador joga:
        if not jogador.em_jogo:
            return 'Jogador não participa no jogo em curso.'

        # Validar se o tamanho_peca_que_vai_ser_colocada pode ser convertido para interio
        if not utils.verificar_se_e_possivel_converter_para_inteiro(parametros[1]):
            return 'Tamanho de peça não disponivel.'

        tamanho_peca_que_vai_ser_colocada = int(parametros[1])

        # Validar se a posição pode ser convertida para inteiro
        if not utils.verificar_se_e_possivel_converter_para_inteiro(parametros[2]):
            return 'Posição irregular.'

        coluna = int(parametros[2]) - 1

        # Validar se a posição está nos limites
        if not coluna >= 0 and coluna <= model.definicoes.comprimento:
            return 'Posição irregular.'

        # Caso exista sentido significa que se trata de uma peça especial
        if len(parametros) >= 4 and tamanho_peca_que_vai_ser_colocada > 1:
            sentido: str = parametros[3]
            # Validar se o jogador pode utilizar a peça especial
            if tamanho_peca_que_vai_ser_colocada not in jogador.pecas_especiais:
                return 'Tamanho de peça não disponivel.'
            # Verificar se o parametro sentido é válido:
            if not sentido.upper() == 'D' and not sentido.upper() == "E":
                return 'Posição irregular.'

            # Verificar se é possível colocar essa peça nas colunas pretendidas.
            x: int
            for x in range(coluna,
                           coluna + tamanho_peca_que_vai_ser_colocada if sentido == 'D' else coluna -
                           tamanho_peca_que_vai_ser_colocada,
                           1 if sentido == 'D' else -1):
                if x < 0 or x > model.definicoes.comprimento - 1:
                    return 'Posição irregular.'

                if not self.colocar_peca_na_grelha_do_jogo(model, x, 0, model.jogo.grelha):
                    return 'Posição irregular.'

            # Caso seja possivel introduzimos os valores nas colunas:
            x: int
            for x in range(coluna,
                           coluna + tamanho_peca_que_vai_ser_colocada if sentido == 'D' else coluna -
                           tamanho_peca_que_vai_ser_colocada,
                           1 if sentido == 'D' else -1):
                self.colocar_peca_na_grelha_do_jogo(
                    model, x, vez_atual, model.jogo.grelha)
            # Trocar a vez do jogador.
            model.definicoes.vez = 2 if model.definicoes.vez == 1 else 1

            # Remover peça especial ao jogador.
            removido: bool = False
            nova_lista_de_pecas: list[int] = []

            peca: int
            for peca in jogador.pecas_especiais:
                if not removido and peca == tamanho_peca_que_vai_ser_colocada:
                    removido = True
                else:
                    nova_lista_de_pecas.append(peca)
            jogador.pecas_especiais = nova_lista_de_pecas

            # Aumentar numero de espacos ocupados
            model.definicoes.espacos_ocupados += tamanho_peca_que_vai_ser_colocada

            if self.validar_vitoria(model):
                self.reset(model)
                return "Sequência conseguida. Jogo terminado."
            return 'Peça colocada.'

        if tamanho_peca_que_vai_ser_colocada == 1:
            # Colocar a peca na matriz
            if self.colocar_peca_na_grelha_do_jogo(model, coluna, vez_atual, model.jogo.grelha):
                # Trocar a vez do jogador.
                model.definicoes.vez = 2 if model.definicoes.vez == 1 else 1
                # Aumentar numero de espacos ocupados
                model.definicoes.espacos_ocupados += 1
                if self.validar_vitoria(model):
                    self.reset(model)
                    return "Sequência conseguida. Jogo terminado."
                return 'Peça colocada.'
            else:
                return 'Posição irregular.'

        return 'Tamanho da peça inválido.'

    @staticmethod
    def desistir_do_jogo(model: Model, nomes_dos_jogadores: list[str]) -> str:
        # Esta funcionalidade foi feita pelo Bruno.
        nome: str
        for nome in nomes_dos_jogadores:
            jogador_analisado: Jogador = model.lista.obter(nome)
            if jogador_analisado is None:
                return 'Jogador não registado.'
            if not model.definicoes.em_curso:
                return 'Não existe jogo em curso.'
            if not jogador_analisado.em_jogo:
                return 'Jogador não participa no jogo em curso.'

        # Obter nomes dos jogadores em jogo.
        nomes_dos_jogadores_em_jogo: list[str] = model.definicoes.nomes_dos_jogadores

        # Obter dicionarios jogadores através do nome
        jogador1: Jogador = model.lista.obter(nomes_dos_jogadores_em_jogo[0])
        jogador2: Jogador = model.lista.obter(nomes_dos_jogadores_em_jogo[1])

        # Lista que armazena o número de desistencias:
        # [0] = jogador1
        # [1] = jogador2
        numero_de_desistencias = [False, False]

        # Contar numero de desistencias para saber ser ambos desistiram
        i: int
        for i in range(len(nomes_dos_jogadores)):
            jogador: Jogador = model.lista.obter(nomes_dos_jogadores[i])

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
        model.definicoes.reset()
        return 'Desistência com sucesso. Jogo terminado.'

    @staticmethod
    def eliminar_jogador(model: Model, nome_do_jogador: str) -> str:
        # Esta funcionalidade foi feita pela Ive
        jogador: Jogador
        for jogador in model.lista.dados:
            if jogador.nome == nome_do_jogador:
                if jogador.em_jogo:
                    return 'Jogador participa no jogo em curso.'
                else:
                    model.lista.remover(jogador.nome)
                    return 'Jogador removido com sucesso.'
        return 'Jogador não existente.'

    @staticmethod
    def iniciar_jogo(model: Model, lista_de_parametros: list[str]) -> str:
        # Esta funcionalidade foi feita pelo Bruno

        # Verificar se foram passados no minimo 6 parametros se não for temos um erro
        if len(lista_de_parametros) < 5:
            return 'Instrução Invalida.'

        parametros: dict = {
            "nome_1": lista_de_parametros[0],
            "nome_2": lista_de_parametros[1],
            "comprimento": lista_de_parametros[2],
            "altura": lista_de_parametros[3],
            "tamanho_sequencia": lista_de_parametros[4],
            "tamanho_peca": []
        }

        # Validar se existe um jogo em curso
        if model.definicoes.em_curso:
            return 'Existe um jogo em curso.'

        if parametros['nome_1'] == parametros['nome_2']:
            return 'Não foi possível iniciar o jogo.'

        # Verificar se os jogadores existem e se não estão em jogo.
        nomes_dos_jogadores: list[str] = [
            parametros['nome_1'], parametros['nome_2']]

        # Para cada nome vamos validar se o jogador existe e pode jogar
        for nome in nomes_dos_jogadores:
            if not model.lista.obter(nome):
                return 'Jogador não registado.'
            if model.lista.obter(nome).em_jogo:
                return 'Jogador não registado.'

        # Obter jogadores pelo nome
        jogador1: Jogador = model.lista.obter(parametros['nome_1'])
        jogador2: Jogador = model.lista.obter(parametros['nome_2'])

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
                if int(lista_de_parametros[i]) > parametros['tamanho_sequencia'] or int(
                        lista_de_parametros[i]) <= 0:
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
        model.definicoes.nomes_dos_jogadores = [
            parametros['nome_1'], parametros['nome_2']]
        model.definicoes.tamanho_sequencia = parametros['tamanho_sequencia']
        model.definicoes.altura = parametros['altura']
        model.definicoes.comprimento = parametros['comprimento']
        model.definicoes.pecas_especiais = parametros['tamanho_peca']
        model.definicoes.vez = 1
        model.definicoes.em_curso = True
        model.definicoes.altura_maxima_ocupada = parametros['altura']
        model.definicoes.comprimento_maximo_ocupado = 0

        # Atualizar numero de espacos livres na matriz
        model.definicoes.espacos_livres_total = parametros['altura'] * \
            parametros['comprimento']
        # Atualizar numero de espacos ocupados na matriz
        model.definicoes.espacos_ocupados = 0
        # Atualizar Jogo.
        model.jogo.grelha = utils.criar_matriz(
            parametros['altura'], parametros['comprimento'])

        return f'Jogo iniciado entre {jogador1.nome} e {jogador2.nome}.'

    @staticmethod
    def registar_jogador(model: Model, nome_do_jogador: str) -> str:
        # Esta funcionalidade foi feita pela Ive

        # Verificar se jogador existe.
        if model.lista.obter(nome_do_jogador) is not None:
            return 'Jogador existente.'
        # Criar Jogador.
        novo_jogador = Jogador()
        # Alterar o nome do novo jogador para o nome pretendido.
        novo_jogador.nome = nome_do_jogador
        # Adicionar jogador à lista de jogadores.
        model.lista.adicionar(novo_jogador)
        return 'Jogador registado com sucesso.'

    @staticmethod
    def validar_vitoria(model: Model) -> bool:
        # Esta funcionalidade foi feita pelo Bruno.
        jogo_atual = model.jogo.grelha
        altura = model.definicoes.altura
        comprimento = model.definicoes.comprimento
        y_minimo = model.definicoes.altura_maxima_ocupada
        x_maximo = model.definicoes.comprimento_maximo_ocupado + 1
        tamanho_sequencia = model.definicoes.tamanho_sequencia
        maximo_ciclos = altura * comprimento * 4

        jogadores: list[Jogador] = model.lista.obter_jogadores_em_jogo()

        jogador1: Jogador = jogadores[0]
        jogador2: Jogador = jogadores[1]

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

            if model.definicoes.espacos_ocupados < model.definicoes.tamanho_sequencia:
                return False

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
                        if peca_atual == 1:
                            jogador1.vitorias += 1
                            jogador2.derrotas += 1
                        else:
                            jogador2.vitorias += 1
                            jogador1.derrotas += 1

                        utils.limpar_ecran()
                        return True

                    sequencia_atual = 1 if jogo_atual[y][x] == 0 else sequencia_atual
                    sequencia_atual = 1 if peca_atual != jogo_atual[y][x] else sequencia_atual + 1
                    peca_atual = jogo_atual[y][x] if peca_atual != jogo_atual[y][x] else peca_atual

                    contador_de_ciclos += 1
                    time.sleep(FPS)
                    utils.limpar_ecran()
                    print(
                        f'A verificar vitória na horizontal ({round((contador_de_ciclos / maximo_ciclos) * 100)}%)')
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

                    if sequencia_atual == tamanho_sequencia:
                        if peca_atual == 1:
                            jogador1.vitorias += 1
                            jogador2.derrotas += 1
                        else:
                            jogador2.vitorias += 1
                            jogador1.derrotas += 1

                        utils.limpar_ecran()
                        return True

                    sequencia_atual = 0 if jogo_atual[y][x] == 0 else sequencia_atual
                    sequencia_atual = 1 if peca_atual != jogo_atual[y][x] else sequencia_atual + 1
                    peca_atual = jogo_atual[y][x] if peca_atual != jogo_atual[y][x] else peca_atual

                    contador_de_ciclos += 1

                    time.sleep(FPS)
                    utils.limpar_ecran()
                    print(
                        f'A verificar vitória na vertical ({round((contador_de_ciclos / maximo_ciclos) * 100) + 25}%)')

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

            y: int
            for y in range(y_inicial, y_final, y_passo):
                x: int
                for x in range(x_inicial, x_final, x_passo):
                    incremento: int
                    for incremento in range(incremento_inicial, incremento_final, incremento_passo):
                        if sequencia_atual == tamanho_sequencia:
                            if peca_atual == 1:
                                jogador1.vitorias += 1
                                jogador2.derrotas += 1
                            else:
                                jogador2.vitorias += 1
                                jogador1.derrotas += 1

                            utils.limpar_ecran()
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
                            processados.append(
                                (y - incremento, x + incremento))

                        if peca_atual == 0:
                            sequencia_atual = 0
                        if peca_atual == jogo_atual[y - incremento][x + incremento]:
                            sequencia_atual += 1
                        else:
                            sequencia_atual = 1

                        peca_atual = jogo_atual[y - incremento][x + incremento]

                        contador_de_ciclos += 1

                        time.sleep(FPS)
                        utils.limpar_ecran()
                        print(
                            f'A verificar vitória na diagonal ({round((contador_de_ciclos / maximo_ciclos) * 100) + 50}%)')

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
                            if peca_atual == 1:
                                jogador1.vitorias += 1
                                jogador2.derrotas += 1
                            else:
                                jogador2.vitorias += 1
                                jogador1.derrotas += 1

                            utils.limpar_ecran()
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
                            processados.append(
                                (y - incremento, x - incremento))

                        if peca_atual == 0:
                            sequencia_atual = 0
                        if peca_atual == jogo_atual[y - incremento][x - incremento]:
                            sequencia_atual += 1
                        else:
                            sequencia_atual = 1

                        peca_atual = jogo_atual[y - incremento][x - incremento]

                        contador_de_ciclos += 1

                        time.sleep(FPS)
                        utils.limpar_ecran()
                        print(
                            f'A verificar vitória na diagonal ({round((contador_de_ciclos / maximo_ciclos) * 100) + 75}%)')
            utils.limpar_ecran()
            return False

        resultado = horizontal() or vertical() or diagonal_esquerda_direita() or diagonal_direita_esquerda()
        return resultado

    @staticmethod
    def validar_empate(model: Model, ) -> bool:
        return model.definicoes.espacos_livres_total == 0

    @staticmethod
    def visualizar_jogo(model: Model, ) -> str:
        if not model.definicoes.em_curso:
            return 'Não existe jogo em curso.'

    @staticmethod
    def mostrar_lista_de_jogadores(model: Model) -> PrettyTable | str:
        # Esta funcionalidade foi feita pela Ive.
        if len(model.lista.dados) == 0:
            return 'Não existem jogadores registados.'
        cabecalho = ["Nome", "Vitorias", "Derrotas", "Empates", "Jogos Jogados"]
        linhas = []
        lista_atual = model.lista.dados
        for jogador in lista_atual:
            total_jogos = jogador.vitorias + jogador.derrotas + jogador.empates
            linha = [jogador.nome, jogador.vitorias,
                     jogador.derrotas, jogador.empates, total_jogos]
            linhas.append(linha)
        # PrettyTable é uma classe que cria tabelas
        tabela = PrettyTable(cabecalho)
        tabela.add_rows(linhas)  # add_rows add linhas
        return tabela

        # Este código foi desenvolvido em fase de testes, ficou aqui por precaução.
        #
        # if len(model.lista.dados) == 0:
        #     return 'Não existem jogadores registados.'

        # lista: list[dict] = sorted([jogador.__dict__ for jogador in model.lista.dados], key=lambda j: j['nome'])
        # cabecalho: list[str] = [k.replace('_', ' ').title() for k in lista[0].keys()]
        # linhas: list[list[str]] = []

        # try:
        #     cabecalho.remove('pecas_especiais'.replace('_', ' ').title())
        #     cabecalho.remove('em_jogo'.replace('_', ' ').title())
        #     cabecalho.remove('eliminado'.replace('_', ' ').title())
        # except ValueError:
        #     pass

        # jogador: Jogador
        # for index in range(len(lista)):
        #     linhas.append([])
        #     for key in cabecalho:
        #         linhas[index].append(lista[index][key.replace(' ', '_').lower()])

        # tab = PrettyTable(cabecalho)
        # tab.add_rows(linhas)
        # return tab

    @staticmethod
    def mostrar_detalhes_do_jogo(model: Model, ) -> PrettyTable | str:
        if not model.definicoes.em_curso:
            return 'Não existe jogo em curso.'

        cabecalho: list[str] = ['Chave', 'Valor']
        tab = PrettyTable(cabecalho)

        definicoes_dict: dict = OrderedDict(
            sorted(model.definicoes.__dict__.items()))

        jogadores_em_jogo = model.lista.obter_jogadores_em_jogo()

        key: str
        for key in definicoes_dict.keys():
            tab.add_row([key.replace('_', ' ').title(), definicoes_dict[key]])

        jogador: Jogador
        for jogador in jogadores_em_jogo:
            tab.add_row(
                [f'Pecas especiais do Jogador {jogador.nome}', jogador.pecas_especiais])

        return tab
