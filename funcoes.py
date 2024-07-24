import random
from typing import List, Tuple

import numpy as np
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from tipos import Individuo

# Variáveis globais para armazenar as gerações e os tempos
geracoes = []
tempos = []

def calcular_matriz_distancias(
    local_cidades: List[Tuple[int, int]]
) -> List[List[float]]:
    dist_matrix = np.zeros((len(local_cidades), len(local_cidades)))

    for i in range(len(local_cidades)):
        for j in range(len(local_cidades)):
            x1, y1 = local_cidades[i]
            x2, y2 = local_cidades[j]
            distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            dist_matrix[i][j] = distance

    return dist_matrix


def gerar_populacao(
    local_cidades: List[Tuple[int, int]],
    maximo_veiculos: int,
    capacidade_maxima: int,
    tamanho_populacao: int,
) -> List[Individuo]:
    populacao = []
    for _ in range(tamanho_populacao):
        veiculo = random.randint(1, maximo_veiculos)
        capacidade = random.randint(1, capacidade_maxima)

        rota = random.sample(range(len(local_cidades)), len(local_cidades))
        individuo = Individuo(veiculo, capacidade, rota)

        populacao.append(individuo)
    return populacao


def order_crossover(pai1: Individuo, pai2: Individuo) -> Individuo:

    tamanho = len(pai1.rota)

    start_index = random.randint(0, tamanho - 1)
    end_index = random.randint(start_index + 1, tamanho)

    filho = Individuo(pai1.veiculos, pai1.capacidade, [])

    filho.rota.extend(pai1.rota[start_index:end_index])

    remaining_positions = [
        i for i in range(tamanho) if i < start_index or i >= end_index
    ]
    remaining_genes = [gene for gene in pai2.rota if gene not in filho.rota]

    for position, gene in zip(remaining_positions, remaining_genes):
        filho.rota.insert(position, gene)

    return filho


def mutate(solution: Individuo, mutation_probability: float) -> Individuo:
    if random.random() < mutation_probability:
        index1 = random.randint(0, len(solution.rota) - 1)
        index2 = random.randint(0, len(solution.rota) - 1)

        solution.rota[index1], solution.rota[index2] = (
            solution.rota[index2],
            solution.rota[index1],
        )

    return solution

# Função para inicializar a tela do Pygame
def init_screen(width: int, height: int, caption: str) -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen

def desenhar_rotas(screen, melhor_rota, armazens):
    # Cores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Limpa a tela
    screen.fill(BLACK)

    font = pygame.font.Font(None, 20)
    
    # Desenha os pontos (dots) na tela
    for armazem in armazens:
        x, y = armazem.localizacao
        pygame.draw.circle(screen, BLUE, (x, y), 5)
        
        text = font.render(armazem.nome_cidade, True, WHITE)
        text_rect = text.get_rect(center=(x - 15, y - 15))
        screen.blit(text, text_rect)
    
    # Desenha as linhas da melhor rota
    for i in range(len(melhor_rota)):
        cidade_atual = melhor_rota[i]
        proxima_cidade = melhor_rota[(i + 1) % len(melhor_rota)]

        pygame.draw.line(
            screen,
            RED,
            armazens[cidade_atual].localizacao,
            armazens[proxima_cidade].localizacao,
            2,
        )
        text = font.render(f"({i + 1})", True, WHITE)
        x, y = armazens[cidade_atual].localizacao
        text_rect = text.get_rect(center=(x - 20, y - 30))
        screen.blit(text, text_rect)

    pygame.display.flip()  # Atualiza a tela

def plotar_grafico(geracoes, tempos):

    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.plot(geracoes, tempos, marker='o', color='b', linestyle='-')
    ax.set_title('Melhor Tempo por Geração', fontsize=8)
    ax.set_xlabel('Geração', fontsize=8)
    ax.set_ylabel('Melhor Tempo', fontsize=8)
    ax.grid(True)
    
    # Converter o gráfico matplotlib para uma superfície pygame
    canvas = FigureCanvas(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    
    return pygame.image.fromstring(raw_data, size, "RGB")

def desenhar_info(screen, geracao, melhor_tempo, melhor_individuo, metodo_selecao_escolhido, WIDTH, HEIGHT):
    font = pygame.font.Font(None, 20)
    GREEN = (0, 255, 0)

    # Calcula a altura onde a linha divisória inferior deve ser desenhada
    altura_parte_inferior = int(HEIGHT * 0.60)  # 65% da altura total da tela

    # Desenha a linha horizontal na parte inferior
    #pygame.draw.line(screen, GREEN, (0, altura_parte_inferior), (WIDTH, altura_parte_inferior), 2)

    # Ajusta as posições verticais das linhas de texto
    linha1_y = altura_parte_inferior + 20
    linha2_y = linha1_y + 20
    linha3_y = linha2_y + 20
    linha4_y = linha3_y + 20

    text = font.render(f"Geração: {geracao}", True, GREEN)
    screen.blit(text, (10, linha1_y))

    if melhor_individuo:
        text = font.render(f"Melhor indivíduo: {melhor_individuo}", True, GREEN)
        screen.blit(text, (10, linha2_y))
        text = font.render(f"Melhor tempo: {melhor_tempo}", True, GREEN)
        screen.blit(text, (10, linha3_y))
        
        # Adicionar a geração atual e o melhor tempo às listas globais
        geracoes.append(geracao)
        tempos.append(melhor_tempo)

        # Plotar o gráfico
        if geracoes and tempos:
            graph_surface = plotar_grafico(geracoes, tempos)
            screen.blit(graph_surface, (int(WIDTH/2), altura_parte_inferior))


    text = font.render(f"Método de seleção de pais escolhido: {metodo_selecao_escolhido}", True, GREEN)  
    screen.blit(text, (10, linha4_y))

    pygame.display.flip()
    
def metodo_selecao_aleatorio(populacao_fitness):
    pai1_fitness, pai2_fitness = random.choices(populacao_fitness[:10], k=2)
    pai1 = pai1_fitness[0]
    pai2 = pai2_fitness[0]
    return pai1, pai2

def metodo_selecao_torneio(populacao_fitness):
    def torneio(populacao_fitness):
        tamanho_torneio = 3 # Tamanho do torneio igual a 3 competidores
        competidores = random.sample(populacao_fitness, tamanho_torneio)
        competidores.sort(key=lambda x: x[1])  # Ordena por fitness
        return competidores[0][0]  # Retorna o melhor competidor

    pai1 = torneio(populacao_fitness[:10])
    pai2 = torneio(populacao_fitness[:10])
    return pai1, pai2

def metodo_selecao_roleta(populacao_fitness):
    # Calcula a soma total dos fitness para calcular as probabilidades
    soma_fitness = sum(fitness for _, fitness in populacao_fitness)

    # Seleciona aleatoriamente um valor de fitness
    valor_selecionado = random.uniform(0, soma_fitness)
    acumulado = 0.0

    pai1 = None
    pai2 = None

    for individuo, fitness in populacao_fitness:
        acumulado += fitness
        if acumulado >= valor_selecionado and pai1 is None:
            pai1 = individuo

    # Seleciona o segundo pai de forma semelhante ao primeiro, garantindo que sejam diferentes
    while True:
        valor_selecionado = random.uniform(0, soma_fitness)
        acumulado = 0.0

        for individuo, fitness in populacao_fitness:
            acumulado += fitness
            if acumulado >= valor_selecionado and individuo != pai1:
                pai2 = individuo
                return pai1, pai2  # Retorna os pais selecionados

    return pai1, pai2  # Caso não encontre um segundo pai válido, retorna None para ambos

def metodo_selecao_rank(populacao_fitness):
    populacao_ordenada = sorted(populacao_fitness[:10], key=lambda x: x[1])
    ranks = list(range(1, len(populacao_ordenada) + 1))
    total_ranks = sum(ranks)
    pick1 = random.uniform(0, total_ranks)
    pick2 = random.uniform(0, total_ranks)

    current = 0
    for rank, (individuo, _) in zip(ranks, populacao_ordenada):
        current += rank
        if current > pick1:
            pai1 = individuo
            break

    current = 0
    for rank, (individuo, _) in zip(ranks, populacao_ordenada):
        current += rank
        if current > pick2:
            pai2 = individuo
            break

    return pai1, pai2
