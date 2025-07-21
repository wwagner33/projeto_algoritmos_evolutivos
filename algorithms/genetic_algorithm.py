from .base_algorithm import BaseAlgorithm
from agents.search_agent import SearchAgent

class GeneticAlgorithm(BaseAlgorithm):
    def initialize_agents(self):
        self.agents = [SearchAgent(self.environment.grid.get_random_free_cell()) for _ in range(self.num_agents)]

    def step(self):
        # Aqui implementa-se um passo evolutivo do GA
        pass
