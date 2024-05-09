import json
import random
import sys
import os
import pandas as pd
from time import sleep

# classe que contem os codigos das cores
class cor:
    # \033[estilo; texto; fundo+m  \033[m
    # estilo -> 0 = nenhum, 1 = negrito, 4 = sublinhado, 7 = invertido
    # texto -> 30(branco), 31(vermelho), 32(verde), 33(amarelo), 34(azul), 35(roxo), 36(ciano), 37(cinza)
    # fundo -> 40(branco), 41(vermelho), 42(verde), 43(amarelo), 44(azul), 45(roxo), 46(ciano), 47(cinza)

    branco = '\033[30m'
    vermelho = '\033[31m'
    verde = '\033[32m'
    amarelo = '\033[33m'
    azul = '\033[34m'
    roxo = '\033[35m'
    ciano = '\033[36m'
    cinza = '\033[37m'

    branco_neg = '\033[1;30m'
    vermelho_neg = '\033[1;31m'
    verde_neg = '\033[1;32m'
    amarelo_neg = '\033[1;33m'
    azul_neg = '\033[1;34m'
    roxo_neg = '\033[1;35m'
    ciano_neg = '\033[1;36m'
    cinza_neg = '\033[1;37m'

    branco_sub = '\033[4;30m'
    vermelho_sub = '\033[4;31m'
    verde_sub = '\033[4;32m'
    amarelo_sub = '\033[4;33m'
    azul_sub = '\033[4;34m'
    roxo_sub = '\033[4;35m'
    ciano_sub = '\033[4;36m'
    cinza_sub = '\033[4;37m'

    end = '\033[0m'



#               BASE DE DADOS
# dados das armaduras (dicionario)
with open("armor.json", "r", encoding="utf8") as fd:
    armaduras = json.load(fd)
# dataframe do dicionario contendo os dados das armaduras |pandas
df_armaduras = pd.DataFrame(armaduras).T

# dados das armas (dicionario)
with open("weapons.json", "r", encoding="utf8") as fd:
    armas = json.load(fd)
# dataframe do dicionario contendo os dados das armas |pandas
df_armas = pd.DataFrame(armas).T

# lista com os dados dos atributos
with open("attributes.json", "r", encoding="utf8") as fd:
    atributos = json.load(fd)



#               FICHA DOS PERSONAGENS
try:
    arquivo1 = sys.argv[1]
    arquivo2 = sys.argv[2]
except:
    arquivo1 = input(f"Digite o nome do arquivo da ficha do {cor.verde_neg}primeiro personagem{cor.end}, exemplo (personagem1.json): ")
    arquivo2 = input(f"Digite o nome do arquivo da ficha do {cor.azul}segundo personagem{cor.end}, exemplo (personagem2.json): ")

try:
    # ficha_personagem1
    with open(arquivo1, "r", encoding="utf8") as fd:
        ficha_personagem1 = json.load(fd)
        
    # ficha_personagem2
    with open(arquivo2, "r", encoding="utf8") as fd:
        ficha_personagem2 = json.load(fd)
except:
    print(f'{cor.vermelho_neg}Arquivo não encontrado :({cor.end}')
    print(f'{cor.amarelo_neg}Verifique se os arquivos estão corretos ou se estao na mesma pasta do programa e tente novamente!{cor.end}\n')
    exit()
    
# dataframe com os dados dos dois personagens
df_personagens = pd.DataFrame((ficha_personagem1, ficha_personagem2))



#               REGRAS
# o personagem com maior destreza ataca primeiro

# perso1 = personagem que ataca primeiro
perso1 = df_personagens.sort_values(by='dexterity', ascending=False).iloc[0]

# perso2 = personagem que ataca em segundo
perso2 = df_personagens.sort_values(by='dexterity', ascending=False).iloc[1]

# calculo da classe de armadura (AC)
for personagem in (perso1, perso2):

    # criando os bonus de força e destreza dos personagens
    personagem['bonus_forca'] = atributos[personagem.strength]
    personagem['bonus_destreza'] = atributos[personagem.dexterity]

    # criando a clase de armadura (AC) dos personagens de acordo com a armadura utilizada
    personagem['AC'] = df_armaduras['AC'][personagem.armor]

    # armadura leve (light) = somar o bônus de destreza do personagem à sua classe de armadura.
    if (df_armaduras.loc[personagem.armor].type) == 'light':
        personagem.AC += personagem.bonus_destreza

    # armadura media (medium) = somar ate dois pontos positivos do bônus de destreza do personagem à sua AC.
    elif (df_armaduras.loc[personagem.armor].type) == 'medium':
        personagem.AC += min(personagem.bonus_destreza, 2)

    # armadura pesada (heavy) = nao somar pontos positivos do bônus de destreza do personagem à sua AC.
    elif (df_armaduras.loc[personagem.armor].type) == 'heavy':
        personagem.AC += min(personagem.bonus_destreza, 0)

    # arma de uma mao (sem 2-hand) e usar shield = recebe +2 na AC
    if (('2-hand' in df_armas.props[personagem.weapon]) == False) and personagem.shield:
        personagem.AC += 2



#               ROLAGENS
# simula a rolagem do dado
def joga_dado(dado):
    ''' Recebe a string do num de lados e simula a rolagem de dados '''
    # desmembrando o damage e pegando o num de lados 'x' do dado
    x = int((dado.split('d'))[1])
    return random.randint(1, x)

# rolagem de ataque
def ataque(personagem):
    ''' Recebe um personagem e calcula seu ataque. Retorna o ataque total '''

    print('\n{}Rolagem de ataque do personagem {}:{}'.format(cor.ciano_neg, personagem['name'], cor.end))

    d20 = joga_dado('d20')
    print(f'    Resultado da rolagem do d20 = {d20}')

    # se a arma tiver 'finesse' = o bonus é o maior valor entre forca e destreza
    if ('finesse' in df_armas.props[personagem.weapon]):
        ataque_total = d20 + max(personagem.bonus_forca, personagem.bonus_destreza)
        print("    A arma do personagem possui a propriedade 'finesse'!")

        if max(personagem.bonus_forca, personagem.bonus_destreza) == personagem.bonus_forca:
            print('    Bonus aplicado (bonus de força) = {}'.format(personagem.bonus_forca))
       
        else:
            print('    Bonus aplicado (bonus de destreza) = {}'.format(personagem.bonus_destreza))

    else:
        # somar o bônus de força do personagem ao total do seu ataque
        ataque_total = d20 + personagem.bonus_forca
        print("    A arma do personagem não possui a propriedade 'finesse'!")
        print(f'    Bonus aplicado (bonus de força) = {personagem.bonus_forca}')

    print(f'    Resultado total do ataque (d20 + bonus aplicado) = {cor.ciano_neg}{cor.ciano_sub}{ataque_total}{cor.end}')

    return ataque_total

# rolagem de dano
def dano(personagem):
    ''' Recebe um personagem e calcula seu dano. Retorna o dano total'''

    print('\n{}Rolagem de dano do personagem {}:{}'.format(cor.verde_neg, personagem['name'], cor.end))

    dado_dano_arma = df_armas.loc[personagem.weapon].damage
    dano_arma = joga_dado(dado_dano_arma)

    print('    Dado de dano do personagem = {}'.format(df_armas.loc[personagem.weapon].damage))
    print('    Resultado da rolagem do {} = {}'.format(df_armas.loc[personagem.weapon].damage, dano_arma))

    # se a arma tiver 'finesse' = o bonus é o maior valor entre forca e destreza
    if (df_armas.loc[personagem.weapon].props == ['finesse']):
        print("    A arma do personagem possui a propriedade 'finesse'!")
        dano_total = dano_arma + max(personagem.bonus_forca, personagem.bonus_destreza)
        
        if max(personagem.bonus_forca, personagem.bonus_destreza) == personagem.bonus_forca:
            print('    Bonus aplicado (bonus de força) = {}'.format(
                personagem.bonus_forca))
       
        else:
            print('    Bonus aplicado (bonus de destreza) = {}'.format(personagem.bonus_destreza))
            
    else:
        # somar o bônus de força do personagem ao total do seu dano
        print("    A arma do personagem não possui a propriedade 'finesse'!")
        dano_total = dano_arma + personagem.bonus_forca
        print(f'    Bonus aplicado (bonus de força) = {personagem.bonus_forca}')

    print('    Resultado total do dano ({} + bonus aplicado) = {}{}{}{}'.format(df_armas.loc[personagem.weapon].damage, cor.verde_neg,cor.verde_sub, dano_total, cor.end))

    return dano_total



#               SIMULAÇÃO DO COMBATE
# simula o turno de um personagem
def turno(i, atacante, alvo, hp_alvo):
    ''' Simula o turno de um personagem e retorna o valor do HP restante do alvo ao final do turno'''

    #titulo personalizado para cada personagem
    if atacante['name'] == perso1['name']:
        print('\n\n\033[7;49;37m-------- INICIO DO TURNO {} DO PERSONAGEM {} --------\033[m'.format(
            i, atacante['name'].upper()))
    else:
        print('\n\n\033[7;49;90m-------- INICIO DO TURNO {} DO PERSONAGEM {} --------\033[m'.format(
            i, atacante['name'].upper()))

    ataque_atacante = ataque(atacante)

    print('\n{}Classe de armadura (AC) do alvo (personagem {}){} = {}{}{}'.format(
        cor.cinza_neg, alvo['name'], cor.end, cor.cinza_sub, alvo.AC, cor.end))

    if ataque_atacante > alvo.AC:
        print(f'\n{cor.verde_neg}O ataque acertou o alvo!!!{cor.end}')

        dano_atacante = dano(atacante)

        hp_alvo -= dano_atacante

    else:
        print(f'\n{cor.vermelho_neg}O ataque não acertou o alvo!!!{cor.end}')

    print(
        f'\n{cor.amarelo_neg}Pontos de vida (HP) restantes do alvo{cor.end} = {cor.amarelo_sub}{hp_alvo}{cor.end}')

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
    
    sleep(0.2)
    print('\n\n\033[1;43;95m********** COMBATE FINALIZADO!!! **********\033[m\n')
    if hp1 <= 0:
        print('{}Vencedor:{} {}{}{}'.format(cor.roxo_neg, cor.end, cor.azul_neg,perso2['name'], cor.end))
        print(f'{cor.roxo_neg}Pontos de vida (HP) restantes:{cor.end} {cor.amarelo_neg}{hp2}{cor.end}')
    elif hp2 <= 0:
        print('{}Vencedor:{} {}{}{}'.format(cor.roxo_neg, cor.end, cor.azul_neg,perso1['name'], cor.end))
        print(f'{cor.roxo_neg}Pontos de vida (HP) restantes:{cor.end} {cor.amarelo_neg}{hp1}{cor.end}')
    print(f'{cor.roxo_neg}Total de turnos realizados:{cor.end} {cor.cinza_neg}{i}{cor.end}\n')

def limpa_terminal():
    ''' Limpa o terminal de qualquer sistema operacional'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def finalizar_progama():
    print(f'{cor.vermelho_neg}Progama finalizado!\n {cor.end}')
    exit()

def mensagem_inicial():
    print('\033[1;43;95m********** SIMULADOR DE COMBATE D&D **********\033[m\n')
    
    print(f'{cor.cinza}Esse progama é um simulador de combate para uma versão simplificada do D&D 5a edição. \nO simulador irá considerar apenas combate corpo a corpo e irá simular turnos de combate onde os personagens atacam um ao outro consecutivamente, \naté que um deles seja reduzido a zero pontos de vida.{cor.end}')
    
    print(f'\n{cor.amarelo_neg}Dados dos pesonagens carregados:{cor.end}')
    
    for personagem in (perso1, perso2):
        print('\n{}Nome:{} {}'.format(cor.roxo, cor.end, personagem['name']))
        print(f'{cor.roxo}Força:{cor.end} {personagem.strength}')
        print(f'{cor.roxo}Destreza:{cor.end} {personagem.dexterity}')
        print(f'{cor.roxo}Armadura:{cor.end} {personagem.armor}')
        print(f'{cor.roxo}Arma:{cor.end} {personagem.weapon}')
        print(f'{cor.roxo}Escudo:{cor.end} {personagem.shield}')
        print(f'{cor.roxo}HP inicial:{cor.end} {personagem.HP}')
        print(f'{cor.roxo}Bonus de forca aplicado:{cor.end} {personagem.bonus_forca}')
        print(f'{cor.roxo}Bonus de destreza aplicado:{cor.end} {personagem.bonus_destreza}')
        print(f'{cor.roxo}Classe de Armadura (AC):{cor.end} {personagem.AC}')
       
    print(f'{cor.azul}\nVamos começar o combate!{cor.end}')
    input(f"{cor.cinza}Pressione a tecla {cor.azul_sub}ENTER{cor.end} {cor.cinza}para continuar  {cor.end}")

# verifica de o usuario deseja jogar novamente
def jogar_novamente():
    ''' Verifica se o usuario deseja jogar novamente e retorna o valor do 'sair' '''
    resposta_valida = False

    while resposta_valida == False:

        rodar_novamente = input(f'{cor.cinza_neg}Deseja simular o combate novamente (s/n)? ')

        if rodar_novamente == 'n' or rodar_novamente == 'N':
            finalizar_progama()
            resposta_valida = True
            sair = True

        elif rodar_novamente == 's' or rodar_novamente =='S':
            resposta_valida = True
            sair = False

        else:
            print(f'\n{cor.vermelho_sub}Resposta inválida!{cor.end}')
            print(f"{cor.vermelho}Digite 's' para 'sim' ou 'n' para não{cor.end}\n")

    return sair


#               EXECUÇÃO
limpa_terminal()
mensagem_inicial()
   
sair = False
while sair == False:

    limpa_terminal()

    simula_combate()

    sair = jogar_novamente()
