# =========================================================
# PROJETO PIBIC - LEI DE FARADAY E LENZ COM ARDUINO
# Autor: JP
#
# Funções:
# ✓ Ler dados do Arduino em tempo real
# ✓ Plotar gráfico ao vivo
# ✓ Detectar picos da f.e.m.
# ✓ Salvar dados em CSV
# ✓ Mostrar valor instantâneo
#
# Instale antes:
# pip install pyserial matplotlib pandas
# =========================================================

import serial
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# =========================================================
# CONFIGURAÇÕES
# =========================================================

PORTA = 'COM3'        # MUDE para a porta do seu Arduino
BAUDRATE = 115200

MAX_PONTOS = 300      # quantidade de pontos na tela
LIMIAR_PICO = 40      # sensibilidade do pico

# =========================================================
# CONEXÃO SERIAL
# =========================================================

print("Conectando ao Arduino...")

ser = serial.Serial(PORTA, BAUDRATE)
time.sleep(2)

print("Arduino conectado!")

# =========================================================
# DADOS
# =========================================================

x_data = deque(maxlen=MAX_PONTOS)
y_data = deque(maxlen=MAX_PONTOS)

dados_csv = []

inicio = time.time()

# =========================================================
# GRÁFICO
# =========================================================

fig, ax = plt.subplots(figsize=(10,5))

linha, = ax.plot([], [], linewidth=2)

ax.set_title("F.E.M. Induzida - Lei de Faraday")
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Amplitude do Sinal")

# linha central
ax.axhline(0)

# =========================================================
# FUNÇÃO DE ATUALIZAÇÃO
# =========================================================

def update(frame):

    global dados_csv

    try:

        # leitura serial
        dado = ser.readline().decode('utf-8').strip()

        valor = float(dado)

        # centraliza o sinal
        valor = valor - 512

        tempo = time.time() - inicio

        # salva nos vetores
        x_data.append(tempo)
        y_data.append(valor)

        # salva para CSV
        dados_csv.append([tempo, valor])

        # atualiza gráfico
        linha.set_data(x_data, y_data)

        ax.relim()
        ax.autoscale_view()

        # detecção de pico
        if abs(valor) > LIMIAR_PICO:

            print(f'PICO DETECTADO -> {valor:.2f}')

            # Lei de Lenz:
            if valor > 0:
                print("Campo induzido: sentido positivo")
            else:
                print("Campo induzido: sentido negativo")

    except:
        pass

    return linha,

# =========================================================
# ANIMAÇÃO
# =========================================================

ani = FuncAnimation(
    fig,
    update,
    interval=10,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()

# =========================================================
# SALVAR CSV
# =========================================================

print("Salvando dados...")

df = pd.DataFrame(
    dados_csv,
    columns=["tempo_s", "fem_induzida"]
)

nome_arquivo = f"dados_faradey_{int(time.time())}.csv"

df.to_csv(nome_arquivo, index=False)

print(f"Dados salvos em: {nome_arquivo}")

ser.close()