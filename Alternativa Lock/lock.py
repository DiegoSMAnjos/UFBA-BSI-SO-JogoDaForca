import random
import threading
from time import sleep
import os

MAX_TENTATIVAS = 6

palavra = ""
dicaPalavra = ""
tamanho = 0
nomeVencedor = ''
lock_leitura_palavra = threading.Lock()
lock_validacao_turno = threading.Lock()

class Jogador():
    def __init__(self, name: str):
        self.name = name
        self.tentativas_restantes = MAX_TENTATIVAS
        self.adivinhacao = ""
        self.vitoria = False
        self.jogo_continua = True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def desenharArvore(tentativas):
    if tentativas >= 6:
        print("  _______")
        print(" |/      |")
        print(" |")
        print(" |")
        print(" |")
        print(" |")
        print("_|___")
    elif tentativas == 5:
        print("  _______")
        print(" |/      |")
        print(" |      (_)")
        print(" |")
        print(" |")
        print(" |")
        print("_|___")
    elif tentativas == 4:
        print("  _______")
        print(" |/      |")
        print(" |      (_)")
        print(" |       |")
        print(" |       |")
        print(" |")
        print("_|___")
    elif tentativas == 3:
        print("  _______")
        print(" |/      |")
        print(" |      (_)")
        print(" |       |")
        print(" |       |")
        print(" |      /")
        print("_|___")
    elif tentativas == 2:
        print("  _______")
        print(" |/      |")
        print(" |      (_)")
        print(" |       |")
        print(" |       |")
        print(" |      / \\")
        print("_|___")
    elif tentativas == 1:
        print("  _______")
        print(" |/      |")
        print(" |      (_)")
        print(" |      /|")
        print(" |       |")
        print(" |      / \\")
        print("_|___")
    else:
        print("  _______")
        print(" |/      |")
        print(" |      (_)")
        print(" |      /|\\")
        print(" |       |")
        print(" |      / \\")
        print("_|___")

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
    palavra = escolhido[1].lower()

    lock_leitura_palavra.release()

def jogar(player: Jogador):
    global palavra, tamanho, nomeVencedor

    tamanho = len(palavra)

    player.adivinhacao = "_" * tamanho
    
    while player.jogo_continua:
        sleep(1)

        lock_validacao_turno.acquire()
        if len(nomeVencedor) > 0:
            lock_validacao_turno.release()
            break
        lock_validacao_turno.release()
       
        print(f"{player.name}, tente adivinhar a palavra (DICA: {dicaPalavra}): {player.adivinhacao}")
        print(f"Você tem {player.tentativas_restantes} tentativas restantes.")

        letra = input("Digite uma letra: ")
        
        encontrou = False
        if letra in palavra:
            for i in range(tamanho):
                if palavra[i].lower() == letra.lower():
                    player.adivinhacao = player.adivinhacao[:i] + letra + player.adivinhacao[i + 1:]
                    encontrou = True
            if encontrou:
                print(f"Letra correta!")
        else:
            print(f"A letra '{letra}' não faz parte da palavra.")
            player.tentativas_restantes -= 1
            if player.tentativas_restantes == 0:
                player.jogo_continua = False
        desenharArvore(player.tentativas_restantes)
        print(f"Palavra: {player.adivinhacao}")
        if palavra.lower() == player.adivinhacao.lower():
            nomeVencedor = player.name
            player.jogo_continua = False
        sleep(5)
        clear_screen()

def main():
    clear_screen()
    t1 = threading.Thread(target=definirPalavra)
    player_nome1 = input("Digite o nome do primeiro jogador: ")
    player_nome2 = input("Digite o nome do segundo jogador: ")
    player1 = threading.Thread(target=jogar, args=[Jogador(player_nome1)])
    player2 = threading.Thread(target=jogar, args=[Jogador(player_nome2)])

    lock_leitura_palavra.acquire()
    t1.start()
    lock_leitura_palavra.acquire()
    lock_leitura_palavra.release()

    clear_screen()
    player1.start()
    player2.start()

    player1.join()
    player2.join()

    if len(nomeVencedor) > 0:
        print(f"Parabéns {nomeVencedor}, você venceu! A palavra era {palavra}.")
    else:
        print(f"Vocês perderam! A palavra era {palavra}.")

if __name__ == "__main__":
    main()

