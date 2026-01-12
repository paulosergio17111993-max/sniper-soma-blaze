import requests
import time
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

def rodar_ferramenta():
    url_recentes = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1"
    ultimo_id = None
    cor_abertura = None
    aguardando_gale = False
    placar = {"WIN": 0, "G1": 0, "LOSS": 0}

    print(f"\n{Back.WHITE}{Fore.BLACK} 🔥 BLAZE SCANNER PRO: ESTRATÉGIA DE MINUTO 🔥 ")

    while True:
        try:
            res_recent = requests.get(url_recentes).json()
            dado = res_recent[0]
            id_agora = dado.get('id')
            cor_atual = dado.get('color')
            segundo = datetime.now().second

            if id_agora != ultimo_id:
                ultimo_id = id_agora
                
                # FASE 1: GERA PREVISÃO NA ABERTURA (0s - 25s)
                if 0 <= segundo <= 25:
                    if aguardando_gale:
                        if cor_atual == cor_abertura:
                            placar["G1"] += 1
                            print(f"{Back.GREEN}{Fore.BLACK} ✅ VITÓRIA NO GALE 1! ")
                        else:
                            placar["LOSS"] += 1
                            print(f"{Back.RED}{Fore.WHITE} ❌ LOSS NO GALE 1... ")
                        aguardando_gale = False

                    cor_abertura = cor_atual
                    cor_sugerida = "VERMELHO 🔴" if cor_atual == 1 else "PRETO ⚫" if cor_atual == 2 else "BRANCO ⚪"
                    fundo = Back.RED if cor_atual == 1 else Back.BLACK
                    
                    print(f"\n{Fore.CYAN}ID ATUAL: {id_agora}")
                    print(f"{fundo}{Fore.WHITE} 🎯 PREVISÃO: JOGUE NO {cor_sugerida} ")
                    print(f"{Fore.YELLOW}⏱️ ENTRAR NO SEGUNDO GIRO DO MINUTO (:30)")

                # FASE 2: CHECA O RESULTADO NO FECHAMENTO (:30 - :59)
                elif 30 <= segundo <= 59:
                    if cor_abertura is not None:
                        if cor_atual == cor_abertura:
                            placar["WIN"] += 1
                            print(f"{Back.GREEN}{Fore.BLACK} ✅ WIN DE PRIMEIRA! ")
                        else:
                            print(f"{Back.YELLOW}{Fore.BLACK} ⚠️ COR DIFERENTE: PREPARAR GALE 1 ")
                            aguardando_gale = True
                
                # MOSTRA O PLACAR SEMPRE
                print(f"📊 PLACAR: {Fore.GREEN}WIN: {placar['WIN']} {Fore.YELLOW}| G1: {placar['G1']} {Fore.RED}| LOSS: {placar['LOSS']}")
                print("-" * 50)

        except: pass
        time.sleep(1)

if __name__ == "__main__":
    rodar_ferramenta()