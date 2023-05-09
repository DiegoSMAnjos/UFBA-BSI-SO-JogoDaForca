import random
import threading
from time import sleep

MAX_TENTATIVAS = 6
MAX_PALAVRA = 5

palavra = ""
dicaPalavra = ""
tamanho = 0
jogo_continua = True
sem_leitura_palavra = threading.Semaphore(0)
esperar_teclado_ser_liberado = threading.Semaphore(1)
esperar_turno_validacao = threading.Semaphore(1)


# sem_leitura_letra = threading.Semaphore(0)
# sem_atualiza_palavra = threading.Semaphore(1)
# sem_atualiza_tentativas = threading.Semaphore(1)
# esperarDefinicaoVariaveis = threading.Semaphore(1)


class Jogador():
    def __init__(self, name: str):
        self.name = name
        self.tentativas_restantes = MAX_TENTATIVAS
        self.adivinhacao = ""
        self.vitoria = False


def desenharArvore(tentativas):
    if tentativas >= 6:
        print("  _______\n"
              " |/      |\n"
              " |\n"
              " |\n"
              " |\n"
              " |\n"
              "_|___")
    elif tentativas == 5:
        print("  _______\n"
              " |/      |\n"
              " |      (_)\n"
              " |\n"
              " |\n"
              " |\n"
              "_|___")
    elif tentativas == 4:
        print("  _______\n"
              " |/      |\n"
              " |      (_)\n"
              " |       |\n"
              " |       |\n"
              " |\n"
              "_|___")
    elif tentativas == 3:
        print("  _______\n"
              " |/      |\n"
              " |      (_)\n"
              " |       |\n"
              " |       |\n"
              " |      /\n"
              "_|___")
    elif tentativas == 2:
        print("  _______\n"
              " |/      |\n"
              " |      (_)\n"
              " |       |\n"
              " |       |\n"
              " |      / \\\n"
              "_|___")
    elif tentativas == 1:
        print("  _______\n"
              " |/      |\n"
              " |      (_)\n"
              " |      /|\n"
              " |       |\n"
              " |      / \\\n"
              "_|___")
    else:
        pass  # não imprime nada se tentativas = 0


def definirPalavra():
    global palavra, dicaPalavra

    db_palavras = [
        ['Fruta', 'Laranja'],
        ['Fruta', 'Abacaxi'],
        ['Fruta', 'Melancia'],
        ['Animal', 'Cachorro'],
        ['Animal', 'Gato'],
        ['Animal', 'Rinoceronte'],
        ['Animal', 'Rinoceronte'],
        ['Cor', 'Vermelho'],
        ['Cor', 'Verde'],
        ['Cor', 'Roxo'],
        ['Cor', 'Amarelo'],
        ['País', 'Venezuela'],
        ['País', 'Hungria'],
        ['País', 'Eslovaquia'],
    ]
    escolhido = random.choice(db_palavras)
    dicaPalavra = escolhido[0]
    palavra = escolhido[1]

    # palavra = input("ADM: insira a palavra para o jogo da forca (sem acentos): ")
    sem_leitura_palavra.release()


def jogar(player: Jogador):
    # esperarDefinicaoVariaveis.acquire()
    # sem_leitura_palavra.acquire()
    global palavra, tamanho, jogo_continua

    tamanho = len(palavra)

    player.adivinhacao = "_" * tamanho
    # esperarDefinicaoVariaveis.release()
    # sem_leitura_palavra.release()
    while jogo_continua:
        esperar_teclado_ser_liberado.acquire()
        # sleep(1)

        # sem_atualiza_palavra.acquire()
        print(f"{player.name}, tente adivinhar a palavra (DICA: {dicaPalavra}): {player.adivinhacao}")
        # sem_atualiza_palavra.release()

        # sem_atualiza_tentativas.acquire()
        print(f"Você tem {player.tentativas_restantes} tentativas restantes.")
        # sem_atualiza_tentativas.release()

        letra = input("Digite uma letra: ")
        letra = letra.lower()

        esperar_teclado_ser_liberado.release()
        esperar_turno_validacao.acquire()
        if letra in palavra:
            for i in range(tamanho):
                if palavra[i] == letra:
                    player.adivinhacao = player.adivinhacao[:i] + letra + player.adivinhacao[i + 1:]
        else:
            print(f"A letra '{letra}' não faz parte da palavra.\n")
            player.tentativas_restantes -= 1
            if player.tentativas_restantes == 0:
                jogo_continua = False
        desenharArvore(player.tentativas_restantes)
        if palavra == player.adivinhacao:
            player.vitoria = True
            jogo_continua = False
        esperar_turno_validacao.release()



def main():
    t1 = threading.Thread(target=definirPalavra)
    player1 = threading.Thread(target=jogar, args=[Jogador('Luiz')])
    player2 = threading.Thread(target=jogar, args=[Jogador('Victor')])

    t1.start()
    t1.join()
    player1.start()
    player2.start()

    # sem_leitura_letra.acquire()

    player1.join()
    player2.join()

    vitoria = False
    if vitoria:
        print(f"Parabéns, você venceu! A palavra era {palavra}.")
    else:
        print(f"Você perdeu! A palavra era {palavra}.")


if __name__ == "__main__":
    main()
