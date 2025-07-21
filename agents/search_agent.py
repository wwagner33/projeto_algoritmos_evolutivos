from .agent import Agent

class SearchAgent(Agent):
    def __init__(self, position):
        super().__init__(position)
        self.found_targets = []

    def search(self, environment):
        # Método que implementará o comportamento específico de busca
        pass
