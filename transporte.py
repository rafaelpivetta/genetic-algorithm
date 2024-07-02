import pygame
from pygame.locals import *
import random
import itertools
import sys
import numpy as np
import pygame
from typing import List, Tuple

TAMANHO_POPULACAO = 10000
TOTAL_GERACOES = 100


CAPACIDADE_MAXIMA = 60
MAXIMO_VEICULOS = 10
TOTAL_DEMANDA = 5000000
DISTANCIA = 10000

random.seed(2)

def gerar_populacao(maximo_veiculos: int, capacidade_maxima: int, tamanho_populacao: int) -> List[Tuple[int, int]]:
    populacao = []
    for _ in range(tamanho_populacao):
        veiculo = random.randint(1, maximo_veiculos)
        capacidade = random.randint(1, capacidade_maxima)
        individuo = (veiculo, capacidade)

        populacao.append(individuo)
    return populacao

populacao = gerar_populacao(MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, TAMANHO_POPULACAO)


def calcular_fitness(individuo: Tuple[int, int], demanda: int, distancia: int) -> float:
    quantidade_veiculos = individuo[0]
    capacidade_veiculo = individuo[1]
    
    velocidade = 120 - capacidade_veiculo
    tempo = distancia / velocidade

    demanda_por_veiculo = demanda / quantidade_veiculos

    viagens = demanda_por_veiculo / capacidade_veiculo
    tempo_total = tempo * viagens

    return quantidade_veiculos * tempo_total


geracao = gerar_populacao(MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, TAMANHO_POPULACAO)

contador_geracao = itertools.count(start=1)

for _ in range(TOTAL_GERACOES):
    #print(geracao)
    populacao_fitness = []
    
    for individuo in geracao:
        fitness = calcular_fitness(individuo, TOTAL_DEMANDA, DISTANCIA)
        populacao_fitness.append((individuo, fitness))
        #print(f"Individuo: {individuo}, fitness: {fitness}")

    populacao_fitness = sorted(populacao_fitness, key=lambda x: x[1])
    melhor_individuo, melhor_tempo = populacao_fitness[0]

    print(f"Geração: {contador_geracao} Melhor individuo: {melhor_individuo}, melhor tempo: {melhor_tempo}")

    nova_geracao = gerar_populacao(MAXIMO_VEICULOS, CAPACIDADE_MAXIMA, TAMANHO_POPULACAO - 1)

    nova_geracao.append(melhor_individuo)

    geracao = nova_geracao
    numero_geracao = next(contador_geracao)


    

