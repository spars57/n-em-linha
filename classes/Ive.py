from Jogador import *
from ListaDeJogadores import *
lista = ListaDeJogadores()
class Ive: 
    def criar_jogador(nome: str) -> Jogador:
        return Jogador(nome)

    def registar_jogador_na_lista(jogador: Jogador, lista_jogadores: ListaDeJogadores) -> str:
        lista_jogadores.adicionar_jogador(jogador)
        return 'Jogador registado com sucesso.'


    def verificar_nome(nome):
        return lista.verificar_se_jogador_existe_pelo_nome(nome)

    def retornar_jogador(nome: str) -> dict:# vai buscar o jogador pelo nome
        # lista_jogadores.append(registar_jogador('ive'))
        return lista.obter_por_nome(nome)
        # print(a) 


    def eliminar_jogador(nome):
        lista_antiga: list[Jogador] = lista.dados
        lista_nova: list[Jogador] = [jogador for jogador in lista_antiga if jogador.obter_nome != nome]

        for jogador in lista_antiga:
            if jogador.obter_nome != nome:
                lista_nova.append(jogador)

        lista.dados = lista_nova

        
        # ['ive', 'bruno', 'alexis']
        # Eliminar alexis
        # eliminar_jogador('alexis')
        # ['ive', 'bruno']

        # lista = ListaDeJogadores()
        # []
        # lista.adicionar_jogador('Ive')
        # [Jogador('Ive')]

       

ive = Ive()

ive.criar_jogador('')