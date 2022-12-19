from Controller import *
from Model import *
from Informador import *
from Utilitarios import *


class View:
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model)
        self.informador = Informador()
        self.utilitarios = Utilitarios()

    def main(self):
        self.controller.utilitarios.limpar_ecran()
        print('IJ spars alexis_silvery 16 12 6 4 3')
        self.model.ler_dados_de_um_ficheiro('dados.json')
        while True:
            self.controller.imprimir_menu()
            comando: str = input("Comando:")
            # Validar se o comando não vem vazio
            if len(comando) == 0:
                self.utilitarios.limpar_ecran()
                continue
            separar: list[str] = comando.split(None, 1)
            instrucao: str = separar[0].upper()
            match instrucao:
                case 'LJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Lista de Jogadores\n')
                    self.controller.mostrar_lista_de_jogadores()
                    self.controller.finalizar_instrucao()
                case 'RJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Registar um novo Jogador\n')
                    # Comando exemplo: RJ João Pedro
                    if len(separar) != 2:
                        self.informador.erro('O Comando RJ necessita de receber parametros.')
                        self.controller.finalizar_instrucao()
                        continue
                    # Guardar os todos os params
                    nome_do_jogador: str = separar[1].split(' ')[0]
                    self.informador.predefinicao(f'Registar jogador "{nome_do_jogador}".')
                    if self.controller.registar_jogador(nome_do_jogador):
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
                        self.controller.finalizar_instrucao()
                        continue
                    # Guardar os todos os params
                    nome_do_jogador: str = separar[1].split(' ')[0]
                    self.informador.predefinicao(f'Eliminar jogador "{nome_do_jogador}".')
                    if self.controller.eliminar_jogador_pelo_nome(nome_do_jogador):
                        self.informador.sucesso('Jogador eliminado.')
                    else:
                        self.informador.erro('Jogador Inexistente.')
                    self.controller.finalizar_instrucao()
                    pass
                case 'D':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Desistir do Jogo\n')
                    if len(separar) != 2:
                        self.informador.erro('O Comando D necessita de receber parametros.')
                        self.controller.finalizar_instrucao()
                        continue
                        # Guardar os todos os params
                    nomes_dos_jogadores: list[str] = separar[1].split(' ')
                    if self.controller.desistir_do_jogo(nomes_dos_jogadores):
                        self.informador.sucesso('Desistência com sucesso. Jogo terminado.')
                    self.controller.finalizar_instrucao()
                    pass
                case 'DJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Detalhes do Jogo\n')
                    self.informador.predefinicao(self.model.definicoes_do_jogo.obter())
                    self.controller.finalizar_instrucao()
                    pass
                case 'IJ':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Iniciar Jogo\n')
                    # Comando exemplo: IJ spars alexis_silvery 16 12 6 4 3
                    if len(separar) != 2:
                        self.informador.erro('O Comando IJ necessita de receber parametros.')
                        self.controller.finalizar_instrucao()
                        continue
                    # Guardar os todos os params
                    parametros: list[str] = separar[1].split(' ')
                    if self.controller.iniciar_jogo(parametros):
                        self.informador.sucesso(f'Jogo iniciado entre {parametros[0]} e {parametros[1]}')
                    self.controller.finalizar_instrucao()
                case 'CP':
                    # CP spars 1 4
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Colocar Peça\n')
                    if len(separar) < 2:
                        self.informador.erro('O Comando G necessita de receber parametros.')
                        self.controller.finalizar_instrucao()
                        continue
                    parametros = separar[1].split(' ')
                    if self.controller.colocar_peca(parametros):
                        self.informador.sucesso('Peca inserida com sucesso.')
                        self.controller.visualizar_jogo()
                    self.controller.finalizar_instrucao()
                    pass
                case 'G':
                    self.controller.inicializar_instrucao()
                    self.informador.predefinicao('Guardar num ficheiro\n')
                    if len(separar) != 2:
                        self.informador.erro('O Comando G necessita de receber parametros.')
                        self.controller.finalizar_instrucao()
                        continue
                    nome_do_ficheiro = separar[1].split(' ')[0]
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
                        self.controller.finalizar_instrucao()
                        continue
                        # Guardar os todos os parametros
                    nome_do_ficheiro = separar[1].split(' ')[0]
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
