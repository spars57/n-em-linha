from controller import *
import random

nome = input(' Bem-Vindo ao Jogo ')
if verificar_nome(nome, lista_jogadores):
    print(f'Utilizador já existente escolha outro nome')
else:
    lista_jogadores.append(jogador)
    print(lista_jogadores)
    for i, item in lista_jogadores:
        print(i, item)
    if cmd == 'RJ':
        nome1 = input(f'Digite nome do jogador 1: ')

    while verificar_nome(nome1, lista_jogadores) == False:
        nome1 = input(f'Digite nome do jogador 1: ')
        nome2 = input(f'Gigite nome do jogador 2 ')
    while verificar_nome(nome2, lista_jogadores) == False:
        nome2 = input(f'Digite nome do jogador 2: ')