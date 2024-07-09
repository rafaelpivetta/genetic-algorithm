from pygame.locals import *
import random
import itertools
import numpy as np
import pygame
from typing import Tuple

from funcoes import gerar_populacao, calcular_matriz_distancias, order_crossover, mutate
from tipos import Armazem

# Inicializa Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Distribuição de carga em armazéns - GA")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TAMANHO_POPULACAO = 100
TOTAL_GERACOES = 100

CAPACIDADE_MAXIMA = 50
MAXIMO_VEICULOS = 10

PROBABILIDADE_MUTACAO = 0.7

LOCAL_CIDADES = [(733, 251), (706, 87), (546, 97), (562, 49), (576, 253)]
NOMES_CIDADES = ['0', '1', '2', '3', '4']

ESTOQUE_MINIMO_CIDADES = [7000, 4200, 3500, 2500, 5000]

armazens = []
for local_cidade, estoque in zip(LOCAL_CIDADES, ESTOQUE_MINIMO_CIDADES):
    armazem = Armazem(local_cidade, estoque)
    armazens.append(armazem)

dist_matrix = calcular_matriz_distancias(LOCAL_CIDADES)
print(dist_matrix)

random.seed(34)

def main():
    geracao = gerar_populacao(LOCAL_CIDADES, MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, TAMANHO_POPULACAO)

    contador_geracao = itertools.count(start=1)

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
        # print(f"Melhor indivíduo:", melhor_individuo)

        clock.tick(30)
        print(f"Geração: {contador_geracao} Melhor indivíduo: {melhor_individuo}, melhor tempo: {melhor_tempo}")

        # Desenha os pontos (dots) na tela
        for i, (x, y) in enumerate(LOCAL_CIDADES):
            pygame.draw.circle(screen, BLUE, (x, y), 5)
            font = pygame.font.Font(None, 20)
            text = font.render(NOMES_CIDADES[i], True, WHITE)
            text_rect = text.get_rect(center=(x, y - 15))
            screen.blit(text, text_rect)

        pygame.display.flip()  # Atualiza a tela

        nova_geracao = []

        nova_geracao.append(melhor_individuo) # Elitismo - nova geração começa com o melhor indivíduo

        while len(nova_geracao) < (TAMANHO_POPULACAO / 5): # 20% da nova geração é filha dos 10 melhores indivíduos da geração anterior
            pai1_fitness, pai2_fitness = random.choices(populacao_fitness[:10], k=2)

            pai1 = pai1_fitness[0]
            pai2 = pai2_fitness[0]
        
            filho = order_crossover(pai1, pai2)

            filho = mutate(filho, PROBABILIDADE_MUTACAO)

            nova_geracao.append(filho)

        restante = TAMANHO_POPULACAO - len(nova_geracao)

        nova_geracao.extend(gerar_populacao(LOCAL_CIDADES, MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, restante)) # Preenche o restante da nova geração com indivíduos aleatórios   

        geracao = nova_geracao
        numero_geracao = next(contador_geracao)

    # Mentém a tela aberta depois de completar a exceção
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        clock.tick(30)

if __name__ == "__main__":
    main()
