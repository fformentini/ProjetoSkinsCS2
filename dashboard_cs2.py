import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CS2 Skins · Trading Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"], [data-testid="stAppViewContainer"],
[data-testid="stSidebar"], button, input, select, textarea {
    font-family: 'Inter', 'Segoe UI Variable', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}
[data-testid="stAppViewContainer"] { background: #0a0a0a; }
[data-testid="stSidebar"]          { background: #111111; border-right: 1px solid #1e1e1e; }
[data-testid="stHeader"]           { background: transparent; }
h1,h2,h3,h4 { color:#f0f0f0; font-family:'Inter','Segoe UI Variable','Segoe UI',system-ui,sans-serif !important; }
p,span,div,label { color:#b0b0b0; }

.kpi-card {
    background:#141414; border:1px solid #222; border-radius:10px;
    padding:20px 24px; margin-bottom:8px;
}
.kpi-label { font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:#555; margin-bottom:6px; }
.kpi-value { font-size:28px; font-weight:700; color:#f0f0f0; }
.kpi-value.green  { color:#00e676; }
.kpi-value.red    { color:#ff5252; }
.kpi-value.blue   { color:#40c4ff; }
.kpi-value.yellow { color:#ffd740; }
.kpi-value.orange { color:#ff8a65; }
.kpi-delta { font-size:12px;font-weight: 800; margin-top:4px; color:#444; }

.section-title {
    font-size:11px; text-transform:uppercase; letter-spacing:2px;
    color:#444; padding:20px 0 8px; border-bottom:1px solid #1e1e1e; margin-bottom:16px;
}

/* Hero card – melhor skin */
.hero-card {
    background: linear-gradient(135deg,#0d1a0d 0%,#0a0a0a 60%,#001a1a 100%);
    border:1px solid #1a3a1a; border-radius:14px; padding:28px 32px; margin-bottom:16px;
    position:relative; overflow:hidden;
}
.hero-card::before {
    content:''; position:absolute; top:-40px; right:-40px;
    width:200px; height:200px; border-radius:50%;
    background:radial-gradient(circle,rgba(0,230,118,0.06) 0%,transparent 70%);
}
.hero-tag { font-size:10px; text-transform:uppercase; letter-spacing:2px;
    color:#00e676; margin-bottom:10px; }
.hero-title { font-size:26px; font-weight:800; color:#f0f0f0; margin-bottom:4px; }
.hero-sub   { font-size:13px; color:#555; margin-bottom:20px; }
.hero-stats { display:flex; gap:32px; flex-wrap:wrap; }
.hero-stat-label { font-size:10px; text-transform:uppercase; letter-spacing:1px; color:#444; margin-bottom:4px; }
.hero-stat-value { font-size:20px; font-weight:700; color:#00e676; }
.hero-stat-value.blue { color:#40c4ff; }
.hero-stat-value.yellow { color:#ffd740; }

/* ── ABOUT HERO ────────────────────────────────────────── */
.about-hero {
    background: linear-gradient(135deg, #0e0e0e 0%, #0a0a0a 50%, #080f14 100%);
    border: 1px solid #1c1c1c;
    border-radius: 16px;
    padding: 48px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.about-hero::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle, rgba(64,196,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.about-hero::after {
    content: '';
    position: absolute; bottom: -40px; left: 30%;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,230,118,0.04) 0%, transparent 70%);
    pointer-events: none;
}
.about-eyebrow {
    font-size: 10px; text-transform: uppercase; letter-spacing: 3px;
    color: #40c4ff; margin-bottom: 14px;
    display: flex; align-items: center; justify-content: center; gap: 8px;
}
.about-eyebrow::before { content:''; display:inline-block; width:24px; height:1px; background:#40c4ff; }
.about-eyebrow::after  { content:''; display:inline-block; width:24px; height:1px; background:#40c4ff; }
.about-title {
    font-size: 36px; font-weight: 900; color: #f0f0f0;
    letter-spacing: -1px; line-height: 1.15; margin-bottom: 14px;
}
.about-title span { color: #40c4ff; }
.about-desc {
    font-size: 14px; color: #555; line-height: 1.75;
    max-width: 620px; margin: 0 auto 32px auto;
}
.about-pills {
    display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 32px;
    justify-content: center;
}
.pill {
    background: #141414; border: 1px solid #222; border-radius: 999px;
    padding: 5px 14px; font-size: 11px; color: #666; letter-spacing: 0.5px;
}
.about-divider {
    height: 1px; background: #1a1a1a; margin-bottom: 28px;
}
.about-meta {
    display: flex; gap: 40px; flex-wrap: wrap;
    justify-content: center;
}
.about-meta-item { text-align: center; }
.about-meta-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #333; margin-bottom: 5px; }
.about-meta-value { font-size: 18px; font-weight: 700; }
.about-meta-value.green  { color: #00e676; }
.about-meta-value.blue   { color: #40c4ff; }
.about-meta-value.yellow { color: #ffd740; }
.about-meta-value.gray   { color: #888; }

/* Loss alert card */
.loss-card {
    background:#140a0a; border:1px solid #3a1a1a; border-radius:10px;
    padding:18px 22px; margin-bottom:8px;
}
.loss-card-label { font-size:10px; text-transform:uppercase; letter-spacing:1.5px; color:#663333; margin-bottom:6px; }
.loss-card-value { font-size:24px; font-weight:700; color:#ff5252; }
.loss-card-delta { font-size:11px; font-weight:700; color:#442222; margin-top:4px; }

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color:#888 !important; font-size:12px; }
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel(
        "skinsCS2.xlsx",
        sheet_name="Controle de Skins", engine="openpyxl",
    )
    df = df[["Nome da Skin", "Categoria", "Preço de Compra (R$)", "Preço de Venda Bruto (R$)",
             "Taxa (6%)", "Receita Líquida (R$)", "Lucro (R$)", "ROI (%)"]]
    df.columns = ["Nome", "Categoria", "Compra", "Venda_Bruta", "Taxa", "Receita_Liq", "Lucro", "ROI"]
    df = df[df["Nome"].notna() & df["Compra"].notna() & (df["Compra"] != 0) & df["Categoria"].notna()]
    for col in ["Lucro", "ROI", "Compra", "Venda_Bruta", "Receita_Liq", "Taxa"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df["Win"] = df["Lucro"] > 0
    df["Trade_ID"] = range(1, len(df) + 1)
    return df


df = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 Filtros")
    st.markdown("---")
    cat_sel = st.selectbox("Categoria", ["Todas"] + sorted(df["Categoria"].unique().tolist()))
    resultado = st.selectbox("Resultado", ["Todos", "✅ Lucro", "❌ Prejuízo"])
    roi_min, roi_max = float(df["ROI"].min()), float(df["ROI"].max())
    roi_range = st.slider("ROI (%)", roi_min, roi_max, (roi_min, roi_max), step=1.0)
    st.markdown("---")
    st.markdown("<div style='color:#333;font-size:11px;'>CS2 Trading · Fabricio</div>", unsafe_allow_html=True)

# ── FILTER ────────────────────────────────────────────────────────────────────
fdf = df.copy()
if cat_sel != "Todas":        fdf = fdf[fdf["Categoria"] == cat_sel]
if resultado == "✅ Lucro":
    fdf = fdf[fdf["Lucro"] > 0]
elif resultado == "❌ Prejuízo":
    fdf = fdf[fdf["Lucro"] < 0]
fdf = fdf[(fdf["ROI"] >= roi_range[0]) & (fdf["ROI"] <= roi_range[1])]

# ── FLAGS DE VISIBILIDADE (conforme filtro de Resultado) ───────────────────────
show_lucro = resultado != "❌ Prejuízo"  # esconde blocos de lucro quando filtro = Prejuízo
show_prejuizo = resultado != "✅ Lucro"  # esconde blocos de prejuízo quando filtro = Lucro

# ── DERIVED GLOBALS (usando df completo para análise de prejuízo) ──────────
prej_df = df[df["Lucro"] < 0]
total_prej = prej_df["Lucro"].sum()
n_prej = len(prej_df)
pior_trade = prej_df.loc[prej_df["Lucro"].idxmin()] if n_prej else None
pior_roi_tr = prej_df.loc[prej_df["ROI"].idxmin()] if n_prej else None

# melhor skin por lucro agregado
skin_rank = (
    df.groupby("Nome")
    .agg(Lucro_Total=("Lucro", "sum"), Trades=("Lucro", "count"),
         ROI_Med=("ROI", "mean"), Compra_Total=("Compra", "sum"))
    .reset_index()
    .sort_values("Lucro_Total", ascending=False)
)
best_skin = skin_rank.iloc[0]
best_skin_trades = df[df["Nome"] == best_skin["Nome"]]

# ── PLOTLY BASE ───────────────────────────────────────────────────────────────
PLOT_BG = PAPER_BG = "#0d0d0d"
GRID = "#1a1a1a"
FONT = "#888"
ACCENT = "#40c4ff"
GREEN = "#00e676"
RED = "#ff5252"
YELLOW = "#ffd740"
ORANGE = "#ff8a65"
PALETTE = [ACCENT, GREEN, YELLOW, RED, "#b39ddb", ORANGE, "#80cbc4"]

base = dict(
    plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
    font=dict(color=FONT, family="Segoe UI"),
    xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=FONT)),
    yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=FONT)),
    margin=dict(l=16, r=16, t=40, b=16),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#666")),
)


def kpi(label, value, color="", delta=""):
    return f"<div class='kpi-card'><div class='kpi-label'>{label}</div><div class='kpi-value {color}'>{value}</div><div class='kpi-delta'>{delta}</div></div>"


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<h1 style='font-size:32px;font-weight:800;letter-spacing:-1px;margin-bottom:4px;text-align:center;'>
   CS2 Skins <span style='color:#40c4ff;'>Trading</span> Dashboard
</h1>
<p style='color:#333;font-size:13px;font-weight:600;margin-bottom:24px;text-align:center;'>Análise completa de performance · Lucros & Prejuízos</p>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO ABOUT — HERO
# ═══════════════════════════════════════════════════════════════════════════════
_total_trades_geral = len(df)
_lucro_geral = df["Lucro"].sum()
_roi_geral = df["ROI"].mean()
_categorias_n = df["Categoria"].nunique()
_lucro_color = "green" if _lucro_geral >= 0 else "red"
_lucro_fmt = f"R$ {_lucro_geral:+,.0f}".replace(",", ".")
_roi_fmt = f"{_roi_geral:+.1f}%"
_roi_color = "green" if _roi_geral >= 0 else "red"

st.markdown(f"""
<div class="about-hero">
  <div class="about-eyebrow">Sobre o projeto</div>
  <div class="about-title">
    Rastreador de <span>Trades</span> de Skins CS2
  </div>
  <div class="about-desc">
    Este dashboard foi construído para acompanhar e analisar operações de compra e venda
    de skins do Counter‑Strike 2. Cada trade é registrado com preço de compra,
    preço de venda, taxa da plataforma e lucro líquido — gerando métricas reais de
    performance como ROI, win rate e evolução de capital ao longo do tempo.<br><br>
    O objetivo é transformar dados brutos de trading em inteligência visual: identificar
    as categorias mais lucrativas, os padrões de acerto e erro, e acompanhar o crescimento
    do portfólio de forma objetiva.
  </div>
  <div class="about-pills">
    <span class="pill">📊 Streamlit + Plotly</span>
    <span class="pill">🐍 Python · Pandas</span>
    <span class="pill">📂 Excel como banco de dados</span>
    <span class="pill">💹 Análise de ROI</span>
    <span class="pill">🏷️ {_categorias_n} categorias de skins</span>
    <span class="pill">🔫 Counter‑Strike 2</span>
  </div>
  <div class="about-divider"></div>
  <div class="about-meta">
    <div class="about-meta-item">
      <div class="about-meta-label">Total de Trades</div>
      <div class="about-meta-value blue">{_total_trades_geral}</div>
    </div>
    <div class="about-meta-item">
      <div class="about-meta-label">Resultado Acumulado</div>
      <div class="about-meta-value {_lucro_color}">{_lucro_fmt}</div>
    </div>
    <div class="about-meta-item">
      <div class="about-meta-label">ROI Médio Geral</div>
      <div class="about-meta-value {_roi_color}">{_roi_fmt}</div>
    </div>
    <div class="about-meta-item">
      <div class="about-meta-label">Categorias</div>
      <div class="about-meta-value gray">{_categorias_n}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 0 — HERO: MELHOR SKIN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>⭐ Destaque · Skin Mais Lucrativa</div>", unsafe_allow_html=True)

col_hero, col_hero_chart = st.columns([2, 3])

with col_hero:
    roi_trades_str = " · ".join([f"R$ {r:,.0f}".replace(",", ".") for r in best_skin_trades["Lucro"]])
    st.markdown(f"""
    <div class='hero-card'>
        <div class='hero-tag'>🏆 Skin com maior lucro acumulado</div>
        <div class='hero-title'>{best_skin['Nome']}</div>
        <div class='hero-sub'>{int(best_skin['Trades'])} trades · {best_skin_trades['Categoria'].iloc[0]}</div>
        <div class='hero-stats'>
            <div>
                <div class='hero-stat-label'>Lucro Total</div>
                <div class='hero-stat-value'>R$ {best_skin['Lucro_Total']:,.0f}</div>
            </div>
            <div>
                <div class='hero-stat-label'>ROI Médio</div>
                <div class='hero-stat-value yellow'>{best_skin['ROI_Med']:.1f}%</div>
            </div>
            <div>
                <div class='hero-stat-label'>Investido Total</div>
                <div class='hero-stat-value blue'>R$ {best_skin['Compra_Total']:,.0f}</div>
            </div>
        </div>
        <div style='margin-top:18px;font-size:11px;color:#333;'>Lucros por trade: {roi_trades_str}</div>
    </div>
    """, unsafe_allow_html=True)

with col_hero_chart:
    bst = best_skin_trades.reset_index(drop=True)
    bst["Label"] = [f"Trade {i + 1}" for i in range(len(bst))]
    bst["Lucro_Acum"] = bst["Lucro"].cumsum()

    fig_hero = go.Figure()
    fig_hero.add_trace(go.Bar(
        x=bst["Label"], y=bst["Lucro"],
        name="Lucro por trade",
        marker_color=[GREEN if v >= 0 else RED for v in bst["Lucro"]],
        text=[f"R$ {v:,.0f}".replace(",", ".") for v in bst["Lucro"]],
        textposition="outside", textfont=dict(color="#ccc", size=11),
        hovertemplate="<b>%{x}</b><br>Lucro: R$ %{y:,.0f}<br>Compra: R$ " +
                      bst["Compra"].astype(str).str.replace(r"\.0", "", regex=True) + "<extra></extra>",
    ))
    fig_hero.add_trace(go.Scatter(
        x=bst["Label"], y=bst["Lucro_Acum"],
        name="Acumulado", mode="lines+markers",
        line=dict(color=GREEN, width=2, dash="dot"),
        marker=dict(size=6, color=GREEN),
        yaxis="y2",
        hovertemplate="Acumulado: R$ %{y:,.0f}<extra></extra>",
    ))
    fig_hero.update_layout(
        **base,
        title=dict(text=f"Performance dos {int(best_skin['Trades'])} trades · {best_skin['Nome']}",
                   font=dict(color="#ccc", size=13)),
        height=260,
        yaxis2=dict(overlaying="y", side="right", gridcolor=GRID,
                    tickfont=dict(color="#444"), showgrid=False),
        barmode="group",
    )
    st.plotly_chart(fig_hero, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 1 — KPIs GERAIS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Visão Geral · KPIs</div>", unsafe_allow_html=True)

total_lucro = fdf["Lucro"].sum()
total_investido = fdf["Compra"].sum()
roi_medio = (total_lucro / total_investido * 100) if total_investido else 0
total_trades = len(fdf)
win_rate = (fdf["Win"].sum() / total_trades * 100) if total_trades else 0
total_prej_fil = fdf[fdf["Lucro"] < 0]["Lucro"].sum()

kpi_cols_n = 4 + (1 if show_prejuizo else 0) + (1 if show_lucro else 0)
kpi_cols = st.columns(kpi_cols_n)
idx = 0
with kpi_cols[idx]: st.markdown(kpi("Lucro Líquido", f"R$ {total_lucro:,.0f}".replace(",", "."),
                                    "green" if total_lucro >= 0 else "red",
                                    f"de R$ {total_investido:,.0f} investidos".replace(",", ".")),
                                unsafe_allow_html=True)
idx += 1
with kpi_cols[idx]: st.markdown(kpi("ROI Médio", f"{roi_medio:.1f}%",
                                    "green" if roi_medio >= 0 else "red", "retorno sobre capital"),
                                unsafe_allow_html=True)
idx += 1
with kpi_cols[idx]: st.markdown(kpi("Total Trades", str(total_trades), "blue",
                                    f"{int(fdf['Win'].sum())} wins · {total_trades - int(fdf['Win'].sum())} losses"),
                                unsafe_allow_html=True)
idx += 1
with kpi_cols[idx]: st.markdown(kpi("Win Rate", f"{win_rate:.1f}%",
                                    "green" if win_rate >= 60 else ("yellow" if win_rate >= 50 else "red"),
                                    "% de trades positivos"), unsafe_allow_html=True)
idx += 1
if show_prejuizo:
    with kpi_cols[idx]: st.markdown(kpi("Total Prejuízo", f"R$ {total_prej_fil:,.0f}".replace(",", "."),
                                        "red", f"{len(fdf[fdf['Lucro'] < 0])} trades negativos"),
                                    unsafe_allow_html=True)
    idx += 1
if show_lucro:
    with kpi_cols[idx]:
        if len(fdf):
            best = fdf.loc[fdf["Lucro"].idxmax()]
            st.markdown(kpi("Melhor Trade", f"R$ {best['Lucro']:,.0f}".replace(",", "."),
                            "yellow", str(best["Nome"])[:20]), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 2 — PERFORMANCE POR CATEGORIA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Performance por Categoria</div>", unsafe_allow_html=True)
ca, cb = st.columns([3, 2])

with ca:
    cat_stats = (
        fdf.groupby("Categoria")
        .agg(Lucro=("Lucro", "sum"), Trades=("Lucro", "count"), ROI_med=("ROI", "mean"))
        .reset_index().sort_values("Lucro", ascending=True)
    )
    fig = go.Figure(go.Bar(
        x=cat_stats["Lucro"], y=cat_stats["Categoria"], orientation="h",
        marker_color=[GREEN if v >= 0 else RED for v in cat_stats["Lucro"]],
        text=[f"R$ {v:,.0f}".replace(",", ".") for v in cat_stats["Lucro"]],
        textposition="outside", textfont=dict(color="#ccc", size=11),
        hovertemplate="<b>%{y}</b><br>Lucro: R$ %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(**base, title=dict(text="Lucro Total por Categoria (R$)", font=dict(color="#ccc", size=13)),
                      height=300, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

with cb:
    if show_lucro:
        pie_data = fdf.groupby("Categoria")["Lucro"].sum().reset_index()
        pie_data = pie_data[pie_data["Lucro"] > 0]
        fig2 = go.Figure(go.Pie(
            labels=pie_data["Categoria"], values=pie_data["Lucro"], hole=0.55,
            marker=dict(colors=PALETTE, line=dict(color="#0d0d0d", width=2)),
            textfont=dict(color="#ccc", size=11),
            hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig2.update_layout(**base, title=dict(text="Participação no Lucro", font=dict(color="#ccc", size=13)),
                           height=300,
                           annotations=[
                               dict(text="Lucro", x=0.5, y=0.5, font_size=13, font_color="#555", showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem dados de lucro para exibir com o filtro atual.")

# ROI médio + Scatter
cc, cd = st.columns(2)

with cc:
    roi_cat = fdf.groupby("Categoria")["ROI"].mean().reset_index().sort_values("ROI", ascending=False)
    fig3 = go.Figure(go.Bar(
        x=roi_cat["Categoria"], y=roi_cat["ROI"],
        marker_color=[YELLOW if v >= 0 else RED for v in roi_cat["ROI"]],
        text=[f"{v:.1f}%" for v in roi_cat["ROI"]],
        textposition="outside", textfont=dict(color="#ccc", size=11),
        hovertemplate="<b>%{x}</b><br>ROI: %{y:.1f}%<extra></extra>",
    ))
    fig3.update_layout(**base, title=dict(text="ROI Médio por Categoria (%)", font=dict(color="#ccc", size=13)),
                       height=300, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig3, use_container_width=True)

with cd:
    fig4 = px.scatter(
        fdf, x="Compra", y="Lucro", color="Categoria",
        size=fdf["Lucro"].abs().clip(lower=5), hover_name="Nome",
        color_discrete_sequence=PALETTE,
        labels={"Compra": "Preço de Compra (R$)", "Lucro": "Lucro (R$)"},
    )
    fig4.add_hline(y=0, line_dash="dash", line_color="#2a2a2a")
    fig4.update_layout(**base, title=dict(text="Dispersão: Investimento × Lucro", font=dict(color="#ccc", size=13)),
                       height=300)
    st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 3 — EVOLUÇÃO & WIN RATE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Evolução & Win Rate</div>", unsafe_allow_html=True)
ce, cf = st.columns([3, 2])

with ce:
    fdf_s = fdf.copy().reset_index(drop=True)
    fdf_s["Lucro_Acum"] = fdf_s["Lucro"].cumsum()
    fdf_s["Cor"] = fdf_s["Lucro"].apply(lambda v: GREEN if v >= 0 else RED)

    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=fdf_s["Trade_ID"], y=fdf_s["Lucro_Acum"],
        mode="lines", line=dict(color=ACCENT, width=2),
        fill="tozeroy", fillcolor="rgba(64,196,255,0.06)",
        name="Acumulado",
        hovertemplate="Trade #%{x}<br>Acumulado: R$ %{y:,.0f}<extra></extra>",
    ))
    # Marcar os trades negativos com pontos vermelhos
    if show_prejuizo:
        prej_pts = fdf_s[fdf_s["Lucro"] < 0]
        fig5.add_trace(go.Scatter(
            x=prej_pts["Trade_ID"], y=prej_pts["Lucro_Acum"],
            mode="markers", marker=dict(color=RED, size=9, symbol="x"),
            name="Prejuízo",
            hovertemplate="Trade #%{x}<br>⚠️ Acumulado: R$ %{y:,.0f}<extra></extra>",
        ))
    fig5.add_hline(y=0, line_dash="dot", line_color="#222")
    fig5.update_layout(**base, title=dict(text="Curva de Lucro Acumulado · ✕ = Trades com Prejuízo",
                                          font=dict(color="#ccc", size=13)),
                       height=300, xaxis_title="Nº do Trade", yaxis_title=None)
    st.plotly_chart(fig5, use_container_width=True)

with cf:
    wr_cat = fdf.groupby("Categoria")["Lucro"].agg(
        Wins=lambda s: (s > 0).sum(),
        Losses=lambda s: (s <= 0).sum()
    ).reset_index()
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(name="Wins", x=wr_cat["Categoria"], y=wr_cat["Wins"], marker_color=GREEN))
    fig6.add_trace(go.Bar(name="Losses", x=wr_cat["Categoria"], y=wr_cat["Losses"], marker_color=RED))
    fig6.update_layout(**base, title=dict(text="Wins vs Losses por Categoria", font=dict(color="#ccc", size=13)),
                       barmode="group", height=300, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig6, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 4 — ANÁLISE DE PREJUÍZOS
# ═══════════════════════════════════════════════════════════════════════════════
if show_prejuizo:
    st.markdown("<div class='section-title'>🔴 Análise de Prejuízos</div>", unsafe_allow_html=True)

    # KPIs de prejuízo (sempre do df completo, não filtrado)
    pk1, pk2, pk3, pk4 = st.columns(4)

    prej_df_full = df[df["Lucro"] < 0]
    cat_mais_prej = prej_df_full.groupby("Categoria")["Lucro"].sum().idxmin() if len(prej_df_full) else "—"
    capital_em_risco = prej_df_full["Compra"].sum()

    with pk1:
        st.markdown(f"""<div class='loss-card'>
            <div class='loss-card-label'>Total de Prejuízo</div>
            <div class='loss-card-value'>R$ {total_prej:,.0f}</div>
            <div class='loss-card-delta'>sobre toda a carteira</div>
        </div>""", unsafe_allow_html=True)
    with pk2:
        st.markdown(f"""<div class='loss-card'>
            <div class='loss-card-label'>Trades Negativos</div>
            <div class='loss-card-value'>{n_prej}</div>
            <div class='loss-card-delta'>{n_prej / len(df) * 100:.1f}% do total de trades</div>
        </div>""", unsafe_allow_html=True)
    with pk3:
        if pior_trade is not None:
            st.markdown(f"""<div class='loss-card'>
                <div class='loss-card-label'>Pior Trade (R$)</div>
                <div class='loss-card-value'>R$ {pior_trade['Lucro']:,.0f}</div>
                <div class='loss-card-delta'>{str(pior_trade['Nome'])[:22]}</div>
            </div>""", unsafe_allow_html=True)
    with pk4:
        if pior_roi_tr is not None:
            st.markdown(f"""<div class='loss-card'>
                <div class='loss-card-label'>Pior ROI</div>
                <div class='loss-card-value'>{pior_roi_tr['ROI']:.1f}%</div>
                <div class='loss-card-delta'>{str(pior_roi_tr['Nome'])[:22]}</div>
            </div>""", unsafe_allow_html=True)

    # Gráficos de prejuízo
    pg1, pg2, pg3 = st.columns(3)

    with pg1:
        # Barras horizontais dos trades negativos
        prej_sorted = prej_df_full.sort_values("Lucro")
        fig_p1 = go.Figure(go.Bar(
            x=prej_sorted["Lucro"],
            y=prej_sorted["Nome"].str[:22],
            orientation="h",
            marker=dict(
                color=prej_sorted["Lucro"],
                colorscale=[[0, "#ff1744"], [1, "#ff7043"]],
                showscale=False,
            ),
            text=[f"ROI: {v:.1f}%" for v in prej_sorted["ROI"]],
            textposition="outside",
            textfont=dict(color="#cc4444", size=10),
            hovertemplate="<b>%{y}</b><br>Prejuízo: R$ %{x:,.0f}<extra></extra>",
        ))
        fig_p1.update_layout(**base, title=dict(text="Trades com Prejuízo (R$)", font=dict(color="#ccc", size=13)),
                             height=300, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_p1, use_container_width=True)

    with pg2:
        # Prejuízo por categoria — donut
        cat_prej_data = prej_df_full.groupby("Categoria")["Lucro"].sum().abs().reset_index()
        cat_prej_data.columns = ["Categoria", "Prejuizo"]
        fig_p2 = go.Figure(go.Pie(
            labels=cat_prej_data["Categoria"],
            values=cat_prej_data["Prejuizo"],
            hole=0.55,
            marker=dict(colors=["#ff5252", "#ff7043", "#ff8a65", "#ffab91"], line=dict(color="#0d0d0d", width=2)),
            textfont=dict(color="#ccc", size=11),
            hovertemplate="<b>%{label}</b><br>Prejuízo: R$ %{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig_p2.update_layout(**base, title=dict(text="Prejuízo por Categoria", font=dict(color="#ccc", size=13)),
                             height=300,
                             annotations=[
                                 dict(text="Risco", x=0.5, y=0.5, font_size=13, font_color="#663333", showarrow=False)])
        st.plotly_chart(fig_p2, use_container_width=True)

    with pg3:
        # Comparativo lucro vs prejuízo por categoria (barras empilhadas)
        cat_all = df.groupby("Categoria").apply(
            lambda x: pd.Series({
                "Lucro Positivo": x.loc[x["Lucro"] > 0, "Lucro"].sum(),
                "Prejuízo": x.loc[x["Lucro"] < 0, "Lucro"].sum(),
            })
        ).reset_index()

        fig_p3 = go.Figure()
        fig_p3.add_trace(go.Bar(name="Lucro", x=cat_all["Categoria"], y=cat_all["Lucro Positivo"], marker_color=GREEN))
        fig_p3.add_trace(go.Bar(name="Prejuízo", x=cat_all["Categoria"], y=cat_all["Prejuízo"], marker_color=RED))
        fig_p3.add_hline(y=0, line_color="#333", line_width=1)
        fig_p3.update_layout(**base,
                             title=dict(text="Lucro × Prejuízo por Categoria", font=dict(color="#ccc", size=13)),
                             barmode="overlay", height=300, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_p3, use_container_width=True)

    # Tabela detalhada dos prejuízos
    st.markdown("##### Detalhamento dos trades negativos")
    prej_show = prej_df_full[["Nome", "Categoria", "Compra", "Venda_Bruta", "Lucro", "ROI"]].copy()
    prej_show.columns = ["Skin", "Categoria", "Compra (R$)", "Venda Bruta (R$)", "Prejuízo (R$)", "ROI (%)"]
    prej_show = prej_show.sort_values("Prejuízo (R$)")


    def red_fmt(val):
        return "color:#ff5252;font-weight:600"


    st.dataframe(
        prej_show.style
        .map(red_fmt, subset=["Prejuízo (R$)", "ROI (%)"])
        .format({"Compra (R$)": "R$ {:,.0f}", "Venda Bruta (R$)": "R$ {:,.0f}",
                 "Prejuízo (R$)": "R$ {:,.2f}", "ROI (%)": "{:.1f}%"}),
        use_container_width=True, height=220,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 5 — RANKING COMPLETO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Ranking de Trades</div>", unsafe_allow_html=True)
ra, rb = st.columns(2)

with ra:
    if show_lucro:
        top10 = fdf.nlargest(10, "Lucro")
        fig7 = go.Figure(go.Bar(
            x=top10["Lucro"], y=top10["Nome"].str[:22], orientation="h",
            marker_color=GREEN,
            text=[f"{v:.0f}% ROI" for v in top10["ROI"]],
            textposition="outside", textfont=dict(color="#ccc", size=10),
            hovertemplate="<b>%{y}</b><br>Lucro: R$ %{x:,.0f}<extra></extra>",
        ))
        fig7.update_layout(**base, title=dict(text="🏆 Top 10 Melhores Trades", font=dict(color="#ccc", size=13)),
                           height=360, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig7, use_container_width=True)
    else:
        top10_neg = fdf.nsmallest(10, "Lucro")
        fig7 = go.Figure(go.Bar(
            x=top10_neg["Lucro"], y=top10_neg["Nome"].str[:22], orientation="h",
            marker_color=RED,
            text=[f"{v:.0f}% ROI" for v in top10_neg["ROI"]],
            textposition="outside", textfont=dict(color="#ccc", size=10),
            hovertemplate="<b>%{y}</b><br>Prejuízo: R$ %{x:,.0f}<extra></extra>",
        ))
        fig7.update_layout(**base, title=dict(text="🔻 Top 10 Piores Trades", font=dict(color="#ccc", size=13)),
                           height=360, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig7, use_container_width=True)

with rb:
    if show_lucro:
        # Top 10 por ROI
        top_roi = fdf[fdf["Lucro"] > 0].nlargest(10, "ROI")
        fig8 = go.Figure(go.Bar(
            x=top_roi["ROI"], y=top_roi["Nome"].str[:22], orientation="h",
            marker=dict(
                color=top_roi["ROI"],
                colorscale=[[0, "#ffd740"], [1, "#ff8a65"]],
                showscale=False,
            ),
            text=[f"R$ {v:,.0f}".replace(",", ".") for v in top_roi["Lucro"]],
            textposition="outside", textfont=dict(color="#ccc", size=10),
            hovertemplate="<b>%{y}</b><br>ROI: %{x:.1f}%<extra></extra>",
        ))
        fig8.update_layout(**base, title=dict(text="🚀 Top 10 Maior ROI (%)", font=dict(color="#ccc", size=13)),
                           height=360, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig8, use_container_width=True)
    else:
        # Top 10 piores ROI
        worst_roi = fdf[fdf["Lucro"] < 0].nsmallest(10, "ROI")
        fig8 = go.Figure(go.Bar(
            x=worst_roi["ROI"], y=worst_roi["Nome"].str[:22], orientation="h",
            marker=dict(
                color=worst_roi["ROI"],
                colorscale=[[0, "#b71c1c"], [1, "#ff8a65"]],
                showscale=False,
            ),
            text=[f"R$ {v:,.0f}".replace(",", ".") for v in worst_roi["Lucro"]],
            textposition="outside", textfont=dict(color="#ccc", size=10),
            hovertemplate="<b>%{y}</b><br>ROI: %{x:.1f}%<extra></extra>",
        ))
        fig8.update_layout(**base, title=dict(text="📉 Top 10 Pior ROI (%)", font=dict(color="#ccc", size=13)),
                           height=360, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig8, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 6 — HISTOGRAMA DE DISTRIBUIÇÃO + SKIN RANKING AGREGADO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Distribuição & Ranking por Skin</div>", unsafe_allow_html=True)
ha, hb = st.columns(2)

with ha:
    fig_hist = go.Figure()
    if show_lucro:
        lucros_pos = fdf[fdf["Lucro"] >= 0]["Lucro"]
        fig_hist.add_trace(go.Histogram(x=lucros_pos, name="Lucro", marker_color=GREEN, opacity=0.8, nbinsx=20))
    if show_prejuizo:
        lucros_neg = fdf[fdf["Lucro"] < 0]["Lucro"]
        fig_hist.add_trace(go.Histogram(x=lucros_neg, name="Prejuízo", marker_color=RED, opacity=0.8, nbinsx=10))
    fig_hist.add_vline(x=0, line_dash="dash", line_color="#444")
    fig_hist.update_layout(**base, title=dict(text="Distribuição de Resultados (R$)", font=dict(color="#ccc", size=13)),
                           barmode="overlay", height=300, xaxis_title="Lucro (R$)", yaxis_title="Nº de Trades")
    st.plotly_chart(fig_hist, use_container_width=True)

with hb:
    top_skins = skin_rank.head(10)
    fig_sr = go.Figure(go.Bar(
        x=top_skins["Lucro_Total"], y=top_skins["Nome"].str[:22], orientation="h",
        marker=dict(
            color=top_skins["Lucro_Total"],
            colorscale=[[0, "#003300"], [0.5, "#00aa44"], [1, "#00e676"]],
            showscale=False,
        ),
        text=[f"{int(t)} trades" for t in top_skins["Trades"]],
        textposition="outside", textfont=dict(color="#ccc", size=10),
        hovertemplate="<b>%{y}</b><br>Lucro Total: R$ %{x:,.0f}<extra></extra>",
    ))
    fig_sr.update_layout(**base, title=dict(text="Top 10 Skins por Lucro Acumulado", font=dict(color="#ccc", size=13)),
                         height=300, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_sr, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SEÇÃO 7 — TABELA COMPLETA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-title'>Histórico Completo</div>", unsafe_allow_html=True)

show_df = fdf[["Nome", "Categoria", "Compra", "Venda_Bruta", "Taxa", "Receita_Liq", "Lucro", "ROI"]].copy()
show_df.columns = ["Skin", "Categoria", "Compra (R$)", "Venda Bruta (R$)", "Taxa (R$)", "Receita Líq. (R$)",
                   "Lucro (R$)", "ROI (%)"]
show_df = show_df.sort_values("Lucro (R$)", ascending=False).reset_index(drop=True)


def color_lucro(val):
    return f"color:{'#00e676' if val > 0 else ('#ff5252' if val < 0 else '#888')};font-weight:600"


def color_roi(val):
    return f"color:{'#ffd740' if val > 30 else ('#ff5252' if val < 0 else '#aaa')}"


st.dataframe(
    show_df.style
    .map(color_lucro, subset=["Lucro (R$)"])
    .map(color_roi, subset=["ROI (%)"])
    .format({"Compra (R$)": "R$ {:,.0f}", "Venda Bruta (R$)": "R$ {:,.0f}",
             "Taxa (R$)": "R$ {:,.2f}", "Receita Líq. (R$)": "R$ {:,.2f}",
             "Lucro (R$)": "R$ {:,.2f}", "ROI (%)": "{:.1f}%"}),
    use_container_width=True, height=400,
)

st.markdown("""
<div style='text-align:center;padding:32px 0 16px;color:#222;font-size:11px;letter-spacing:1px;'>
  CS2 SKINS TRADING DASHBOARD · FABRICIO FORMENTINI · 2026
</div>""", unsafe_allow_html=True)