import streamlit as st
import pandas as pd
import altair as alt
import os
import subprocess

# ─── Página e Configuração ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Simulação & Dashboard Busca e Salvamento",
    layout="wide"
)
st.title("🚀 Ambiente de Simulação & Dashboard")

# ─── Sidebar: Parâmetros ─────────────────────────────────────────────────────
st.sidebar.header("Parâmetros da Simulação")
grid_width      = st.sidebar.number_input("Grid Width",      10, 100, 40)
grid_height     = st.sidebar.number_input("Grid Height",     10, 100, 30)
num_obstacles   = st.sidebar.number_input("Número de Obstáculos", 0, grid_width*grid_height//2, 50)
num_agents      = st.sidebar.number_input("Número de Agentes",   1, grid_width*grid_height//4, 10)
num_targets     = st.sidebar.number_input("Número de Alvos",      1, grid_width*grid_height//4, 3)
agent_battery   = st.sidebar.number_input("Bateria Inicial",     1, 1000, 100)
agent_speed     = st.sidebar.number_input("Velocidade do Agente", 1, 10, 1)
target_lifetime = st.sidebar.number_input("Tempo de Vida do Alvo",1, 10000, 200)
max_steps       = st.sidebar.number_input("Max Steps",          1, 5000, 1000)
num_runs        = st.sidebar.number_input("Número de Execuções", 1, 100, 10)

run_button = st.sidebar.button("▶️ Executar Simulações")
log_path   = os.path.join("data", "simulation_log.csv")

# ─── Executar Script de Simulação Externo ─────────────────────────────────────
if run_button:
    # limpa log anterior
    if os.path.isfile(log_path): os.remove(log_path)
    st.info("🔄 Iniciando simulações com Pygame... janela aparecerá")
    # Chama o script externo que abre uma janela Pygame e grava o log
    subprocess.call([
        "python3", "simulation/sim_pygame.py",
        str(grid_width), str(grid_height),
        str(num_obstacles), str(num_agents), str(num_targets),
        str(agent_battery), str(agent_speed), str(target_lifetime),
        str(max_steps), str(num_runs)
    ])
    st.success("✅ Simulações concluídas! Log gravado em data/simulation_log.csv")

# ─── Ler e Exibir Logs ───────────────────────────────────────────────────────
if os.path.isfile(log_path):
    df = pd.read_csv(log_path)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        st.subheader("📋 Resultados de Simulação")
        st.dataframe(df)
        st.markdown("---")

        # Zoom eixo Y para pequenas diferenças
        min_t, max_t = df['search_time_seconds'].min(), df['search_time_seconds'].max()
        pad = (max_t - min_t) * 0.05
        ydom = [min_t - pad, max_t + pad]

        # Tempo por Run
        st.subheader("⏱ Tempo por Run")
        c1 = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('simulation_id:O', title='Run ID'),
            y=alt.Y('search_time_seconds:Q', scale=alt.Scale(domain=ydom), title='Tempo (s)'),
            tooltip=['simulation_id', 'search_time_seconds']
        ).properties(height=300)
        st.altair_chart(c1, use_container_width=True)

        # Distribuição de Tempos
        st.subheader("📊 Distribuição dos Tempos de Busca")
        c2 = alt.Chart(df).mark_bar().encode(
            x=alt.X('search_time_seconds:Q', bin=alt.Bin(maxbins=20), title='Tempo (s)'),
            y=alt.Y('count():Q', title='Frequência'),
            tooltip=['count()']
        ).properties(height=300)
        st.altair_chart(c2, use_container_width=True)

        # Bateria Média Restante
        st.subheader("🔋 Bateria Média Restante por Run")
        c3 = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('simulation_id:O', title='Run ID'),
            y=alt.Y('avg_battery_remaining:Q', title='Bateria Média'),
            tooltip=['simulation_id', 'avg_battery_remaining']
        ).properties(height=300)
        st.altair_chart(c3, use_container_width=True)

        # Targets Expirados
        st.subheader("💀 Targets Expirados por Run")
        c4 = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('simulation_id:O', title='Run ID'),
            y=alt.Y('targets_expired:Q', title='Expirados'),
            tooltip=['simulation_id', 'targets_expired']
        ).properties(height=300)
        st.altair_chart(c4, use_container_width=True)

        # Sucesso vs Fracasso
        st.subheader("✅ Sucesso vs ❌ Fracasso")
        pie = alt.Chart(df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('count():Q', title='Contagem'),
            color=alt.Color('success:N', legend=alt.Legend(title='Sucesso'))
        ).properties(width=300, height=300)
        st.altair_chart(pie)

    else:
        st.warning("Arquivo de log vazio, execute as simulações.")
else:
    st.info("Nenhum log encontrado. Execute as simulações pelo botão.")
