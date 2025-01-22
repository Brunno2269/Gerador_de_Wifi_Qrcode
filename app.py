from flask import Flask, render_template, request, send_file
import qrcode
import io
import webbrowser
import os
import signal
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    ssid = request.form['ssid']
    password = request.form['password']
    security = request.form['security']

    wifi_config = f"WIFI:T:{security};S:{ssid};P:{password};;"

    # Gera o QR Code com tamanho aumentado
    qr = qrcode.QRCode(
        version=1,
        box_size=20,  # Tamanho aumentado
        border=10     # Borda aumentada
    )
    qr.add_data(wifi_config)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Salva a imagem em um buffer
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

# Novo endpoint para notificar o fechamento da guia
@app.route('/fechar_guia', methods=['POST'])
def fechar_guia():
    print("Guia fechada. Encerrando servidor...")
    os._exit(0)  # Encerra o servidor Flask
    return '', 204  # Resposta vazia com status 204 (No Content)

def abrir_navegador():
    # Abre o navegador na URL do Flask
    webbrowser.open_new('http://127.0.0.1:5000/')

def encerrar_servidor(signal, frame):
    print("\nServidor encerrado. Fechando o terminal...")
    sys.exit(0)

if __name__ == '__main__':
    # Abre o navegador automaticamente
    abrir_navegador()

    # Configura o sinal para encerrar o servidor ao pressionar Ctrl+C
    signal.signal(signal.SIGINT, encerrar_servidor)

    # Executa o servidor Flask
    app.run(debug=False)