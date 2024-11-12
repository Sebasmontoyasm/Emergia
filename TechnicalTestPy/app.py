import requests
from flask import Flask, render_template, request, jsonify

from Controllers.tools.ExtractData import ExtractData
from Controllers.client.Client import Client
from Controllers.rpa.scrap_page import Scrapping_Page

import re

app = Flask(__name__)
'''Carga el cliente normalizado'''
def load_client_data(file_path="../output/clientes_normalizados.csv", file_type=".csv"):
    extractorClient = ExtractData(file_path, file_type)
    dataClient = extractorClient.readFile()
    return Client(dataClient)

'''Guarda el archivo .csv del cliente'''
def saveFile(file_path, file_type,response):
    extractorClient = ExtractData(file_path, file_type)
    extractorClient.save_to_csv(response)

'''Valida el archivo json cuando se quiere crear un cliente'''
def validate_client_data(client_data):
    """Valida los datos de un nuevo cliente"""
    required_fields = ['nombre', 'apellido', 'email', 'teléfono', 'fechaRegistro']

    for field in required_fields:
        if field not in client_data:
            return False, f"Falta el campo obligatorio: {field}"

    client_data['nombre'] = client_data['nombre'].strip().capitalize()
    client_data['apellido'] = client_data['apellido'].strip().capitalize()

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-za-z]+\.com$'
    if not re.match(email_pattern, client_data['email']):
        return False, "El formato del email no es válido."

    telefono_pattern = r'^\d{9}$'
    if not re.match(telefono_pattern, client_data['teléfono']):
        return False, "El campo 'teléfono' debe contener solo números y tener entre 8 y 10 caracteres"

    return True, None

'''Realiza la petición para normalizar el archivo .csv y guardarlo'''
@app.route(rule="/client/normalization",methods=['GET'])
def client_normalization():
    client = load_client_data(file_path="../input/clientes.csv", file_type=".csv")
    status,response, error = client.normalization()
    if status:
        saveFile(file_path="../input/clientes.csv", file_type=".csv",response=response)
        return "<p>Información del cliente normalizada</p>"
    else:
        print(error)
        return "<p>Información del cliente no normalizada</p>"
'''Inicia el proceso de anexar los clientes normalizados a la tabla de clientes'''
@app.route(rule="/client/insert",methods=['GET'])
def insert_client():
    client = load_client_data(file_path="../output/clientes_normalizados.csv", file_type=".csv")
    status, response, error = client.addClients()
    if status:
        return "<p>Información del cliente insertada</p>"
    else:
        print(error)
        return "<p>Información del cliente no insertada</p>"

'''Consulta y devuelve los clientes por año y los muestra en un template HMTL como impreso'''
@app.route(rule="/client/year",methods=['GET'])
def get_clientsByYear():
    getClients = Client.getClientsbyYear()
    if getClients is not None and not getClients.empty:
        columns = getClients.columns.tolist()
        rows = getClients.values.tolist()
        return render_template('clientPage.html', columns=columns, rows=rows)
    else:
        return "<p>No se encuentran clientes cargados por años</p>"

'''Consulta y devuelve los clientes y los muestra en un template HMTL como impreso'''
@app.route(rule='/clientes', methods=['GET'])
def get_clients():
    client = load_client_data(file_path="../output/clientes_normalizados.csv", file_type=".csv")
    getClients = client.getClients()
    if getClients is not None and not getClients.empty:
        columns = getClients.columns.tolist()
        rows = getClients.values.tolist()
        return render_template('clientPage.html', columns=columns, rows=rows)
    else:
        return "<p>No se encuentran clientes cargados</p>"

'''Recibe un JSON como cliente y lo sube a la base de datos'''
@app.route(rule='/clientes', methods=['POST'])
def post_clients():
    if not request.is_json:
        return jsonify({"error": "El cuerpo de la solicitud debe ser JSON"}), 400

    newClient = request.get_json()

    is_valid, error_message = validate_client_data(newClient)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    status, response = Client.createClient(newClient)

    if status:
        return jsonify({"message": "Cliente insertado exitosamente"}), 201
    else:
        return jsonify({"error": f"Error en la carga del cliente: {response}"}), 500

'''Filtra el cliente por correo electronico'''
@app.route(rule="/clientes/<email>",methods=['GET'])
def clientsByEmail(email):
    client = load_client_data(file_path="../output/clientes_normalizados.csv", file_type=".csv")
    getClients = client.getClientsbyEmail(email=email)
    if getClients is not None and not getClients.empty:
        columns = getClients.columns.tolist()
        rows = getClients.values.tolist()
        return render_template('clientPage.html', columns=columns, rows=rows)
    else:
        return "<p>No se encontraron clientes con ese criterio de búsqueda.</p>"

'''Accede a la pagina web y retorna la pagina'''
@app.route(rule="/rpa/httpbin.org",methods=['GET'])
def scrappingRPA():
    url = "https://httpbin.org"

    response = requests.get(url)

    if response.status_code == 200:
        page = Scrapping_Page(page=response)
        return page.parserHTML()
    else:
        return "Error al acceder a la página.", 400

'''Accede a la pagina web y retorna el titulo de la pagina web'''
@app.route(rule="/rpa/httpbin.org/title", methods=['GET'])
def scrappingRPATitle():
    url = "https://httpbin.org"

    response = requests.get(url)

    if response.status_code == 200:
        page = Scrapping_Page(page=response)
        return page.extractTitle()
    else:
        return "Error al acceder a la página.", 400

if __name__ == '__main__':
    app.run(debug=True)