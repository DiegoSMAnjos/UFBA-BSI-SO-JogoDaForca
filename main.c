/*
Integrantes:

- Victor Rafael
- Diego Anjos

Descricao:

Este jogo foi desenvolvido para aprovacao na disciplina de Sistemas Operacionais, semestre 2023.1, da Universidade Federal da Bahia.

*/



#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_TENTATIVAS 6





int main() {
    char* palavras[] = {"banana", "morango", "abacaxi", "uva", "laranja", "limao"};
    int n_palavras = 6;
    char palavra_secreta[50];
    char palavra_codificada[50];
    int tam_palavra;
    char letra;
    int tentativas = 0;
    int acertos = 0;
    int i, j;

    print("---------------------------\n");
    print("--                       --\n");
    print("--   JOGO DA FORCA       --\n");
    print("--                       --\n");
    print("---------------------------\n\n");


    // Escolhe uma palavra aleatória
    srand(time(NULL));
    int indice_palavra = rand() % n_palavras;
    strcpy(palavra_secreta, palavras[indice_palavra]);
    tam_palavra = strlen(palavra_secreta);

    // Inicializa a palavra codificada
    for (i = 0; i < tam_palavra; i++) {
        palavra_codificada[i] = '_';
    }
    palavra_codificada[tam_palavra] = '\0';

    // Jogo da forca
    while (tentativas < MAX_TENTATIVAS && acertos < tam_palavra) {
        printf("Palavra: %s\n", palavra_codificada);
        printf("Digite uma letra: ");
        letra = getchar();

        // Verifica se a letra está na palavra
        int acertou
