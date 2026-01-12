import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animar(i):
    try:
        dados = open('historico_tendencia.txt', 'r').read().split('\n')
        eixo_x = []
        eixo_y = []
        
        for linha in dados:
            if len(linha) > 1:
                id_rodada, cor, forca = linha.split(',')
                eixo_y.append(int(forca))
                eixo_x.append(len(eixo_y))

        plt.cla() # Limpa o gráfico anterior
        
        # Desenha a linha de tendência
        plt.plot(eixo_x, eixo_y, color='black', linewidth=2, label='Tendência de Cor')
        
        # Cria as zonas de força (Estilo BTC)
        plt.axhline(y=3, color='green', linestyle='--', label='Zona de Alta (Preto)')
        plt.axhline(y=-3, color='red', linestyle='--', label='Zona de Baixa (Vermelho)')
        plt.axhline(y=0, color='gray', linewidth=0.5)

        plt.title('BlazeTrend Pro - Elevação em Tempo Real')
        plt.legend(loc='upper left')
        plt.grid(True, alpha=0.3)
    except:
        pass

fig = plt.figure(facecolor='#f0f0f0')
ani = animation.FuncAnimation(fig, animar, interval=5000) # Atualiza a cada 5s
plt.show()