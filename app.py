from flask import Flask, render_template, request
from datetime import datetime
import csv
import os

app = Flask(__name__)

ARQUIVO = "dados.csv"

estados = {
    "AC": "ACRE", "AL": "ALAGOAS", "AP": "AMAPÁ", "AM": "AMAZONAS",
    "BA": "BAHIA", "CE": "CEARÁ", "DF": "DISTRITO FEDERAL",
    "ES": "ESPÍRITO SANTO", "GO": "GOIÁS", "MA": "MARANHÃO",
    "MT": "MATO GROSSO", "MS": "MATO GROSSO DO SUL",
    "MG": "MINAS GERAIS", "PA": "PARÁ", "PB": "PARAÍBA",
    "PR": "PARANÁ", "PE": "PERNAMBUCO", "PI": "PIAUÍ",
    "RJ": "RIO DE JANEIRO", "RN": "RIO GRANDE DO NORTE",
    "RS": "RIO GRANDE DO SUL", "RO": "RONDÔNIA", "RR": "RORAIMA",
    "SC": "SANTA CATARINA", "SP": "SÃO PAULO",
    "SE": "SERGIPE", "TO": "TOCANTINS"
}

def criar_csv():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nome", "Idade", "Estado", "DataHora"])

def proximo_id():
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return len(list(csv.reader(f)))

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""
    sucesso = False

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        idade = request.form.get("idade", "").strip()
        estado_input = request.form.get("estado", "").strip().upper()

        if not nome or not nome.replace(" ", "").isalpha():
            mensagem = "Nome inválido."
        elif not idade.isdigit() or not (1 <= int(idade) <= 120):
            mensagem = "Idade inválida."
        elif estado_input not in estados and estado_input not in estados.values():
            mensagem = "Estado inválido."
        else:
            estado = estados.get(estado_input, estado_input.title())
            datahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            with open(ARQUIVO, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    proximo_id(),
                    nome,
                    idade,
                    estado,
                    datahora
                ])

            mensagem = "Cadastro salvo com sucesso."
            sucesso = True

    return render_template("index.html", mensagem=mensagem, sucesso=sucesso)

if __name__ == "__main__":
    criar_csv()
    app.run(debug=True)
app.run(host="0.0.0.0", port=10000)
