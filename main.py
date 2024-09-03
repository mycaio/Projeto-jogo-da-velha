import os
import random
from typing import Iterable

TEMPLATE_MATRIZ = """
|---------|---------|---------|
|         |         |         |
|    1    |    2    |    3    |
|         |         |         |
|---------|---------|---------|
|         |         |         |
|    4    |    5    |    6    |
|         |         |         |
|---------|---------|---------|
|         |         |         |
|    7    |    8    |    9    |
|         |         |         |
|---------|---------|---------|
"""

TEMPLATE_JOGADA_ATUAL = """
· \033[1mJogador da vez\033[0m       $JOGADOR
· \033[1mRodada Nº\033[0m            $RODADA
"""

TEMPLATE_MENU_PRINCIPAL: str = """
Você pode jogar esse jogo de duas formas:
    
  1) Multi Player
  2) Single Player

Para sair do jogo digite "sair".

Informe o número da opção que deseja jogar:
"""

TEMPLATE_MENSAGEM_SINGLE_PLAYER: str = """
Bora começar! 😎

Você será o jogador X e eu — máquina invencível! — serei o bolinha, ou O

Que vença o melhor!
"""

def main(): inicia_jogo()

def inicia_jogo():
    print("Bem-vindo ao jogo da velha!")
    modo_de_jogo = seleciona_modo_de_jogo()

    if modo_de_jogo == "1":
        modo_multi_player()
    else:
        modo_single_player()


def seleciona_modo_de_jogo():
    opcao_escolhida = input(TEMPLATE_MENU_PRINCIPAL)

    while not modo_de_jogo_eh_valido(opcao_escolhida):
        opcao_escolhida = input("A opção escolhida não é válida, de qual forma deseja jogar?\n")

    if opcao_escolhida == "sair":
        encerra_jogo()

    return opcao_escolhida


def limpa_a_tela() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def cria_lista_de_jogadas_possiveis() -> list[str]:
  return ["" for _ in range(0, 9)]

def modo_multi_player():
    rodada_atual: int = 1
    jogador_atual = "❎"
    template_da_matriz = TEMPLATE_MATRIZ
    jogadas: list[str] = cria_lista_de_jogadas_possiveis()

    while True:
        limpa_a_tela()
        imprime_rodada_atual(jogador_atual, rodada_atual)
        print(template_da_matriz)

        opcao_escolhida = input('\nOnde deseja jogar?\n')

        if not (opcao_escolhida in template_da_matriz):
            print("\nLugar inválido\n")
        else:
            rodada_atual += 1
            indice = int(opcao_escolhida) - 1
            jogadas[indice] = jogador_atual
            template_da_matriz = atualiza_template(jogador_atual, indice + 1, template_da_matriz)

            if tem_ganhador(jogadas, template_da_matriz):
                limpa_a_tela()
                imprime_ganhador(jogador_atual, True)
                inicia_jogo()
                return

            if jogador_atual == "❎":
                jogador_atual = "🟠"
            else:
                jogador_atual = "❎"

        if not tem_lugar_livre_para_jogar(template_da_matriz):
            limpa_a_tela()
            print(f'Shiii, deu velha 😬😄 Bora tentar de novo!\n')
            inicia_jogo()
            return


def modo_single_player():
    limpa_a_tela()
    print(TEMPLATE_MENSAGEM_SINGLE_PLAYER)

    rodada_atual: int = 1
    jogador_atual: str = "❎"
    forcar_limpeza_da_tela: bool = False
    template_da_matriz: str = TEMPLATE_MATRIZ
    jogadas: list[str] = cria_lista_de_jogadas_possiveis()

    print(template_da_matriz)

    while True:
        if forcar_limpeza_da_tela:
            limpa_a_tela()
            imprime_rodada_atual(jogador_atual, rodada_atual)
            print(template_da_matriz)
            forcar_limpeza_da_tela = False

        if not tem_lugar_livre_para_jogar(template_da_matriz):
            print(f'Shiii, deu velha 😬😄Bora tentar de novo!\n')
            inicia_jogo()
            return

        opcao_escolhida: str = ''
        eh_maquina = eh_vez_do_computador(jogador_atual)

        if not eh_maquina:
            opcao_escolhida = input('\nOnde deseja jogar?\n')

        opcao_existe = posicao_escolhida_eh_valida(opcao_escolhida, template_da_matriz)

        if not eh_maquina and not opcao_existe:
            print("\nEsse lugar é inválido\n")
        else:
            rodada_atual += 1
            proxima_posicao: int

            if eh_maquina:
                proxima_posicao = sorteia_jogada_da_maquina(jogadas)
            else:
                proxima_posicao = int(opcao_escolhida, 10)
                forcar_limpeza_da_tela = True

            jogadas[proxima_posicao - 1] = jogador_atual
            template_da_matriz = atualiza_template(jogador_atual, proxima_posicao, template_da_matriz)

            if eh_maquina:
                limpa_a_tela()
                print(f"\nEscolhi jogar no {proxima_posicao}!")
                print(template_da_matriz)

            if tem_ganhador(jogadas, template_da_matriz):
                limpa_a_tela()
                imprime_ganhador(jogador_atual, False)
                inicia_jogo()
                return

            jogador_atual = alterna_jogador(jogador_atual)

def eh_vez_do_computador(jogador_atual:str) -> bool:
    return jogador_atual == "🟠"

def alterna_jogador(jogador_atual: str) -> str:
    return "🟠" if jogador_atual == "❎" else "❎"

def sorteia_jogada_da_maquina(jogadas: list[str]) -> int:
    jogadas_livres = list(apenas_jogadas_livres(jogadas))

    numero_de_jogadas_restantes = len(list(jogadas_livres))

    posicao_sorteada = random.randint(0, numero_de_jogadas_restantes - 1)

    jogada = next(filter(lambda x: x[0] == posicao_sorteada, enumerate(apenas_jogadas_livres(jogadas))), None)[1]

    return jogada[0] + 1

def apenas_jogadas_livres(jogadas: list[str]) -> Iterable[str]:
    return filter(
        lambda tupla: tupla[1] == '',
        enumerate(jogadas)
    )

def encerra_jogo():
    print("Até mais! ;)")
    exit(1)


def modo_de_jogo_eh_valido(opcao: str) -> bool:
    return opcao is not None and opcao == "1" or opcao == "2" or opcao.lower() == "sair"

def posicao_escolhida_eh_valida(posicao: str, template: str) -> bool:
    return posicao != '' and posicao != 'X' and posicao != "🟠" and posicao in template

def imprime_rodada_atual(jogador_atual: str, rodada_atual: int):
    print(
        TEMPLATE_JOGADA_ATUAL
        .replace("$JOGADOR", jogador_atual)
        .replace("$RODADA", str(rodada_atual))
    )

def imprime_ganhador(vencedor: str, eh_multiplayer: bool):
    if not eh_multiplayer and eh_vez_do_computador(vencedor):
        print('\033[1mO que te disse? 😎 Venci a rodada! Tente na próxima! \033[0m\n')
    else:
        print(f'\033[1m🚀Parabéns! A vitória é sua {vencedor} ! \033[0m\n')

def atualiza_template(jogador: str, posicao: int, template: str) -> str:
    posicao_em_emoji = f"{posicao}"

    return template.replace(posicao_em_emoji, jogador)

def tem_lugar_livre_para_jogar(template: str) -> bool:

    for indice in range(0, 9):
        if str(indice + 1) in template:
            return True

    return False


def tem_ganhador(jogadas: list[str], template_atual: str) -> bool:
    vitorias_possiveis: list[list[int]] = [
        [0, 1, 2], #linha superior
        [3, 4, 5], #linha do meio
        [6, 7, 8], #linha inferior
        [0, 3, 6], #coluna esquerda
        [1, 4, 7], #coluna do meio
        [2, 5, 8], #coluna direita
        [0, 4, 8], #diagonal esquerda → direita
        [2, 4, 6], #diagonal direita → esquerda
    ]

    existe_ganhador: bool = False

    for indices in vitorias_possiveis:
        indice_1 = indices[0]
        indice_2 = indices[1]
        indice_3 = indices[2]

        if eh_uma_sequencia_vitoriosa(jogadas[indice_1], jogadas[indice_2]) and eh_uma_sequencia_vitoriosa(jogadas[indice_2], jogadas[indice_3]):
            existe_ganhador = True

            return existe_ganhador

    return existe_ganhador


def eh_uma_sequencia_vitoriosa(posicao_1, posicao_2):
    return posicao_1 and posicao_2 and posicao_1 == posicao_2

main()