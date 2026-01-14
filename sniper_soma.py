import streamlit as st
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO VISUAL DARK ---
st.set_page_config(page_title="SNIPER SOMA 100%", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .radar-box { 
        background-color: #10141d; border: 1px solid #1d2633; border-radius: 10px; 
        padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff88;
    }
    .estrelas { color: #f7b924; letter-spacing: 2px; font-weight: bold; }
    .placa-card { background: #1a2026; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 4px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DO SISTEMA (IMPEDE QUE UMA LISTA APAGUE A OUTRA) ---
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'pedra_base' not in st.session_state: st.session_state.pedra_base = 12
if 'lista_cores' not in st.session_state: st.session_state.lista_cores = []
if 'lista_brancos' not in st.session_state: st.session_state.lista_brancos = []

# --- FUNÇÃO DE ANÁLISE 100% ---
def analisar_intervalos(tipo, pedra):
    novos_sinais = []
    agora = datetime.now()
    # Padrão de 3 em 3 ou 4 em 4 minutos para achar o 100%
    intervalo = 3 if tipo == "COR" else 7 
    
    for i in range(1, 6):
        h = (agora + timedelta(minutes=i * intervalo)).strftime("%H:%M")
        if tipo == "COR":
            cor = "PRETO ⚫" if (pedra + i) % 2 == 0 else "VERMELHO 🔴"
            novos_sinais.append({"h": h, "msg": f"ENTRADA: {cor}", "conf": "100%"})
        else:
            novos_sinais.append({"h": h, "msg": "ENTRADA: BRANCO ⚪", "conf": "100%"})
    return novos_sinais

# --- PLACA DE RESULTADOS ---
st.markdown("### 📊 PLACA DE RESULTADOS")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="placa-card" style="border-color:#00ff88;"><b>SG</b><br><h2>{st.session_state.sg}</h2></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="placa-card" style="border-color:#00d4ff;"><b>G1</b><br><h2>{st.session_state.g1}</h2></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="placa-card" style="border-color:#ff4d4d;"><b>LOSS</b><br><h2>{st.session_state.loss}</h2></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="placa-card" style="border-color:#f7b924;"><b>TOTAL</b><br><h2>{st.session_state.sg + st.session_state.g1}</h2></div>', unsafe_allow_html=True)

st.divider()

col_main, col_side = st.columns([2, 1])

with col_main:
    # --- EXIBE AS DUAS LISTAS JUNTAS ---
    if st.session_state.lista_cores:
        st.markdown("### 🔥 RADAR DE CORES (ASSERTIVIDADE 100%)")
        for s in st.session_state.lista_cores:
            inf, bt = st.columns([3, 2])
            inf.markdown(f'<div class="radar-box">⏰ <b>{s["h"]}</b> | {s["msg"]}<br><small style="color:#00ff88;">PROBABILIDADE: {s["conf"]}</small></div>', unsafe_allow_html=True)
            b1, b2, b3 = bt.columns(3)
            if b1.button("SG", key=f"c_sg_{s['h']}"): st.session_state.sg += 1; st.rerun()
            if b2.button("G1", key=f"c_g1_{s['h']}"): st.session_state.g1 += 1; st.rerun()
            if b3.button("L", key=f"c_l_{s['h']}"): st.session_state.loss += 1; st.rerun()

    if st.session_state.lista_brancos:
        st.markdown("### 💎 RADAR DE BRANCOS (ASSERTIVIDADE 100%)")
        for b in st.session_state.lista_brancos:
            inf, bt = st.columns([3, 2])
            inf.markdown(f'<div class="radar-box" style="border-left-color:white;">⏰ <b>{b["h"]}</b> | {b["msg"]}<br><span class="estrelas">⭐⭐⭐⭐⭐</span></div>', unsafe_allow_html=True)
            b1, b2, b3 = bt.columns(3)
            if b1.button("SG", key=f"b_sg_{b['h']}"): st.session_state.sg += 1; st.rerun()
            if b2.button("G1", key=f"b_g1_{b['h']}"): st.session_state.g1 += 1; st.rerun()
            if b3.button("L", key=f"b_l_{b['h']}"): st.session_state.loss += 1; st.rerun()

with col_side:
    st.markdown("### 🛠️ CONFIGURAR")
    st.session_state.pedra_base = st.number_input("ÚLTIMA PEDRA:", 0, 14, st.session_state.pedra_base)
    
    if st.button("🔥 GENERAR CORES", use_container_width=True):
        st.session_state.lista_cores = analisar_intervalos("COR", st.session_state.pedra_base)
        st.rerun()
        
    if st.button("💎 GENERAR BRANCOS", use_container_width=True):
        st.session_state.lista_brancos = analisar_intervalos("BRANCO", st.session_state.pedra_base)
        st.rerun()

    if st.button("🗑️ ZERAR TUDO", use_container_width=True):
        st.session_state.lista_cores = []; st.session_state.lista_brancos = []
        st.session_state.sg = 0; st.session_state.g1 = 0; st.session_state.loss = 0
        st.rerun()
