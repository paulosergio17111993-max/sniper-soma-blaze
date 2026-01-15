import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER MS - CRUZAMENTO", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .box-resultado { 
        background: #161b22; border: 2px solid #00ff88; padding: 20px; 
        border-radius: 10px; text-align: center; margin-top: 10px;
    }
    .radar-box { 
        background-color: #10141d; border: 1px solid #1d2633; border-radius: 10px; 
        padding: 10px; margin-bottom: 5px; border-left: 5px solid #00ff88; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if 'cor_final' not in st.session_state: st.session_state.cor_final = "Aguardando..."
if 'l_cores' not in st.session_state: st.session_state.l_cores = []
if 'l_brancos' not in st.session_state: st.session_state.l_brancos = []

# --- LÓGICA DE CRUZAMENTO (PEDRA + MINUTO) ---
def calcular_cor_cruzada(pedra, minuto):
    # Lógica: Soma a pedra com o minuto escolhido
    # Se o resultado for par = Vermelho, se for ímpar = Preto
    resultado = pedra + minuto
    if resultado % 2 == 0:
        return "VERMELHO 🔴"
    else:
        return "PRETO ⚫"

def gerar_lista(tipo, intervalo, cor_base):
    agora = datetime.now(fuso_ms)
    lista = []
    referencia = agora
    for i in range(6):
        referencia = referencia + timedelta(minutes=intervalo)
        if tipo == "COR":
            lista.append({"h": referencia.strftime("%H:%M"), "msg": f"ENTRADA: {cor_base}"})
        else:
            lista.append({"h": referencia.strftime("%H:%M"), "msg": "ENTRADA: BRANCO ⚪"})
    return lista

# --- INTERFACE ---
st.title("🎯 SNIPER MS - CRUZAMENTO PEDRA/MINUTO")

col_lista, col_ctrl = st.columns([2, 1])

with col_ctrl:
    st.subheader("🛠️ ENTRADA DE DADOS")
    
    # OS DOIS LUGARES PARA COLOCAR OS DADOS
    v_pedra = st.number_input("DIGITE A PEDRA:", 0, 14, 5)
    v_minuto = st.number_input("DIGITE O MINUTO:", 0, 60, 4)
    
    # BOTÃO PARA GERAR A COR DAQUELA PEDRA + MINUTO
    if st.button("🔄 CRUZAR DADOS E GERAR COR", use_container_width=True):
        st.session_state.cor_final = calcular_cor_cruzada(v_pedra, v_minuto)
    
    st.markdown(f"""
        <div class="box-resultado">
            <small>RESULTADO DO CRUZAMENTO:</small><br>
            <h2 style="color:#00ff88;">{st.session_state.cor_final}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # BOTÕES PARA GERAR AS LISTAS (USANDO O INTERVALO QUE VOCÊ COLOCOU NO MINUTO)
    if st.button("🔥 GERAR LISTA DE CORES", use_container_width=True):
        if st.session_state.cor_final != "Aguardando...":
            st.session_state.l_cores = gerar_lista("COR", v_minuto, st.session_state.cor_final)
            
    if st.button("⚪ GERAR LISTA DE BRANCOS", use_container_width=True):
        st.session_state.l_brancos = gerar_lista("BRANCO", v_minuto, "")

    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        st.session_state.l_cores = []; st.session_state.l_brancos = []
        st.session_state.cor_final = "Aguardando..."
        st.rerun()

with col_lista:
    if st.session_state.l_cores:
        st.subheader("🔥 RADAR DE CORES")
        for s in st.session_state.l_cores:
            st.markdown(f'<div class="radar-box">⏰ <b>{s["h"]}</b> | {s["msg"]}</div>', unsafe_allow_html=True)

    if st.session_state.l_brancos:
        st.subheader("⚪ RADAR DE BRANCOS")
        for s in st.session_state.l_brancos:
            st.markdown(f'<div class="radar-box" style="border-left-color:white;">⏰ <b>{s["h"]}</b> | {s["msg"]}</div>', unsafe_allow_html=True)
