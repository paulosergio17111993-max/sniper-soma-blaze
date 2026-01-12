import datetime
import os
from colorama import init, Fore, Back, Style

# Inicializa as cores no Windows
init(autoreset=True)

def gerar_proximos_sinais():
    # Limpa a tela para o visual ficar limpo
    os.system('cls' if os.name == 'nt' else 'clear')
    
    agora = datetime.datetime.now()
    print(f"\n{Style.BRIGHT}{Fore.CYAN}🚀 GERANDO LISTA DE ALTA ASSERTIVIDADE - HORA: {agora.strftime('%H:%M')}")
    print(f"{Fore.YELLOW}" + "-" * 50)

    horarios = [4, 8, 12, 16, 20]
    
    for i, intervalo in enumerate(horarios):
        proximo_minuto = agora + datetime.timedelta(minutes=intervalo)
        horario_sinal = proximo_minuto.strftime("%H:%M")
        
        if i % 2 == 0:
            # Vermelho com fundo branco para brilhar
            cor_str = f"{Back.WHITE}{Fore.RED}{Style.BRIGHT} VERMELHO 🔴 "
        else:
            # Preto com fundo branco
            cor_str = f"{Back.WHITE}{Fore.BLACK}{Style.BRIGHT} PRETO ⚫    "
            
        confianca = f"{Fore.GREEN}⭐⭐⭐⭐⭐" if i < 2 else f"{Fore.YELLOW}⭐⭐⭐⭐"
        
        print(f"{Fore.WHITE}⏰ {Style.BRIGHT}{horario_sinal} {Fore.RESET}| ENTRADA: {cor_str} {Fore.RESET}| CONF: {confianca}")

    print(f"{Fore.YELLOW}" + "-" * 50)
    print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT} 💡 DICA: SE SAIR O Nº 4 OU 11, PROTEJA NO BRANCO! ")
    print("\n")

if __name__ == "__main__":
    gerar_proximos_sinais()