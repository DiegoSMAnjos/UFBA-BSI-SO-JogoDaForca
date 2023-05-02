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
#include <pthread.h>
#include <semaphore.h>

#define MAX_TENTATIVAS 6
#define MAX_JOGADORES 2

char palavra_secreta[50];
char palavra_codificada[50];
int tam_palavra;
char letra;
int tentativas = 0;
int acertos = 0;
char desenho_forca[MAX_TENTATIVAS][8] = {" O\n", "/|\\\n", "/ \\\n", "", "", ""};

sem_t sem_exclusao_mutua;
sem_t sem_sincronizacao;

void* jogar(void* arg) {
    int jogador = *(int*) arg;
    int acertou = 0;
    int i, j;

    while (tentativas < MAX_TENTATIVAS && !acertou) {
        sem_wait(&sem_sincronizacao);

        printf("Jogador %d:\n", jogador);
        printf("Palavra: %s\n", palavra_codificada);
        printf("Tentativas restantes: %d\n", MAX_TENTATIVAS - tentativas);
        printf("Digite uma letra: ");
        letra = getchar();
        getchar(); // Limpa o buffer do teclado

        // Verifica se a letra está na palavra
        sem_wait(&sem_exclusao_mutua);
        acertou = 0;
        for (i = 0; i < tam_palavra; i++) {
            if (palavra_secreta[i] == letra && palavra_codificada[i] == '_') {
                palavra_codificada[i] = letra;
                acertou = 1;
                acertos++;
            }
        }
        if (!acertou) {
            printf("Letra %c não encontrada na palavra.\n", letra);
            printf("%s", desenho_forca[tentativas]);
            tentativas++;
        }
        sem_post(&sem_exclusao_mutua);

        sem_post(&sem_sincronizacao);
    }

