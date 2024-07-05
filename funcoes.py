import random
from typing import List, Tuple

import numpy as np

from tipos import Individuo

def calcular_matriz_distancias(local_cidades: List[Tuple[int, int]]) -> List[List[float]]:
    dist_matrix = np.zeros((len(local_cidades), len(local_cidades)))

    for i in range(len(local_cidades)):
        for j in range(len(local_cidades)):
            x1, y1 = local_cidades[i]
            x2, y2 = local_cidades[j]
            distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            dist_matrix[i][j] = distance

    return dist_matrix

def gerar_populacao(local_cidades: List[Tuple[int, int]], maximo_veiculos: int, capacidade_maxima: int, tamanho_populacao: int) -> List[Individuo]:
    populacao = []
    for _ in range(tamanho_populacao):
        veiculo = random.randint(1, maximo_veiculos)
        capacidade = random.randint(1, capacidade_maxima)

        rota = random.sample(range(len(local_cidades)), len(local_cidades))
        individuo = Individuo(veiculo, capacidade, rota)

        populacao.append(individuo)
    return populacao

def order_crossover(
        pai1: Individuo, 
        pai2: Individuo) -> Individuo:
    
    tamanho = len(pai1.rota)

    start_index = random.randint(0, tamanho - 1)
    end_index = random.randint(start_index + 1, tamanho)

    filho = Individuo(pai1.veiculos, pai1.capacidade, [])

    filho.rota.extend(pai1.rota[start_index:end_index])

    remaining_positions = [i for i in range(tamanho) if i < start_index or i >= end_index]
    remaining_genes = [gene for gene in pai2.rota if gene not in filho.rota]

    for position, gene in zip(remaining_positions, remaining_genes):
        filho.rota.insert(position, gene)

    return filho

def mutate(solution: Individuo, mutation_probability: float) -> Individuo:
    if random.random() < mutation_probability:
        index1 = random.randint(0, len(solution.rota) - 1)
        index2 = random.randint(0, len(solution.rota) - 1)

        solution.rota[index1], solution.rota[index2] = solution.rota[index2], solution.rota[index1]

    return solution