import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE TELA (Estilo Algoritmo-Soma-Pro) ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

# Estilo para remover poluição e focar nos dados
st.markdown("""
    <style>
    .stApp { background-color: #080808; color: white; }
    
    /* Lista de Cores Vertical */
    .linha-cor {
        padding: 10px; margin-bottom: 5px; border-radius: 4px;
        text-align: center; font-weight: bold; font-size: 14px;
        text-transform: uppercase;
    }
    .cor-0 { background: #ffffff; color: #000; border: 1px solid #ccc; }
    .cor-1 { background: #f12c4c; color: #fff; }
    .cor-2 { background: #2b2b2b; color: #fff; border: 1px solid #444; }

    /* Horários de Branco (Terminais) */
    .card-terminal {
        background: #151515; border-left: 5px solid #00ff00;
        padding: 15px; margin-bottom: 8px; border-radius: 4px;
    }
    
    /* Painel Central de Sinal */
    .box-sinal {
        background: #000; border: 2px solid #00ff00;
        padding: 40px; text-align: center; border-radius: 15px;
        box-shadow: 0 0 15px rgba(0,255,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 ALGORITMO SOMA PRO")

# Criando as 3 colunas laterais conforme o layout original
col_historico, col_principal, col_terminais = st.columns([1, 1.8, 1])

with col_historico:
    st.markdown("### 🕒 CORES")
    area_lista = st.empty()

with col_principal:
    st.markdown("### 🎯 ENTRADA")
    area_entrada = st.empty()

with col_terminais:
    st.markdown("### ⚪ TERMINAIS")
    area_brancos = st.empty()

# URL DA API DA PLATAFORMA
URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        # Puxa os dados reais da API
        r = requests.get(URL_API, timeout=10)
        dados = r.json()
        
        # Identifica se os dados estão em 'records' ou direto na lista
        lista = dados.get('records', []) if isinstance(dados, dict) else dados
        
        if lista:
            # 1. LISTA VERTICAL DE CORES (Esquerda)
            with area_lista.container():
                for item in lista[:15]:
                    c_id = item['color']
                    num = item['roll']
                    label = "BRANCO" if c_id == 0 else ("VERMELHO" if c_id == 1 else "PRETO")
                    st.markdown(f'<div class="linha-cor cor-{c_id}">{label} ({num})</div>', unsafe_allow_html=True)

            # 2. SINAL DE ENTRADA (Centro)
            ultima = lista[0]
            sinal = "VERMELHO 🔴" if ultima['color'] == 2 else "PRETO ⚫"
            if ultima['color'] == 0: sinal = "AGUARDAR..."
            
            with area_entrada.container():
                st.markdown(f"""
                    <div class="box-sinal">
                        <h2 style="color: #00ff00; margin-bottom: 20px;">ENTRADA ANALISADA</h2>
                        <div style="font-size: 50px; font-weight: bold;">{sinal}</div>
                        <p style="margin-top: 20px; color: #888;">COBRIR O BRANCO ⚪</p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. TERMINAIS VICIADOS (Direita) - Extrai horários do campo created_at
            with area_brancos.container():
                brancos = [i for i in lista if i['color'] == 0]
                if brancos:
                    for b in brancos[:8]:
                        # Extrai apenas Hora:Minuto da string enviada (ex: 01:03)
                        hora_minuto = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-terminal">
                                <small style="color: #666;">HORÁRIO VICIADO</small><br>
                                <b style="font-size: 24px;">{hora_minuto}</b>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("Aguardando novo Branco...")

    except:
        # Se falhar, mostra a mensagem de erro que você viu
        st.warning("Reconectando ao servidor...")

    time.sleep(5)
