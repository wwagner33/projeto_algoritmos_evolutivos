# sim_log_analyzer.py

import pandas as pd
import matplotlib.pyplot as plt

# 1. Carrega o log
df = pd.read_csv("data/simulation_log.csv")

if df.empty:
    print("⚠️ Nenhum dado encontrado em simulation_log.csv")
    exit()

# 2. Estatísticas básicas
print("\n===== Estatísticas Gerais =====")
print(f"Total de runs: {len(df)}")
print(f"Taxa de sucesso: {df['success'].mean()*100:.1f}%")
print(f"Tempo médio de busca: {df['search_time_seconds'].mean():.2f}s")
print(f"Targets expirados médio: {df['targets_expired'].mean():.2f}")
print(f"Bateria média restante: {df['avg_battery_remaining'].mean():.2f}\n")

# 3. Evolução do tempo por run (linha)
plt.figure()
plt.plot(df["simulation_id"], df["search_time_seconds"], marker="o")
plt.title("Evolução do Tempo de Busca")
plt.xlabel("ID da Simulação")
plt.ylabel("Tempo (s)")
plt.grid(True)
plt.tight_layout()
plt.show()

# 4. Evolução da bateria média restante por run
plt.figure()
plt.plot(df["simulation_id"], df["avg_battery_remaining"], marker="o")
plt.title("Bateria Média Restante por Simulação")
plt.xlabel("ID da Simulação")
plt.ylabel("Bateria Média Restante")
plt.grid(True)
plt.tight_layout()
plt.show()

# 5. Evolução dos targets expirados por run
plt.figure()
plt.plot(df["simulation_id"], df["targets_expired"], marker="o")
plt.title("Targets Expirados por Simulação")
plt.xlabel("ID da Simulação")
plt.ylabel("Número de Expirações")
plt.grid(True)
plt.tight_layout()
plt.show()

# 6. Histograma dos tempos de busca
plt.figure()
plt.hist(df["search_time_seconds"], bins=10, edgecolor="black")
plt.title("Distribuição dos Tempos de Busca")
plt.xlabel("Tempo (s)")
plt.ylabel("Frequência")
plt.grid(True)
plt.tight_layout()
plt.show()

# 7. Pizza de sucesso vs fracasso
plt.figure()
df["success"].value_counts().plot.pie(autopct="%1.1f%%", label="")
plt.title("Sucesso vs Fracasso")
plt.tight_layout()
plt.show()
