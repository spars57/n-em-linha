from model import lista_jogadores
def registar_jogador(nome: str):
              
 jogador = {'nome':nome, 'vitorias':0, 'derrotas':0,  'empates':0, 'em_jogo':True, 'eliminado':False}
 return jogador


def verificar_nome(nome, lista_jogadores): # verificar se o jogador existe 
    for dicionario in lista_jogadores : 
        if dicionario['nome'] == nome: 
            return True 
    return False
def retornar_jogador(nome: str, lista_jogadores: list) -> dict:# vai buscar o jogador pelo nome
     for jogador in lista_jogadores:
        if jogador['nome'] == nome: 
            return jogador

lista_jogadores.append(registar_jogador('ive'))
a= retornar_jogador('ive', lista_jogadores)
print(a) 

lista= []

def eliminar_jogador(nome, lista ):
    if not  verificar_nome (nome, lista):
        return False
    # falta uma função para verificar se o jofador esta a jogar 

    for jogador in lista: 
    #percorrer a lista 
        if 