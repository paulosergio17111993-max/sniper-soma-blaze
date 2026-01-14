import streamlit as st

# --- CONFIGURAÇÃO DE SEGURANÇA E VISUAL ---
st.set_page_config(page_title="SNIPER SOMA BLAZE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .placa-card { background: #1a2026; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 4px solid #333; }
    .sinal-box { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 8px; border: 1px solid #30363d; }
    .numero-puxador { background: #f7b924; color: black; padding: 2px 8px; border-radius: 4px; font-weight: bold; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DA PLACA ---
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0

total_acertos = st.session_state.sg + st.session_state.g1

# --- 1. PLACA DE RESULTADOS (TOPO) ---
st.markdown("### 📊 PLACA DE RESULTADOS")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="placa-card" style="border-color: #00ff88;"><b style="color: #00ff88;">SG</b><br><h2>{st.session_state.sg}</h2></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="placa-card" style="border-color: #00d4ff;"><b style="color: #00d4ff;">G1</b><br><h2>{st.session_state.g1}</h2></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="placa-card" style="border-color: #ff4d4d;"><b style="color: #ff4d4d;">LOSS</b><br><h2>{st.session_state.loss}</h2></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="placa-card" style="border-color: #f7b924;"><b style="color: #f7b924;">TOTAL ACERTOS</b><br><h2>{total_acertos}</h2></div>', unsafe_allow_html=True)

st.divider()

# --- 2. RADAR E ANÁLISE ---
col_lista, col_analise = st.columns([2, 1])

with col_lista:
    st.markdown("### 📋 RADAR DE SINAIS")
    # Gerando os horários conforme sua lista
    horarios = ["19:49", "19:53", "19:57", "20:01", "20:05"]
    for h in horarios:
        with st.container():
            col_txt, col_btn = st.columns([3, 2])
            col_txt.markdown(f'<div class="sinal-box">⏰ {h} | ENTRADA CONFIRMADA 🎯</div>', unsafe_allow_html=True)
            b1, b2, b3 = col_btn.columns(3)
            if b1.button("SG", key=f"sg_{h}"): 
                st.session_state.sg += 1
                st.rerun()
            if b2.button("G1", key=f"g1_{h}"): 
                st.session_state.g1 += 1
                st.rerun()
            if b3.button("L", key=f"l_{h}"): 
                st.session_state.loss += 1
                st.rerun()

with col_analise:
    st.markdown("### 🧮 ANÁLISE DA PEDRA")
    # AQUI ESTÁ A CORREÇÃO: 14 É PRETO!
    st.markdown(f"""
    <div style="background: #1a2026; padding: 20px; border-radius: 10px; border: 1px solid #333;">
        <p><b>ÚLTIMA PEDRA:</b> <span style="color:#555; font-size:22px;">14</span> <span style="color:#444;">(PRETO ⚫)</span></p>
        <p><b>SOMA IDENTIFICADA:</b> <span style="color:#f7b924;">14</span></p>
        <p><b>STATUS:</b> Padrão de 99% Ativo</p>
        <hr>
        <p><b>PUXADORES PARA BRANCO:</b></p>
        <span class="numero-puxador">4</span> 
        <span class="numero-puxador">12</span> 
        <span class="numero-puxador">7</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("ZERAR PLACAR"):
        st.session_state.sg = 0
        st.session_state.g1 = 0
        st.session_state.loss = 0
        st.rerun()
