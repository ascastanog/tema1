import boto3
import hashlib
import hmac
import requests
import datetime
import base64
import json
from urllib.parse import urlencode
def menu():
    print("Bienvenido")
    valor = int(input("""Ingrese la funcion que desea realizar:
    1.- Detect Labels mediante llamada HTTP
    2.- Detect Labels mediante libreria boto3
    3.- Detect faces mediante libreria boto3
    4.- text extract mediante libreria boto3"""))

    ruta = input("Introduzca la ruta de la imagen con la que quiere trabajar de forma absoluta:")

    match valor:
        case 1:
            respuesta = llamada_http_api(ruta)
        case 2:
            respuesta = detect_labels_boto3(ruta)
        case 3:
            respuesta = detect_faces_boto3(ruta)
        case 4:
            respuesta = textract_boto3(ruta)


    # Verificar la respuesta
    if valor != 1 and respuesta.get("ResponseMetadata")['HTTPStatusCode'] == 200:
        print(respuesta)
    elif valor == 1 and respuesta.status_code == 200:
            response_json = respuesta.json()
            print(json.dumps(response_json, indent=2))
    else:
        print(f'Error: {respuesta.get("ResponseMetadata")['HTTPStatusCode']}')
        print(respuesta.text)


def textract_boto3(ruta):
    textract_cliente = boto3.client("textract", region_name=REGION,
                                       aws_access_key_id=AWS_ACCESS_KEY,
                                       aws_secret_access_key=AWS_SECRET_KEY,
                                       aws_session_token=AWS_SESSION_TOKEN)

    with open(ruta, "rb") as document_file:
        document_bytes = document_file.read()

    response = textract_cliente.detect_document_text(Document={"Bytes": document_bytes})

    return response


def detect_faces_boto3(ruta):
    rekognition_cliente = boto3.client("rekognition", region_name=REGION,
                                        aws_access_key_id=AWS_ACCESS_KEY,
                                        aws_secret_access_key=AWS_SECRET_KEY,
                                        aws_session_token=AWS_SESSION_TOKEN)

    with open(ruta, "rb") as image_file:
       image_bytes = image_file.read()

    response = rekognition_cliente.detect_faces(
        Image={'Bytes':image_bytes},
        Attributes=['ALL']
    )
    return response



def detect_labels_boto3(ruta):
    rekognition_cliente = boto3.client("rekognition", region_name=REGION,
                                        aws_access_key_id=AWS_ACCESS_KEY,
                                        aws_secret_access_key=AWS_SECRET_KEY,
                                        aws_session_token=AWS_SESSION_TOKEN)

    with open(ruta, "rb") as image_file:
        image_bytes = image_file.read()

    response = rekognition_cliente.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=15,
        MinConfidence=95.0
    )

    return response

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def llamada_http_api(ruta):
    rekognition_url = 'https://rekognition.us-east-1.amazonaws.com/'
    with open(ruta, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Crear el cuerpo de la solicitud
    request_body = {
        "Image": {
            "Bytes": image_base64
            # Aquí le proporcinamos la imagen sobre la que vamos a trabajar. Tiene que estar codificada en base64
        },

        "Attributes": ["ALL"],  # Especifica que quieres todos los atributos
        #   "MaxLabels": 10,       # Si quiero limitar el tamaño de la respuesta, puedo indicarle el número de etiquetas que quiero que me envíe
        "MinConfidence": 75
        # Especifico la confianza mínima que debe tener esa características. Cuanto más próxima esté la confianza a 100, más seguro está el modelo de que esa característica es verdadera
    }

    # Convertir el cuerpo de la petición a JSON
    request_payload = json.dumps(request_body)

    # Parámetros para la cabecera

    content_type = 'application/x-amz-json-1.1'  # tipo de contenido que le vamos a enviar

    # Obtener la fecha actual en el formato requerido
    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')  # fecha y hora en que se hace la solictud
    date_stamp = t.strftime('%Y%m%d')  # fecha en la que se hace la solicitud en formato aaaammdd

    # amz_target = 'RekognitionService.DetectLabels'             # identificador del tipo de servicio al que quiero acceder. En este caso DetectLabels
    amz_target = 'RekognitionService.DetectFaces'  # identificador del tipo de servicio al que quiero acceder. En este caso DetectFaces

    host = f'rekognition.{REGION}.amazonaws.com'  # identificación del nodo que da soporte al servicio


    # Creo la cabecera con los parámetros necesarios
    headers = {
        'Content-Type': content_type,
        'X-Amz-Date': amz_date,
        'X-Amz-Target': amz_target,
        'Host': host,
        'X-Amz-Security-Token': AWS_SESSION_TOKEN  # Token de sesión. Sólo si trabajamos con AWS_TOKEN_SESSION
    }

    # Crear el string para firmar

    # Si no estamos trabajando con AWS_SESSION_TOKEN
    # canonical_headers = f'content-type:{content_type}\nhost:{host}\nx-amz-date:{amz_date}\nx-amz-target:{amz_target}\n'
    # signed_headers = 'content-type;host;x-amz-date;x-amz-target'
    # Si estamos trabajando con AWS_SESSION_TOKEN

    # Componemos un string con los atributos que tiene el header y sus valores, separados por \n
    canonical_headers = f'content-type:{content_type}\nhost:{host}\nx-amz-date:{amz_date}\nx-amz-security-token:{AWS_SESSION_TOKEN}\nx-amz-target:{amz_target}\n'

    # le indicamos en este string qué atributos van a ser firmados
    signed_headers = 'content-type;host;x-amz-date;x-amz-security-token;x-amz-target'

    # Obtenemos el hash del cuerpo de la petición que vamos a enviar
    payload_hash = hashlib.sha256(request_payload.encode('utf-8')).hexdigest()

    # Componemos la canonical_request de la solicitud que se va a enviar
    method = 'POST'  # operación HTTP que se quiere hacer
    canonical_uri = '/'
    canonical_querystring = ''

    canonical_request = f'{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'

    print(canonical_request)


    # Crear la string para la firma
    algorithm = 'AWS4-HMAC-SHA256'  # algoritmo usado para la firma
    service = 'rekognition'  # servicio de AWS al que quiero invocar
    credential_scope = f'{date_stamp}/{REGION}/{service}/aws4_request'
    string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}'


    # Firmar la solicitud
    signing_key = getSignatureKey(AWS_SECRET_KEY, date_stamp, REGION, service)
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()


    # Agregar la firma a los encabezados
    authorization_header = f'{algorithm} Credential={AWS_ACCESS_KEY}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
    headers['Authorization'] = authorization_header



    # Hacer la solicitud POST
    response = requests.post(rekognition_url, headers=headers, data=request_payload)

    return response




AWS_ACCESS_KEY = 'ASIATOBR4A7RBWSFKRO3'
AWS_SECRET_KEY = '7MyDDAlnDEx91ji0KVJYF26ob5nJNMETUe7x2tO3'
AWS_SESSION_TOKEN = 'IQoJb3JpZ2luX2VjECIaCXVzLXdlc3QtMiJHMEUCIF2cdAvPE6uIK1MbsznuvJslzaaI9gvVwvuO+t6sA9uVAiEA22b+DjUS1p/nx5DFAYwyzgYCsXsqgwpt2/hVmDrFGmsqsgIIGxABGgwyMzYzMjc3OTg3NTQiDI3T6oG3AyECInNs0iqPApE25PDXRqI/CgT2zOUIqxaXPNIgeB6GbTcwEg/PacMT230HEgwULsTfhdwLo5FTXvm60fIdXJOUX5wFWXNfHohH+ci4CAwoyfh4V+C7AgLOXDujztGYYoEtU6//Syfcoh4YZgdbS4wN6c6K/rLJiNiq7qhgBKLsJbnFBIMrYJLOX2A8b8zdVgtn0Xwz9M/v2RlLyRLnXcE8igsrdiFRXS8CJbYxg6rql1gVCW5BBvmn5+voTlbYAqHc3jaNHWVJTgH7PUQSjm7fmsMAPwhOQprMqMvBFrxrSFSZqFf07D4BKBeIgbv0mrHONjJuJmjLmDgpzesaryOEfQoioYl1+vlquU1z0GgUrc6ROy5HwYcwyr2avAY6nQHznpPPuheA1MEt3Zpj8EoI4/dJkwnbbMjyKEHoV9AdaWza49/V5JLWkwfeVpN0wu3hSEFQT7ezgsoqpkAjaBoBeR10XE4Tse+Fn0Gh66piw5oiTcAKA1ZHa2JU+Ln323QZ/2hRyx1SwxyQYqxueaSbDj9NJE57DBgVGJG9X4U4dFI2/u9TiOq16EFFRvq45eZYXE8xfEpjwNH87HX8'
REGION = 'us-east-1'

menu()