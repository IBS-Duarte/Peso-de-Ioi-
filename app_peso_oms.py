import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

def calcular_idade_meses(data_nascimento, data_medicao):
    delta = data_medicao - data_nascimento
    idade_meses = delta.days / 30.44
    return round(idade_meses, 2)

# Medidas reais do usuário (datas no formato yyyy, m, d)
medicoes_reais = [
    {"data_medicao": date(2025, 5, 11), "peso_kg": 2.77},
    {"data_medicao": date(2025, 5, 17), "peso_kg": 2.78},
    {"data_medicao": date(2025, 6, 18), "peso_kg": 3.312},
    {"data_medicao": date(2025, 7, 1), "peso_kg": 3.615},
    {"data_medicao": date(2025, 7, 3), "peso_kg": 3.684},
    {"data_medicao": date(2025, 8, 12), "peso_kg": 4.36},
    {"data_medicao": date(2025, 9, 9), "peso_kg": 4.77},
    {"data_medicao": date(2025, 10, 14), "peso_kg": 5.402},
    {"data_medicao": date(2025, 11, 11), "peso_kg": 5.756},
    {"data_medicao": date(2025, 11, 27), "peso_kg": 5.920},
    {"data_medicao": date(2025, 12, 9), "peso_kg": 6.090},
    {"data_medicao": date(2026, 1, 19), "peso_kg": 6.578},
]

# Curvas OMS (mantidas do exemplo anterior)
who_data = {
    #'z_plus_3': {0: 4.8, 1: 6.2, 2: 7.5, 3: 8.5, 4: 9.3, 5: 10.0, 6: 10.6, 7: 11.1, 8: 11.6, 9: 12.0, 10: 12.4, 11: 12.8, 12: 13.1, 15: 14.1, 18: 15.1, 21: 16.1, 24: 17.1, 30: 19.0, 36: 20.9, 42: 22.9, 48: 24.9, 54: 26.9, 60: 28.8},
    #'z_plus_2': {0: 4.2, 1: 5.5, 2: 6.6, 3: 7.5, 4: 8.2, 5: 8.8, 6: 9.3, 7: 9.8, 8: 10.2, 9: 10.5, 10: 10.9, 11: 11.2, 12: 11.5, 15: 12.4, 18: 13.2, 21: 14.1, 24: 14.8, 30: 16.5, 36: 18.1, 42: 19.8, 48: 21.5, 54: 23.1, 60: 24.8},
    #'z_0': {0: 3.2, 1: 4.2, 2: 5.1, 3: 5.8, 4: 6.4, 5: 6.9, 6: 7.3, 7: 7.6, 8: 7.9, 9: 8.2, 10: 8.5, 11: 8.7, 12: 8.9, 15: 9.6, 18: 10.2, 21: 10.9, 24: 11.5, 30: 12.7, 36: 13.9, 42: 15.1, 48: 16.3, 54: 17.5, 60: 18.7},
    #'z_minus_2': {0: 2.4, 1: 3.2, 2: 3.9, 3: 4.5, 4: 5.0, 5: 5.4, 6: 5.7, 7: 6.0, 8: 6.3, 9: 6.5, 10: 6.7, 11: 6.9, 12: 7.0, 15: 7.6, 18: 8.1, 21: 8.6, 24: 9.0, 30: 9.9, 36: 10.8, 42: 11.7, 48: 12.6, 54: 13.5, 60: 14.3},
    #'z_minus_3': {0: 2.0, 1: 2.7, 2: 3.4, 3: 3.9, 4: 4.4, 5: 4.8, 6: 5.1, 7: 5.3, 8: 5.6, 9: 5.8, 10: 6.0, 11: 6.2, 12: 6.3, 15: 6.9, 18: 7.3, 21: 7.7, 24: 8.1, 30: 8.8, 36: 9.6, 42: 10.4, 48: 11.2, 54: 12.0, 60: 12.7}
    'z_plus_3': {0: 4.8, 1: 6.2, 2: 7.5, 3: 8.5, 4: 9.3, 5: 10.0, 6: 10.6, 7: 11.1, 8: 11.6, 9: 12.0, 10: 12.4, 11: 12.8, 12: 13.1},
    'z_plus_2': {0: 4.2, 1: 5.5, 2: 6.6, 3: 7.5, 4: 8.2, 5: 8.8, 6: 9.3, 7: 9.8, 8: 10.2, 9: 10.5, 10: 10.9, 11: 11.2, 12: 11.5},
    'z_0': {0: 3.2, 1: 4.2, 2: 5.1, 3: 5.8, 4: 6.4, 5: 6.9, 6: 7.3, 7: 7.6, 8: 7.9, 9: 8.2, 10: 8.5, 11: 8.7, 12: 8.9},
    'z_minus_2': {0: 2.4, 1: 3.2, 2: 3.9, 3: 4.5, 4: 5.0, 5: 5.4, 6: 5.7, 7: 6.0, 8: 6.3, 9: 6.5, 10: 6.7, 11: 6.9, 12: 7.0},
    'z_minus_3': {0: 2.0, 1: 2.7, 2: 3.4, 3: 3.9, 4: 4.4, 5: 4.8, 6: 5.1, 7: 5.3, 8: 5.6, 9: 5.8, 10: 6.0, 11: 6.2, 12: 6.3}
}

st.set_page_config(page_title="Acompanhamento de Peso - OMS", layout="wide")
st.title("📊 Acompanhamento de Peso para Meninas (OMS)")
st.markdown("Gráfico baseado nos padrões da Organização Mundial da Saúde")

if 'data_nascimento' not in st.session_state:
    st.session_state.data_nascimento = date(2025, 5, 11)

data_nascimento = st.date_input("Data de nascimento da criança", value=st.session_state.data_nascimento)
st.session_state.data_nascimento = data_nascimento

if st.session_state.data_nascimento is not None and 'measurements' not in st.session_state:
    st.session_state.measurements = []
    for m in medicoes_reais:
        idade_meses = calcular_idade_meses(data_nascimento, m["data_medicao"])
        st.session_state.measurements.append({
            "data_medicao": m["data_medicao"],
            "peso_kg": m["peso_kg"],
            "idade_meses": idade_meses
        })

with st.form("add_measurement"):
    data_medicao = st.date_input("Data da medição", value=date.today())
    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=20.0, value=5.5, step=0.01, format="%.2f")
    submitted = st.form_submit_button("Adicionar Medição")
    if submitted:
        if st.session_state.data_nascimento is not None:
            idade_meses = calcular_idade_meses(data_nascimento, data_medicao)
            st.session_state.measurements.append({
                "data_medicao": data_medicao,
                "peso_kg": peso,
                "idade_meses": idade_meses
            })
            st.success(f"Medição adicionada: {data_medicao.strftime('%d/%m/%Y')}, {peso} kg (Idade: {idade_meses} meses)")
        else:
            st.warning("Por favor, informe a data de nascimento antes de adicionar medições.")

if st.session_state.measurements:
    df = pd.DataFrame(st.session_state.measurements)
    df = df.sort_values('data_medicao')
    df['data_medicao'] = pd.to_datetime(df['data_medicao'])
    df['data_medicao'] = df['data_medicao'].dt.strftime('%d/%m/%y')
    st.dataframe(df, width='stretch')

    if st.button("🗑️ Remover Última Medição"):
        if st.session_state.measurements:
            st.session_state.measurements.pop()
            st.experimental_rerun()

fig = go.Figure()
for z_score, data_dict in who_data.items():
    ages = sorted(data_dict.keys())
    weights = [data_dict[age] for age in ages]
    z_names = {'z_minus_3': 'Z = -3', 'z_minus_2': 'Z = -2', 'z_0': 'Z = 0 (mediana)', 'z_plus_2': 'Z = +2', 'z_plus_3': 'Z = +3'}
    colors = {'z_minus_3': 'red', 'z_minus_2': 'orange', 'z_0': 'green', 'z_plus_2': 'orange', 'z_plus_3': 'red'}
    fig.add_trace(go.Scatter(x=ages, y=weights, mode='lines', name=z_names[z_score],
                             line=dict(color=colors[z_score], width=2, dash='solid' if z_score == 'z_0' else 'dash'), opacity=0.7))

if st.session_state.measurements and st.session_state.data_nascimento is not None:
    df_plot = pd.DataFrame(st.session_state.measurements)
    df_plot = df_plot.sort_values('data_medicao')
    fig.add_trace(go.Scatter(x=df_plot['idade_meses'], y=df_plot['peso_kg'],
                             mode='lines+markers', name='Ioiô',
                             line=dict(color='blue', width=3), marker=dict(size=10, color='blue', symbol='circle')))

fig.update_layout(
    title='Peso para Idade - Meninas (OMS)',
    xaxis_title='Idade (meses)',
    yaxis_title='Peso (kg)',
    hovermode='x unified',
    height=600,
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    xaxis=dict(range=[0, 12], dtick=6),
    yaxis=dict(range=[0, 15])
)
st.plotly_chart(fig, use_container_width=True)

st.info("""
**Interpretação dos Z-scores (OMS):**
- **Z < -3**: Muito baixo peso
- **-3 ≤ Z < -2**: Baixo peso
- **-2 ≤ Z < +2**: Peso adequado
- **Z ≥ +2**: Peso elevado
""")

st.markdown("---")

st.markdown("*Dados baseados nos padrões WHO Child Growth Standards (OMS, 2006)*")


