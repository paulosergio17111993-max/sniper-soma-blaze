import streamlit as st
import datetime

st.set_page_config(page_title="Sniper Soma", layout="centered")

st.markdown("<style>.stApp { background-color: #0e1117; color: white; }</style>", unsafe_allow_html=True)

st.title("⚖️ Sniper: Soma de Pedras")
st.write("Digite a última pedra e o minuto que ela saiu.")

col1, col2 = st.columns(2)
with col1:
    pedra = st.number_input("Nº da Pedra", 1, 14, 13)
with col2:
    minuto_saiu = st.number_input("Minuto da Saída", 0, 59, datetime.datetime.now().minute)

if st.button('CALCULAR ENTRADA AGORA'):
    soma = pedra + minuto_saiu
    alvo = soma if soma < 60 else soma - 60
    cor = "⚫ PRETO" if pedra > 7 else "🔴 VERMELHO"
    st.markdown(f"## 🎯 ALVO: Minuto {alvo:02d}")
    st.markdown(f"### COR: {cor}")
    st.info("Estratégia: Pedra + Minuto de Saída")