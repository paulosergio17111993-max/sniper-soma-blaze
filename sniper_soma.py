import streamlit as st

# Configuração da página para celular
st.set_page_config(page_title="Algoritmo Soma Pro", layout="centered")

# --- SISTEMA DE SENHA ---
SENHA_CORRETA = "SOMA77"  # <--- VOCÊ PODE MUDAR A SUA SENHA AQUI

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔑 Acesso Restrito")
    senha = st.text_input("Digite a Chave de Acesso:", type="password")
    if st.button("Entrar"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Chave incorreta! Chame o suporte no WhatsApp.")
    st.stop()

# --- ABAIXO O CÓDIGO DO SEU ROBÔ (SÓ APARECE APÓS A SENHA) ---
st.title("🎯 Algoritmo Soma Pro")
st.subheader("Cálculo por Peso de Pedra")

pedra = st.number_input("Nº da Pedra que saiu:", min_value=0, max_value=14, step=1)
minuto = st.number_input("Minuto da Saída (0-59):", min_value=0, max_value=59, step=1)

if st.button("GERAR ALVO"):
    resultado = pedra + minuto
    # Se passar de 60 minutos, ele ajusta
    if resultado >= 60:
        resultado = resultado - 60
    
    st.success(f"🔥 ALVO CALCULADO: MINUTO {resultado}")
    st.info("Entre 1 minuto antes e 1 minuto depois para garantir!")
