| Categoria                         | Algoritmo                              | Inspiração                                 | Bibliotecas Python Recomendadas                  | Visualização com `pygame`/`matplotlib`                        |
| --------------------------------- | -------------------------------------- | ------------------------------------------ | ------------------------------------------------ | ------------------------------------------------------------- |
| **1. Evolutivos Clássicos**       | **Genetic Algorithm (GA)**             | Genética natural                           | `DEAP`, `PyGAD`, `Inspyred`                      | Trajetória da melhor solução, evolução do fitness             |
|                                   | **Programação Genética (GP)**          | Evolução de programas                      | `DEAP`, `Karoo GP`, `TPOT`                       | Árvore de expressão, evolução da solução                      |
|                                   | **Estrategias Evolutivas (ES)**        | Mutação e seleção com variância adaptativa | `DEAP`, `Nevergrad`, `CMA-ES`                    | Curvas de convergência                                        |
|                                   | **Evolução Diferencial (DE)**          | Vetores diferenciais                       | `SciPy`, `Nevergrad`, `Inspyred`                 | Nuvem de soluções e fitness                                   |
|                                   | **CMA-ES**                             | Estatísticas de população                  | `pycma`, `Nevergrad`                             | Covariância entre variáveis, convergência                     |
| **2. Inteligência de Enxames**    | **Particle Swarm Optimization (PSO)**  | Bandos de pássaros/peixes                  | `pyswarms`, `optuna`, `Inspyred`                 | Partículas se movendo no espaço de busca (ótimo com `pygame`) |
|                                   | **Ant Colony Optimization (ACO)**      | Caminhos com feromônio                     | `ACO-Pants`, `inspyred`, `opt4jpy`               | Caminhos otimizados, rede de trilhas (com `pygame`)           |
|                                   | **Bee Colony Optimization (BCO)**      | Abelhas explorando alimento                | `inspyred`, `PySwarm`                            | Trajetória e área explorada                                   |
|                                   | **Firefly Algorithm**                  | Atração por intensidade (fitness)          | `firefly-algorithm`, `optproblems`, `inspyred`   | Luzes se movendo no espaço 2D (com brilho proporcional)       |
|                                   | **Bat Algorithm**                      | Eco-localização e busca adaptativa         | `bat_algorithm`, `nature-inspired-algorithms`    | Movimento das soluções (com som, se for ousado 😄)            |
| **3. Coletivos e Populacionais**  | **Cuckoo Search**                      | Postura de ovos em ninhos alheios          | `inspyred`, `pynature`, `nevergrad`              | Substituição de soluções e outliers no fitness                |
|                                   | **Grey Wolf Optimizer (GWO)**          | Hierarquia de caça                         | `nature-inspired-algorithms`, `mealpy`, `optuna` | Movimento coordenado em torno da melhor solução               |
|                                   | **Whale Optimization Algorithm (WOA)** | Movimento em espiral de baleias            | `mealpy`, `nature-inspired-algorithms`           | Curvas em espiral para solução ótima                          |
|                                   | **Artificial Immune Systems (AIS)**    | Imunologia adaptativa                      | `libais`, `inspyred`, `clonalg`                  | Gráfico de detecção de anomalias (com `matplotlib`)           |
| **4. Baseados em Física/Química** | **Simulated Annealing (SA)**           | Resfriamento térmico                       | `SciPy`, `Simanneal`                             | Temperatura x energia (fitness)                               |
|                                   | **Harmony Search (HS)**                | Composição musical                         | `pyharmonysearch`, `inspyred`                    | Acordes e notas vs aptidão (score)                            |
| **5. Ecossistemas e Sociais**     | **Coevolutionary Algorithms**          | Espécies interagindo (predador-presa)      | `DEAP`, `Lea`, `eco-evo`                         | Populações separadas com fitness cruzado                      |
|                                   | **Cultural Algorithms**                | Memória coletiva da população              | `cultural`, `inspyred`                           | Fitness individual vs conhecimento cultural médio             |

Vamos usar uma grade 2D (grid) onde:

0 = célula livre

1 = obstáculo

2 = ponto de partida

3 = alvo

A = posição do agente

Representar cada célula da grid com cor:

Branco = livre

Cinza = obstáculo

Verde = início

Vermelho = alvo

Azul = agente

search_and_rescue_sim/
│
├── main.py # Script principal para execução das simulações
│
├── algorithms/ # Algoritmos bioinspirados (GA, PSO, ACO, etc.)
│ ├── genetic_algorithm.py
│ ├── particle_swarm.py
│ ├── ant_colony.py
│ └── base_algorithm.py
│
├── environment/ # Ambiente de simulação
│ ├── environment.py
│ ├── open_environment.py
│ ├── closed_environment.py
│ ├── grid.py
│ └── target.py
│
├── agents/ # Definição dos agentes (buscadores e alvos)
│ ├── agent.py
│ └── search_agent.py
│
├── visualization/ # Visualização com Pygame
│ └── pygame_visualizer.py
│
├── utils/ # Funções utilitárias e helpers
│ ├── metrics.py
│ └── helpers.py
│
├── data/ # Dados salvos (resultados, logs)
│
├── requirements.txt # Dependências do projeto
└── README.md # Documentação do projeto

Para os agentes:

Implementar e detalhar cada algoritmo bioinspirado (GA, PSO, ACO).

Definir estratégias de movimentação dos agentes.

Criar módulos de métricas para medir eficiência dos algoritmos (tempo médio, sucesso, etc).

Salvar e analisar logs e gráficos usando matplotlib.
