import json
import random
import sys
import os
from rich import print

import pandas as pd


#               BASE DE DADOS

# dados das armaduras (dicionario)
with open("armor.json", "r", encoding="utf8") as fd:
    armaduras = json.load(fd)
# dataframe do dicionario contendo os dados das armaduras |pandas
df_armaduras = pd.DataFrame(armaduras).T
df_armaduras.columns.name = 'armor_name'


# dados das armas (dicionario)
with open("weapons.json", "r", encoding="utf8") as fd:
    armas = json.load(fd)
# dataframe do dicionario contendo os dados das armas |pandas
df_armas = pd.DataFrame(armas).T
df_armas.columns.name = 'weapon_name'


# lista com os dados dos atributos
with open("attributes.json", "r", encoding="utf8") as fd:
    atributos = json.load(fd)


#               FICHA DOS PERSONAGENS

# ALTERNATIVA PARA O CAMINHO DAS FICHAS DE PERSONAGEM POR INPUT

# arquivo1 = sys.argv[1]
# arquivo2 = sys.argv[2]


arquivo1 = input("Digite o nome do arquivo da ficha do primeiro personagem: ")
with open(arquivo1, "r", encoding="utf8") as fd:
	ficha_personagem1 = json.load(fd)

arquivo2 = input("Digite o nome do arquivo da ficha do segundo personagem: ")
with open(arquivo2, "r", encoding="utf8") as fd:
	ficha_personagem2 = json.load(fd)


with open('neymar.json', "r", encoding="utf8") as fd:
	ficha_personagem1 = json.load(fd)

with open('mbappe.json', "r", encoding="utf8") as fd:
	ficha_personagem2 = json.load(fd)







# FICHAS DE TESTE
ficha_personagem1 = {
    'name': 'Mbappe',
    'strength': 20,
    'dexterity': 14,
    'armor': 'plate',
    'weapon': 'maul',
    'shield': True,
    'HP': 50
}

ficha_personagem2 = {
    'name': 'Neymar',
    'strength': 18,
    'dexterity': 20,
    'armor': 'half plate',
    'weapon': 'rapier',
    'shield': True,
    'HP': 50
}


# dataframe com os dados dos dois personagens
df_personagens = pd.DataFrame((ficha_personagem1, ficha_personagem2))

#               REGRAS
# o personagem com maior destreza ataca primeiro
perso1 = df_personagens.sort_values(by='dexterity', ascending=False).iloc[0]
perso2 = df_personagens.sort_values(by='dexterity', ascending=False).iloc[1]

# classe de armadura (AC)
for personagem in (perso1, perso2):

    # criando os bonus de força e destreza dos personagens
    personagem['bonus_forca'] = atributos[personagem.strength]
    personagem['bonus_destreza'] = atributos[personagem.dexterity]

    # criando a clase de armadura (AC) dos personagens de acordo com a armadura utilizada
    personagem['AC'] = df_armaduras['AC'][personagem.armor]

    # armadura leve (light) = somar o bônus de destreza do personagem à sua classe de armadura.
    if (df_armaduras.loc[personagem.armor].type) == 'light':
        personagem.AC += personagem.bonus_destreza

    # armadura media (medium) = somar ate dois pontos do bônus de destreza do personagem à sua AC.
    elif (df_armaduras.loc[personagem.armor].type) == 'medium':
        personagem.AC += min(personagem.bonus_destreza, 2)

    # armadura pesada (heavy) = nao somar o bônus de destreza do personagem à sua AC.
    elif (df_armaduras.loc[personagem.armor].type) == 'heavy':
        personagem.AC = personagem.AC

    # arma de uma mao (sem 2-hand) e usar shield = recebe +2 na AC
    if (df_armas.props[personagem.weapon] != ['2-hand']) and personagem.shield:
        personagem.AC += 2
        
        



# simula a rolagem do dado
def joga_dado(dado):
    ''' Recebe a string do num de lados e simula a rolagem de dados '''
    # desmembrando o damage e pegando o num de lados 'x' do dado
    x = int((dado.split('d'))[1])
    return random.randint(1, x)

# rolagem de ataque


def ataque(personagem):
    ''' Recebe um personagem e calcula seu ataque '''

    print('\nRolagem de ataque do personagem {}:'.format(personagem['name']))

    d20 = joga_dado('d20')
    print(f'    Resultado da rolagem do d20 = {d20}')

    # se a arma tiver 'finesse' = o bonus é o maior valor entre forca e destreza
    if (df_armas.loc[personagem.weapon].props == ['finesse']):
        ataque_total = d20 + max(personagem.bonus_forca,
                                 personagem.bonus_destreza)
        print("    A arma do personagem possui a propriedade 'finesse'!")
        if max(personagem.bonus_forca, personagem.bonus_destreza) == personagem.bonus_forca:
            print('    Bonus aplicado (bonus de força) = {}'.format(
                personagem.bonus_forca))
        else:
            print('    Bonus aplicado (bonus de destreza) = {}'.format(
                personagem.bonus_destreza))
    else:
        # somar o bônus de força do personagem ao total do seu ataque
        ataque_total = d20 + personagem.bonus_forca
        print("    A arma do personagem não possui a propriedade 'finesse'!")
        print(
            f'    Bonus aplicado (bonus de força) = {personagem.bonus_forca}')

    print(
        f'    Resultado total do ataque (d20 + bonus aplicado) = {ataque_total}')

    return ataque_total

# rolagem de dano


def dano(personagem):
    ''' Recebe um personagem e calcula seu dano'''

    print('\nRolagem de dano do personagem {}:'.format(personagem['name']))

    dado_dano_arma = df_armas.loc[personagem.weapon].damage
    dano_arma = joga_dado(dado_dano_arma)

    print('    Dado de dano do personagem = {}'.format(
        df_armas.loc[personagem.weapon].damage))
    print('    Resultado da rolagem do {} = {}'.format(
        df_armas.loc[personagem.weapon].damage, dano_arma))

    # se a arma tiver 'finesse' = o bonus é o maior valor entre forca e destreza
    if (df_armas.loc[personagem.weapon].props == ['finesse']):
        print("    A arma do personagem possui a propriedade 'finesse'!")
        dano_total = dano_arma + \
            max(personagem.bonus_forca, personagem.bonus_destreza)
        if max(personagem.bonus_forca, personagem.bonus_destreza) == personagem.bonus_forca:
            print('    Bonus aplicado (bonus de força) = {}'.format(
                personagem.bonus_forca))
        else:
            print('    Bonus aplicado (bonus de destreza) = {}'.format(
                personagem.bonus_destreza))
    else:
        # somar o bônus de força do personagem ao total do seu dano
        print("    A arma do personagem não possui a propriedade 'finesse'!")
        dano_total = dano_arma + personagem.bonus_forca
        print(
            f'    Bonus aplicado (bonus de força) = {personagem.bonus_forca}')

    print('    Resultado total do dano ({} + bonus aplicado) = {}'.format(
        df_armas.loc[personagem.weapon].damage, dano_total))

    return dano_total


#               SIMULAÇÃO DO COMBATE

# simula o turno de um personagem
def turno(i, atacante, alvo, hp_alvo):
    ''' Simula o turno de um personagem e retorna o valor do HP restante do alvo ao final do turno'''

    print('\n\n-------- Inicio do turno {} do personagem {} --------'.format(i,
          atacante['name']))

    ataque_atacante = ataque(atacante)

    print('\nClasse de armadura (AC) do alvo (personagem {}) = {}'.format(
        alvo['name'], alvo.AC))

    if ataque_atacante > alvo.AC:
        print('\n[green]O ataque acertou o alvo!!![/]')

        dano_atacante = dano(atacante)

        hp_alvo -= dano_atacante

    else:
        print('\nO ataque não acertou o alvo!!!')

    print(f'\nPontos de vida (HP) restantes do alvo = {hp_alvo}')

    return hp_alvo

# simula o combate dos dois personagens


def simula_combate():
    ''' Simula o combate dos dois personagens e printa o resultado final '''
    hp1 = perso1.HP
    hp2 = perso2.HP
    i = 1

    while hp1 > 0 and hp2 > 0:

        hp2 = turno(i, perso1, perso2, hp2)
        if hp2 <= 0:
            break

        hp1 = turno(i, perso2, perso1, hp1)
        if hp1 <= 0:
            break

        i += 1

    # mensagem final
    print('\n\n******** COMBATE TERMINADO!!! ********')
    if hp1 <= 0:
        print('Vencedor: {}'.format(perso2['name']))
        print(f'Pontos de vida (HP) restantes: {hp2}')
    elif hp2 <= 0:
        print('Vencedor: {}'.format(perso1['name']))
        print(f'Pontos de vida (HP) restantes: {hp1}')
    print(f'Total de turnos realizados: {i}\n')


def limpa_terminal():
    ''' Limpa o terminal de qualquer sistema operacional'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def finalizar_progama():
    print('Progama finalizado!\n ')
    exit()


def mensagem_inicial():
    print('------ SIMULADOR DE COMBATE D&D ------')
    input("Pressione a tecla 'ENTER' para continuar  ")

# verifica de o usuario deseja jogar novamente


def jogar_novamente():
    ''' Verifica se o usuario deseja jogar novamente e retorna o valor do 'sair' '''
    resposta_valida = False

    while resposta_valida == False:

        rodar_novamente = input('Deseja simular o combate novamente (s/n)? ')

        if rodar_novamente == 'n':
            finalizar_progama()
            resposta_valida = True
            sair = True

        elif rodar_novamente == 's':
            resposta_valida = True
            sair = False

        else:
            print('\nResposta inválida!')
            print("Digite 's' para 'sim' ou 'n' para não\n")

    return sair


sair = False
while sair == False:

    limpa_terminal()

    mensagem_inicial()

    simula_combate()

    sair = jogar_novamente()
