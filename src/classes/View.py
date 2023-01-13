from classes.Controller import Controller
from classes.Model import Model
from tools import utilitarios as utils


class View:
    def __init__(self):
        self.controller = Controller()
        
    def main(self):
        model = Model()
        utils.limpar_ecran()
        while True:
            utils.imprimir_menu()
            comando: str = input("Comando:")
            # Validar se o comando não vem vazio
            if len(comando) == 0:
                utils.limpar_ecran()
                continue

            separar: list[str] = comando.split(None, 1)
            instrucao: str = separar[0].upper()

            match instrucao:
                case 'LJ':
                    utils.inicializar_instrucao()
                    print(self.controller.mostrar_lista_de_jogadores(model))
                    utils.finalizar_instrucao()

                case 'RJ':
                    utils.inicializar_instrucao()
                    if len(separar) < 2:
                        print('Instrução Invalida')
                        utils.finalizar_instrucao()
                        continue
                    nome_do_jogador: str = separar[1].split()[0]
                    print(self.controller.registar_jogador(model, nome_do_jogador))
                    utils.finalizar_instrucao()

                case 'EJ':
                    utils.inicializar_instrucao()
                    if len(separar) < 2:
                        print('Instrução Invalida')
                        utils.finalizar_instrucao()
                        continue
                    nome_do_jogador: str = separar[1].split()[0]
                    print(self.controller.eliminar_jogador(model, nome_do_jogador))
                    utils.finalizar_instrucao()

                case 'D':
                    utils.inicializar_instrucao()
                    if len(separar) < 2:
                        print('Instrução Invalida')
                        utils.finalizar_instrucao()
                        continue
                    nomes_dos_jogadores: list[str] = separar[1].split()
                    print(self.controller.desistir_do_jogo(model, nomes_dos_jogadores))
                    utils.finalizar_instrucao()
                    pass

                case 'DJ':
                    utils.inicializar_instrucao()
                    print(self.controller.mostrar_detalhes_do_jogo(model))
                    utils.finalizar_instrucao()
                    pass

                case 'IJ':
                    utils.inicializar_instrucao()
                    if len(separar) < 2:
                        print('Instrução Invalida')
                        utils.finalizar_instrucao()
                        continue
                    parametros: list[str] = separar[1].split()
                    print(self.controller.iniciar_jogo(model, parametros))
                    utils.finalizar_instrucao()

                case 'CP':
                    utils.inicializar_instrucao()
                    if len(separar) < 2:
                        print('Instrução Invalida')
                        utils.finalizar_instrucao()
                        continue
                    parametros = separar[1].split()
                    print(self.controller.colocar_peca(model, parametros))
                    utils.finalizar_instrucao()

                case 'G':
                    utils.inicializar_instrucao()
                    if len(separar) < 2:
                        print('Instrução Invalida')
                        utils.finalizar_instrucao()
                        continue
                    nome_do_ficheiro = separar[1].split()[0]
                    print(model.salvar(nome_do_ficheiro))
                    utils.finalizar_instrucao()

                case 'L':
                    utils.inicializar_instrucao()
                    if len(separar) < 2:
                        print('Instrução Invalida')
                        utils.finalizar_instrucao()
                        continue
                    nome_do_ficheiro = separar[1].split()[0]
                    print(model.ler(nome_do_ficheiro))
                    utils.finalizar_instrucao()

                case 'V':
                    utils.inicializar_instrucao()
                    visualizar = self.controller.visualizar_jogo(model)
                    if visualizar is not None:
                        print(visualizar)
                        utils.finalizar_instrucao()
                        continue

                    jogo = model.jogo.grelha
                    altura = model.definicoes.altura
                    comprimento = model.definicoes.comprimento

                    utils.prettytable_matriz(jogo, altura, comprimento)
                    utils.finalizar_instrucao()

                case 'AJUDA':
                    utils.inicializar_instrucao()
                    utils.imprimir_ajuda()
                    utils.finalizar_instrucao()

                case 'SAIR':
                    exit()

                case _:
                    utils.inicializar_instrucao()
                    print(f'Instrução inválida.')
                    utils.finalizar_instrucao()
