import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER SOMA BLAZE", layout="wide")

# ESTILO VISUAL (DARK MODE E CORES DO RADAR)
st.markdown("""
    <style>
    .main { background-color: #0b0e11; }
    .stApp { background-color: #0b0e11; color: white; }
    .placa-card { background: #1a2026; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 4px solid #333; }
    .sinal-box { background: #161b22; border-radius: 8px; padding: 10px; margin-bottom: 5px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DOS CONTADORES ---
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0

total_acertos = st.session_state.sg + st.session_state.g1

# --- CABEÇALHO: PLACA DE RESULTADOS ---
st.markdown("### 📊 PLACA DE RESULTADOS")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="placa-card" style="border-color: #00ff88;"><b style="color: #00ff88;">SG</b><br><h2>{st.session_state.sg}</h2></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="placa-card" style="border-color: #00d4ff;"><b style="color: #00d4ff;">G1</b><br><h2>{st.session_state.g1}</h2></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="placa-card" style="border-color: #ff4d4d;"><b style="color: #ff4d4d;">LOSS</b><br><h2>{st.session_state.loss}</h2></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="placa-card" style="border-color: #f7b924;"><b style="color: #f7b924;">TOTAL</b><br><h2>{total_acertos}</h2></div>', unsafe_allow_html=True)

st.markdown("---")

col_lista, col_soma = st.columns([2, 1])

with col_lista:
    st.markdown("### 📋 RADAR DE CORES")
    # LISTA DE CORES (Simulando a geração da sua lista)
    cores = [
        {"h": "20:30", "c": "VERMELHO 🔴"},
        {"h": "20:34", "c": "PRETO ⚫"},
        {"h": "20:38", "c": "VERMELHO 🔴"}
    ]
    for s in cores:
        with st.container():
            st.markdown(f'<div class="sinal-box">⏰ {s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            if b1.button(f"SG", key=f"sg_{s['h']}"): 
                st.session_state.sg += 1
                st.rerun()
            if b2.button(f"G1", key=f"g1_{s['h']}"): 
                st.session_state.g1 += 1
                st.rerun()
            if b3.button(f"L", key=f"l_{s['h']}"): 
                st.session_state.loss += 1
                st.rerun()

    st.markdown("### ⚪ LISTA DE BRANCOS")
    brancos = ["20:45", "21:02", "21:15"]
    for b in brancos:
        st.markdown(f'<div class="sinal-box" style="border-left: 5px solid white;">⏰ {b} | BRANCO ⚪</div>', unsafe_allow_html=True)

with col_soma:
    st.markdown("### 🧮 SOMA DAS PEDRAS")
    # Aqui entra a parte visual das somas que o robô identifica
    st.info("Aguardando próxima pedra para calcular soma...")
    st.markdown("""
        - **Última Soma:** 14 (Vermelho)
        - **Padrão Detectado:** Quebra no 2x1
        - **Puxador Ativo:** Número 4 e 12
    """)
    
    if st.button("Zerar Placa"):
        st.session_state.sg = 0
        st.session_state.g1 = 0
        st.session_state.loss = 0
        st.rerun()
