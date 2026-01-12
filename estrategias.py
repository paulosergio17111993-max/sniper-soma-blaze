def check_strategy(historico_cores, historico_numeros):
    # Filtro de segurança: se não tiver dados suficientes, não faz nada
    if len(historico_cores) < 4:
        return None

    ultima_pedra = historico_numeros[-1]
    
    # --- REGRA DE OURO: SE CAIR 11 OU 4, ESPERAMOS 1 GIRO ---
    # Isso evita o Loss que você acabou de tomar no Gale 2!
    if ultima_pedra in [4, 11]:
        return "⏳ AGUARDANDO: MESA EM TRANSIÇÃO (Gatilho Detectado)"

    # --- ESTRATÉGIA 1: SURFE DE ALTA ASSERTIVIDADE (3 iguais -> entra na 4ª) ---
    if historico_cores[-3:] == [1, 1, 1]:
        return "🎯 ENTRADA CONFIRMADA: VERMELHO 🔴 (Surfe)"
    
    if historico_cores[-3:] == [2, 2, 2]:
        return "🎯 ENTRADA CONFIRMADA: PRETO ⚫ (Surfe)"

    # --- ESTRATÉGIA 2: XADREZ DE ELITE (1x1 repetido) ---
    if historico_cores[-4:] == [1, 2, 1, 2]:
        return "⚡ ENTRADA CONFIRMADA: VERMELHO 🔴 (Quebra Xadrez)"
    
    if historico_cores[-4:] == [2, 1, 2, 1]:
        return "⚡ ENTRADA CONFIRMADA: PRETO ⚫ (Quebra Xadrez)"

    return None