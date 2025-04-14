from pdfminer.high_level import extract_text
import re
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Função para extrair o texto dos PDFs
def ler_pdf(path):
    try:
        return extract_text(path)
    except:
        return ""

# Função para identificar palavras nos arquivos que colocamos e retornar as que aparecem em mais de um arquivo
def identificar_palavras_comuns(arquivos):
    textos = {nome: ler_pdf(nome) for nome in arquivos}
    palavras_comuns = {}

    for nome, texto in textos.items():
        palavras = re.findall(r'\b\w{4,}\b', texto.lower())  # Filtra palavras com 4 ou mais letras
        for palavra in set(palavras):  # Usa set para evitar contar a mesma palavra várias vezes no mesmo arquivo
            if palavra in palavras_comuns:
                palavras_comuns[palavra].append(nome)
            else:
                palavras_comuns[palavra] = [nome]

    # Filtra palavras que aparecem em mais de um arquivo
    palavras_comuns = {p: a for p, a in palavras_comuns.items() if len(a) > 1}
    return palavras_comuns

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado_html = None  # Inicializa uma string vazia pra não retornar de inicio a mensagem de erro falando que n encontrou nada igual
    if request.method == 'POST':
        arquivos = request.files.getlist('pdfs')
        caminhos = []

        for arquivo in arquivos:
            if arquivo and arquivo.filename.endswith('.pdf'):
                caminho = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(arquivo.filename))
                arquivo.save(caminho)
                caminhos.append(caminho)

        palavras_comuns = identificar_palavras_comuns(caminhos)

        if palavras_comuns: 
            resultado_html = palavras_comuns  # Preenche o resultado com as palavras e arquivos

    return render_template('index.html', resultado=resultado_html)

if __name__ == '__main__':
    #app.run(debug=True) COMENTANDO PARA RODAR NO SERVIDOR RAILWAY
    pass