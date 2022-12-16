from Controller import *
from Model import *
from Informador import *


class View:
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model)
        self.informador = Informador()

    def main(self):
        self.controller.limpar_ecran()
        self.model.ler_dados_de_um_ficheiro('../dados.json')
        while True:
            self.controller.imprimir_menu()
            comando: str = input("Comando:")

            # Validar se o comando não vem vazio
            if len(comando) == 0:
                self.controller.limpar_ecran()
                continue

            separar: list[str] = comando.split(None, 1)
            instrucao: str = separar[0]

            match instrucao:
                case 'LJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Lista de Jogadores\n')
                    self.informador.predefinicao(json.dumps(self.model.obter_lista_de_jogadores(), indent=2))
                    self.controller.finalizar_instrucao()
                case 'RJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Registar um novo Jogador\n')
                    # Comando exemplo: RJ João Pedro
                    if len(separar) != 2:
                        self.informador.erro('O Comando RJ necessita de receber parametros.')
                        continue
                    # Guardar os todos os params
                    nome_do_jogador: str = separar[1].split(' ')[0]

                    self.informador.predefinicao(f'Registar jogador "{nome_do_jogador}".')

                    novo_jogador = self.controller.criar_novo_jogador(nome_do_jogador)
                    if self.controller.adicionar_jogador_a_lista_de_jogadores(novo_jogador):
                        self.informador.sucesso('Jogador registado com sucesso.')
                    else:
                        self.informador.erro('Jogador existente.')

                    self.controller.finalizar_instrucao()
                    pass
                case 'EJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Eliminar um Jogador\n')
                    if len(separar) != 2:
                        self.informador.erro('O Comando EJ necessita de receber parametros.')
                        continue
                    # Guardar os todos os params
                    nome_do_jogador: str = separar[1].split(' ')[0]

                    self.informador.predefinicao(f'Eliminar jogador "{nome_do_jogador}".')

                    if self.controller.eliminar_jogador_pelo_nome(nome_do_jogador):
                        self.informador.sucesso('Jogador removido com sucesso.')
                    else:
                        self.informador.erro('Jogador não existente.')
                    self.controller.finalizar_instrucao()
                    pass
                case 'D':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Desistir do Jogo\n')
                    self.controller.finalizar_instrucao()
                    pass
                case 'DJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Detalhes do Jogo\n')
                    self.informador.predefinicao(json.dumps(self.model.obter_definicoes_do_jogo(), indent=2))
                    self.controller.finalizar_instrucao()
                    pass
                case 'IJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Iniciar Jogo\n')
                    # Comando exemplo: IJ spars57 alexis_silvery 16 12 6 4 3
                    if len(separar) != 2:
                        self.informador.erro('O Comando IJ necessita de receber parametros.')
                        continue
                    # Guardar os todos os params
                    parametros: list[str] = separar[1].split(' ')
                    if self.controller.iniciar_jogo(parametros):
                        self.informador.sucesso(f'Jogo iniciado entre {parametros[0]} e {parametros[1]}')
                    self.controller.finalizar_instrucao()
                case 'CP':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Colocar Peça\n')
                    self.controller.finalizar_instrucao()
                    pass
                case 'G':
                    self.controller.inicializar_instrucao()

                    self.informador.predefinicao('Guardar num ficheiro\n')

                    if len(separar) != 2:
                        self.informador.erro('O Comando G necessita de receber parametros.')
                        continue

                    nome_do_ficheiro: str = separar[1].split(' ')[0]

                    if self.model.salvar_dados_em_ficheiro(nome_do_ficheiro):
                        self.informador.sucesso('Dados Salvos.')
                    else:
                        self.informador.erro('Ocorreu um erro na gravação.')

                    self.controller.finalizar_instrucao()
                case 'L':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Ler de um Ficheiro\n')
                    # Guardar dados no ficheiro
                    if len(separar) != 2:
                        self.informador.erro('O Comando L necessita de receber parametros.')
                        continue
                        # Guardar os todos os parametros
                    nome_do_ficheiro: str = separar[1].split(' ')[0]

                    if self.model.ler_dados_de_um_ficheiro(nome_do_ficheiro):
                        self.informador.sucesso('Jogo carregado.')
                    else:
                        self.informador.erro('Ocorreu um erro no carregamento.')

                    self.controller.finalizar_instrucao()
                case 'V':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Visualizar Jogo Atual\n')
                    if not self.controller.visualizar_jogo():
                        self.informador.erro('Não existe jogo em curso.')
                    self.controller.finalizar_instrucao()
                case 'sair':
                    exit()
                case default:
                    self.controller.inicializar_instrucao()
                    self.informador.erro('Instrução inválida.')
                    self.controller.finalizar_instrucao()
