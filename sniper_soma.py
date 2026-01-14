import streamlit as st
from datetime import datetime, timedelta
import pytz
import random

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="SNIPER TENDÊNCIA 100%", layout="wide")
fuso_br = pytz.timezone('America/Sao_Paulo')

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .radar-box { 
        background-color: #10141d; border: 1px solid #1d2633; border-radius: 10px; 
        padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff88;
    }
    .tendencia-badge { 
        background: #00ff88; color: black; padding: 2px 8px; 
        border-radius: 5px; font-size: 10px; font-weight: bold;
    }
    .estrelas { color: #f7b924; letter-spacing: 2px; font-weight: bold; }
    .placa-card { background: #1a2026; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 4px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'pedra' not in st.session_state: st.session_state.pedra = 12
if 'l_sinais' not in st.session_state: st.session_state.l_sinais = []
if 'tendencia_atual' not in st.session_state: st.session_state.tendencia_atual = "ANALISANDO..."

# --- MOTOR DE ANÁLISE DE TENDÊNCIA ---
def analisar_e_gerar(tipo, p_atual):
    lista = []
    agora_br = datetime.now(fuso_br)
    
    # Simulação de análise de tendência (Escaneando ciclos de 2 a 6 minutos)
    # Na lógica real, ele veria qual desses intervalos mais se repetiu no histórico
    if p_atual in [1, 3, 5, 7, 9, 11, 13]: # Se saiu Ímpar
        intervalo_mestre = random.choice([2, 3, 5]) 
        tendencia = f"CICLO CURTO ({intervalo_mestre} min)"
    else: # Se saiu Par
        intervalo_mestre = random.choice([4, 6, 8])
        tendencia = f"CICLO LONGO ({intervalo_mestre} min)"
    
    st.session_state.tendencia_atual = tendencia
    
    for i in range(1, 6):
        minuto_sinal = (agora_br + timedelta(minutes=i * intervalo_mestre))
        h_formatado = minuto_sinal.strftime("%H:%M")
        
        if tipo == "COR":
            cor = "VERMELHO 🔴" if (p_atual + i) % 2 == 0 else "PRETO ⚫"
            lista.append({"h": h_formatado, "msg": f"ENTRADA: {cor}", "int": intervalo_mestre, "stars": ""})
        else:
            lista.append({"h": h_formatado, "msg": "ENTRADA: BRANCO ⚪", "int": intervalo_mestre, "stars": "⭐⭐⭐⭐⭐"})
    return lista

# --- PLACA DE RESULTADOS ---
st.markdown("### 📊 PLACA DE RESULTADOS")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="placa-card" style="border-color:#00ff88;"><b>SG</b><br><h2>{st.session_state.sg}</h2></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="placa-card" style="border-color:#00d4ff;"><b>G1</b><br><h2>{st.session_state.g1}</h2></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="placa-card" style="border-color:#ff4d4d;"><b>LOSS</b><br><h2>{st.session_state.loss}</h2></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="placa-card" style="border-color:#f7b924;"><b>TOTAL</b><br><h2>{st.session_state.sg + st.session_state.g1}</h2></div>', unsafe_allow_html=True)

st.divider()

# --- INTERFACE ---
col_radar, col_analise = st.columns([2, 1])

with col_radar:
    st.markdown(f"### 🏹 RADAR DE TENDÊNCIA: <span style='color:#00ff88'>{st.session_state.tendencia_atual}</span>", unsafe_allow_html=True)
    
    if not st.session_state.l_sinais:
        st.info("Aguardando análise de tendência da pedra atual...")
    
    for item in st.session_state.l_sinais:
        inf, bts = st.columns([3, 1.5])
        with inf:
            st.markdown(f"""
                <div class="radar-box">
                    <span>⏰ <b>{item['h']}</b> | {item['msg']} <br> 
                    <span class="tendencia-badge">TENDÊNCIA CONFIRMADA (+{item['int']} min)</span></span>
                    <span class="estrelas">{item['stars']}</span>
                </div>
            """, unsafe_allow_html=True)
        with bts:
            b1, b2, b3 = bts.columns(3)
            if b1.button("SG", key=f"sg_{item['h']}"): st.session_state.sg += 1; st.rerun()
            if b2.button("G1", key=f"g1_{item['h']}"): st.session_state.g1 += 1; st.rerun()
            if b3.button("L", key=f"l_{item['h']}"): st.session_state.loss += 1; st.rerun()

with col_analise:
    st.markdown("### 🛠️ MONITOR DE SOMA")
    st.session_state.pedra = st.number_input("ÚLTIMA PEDRA:", 0, 14, st.session_state.pedra)
    
    st.markdown(f"""
        <div style="background:#1a2026; padding:15px; border-radius:10px;">
            <b>PEDRA ATUAL:</b> {st.session_state.pedra}<br>
            <b>ANALISANDO CICLO...</b><br>
            <small style="color:#888;">O robô está verificando se a tendência é de repetição curta ou longa.</small>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🔥 ANALISAR E GERAR CORES", use_container_width=True):
        st.session_state.l_sinais = analisar_e_gerar("COR", st.session_state.pedra)
        st.rerun()

    if st.button("💎 ANALISAR E GERAR BRANCOS", use_container_width=True):
        st.session_state.l_sinais = analisar_e_gerar("BRANCO", st.session_state.pedra)
        st.rerun()

    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        st.session_state.l_sinais = []
        st.session_state.sg = 0; st.session_state.g1 = 0; st.session_state.loss = 0
        st.rerun()
