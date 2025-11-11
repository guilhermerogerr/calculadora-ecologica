from flask import Flask, render_template, request

app = Flask(__name__)

# --- Funções de cálculo ---
def calcular_emissao_energia(kwh, tem_ar, horas_ar, tem_chuveiro, minutos_chuveiro):
    total = 0
    fator_kwh = 0.000055  
    total += kwh * fator_kwh

    if tem_ar == "s":
        potencia_ar = 1500
        kwh_ar = (potencia_ar * horas_ar * 30) / 1000
        total += kwh_ar * fator_kwh

    if tem_chuveiro == "s":
        potencia_chuveiro = 5500
        kwh_chuveiro = (potencia_chuveiro * minutos_chuveiro * 30) / (1000 * 60)
        total += kwh_chuveiro * fator_kwh

    return total * 1000 


def calcular_emissao_residuos(sacos_lixo, recicla, percentual_recicla):
    # Cada saco de 30L ≈ 3 kg de lixo
    kilos_lixo = sacos_lixo * 3
    total = (kilos_lixo * 0.0012)
    if recicla == "s":
        total *= (1 - (percentual_recicla / 100) * 0.3)
    return total * 1000  


def calcular_emissao_tecnologia(usa_pc, horas_pc, usa_cel, horas_cel, usa_internet, horas_net):
    total = 0
    if usa_pc == "s":
        total += horas_pc * 30 * 0.00004
    if usa_cel == "s":
        total += horas_cel * 30 * 0.00002
    if usa_internet == "s":
        total += horas_net * 30 * 0.00002
    return total * 1000  


# --- Rotas ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/resultado', methods=['POST'])
def resultado():
    # Coleta dos dados do formulário
    #--- Energia ---
    kwh = float(request.form.get('kwh', 0))
    tem_ar = request.form.get('tem_ar', 'n')
    horas_ar = float(request.form.get('horas_ar', 0))
    tem_chuveiro = request.form.get('tem_chuveiro', 'n')
    minutos_chuveiro = float(request.form.get('minutos_chuveiro', 0))

    #--- Reciclagem ---
    recicla = request.form.get('recicla', 'n')
    percentual_recicla = float(request.form.get('percentual_recicla', 0))
    sacos_lixo = float(request.form.get('sacos_lixo', 0))

    #--- Tecnologia ---
    usa_pc = request.form.get('usa_pc', 'n')
    horas_pc = float(request.form.get('horas_pc', 0))
    usa_cel = request.form.get('usa_cel', 'n')
    horas_cel = float(request.form.get('horas_cel', 0))
    usa_internet = request.form.get('usa_internet', 'n')
    horas_net = float(request.form.get('horas_net', 0))

    # --- Cálculo total (em kg) ---
    energia = calcular_emissao_energia(kwh, tem_ar, horas_ar, tem_chuveiro, minutos_chuveiro)
    residuos = calcular_emissao_residuos(sacos_lixo, recicla, percentual_recicla)
    tecnologia = calcular_emissao_tecnologia(usa_pc, horas_pc, usa_cel, horas_cel, usa_internet, horas_net)

    total = energia + residuos + tecnologia

    # --- Classificação geral ---
    if total < 50:
        nivel = "Ecológico"
    elif total < 200:
        nivel = "Moderado"
    else:
        nivel = "Poluidor"

    return render_template(
        'resultado.html',
        total=round(total, 2),
        nivel=nivel
    )


if __name__ == '__main__':
    app.run(debug=True)