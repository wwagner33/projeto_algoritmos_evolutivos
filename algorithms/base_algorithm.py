class BaseAlgorithm:
    def __init__(self, environment, num_agents):
        self.environment = environment
        self.agents = []
        self.num_agents = num_agents
        self.initialize_agents()

    def initialize_agents(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError
