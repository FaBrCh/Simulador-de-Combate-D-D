
import json
import random
import sys
import os
import pandas as pd


try:
    arquivo1 = sys.argv[1]
    arquivo2 = sys.argv[2]
except:
    arquivo1 = input("Digite o nome do arquivo da ficha do primeiro personagem: ")
    arquivo2 = input("Digite o nome do arquivo da ficha do segundo personagem: ")


# ficha_personagem1
with open(arquivo1, "r", encoding="utf8") as fd:
    ficha_personagem1 = json.load(fd)

# ficha_personagem2
with open(arquivo2, "r", encoding="utf8") as fd:
    ficha_personagem2 = json.load(fd)

# dataframe com os dados dos dois personagens
df_personagens = pd.DataFrame((ficha_personagem1, ficha_personagem2))

print(df_personagens)