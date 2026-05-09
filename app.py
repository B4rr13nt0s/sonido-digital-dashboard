"""
app.py  —  Sonido Digital Intelligence Dashboard
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sonido Digital – Intelligence Dashboard",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── THEME COLORS ───────────────────────────────────────────────────────────────
C_DARK   = "#1A2B4A"
C_BLUE   = "#0E6DB5"
C_ACCENT = "#00BFFF"
C_WARN   = "#FF6B35"
C_OK     = "#2ECC71"
C_GRAY   = "#7F8C8D"

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #1A2B4A; }
    [data-testid="stSidebar"] * { color: white !important; }
    .metric-card {
        background: linear-gradient(135deg, #1A2B4A 0%, #0E6DB5 100%);
        border-radius: 12px; padding: 20px; color: white;
        box-shadow: 0 4px 15px rgba(14,109,181,0.3);
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #00BFFF; }
    .metric-label { font-size: 0.85rem; color: #A8C8E8; margin-top: 4px; }
    .alert-critical {
        background: rgba(231,76,60,0.15); border-left: 4px solid #E74C3C;
        border-radius: 8px; padding: 12px 16px; margin: 6px 0;
    }
    .alert-low {
        background: rgba(255,107,53,0.12); border-left: 4px solid #FF6B35;
        border-radius: 8px; padding: 12px 16px; margin: 6px 0;
    }
    .section-title {
        font-size: 1.3rem; font-weight: 700; color: #1A2B4A;
        border-bottom: 3px solid #0E6DB5; padding-bottom: 6px; margin-bottom: 16px;
    }
    div[data-testid="stTabs"] button { font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── DATA LOADING ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    products   = pd.read_csv(f"{base}/data/products.csv")
    inventory  = pd.read_csv(f"{base}/data/inventory.csv")
    sales      = pd.read_csv(f"{base}/data/sales.csv", parse_dates=["date"])
    inquiries  = pd.read_csv(f"{base}/data/inquiries.csv", parse_dates=["date"])
    inv_full   = inventory.merge(products[["product_id","product_name","brand","category","price_gtq","cost_gtq"]], on="product_id")
    return products, inventory, sales, inquiries, inv_full

products, inventory, sales, inquiries, inv_full = load_data()

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
st.sidebar.image("https://sonidodigital.com.gt/wp-content/uploads/2025/06/cropped-LOGO-SONIDO-DIGITAL-NEGRO-1.png",
                 use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Filtro de Fechas")
min_date = sales["date"].min().date()
max_date = sales["date"].max().date()
date_from = st.sidebar.date_input("Desde", value=datetime(2025, 1, 1).date(), min_value=min_date, max_value=max_date)
date_to   = st.sidebar.date_input("Hasta", value=max_date, min_value=min_date, max_value=max_date)

st.sidebar.markdown("### 🏷️ Marcas")
all_brands = sorted(products["brand"].unique())
sel_brands = st.sidebar.multiselect("Filtrar por marca", all_brands, default=all_brands)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📂 Categorías")
all_cats = sorted(products["category"].unique())
sel_cats = st.sidebar.multiselect("Filtrar por categoría", all_cats, default=all_cats)

# Apply filters
mask = (
    (sales["date"].dt.date >= date_from) &
    (sales["date"].dt.date <= date_to) &
    (sales["brand"].isin(sel_brands)) &
    (sales["category"].isin(sel_cats))
)
df_s = sales[mask].copy()

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='background:linear-gradient(135deg,{C_DARK} 0%,{C_BLUE} 100%);
            border-radius:14px; padding:24px 32px; margin-bottom:24px;'>
    <h1 style='color:white; margin:0; font-size:2rem;'>🔊 Sonido Digital — Intelligence Dashboard</h1>
    <p style='color:#A8C8E8; margin:6px 0 0;'>
        Car Audio · Motorsports · Marino &nbsp;|&nbsp;
        Datos: {date_from.strftime('%d/%m/%Y')} – {date_to.strftime('%d/%m/%Y')}
    </p>
</div>
""", unsafe_allow_html=True)

# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 KPIs & Ventas", "📦 Inventario", "📈 Pronóstico", "🤖 Asistente IA"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — KPIs & VENTAS
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    total_rev    = df_s["revenue_gtq"].sum()
    total_profit = df_s["profit_gtq"].sum()
    total_units  = df_s["quantity"].sum()
    margin_pct   = (total_profit / total_rev * 100) if total_rev > 0 else 0
    num_txn      = len(df_s)

    c1, c2, c3, c4, c5 = st.columns(5)
    def kpi(col, value, label, prefix="Q", suffix=""):
        col.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{prefix}{value:,.0f}{suffix}</div>
            <div class='metric-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

    kpi(c1, total_rev,    "Ingresos Totales")
    kpi(c2, total_profit, "Ganancia Bruta")
    kpi(c3, margin_pct,   "Margen Bruto", prefix="", suffix="%")
    kpi(c4, total_units,  "Unidades Vendidas", prefix="")
    kpi(c5, num_txn,      "Transacciones", prefix="")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("<div class='section-title'>Ingresos Mensuales por Categoría</div>", unsafe_allow_html=True)
        monthly = df_s.copy()
        monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
        monthly_cat = monthly.groupby(["month","category"])["revenue_gtq"].sum().reset_index()
        fig1 = px.bar(monthly_cat, x="month", y="revenue_gtq", color="category",
                      labels={"revenue_gtq":"Ingresos (Q)", "month":"Mes", "category":"Categoría"},
                      color_discrete_sequence=px.colors.qualitative.Bold)
        fig1.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="white", paper_bgcolor="white",
                           legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>Ingresos por Marca</div>", unsafe_allow_html=True)
        brand_rev = df_s.groupby("brand")["revenue_gtq"].sum().reset_index().sort_values("revenue_gtq", ascending=False)
        fig2 = px.pie(brand_rev, values="revenue_gtq", names="brand",
                      hole=0.45,
                      color_discrete_sequence=px.colors.qualitative.Bold)
        fig2.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                           paper_bgcolor="white",
                           legend=dict(orientation="h", y=-0.15, font_size=10))
        fig2.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("<div class='section-title'>Top 10 Productos por Ingresos</div>", unsafe_allow_html=True)
        top_prod = df_s.merge(products[["product_id","product_name"]], on="product_id")
        top_prod = top_prod.groupby("product_name")["revenue_gtq"].sum().reset_index()
        top_prod = top_prod.nlargest(10, "revenue_gtq")
        fig3 = px.bar(top_prod, x="revenue_gtq", y="product_name", orientation="h",
                      labels={"revenue_gtq":"Ingresos (Q)", "product_name":""},
                      color="revenue_gtq", color_continuous_scale=["#A8C8E8","#0E6DB5","#1A2B4A"])
        fig3.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="white", paper_bgcolor="white",
                           showlegend=False, coloraxis_showscale=False,
                           yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown("<div class='section-title'>Canal de Consultas vs. Conversión</div>", unsafe_allow_html=True)
        inq_f = inquiries[(inquiries["date"].dt.date >= date_from) & (inquiries["date"].dt.date <= date_to)]
        ch_conv = inq_f.groupby(["channel","outcome"]).size().reset_index(name="count")
        fig4 = px.bar(ch_conv, x="channel", y="count", color="outcome",
                      labels={"count":"Consultas", "channel":"Canal", "outcome":"Resultado"},
                      color_discrete_map={
                          "Venta concretada":"#2ECC71",
                          "Cotización enviada":"#0E6DB5",
                          "Sin respuesta":"#95A5A6",
                          "Cancelado":"#E74C3C"
                      })
        fig4.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="white", paper_bgcolor="white",
                           legend=dict(orientation="h", y=-0.25, font_size=10))
        st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — INVENTARIO
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-title'>Estado del Inventario</div>", unsafe_allow_html=True)

    crit = inv_full[inv_full["status"] == "Crítico"]
    low  = inv_full[inv_full["status"] == "Bajo"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔴 Crítico (sin stock)", len(crit))
    col2.metric("🟠 Stock Bajo", len(low))
    col3.metric("🟢 Normal", len(inv_full[inv_full["status"]=="OK"]))
    col4.metric("🔵 Sobrestock", len(inv_full[inv_full["status"]=="Sobrestock"]))

    if len(crit) > 0:
        st.markdown("#### 🔴 Productos sin stock — requieren reposición inmediata")
        for _, r in crit.iterrows():
            st.markdown(f"""
            <div class='alert-critical'>
                <strong>{r['product_name']}</strong> ({r['brand']}) — {r['category']}<br>
                <small>Stock: 0 / Punto de reorden: {r['reorder_point']} / Máx: {r['max_stock']}</small>
            </div>""", unsafe_allow_html=True)

    if len(low) > 0:
        st.markdown("#### 🟠 Productos con stock bajo")
        for _, r in low.iterrows():
            st.markdown(f"""
            <div class='alert-low'>
                <strong>{r['product_name']}</strong> ({r['brand']}) — {r['category']}<br>
                <small>Stock: {r['current_stock']} / Punto de reorden: {r['reorder_point']}</small>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown("<div class='section-title'>Stock Actual por Producto</div>", unsafe_allow_html=True)
        status_colors = {"Crítico":"#E74C3C","Bajo":"#FF6B35","OK":"#2ECC71","Sobrestock":"#3498DB"}
        inv_full["color"] = inv_full["status"].map(status_colors)
        fig5 = px.bar(inv_full.sort_values("current_stock"),
                      x="current_stock", y="product_name", orientation="h",
                      color="status",
                      color_discrete_map=status_colors,
                      labels={"current_stock":"Unidades en Stock","product_name":"","status":"Estado"})
        fig5.update_layout(height=480, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="white", paper_bgcolor="white",
                           yaxis=dict(tickfont=dict(size=9)))
        st.plotly_chart(fig5, use_container_width=True)

    with col_f:
        st.markdown("<div class='section-title'>Valor de Inventario por Marca</div>", unsafe_allow_html=True)
        inv_full["inventory_value"] = inv_full["current_stock"] * inv_full["cost_gtq"]
        brand_val = inv_full.groupby("brand")["inventory_value"].sum().reset_index()
        fig6 = px.bar(brand_val.sort_values("inventory_value", ascending=False),
                      x="brand", y="inventory_value",
                      labels={"inventory_value":"Valor (Q costo)","brand":"Marca"},
                      color="inventory_value",
                      color_continuous_scale=["#A8C8E8","#0E6DB5","#1A2B4A"])
        fig6.update_layout(height=480, margin=dict(t=10,b=10,l=10,r=10),
                           plot_bgcolor="white", paper_bgcolor="white",
                           coloraxis_showscale=False)
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("<div class='section-title'>Tabla Completa de Inventario</div>", unsafe_allow_html=True)
    display_inv = inv_full[["product_name","brand","category","current_stock","reorder_point","max_stock","status","last_restock"]].copy()
    display_inv.columns = ["Producto","Marca","Categoría","Stock Actual","Punto Reorden","Stock Máx","Estado","Último Restock"]
    st.dataframe(display_inv, use_container_width=True, hide_index=True,
                 column_config={"Estado": st.column_config.TextColumn("Estado")})

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PRONÓSTICO DE DEMANDA
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-title'>Pronóstico de Demanda — Próximos 90 días</div>", unsafe_allow_html=True)
    st.info("Modelo: Media Móvil Ponderada + ajuste de estacionalidad mensual. Para producción, reemplazar con Prophet o ARIMA.")

    # Simple weighted moving average forecast per category
    sales_full = sales.copy()
    sales_full["month"] = sales_full["date"].dt.to_period("M")
    monthly_units = sales_full.groupby(["month","category"])["quantity"].sum().reset_index()
    monthly_units["month_dt"] = monthly_units["month"].dt.to_timestamp()

    seasonality_idx = {1:0.9,2:0.85,3:1.0,4:1.0,5:0.95,6:1.15,
                       7:1.1,8:1.0,9:0.95,10:1.05,11:1.2,12:1.4}

    cats_for_forecast = sorted(sales_full["category"].unique())
    sel_cat_f = st.selectbox("Seleccionar Categoría", cats_for_forecast)

    cat_data = monthly_units[monthly_units["category"] == sel_cat_f].sort_values("month_dt")

    # Weighted moving average (more weight on recent months)
    values = cat_data["quantity"].values
    weights = np.arange(1, len(values)+1, dtype=float)
    wma = np.dot(weights, values) / weights.sum()

    # Generate 3-month forecast
    last_month = cat_data["month_dt"].max()
    forecast_months = pd.date_range(last_month + pd.offsets.MonthBegin(1), periods=3, freq="MS")
    forecast_vals = [round(wma * seasonality_idx[m.month]) for m in forecast_months]

    # Upper/lower bands (±15%)
    upper = [round(v * 1.15) for v in forecast_vals]
    lower = [round(v * 0.85) for v in forecast_vals]

    fig7 = go.Figure()
    # Historical
    fig7.add_trace(go.Scatter(
        x=cat_data["month_dt"], y=cat_data["quantity"],
        name="Histórico", line=dict(color=C_BLUE, width=2),
        mode="lines+markers"
    ))
    # Forecast
    fig7.add_trace(go.Scatter(
        x=forecast_months, y=forecast_vals,
        name="Pronóstico", line=dict(color=C_ACCENT, width=2, dash="dash"),
        mode="lines+markers", marker=dict(size=8, symbol="diamond")
    ))
    # Confidence band
    fig7.add_trace(go.Scatter(
        x=list(forecast_months) + list(forecast_months[::-1]),
        y=upper + lower[::-1],
        fill="toself", fillcolor="rgba(0,191,255,0.12)",
        line=dict(color="rgba(0,0,0,0)"), name="Banda ±15%"
    ))
    fig7.update_layout(
        height=380, margin=dict(t=10,b=10,l=10,r=10),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis_title="Mes", yaxis_title="Unidades",
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig7, use_container_width=True)

    # Forecast table
    fc_df = pd.DataFrame({
        "Mes": [m.strftime("%B %Y") for m in forecast_months],
        "Pronóstico (unidades)": forecast_vals,
        "Mínimo estimado": lower,
        "Máximo estimado": upper,
    })
    st.dataframe(fc_df, use_container_width=True, hide_index=True)

    st.markdown("<br>")
    st.markdown("<div class='section-title'>Comparativa Estacional por Categoría</div>", unsafe_allow_html=True)
    monthly_units["month_num"] = monthly_units["month_dt"].dt.month
    monthly_units["month_name"] = monthly_units["month_dt"].dt.strftime("%b")
    seasonal = monthly_units.groupby(["month_num","month_name","category"])["quantity"].mean().reset_index()
    seasonal = seasonal.sort_values("month_num")
    fig8 = px.line(seasonal, x="month_name", y="quantity", color="category",
                   labels={"quantity":"Unidades Promedio","month_name":"Mes","category":"Categoría"},
                   markers=True,
                   color_discrete_sequence=px.colors.qualitative.Bold)
    fig8.update_layout(height=320, margin=dict(t=10,b=10,l=10,r=10),
                       plot_bgcolor="white", paper_bgcolor="white",
                       legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig8, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — AI ASSISTANT
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-title'>🤖 Asistente de Inteligencia de Negocio</div>", unsafe_allow_html=True)
    st.markdown("Consultame sobre inventario, ventas, marcas o productos. Tengo acceso a los datos en tiempo real.")

    # Build context snapshot for the LLM
    def build_context():
        total_r = sales["revenue_gtq"].sum()
        total_p = sales["profit_gtq"].sum()
        top_brand = sales.groupby("brand")["revenue_gtq"].sum().idxmax()
        top_prod_id = sales.groupby("product_id")["revenue_gtq"].sum().idxmax()
        top_prod_name = products[products["product_id"]==top_prod_id]["product_name"].values[0]
        crit_items = inv_full[inv_full["status"]=="Crítico"]["product_name"].tolist()
        low_items  = inv_full[inv_full["status"]=="Bajo"]["product_name"].tolist()
        brands = products["brand"].unique().tolist()
        cats   = products["category"].unique().tolist()

        return f"""
Eres un asistente de inteligencia de negocio para Sonido Digital Guatemala,
una empresa distribuidora de audio profesional para Car Audio, Motorsports y Marino.

DATOS ACTUALES DEL NEGOCIO:
- Ingresos totales históricos: Q{total_r:,.0f}
- Ganancia bruta histórica: Q{total_p:,.0f}
- Margen promedio: {total_p/total_r*100:.1f}%
- Marca con mayores ventas: {top_brand}
- Producto top en ingresos: {top_prod_name}
- Productos SIN stock (crítico): {', '.join(crit_items) if crit_items else 'Ninguno'}
- Productos con stock bajo: {', '.join(low_items) if low_items else 'Ninguno'}
- Marcas distribuidas: {', '.join(brands)}
- Categorías: {', '.join(cats)}
- Total productos en catálogo: {len(products)}
- Total transacciones registradas: {len(sales)}
- Período de datos: Enero 2024 – Junio 2025

INSTRUCCIONES:
- Responde siempre en español, de forma clara y orientada a decisiones de negocio.
- Si te preguntan sobre datos específicos, usa los datos reales arriba.
- Si te piden una recomendación, sé concreto y accionable.
- Mantén un tono profesional pero amigable.
- Si no tienes el dato exacto, indícalo claramente.
"""

    # Chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Suggested questions
    st.markdown("**Preguntas sugeridas:**")
    qcols = st.columns(3)
    suggestions = [
        "¿Cuáles productos necesitan reposición urgente?",
        "¿Qué marca genera más ganancia?",
        "¿Cómo van las ventas de Subwoofers este año?",
        "¿Cuál es el canal de ventas más efectivo?",
        "¿Qué productos tienen sobrestock?",
        "Dame un resumen ejecutivo del negocio",
    ]
    for i, q in enumerate(suggestions):
        if qcols[i % 3].button(q, key=f"sug_{i}"):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

    st.markdown("---")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Escribe tu pregunta sobre el negocio..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analizando datos..."):
                try:
                    import anthropic
                    client = anthropic.Anthropic()
                    system_ctx = build_context()

                    # Keep last 10 messages for context
                    history = st.session_state.messages[-10:]
                    api_messages = [{"role": m["role"], "content": m["content"]} for m in history]

                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1024,
                        system=system_ctx,
                        messages=api_messages
                    )
                    answer = response.content[0].text
                except Exception as e:
                    answer = f"⚠️ Error al conectar con el asistente: {str(e)}\n\nAsegúrate de tener configurada la variable de entorno `ANTHROPIC_API_KEY`."

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

    if st.session_state.messages:
        if st.button("🗑️ Limpiar conversación"):
            st.session_state.messages = []
            st.rerun()
