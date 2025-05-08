# 🏁 F1 Performance Strategy Simulation — Bahrain GP 2025

Este projeto é uma **análise estratégica de stint final** baseada em dados reais da Fórmula 1, usando a biblioteca [FastF1](https://theoehrly.github.io/Fast-F1/). Exploramos como **Oscar Piastri poderia ajudar Lando Norris a ultrapassar George Russell** manipulando o ritmo em função do desgaste dos pneus e do ar sujo.

---

## 🎯 Objetivo

Simular, com dados reais:
- Como o ritmo de **Russell se deterioraria** sob efeito do ar sujo de Piastri
- Se **Norris conseguiria ultrapassar** considerando seus tempos reais de volta
- Em qual volta isso aconteceria, se fosse possível

---

## ⚙️ Tecnologias utilizadas

- **Python 3.11**
- **FastF1** para coleta de dados oficiais da corrida
- **Pandas** para manipulação de dados
- **Matplotlib + Seaborn** para visualização
- **Simulação customizada** de desgaste de pneus e perda por ar sujo

---

## 📊 Métricas calculadas

- Média de tempo por volta no stint final
- Gap acumulado volta a volta
- Simulação de perda progressiva de performance com o tempo
- Efeito do ar sujo estimado em +0.25s/volta
- Desgaste estimado em +0.03s por volta após troca

---

## 📈 Resultados

- Russell manteve ritmo mais forte que Norris no stint final
- Com desgaste + ar sujo, seu tempo simulado ficou **mais lento a cada volta**
- A simulação mostra **que Norris ultrapassaria Russell na volta 56**, caso Piastri tivesse mantido o ritmo e forçado o ar sujo

---

## 📷 Gráficos gerados

- Tempo de volta dos últimos stints (Piastri, Russell, Norris)
- Comparação visual de desempenho por volta
- Simulação com gaps e ganhos de tempo acumulados

---

## 🤖 Aplicações práticas

- **Tomada de decisão em tempo real em equipes de corrida**
- **Modelagem de estratégias de pit stop e ritmo**
- **Avaliação de pilotos com base em performance relativa**
- **Simulações em contextos esportivos reais com Data Science**
