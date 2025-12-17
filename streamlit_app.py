# -*- coding: utf-8 -*-
"""
Dashboard de Estabilidade - Indovinya
Interface moderna para análise de produtos
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

# ============================================================
# CONFIGURACAO DA PAGINA
# ============================================================

st.set_page_config(
    page_title="Estabilidade Indovinya",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado - Design Indorama Ventures
st.markdown("""
<style>
    /* Reset e base - Cores Indorama */
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #0d2137 50%, #0f2847 100%);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d2137 0%, #0a1628 100%);
        border-right: 1px solid rgba(0, 163, 224, 0.2);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }

    /* Headers */
    h1, h2, h3 {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    /* Main title styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #003366 0%, #0055a4 50%, #00a3e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }

    /* Header container with logo */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0;
        margin-bottom: 1rem;
        border-bottom: 2px solid rgba(0, 163, 224, 0.3);
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }

    .header-title-section {
        display: flex;
        flex-direction: column;
    }

    /* Metric cards */
    .metric-container {
        background: linear-gradient(135deg, rgba(0, 51, 102, 0.2) 0%, rgba(0, 85, 164, 0.15) 100%);
        border: 1px solid rgba(0, 163, 224, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .metric-container:hover {
        border-color: rgba(0, 163, 224, 0.6);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 163, 224, 0.2);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0055a4 0%, #00a3e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }

    .metric-delta {
        color: #00a651;
        font-size: 0.85rem;
        margin-top: 0.25rem;
    }

    .metric-delta.negative {
        color: #c8102e;
    }

    /* Cards de info */
    .info-card {
        background: rgba(0, 51, 102, 0.3);
        border: 1px solid rgba(0, 163, 224, 0.15);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
    }

    .info-label {
        color: #64748b;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }

    .info-value {
        color: #e2e8f0;
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(0, 51, 102, 0.3);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(0, 163, 224, 0.15);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #94a3b8;
        padding: 12px 24px;
        font-weight: 500;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #003366 0%, #0055a4 100%);
        color: white !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #e2e8f0;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(0, 51, 102, 0.4);
        border: 1px solid rgba(0, 163, 224, 0.2);
        border-radius: 10px;
        color: #e2e8f0;
    }

    .stSelectbox > div > div:hover {
        border-color: rgba(0, 163, 224, 0.5);
    }

    /* Radio buttons */
    .stRadio > div {
        background: rgba(0, 51, 102, 0.3);
        padding: 0.75rem 1rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 163, 224, 0.15);
    }

    .stRadio label {
        color: #e2e8f0 !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        background: rgba(0, 51, 102, 0.3);
        border-radius: 12px;
        border: 1px solid rgba(0, 163, 224, 0.15);
    }

    /* Alert/Info boxes */
    .stAlert {
        background: rgba(0, 85, 164, 0.15);
        border: 1px solid rgba(0, 163, 224, 0.3);
        border-radius: 10px;
        color: #e2e8f0;
    }

    /* Divider */
    hr {
        border-color: rgba(0, 163, 224, 0.15);
        margin: 2rem 0;
    }

    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(0, 163, 224, 0.2);
    }

    .section-icon {
        font-size: 1.5rem;
    }

    .section-title {
        color: #f1f5f9;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
    }

    /* Status badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .badge-success {
        background: rgba(0, 166, 81, 0.2);
        color: #00a651;
        border: 1px solid rgba(0, 166, 81, 0.3);
    }

    .badge-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .badge-danger {
        background: rgba(200, 16, 46, 0.2);
        color: #c8102e;
        border: 1px solid rgba(200, 16, 46, 0.3);
    }

    /* Plotly chart container */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(0, 51, 102, 0.3);
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(0, 163, 224, 0.5);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 163, 224, 0.7);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Product info card */
    .product-info {
        background: linear-gradient(135deg, rgba(0, 51, 102, 0.15) 0%, rgba(0, 85, 164, 0.1) 100%);
        border: 1px solid rgba(0, 163, 224, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }

    .product-name {
        color: #f1f5f9;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }

    /* Ensaio selector card */
    .ensaio-card {
        background: rgba(0, 51, 102, 0.35);
        border: 1px solid rgba(0, 163, 224, 0.2);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    /* Spec info */
    .spec-info {
        background: linear-gradient(135deg, rgba(0, 166, 81, 0.1) 0%, rgba(0, 163, 224, 0.1) 100%);
        border: 1px solid rgba(0, 166, 81, 0.2);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        color: #00a651;
        font-weight: 500;
    }

    /* Footer styling */
    .footer-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        padding: 2rem 0;
        border-top: 1px solid rgba(0, 163, 224, 0.2);
        margin-top: 2rem;
    }

    .footer-text {
        color: #64748b;
        font-size: 0.85rem;
        text-align: center;
    }

    /* Sidebar logo container */
    .sidebar-logo {
        display: flex;
        justify-content: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(0, 163, 224, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CARREGAR DADOS
# ============================================================

@st.cache_data
def carregar_dados():
    """Carrega os dados tratados"""
    # Usa caminho relativo para funcionar no Streamlit Cloud
    base_path = Path(__file__).parent
    df_long = pd.read_excel(base_path / "dados_long.xlsx")
    df_acelerado = pd.read_excel(base_path / "dados_acelerado.xlsx")
    df_longa = pd.read_excel(base_path / "dados_longa_duracao.xlsx")
    return df_long, df_acelerado, df_longa

df_long, df_acelerado, df_longa = carregar_dados()

ORDEM_PERIODOS = {
    '0 dia': 0, '1 sem': 7, '2 sem': 14,
    '1m': 30, '2m': 60, '3m': 90, '4m': 120, '5m': 150, '6m': 180,
    '9m': 270, '12m': 365, '18m': 545, '24m': 730, '30m': 912, '36m': 1095
}

# Cores do tema - Baseado na identidade visual Indorama Ventures
COLORS = {
    'primary': '#003366',      # Azul Indorama escuro
    'secondary': '#0055a4',    # Azul Indorama médio
    'accent': '#00a3e0',       # Azul Dobslit/Accent
    'success': '#00a651',      # Verde Indorama
    'warning': '#f59e0b',      # Amarelo alerta
    'danger': '#c8102e',       # Vermelho Indorama
    'bg_dark': '#0a1628',      # Fundo escuro azulado
    'bg_card': 'rgba(0, 51, 102, 0.3)',
    'text': '#e2e8f0',
    'text_muted': '#94a3b8',
    'border': 'rgba(0, 163, 224, 0.2)'
}

# ============================================================
# HEADER
# ============================================================

# Header com logo Indorama
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("Indorama_Ventures_Logo.png", width=180)
with col_title:
    st.markdown('<h1 class="main-title">Dashboard de Estabilidade</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Indovinya - Especialidades Quimicas</p>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    # Logo Dobslit no topo da sidebar
    st.image("LOGOMARCA_DOBSLIT.PNG", width=150)
    st.markdown("---")
    st.markdown("### Filtros")

    # Tipo de estudo com visual melhorado
    tipo_estudo = st.radio(
        "**Tipo de Estudo**",
        ["Acelerado", "Longa Duração"],
        horizontal=True,
        key="tipo_estudo"
    )

    if tipo_estudo == "Acelerado":
        df = df_acelerado.copy()
        emoji_tipo = "⚡"
    else:
        df = df_longa.copy()
        emoji_tipo = "📅"

    st.markdown("---")

    # Produto
    produtos = sorted(df['Nome do produto'].unique())
    produto_selecionado = st.selectbox(
        "**🏭 Selecione o Produto**",
        produtos,
        index=0
    )

    df_produto = df[df['Nome do produto'] == produto_selecionado].copy()

    # Info do produto
    st.markdown("---")
    st.markdown("### 📋 Informações")

    if len(df_produto) > 0:
        info = df_produto.iloc[0]

        info_items = [
            ("Descrição", info.get('Descrição química')),
            ("Família", info.get('Família de Produtos')),
            ("Etoxilação", info.get('Grau de Etoxilação')),
            ("Início", info.get('Data inicial do estudo'))
        ]

        for label, value in info_items:
            if pd.notna(value) and str(value).strip():
                st.markdown(f"""
                <div class="info-card">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# METRICAS
# ============================================================

# Calcular conformidade
def calcular_conformidade(row):
    try:
        valor = float(row['valor'])
        spec_tipo = row['spec_tipo']
        spec_min = row['spec_min']
        spec_max = row['spec_max']

        if spec_tipo == 'RANGE' and pd.notna(spec_min) and pd.notna(spec_max):
            return spec_min <= valor <= spec_max
        elif spec_tipo == 'MAXIMO' and pd.notna(spec_max):
            return valor <= spec_max
        elif spec_tipo == 'MINIMO' and pd.notna(spec_min):
            return valor >= spec_min
        return None
    except:
        return None

df_produto['conforme'] = df_produto.apply(calcular_conformidade, axis=1)
total_ensaios = df_produto['ensaio_normalizado'].nunique()
total_periodos = df_produto['periodo'].nunique()
conformes = df_produto['conforme'].sum()
total_verificaveis = df_produto['conforme'].notna().sum()
pct_conforme = (conformes / total_verificaveis * 100) if total_verificaveis > 0 else 0
alertas = int(total_verificaveis - conformes)

# Métricas em cards
col1, col2, col3, col4 = st.columns(4)

metrics = [
    (col1, "📊", total_ensaios, "Ensaios", None),
    (col2, "📅", total_periodos, "Períodos", None),
    (col3, "✅", f"{pct_conforme:.0f}%", "Conformidade", f"{int(conformes)}/{int(total_verificaveis)}"),
    (col4, "⚠️", alertas, "Alertas", "fora da spec" if alertas > 0 else "tudo OK")
]

for col, icon, value, label, delta in metrics:
    with col:
        delta_class = "negative" if label == "Alertas" and alertas > 0 else ""
        delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>' if delta else ""
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{icon} {value}</div>
            <div class="metric-label">{label}</div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ABAS POR CATEGORIA
# ============================================================

categorias = df_produto['categoria_ensaio'].unique().tolist()

if len(categorias) > 0:
    tabs = st.tabs([f"📁 {cat}" for cat in categorias])

    for i, categoria in enumerate(categorias):
        with tabs[i]:
            df_cat = df_produto[df_produto['categoria_ensaio'] == categoria].copy()
            ensaios_disponiveis = sorted(df_cat['ensaio_normalizado'].unique())

            col_select, col_spacer, col_info = st.columns([2, 0.5, 2.5])

            with col_select:
                st.markdown('<div class="ensaio-card">', unsafe_allow_html=True)
                ensaio_selecionado = st.selectbox(
                    "🔬 Selecione o Ensaio",
                    ensaios_disponiveis,
                    key=f"ensaio_{categoria}_{i}"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            df_ensaio = df_cat[df_cat['ensaio_normalizado'] == ensaio_selecionado].copy()

            with col_info:
                if len(df_ensaio) > 0:
                    spec_tipo = df_ensaio['spec_tipo'].iloc[0]
                    spec_min = df_ensaio['spec_min'].iloc[0]
                    spec_max = df_ensaio['spec_max'].iloc[0]

                    if spec_tipo == 'RANGE' and pd.notna(spec_min) and pd.notna(spec_max):
                        spec_text = f"📏 Faixa: {spec_min} — {spec_max}"
                    elif spec_tipo == 'MAXIMO' and pd.notna(spec_max):
                        spec_text = f"📏 Máximo: {spec_max}"
                    elif spec_tipo == 'MINIMO' and pd.notna(spec_min):
                        spec_text = f"📏 Mínimo: {spec_min}"
                    else:
                        spec_text = "📏 Qualitativo"

                    st.markdown(f'<div class="spec-info">{spec_text}</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Layout principal
            col_grafico, col_dados = st.columns([3, 2])

            with col_grafico:
                is_quant = df_ensaio['is_quantitativo'].iloc[0] if len(df_ensaio) > 0 else True

                if is_quant:
                    df_ensaio['valor_num'] = pd.to_numeric(df_ensaio['valor'], errors='coerce')
                    df_plot = df_ensaio.dropna(subset=['valor_num']).copy()

                    if len(df_plot) > 0:
                        df_plot['ordem'] = df_plot['periodo'].map(ORDEM_PERIODOS)
                        df_plot = df_plot.sort_values('ordem')

                        fig = go.Figure()

                        # Área de especificação
                        spec_tipo = df_plot['spec_tipo'].iloc[0]
                        spec_min = df_plot['spec_min'].iloc[0]
                        spec_max = df_plot['spec_max'].iloc[0]
                        x_vals = df_plot['periodo'].tolist()

                        if spec_tipo == 'RANGE' and pd.notna(spec_min) and pd.notna(spec_max):
                            fig.add_trace(go.Scatter(
                                x=x_vals + x_vals[::-1],
                                y=[spec_max]*len(x_vals) + [spec_min]*len(x_vals),
                                fill='toself',
                                fillcolor='rgba(16, 185, 129, 0.15)',
                                line=dict(color='rgba(16, 185, 129, 0)'),
                                name='Faixa OK',
                                showlegend=True,
                                hoverinfo='skip'
                            ))
                            fig.add_hline(y=spec_max, line_dash="dash", line_color="#10b981", line_width=1)
                            fig.add_hline(y=spec_min, line_dash="dash", line_color="#10b981", line_width=1)

                        elif spec_tipo == 'MAXIMO' and pd.notna(spec_max):
                            fig.add_hline(y=spec_max, line_dash="dash", line_color="#ef4444", line_width=2,
                                         annotation_text=f"Máx: {spec_max}", annotation_position="top right")

                        elif spec_tipo == 'MINIMO' and pd.notna(spec_min):
                            fig.add_hline(y=spec_min, line_dash="dash", line_color="#ef4444", line_width=2,
                                         annotation_text=f"Mín: {spec_min}", annotation_position="bottom right")

                        # Linha dos valores
                        fig.add_trace(go.Scatter(
                            x=df_plot['periodo'],
                            y=df_plot['valor_num'],
                            mode='lines+markers',
                            name='Valor Medido',
                            line=dict(color='#00a3e0', width=3),
                            marker=dict(size=12, symbol='circle', color='#0055a4',
                                       line=dict(color='#ffffff', width=2)),
                            hovertemplate='<b>%{x}</b><br>Valor: %{y:.2f}<extra></extra>'
                        ))

                        fig.update_layout(
                            title=dict(
                                text=f"<b>Evolução Temporal - {ensaio_selecionado}</b>",
                                font=dict(size=16, color='#f1f5f9')
                            ),
                            xaxis=dict(
                                title=dict(text="Período", font=dict(color='#94a3b8')),
                                gridcolor='rgba(148, 163, 184, 0.1)',
                                tickfont=dict(color='#94a3b8')
                            ),
                            yaxis=dict(
                                title=dict(text="Valor", font=dict(color='#94a3b8')),
                                gridcolor='rgba(148, 163, 184, 0.1)',
                                tickfont=dict(color='#94a3b8')
                            ),
                            plot_bgcolor='rgba(15, 15, 26, 0.8)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            height=400,
                            margin=dict(l=60, r=30, t=60, b=60),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1,
                                font=dict(color='#94a3b8')
                            ),
                            hovermode='x unified'
                        )

                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Sem dados numéricos para este ensaio.")
                else:
                    st.markdown("#### 📋 Evolução Qualitativa")
                    df_ensaio['ordem'] = df_ensaio['periodo'].map(ORDEM_PERIODOS)
                    df_ensaio = df_ensaio.sort_values('ordem')
                    for _, row in df_ensaio.iterrows():
                        st.markdown(f"**{row['periodo']}:** `{row['valor']}`")

            with col_dados:
                st.markdown("#### 📊 Dados")

                df_ensaio['ordem'] = df_ensaio['periodo'].map(ORDEM_PERIODOS)
                df_tabela = df_ensaio.sort_values('ordem')[['periodo', 'valor', 'conforme']].copy()

                def format_status(val):
                    if val == True:
                        return "✅"
                    elif val == False:
                        return "❌"
                    return "➖"

                df_tabela['Status'] = df_tabela['conforme'].apply(format_status)
                df_tabela = df_tabela.rename(columns={'periodo': 'Período', 'valor': 'Valor'})

                st.dataframe(
                    df_tabela[['Período', 'Valor', 'Status']],
                    hide_index=True,
                    use_container_width=True,
                    height=300
                )

                # Métricas do ensaio
                if is_quant and 'valor_num' in df_ensaio.columns and len(df_ensaio.dropna(subset=['valor_num'])) > 0:
                    st.markdown("#### 📈 Métricas")

                    df_calc = df_ensaio.dropna(subset=['valor_num']).sort_values('ordem')
                    valor_t0 = df_calc[df_calc['periodo'] == '0 dia']['valor_num'].values
                    valor_atual = df_calc['valor_num'].iloc[-1] if len(df_calc) > 0 else None

                    if len(valor_t0) > 0 and valor_atual is not None and valor_t0[0] != 0:
                        var_pct = ((valor_atual - valor_t0[0]) / valor_t0[0]) * 100

                        col_m1, col_m2 = st.columns(2)
                        with col_m1:
                            st.metric("Valor T0", f"{valor_t0[0]:.2f}")
                        with col_m2:
                            st.metric("Variação", f"{var_pct:+.1f}%",
                                     delta_color="inverse" if var_pct > 10 else "normal")

                    if len(df_calc) >= 3:
                        valores = df_calc['valor_num'].values
                        if valores[-1] > valores[0] * 1.05:
                            tendencia = "📈 Tendência de alta"
                            cor = "warning"
                        elif valores[-1] < valores[0] * 0.95:
                            tendencia = "📉 Tendência de queda"
                            cor = "warning"
                        else:
                            tendencia = "➡️ Estável"
                            cor = "success"

                        badge_class = f"badge badge-{cor}"
                        st.markdown(f'<span class="{badge_class}">{tendencia}</span>', unsafe_allow_html=True)

# ============================================================
# HEATMAP
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <span class="section-icon">🔥</span>
    <h3 class="section-title">Heatmap de Conformidade</h3>
</div>
""", unsafe_allow_html=True)

df_quant = df_produto[df_produto['is_quantitativo'] == True].copy()

if len(df_quant) > 0:
    df_quant['conforme_num'] = df_quant['conforme'].map({True: 1, False: 0, None: 0.5})

    pivot = df_quant.pivot_table(
        index='ensaio_normalizado',
        columns='periodo',
        values='conforme_num',
        aggfunc='mean'
    )

    cols_ordenadas = sorted(pivot.columns, key=lambda x: ORDEM_PERIODOS.get(x, 999))
    pivot = pivot[cols_ordenadas]

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=[
            [0, '#c8102e'],
            [0.5, '#0055a4'],
            [1, '#00a651']
        ],
        showscale=True,
        colorbar=dict(
            title=dict(text="Status", font=dict(color='#94a3b8')),
            tickvals=[0, 0.5, 1],
            ticktext=['Fora', 'N/A', 'OK'],
            tickfont=dict(color='#94a3b8'),
            bgcolor='rgba(0,0,0,0)'
        ),
        hovertemplate='<b>%{y}</b><br>Período: %{x}<br>Status: %{z:.0%}<extra></extra>'
    ))

    fig_heat.update_layout(
        xaxis=dict(
            title=dict(text="Período", font=dict(color='#94a3b8')),
            tickfont=dict(color='#94a3b8')
        ),
        yaxis=dict(
            title=dict(text="Ensaio", font=dict(color='#94a3b8')),
            tickfont=dict(color='#94a3b8', size=10)
        ),
        plot_bgcolor='rgba(15, 15, 26, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=max(400, len(pivot) * 28),
        margin=dict(l=200, r=50, t=30, b=60)
    )

    st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.info("Sem dados quantitativos para exibir o heatmap.")

# ============================================================
# FOOTER
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

# Footer com logos e texto
col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
with col_f1:
    st.image("Indorama_Ventures_Logo.png", width=120)
with col_f2:
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 1rem 0;">
        <strong>Dashboard de Estabilidade</strong><br>
        Indovinya - Especialidades Quimicas<br>
        <span style="color: #00a3e0;">Desenvolvido por Dobslit</span>
    </div>
    """, unsafe_allow_html=True)
with col_f3:
    st.image("LOGOMARCA_DOBSLIT.PNG", width=100)
