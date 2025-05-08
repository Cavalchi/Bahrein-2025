import fastf1
from fastf1 import get_session
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta

#  Configuração inicial 
session = get_session(2025, 'Bahrain', 'R')
session.load()

# Definindo os pilotos e coletando dados dos stints finais 
drivers = {'Russell': '63', 'Norris': '4'}
laps = session.laps

# Coletando os dados reais de Norris e Russell
voltas_russell = laps.pick_driver(drivers['Russell']).copy()
voltas_norris = laps.pick_driver(drivers['Norris']).copy()

# Focando nas voltas finais após o pit stop (voltando do 52 até a 57)
voltas_russell = voltas_russell[(voltas_russell['LapNumber'] >= 52) & (voltas_russell['LapNumber'] <= 57)]
voltas_norris = voltas_norris[(voltas_norris['LapNumber'] >= 52) & (voltas_norris['LapNumber'] <= 57)]

# Convertendo os tempos para segundos
voltas_russell['LapTimeSeconds'] = voltas_russell['LapTime'].dt.total_seconds()
voltas_norris['LapTimeSeconds'] = voltas_norris['LapTime'].dt.total_seconds()

# Função auxiliar para formatar tempo 
def format_time(seconds):
    mins = int(seconds // 60)
    secs = seconds % 60
    return f"{mins}:{secs:04.1f}"

#Simulação simplificada (modelo teórico) 
norris_times = voltas_norris['LapTimeSeconds'].values
russell_times = voltas_russell['LapTimeSeconds'].values


initial_gap = 2.6 
dirty_air_penalty = 0.15  
pace_drop_per_lap = 0.1  


gap_evolution = [initial_gap]
ultrapassagem_volta = None


for i, (n_time, r_time) in enumerate(zip(norris_times, russell_times)):
    r_time_simulated = r_time + dirty_air_penalty + (i * pace_drop_per_lap)
    gap_change = r_time_simulated - n_time
    current_gap = gap_evolution[-1] - gap_change

    
    if current_gap < 0 and ultrapassagem_volta is None:
        ultrapassagem_volta = 52 + i + 1

    gap_evolution.append(current_gap)

# Gap para todas as voltas (52 a 57)
voltas = np.arange(52, 58)
if len(gap_evolution) < len(voltas):
    gap_evolution.extend([gap_evolution[-1]] * (len(voltas) - len(gap_evolution)))

#  Resultados e Gráficos
print(f"\nResumo da Simulação:")
print(f"Gap inicial: {initial_gap} segundos")
print(f"Gap final após simulação: {gap_evolution[-1]:.2f} segundos")
if ultrapassagem_volta:
    print(f"✅ Ultrapassagem ocorreu na volta {ultrapassagem_volta}")
else:
    print(f"❌ Sem ultrapassagem")

# Gráfico de Comparação de Tempos
plt.figure(figsize=(10, 5))
plt.plot(voltas_russell['LapNumber'], voltas_russell['LapTimeSeconds'], marker='o', color='blue', label='Russell (Real)')
plt.plot(voltas_norris['LapNumber'], voltas_norris['LapTimeSeconds'], marker='o', color='red', label='Norris (Real)')
plt.title('Comparação de Ritmo nas Voltas Finais (Real)')
plt.xlabel('Volta')
plt.ylabel('Tempo (segundos)')
plt.legend()
plt.grid(True)
plt.gca().invert_yaxis()


locs, _ = plt.yticks()
plt.yticks(locs, [format_time(t) for t in locs])
plt.xlim(52, 57)
plt.show()

# Gráfico de Evolução do Gap 
plt.figure(figsize=(10, 4))
plt.plot(voltas, gap_evolution[:len(voltas)], marker='x', color='purple')
plt.title('Evolução do Gap - Norris vs Russell (Simulação)')
plt.xlabel('Volta')
plt.ylabel('Gap (s)')
plt.axhline(0, color='black', linestyle='--', alpha=0.7)


if ultrapassagem_volta:
    plt.axvline(ultrapassagem_volta, color='green', linestyle=':', label=f'Ultrapassagem na volta {ultrapassagem_volta}')
    plt.legend()

plt.grid(True)
plt.show()
