import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

# Configuração da página
st.set_page_config(page_title="Acompanhamento de Peso - OMS", layout="wide")

# Título
st.title("📊 Acompanhamento de Peso para Meninas (OMS)")
st.markdown("Gráfico baseado nos padrões da Organização Mundial da Saúde")

# Dados das curvas de referência OMS (z-scores)
who_data = {
    'z_minus_3': {0: 2.0, 1: 2.7, 2: 3.4, 3: 3.9, 4: 4.4, 5: 4.8, 6: 5.1, 7: 5.3, 8: 5.6, 9: 5.8, 10: 6.0, 11: 6.2, 12: 6.3, 15: 6.9, 18: 7.3, 21: 7.7, 24: 8.1, 30: 8.8, 36: 9.6, 42: 10.4, 48: 11.2, 54: 12.0, 60: 12.7},
    'z_minus_2': {0: 2.4, 1: 3.2, 2: 3.9, 3: 4.5, 4: 5.0, 5: 5.4, 6: 5.7, 7: 6.0, 8: 6.3, 9: 6.5, 10: 6.7, 11: 6.9, 12: 7.0, 15: 7.6, 18: 8.1, 21: 8.6, 24: 9.0, 30: 9.9, 36: 10.8, 42: 11.7, 48: 12.6, 54: 13.5, 60: 14.3},
    'z_0': {0: 3.2, 1: 4.2, 2: 5.1, 3: 5.8, 4: 6.4, 5: 6.9, 6: 7.3, 7: 7.6, 8: 7.9, 9: 8.2, 10: 8.5, 11: 8.7, 12: 8.9, 15: 9.6, 18: 10.2, 21: 10.9, 24: 11.5, 30: 12.7, 36: 13.9, 42: 15.1, 48: 16.3, 54: 17.5, 60: 18.7},
    'z_plus_2': {0: 4.2, 1: 5.5, 2: 6.6, 3: 7.5, 4: 8.2, 5: 8.8, 6: 9.3, 7: 9.8, 8: 10.2, 9: 10.5, 10: 10.9, 11: 11.2, 12: 11.5, 15: 12.4, 18: 13.2, 21: 14.1, 24: 14.8, 30: 16.5, 36: 18.1, 42: 19.8, 48: 21.5, 54: 23.1, 60: 24.8},
    'z_plus_3': {0: 4.8, 1: 6.2, 2: 7.5, 3: 8.5, 4: 9.3, 5: 10.0, 6: 10.6, 7: 11.1, 8: 11.6, 9: 12.0, 10: 12.4, 11: 12.8, 12: 13.1, 15: 14.1, 18: 15.1, 21: 16.1, 24: 17.1, 30: 19.0, 36: 20.9, 42: 22.9, 48: 24.9, 54: 26.9, 60: 28.8}
}

# Inicializar os dados no session_state
if 'measurements' not in st.session_state:
    # Dados de exemplo
    st.session_state.measurements = [
        {'idade_meses': 0, 'peso_kg': 2.37, 'data': '2025-05-11'},
        {'idade_meses': 1, 'peso_kg': 3.29, 'data': '2025-06-11'},
        {'idade_meses': 2, 'peso_kg': 3.95, 'data': '2025-07-11'},
        {'idade_meses': 3, 'peso_kg': 4.52, 'data': '2025-08-11'},
        {'idade_meses': 4, 'peso_kg': 4.93, 'data': '2025-09-11'},
        {'idade_meses': 5, 'peso_kg': 5.33, 'data': '2025-10-11'},
        {'idade_meses': 6, 'peso_kg': 5.61, 'data': '2025-11-11'}
    ]

# Layout em colunas
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("➕ Adicionar Nova Medição")

    with st.form("add_measurement"):
        idade = st.number_input("Idade (meses)", min_value=0, max_value=60, value=7, step=1)
        peso = st.number_input("Peso (kg)", min_value=0.0, max_value=40.0, value=5.8, step=0.1, format="%.2f")
        data_medicao = st.date_input("Data da medição", value=date.today())

        submitted = st.form_submit_button("Adicionar Medição")

        if submitted:
            st.session_state.measurements.append({
                'idade_meses': idade,
                'peso_kg': peso,
                'data': data_medicao.strftime('%Y-%m-%d')
            })
            st.success(f"Medição adicionada: {idade} meses, {peso} kg")

    st.subheader("📋 Medições Registradas")

    if st.session_state.measurements:
        df = pd.DataFrame(st.session_state.measurements)
        df = df.sort_values('idade_meses')
        st.dataframe(df, width='stretch')

        # Opção para remover última medição
        if st.button("🗑️ Remover Última Medição"):
            if st.session_state.measurements:
                st.session_state.measurements.pop()
                st.rerun()

        # Download dos dados
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar dados (CSV)",
            data=csv,
            file_name="peso_crianca.csv",
            mime="text/csv"
        )

with col1:
    st.subheader("📈 Gráfico de Crescimento")

    # Criar o gráfico
    fig = go.Figure()

    # Adicionar curvas de referência OMS
    for z_score, data_dict in who_data.items():
        ages = sorted(data_dict.keys())
        weights = [data_dict[age] for age in ages]

        # Mapear nomes das curvas
        z_names = {
            'z_minus_3': 'Z = -3',
            'z_minus_2': 'Z = -2',
            'z_0': 'Z = 0 (mediana)',
            'z_plus_2': 'Z = +2',
            'z_plus_3': 'Z = +3'
        }

        # Cores para cada curva
        colors = {
            'z_minus_3': 'red',
            'z_minus_2': 'orange',
            'z_0': 'green',
            'z_plus_2': 'orange',
            'z_plus_3': 'red'
        }

        fig.add_trace(go.Scatter(
            x=ages,
            y=weights,
            mode='lines',
            name=z_names[z_score],
            line=dict(color=colors[z_score], width=2, dash='solid' if z_score == 'z_0' else 'dash'),
            opacity=0.7
        ))

    # Adicionar os dados da criança
    if st.session_state.measurements:
        df = pd.DataFrame(st.session_state.measurements)
        df = df.sort_values('idade_meses')

        fig.add_trace(go.Scatter(
            x=df['idade_meses'],
            y=df['peso_kg'],
            mode='lines+markers',
            name='Sua filha',
            line=dict(color='blue', width=3),
            marker=dict(size=10, color='blue', symbol='circle')
        ))

    # Configurar layout
    fig.update_layout(
        title="Peso para Idade - Meninas (0-60 meses)",
        xaxis_title="Idade (meses)",
        yaxis_title="Peso (kg)",
        hovermode='x unified',
        height=600,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        xaxis=dict(range=[0, 60], dtick=6),
        yaxis=dict(range=[0, 30])
    )

    st.plotly_chart(fig, use_container_width=True)

    # Legenda
    st.info("""
    **Interpretação dos Z-scores (OMS):**
    - **Z < -3**: Muito baixo peso
    - **-3 ≤ Z < -2**: Baixo peso
    - **-2 ≤ Z < +2**: Peso adequado
    - **Z ≥ +2**: Peso elevado
    """)

# Rodapé
st.markdown("---")
st.markdown("*Dados baseados nos padrões WHO Child Growth Standards (OMS, 2006)*")
