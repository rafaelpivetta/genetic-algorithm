from pygame.locals import *
import random
import itertools
import numpy as np
from typing import Tuple
import pygame

from funcoes import (
    gerar_populacao,
    calcular_matriz_distancias,
    order_crossover,
    mutate,
    init_screen,
    desenhar_rotas,
    metodo_selecao_aleatorio,
    metodo_selecao_torneio,
    metodo_selecao_roleta,
    metodo_selecao_rank,
    metodo_selecao_elitismo,
    metodo_selecao_truncamento,
)

from tipos import Armazem

# Constantes e dados do problema
WIDTH, HEIGHT = 800, 600
TAMANHO_POPULACAO = 100
TOTAL_GERACOES = 100
CAPACIDADE_MAXIMA = 50
MAXIMO_VEICULOS = 10
PROBABILIDADE_MUTACAO = 0.7

PERCENTUAL_MARGEM_TELA = 0.07  # 7% de margem
margin_x = int(WIDTH * PERCENTUAL_MARGEM_TELA)
margin_y = int(HEIGHT * PERCENTUAL_MARGEM_TELA)

NOMES_CIDADES = ["0", "1", "2", "3", "4"]
LOCAL_CIDADES = [(random.randint(margin_x, WIDTH - margin_x), random.randint(margin_y, HEIGHT - margin_y)) for _ in range(len(NOMES_CIDADES))]
ESTOQUE_MINIMO_CIDADES = [7000, 4200, 3500, 2500, 5000]

# Inicializa a tela do Pygame
screen = init_screen(WIDTH, HEIGHT, "Distribuição de carga em armazéns - GA")

#armazens = [Armazem(localizacao, nome_cidade, estoque) for localizacao, nome_cidade, estoque in zip(LOCAL_CIDADES, NOMES_CIDADES, ESTOQUE_MINIMO_CIDADES)]

armazens = []
for local_cidade, nome_cidade, estoque in zip(LOCAL_CIDADES, NOMES_CIDADES, ESTOQUE_MINIMO_CIDADES):
    armazem = Armazem(local_cidade, nome_cidade, estoque)
    armazens.append(armazem)

# Cálculo da matriz de distâncias
dist_matrix = calcular_matriz_distancias(LOCAL_CIDADES)

random.seed(34)  # Valor inicial usado para inicializar um gerador de números aleatórios

def main(screen):
    geracao = gerar_populacao(LOCAL_CIDADES, MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, TAMANHO_POPULACAO)

    contador_geracao = itertools.count(start=1)

    # Mapeamento dos métodos de seleção de pais
    metodos_selecao = {
        1: metodo_selecao_aleatorio,
        2: metodo_selecao_torneio,
        3: metodo_selecao_roleta,
        4: metodo_selecao_rank,
        5: metodo_selecao_elitismo,
        6: metodo_selecao_truncamento,
    }

    for _ in range(TOTAL_GERACOES):
        clock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        populacao_fitness = []

        for individuo in geracao:
            fitness = individuo.calcular_fitness(ESTOQUE_MINIMO_CIDADES, dist_matrix)
            populacao_fitness.append((individuo, fitness))

        populacao_fitness = sorted(populacao_fitness, key=lambda x: x[1])
        melhor_individuo, melhor_tempo = populacao_fitness[0]

        clock.tick(30)
        print(f"Geração: {contador_geracao} Melhor indivíduo: {melhor_individuo} Melhor tempo: {melhor_tempo}")

        # Chama a função para desenhar as rotas
        desenhar_rotas(screen, melhor_individuo.rota, armazens)

        nova_geracao = []

        nova_geracao.append(melhor_individuo)  # Elitismo - nova geração começa com o melhor indivíduo

        while len(nova_geracao) < (TAMANHO_POPULACAO / 5):  # 20% da nova geração é filha dos 10 melhores indivíduos da geração anterior
            metodo = random.randint(1, len(metodos_selecao))  # Gera um número aleatório baseado no tamanho do dicionário de seleção de pais

            pai1, pai2 = metodos_selecao[metodo](populacao_fitness)

            filho = order_crossover(pai1, pai2)

            filho = mutate(filho, PROBABILIDADE_MUTACAO)

            nova_geracao.append(filho)

        restante = TAMANHO_POPULACAO - len(nova_geracao)

        nova_geracao.extend(gerar_populacao(LOCAL_CIDADES, MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, restante))  # Preenche o restante da nova geração com indivíduos aleatórios

        geracao = nova_geracao
        numero_geracao = next(contador_geracao)

    # Mantém a tela aberta depois de completar a execução
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        clock.tick(30)

if __name__ == "__main__":
    main(screen)
