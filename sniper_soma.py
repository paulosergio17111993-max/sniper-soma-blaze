import streamlit as st
import random
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="SNIPER SOMA 99%", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .placa-card { background: #1a2026; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 4px solid #333; }
    .sinal-box { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 8px; border: 1px solid #30363d; }
    .numero-puxador { background: #f7b924; color: black; padding: 5px 12px; border-radius: 4px; font-weight: bold; margin-right: 5px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DO SISTEMA ---
if 'lista_cores' not in st.session_state: st.session_state.lista_cores = []
if 'lista_brancos' not in st.session_state: st.session_state.lista_brancos = []
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'pedra_atual' not in st.session_state: st.session_state.pedra_atual = 12

# --- LÓGICA DE SOMA (O CORAÇÃO DO BOTÃO) ---
def calcular_puxada_por_soma(pedra):
    # Lógica baseada nos seus puxadores: 4, 12, 7
    if pedra in [4, 12, 7]:
        return "BRANCO ⚪ (Puxador Ativo)"
    elif pedra <= 7:
        return "PRETO ⚫ (Quebra de Soma)"
    else:
        return "VERMELHO 🔴 (Quebra de Soma)"

def gerar_lista_inteligente(tipo):
    novos_sinais = []
    agora = datetime.now()
    puxada = calcular_puxada_por_soma(st.session_state.pedra_atual)
    
    for i in range(5):
        # Ajustando os horários para serem próximos ao atual
        minutos_frente = (i + 1) * 3 
        horario = (agora + timedelta(minutes=minutos_frente)).strftime("%H:%M")
        
        if tipo == "cor":
            # Se for cor, ele alterna conforme a soma da pedra atual
            cor = puxada if "BRANCO" not in puxada else random.choice(["VERMELHO 🔴", "PRETO ⚫"])
            novos_sinais.append({"h": horario, "c": cor})
        else:
            novos_sinais.append({"h": horario, "c": "BRANCO ⚪"})
    return novos_sinais

# --- PLACA DE RESULTADOS ---
st.markdown("### 📊 PLACA DE RESULTADOS")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="placa-card" style="border-color: #00ff88;"><b style="color: #00ff88;">SG</b><br><h2>{st.session_state.sg}</h2></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="placa-card" style="border-color: #00d4ff;"><b style="color: #00d4ff;">G1</b><br><h2>{st.session_state.g1}</h2></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="placa-card" style="border-color: #ff4d4d;"><b style="color: #ff4d4d;">LOSS</b><br><h2>{st.session_state.loss}</h2></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="placa-card" style="border-color: #f7b924;"><b style="color: #f7b924;">TOTAL</b><br><h2>{st.session_state.sg + st.session_state.g1}</h2></div>', unsafe_allow_html=True)

st.divider()

# --- CONTROLES LATERAIS ---
with st.sidebar:
    st.header("🎮 GERAR SINAIS")
    # BOTÃO QUE GERA BASEADO NA SOMA DA PEDRA
    if st.button("🔄 GERAR POR SOMA (CORES)"):
        st.session_state.lista_cores = gerar_lista_inteligente("cor")
    
    if st.button("⚪ GERAR POR SOMA (BRANCOS)"):
        st.session_state.lista_brancos = gerar_lista_inteligente("branco")
    
    st.divider()
    st.session_state.pedra_atual = st.number_input("PEDRA QUE SAIU:", 0, 14, st.session_state.pedra_atual)
    
    if st.button("🗑️ LIMPAR TUDO"):
        st.session_state.lista_cores = []
        st.session_state.lista_brancos = []
        st.rerun()

# --- RADAR E ANÁLISE ---
col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.lista_cores:
        st.markdown("### 📋 RADAR DE CORES (Soma Ativa)")
        for s in st.session_state.lista_cores:
            col_t, col_b = st.columns([3, 2])
            col_t.markdown(f'<div class="sinal-box">⏰ {s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)
            b1, b2, b3 = col_b.columns(3)
            if b1.button("SG", key=f"s_{s['h']}"): st.session_state.sg += 1; st.rerun()
            if b2.button("G1", key=f"g_{s['h']}"): st.session_state.g1 += 1; st.rerun()
            if b3.button("L", key=f"l_{s['h']}"): st.session_state.loss += 1; st.rerun()

    if st.session_state.lista_brancos:
        st.markdown("### ⚪ RADAR DE BRANCOS")
        for b in st.session_state.lista_brancos:
            st.markdown(f'<div class="sinal-box" style="border-left: 5px solid white;">⏰ {b["h"]} | {b["c"]}</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### 🧮 ANÁLISE DA SOMA")
    st.markdown(f"""
    <div style="background: #1a2026; padding: 20px; border-radius: 10px; border: 1px solid #333;">
        <p><b>PEDRA NO HISTÓRICO:</b> <span style="font-size:30px; color:#f7b924;">{st.session_state.pedra_atual}</span></p>
        <p><b>SOMA PARA O BOTÃO:</b> {st.session_state.pedra_atual}</p>
        <hr>
        <p><b>PUXADORES ATIVOS:</b></p>
        <span class="numero-puxador">4</span> 
        <span class="numero-puxador">12</span> 
        <span class="numero-puxador">7</span>
    </div>
    """, unsafe_allow_html=True)
