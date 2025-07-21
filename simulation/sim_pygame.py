# Arquivo: simulation/sim_pygame.py

import pygame
import sys
import random
import time
import csv
import os
from datetime import datetime
import argparse

# ─── CONFIGURAÇÕES GERAIS ───────────────────────────────────────────────────────
GRID_WIDTH, GRID_HEIGHT = 40, 30
CELL_SIZE = 20
FPS = 20
NUM_OBSTACLES = 100  # aumenta chance de falha
NUM_AGENTS = 15      # agentes para busca
NUM_TARGETS = 3      # alvos a encontrar
INFO_AREA_HEIGHT = 40

# ─── CONSTRAINTS ────────────────────────────────────────────────────────────────
AGENT_BATTERY = 200
AGENT_SPEED = 1
TARGET_LIFETIME = 400
MAX_STEPS = 1000
NUM_RUNS = 10       # número padrão de execuções

# ─── LOG PATH ───────────────────────────────────────────────────────────────────
LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'simulation_log.csv')

# ─── CORES ───────────────────────────────────────────────────────────────────────
COLORS = {
    'background': (245, 245, 245),
    'grid':       (200, 200, 200),
    'obstacle':   (50, 50, 50),
    'agent':      (0, 100, 250),
    'target':     (250, 50, 100),
    'info_area':  (230, 230, 230),
}

# ─── CLASSES ─────────────────────────────────────────────────────────────────────
class Agent:
    def __init__(self, pos):
        self.position = pos
        self.battery = AGENT_BATTERY
        self.speed = AGENT_SPEED

    def step(self, obstacles):
        if self.battery <= 0:
            return
        x, y = self.position
        moves = [(0,-1),(0,1),(-1,0),(1,0)]
        random.shuffle(moves)
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and (nx, ny) not in obstacles:
                self.position = (nx, ny)
                self.battery -= 1
                return

class Target:
    def __init__(self, pos):
        self.position = pos
        self.ttl = TARGET_LIFETIME
    def step(self):
        self.ttl -= 1
        return self.ttl > 0

# ─── HELPERS ─────────────────────────────────────────────────────────────────────
def create_obstacles():
    s = set()
    while len(s) < NUM_OBSTACLES:
        s.add((random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT)))
    return s

def random_free_position(obstacles, occupied):
    while True:
        p = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        if p not in obstacles and p not in occupied:
            return p

def log_simulation_result(sim_id, stats):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(stats.keys()))
        if not exists:
            writer.writeheader()
        writer.writerow(stats)
    print(f"→ Sim #{sim_id} log gravado")

# ─── HEADLESS MODE: MULTI-RUNS ───────────────────────────────────────────────────
def simulate_headless(num_runs):
    for sim_id in range(1, num_runs + 1):
        # setup
        obstacles = create_obstacles()
        occupied = set(obstacles)
        targets = []
        for _ in range(NUM_TARGETS):
            p = random_free_position(obstacles, occupied)
            occupied.add(p)
            targets.append(Target(p))
        agents = []
        for _ in range(NUM_AGENTS):
            p = random_free_position(obstacles, occupied)
            occupied.add(p)
            agents.append(Agent(p))

        # stats
        stats = {
            'simulation_id': sim_id,
            'timestamp': datetime.now().isoformat(),
            'grid_size': f"{GRID_WIDTH}x{GRID_HEIGHT}$",
            'num_agents': NUM_AGENTS,
            'num_targets': NUM_TARGETS,
            'num_obstacles': NUM_OBSTACLES,
            'search_time_seconds': 0,
            'targets_found': 0,
            'targets_expired': 0,
            'avg_battery_remaining': 0,
            'success': False
        }

        start = time.time()
        step = 0
        sim_done = False
        while step < MAX_STEPS and not sim_done and any(a.battery > 0 for a in agents):
            step += 1
            # targets TTL
            for t in targets[:]:
                if not t.step():
                    targets.remove(t)
                    stats['targets_expired'] += 1
            # move agents
            for a in agents:
                a.step(obstacles)
                for t in targets[:]:
                    if a.position == t.position:
                        stats['targets_found'] += 1
                        targets.remove(t)
            # stop if all found
            if stats['targets_found'] == NUM_TARGETS:
                sim_done = True
        end = time.time()
        # finalize stats
        stats['search_time_seconds'] = round(end - start, 2)
        stats['avg_battery_remaining'] = round(sum(a.battery for a in agents) / len(agents), 2)
        stats['success'] = (stats['targets_found'] == NUM_TARGETS)

        log_simulation_result(sim_id, stats)
    print("🎉 Simulações headless concluídas!")

# ─── INTERACTIVE MODE: PYGAME WINDOW ────────────────────────────────────────────
def simulate_interactive(num_runs):
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH*CELL_SIZE, GRID_HEIGHT*CELL_SIZE + INFO_AREA_HEIGHT))
    pygame.display.set_caption("Busca & Salvamento Com Falhas")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 16)

    for sim_id in range(1, num_runs + 1):
        obstacles = create_obstacles()
        occupied = set(obstacles)
        targets = []
        for _ in range(NUM_TARGETS):
            p = random_free_position(obstacles, occupied)
            occupied.add(p)
            targets.append(Target(p))
        agents = []
        for _ in range(NUM_AGENTS):
            p = random_free_position(obstacles, occupied)
            occupied.add(p)
            agents.append(Agent(p))

        stats = {
            'simulation_id': sim_id,
            'timestamp': datetime.now().isoformat(),
            'grid_size': f"{GRID_WIDTH}x{GRID_HEIGHT}$",
            'num_agents': NUM_AGENTS,
            'num_targets': NUM_TARGETS,
            'num_obstacles': NUM_OBSTACLES,
            'search_time_seconds': 0,
            'targets_found': 0,
            'targets_expired': 0,
            'avg_battery_remaining': 0,
            'success': False
        }

        start = time.time()
        step = 0
        sim_done = False
        while step < MAX_STEPS and not sim_done and any(a.battery > 0 for a in agents):
            step += 1
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # TTL
            for t in targets[:]:
                if not t.step():
                    targets.remove(t)
                    stats['targets_expired'] += 1
            # move e encontro
            for a in agents:
                a.step(obstacles)
                for t in targets[:]:
                    if a.position == t.position:
                        stats['targets_found'] += 1
                        targets.remove(t)
            # stop
            if stats['targets_found'] == NUM_TARGETS:
                sim_done = True

            # desenho
            screen.fill(COLORS['background'])
            for x in range(0, GRID_WIDTH*CELL_SIZE, CELL_SIZE):
                pygame.draw.line(screen, COLORS['grid'], (x,0), (x, GRID_HEIGHT*CELL_SIZE))
            for y in range(0, GRID_HEIGHT*CELL_SIZE, CELL_SIZE):
                pygame.draw.line(screen, COLORS['grid'], (0,y), (GRID_WIDTH*CELL_SIZE, y))
            for ox, oy in obstacles:
                pygame.draw.rect(screen, COLORS['obstacle'], pygame.Rect(ox*CELL_SIZE, oy*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for t in targets:
                pygame.draw.circle(screen, COLORS['target'], (t.position[0]*CELL_SIZE+CELL_SIZE//2, t.position[1]*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3)
            for a in agents:
                pygame.draw.circle(screen, COLORS['agent'], (a.position[0]*CELL_SIZE+CELL_SIZE//2, a.position[1]*CELL_SIZE+CELL_SIZE//2), int(CELL_SIZE/2.5))
            elapsed = time.time() - start
            pygame.draw.rect(screen, COLORS['info_area'], pygame.Rect(0, GRID_HEIGHT*CELL_SIZE, GRID_WIDTH*CELL_SIZE, INFO_AREA_HEIGHT))
            info = f"Tempo: {elapsed:.2f}s  Encontrados: {stats['targets_found']} / {NUM_TARGETS}  Step {step}"
            screen.blit(font.render(info, True, (10,10,10)), (10, GRID_HEIGHT*CELL_SIZE+10))
            pygame.display.flip()
            clock.tick(FPS)

        stats['search_time_seconds'] = round(time.time() - start, 2)
        stats['avg_battery_remaining'] = round(sum(a.battery for a in agents)/len(agents), 2)
        stats['success'] = (stats['targets_found'] == NUM_TARGETS)
        log_simulation_result(sim_id, stats)

    print("🎉 Simulações interativas concluídas! Veja data/simulation_log.csv")
    pygame.quit()

# ─── API para Streamlit ─────────────────────────────────────────────────────────
def run_simulation(params):
    simulate_headless(params.get('num_runs', NUM_RUNS))

# ─── CLI ENTRYPOINT ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--headless', action='store_true', help='Executar sem GUI')
    parser.add_argument('--num-runs',    type=int, default=10, help='Número de execuções (padrão 10)')
    args = parser.parse_args()

    if os.path.isfile(LOG_PATH):
        os.remove(LOG_PATH)

    if args.headless:
        simulate_headless(args.num_runs)
    else:
        simulate_interactive(args.num_runs)

if __name__ == '__main__':
    main()
