## Simulador de Combate D&D
---
A combat simulator the the world's greatest role playing game

### Introdução
---
Neste trabalho iremos implementar um simulador de combate para uma versão simplificada do D&D 5a edição. O nosso simulador irá considerar apenas combate corpo a corpo. O simulador deverá carregar diversas bases de dados (contendo estatísticas de armas, armaduras e bônus de atributos) e ler as fichas de dois personagens. Após isso, o programa deve simular turnos de combate onde os personagens atacam um ao outro consecutivamente, até que um deles seja reduzido a zero pontos de vida.

### Bases de Dados e o Formato JSON
---
As bases de dados neste trabalho serão armazenadas no formato JSON. O formato JSON é amplamente utilizado na indústria; ele tem a vantagem de ser fácil de ler e editar por humanos, e possui integração com diversas linguagens de programação, incluindo Python.

Para ler um arquivo JSON em Python, utilize o módulo json da biblioteca padrão. Por exemplo, se a ficha de um personagem está em um arquivo tank.json, você pode carregar o conteúdo do arquivo em seu programa utilizando o esqueleto de código abaixo:

```
import json

with open("tank.json", "r", encoding="utf8") as fd:
  personagem = json.load(fd)

```

Ao serem lidos pelo código acima, as bases de dados são carregadas como um dicionário ou uma lista em Python, dependendo dos dados contidos no arquivo JSON. Após lidos do arquivo, os dicionários e listas podem ser acessados normalmente.

### Base de Dados de Armaduras
---
A base de dados de armaduras é um arquivo JSON contendo um dicionário onde as chaves são o nome da armadura, e os valores são outro dicionário contendo o custo (cost, inteiro, em peças de ouro), a classe de armadura (AC, inteiro) e o tipo da armadura (type, um string que pode conter os valores light, medium, ou heavy). Exemplo:
```
{
    "leather": {
        "cost": 10,
        "AC": 11,
        "type": "light"
    },
    "breastplate": {
        "cost": 400,
        "AC": 14,
        "type": "medium"
    },
    "plate": {
        "cost": 1500,
        "AC": 18,
        "type": "heavy"
    }
}
```
### Base de Dados de Armas
---
A base de dados de armas é um arquivo JSON contendo um dicionário onde as chaves são o nome da arma, e os valores são outro dicionário contendo o custo (cost, inteiro, em peças de ouro), o dado de dano (damage, um string que pode ser d4, d6, d8, d10, ou d12) e as propriedades da arma (props, uma lista de strings). As propriedades de arma incluídas na base podem ser 2-hand e finesse. Exemplo:
```
{
    "dagger": {
        "cost": 2,
        "damage": "d4",
        "props": ["finesse"],
    },
    "longsword": {
        "cost": 15,
        "damage": "d8",
        "props": [],
    },
    "greatsword": {
        "cost": 50,
        "damage": "d12",
        "props": ["2-hand"],
    }
}
```
### Base de Dados de Atributos
---
Nosso simulador armazena apenas dois atributos de personagens: força (strength) e destreza (dexterity). Atributos com valores altos conferem um bônus e atributos com valores baixos conferem uma penalidade ao personagem. A base de dados de atributos é um arquivo JSON contendo uma lista onde o índice i contém o bônus correspondente a um atributo com o valor i. Por exemplo, o índice 14 da lista contém o bônus que um personagem recebe quando ele tem um atributo com valor 14. Exemplo:
``` 
[null, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5]
``` 

### Rolando Dados
---
Várias ações no jogo de D&D são definidas aleatoriamente rolando dados. Para simular a rolagem de um dado em Python, iremos usar um gerador de números aleatórios. Em python, podemos gerar um número inteiro aleatório entre a e b utilizando a função randint do módulo random da biblioteca padrão. Desta forma, para rolar um dado de x lados, basta utilizar o esqueleto abaixo:
```
import random
x = 6
random.randint(1, x)  # rolando um dado de 6 lados (d6)
```
### Ficha de Personagens
---

A ficha de personagens também serão armazenadas em arquivos JSON contendo um dicionário, que deve conter os seguintes campos:

* name: Um string contendo o nome do personagem.
* strength: Um valor inteiro entre 1 e 20 correspondendo ao atributo de força do personagem.
* dexterity: Um valor inteiro entre 1 e 20 correspondendo ao atributo de destreza do personagem.
* armor: Um string correspondendo à armadura utilizada pelo personagem; o string deve ser uma chave na base de dados de armaduras.
* weapon: Um string correspondendo à arma utilizada pelo personagem; o string deve ser uma chave na base de dados de armas.
* shield: Um valor booleano (verdadeiro ou falso) que indica se o personagem usa um escudo.
* HP: A quantidade de pontos de vida do personagem.
Exemplo:
```
{
    "name": "Warren",
    "strength": 16,
    "dexterity": 12,
    "armor": "half plate",
    "weapon": "maul",
    "shield": false,
    "HP": 56
}
```
### Regras simplificadas
---

* Seu programa deve carregar a ficha de dois personagens.
* Seu programa deve simular turnos de combate, onde cada personagem irá desferir um ataque contra o oponente.
* O personagem com maior destreza ataca primeiro.
* A classe de armadura (AC) de um personagem é determinada pela sua armadura, mais um bônus que depende do tipo da armadura, da destreza do personagem e se o personagem utiliza um escudo:
    * Se a armadura for leve (light), some o bônus de destreza do personagem à sua classe de armadura.
    * Se a armadura for média (medium), some até dois pontos de bônus de destreza do personagem à sua classe de armadura.
    * Se a armadura for pesada (heavy), o personagem não soma seu bônus de destreza à sua classe de armadura.
    * Se a arma do personagem for de uma mão (isto é, não tiver a propriedade 2-hand) e se o personagem utilizar um escudo (shield), ele recebe um bônus de +2 em sua classe de armadura.
* Ao realizar um ataque, um personagem rola um d20 e soma um bônus que depende da arma utilizada e de seus atributos:
    * Some o bônus de força do personagem ao total do seu ataque.
    * Alternativamente, se a arma do personagem tiver a propriedade finesse, ele pode utilizar seu bônus de destreza em vez do bônus de força. No simulador, utilize o bônus de destreza sempre que ele for maior que o bônus de força e a arma tiver a propriedade finesse.
* Se o resultado do ataque (calculado acima) for maior que a classe de armadura do alvo, o ataque acerta o alvo e o atacante rola dados para calcular o dano. O dano de um ataque é determinado pela arma utilizada acrescida de um bônus que depende de seus atributos:
    * Some o bônus de força do personagem ao seu dano.
    * Alternativamente, se a arma do personagem tiver a propriedade finesse, ele pode utilizar seu bônus de destreza em vez do bônus de força.
* O dano de um ataque deve ser subtraído dos pontos de vida do alvo. Quando um alvo tem seus pontos de vida reduzidos a zero ou menos, ele está rendido e seu simulador deve interromper o combate.
* Seu simulador deve executar rodadas de combate até que um dos personagens seja rendido.

### Saída do Simulador
---
Seu simulador deve imprimir um log detalhado do combate. A cada turno combate ele deve imprimir as seguintes informações:

1. Identificar o início do turno de um personagem
2. Indicar o resultado a rolagem de ataque do personagem, detalhando os bônus aplicados
3. Indicar a classe de armadura do alvo e se o ataque acertou
4. Caso o ataque tenha acertado o alvo, indique
 * O resultado da rolagem de dano, detalhando os bônus aplicados
 * O total de pontos de vida restantes do alvo

Quando um personagem for rendido indique o vencedor e a quantidade de pontos de vida que lhe restam.

### Execução do Simulador
---
Seu simulador deve receber como entrada dois parâmetros na linha de comando. Cada parâmetro deve corresponder ao nome de um arquivo contendo uma ficha de personagem. Por exemplo:
```
$ python3 dndsim.py warren.json nolden.json
```
Para processar parâmetros recebidos na linha de comando, utilize a variável argv contida no módulo sys (de sistema). A variável argv é uma lista de strings onde cada string corresponde aos parâmetros passados pela linha de comando, por exemplo, considere que o código abaixo está em um arquivo chamado print-argv.py:
```
import sys
print(sys.argv)
```
Imprimiria o seginte na linha de comando:

```
% python3 print-argv.py warren.json nolden.json
['print-argv.py', 'warren.json', 'nolden.json']
% python3 print-argv.py fulano.json cicrano.json parametro-adicional-sem-utilidade
['print-argv.py', 'fulano.json', 'cicrano.json', 'parametro-adicional-sem-utilidade']
```
### Carregamento dos Arquivos
---
Para permitir a execução do seu programa em qualquer computador, é essencial que ele não contenha caminhos absolutos para arquivos. No Windows, caminhos que começam com um identificador de disco, como C:, são absolutos. No Linux, caminhos que começam com uma barra / são absolutos.

Você deve submeter seu programa utilizando apenas caminhos relativos para as bases de dados. Em particular, seu programa deve abrir as bases de dados passando caminhos relativos assumindo que as bases de dados estão na mesma pasta onde o programa está sendo executado. Consequentemente, seu programa precisa abrir os arquivos com os seguintes comandos:

```
with open("armor.json", encoding="utf8") as fd:
    ...
with open("weapons.json", encoding="utf8") as fd:
    ...
with open("attributes.json", encoding="utf8") as fd:
    ...
```

### Estrutura do Código e Acesso às Bases de Dados
---
O seu código deve ser independente do conteúdo da base de dados. Em outras palavras, seu código deve carregar a acessar as bases de dados; o código deve funcionar (sem alterações) para diferentes bases. Durante a correção do trabalho, iremos testar a compatibilidade do seu código com uma base de dados expandida. A base expandida conterá armas e armaduras adicionais, mas seu programa deve continuar funcionando corretamente visto que as regras aplicadas são as mesmas.
