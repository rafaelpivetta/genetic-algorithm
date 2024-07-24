# genetic-algorithm 

## O Problema 
O problema consiste na otimização das rotas de entrega de uma empresa de logística que precisa reabastecer armazéns distribuídos por várias cidades com sua frota de veículos.

## Parâmetros
O problema foi delimitado conforme:
- Cada cidade tem um armazém com um estoque mínimo de itens que precisa ser abastecido, e possui coordenadas específicas em um plano cartesiano, geradas aleatoriamente de forma a possibilitar sua plotagem numa área de tela específica.
- A empresa dispõe de uma frota limitada de veículos, cuja capacidade de carga é inversamente proporcional à sua velocidade (Velocidade = 120 km/h − Itens de Carga). Por exemplo, um veículo com capacidade para 20 itens viaja a 100 km/h, enquanto sua velocidade máxima seria 120 km/h sem carga. 
- Cada solução testada pelo algoritmo (indivíduo) tem de 1 a 10 de veículos, com a mesma capacidade de carga de até 100 itens cada. 
- Os veículos partem sempre abastecidos de uma cidade para a outra, e os armazéns estão inicialmente todos vazios. 
- Quando um armazém tiver seu estoque mínimo totalmente abastecido ele deixa de fazer parte da nova rota de entregas.
- O tempo total gasto para o abastecimento é o tempo somado de todas as viagens de todos os veículos utilizados.

## Solução
O desafio é encontrar o melhor balanceamento entre carga e velocidade dos veículos, número de veículos e rota de entrega entre as cidades, de forma a abastecer o estoque mínimo de todos os armazéns no menor tempo possível. 

## O código da Solução em Python
O código é uma implementação de um algoritmo genético, que inclui funções para calcular a matriz de distâncias entre cidades, gerar uma população inicial de indivíduos, e realizar seleção por diversos métodos, como seleção aleatória, torneio, roleta, rank.

O código inclui:
- As principais funções utilizadas para a implementação detalhada do algoritmo genético combinado com a biblioteca Pygame para visualização (funções.py).
- A definição de duas classes, Armazém e Individuo, e implementação da funcionalidade de cálculo de fitness para um algoritmo genético focado em logística e distribuição.
- Loop principal que simula o processo evolutivo de um algoritmo genético, iterando através de gerações, avaliando fitness, selecionando pais, aplicando crossover e mutação, e finalmente atualizando a população com novos indivíduos. 
- O uso de Pygame permite uma visualização interativa da evolução do algoritmo em tempo real, tornando possível observar seu funcionamento na busca pela melhor solução.

## Detalhamento do código da solução

### funcoes.py:

A implementação define as principais funções usadas utilizadas para a implementação detalhada de um algoritmo genético combinado com a biblioteca Pygame para visualização.

Aqui estão os principais componentes e funcionalidades do código:
- Cálculo da Matriz de Distâncias: `calcular_matriz_distancias(local_cidades)`: Calcula e retorna uma matriz de distâncias euclidianas entre cidades, baseada nas coordenadas (x, y) fornecidas para cada cidade.
- Geração de População: `gerar_populacao(local_cidades, maximo_veiculos, capacidade_maxima, tamanho_populacao)`: Gera uma população inicial de indivíduos (cada um representando uma solução potencial), onde cada indivíduo tem uma rota aleatória, capacidade de veículo e número de veículos atribuídos aleatoriamente.
- Operadores Genéticos: `order_crossover(pai1, pai2)`: Realiza o crossover ordenado entre dois indivíduos pais para produzir um filho, combinando partes das rotas dos pais.`mutate(solution, mutation_probability)`: Aplica uma mutação a um indivíduo com uma probabilidade dada, trocando aleatoriamente dois pontos em sua rota.
- Inicialização e Configuração do Pygame: `init_screen(width, height, caption)`: Configura a tela do Pygame com as dimensões e o título especificados.:
- Visualização com Pygame: `desenhar_rotas(screen, melhor_rota, armazens)`: Visualiza a melhor rota encontrada, desenhando linhas entre as cidades na tela do Pygame. `desenhar_info(screen, geracao, melhor_tempo, melhor_individuo)`: Exibe informações sobre a geração atual, o melhor tempo de rota encontrado, e o melhor indivíduo.
- Métodos de Seleção: Vários métodos de seleção são implementados para escolher pais para a reprodução, como seleção aleatória, torneio, roleta, rank, elitismo e truncamento. Esses métodos ajudam a diversificar as soluções e a selecionar os melhores candidatos para a reprodução baseada em fitness.


### tipos.py:

Responsável pela definição de duas classes, Armazem e Individuo, que implementam a funcionalidade de cálculo de fitness para um algoritmo genético focado em logística e distribuição.

Vamos comentar cada parte do código para entender suas funcionalidades e interações.
- Classe Armazem: Esta classe representa um armazém localizado em uma cidade específica. Ela armazena informações sobre a localização geográfica do armazém, o nome da cidade onde está localizado, e o estoque mínimo necessário que deve ser mantido.
- Classe Individuo: Representa um possível "indivíduo" ou solução no contexto de um algoritmo genético. Um Individuo é caracterizado pela quantidade de veículos, a capacidade de cada veículo e a rota que eles devem seguir para atender aos armazéns.
- Método calcular_fitness: Este método é crucial, pois calcula o "fitness", a aptidão de um Individuo baseado no total de tempo necessário para completar a rota de entrega considerando as limitações de carga e a velocidade dos veículos. 
    - O fitness é uma medida de quão boa é a solução representada pelo indivíduo. O método faz uso de uma matriz de distâncias entre as cidades para calcular os deslocamentos e os tempos de viagem.
    - O método assume que os armazéns que já atingiram o estoque mínimo são removidos da rota, minimizando o percurso e, consequentemente, o tempo total de entrega. 
    - A cada iteração do loop principal, a rota é recalculada para garantir que apenas os armazéns que ainda precisam de reabastecimento sejam visitados.

### transporte.py

Responsável pela implementação do sistema de otimização de rotas, visualizado através da biblioteca Pygame, utilizando as classes e métodos definidos anteriormente. 

Vamos agora revisar e detalhar as principais funções e objetivos do código.

Importações e Configurações Iniciais: 
- Pygame e outras bibliotecas: Utilizadas para a interface gráfica e manipulações matemáticas.
- Constantes de configuração: Incluem dimensões da tela, tamanho da população, número de gerações, etc.

Classes Definidas: 
- Armazém: Armazena dados como localização, nome da cidade e estoque mínimo.
- Individuo: Representa uma solução potencial no algoritmo genético, incluindo veículos, capacidade e rota.

Funções Principais:
- calcular_matriz_distancias(): Calcula e retorna uma matriz de distâncias entre todas as cidades.
- gerar_populacao(): Gera uma população inicial de indivíduos com rotas aleatórias.
- order_crossover(): Realiza o crossover ordenado entre dois indivíduos para gerar um novo.
- mutate(): Aplica uma mutação aleatória na rota de um indivíduo.
- init_screen(): Inicializa a tela do Pygame.
- desenhar_rotas(): Visualiza as rotas entre armazéns na tela do Pygame.
- desenhar_info(): Exibe informações sobre a geração atual e o melhor indivíduo.

Métodos de Seleção: 
- Vários métodos de seleção de pais como seleção aleatória, torneio, roleta, rank são definidos para escolher os pais.

Loop Principal:
- main(): Contém o loop principal onde ocorre o processo do algoritmo genético:
- Avalia o fitness de cada indivíduo.
- Mantém o melhor indivíduo como parte da técnica de elitismo.
- Seleciona pais e gera novos indivíduos através de crossover e mutação.
- Repete o processo para o número definido de gerações.

### Apresentação dos resultados

Criação de uma simulação gráfica para observar o comportamento e a eficácia das rotas geradas pela evolução de indivíduos em um ambiente simulado.
Execução e Visualização:
- Visualização da melhor rota de forma interativa conforme ocorre a evolução ao longo das gerações.
- O gráfico exibe as coordenadas x,y permitindo ao usuário observar a evolução da otimização do tempo em relação à geração.


### Conclusão

Este código serve como um exemplo robusto de como aplicar conceitos de algoritmos genéticos a problemas práticos de otimização, com o benefício adicional de visualização gráfica para uma melhor compreensão dos processos envolvidos.
