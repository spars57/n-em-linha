from Controller import *
from Model import *
from Utilitarios import *
from Informador import *


class View:
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model)
        self.utilitarios = Utilitarios()
        self.informador = Informador()

    def main(self):
        self.utilitarios.limpar_ecran()
        while True:
            self.utilitarios.imprimir_menu()
            comando: str = input("Comando:")
            # Validar se o comando não vem vazio
            if len(comando) == 0:
                self.utilitarios.limpar_ecran()
                continue
            separar: list[str] = comando.split(None, 1)
            instrucao: str = separar[0].upper()

            match instrucao:
                case 'LJ':
                    self.utilitarios.inicializar_instrucao()
                    print(self.controller.mostrar_lista_de_jogadores())
                    self.utilitarios.finalizar_instrucao()

                case 'RJ':
                    self.utilitarios.inicializar_instrucao()
                    if len(separar) < 2:
                        continue
                    nome_do_jogador: str = separar[1].split()[0]
                    self.informador.predefinicao(self.controller.registar_jogador(nome_do_jogador))
                    self.utilitarios.finalizar_instrucao()

                case 'EJ':
                    self.utilitarios.inicializar_instrucao()
                    if len(separar) < 2:
                        continue
                    nome_do_jogador: str = separar[1].split()[0]
                    self.informador.predefinicao(self.controller.eliminar_jogador(nome_do_jogador))

                case 'D':
                    self.utilitarios.inicializar_instrucao()
                    if len(separar) < 2:
                        continue
                    nomes_dos_jogadores: list[str] = separar[1].split()
                    self.informador.predefinicao(self.controller.desistir_do_jogo(nomes_dos_jogadores))
                    self.utilitarios.finalizar_instrucao()
                    pass

                case 'DJ':
                    self.utilitarios.inicializar_instrucao()
                    self.informador.predefinicao(self.model.definicoes_do_jogo.json())
                    self.utilitarios.finalizar_instrucao()
                    pass

                case 'IJ':
                    self.utilitarios.inicializar_instrucao()
                    if len(separar) < 2:
                        continue
                    parametros: list[str] = separar[1].split()
                    self.informador.predefinicao(self.controller.iniciar_jogo(parametros))
                    self.utilitarios.finalizar_instrucao()

                case 'CP':
                    self.utilitarios.inicializar_instrucao()
                    if len(separar) < 2:
                        self.utilitarios.finalizar_instrucao()
                        continue
                    parametros = separar[1].split()
                    self.informador.predefinicao(self.controller.colocar_peca(parametros))
                    self.utilitarios.finalizar_instrucao()

                case 'G':
                    self.utilitarios.inicializar_instrucao()
                    if len(separar) < 2:
                        continue
                    nome_do_ficheiro = separar[1].split(' ')[0]
                    self.informador.predefinicao(self.model.salvar_dados_em_ficheiro(nome_do_ficheiro))
                    self.utilitarios.finalizar_instrucao()

                case 'L':
                    self.utilitarios.inicializar_instrucao()
                    if len(separar) < 2:
                        continue
                    nome_do_ficheiro = separar[1].split(' ')[0]
                    self.informador.predefinicao(self.model.ler_dados_de_um_ficheiro(nome_do_ficheiro))
                    self.utilitarios.finalizar_instrucao()

                case 'V':
                    self.utilitarios.inicializar_instrucao()
                    if not self.controller.visualizar_jogo():
                        self.informador.erro('Não existe jogo em curso.')
                        self.utilitarios.finalizar_instrucao()
                        continue

                    jogo = self.model.jogo.grelha
                    altura = self.model.definicoes_do_jogo.altura
                    comprimento = self.model.definicoes_do_jogo.comprimento

                    self.utilitarios.prettytable_matriz(jogo, altura, comprimento)
                    self.utilitarios.finalizar_instrucao()

                case 'AJUDA':
                    self.utilitarios.inicializar_instrucao()
                    print("RJ Nome")
                    print("EJ Nome")
                    print("LJ")
                    print("IJ Nome Nome Comprimento Altura TamanhoSequência[ TamanhoPeça TamanhoPeça TamanhoPeça ...]")
                    print("DJ")
                    print("D Nome[ Nome]")
                    print("CP Nome TamanhoPeça Posição[ Sentido]")
                    print("V")
                    print("G NomeFicheiro")
                    print("L NomeFicheiro")
                    self.utilitarios.finalizar_instrucao()

                case 'SAIR':
                    exit()

                case default:
                    self.utilitarios.inicializar_instrucao()
                    self.informador.predefinicao(f'Instrução inválida.')
                    self.utilitarios.finalizar_instrucao()
