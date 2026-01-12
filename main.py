import requests
import time
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

def rodar_ferramenta():
    url = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1"
    ultimo_id = None
    cor_alvo = None
    num_abertura = None
    estagio_gale = 0 
    placar = {"WIN": 0, "G1": 0, "G2": 0, "LOSS": 0}

    print(f"\n{Back.WHITE}{Fore.BLACK} 🔥 BLAZE TREND PRO: DISPARO AGRESSIVO ATIVADO 🔥 ")

    while True:
        try:
            res = requests.get(url, timeout=5).json()
            dado = res[0]
            id_agora = dado.get('id')
            cor_atual = dado.get('color')
            num_atual = dado.get('roll')
            segundo = datetime.now().second

            if id_agora != ultimo_id:
                ultimo_id = id_agora
                
                # --- PROCESSA RESULTADO DO GIRO ANTERIOR ---
                if cor_alvo is not None:
                    if cor_atual == cor_alvo:
                        if estagio_gale == 0: placar["WIN"] += 1
                        elif estagio_gale == 1: placar["G1"] += 1
                        elif estagio_gale == 2: placar["G2"] += 1
                        print(f"{Back.GREEN}{Fore.BLACK} ✅ WIN NO ALVO! (Nº {num_atual}) ")
                        cor_alvo = None
                        estagio_gale = 0
                    else:
                        if estagio_gale < 2:
                            estagio_gale += 1
                            print(f"{Fore.YELLOW}🔄 SEM CORRESPONDENCIA. GALE {estagio_gale} ATIVADO! (Nº {num_atual})")
                        else:
                            placar["LOSS"] += 1
                            print(f"{Back.RED}{Fore.WHITE} ❌ LOSS NO G2. RESETANDO CICLO. ")
                            cor_alvo = None
                            estagio_gale = 0

                # --- GERA NOVO SINAL (DESTRAVADO - TODO MINUTO) ---
                # Se estiver entre o segundo 0 e 28, ele pega a cor e já projeta a entrada
                if 0 <= segundo <= 28 and estagio_gale == 0 and cor_alvo is None:
                    if cor_atual != 0:
                        cor_alvo = cor_atual # Repete a cor da base (Estratégia dos 11 SGs)
                        num_abertura = num_atual
                        cor_nome = "VERMELHO 🔴" if cor_alvo == 1 else "PRETO ⚫"
                        fundo = Back.RED if cor_alvo == 1 else Back.BLACK
                        
                        print(f"\n{Fore.CYAN}ID: {id_agora} | HORA: {datetime.now().strftime('%H:%M:%S')}")
                        print(f"{fundo}{Fore.WHITE} 🎯 ENTRADA CONFIRMADA: {cor_nome} (BASE: Nº {num_abertura}) ")
                        print(f"{Fore.YELLOW}⏱️ JOGAR NO GIRO DE :30 SEGUNDOS")
                    else:
                        print(f"\n⚪ BRANCO DETECTADO (Nº 0) - AGUARDANDO PROXIMO MINUTO")

                # Placar sempre atualizado para você ver o lucro
                print(f"📊 SG: {placar['WIN']} | G1: {placar['G1']} | G2: {placar['G2']} | LOSS: {placar['LOSS']}")
                print("-" * 55)

        except: pass
        time.sleep(1)

if __name__ == "__main__":
    rodar_ferramenta()