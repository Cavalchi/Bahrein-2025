# --- F1 Strategy Simulation Engine v2.0 ---
# Autor: João Pedro Cavalchi de Carvalho

import fastf1
import matplotlib.pyplot as plt
import numpy as np

def simular_batalha_final(session, piloto_cacador, piloto_alvo, volta_inicial, gap_inicial, penalidade_ar_sujo=0.15, perda_ritmo_pneu=0.05):
    """
    Simula uma batalha de final de corrida, modelando o efeito do ar sujo e desgaste de pneus.

    Args:
        session: Objeto da sessão do FastF1 já carregado.
        piloto_cacador (str): Sigla do piloto que está caçando (ex: 'NOR').
        piloto_alvo (str): Sigla do piloto que está sendo caçado (ex: 'RUS').
        volta_inicial (int): Volta em que a simulação começa.
        gap_inicial (float): Diferença de tempo em segundos no início da simulação.
        penalidade_ar_sujo (float): Segundos de penalidade por volta para o piloto de trás.
        perda_ritmo_pneu (float): Segundos que o pneu do piloto alvo perde a cada volta.

    Returns:
        dict: Um dicionário contendo os resultados da simulação.
    """
    print(f"\n--- Iniciando Simulação: {piloto_cacador} vs {piloto_alvo} ---")
    
    laps = session.laps
    voltas_cacador = laps.pick_driver(piloto_cacador).copy()
    voltas_alvo = laps.pick_driver(piloto_alvo).copy()
    
    # Filtra as voltas relevantes para a simulação
    voltas_cacador = voltas_cacador[voltas_cacador['LapNumber'] >= volta_inicial]
    voltas_alvo = voltas_alvo[voltas_alvo['LapNumber'] >= volta_inicial]
    
    if voltas_cacador.empty or voltas_alvo.empty:
        print("!!! Erro: Não foram encontrados dados de voltas para um dos pilotos no período especificado.")
        return None

    # Converte tempos para segundos
    voltas_cacador['LapTimeSeconds'] = voltas_cacador['LapTime'].dt.total_seconds()
    voltas_alvo['LapTimeSeconds'] = voltas_alvo['LapTime'].dt.total_seconds()

    # Prepara os tempos de volta para a simulação
    tempos_cacador = voltas_cacador['LapTimeSeconds'].values
    tempos_alvo = voltas_alvo['LapTimeSeconds'].values
    
    # Garante que ambos os arrays tenham o mesmo tamanho
    min_laps = min(len(tempos_cacador), len(tempos_alvo))
    tempos_cacador = tempos_cacador[:min_laps]
    tempos_alvo = tempos_alvo[:min_laps]
    
    gap_evolution = [gap_inicial]
    ultrapassagem_volta = None
    
    print(f"Parâmetros: Gap Inicial={gap_inicial}s, Penalidade Ar Sujo={penalidade_ar_sujo}s, Desgaste Pneu={perda_ritmo_pneu}s/volta")

    for i in range(min_laps):
        # O tempo simulado do piloto alvo é seu tempo real + penalidades
        tempo_alvo_simulado = tempos_alvo[i] + penalidade_ar_sujo + (i * perda_ritmo_pneu)
        
        # O ganho/perda na volta é a diferença entre os tempos
        gap_change = tempo_alvo_simulado - tempos_cacador[i]
        
        current_gap = gap_evolution[-1] - gap_change
        
        if current_gap < 0 and ultrapassagem_volta is None:
            ultrapassagem_volta = volta_inicial + i # A ultrapassagem acontece no final da volta i
        
        gap_evolution.append(current_gap)

    voltas_simuladas = np.arange(volta_inicial, volta_inicial + min_laps + 1)

    # --- Plotagem dos Resultados ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Gráfico 1: Comparação de Ritmo
    ax1.plot(voltas_alvo['LapNumber'], tempos_alvo, marker='o', color='deepskyblue', label=f'{piloto_alvo} (Tempo Real)')
    ax1.plot(voltas_cacador['LapNumber'], tempos_cacador, marker='o', color='darkorange', label=f'{piloto_cacador} (Tempo Real)')
    ax1.set_title('Comparativo de Ritmo de Volta (Dados Reais)')
    ax1.set_ylabel('Tempo de Volta (s)')
    ax1.grid(True, linestyle='--')
    ax1.legend()

    # Gráfico 2: Evolução do Gap (Simulação)
    ax2.plot(voltas_simuladas, gap_evolution, marker='x', color='purple', label='Gap Simulado')
    ax2.axhline(0, color='black', linestyle='--', alpha=0.7, label='Ponto de Ultrapassagem')
    if ultrapassagem_volta:
        ax2.axvline(ultrapassagem_volta, color='green', linestyle=':', label=f'Ultrapassagem na Volta {ultrapassagem_volta}')
    ax2.set_title('Evolução do Gap (Simulação)')
    ax2.set_xlabel('Número da Volta')
    ax2.set_ylabel('Gap para o piloto alvo (s)')
    ax2.grid(True, linestyle='--')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

    # Resultados Finais
    resultados = {
        "gap_final": gap_evolution[-1],
        "ultrapassagem_ocorrida": bool(ultrapassagem_volta),
        "volta_da_ultrapassagem": ultrapassagem_volta
    }
    
    print(f"Resultado da Simulação: Gap Final = {resultados['gap_final']:.2f}s. Ultrapassagem: {'Sim' if resultados['ultrapassagem_ocorrida'] else 'Não'}")
    return resultados

# --- Execução  ---
if __name__ == "__main__":
    session = fastf1.get_session(2025, 'Bahrain', 'R')
    session.load()
    
    simular_batalha_final(
        session=session,
        piloto_cacador='NOR',
        piloto_alvo='RUS',
        volta_inicial=52,
        gap_inicial=2.6
    )
