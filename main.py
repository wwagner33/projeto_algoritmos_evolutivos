from environment.open_environment import OpenEnvironment
from simulation.sim_pygame import PygameVisualizer
from algorithms.genetic_algorithm import GeneticAlgorithm

def main():
    # Cria o ambiente
    env = OpenEnvironment(grid_size=(50, 50), num_obstacles=20, num_targets=3)

    # Cria algoritmo bioinspirado (GA, por exemplo)
    algorithm = GeneticAlgorithm(environment=env, num_agents=10)

    # Inicializa visualizador
    visualizer = PygameVisualizer(environment=env, algorithm=algorithm)
    visualizer.run()

if __name__ == "__main__":
    main()
