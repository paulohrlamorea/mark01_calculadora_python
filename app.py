import unicodedata
from flask import Flask, render_template, request

app = Flask(__name__)

def normalizar_texto(texto):
    if texto is None:
        return ""
    
    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )

    return texto

def converter_numero(valor):
    valor = valor.strip().replace(",",".")

    if valor == "":
        raise ValueError("Preencha os dois números.")
    
    return float(valor)

def calcular(numero1, numero2, operacao):
    operacao = operacao.lower().strip()
    operacao = operacao.replace("ç", "c").replace("ã", "a")
    
    print("Operação tratada dentro da função:", operacao)

    if operacao == "soma":
        return numero1 + numero2, "Soma"
    
    elif operacao == "subtracao":
        return numero1 - numero2, "Subtração"
    
    elif operacao.startswith("multiplic"):
        return numero1 * numero2, "Multiplicação"
    
    elif operacao == "divisao":
        if numero2 == 0:
            raise ValueError("Não é possível dividir por zero.")
        return numero1 / numero2, "Divisão"
    
    else:
        raise ValueError(f"Operação inválida recebida: {operacao}")
    

def gerar_informacoes(resultado):
    if resultado > 0:
        situacao = "Positiva"
    elif resultado < 0:
        situacao = "Negativa"
    else:
        situacao = "Zero"
    
    if resultado.is_integer():
        tipo = "Inteiro"
    else:
        tipo = "Decimal"

    return situacao, tipo


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None
    nome_operacao = ""
    situacao = ""
    tipo = ""

    numero1 = ""
    numero2 = ""
    operacao = "soma"

    if request.method == "POST":
        numero1 = request.form.get("numero1", "")
        numero2 = request.form.get("numero2", "")
        operacao = request.form.get("operacao", "soma")
        
        print("Operação recebida do HTML: ", operacao)

        try:
            n1 = converter_numero(numero1)
            n2 = converter_numero(numero2)

            resultado, nome_operacao = calcular(n1, n2, operacao)
            situacao, tipo = gerar_informacoes(resultado)

            print(f"Operação: {nome_operacao} | {n1} e {n2} = {resultado}")

        except ValueError as e:
            erro = str(e)

    return render_template(
        "index.html",
        resultado=resultado,
        erro=erro,
        nome_operacao=nome_operacao,
        situacao=situacao,
        tipo=tipo,
        numero1=numero1,
        numero2=numero2,
        operacao=operacao,
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)