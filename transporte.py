from pygame.locals import *
import random
import itertools
import numpy as np
import pygame
from typing import Tuple

from funcoes import gerar_populacao, calcular_matriz_distancias, order_crossover, mutate
from tipos import Armazem

TAMANHO_POPULACAO = 100
TOTAL_GERACOES = 100

CAPACIDADE_MAXIMA = 50
MAXIMO_VEICULOS = 10

PROBABILIDADE_MUTACAO = 0.7

LOCAL_CIDADES = [(733, 251), (706, 87), (546, 97), (562, 49), (576, 253)]

ESTOQUE_MINIMO_CIDADES = [7000, 4200, 3500, 2500, 5000]

armazens = []
for local_cidade, estoque in zip(LOCAL_CIDADES, ESTOQUE_MINIMO_CIDADES):
    armazem = Armazem(local_cidade, estoque)
    armazens.append(armazem)

dist_matrix = calcular_matriz_distancias(LOCAL_CIDADES)

random.seed(34)

geracao = gerar_populacao(LOCAL_CIDADES, MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, TAMANHO_POPULACAO)

contador_geracao = itertools.count(start=1)

for _ in range(TOTAL_GERACOES):
    populacao_fitness = []
    
    for individuo in geracao:
        fitness = individuo.calcular_fitness(ESTOQUE_MINIMO_CIDADES, dist_matrix)
        populacao_fitness.append((individuo, fitness))

    populacao_fitness = sorted(populacao_fitness, key=lambda x: x[1])
    melhor_individuo, melhor_tempo = populacao_fitness[0]

    print(f"Geração: {contador_geracao} Melhor individuo: {melhor_individuo}, melhor tempo: {melhor_tempo}")

    nova_geracao = []

    nova_geracao.append(melhor_individuo) # Elitismo - nova geração começa com o melhor individuo

    while len(nova_geracao) < (TAMANHO_POPULACAO / 5): # 20% da nova geração é filha dos 10 melhores individuos da geração anterior
        pai1_fitness, pai2_fitness = random.choices(populacao_fitness[:10], k=2)

        pai1 = pai1_fitness[0]
        pai2 = pai2_fitness[0]
        
        filho = order_crossover(pai1, pai2)

        filho = mutate(filho, PROBABILIDADE_MUTACAO)

        nova_geracao.append(filho)

    restante = TAMANHO_POPULACAO - len(nova_geracao)

    nova_geracao.extend(gerar_populacao(LOCAL_CIDADES, MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, restante)) # Preenche o restante da nova geração com individuos aleatórios   

    geracao = nova_geracao
    numero_geracao = next(contador_geracao)

