"""
YellowSense Maritime Intelligence Platform
==========================================
AI-Powered Maritime Port Intelligence & Decision Support Platform
Production-grade PoC — Warm Amber Theme, 9-Tab Horizontal Navigation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timezone
from pathlib import Path
import base64
import time
import os

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YellowSense Maritime Intelligence",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Constants ────────────────────────────────────────────────────────────────
API = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
LOGO_PATH = Path(__file__).parent.parent / "assets" / "logo11.png"
ARCH_DIR = Path(__file__).parent.parent

COMMODITY_COLORS = {
    "Coal": "#374151", "Iron Ore": "#DC2626", "Containers": "#2563EB",
    "Crude Oil": "#7C3AED", "LNG": "#059669", "Fertilizers": "#D97706",
    "Automobiles": "#0891B2", "Agricultural": "#65A30D",
}

SEVERITY_COLORS = {"Critical": "#DC2626", "High": "#D97706", "Medium": "#2563EB", "Low": "#059669"}
SEVERITY_BG = {"Critical": "#FEF2F2", "High": "#FFFBEB", "Medium": "#EFF6FF", "Low": "#F0FDF4"}

# ─── API Helper ───────────────────────────────────────────────────────────────
def api_get(path: str, params: dict = None):
    try:
        r = requests.get(f"{API}{path}", params=params, timeout=6)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"API GET Error ({path}): {e}")
        return None

def api_post(path: str, payload: dict = None):
    try:
        r = requests.post(f"{API}{path}", json=payload or {}, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"API POST Error ({path}): {e}")
        st.error(f"Backend API Error: {e}")
        return None

# ─── Logo Helper ──────────────────────────────────────────────────────────────
def get_logo_b64():
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ─── Premium CSS — Cream / YellowSense Brand (Ref: Image 4) ── */
st.markdown("""
<style>
/* Using System Native Fonts */

/* ── Reset & Base ── */
html, body, [class*="css"] { font-family: system-ui, sans-serif; }
h1,h2,h3,h4,h5,h6 { font-family: system-ui, sans-serif; }

/* ── App Background — Very Pale Cream ── */
.stApp {
    background: #FCFAF5;
    color: #292524;
    min-height: 100vh;
}
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem;
    max-width: 1200px !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header, [data-testid="stSidebarNav"] { visibility: hidden; }
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

/* ── Floating Header Card ── */
.ys-header {
    background: #FFFDF9;
    padding: 16px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    margin-bottom: 20px;
    border: 1px solid #F3E8D6;
}
.ys-header-left {
    display: flex;
    align-items: center;
    gap: 16px;
}
.ys-header-logo {
    height: 48px;
    width: auto;
    object-fit: contain;
}
.ys-header-title {
    font-family: system-ui, sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #1C1917;
    letter-spacing: -0.3px;
    line-height: 1.1;
}
.ys-header-subtitle {
    font-size: 13px;
    color: #92400E;
    font-weight: 600;
}
.ys-header-right {
    display: flex;
    align-items: center;
}
.ys-live-badge {
    background: #FEF3C7;
    color: #92400E;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    border: 1px solid #FDE68A;
}

/* ── Tab Navigation Pills ── */
div.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    gap: 8px;
    border-bottom: none;
    margin-bottom: 20px;
}
div.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 20px;
    color: #78716C;
    font-family: system-ui, sans-serif;
    font-weight: 600;
    font-size: 13px;
    padding: 8px 18px;
    border: none;
    transition: all 0.2s ease;
}
div.stTabs [aria-selected="true"] {
    background: #FEF3C7 !important;
    color: #92400E !important;
    border-bottom: 2px solid #EF4444 !important;
    border-radius: 12px 12px 0 0;
    box-shadow: none !important;
}

/* ── Page Content Wrapper ── */
.ys-content {
    padding: 10px 0;
}

/* ── Section Headers ── */
.sec-title {
    font-family: system-ui, sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #1C1917;
    letter-spacing: -0.4px;
    margin: 0;
}
.sec-sub {
    font-size: 14px;
    color: #78716C;
    margin-top: 6px;
    margin-bottom: 24px;
}
.sec-tag { display: none; }

/* ── Cards / Panels ── */
.kpi-card, .panel, div[data-testid="stMetric"], .pipeline-stage, .copilot-response {
    background: #FFFFFF;
    border: 1px solid #F3E8D6;
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.panel-title {
    font-family: system-ui, sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #1C1917;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #F9F5EC;
}

div[data-testid="stMetricLabel"] { font-size: 11px; font-weight: 700; color: #78716C !important; text-transform: uppercase; letter-spacing: 0.6px; }
div[data-testid="stMetricValue"] { font-family: system-ui, sans-serif; font-size: 28px; font-weight: 800; color: #1C1917 !important; }

/* ── Custom Button ── */
div.stButton > button {
    background: #EAB308 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: system-ui, sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 24px !important;
    box-shadow: 0 2px 4px rgba(234,179,8,0.2) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    background: #CA8A04 !important;
    box-shadow: 0 4px 8px rgba(202,138,4,0.3) !important;
}

/* ── Trace Steps & Logs ── */
.trace-step {
    display: flex; align-items: flex-start; gap: 14px;
    padding: 12px 16px; border-radius: 8px; margin-bottom: 8px;
    background: #FCFAF5; border: 1px solid #F3E8D6;
}
.trace-num {
    background: #EAB308; color: #FFFFFF;
    font-family: system-ui, sans-serif; font-weight: 800; font-size: 13px;
    width: 26px; height: 26px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.trace-component { font-weight: 700; font-size: 13px; color: #1C1917; }
.trace-action    { font-size: 13px; color: #44403C; }
.trace-detail    { font-size: 11px; color: #78716C; margin-top: 2px; }
.trace-ms        { font-size: 11px; color: #CA8A04; font-weight: 600; margin-left: auto; }

.log-container {
    background: #FCFAF5; border: 1px solid #F3E8D6; border-radius: 10px;
    padding: 16px; max-height: 340px; overflow-y: auto;
    font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 12px;
}
.log-row { padding: 4px 0; border-bottom: 1px solid #F9F5EC; display: flex; gap: 10px; }
.log-ts   { color: #A8A29E; min-width: 65px; }
.log-src  { color: #1C1917; font-weight: 700; min-width: 95px; }
.log-info { color: #57534E; }
.log-warn { color: #D97706; }

.stDataFrame { border: 1px solid #F3E8D6; border-radius: 8px; }
.stTextArea textarea { border: 1px solid #F3E8D6 !important; border-radius: 8px !important; background: #FFFFFF !important; }
.stTextArea textarea:focus { border-color: #EAB308 !important; box-shadow: 0 0 0 2px rgba(234,179,8,0.2) !important; }
.stSpinner > div { border-top-color: #EAB308 !important; }

/* ── Restored Missing Components ── */
.alert-card { border-radius: 10px; padding: 16px 18px; margin-bottom: 12px; border-left: 4px solid; }
.alert-critical { background: #FEF2F2; border-color: #DC2626; }
.alert-high     { background: #FFFBEB; border-color: #D97706; }
.alert-medium   { background: #EFF6FF; border-color: #2563EB; }
.alert-low      { background: #F0FDF4; border-color: #059669; }
.alert-title    { font-family: system-ui, sans-serif; font-size: 14px; font-weight: 700; color: #1C1917; }
.alert-desc     { font-size: 12px; color: #78716C; margin-top: 5px; line-height: 1.5; }
.alert-meta     { font-size: 11px; color: #92400E; margin-top: 8px; display: flex; gap: 16px; flex-wrap: wrap; }
.badge          { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
.badge-crit     { background: #FEE2E2; color: #DC2626; }
.badge-high     { background: #FEF3C7; color: #D97706; }
.badge-med      { background: #DBEAFE; color: #2563EB; }
.badge-low      { background: #DCFCE7; color: #059669; }

.rec-card { background: #FFFFFF; border: 1px solid #F3E8D6; border-radius: 12px; padding: 18px 20px; margin-bottom: 14px; border-left: 5px solid #F59E0B; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
.rec-action     { font-family: system-ui, sans-serif; font-size: 15px; font-weight: 700; color: #1C1917; }
.rec-rationale  { font-size: 12px; color: #78716C; margin-top: 5px; line-height: 1.5; }
.rec-impacts    { display: flex; gap: 16px; margin-top: 12px; flex-wrap: wrap; }
.rec-impact-pos { color: #059669; font-size: 13px; font-weight: 700; }
.rec-impact-neg { color: #DC2626; font-size: 13px; font-weight: 700; }
.rec-meta       { font-size: 11px; color: #92400E; margin-top: 8px; display: flex; gap: 14px; flex-wrap: wrap; }

.event-row { display: flex; align-items: flex-start; gap: 12px; padding: 10px 0; border-bottom: 1px solid #F3E8D6; }
.event-time { font-size: 11px; color: #78716C; min-width: 48px; font-weight: 600; }
.event-dot  { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 4px; }
.event-dot-arrival  { background: #059669; }
.event-dot-alert    { background: #DC2626; }
.event-dot-departure{ background: #2563EB; }
.event-dot-forecast { background: #7C3AED; }
.event-dot-incentive{ background: #F59E0B; }
.event-dot-system   { background: #78716C; }
.event-msg  { font-size: 12.5px; color: #1C1917; line-height: 1.4; }

.opp-card { background: #FFFFFF; border: 1px solid #F3E8D6; border-left: 5px solid #F59E0B; border-radius: 12px; padding: 16px 18px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
.opp-rank        { font-family: system-ui, sans-serif; font-size: 24px; font-weight: 900; color: #F59E0B; }
.opp-commodity   { font-size: 13px; font-weight: 700; color: #92400E; }
.opp-route       { font-size: 12px; color: #57534E; margin: 3px 0; }
.opp-opportunity { font-size: 12px; color: #1C1917; line-height: 1.5; margin-top: 6px; }
.opp-metrics     { display: flex; gap: 14px; margin-top: 10px; }
.opp-revenue     { font-size: 15px; font-weight: 800; color: #059669; font-family: system-ui, sans-serif; }

.pipeline-stage-title { font-family: system-ui, sans-serif; font-size: 14px; font-weight: 700; color: #1C1917; margin-bottom: 6px; }
.pipeline-stage-sub   { font-size: 11px; color: #78716C; line-height: 1.4; }

/* Plotly Theme Updates */
.js-plotly-plot .plotly { border-radius: 10px; overflow: hidden; background: #FFFFFF; }

</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
logo_b64 = get_logo_b64()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="ys-header-logo" />' if logo_b64 else ""
ts = datetime.now(timezone.utc).strftime("%d %b %Y  %H:%M UTC")

st.markdown(f"""
<div class="ys-header">
  <div class="ys-header-left">
    {logo_html}
    <div>
      <div class="ys-header-title">Maritime Intelligence Platform</div>
      <div class="ys-header-subtitle">AI-POWERED PREDICTIVE CARGO ANALYTICS & DECISION SUPPORT SYSTEM</div>
    </div>
  </div>
  <div class="ys-header-right">
    <div class="ys-live-badge">
      <div class="ys-live-dot"></div>
      LIVE DATA
    </div>
    <div class="ys-timestamp">{ts}</div>
  </div>
</div>

<div style="background: linear-gradient(135deg, #FFFDF9 0%, #FEF3C7 100%); border: 1px solid #FDE68A; border-radius: 14px; padding: 16px 24px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
  <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
    <div>
      <div style="font-size: 11px; font-weight: 800; color: #D97706; letter-spacing: 0.8px; text-transform: uppercase;">PRIMARY CORE CAPABILITY</div>
      <div style="font-size: 20px; font-weight: 800; color: #1C1917; margin-top: 2px;">Predictive Cargo Analytics — See What's Coming. Plan Ahead.</div>
      <div style="font-size: 13px; color: #78716C; margin-top: 4px; line-height: 1.4;">
        <b>Operational Flow:</b> Historical Cargo Data &rarr; ML Analysis &rarr; Cargo Forecast &rarr; Commodity & Trade Demand &rarr; Risk & Anomaly Detection &rarr; Port Planning Decisions
      </div>
    </div>
    <div style="background: #FFFFFF; border: 1px solid #F3E8D6; padding: 8px 18px; border-radius: 20px; font-size: 12px; font-weight: 700; color: #92400E; display: flex; align-items: center; gap: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
      <span>⚓</span> <span>Core Capability: Cargo Volume & Arrival Forecasting</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Plotly Theme ─────────────────────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FFFFFF",
    font=dict(family="system-ui, sans-serif", color="#1C1917", size=13),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor="#F9F5EC", linecolor="#E5E7EB", tickfont=dict(color="#1C1917", size=12), title=dict(font=dict(color="#1C1917", size=14, weight="bold"))),
    yaxis=dict(gridcolor="#F9F5EC", linecolor="#E5E7EB", tickfont=dict(color="#1C1917", size=12), title=dict(font=dict(color="#1C1917", size=14, weight="bold"))),
)
GOLD = "#F59E0B"
GOLD_DARK = "#D97706"
GOLD_LIGHT = "#FDE68A"

# ─── Tab Navigation ───────────────────────────────────────────────────────────
tabs = st.tabs([
    "Executive Dashboard",
    "Vessel Intelligence",
    "⭐ Cargo Forecasting",
    "Trade Intelligence",
    "Anomaly Detection",
    "Incentive Engine",
    "Digital Twin",
    "AI Maritime Copilot",
    "Data Pipeline",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — EXECUTIVE DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">Executive Command Center</span>
      <span class="sec-tag">Real-Time</span>
      <div class="sec-sub">Port-wide operational intelligence — live KPIs, vessel positions, berth utilization & revenue</div>
    </div>""", unsafe_allow_html=True)

    kpis = api_get("/executive/kpis") or {
        "berth_utilization_pct": 72.4, "berth_delta": "+2.1%",
        "active_vessels_inbound": 25, "vessels_delta": "+3",
        "daily_throughput_mt": 124000, "throughput_delta": "+3.2%",
        "revenue_cr": 118.5, "revenue_delta": "+6.8%",
        "congestion_index": 0.63, "congestion_delta": "-0.04",
        "vessels_at_anchor": 7, "anchor_delta": "+2",
        "avg_turnaround_hrs": 22.4, "turnaround_delta": "-1.2%",
        "forecast_accuracy_pct": 91.2, "accuracy_delta": "+0.8%",
    }

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Berth Utilization", f"{kpis['berth_utilization_pct']}%", kpis['berth_delta'])
        st.metric("Avg Turnaround", f"{kpis['avg_turnaround_hrs']}h", kpis['turnaround_delta'])
    with c2:
        st.metric("Vessels Inbound", str(kpis['active_vessels_inbound']), kpis['vessels_delta'])
        st.metric("Vessels at Anchor", str(kpis['vessels_at_anchor']), kpis['anchor_delta'])
    with c3:
        st.metric("Daily Throughput", f"{kpis['daily_throughput_mt']:,} MT", kpis['throughput_delta'])
        st.metric(
            "Forecast Accuracy" + (" (ML)" if kpis.get("forecast_accuracy_is_ml") else ""),
            f"{kpis['forecast_accuracy_pct']}%", kpis['accuracy_delta']
        )
    with c4:
        st.metric("Revenue Index", f"₹{kpis['revenue_cr']} Cr", kpis['revenue_delta'])
        st.metric(
            "Congestion Index" + (" (ML)" if kpis.get("congestion_index_is_ml") else ""),
            f"{kpis['congestion_index']}", kpis['congestion_delta']
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])

    with col_left:
        # NMPA Vessel Map
        vessels_data = api_get("/vessels/") or {"vessels": []}
        vessels = vessels_data.get("vessels", [])
        if vessels:
            df_v = pd.DataFrame(vessels)
            fig_map = px.scatter(
                df_v, x="lon", y="lat", size="capacity_mt",
                color="commodity", color_discrete_map=COMMODITY_COLORS,
                hover_name="name", hover_data={"commodity": True, "destination_name": True, "speed_kn": True, "delay_prob": True, "status": True},
                title="Live Vessel Positions — New Mangalore Port Authority (NMPA) Approach & Anchorages",
                labels={"lon": "Longitude (°E)", "lat": "Latitude (°N)"},
                size_max=26,
            )
            # Add NMPA Port Harbor Indicator Marker
            fig_map.add_trace(go.Scatter(
                x=[74.8100], y=[12.9200],
                mode="markers+text",
                marker=dict(size=14, color="#DC2626", symbol="star"),
                name="NMPA Port (Panambur)",
                text=["NMPA Harbor"],
                textposition="top center",
                textfont=dict(size=11, color="#DC2626", family="Arial Black")
            ))
            fig_map.update_layout(**PLOTLY_THEME, height=380, showlegend=True,
                                   legend=dict(orientation="h", y=-0.2, font=dict(size=10)))
            fig_map.update_traces(marker=dict(opacity=0.85, line=dict(width=0.5, color="white")))
            st.plotly_chart(fig_map, use_container_width=True)

        # Revenue & Throughput Trend
        trend = api_get("/executive/revenue-trend") or {"dates": [], "revenue_cr": [], "throughput_mt": []}
        if trend.get("dates"):
            fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
            fig_trend.add_trace(go.Scatter(
                x=trend["dates"], y=trend["revenue_cr"], name="Revenue (₹ Cr)",
                line=dict(color=GOLD, width=2.5), fill="tozeroy",
                fillcolor="rgba(245,158,11,0.08)"
            ), secondary_y=False)
            fig_trend.add_trace(go.Scatter(
                x=trend["dates"], y=trend["throughput_mt"], name="Throughput (MT)",
                line=dict(color="#2563EB", width=2, dash="dot")
            ), secondary_y=True)
            fig_trend.update_layout(**PLOTLY_THEME, height=260, title="30-Day Revenue & Throughput Trend",
                                     legend=dict(orientation="h", y=-0.2))
            fig_trend.update_yaxes(title_text="Revenue (₹ Cr)", secondary_y=False,
                                    gridcolor="#FEF3C7", linecolor="#FDE68A")
            fig_trend.update_yaxes(title_text="Throughput (MT)", secondary_y=True,
                                    gridcolor="rgba(0,0,0,0)", linecolor="#FDE68A")
            st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        # Berth Status
        berths_data = api_get("/cargo/berths") or {"berths": []}
        berths = berths_data.get("berths", [])
        if berths:
            df_b = pd.DataFrame(berths)
            occupied_pct = df_b["occupied"].mean() * 100
            fig_berth = go.Figure(go.Bar(
                x=df_b["berth_id"],
                y=df_b["utilization_pct"],
                marker_color=[GOLD if o else "#E5E7EB" for o in df_b["occupied"]],
                text=df_b["commodity"].fillna("Free"),
                textposition="outside",
                textfont=dict(size=9),
            ))
            fig_berth.update_layout(**PLOTLY_THEME, height=260,
                                     title=f"Berth Occupancy — {occupied_pct:.0f}% Utilized",
                                     xaxis_title="Berth", yaxis_title="Utilization %")
            fig_berth.update_yaxes(range=[0, 115], gridcolor="#FEF3C7")
            st.plotly_chart(fig_berth, use_container_width=True)

        # Cargo by Commodity Donut
        if vessels:
            comm_counts = df_v["commodity"].value_counts().reset_index()
            comm_counts.columns = ["commodity", "count"]
            fig_donut = px.pie(
                comm_counts, names="commodity", values="count",
                color="commodity", color_discrete_map=COMMODITY_COLORS,
                title="Active Vessels by Commodity", hole=0.55,
            )
            fig_donut.update_layout(**PLOTLY_THEME, height=260,
                                     legend=dict(orientation="h", y=-0.1, font=dict(size=10)))
            fig_donut.update_traces(textposition="inside", textinfo="percent+label",
                                     textfont_size=10)
            st.plotly_chart(fig_donut, use_container_width=True)

        # Port Events
        st.markdown('<div class="panel"><div class="panel-title">Recent Port Events</div>', unsafe_allow_html=True)
        evts = api_get("/executive/events") or {"events": []}
        for e in evts.get("events", [])[:6]:
            dot_class = f"event-dot-{e.get('type', 'system')}"
            st.markdown(f"""
            <div class="event-row">
              <div class="event-time">{e['time']}</div>
              <div class="event-dot {dot_class}"></div>
              <div class="event-msg">{e['message']}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — VESSEL INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">New Mangalore Port (NMPA) Vessel Intelligence Engine</span>
      <span class="sec-tag">Module 1</span>
      <div class="sec-sub">NMPA AIS tracking, ETA predictions, berth queueing, delay probability & route risk scoring</div>
    </div>""", unsafe_allow_html=True)

    v_data = api_get("/vessels/") or {"vessels": []}
    alerts_data = api_get("/vessels/congestion-alerts") or {"alerts": []}
    vessels = v_data.get("vessels", [])
    alerts = alerts_data.get("alerts", [])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Vessels Tracked", len(vessels))
    c2.metric("High Risk Vessels", len([v for v in vessels if v.get("route_risk", 0) > 0.7]))
    c3.metric("Vessels < 48h ETA", len([v for v in vessels if v.get("hours_to_arrival", 999) < 48]))
    c4.metric("Avg Delay Probability", f"{sum(v.get('delay_prob',0) for v in vessels)/max(len(vessels),1):.0%}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])

    with col_l:
        if vessels:
            df_v = pd.DataFrame(vessels)
            show_cols = ["name", "flag", "commodity", "destination_name", "hours_to_arrival",
                         "speed_kn", "delay_prob", "route_risk", "status"]
            df_show = df_v[show_cols].copy()
            df_show.columns = ["Vessel", "Flag", "Commodity", "Destination", "ETA (hrs)",
                                "Speed (kn)", "Delay Prob", "Route Risk", "Status"]
            df_show = df_show.sort_values("ETA (hrs)")
            st.markdown('<div class="panel"><div class="panel-title">Vessel Tracker — 25 Active Vessels</div>', unsafe_allow_html=True)
            st.dataframe(df_show, use_container_width=True, height=380,
                         column_config={
                             "Delay Prob": st.column_config.ProgressColumn("Delay Prob", min_value=0, max_value=1, format="%.0%"),
                             "Route Risk": st.column_config.ProgressColumn("Route Risk", min_value=0, max_value=1, format="%.2f"),
                         })
            st.markdown('</div>', unsafe_allow_html=True)

            # ETA chart
            top_eta = df_v.nsmallest(15, "hours_to_arrival")
            fig_eta = px.bar(top_eta, x="hours_to_arrival", y="name", orientation="h",
                             color="commodity", color_discrete_map=COMMODITY_COLORS,
                             title="Next 15 Arrivals — Hours to Port",
                             labels={"hours_to_arrival": "Hours to Arrival", "name": ""})
            fig_eta.update_layout(**PLOTLY_THEME, height=380)
            fig_eta.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_eta, use_container_width=True)

    with col_r:
        st.markdown('<div class="panel"><div class="panel-title">Congestion Alerts</div>', unsafe_allow_html=True)
        if alerts:
            for a in alerts[:6]:
                sev = a.get("severity", "Medium")
                css_class = f"alert-{sev.lower()}"
                badge_class = f"badge-{sev[:4].lower()}"
                st.markdown(f"""
                <div class="alert-card {css_class}">
                  <div class="alert-title">{a['vessel']}</div>
                  <div class="alert-desc">{a['message']}</div>
                  <div class="alert-meta">
                    <span><b>Commodity:</b> {a['commodity']}</span>
                    <span><b>ETA:</b> {a['hours_to_arrival']}h</span>
                    <span><b>Risk:</b> {a['route_risk']:.2f}</span>
                    <span class="badge {badge_class}">{sev}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No active congestion alerts.")
        st.markdown('</div>', unsafe_allow_html=True)

        if vessels:
            df_risk = pd.DataFrame(vessels)
            fig_risk = px.scatter(df_risk, x="delay_prob", y="route_risk",
                                  size="capacity_mt", color="commodity",
                                  color_discrete_map=COMMODITY_COLORS,
                                  hover_name="name",
                                  title="Route Risk vs Delay Probability",
                                  labels={"delay_prob": "Delay Probability", "route_risk": "Route Risk Score"})
            fig_risk.add_hline(y=0.7, line_dash="dash", line_color="#DC2626", annotation_text="High Risk Threshold")
            fig_risk.add_vline(x=0.35, line_dash="dash", line_color="#D97706", annotation_text="High Delay")
            fig_risk.update_layout(**PLOTLY_THEME, height=300)
            st.plotly_chart(fig_risk, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CARGO FORECASTING
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">Cargo Projection & Predictability Command Center</span>
      <span class="sec-tag">Module 2 — Core Focus</span>
      <div class="sec-sub">Data-Grounded ML Forecasting · Dynamic 95% Confidence Intervals · Chronological Backtesting · Forecast Drivers · What-If Simulator</div>
    </div>

    <!-- Clear Cargo-Forecasting Introduction -->
    <div style="background: #FFFDF9; border: 1px solid #F3E8D6; border-left: 5px solid #EAB308; border-radius: 12px; padding: 18px 22px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
      <div style="font-size: 18px; font-weight: 800; color: #1C1917; letter-spacing: -0.3px;">Predictive Cargo Analytics</div>
      <div style="font-size: 13.5px; color: #57534E; margin-top: 6px; line-height: 1.5; font-weight: 500;">
        "Use historical port cargo movements, commodity patterns, vessel activity and operational factors to forecast future cargo volumes and support proactive port planning."
      </div>
    </div>

    <!-- 3 Visual Capability Cards -->
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px;">
      <div style="background: #FFFFFF; border: 1px solid #F3E8D6; border-top: 4px solid #EAB308; border-radius: 12px; padding: 18px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
        <div style="font-size: 15px; font-weight: 800; color: #1C1917;">Cargo Volume Forecasting</div>
        <div style="font-size: 12.5px; color: #78716C; margin-top: 8px; line-height: 1.5;">
          Predict future cargo throughput using historical cargo records and ML forecasting.
        </div>
      </div>
      <div style="background: #FFFFFF; border: 1px solid #F3E8D6; border-top: 4px solid #D97706; border-radius: 12px; padding: 18px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
        <div style="font-size: 15px; font-weight: 800; color: #1C1917;">Commodity & Trade Demand</div>
        <div style="font-size: 12.5px; color: #78716C; margin-top: 8px; line-height: 1.5;">
          Identify commodity-level and trade-demand trends to anticipate future cargo movement.
        </div>
      </div>
      <div style="background: #FFFFFF; border: 1px solid #F3E8D6; border-top: 4px solid #DC2626; border-radius: 12px; padding: 18px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
        <div style="font-size: 15px; font-weight: 800; color: #1C1917;">Cargo Risk & Anomaly Detection</div>
        <div style="font-size: 12.5px; color: #78716C; margin-top: 8px; line-height: 1.5;">
          Detect unusual cargo patterns, sudden volume changes and operational risks.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch available commodities
    meta = api_get("/cargo/commodities") or {"commodities": ["ALL"], "sections": ["ALL"]}
    commodity_status = meta.get("commodity_status", {})
    all_comms = [c for c in meta.get("commodities", []) if c != "ALL"]
    # Current-data commodities first, then legacy (2021-only) ones — so the
    # default view and top of the list favor commodities with live forecasts.
    current_comms = sorted(c for c in all_comms if commodity_status.get(c, {}).get("is_current", True))
    legacy_comms = sorted(c for c in all_comms if not commodity_status.get(c, {}).get("is_current", True))
    comm_list = ["ALL"] + current_comms + legacy_comms
    sec_list = ["ALL", "LOADED", "UNLOADED"]

    def _comm_label(c):
        if c == "ALL":
            return "ALL (Port-Wide)"
        status = commodity_status.get(c)
        if status and not status["is_current"]:
            return f"{c} — ⚠ discontinued {status['last_record_month']}"
        return c

    # Filter Controls — Commodity Selector Prominent
    col_c1, col_c2, col_c3 = st.columns([2, 1, 1])
    with col_c1:
        selected_comm = st.selectbox("Select Commodity for Cargo Analytics", comm_list, index=0, format_func=_comm_label)
        if legacy_comms:
            st.caption(f"⚠ {len(legacy_comms)} of {len(all_comms)} commodities only have data through 2021 (dataset switched to consolidated categories in 2023) — marked above.")
    with col_c2:
        selected_sec = st.selectbox("Flow Section", sec_list, format_func=lambda x: {"ALL": "ALL (Loaded & Unloaded)", "LOADED": "LOADED (Exports)", "UNLOADED": "UNLOADED (Imports)"}[x], index=0)
    with col_c3:
        horizon_m = st.selectbox("Forecast Horizon", [3, 6, 12], format_func=lambda x: f"{x} Months", index=1)

    # Fetch Forecast Payload
    fc_data = api_get("/cargo/forecast", {"horizon": horizon_m, "commodity": selected_comm, "section": selected_sec}) or {}
    
    if fc_data and "summary" in fc_data:
        summ = fc_data["summary"]
        chart_data = fc_data.get("chart", {})
        predict_lvl = summ.get("predictability_level", "MEDIUM")
        nmpa_fac = fc_data.get("nmpa_facility", {})
        accuracy_reliable = summ.get("accuracy_reliable", True)

        def _pct(val, decimals=1):
            return "N/A" if val is None else f"{val:.{decimals}f}%"

        def _signed_pct(val, decimals=1):
            return "New activity" if val is None else f"{val:+.{decimals}f}%"

        growth_val = summ.get("forecast_change_pct")

        # Predictability color styling
        pred_color = "#059669" if predict_lvl == "HIGH" else ("#D97706" if predict_lvl == "MEDIUM" else "#DC2626")
        pred_bg = "#F0FDF4" if predict_lvl == "HIGH" else ("#FFFBEB" if predict_lvl == "MEDIUM" else "#FEF2F2")

        data_currency = fc_data.get("data_currency") or {}
        if data_currency.get("is_stale"):
            st.warning(f"⚠️ **Stale/discontinued commodity label:** {data_currency.get('note', '')}")

        # Commodity Snapshot & Detailed Metrics
        comm_name = selected_comm if selected_comm != "ALL" else "All Port Commodities"
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #F3E8D6; border-left: 5px solid #059669; padding: 14px 20px; border-radius: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
          <div>
            <span style="font-size: 11px; font-weight: 800; color: #059669; letter-spacing: 0.5px; text-transform: uppercase;">SELECTED COMMODITY ANALYTICS</span>
            <div style="font-size: 18px; font-weight: 800; color: #1C1917; margin-top: 2px;">{comm_name}</div>
          </div>
          <div style="display: flex; gap: 20px; font-size: 12.5px; color: #4B5563; flex-wrap: wrap;">
            <div><b>Current Volume:</b> {summ.get('current_monthly_volume_tonnes', 0):,.0f} tonnes</div>
            <div><b>Forecast Average:</b> {summ.get('expected_monthly_avg_tonnes', 0):,.0f} tonnes</div>
            <div><b>Expected Growth:</b> <span style="color: {'#059669' if (growth_val is None or growth_val >= 0) else '#DC2626'}; font-weight: 700;">{_signed_pct(growth_val)}</span></div>
            <div><b>Predictability:</b> <span style="font-weight: 700; color: {pred_color};">{predict_lvl}</span></div>
            <div><b>Forecast Accuracy:</b> <b>{_pct(summ.get('model_accuracy_pct'))}</b>{'' if accuracy_reliable else ' <span style="color:#DC2626;font-size:10px;">(unvalidated)</span>'}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # NMPA Facility Banner
        st.markdown(f"""
        <div style="background: #FFFDF9; border: 1px solid #F3E8D6; border-left: 5px solid #F59E0B; padding: 12px 18px; border-radius: 10px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;">
          <div>
            <span style="font-size: 11px; font-weight: 800; color: #92400E; letter-spacing: 0.5px; text-transform: uppercase;">New Mangalore Port Authority (NMPA) Operational Mapping</span>
            <div style="font-size: 15px; font-weight: 800; color: #1C1917; margin-top: 2px;">{nmpa_fac.get('facility_name', 'General Terminal')} ({nmpa_fac.get('berths', 'All Berths')})</div>
            <div style="font-size: 12px; color: #78716C; margin-top: 2px;"><b>Hinterland Consumer:</b> {nmpa_fac.get('hinterland_consumer', 'Regional Trade')} | <b>Primary Flow:</b> {nmpa_fac.get('primary_flow', 'LOADED/UNLOADED')}</div>
          </div>
          <div style="text-align: right; background: #FEF3C7; padding: 6px 14px; border-radius: 8px; border: 1px solid #FDE68A;">
            <div style="font-size: 10px; font-weight: 700; color: #92400E;">BERTH DRAFT DEPTH</div>
            <div style="font-size: 16px; font-weight: 800; color: #78350F;">{nmpa_fac.get('max_draft_m', 13.5)} Meters</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # KPI Metric Cards
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Current Monthly Volume", f"{summ.get('current_monthly_volume_tonnes', 0):,.0f} Tonnes")
        m2.metric("Expected Monthly Avg", f"{summ.get('expected_monthly_avg_tonnes', 0):,.0f} Tonnes", _signed_pct(growth_val))
        m3.metric("Forecast Trend", summ.get("trend_signal", "Neutral"))
        m4.metric("Predictability Level", predict_lvl, delta=f"WAPE {_pct(summ.get('model_wape_pct'))}", delta_color="normal")
        m5.metric("Model Accuracy (WAPE)", _pct(summ.get('model_accuracy_pct')), "Target 85%+" if accuracy_reliable else "Unvalidated — see warning above")

        st.markdown("<br>", unsafe_allow_html=True)
        col_chart, col_side = st.columns([3, 1])

        with col_chart:
            # Main Forecast Plotly Chart with Dynamic 95% Confidence Band
            fig_fc = go.Figure()
            # Historical Cargo (Tonnes)
            fig_fc.add_trace(go.Scatter(
                x=chart_data.get("history_months", []), y=chart_data.get("history_values", []),
                name="Historical Cargo (Tonnes)", line=dict(color="#4B5563", width=2.5),
                mode="lines+markers", marker=dict(size=4)
            ))
            # 95% Dynamic Prediction Interval
            fore_m = chart_data.get("forecast_months", [])
            low_b = chart_data.get("lower_bounds", [])
            up_b = chart_data.get("upper_bounds", [])
            if fore_m and low_b and up_b:
                fig_fc.add_trace(go.Scatter(
                    x=fore_m + fore_m[::-1],
                    y=up_b + low_b[::-1],
                    fill="toself", fillcolor="rgba(245,158,11,0.12)",
                    line=dict(color="rgba(0,0,0,0)"), name="95% Dynamic Prediction Interval", showlegend=True
                ))
            # Predicted Cargo
            fig_fc.add_trace(go.Scatter(
                x=fore_m, y=chart_data.get("forecast_values", []),
                name="Predicted Cargo", line=dict(color=GOLD, width=3, dash="dash"),
                mode="lines+markers", marker=dict(size=7, color=GOLD)
            ))

            title_str = f"Cargo Volume Forecast — {selected_comm} — {horizon_m} Month Horizon"
            fig_fc.update_layout(**PLOTLY_THEME, height=400, title=title_str,
                                  xaxis_title="Month", yaxis_title="Cargo Volume (Tonnes)",
                                  legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_fc, use_container_width=True)

        with col_side:
            # Predictability & Stats Panel
            st.markdown(f"""
            <div class="panel" style="background: {pred_bg}; border: 1px solid {pred_color};">
              <div class="panel-title" style="color: {pred_color};">Predictability Score: {predict_lvl}</div>
              <p style="font-size: 13px; color: #4B5563; margin-top: 8px;">
                {summ.get('predictability_desc', '')}
              </p>
              <hr style="margin: 12px 0; border-color: #F3E8D6;">
              <div style="font-size: 12px;">
                <div><b>Total Horizon Cargo:</b> {summ.get('total_expected_horizon_tonnes', 0):,.0f} Tonnes</div>
                <div style="margin-top: 6px;"><b>Model Error (WAPE):</b> {_pct(summ.get('model_wape_pct'), 2)}</div>
                <div style="margin-top: 6px;"><b>Target Metric:</b> Weighted Absolute % Error</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Data Quality Panel
            dq = fc_data.get("data_quality", {})
            st.markdown(f"""
            <div class="panel" style="margin-top: 14px;">
              <div class="panel-title">Data Lineage & Quality</div>
              <div style="font-size: 12px; color: #4B5563; margin-top: 8px;">
                <div><b>Dataset:</b> Actual Port Cargo Records</div>
                <div><b>Completeness:</b> {dq.get('completeness_pct', 98.4)}%</div>
                <div><b>Time Range:</b> {dq.get('historical_span', '2021-01 to 2026-07')}</div>
                <div><b>Records Analyzed:</b> {dq.get('total_records_analyzed', 0)}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Forecast Drivers (Explainability) & Operational Recommendations ──
        st.markdown("---")
        col_drv, col_rec = st.columns([1, 1])

        with col_drv:
            st.markdown('<div class="panel"><div class="panel-title">Explainable Forecast Drivers (WHY this prediction?)</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size: 12px; color: #78716C; margin-bottom: 12px; font-weight: 500;"><b>Cargo Forecast Query:</b> Why is cargo volume expected to change? Key contributing operational & market drivers:</div>', unsafe_allow_html=True)
            drivers = fc_data.get("drivers", [])
            for d in drivers:
                dir_icon = "▲" if d.get("direction") == "UP" else ("▼" if d.get("direction") == "DOWN" else "●")
                dir_color = "#059669" if d.get("direction") == "UP" else ("#DC2626" if d.get("direction") == "DOWN" else "#D97706")
                st.markdown(f"""
                <div style="background: #FAFAF9; padding: 10px 14px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid {dir_color};">
                  <div style="display: flex; justify-content: space-between; font-size: 13px; font-weight: 700;">
                    <span>{d['factor']}</span>
                    <span style="color: {dir_color};">{dir_icon} {d['impact']}</span>
                  </div>
                  <div style="font-size: 12px; color: #6B7280; margin-top: 4px;">{d['explanation']} (Weight: {d['weight_pct']}%)</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_rec:
            st.markdown('<div class="panel"><div class="panel-title">AI Operational Recommendations</div>', unsafe_allow_html=True)
            recs = fc_data.get("operational_recommendations", [])
            for r in recs:
                prio = r.get("priority", "MEDIUM")
                prio_color = "#DC2626" if prio == "HIGH" else ("#D97706" if prio == "MEDIUM" else "#059669")
                st.markdown(f"""
                <div style="background: #FFFDF9; border: 1px solid #F3E8D6; padding: 12px 14px; border-radius: 8px; margin-bottom: 10px;">
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 12px; font-weight: 800; color: #1C1917;">{r.get('category', 'Operations')}</span>
                    <span style="background: {prio_color}22; color: {prio_color}; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 12px;">{prio}</span>
                  </div>
                  <div style="font-size: 13px; font-weight: 600; color: #292524; margin-top: 4px;">{r['recommendation']}</div>
                  <div style="font-size: 12px; color: #78716C; margin-top: 4px;"><b>Action:</b> {r['action']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Cargo Forecast Model Validation ──
        st.markdown("---")
        st.markdown("**Cargo Forecast Model Validation (Baseline vs Primary ML Model)**")
        eval_data = api_get("/cargo/accuracy", {"commodity": selected_comm, "section": selected_sec}) or {}
        if eval_data.get("models"):
            models_list = eval_data["models"]
            col_b1, col_b2 = st.columns([3, 2])
            with col_b1:
                test_dates = eval_data.get("test_dates", [])
                actual_v = eval_data.get("actual_test_volumes", [])
                bm_v = models_list[0].get("predicted_volumes", [])
                ml_v = models_list[1].get("predicted_volumes", [])
                
                fig_comp = go.Figure()
                fig_comp.add_trace(go.Scatter(x=test_dates, y=actual_v, name="Actual Cargo Test Data", line=dict(color="#1F2937", width=3), mode="lines+markers"))
                fig_comp.add_trace(go.Scatter(x=test_dates, y=bm_v, name="Baseline Model (Seasonal Naive)", line=dict(color="#9CA3AF", width=2, dash="dot"), mode="lines"))
                fig_comp.add_trace(go.Scatter(x=test_dates, y=ml_v, name="Primary ML Cargo Forecast Model", line=dict(color=GOLD, width=2.5, dash="dash"), mode="lines+markers"))
                fig_comp.update_layout(**PLOTLY_THEME, height=320, title="Chronological Backtesting Validation on Historical Cargo Records",
                                       xaxis_title="Test Month", yaxis_title="Cargo Volume (Tonnes)", legend=dict(orientation="h", y=-0.25))
                st.plotly_chart(fig_comp, use_container_width=True)

            with col_b2:
                rows_metrics = []
                for m in models_list:
                    met = m["metrics"]
                    rows_metrics.append({
                        "Model Name": m["model_name"],
                        "Status": m["status"],
                        "WAPE %": f"{met['wape_pct']}%",
                        "MAPE %": f"{met['mape_pct']}%",
                        "MAE": f"{met['mae_tonnes']:,.0f}",
                        "RMSE": f"{met['rmse_tonnes']:,.0f}",
                        "Accuracy": f"{met['accuracy_score_pct']}%",
                    })
                st.dataframe(pd.DataFrame(rows_metrics), use_container_width=True, hide_index=True)
                st.info(eval_data.get("recommended_metric_explanation", "WAPE evaluates cargo predictability cleanly without division-by-zero artifacts."))
        else:
            st.info(
                f"No backtest available for **{selected_comm} / {selected_sec}** — "
                f"{eval_data.get('error', 'insufficient historical periods (fewer than 12 months of data)')}. "
                "The forecast above is unvalidated model extrapolation, not a measured-accuracy prediction."
            )

        # ── Interactive What-If Cargo Scenario Simulator ──
        st.markdown("---")
        st.markdown('<div class="panel"><div class="panel-title">Interactive What-If Cargo Scenario Simulator</div>', unsafe_allow_html=True)
        st.markdown("<div style='font-size: 13px; color: #6B7280; margin-bottom: 14px;'><b>Objective:</b> How will changing operational conditions affect future cargo throughput? Simulate vessel arrival shifts, trade demand changes, and weather delays.</div>", unsafe_allow_html=True)

        sc_col1, sc_col2, sc_col3 = st.columns(3)
        with sc_col1:
            vessel_shift = st.slider("Vessel Arrival Change (%)", min_value=-50, max_value=50, value=15, step=5, help="Simulates vessel fleet arrival volume shift impacting cargo")
        with sc_col2:
            demand_shift = st.slider("Trade Demand Shift (%)", min_value=-50, max_value=50, value=10, step=5, help="Simulates macro trade demand changes")
        with sc_col3:
            weather_delay = st.slider("Weather Delay (Days)", min_value=0, max_value=7, value=1, step=1, help="Simulates port operational slowdown from monsoon/weather")

        if st.button("Run Cargo Scenario Simulation", type="primary"):
            sim_res = api_post("/cargo/scenario", {
                "commodity": selected_comm,
                "section": selected_sec,
                "vessel_arrival_change_pct": vessel_shift,
                "trade_demand_change_pct": demand_shift,
                "weather_delay_days": weather_delay,
                "horizon_months": horizon_m
            })
            if sim_res and "simulation_summary" in sim_res:
                ss = sim_res["simulation_summary"]
                r1, r2, r3 = st.columns(3)
                r1.metric("Predicted Cargo Throughput", f"{ss['simulated_total_tonnes']:,.0f} Tonnes", f"{ss['volume_delta_pct']:+.1f}% vs Base")
                r2.metric("Net Volume Delta", f"{ss['volume_delta_tonnes']:+,.0f} Tonnes")
                r3.metric("Capacity Stress Level", ss["capacity_risk_level"])

                # Plotly Chart comparing Baseline vs Simulated Scenario
                sim_series = sim_res.get("series", [])
                if sim_series:
                    months_sim = [s["month"] for s in sim_series]
                    base_sim = [s["baseline_tonnes"] for s in sim_series]
                    scen_sim = [s["simulated_tonnes"] for s in sim_series]

                    fig_sim = go.Figure()
                    fig_sim.add_trace(go.Scatter(x=months_sim, y=base_sim, name="Baseline Forecast", line=dict(color="#6B7280", width=2)))
                    fig_sim.add_trace(go.Scatter(x=months_sim, y=scen_sim, name="Simulated Scenario Forecast", line=dict(color="#EF4444" if ss['volume_delta_pct'] < 0 else GOLD, width=3, dash="dash"), mode="lines+markers"))
                    fig_sim.update_layout(**PLOTLY_THEME, height=300, title="Predicted Cargo Throughput — Baseline vs Simulated Scenario", xaxis_title="Month", yaxis_title="Cargo Volume (Tonnes)")
                    st.plotly_chart(fig_sim, use_container_width=True)

                # Advisories
                for adv in sim_res.get("simulated_operational_advisories", []):
                    st.warning(adv)

    else:
        st.error("Unable to load cargo forecast payload from backend API.")

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — TRADE INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">Commodity Demand by Trade Lane</span>
      <span class="sec-tag">Module 3 — Trade & Commodity Demand</span>
      <div class="sec-sub">Trade lane momentum, commodity demand forecasting, historical trade lane volumes and growth metrics supporting cargo prediction.</div>
    </div>""", unsafe_allow_html=True)

    lanes_data = api_get("/trade/lanes") or {"lanes": []}
    prices_data = api_get("/trade/commodity-prices") or {"prices": []}
    opps_data = api_get("/trade/opportunities") or {"opportunities": []}
    lanes = lanes_data.get("lanes", [])
    prices = prices_data.get("prices", [])
    opps = opps_data.get("opportunities", [])

    col_l, col_r = st.columns([3, 2])
    with col_l:
        if lanes:
            df_lanes = pd.DataFrame(lanes)
            df_lanes["Direction"] = df_lanes["growth_pct"].apply(lambda x: "Growing" if x > 0 else "Declining")
            fig_lanes = px.bar(df_lanes.sort_values("growth_pct"), x="growth_pct", y="route",
                               orientation="h", color="Direction",
                               color_discrete_map={"Growing": "#059669", "Declining": "#DC2626"},
                               title="Commodity Demand by Trade Lane — Growth / Decline (YoY %)",
                               labels={"growth_pct": "Growth %", "route": ""},
                               text="growth_pct")
            fig_lanes.update_traces(texttemplate="%{text:+.1f}%", textposition="outside")
            fig_lanes.add_vline(x=0, line_color="#1C1917", line_width=1)
            fig_lanes.update_layout(**PLOTLY_THEME, height=400)
            st.plotly_chart(fig_lanes, use_container_width=True)

            st.markdown('<div class="panel"><div class="panel-title">Commodity Demand & Route Flow Details</div>', unsafe_allow_html=True)
            df_show_lanes = df_lanes[["route", "commodity", "volume_mt", "growth_pct", "vessels_month"]].copy()
            df_show_lanes.columns = ["Trade Route", "Commodity", "Volume (MT)", "Growth %", "Vessels/Month"]
            st.dataframe(df_show_lanes, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        # Commodity Prices
        if prices:
            st.markdown('<div class="panel"><div class="panel-title">Commodity Price Indices</div>', unsafe_allow_html=True)
            for p in prices:
                color = "#059669" if p["trend"] == "up" else "#DC2626"
                arrow = "▲" if p["trend"] == "up" else "▼"
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #FEF3C7;">
                  <div>
                    <div style="font-size:12px;font-weight:700;color:#1C1917;">{p['commodity']}</div>
                    <div style="font-size:10px;color:#78716C;">{p['index']}</div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-size:15px;font-weight:800;font-family:system-ui,sans-serif;color:#1C1917;">${p['price_usd']:,.2f}</div>
                    <div style="font-size:11px;color:{color};font-weight:600;">{arrow} {abs(p['change_30d']):.1f}% (30d)</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Price trend chart for top commodity
            p_sel = prices[0]
            fig_price = go.Figure(go.Scatter(
                x=p_sel["series_dates"], y=p_sel["series_values"],
                fill="tozeroy", fillcolor="rgba(245,158,11,0.1)",
                line=dict(color=GOLD, width=2),
                name=p_sel["commodity"],
            ))
            fig_price.update_layout(**PLOTLY_THEME, height=220,
                                     title=f"{p_sel['commodity']} — 30-Day Price Trend (USD)",
                                     yaxis_title="USD")
            st.plotly_chart(fig_price, use_container_width=True)

    # Market Opportunities
    st.markdown("---")
    st.markdown("""<div class="sec-header" style="margin-top:0">
      <span class="sec-title" style="font-size:18px">Commodity Trade Opportunities</span>
      <span class="sec-tag">AI Ranked</span>
    </div>""", unsafe_allow_html=True)
    cols_opp = st.columns(2)
    for i, opp in enumerate(opps):
        with cols_opp[i % 2]:
            conf_pct = int(opp['confidence'] * 100)
            st.markdown(f"""
            <div class="opp-card">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                <div class="opp-rank">#{opp['rank']}</div>
                <div>
                  <div class="opp-commodity">{opp['commodity']}</div>
                  <div class="opp-route">{opp['route']}</div>
                </div>
              </div>
              <div class="opp-opportunity">{opp['opportunity']}</div>
              <div class="opp-metrics">
                <div><div class="opp-revenue">₹{opp['revenue_potential_cr']} Cr</div><div style="font-size:10px;color:#78716C;">Revenue Potential</div></div>
                <div><div class="opp-revenue" style="color:{GOLD};">{conf_pct}%</div><div style="font-size:10px;color:#78716C;">Confidence</div></div>
                <div><div style="font-size:13px;font-weight:700;color:#2563EB;">{opp['time_horizon']}</div><div style="font-size:10px;color:#78716C;">Time Horizon</div></div>
              </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — ANOMALY DETECTION
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">Cargo Anomaly & Risk Intelligence</span>
      <span class="sec-tag">Module 4 — Risk & Anomaly Engine</span>
      <div class="sec-sub">Multi-algorithm detection of cargo volume surges, volume decline anomalies, commodity movement deviations, and operational disruptions.</div>
    </div>
    
    <!-- Severity Scale Indicator -->
    <div style="background: #FFFDF9; border: 1px solid #F3E8D6; border-radius: 10px; padding: 12px 18px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
      <div style="font-size: 13px; font-weight: 700; color: #1C1917;">Cargo Risk Severity Progression:</div>
      <div style="display: flex; gap: 12px; font-size: 12px; font-weight: 700; flex-wrap: wrap;">
        <span style="background: #F0FDF4; color: #059669; border: 1px solid #DCFCE7; padding: 4px 12px; border-radius: 12px;">● Normal Operation</span>
        <span style="background: #EFF6FF; color: #2563EB; border: 1px solid #DBEAFE; padding: 4px 12px; border-radius: 12px;">▲ Low / Medium Risk</span>
        <span style="background: #FFFBEB; color: #D97706; border: 1px solid #FEF3C7; padding: 4px 12px; border-radius: 12px;">▲ High Risk Warning</span>
        <span style="background: #FEF2F2; color: #DC2626; border: 1px solid #FEE2E2; padding: 4px 12px; border-radius: 12px;">⚡ Critical Anomaly</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    anom_data = api_get("/anomaly/events") or {"events": []}
    hist_data = api_get("/anomaly/history") or {"history": {}}
    anom_events = anom_data.get("events", [])
    anom_hist = hist_data.get("history", {})

    c1, c2, c3, c4 = st.columns(4)
    sev_counts = {}
    for e in anom_events:
        sev_counts[e["severity"]] = sev_counts.get(e["severity"], 0) + 1
    c1.metric("Critical Anomalies", sev_counts.get("Critical", 0))
    c2.metric("High Severity", sev_counts.get("High", 0))
    c3.metric("Medium Severity", sev_counts.get("Medium", 0))
    c4.metric("Low Severity", sev_counts.get("Low", 0))

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 3])

    with col_l:
        st.markdown('<div class="panel"><div class="panel-title">Active Anomaly Events</div>', unsafe_allow_html=True)
        for ev in anom_events:
            sev = ev["severity"]
            css_cls = f"alert-{sev.lower()}"
            badge_cls = f"badge-{sev[:4].lower()}"
            ts_str = ev["timestamp"][:16].replace("T", "  ")
            st.markdown(f"""
            <div class="alert-card {css_cls}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div class="alert-title">{ev['event_id']} — {ev['type']}</div>
                <span class="badge {badge_cls}">{sev}</span>
              </div>
              <div class="alert-desc">{ev['description']}</div>
              <div class="alert-meta">
                <span><b>Commodity:</b> {ev['commodity']}</span>
                <span><b>Algorithm:</b> {ev['algorithm']}</span>
                <span><b>Confidence:</b> {int(ev['confidence']*100)}%</span>
                <span><b>Time:</b> {ts_str}</span>
              </div>
              <div style="margin-top:8px;font-size:11px;color:#92400E;background:rgba(245,158,11,0.08);padding:6px 10px;border-radius:6px;">
                <b>Action:</b> {ev['recommended_action']}
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        if anom_hist:
            fig_hist = go.Figure()
            sev_order = ["Critical", "High", "Medium", "Low"]
            sev_colors_list = ["#DC2626", "#D97706", "#2563EB", "#059669"]
            dates = []
            for sev, color in zip(sev_order, sev_colors_list):
                if sev in anom_hist:
                    dates = anom_hist[sev]["dates"]
                    fig_hist.add_trace(go.Bar(
                        x=dates, y=anom_hist[sev]["counts"],
                        name=sev, marker_color=color, opacity=0.85
                    ))
            fig_hist.update_layout(**PLOTLY_THEME, height=300, barmode="stack",
                                    title="30-Day Anomaly Frequency by Severity",
                                    xaxis_title="Date", yaxis_title="Event Count",
                                    legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_hist, use_container_width=True)

        # Algorithm Legend
        st.markdown("""
        <div class="panel">
          <div class="panel-title">Detection Algorithms</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;padding:12px;">
              <div style="display:flex;justify-content:space-between;"><span style="font-weight:700;font-size:13px;color:#166534;">Isolation Forest</span><span style="font-size:9px;font-weight:800;color:#166534;background:#DCFCE7;padding:2px 6px;border-radius:8px;">ACTIVE — scikit-learn</span></div>
              <div style="font-size:11px;color:#78716C;margin-top:4px;">Trained live on data/port_cargo_monthly.csv — flags real outlier months per commodity, not simulated.</div>
            </div>
            <div style="background:#F5F5F4;border:1px solid #E7E5E4;border-radius:8px;padding:12px;">
              <div style="display:flex;justify-content:space-between;"><span style="font-weight:700;font-size:13px;color:#78716C;">LSTM Anomaly Detection</span><span style="font-size:9px;font-weight:800;color:#78716C;background:#E7E5E4;padding:2px 6px;border-radius:8px;">ROADMAP</span></div>
              <div style="font-size:11px;color:#A8A29E;margin-top:4px;">Not yet implemented — would need daily/hourly sequence data, not present in the monthly dataset.</div>
            </div>
            <div style="background:#F5F5F4;border:1px solid #E7E5E4;border-radius:8px;padding:12px;">
              <div style="display:flex;justify-content:space-between;"><span style="font-weight:700;font-size:13px;color:#78716C;">Autoencoder</span><span style="font-size:9px;font-weight:800;color:#78716C;background:#E7E5E4;padding:2px 6px;border-radius:8px;">ROADMAP</span></div>
              <div style="font-size:11px;color:#A8A29E;margin-top:4px;">Not yet implemented.</div>
            </div>
            <div style="background:#F5F5F4;border:1px solid #E7E5E4;border-radius:8px;padding:12px;">
              <div style="display:flex;justify-content:space-between;"><span style="font-weight:700;font-size:13px;color:#78716C;">Transformer Detector</span><span style="font-size:9px;font-weight:800;color:#78716C;background:#E7E5E4;padding:2px 6px;border-radius:8px;">ROADMAP</span></div>
              <div style="font-size:11px;color:#A8A29E;margin-top:4px;">Not yet implemented.</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    # ── Congestion Risk Classifier (RandomForestClassifier, real ML) ──
    st.markdown("---")
    cong = api_get("/forecast/congestion") or {}
    if cong.get("engine"):
        st.markdown('<div class="panel"><div class="panel-title">Port Congestion Risk Classifier (ML)</div>', unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:12px;color:#78716C;margin-bottom:12px;'>{cong.get('model', '')} — "
            f"backtested accuracy <b>{cong.get('model_accuracy_pct', 0)}%</b> "
            f"(F1 {cong.get('model_f1_macro', 0)}) on held-out months from data/port_cargo_monthly.csv.</div>",
            unsafe_allow_html=True
        )
        cc1, cc2, cc3 = st.columns(3)
        cc1.metric("Current Risk Level", cong.get("risk_level", "—").upper(), f"Score {cong.get('current_risk_score', 0)}/10")
        cc2.metric("Anomalies (last 3 real months)", cong.get("anomalies_detected", 0))
        cc3.metric("Peak Risk Month (forecast)", cong.get("peak_congestion_month", "—"), f"Score {cong.get('peak_congestion_score', 0)}/10")

        traj = cong.get("forecast_risk_trajectory", [])
        if traj:
            fig_cong = go.Figure(go.Bar(
                x=[t["month"] for t in traj], y=[t["risk_score"] for t in traj],
                marker_color=[{"HIGH": "#DC2626", "MODERATE": "#D97706", "LOW": "#059669"}.get(t["risk_tier"], "#78716C") for t in traj],
                text=[t["risk_tier"] for t in traj], textposition="outside",
            ))
            fig_cong.update_layout(**PLOTLY_THEME, height=260, title="Projected Congestion Risk (chained from cargo forecast)",
                                    xaxis_title="Month", yaxis_title="Risk Score (0-10)")
            fig_cong.update_yaxes(range=[0, 11])
            st.plotly_chart(fig_cong, use_container_width=True)

        prs = cong.get("port_risk_scores", {})
        if prs:
            st.markdown("<div style='font-size:12px;color:#78716C;margin-top:4px;'><b>Per-facility risk (data-derived vessel percentile):</b> "
                        + " &nbsp;|&nbsp; ".join(f"{k.replace('_',' ')}: {v}/10" for k, v in prs.items())
                        + "</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — INCENTIVE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">Trade Incentive Recommendation Engine</span>
      <span class="sec-tag">Module 5</span>
      <div class="sec-sub">RL-based policy optimization, Monte Carlo simulation, revenue maximization — proactive trade incentives</div>
    </div>""", unsafe_allow_html=True)

    recs_data = api_get("/incentive/recommendations") or {"recommendations": []}
    recs = recs_data.get("recommendations", [])

    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown('<div class="panel"><div class="panel-title">AI Recommendations — Priority Ranked</div>', unsafe_allow_html=True)
        priority_colors = {"High": "#DC2626", "Medium": "#D97706", "Strategic": "#7C3AED"}
        for r in recs:
            pcolor = priority_colors.get(r["priority"], "#78716C")
            conf_pct = int(r["confidence"] * 100)
            st.markdown(f"""
            <div class="rec-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div class="rec-action">{r['rec_id']}: {r['action']}</div>
                <span class="badge" style="background:rgba(0,0,0,0.05);color:{pcolor};border:1px solid {pcolor}30;">{r['priority']}</span>
              </div>
              <div class="rec-rationale">{r['rationale']}</div>
              <div style="font-size:11px;background:#FFFBEB;border:1px solid #FDE68A;border-radius:6px;padding:6px 10px;margin:8px 0;color:#78716C;">
                <b>Current:</b> {r['current_metric']}
              </div>
              <div class="rec-impacts">
                <div><div class="rec-impact-pos">Traffic: {r['predicted_traffic_impact']}</div></div>
                <div><div class="rec-impact-pos">Revenue: {r['predicted_revenue_impact']}</div></div>
                <div><div style="font-size:13px;font-weight:700;color:{GOLD};">{conf_pct}% confidence</div></div>
              </div>
              <div class="rec-meta">
                <span><b>Method:</b> {r['method']}</span>
                <span><b>Implementation:</b> {r['implementation_weeks']} weeks</span>
              </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown("**Monte Carlo Policy Simulator**")
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        charge_delta = st.slider("Handling Charge Change (%)", min_value=-15.0, max_value=5.0, value=-5.0, step=0.5)
        incentive_pct = st.slider("Incentive Rate Offered (%)", min_value=0.0, max_value=15.0, value=8.0, step=0.5)
        scenario_name = st.selectbox("Scenario Type", ["container_charge", "lng_priority", "coal_volume", "auto_terminal"])

        if st.button("Run Monte Carlo Simulation (1000 iterations)"):
            with st.spinner("Running Monte Carlo..."):
                mc_result = api_post("/incentive/monte-carlo", {
                    "scenario": scenario_name,
                    "charge_delta": charge_delta,
                    "incentive_pct": incentive_pct
                })
                if mc_result and "samples" in mc_result:
                    st.markdown("**Revenue Distribution (₹ Cr)**")
                    fig_mc = go.Figure()
                    fig_mc.add_trace(go.Histogram(
                        x=mc_result["samples"], nbinsx=30,
                        marker_color=GOLD, opacity=0.8, name="Revenue Distribution"
                    ))
                    fig_mc.add_vline(x=mc_result["p50"], line_dash="dash", line_color="#DC2626",
                                     annotation_text=f"P50: ₹{mc_result['p50']} Cr")
                    fig_mc.add_vline(x=mc_result["mean"], line_dash="dot", line_color="#059669",
                                     annotation_text=f"Mean: ₹{mc_result['mean']} Cr")
                    fig_mc.update_layout(**PLOTLY_THEME, height=260,
                                         title="Monte Carlo Revenue Distribution",
                                         xaxis_title="Revenue (₹ Cr)", yaxis_title="Frequency")
                    st.plotly_chart(fig_mc, use_container_width=True)

                    c1, c2, c3 = st.columns(3)
                    c1.metric("P10 (Conservative)", f"₹{mc_result['p10']} Cr")
                    c2.metric("P50 (Median)", f"₹{mc_result['p50']} Cr")
                    c3.metric("P90 (Optimistic)", f"₹{mc_result['p90']} Cr")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 7 — DIGITAL TWIN
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">Digital Twin Simulator</span>
      <span class="sec-tag">Module 6</span>
      <div class="sec-sub">Virtual port environment — what-if scenarios for cargo, vessels, weather, and policy changes</div>
    </div>""", unsafe_allow_html=True)

    scenario_map = {
        "Cargo Surge +20%": "cargo_surge",
        "Vessel Delay Increase": "vessel_delay",
        "Trade Incentive Policy": "incentive_change",
        "Weather Disruption (Cyclone)": "weather_disruption",
    }
    sel_label = st.selectbox("Select Scenario", list(scenario_map.keys()))
    sel_key = scenario_map[sel_label]

    twin_data = api_get(f"/twin/scenario/{sel_key}") or {}
    result = twin_data.get("result", {})
    mc_data = twin_data.get("monte_carlo", {})

    if result:
        risk = result.get("risk_level", "Medium")
        risk_color = {"Low": "#059669", "Medium": "#D97706", "High": "#DC2626", "Critical": "#7C3AED"}.get(risk, "#78716C")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border:1px solid #FDE68A;border-radius:12px;padding:18px 22px;margin-bottom:20px;display:flex;align-items:center;gap:16px;">
          <div style="font-family:system-ui,sans-serif;font-size:18px;font-weight:800;color:#1C1917;">{result.get('name','Scenario')}</div>
          <div style="font-size:13px;color:#78716C;">{result.get('description','')}</div>
          <div style="margin-left:auto;background:{risk_color}15;border:1px solid {risk_color}40;color:{risk_color};padding:5px 14px;border-radius:16px;font-size:11px;font-weight:700;">Risk: {risk}</div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Congestion Index", f"{result.get('congestion_index',0):.2f}", result.get("congestion_delta", ""))
        c2.metric("Berth Utilization", f"{result.get('berth_utilization_pct',0):.1f}%", result.get("berth_delta", ""))
        c3.metric("Storage Utilization", f"{result.get('storage_utilization_pct',0):.1f}%", result.get("storage_delta", ""))
        c4.metric("Expected Revenue", f"₹{result.get('expected_revenue_cr',0):.1f} Cr", result.get("revenue_delta", ""))

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns(2)

        with col_l:
            categories = ["Congestion", "Berth Util", "Storage Util", "Revenue"]
            baseline_vals = [0.63, 72.4, 65.0, 100.0]
            scenario_vals = [
                result.get("congestion_index", 0.63) * 100,
                result.get("berth_utilization_pct", 72.4),
                result.get("storage_utilization_pct", 65.0),
                result.get("expected_revenue_cr", 100.0) / 1.2,
            ]
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=baseline_vals, theta=categories, fill="toself",
                                                  name="Baseline", line_color="#78716C", fillcolor="rgba(120,113,108,0.1)"))
            fig_radar.add_trace(go.Scatterpolar(r=scenario_vals, theta=categories, fill="toself",
                                                  name=sel_label, line_color=GOLD, fillcolor="rgba(245,158,11,0.15)"))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 120])),
                                     paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter"),
                                     height=320, showlegend=True, title="Scenario vs Baseline Comparison",
                                     legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_r:
            add_cranes = result.get("additional_cranes_needed", 0)
            add_workforce = result.get("additional_workforce", 0)
            wf_color = "#DC2626" if add_workforce < 0 else "#059669"
            st.markdown(f"""
            <div class="panel">
              <div class="panel-title">Operational Impact Assessment</div>
              <div style="display:grid;gap:12px;">
                <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;padding:14px;">
                  <div style="font-size:11px;color:#78716C;text-transform:uppercase;letter-spacing:0.6px;">Additional Cranes Required</div>
                  <div style="font-size:28px;font-weight:800;font-family:system-ui,sans-serif;color:#1C1917;">{add_cranes}</div>
                </div>
                <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;padding:14px;">
                  <div style="font-size:11px;color:#78716C;text-transform:uppercase;letter-spacing:0.6px;">Workforce Delta</div>
                  <div style="font-size:28px;font-weight:800;font-family:system-ui,sans-serif;color:{wf_color};">{add_workforce:+d}</div>
                </div>
                <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;padding:14px;">
                  <div style="font-size:11px;color:#78716C;text-transform:uppercase;letter-spacing:0.6px;">Risk Classification</div>
                  <div style="font-size:20px;font-weight:800;font-family:system-ui,sans-serif;color:{risk_color};">{risk}</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

        # Berth utilization comparison
        berths = api_get("/twin/berths") or {"berths": []}
        berths = berths.get("berths", [])
        if berths:
            df_b = pd.DataFrame(berths)
            import random as _rnd
            _rnd.seed(42)
            delta = float(result.get("berth_delta", "+0%").replace("%", ""))
            df_b["simulated_pct"] = df_b["utilization_pct"].apply(lambda x: min(100, x * (1 + delta / 100) + _rnd.gauss(0, 2)))
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(x=df_b["berth_id"], y=df_b["utilization_pct"],
                                       name="Baseline", marker_color="#D1D5DB"))
            fig_comp.add_trace(go.Bar(x=df_b["berth_id"], y=df_b["simulated_pct"],
                                       name=f"Simulated: {sel_label}", marker_color=GOLD, opacity=0.85))
            fig_comp.update_layout(**PLOTLY_THEME, barmode="group", height=280,
                                    title="Berth Utilization — Baseline vs Simulated")
            fig_comp.update_yaxes(range=[0, 110])
            st.plotly_chart(fig_comp, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 8 — AI MARITIME COPILOT
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">AI Maritime Copilot</span>
      <span class="sec-tag">Module 7</span>
      <div class="sec-sub">LangGraph Cognitive Dispatcher — 3-tier fallback: LLM → SLM → Deterministic Zero-LLM</div>
    </div>""", unsafe_allow_html=True)

    # Agent Roster
    agents = [
        ("Forecast Agent", "Cargo volume prediction queries"),
        ("Trade Agent", "Global trade lane & commodity analysis"),
        ("Policy Agent", "Incentive & regulation recommendations"),
        ("Simulation Agent", "Digital twin & what-if scenarios"),
        ("Reporting Agent", "Executive summary generation"),
    ]
    agent_cols = st.columns(5)
    for i, (name, role) in enumerate(agents):
        with agent_cols[i]:
            st.markdown(f"""
            <div style="background:#FFFFFF;border:1px solid #FDE68A;border-top:3px solid #F59E0B;border-radius:10px;padding:12px;text-align:center;">
              <div style="font-family:system-ui,sans-serif;font-size:12px;font-weight:700;color:#1C1917;">{name}</div>
              <div style="font-size:10px;color:#78716C;margin-top:4px;">{role}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Suggested queries
    sugg_data = api_get("/copilot/suggested-queries") or {"queries": []}
    suggestions = sugg_data.get("queries", [])
    if suggestions:
        st.markdown("**Suggested Queries:**")
        chip_html = "".join([f'<span class="query-chip">{q}</span>' for q in suggestions[:4]])
        st.markdown(chip_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 3])

    with col_l:
        query_input = st.text_area(
            "Ask the Maritime Copilot:",
            placeholder="e.g. Why is cargo forecast decreasing? What incentive should be applied?",
            height=120,
        )

        submit = st.button("Submit Query to Copilot")

        active_query = None
        if submit and query_input.strip():
            active_query = query_input

        # Quick query buttons
        st.markdown("**Or one-click submit a suggested query:**")
        qcols = st.columns(2)
        for i, q in enumerate(suggestions[:4]):
            with qcols[i % 2]:
                if st.button(q[:35] + "..." if len(q) > 35 else q, key=f"qbtn_{i}"):
                    active_query = q

        if active_query:
            with st.spinner("Dispatching through LangGraph..."):
                result = api_post("/copilot/query", {"query": active_query})
                if result:
                    st.session_state["last_copilot"] = result

    with col_r:
        if "last_copilot" in st.session_state:
            cop = st.session_state["last_copilot"]
            trace = cop.get("trace", {})
            response = cop.get("response", {})

            # Dispatch trace
            st.markdown('<div class="panel"><div class="panel-title">LangGraph Dispatch Trace</div>', unsafe_allow_html=True)
            tier_color = {"Tier 1: Heavy Synthesis (LLM)": "#DC2626",
                          "Tier 2: Fast Reasoning (SLM)": "#D97706",
                          "Tier 3: Deterministic Zero-LLM": "#059669"}.get(trace.get("tier", ""), GOLD)
            st.markdown(f"""
            <div style="display:flex;gap:20px;margin-bottom:14px;flex-wrap:wrap;">
              <span class="metric-pill">Complexity: {trace.get('complexity','')}</span>
              <span class="metric-pill" style="color:{tier_color};border-color:{tier_color}40;">Tier: {trace.get('tier','')}</span>
              <span class="metric-pill">Agent: {trace.get('agent','')}</span>
              <span class="metric-pill">Total: {trace.get('total_ms',0)}ms</span>
            </div>""", unsafe_allow_html=True)

            for step in trace.get("trace", []):
                st.markdown(f"""
                <div class="trace-step">
                  <div class="trace-num">{step['step']}</div>
                  <div style="flex:1;">
                    <div class="trace-component">{step['component']}</div>
                    <div class="trace-action">{step['action']}</div>
                    <div class="trace-detail">{step['detail']}</div>
                  </div>
                  <div class="trace-ms">{step['ms']}ms</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Response
            if response:
                confidence_pct = int(response.get("confidence", 0.85) * 100)
                st.markdown(f"""
                <div class="copilot-response">
                  <div style="font-size:11px;color:#78716C;margin-bottom:12px;display:flex;gap:12px;flex-wrap:wrap;">
                    <span><b>Confidence:</b> {confidence_pct}%</span>
                    <span><b>Data Sources:</b> {", ".join(response.get("data_refs", []))}</span>
                  </div>
                  {response.get("answer","").replace(chr(10), "<br>")}
                </div>""", unsafe_allow_html=True)

                followups = response.get("suggested_followups", [])
                if followups:
                    st.markdown("<br>**Follow-up Questions:**")
                    fu_html = "".join([f'<span class="query-chip">{q}</span>' for q in followups])
                    st.markdown(fu_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:#FFFBEB;border:2px dashed #FDE68A;border-radius:12px;padding:40px;text-align:center;color:#78716C;">
              <div style="font-family:system-ui,sans-serif;font-size:18px;font-weight:700;color:#92400E;margin-bottom:8px;">LangGraph Copilot Ready</div>
              <div style="font-size:13px;">Type a query and click Submit to see the 3-tier dispatch trace and AI response.</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 9 — DATA PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<div class="ys-content">', unsafe_allow_html=True)
    st.markdown("""
    <div class="sec-header">
      <span class="sec-title">Synthetic Data Pipeline & Architecture</span>
      <span class="sec-tag">Infrastructure</span>
      <div class="sec-sub">Kafka ingestion → Spark fusion → Data pools → AI readiness — real-time processing metrics</div>
    </div>""", unsafe_allow_html=True)

    pipe_data = api_get("/pipeline/status") or {}
    log_data = api_get("/pipeline/log") or {"events": []}
    kafka = pipe_data.get("kafka", {})
    spark = pipe_data.get("spark", {})
    airflow = pipe_data.get("airflow", {})
    pools = pipe_data.get("data_pools", {})

    # Pipeline flow stages
    stage_cols = st.columns(4)
    stages = [
        ("1. DATA INGESTION", "Internal Port Authority Data\nExternal AIS · Weather · Commodity APIs\nKafka Stream · Airflow Scheduler"),
        ("2. SPATIO-TEMPORAL FUSION", "Spark Streaming (temporal alignment)\nPyTorch Grid Matching (ship + weather)\nSLM Text Processor (PII masking)"),
        ("3. DATA POOLS", "PostgreSQL (master port data)\nTimescaleDB (AIS time-series)\nMilvus / Pinecone (vector embeddings)"),
        ("4. AI ORCHESTRATION", "LangGraph Cognitive Dispatcher\n3-Tier Execution & Fallback\n5 Specialized AI Agents"),
    ]
    for col, (title, desc) in zip(stage_cols, stages):
        with col:
            st.markdown(f"""
            <div class="pipeline-stage">
              <div class="pipeline-stage-title">{title}</div>
              <div class="pipeline-stage-sub">{desc.replace(chr(10), '<br>')}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # System Metrics
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Kafka msg/sec", f"{kafka.get('messages_per_sec',0):,}")
    m2.metric("Consumer Lag", str(kafka.get("consumer_lag", 0)))
    m3.metric("Spark rows/sec", f"{spark.get('rows_per_sec',0):,}")
    m4.metric("Airflow Success", f"{airflow.get('success_rate_pct',0)}%")
    m5.metric("Total Records", f"{pools.get('postgresql_records',0)/1e6:.2f}M")
    m6.metric("Storage (GB)", f"{pools.get('total_storage_gb',0):.1f}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_log, col_pool = st.columns([3, 2])

    with col_log:
        st.markdown('<div class="panel"><div class="panel-title">Live Ingestion Event Log</div>', unsafe_allow_html=True)
        events = log_data.get("events", [])
        rows_html = ""
        for ev in events:
            lvl_class = "log-warn" if ev["level"] == "WARN" else "log-info"
            rows_html += f'<div class="log-row"><span class="log-ts">{ev["timestamp"]}</span><span class="log-src">[{ev["source"]}]</span><span class="{lvl_class}">{ev["message"]}</span></div>'
        st.markdown(f'<div class="log-container">{rows_html}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pool:
        st.markdown('<div class="panel"><div class="panel-title">Data Pool Statistics</div>', unsafe_allow_html=True)
        pool_metrics = [
            ("PostgreSQL", "Relational master data", f"{pools.get('postgresql_records',0):,}", "records"),
            ("TimescaleDB", "AIS time-series", f"{pools.get('timescaledb_records',0)/1e6:.1f}M", "records"),
            ("Milvus Vectors", "Contextual RAG embeddings", f"{pools.get('milvus_vectors',0):,}", "vectors"),
        ]
        for name, desc, val, unit in pool_metrics:
            st.markdown(f"""
            <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;padding:14px;margin-bottom:10px;">
              <div style="font-weight:700;font-size:13px;color:#92400E;">{name}</div>
              <div style="font-size:11px;color:#78716C;margin-bottom:6px;">{desc}</div>
              <div style="font-family:system-ui,sans-serif;font-size:22px;font-weight:800;color:#1C1917;">{val} <span style="font-size:11px;color:#78716C;">{unit}</span></div>
            </div>""", unsafe_allow_html=True)

        uptime_data = [
            ("Kafka", kafka.get("uptime_pct", 99.97)),
            ("Spark", spark.get("uptime_pct", 99.91)),
            ("Airflow", airflow.get("uptime_pct", 99.84)),
        ]
        for svc, pct in uptime_data:
            color = "#059669" if pct >= 99.9 else "#D97706"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #FEF3C7;">
              <span style="font-size:12px;font-weight:600;color:#1C1917;">{svc} Uptime</span>
              <span style="font-size:12px;font-weight:700;color:{color};">{pct}%</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Architecture Diagrams
    st.markdown("---")
    st.markdown("""<div class="sec-header" style="margin-top:0">
      <span class="sec-title" style="font-size:18px">System Architecture Diagrams</span>
    </div>""", unsafe_allow_html=True)

    arch_tabs = st.tabs([
        "LangGraph Dispatcher (Diagram 1)",
        "Data Ingestion & Fusion (Diagram 2)",
        "Backend & Security (Diagram 3)",
        "End-to-End Flow (Diagram 4)",
    ])
    for i, atab in enumerate(arch_tabs):
        with atab:
            img_path = ARCH_DIR / "assets" / f"{i+1}.jpeg"
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            else:
                st.info(f"Architecture diagram {i+1} not found at {img_path}")

    st.markdown('</div>', unsafe_allow_html=True)
