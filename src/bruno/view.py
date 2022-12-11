from controller import *
from model import *

if __name__ == '__main__':
    model = Model()
    controller = Controller(model)
    controller.limpar_ecran()

    while True:
        controller.imprimir_menu()
        instrucao: str = input("Comando:")

        # Validar se o comando não vem vazio
        if len(instrucao) == 0:
            continue

        separar: list[str] = instrucao.split(None, 1)
        instrucao: str = separar[0]

        match instrucao:
            case 'RJ':
                controller.limpar_ecran()
                print('REGISTAR JOGADOR\n')
                controller.continuar_e_limpar_ecran()
                pass
            case 'EJ':
                controller.limpar_ecran()
                print('ELIMINAR JOGADOR\n')
                controller.continuar_e_limpar_ecran()
                pass
            case 'D':
                controller.limpar_ecran()
                print('DESISTIR DO JOGO\n')
                controller.continuar_e_limpar_ecran()
                pass
            case 'DJ':
                controller.limpar_ecran()
                print('DETALHES DO JOGO\n')
                print(json.dumps(model.obter_definicoes_do_jogo(), indent=2))
                controller.continuar_e_limpar_ecran()
                pass

            case 'IJ':
                controller.limpar_ecran()
                print('INICIAR JOGO\n')
                # Comando exemplo: IJ a b 16 12 6 4 3
                if len(separar) != 2:
                    print('Erro: O Comando IJ necessita de receber parametros')
                    continue
                # Guardar os todos os params
                params: list[str] = separar[1].split(' ')
                controller.iniciar_jogo(params)
                controller.continuar_e_limpar_ecran()
            case 'CP':
                controller.limpar_ecran()
                print('COLOCAR PEÇA\n')
                controller.continuar_e_limpar_ecran()
                pass
            case 'G':
                controller.limpar_ecran()

                print('GUARDAR\n')

                if len(separar) != 2:
                    print('Erro: O Comando G necessita de receber parametros')
                    continue

                ficheiro: str = separar[1].split(' ')[0]

                if model.salvar_dados_em_ficheiro(ficheiro):
                    print('Dados Salvos')

                controller.continuar_e_limpar_ecran()

            case 'L':
                controller.limpar_ecran()
                print('LER\n')
                # Guardar dados no ficheiro
                if len(separar) != 2:
                    print('Erro: O Comando L necessita de receber parametros')
                    continue
                    # Guardar os todos os params
                ficheiro: str = separar[1].split(' ')[0]

                if model.ler_dados_de_um_ficheiro(ficheiro):
                    print('Dados carregados com sucesso')

                controller.continuar_e_limpar_ecran()

            case 'V':
                controller.limpar_ecran()
                print('VISUALIZAR\n')
                controller.visualizar_jogo()
                controller.continuar_e_limpar_ecran()

            case 'sair':
                exit()

            case default:
                controller.limpar_ecran()
                print('Instrução inválida')
                controller.continuar_e_limpar_ecran()
