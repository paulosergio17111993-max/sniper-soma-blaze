<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Sinais - 99%</title>
    <style>
        body { background-color: #0b0e11; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        
        /* PLACA DE RESULTADOS */
        .placa-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: 100%; max-width: 500px; margin-bottom: 20px; text-align: center; }
        .card { background: #1a2026; padding: 15px; border-radius: 8px; border-bottom: 4px solid #333; }
        .card h3 { font-size: 12px; margin: 0; color: #888; text-transform: uppercase; }
        .card p { font-size: 24px; font-weight: bold; margin: 5px 0 0 0; }
        .sg { border-color: #00ff88; color: #00ff88; }
        .g1 { border-color: #00d4ff; color: #00d4ff; }
        .loss { border-color: #ff4d4d; color: #ff4d4d; }
        .total { border-color: #f7b924; color: #f7b924; }

        /* LISTA DE SINAIS */
        .radar-box { background: #1a2026; width: 100%; max-width: 500px; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h2 { text-align: center; color: #fff; margin-top: 0; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .sinal-item { display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid #2a323a; }
        .sinal-info { display: flex; align-items: center; gap: 10px; }
        .btn-check { cursor: pointer; border: none; padding: 5px 10px; border-radius: 4px; font-weight: bold; }
        .btn-sg { background: #00ff88; color: #000; }
        .btn-g1 { background: #00d4ff; color: #000; }
        .btn-loss { background: #ff4d4d; color: #fff; }
    </style>
</head>
<body>

    <div class="placa-container">
        <div class="card sg">
            <h3>SG</h3>
            <p id="count-sg">0</p>
        </div>
        <div class="card g1">
            <h3>G1</h3>
            <p id="count-g1">0</p>
        </div>
        <div class="card loss">
            <h3>LOSS</h3>
            <p id="count-loss">0</p>
        </div>
        <div class="card total">
            <h3>TOTAL</h3>
            <p id="count-total">0</p>
        </div>
    </div>

    <div class="radar-box">
        <h2>RADAR DE SINAIS</h2>
        <div id="lista-sinais">
            <div class="sinal-item">
                <div class="sinal-info">
                    <span>⏰ 19:49</span>
                    <span style="color: #ff4d4d;">● VERMELHO</span>
                </div>
                <div>
                    <button class="btn-check btn-sg" onclick="registrar('sg')">SG</button>
                    <button class="btn-check btn-g1" onclick="registrar('g1')">G1</button>
                    <button class="btn-check btn-loss" onclick="registrar('loss')">L</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let sg = 0, g1 = 0, loss = 0, total = 0;

        function registrar(tipo) {
            if(tipo === 'sg') {
                sg++;
                total++;
                document.getElementById('count-sg').innerText = sg;
            } else if(tipo === 'g1') {
                g1++;
                total++;
                document.getElementById('count-g1').innerText = g1;
            } else if(tipo === 'loss') {
                loss++;
                document.getElementById('count-loss').innerText = loss;
            }
            document.getElementById('count-total').innerText = total;
        }
    </script>
</body>
</html>
