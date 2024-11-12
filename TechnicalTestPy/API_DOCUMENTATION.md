# Documentación de la API

Esta es la documentación para la API de la prueba técnica para desarrollador python. A continuación se describen los endpoints disponibles, los métodos HTTP que aceptan, los parámetros necesarios y ejemplos de las solicitudes y respuestas.

Documentación detallada: https://documenter.getpostman.com/view/26230773/2sAY545y4L

## Endpoints disponibles

### Normalización de archivo csv

- **Método HTTP**: `GET`
- **URL**: `http://127.0.0.1:5000/client/normalization`
- **Descripción**: Este endpoint inserta los datos normalizados a la tabla cliente

### Carga clientes normalizados a la db

- **Método HTTP**: `GET`
- **URL**: `http://127.0.0.1:5000/client/insert`
- **Descripción**: Este endpoint toma el archivo clientes.csv en el input y lo normaliza en el output clientes_normalizados.csv


### Mostrar clientes por año

- **Método HTTP**: `GET`
- **URL**: `http://127.0.0.1:5000/clientes`
- **Descripción**: Este endpoint muestra los clientes

### Mostrar clientes

- **Método HTTP**: `GET`
- **URL**: `/clientes`
- **Descripción**: Este endpoint muestra los clientes
  
### Mostrar clientes por email

- **Método HTTP**: `GET`
- **URL**: `http://127.0.0.1:5000/clientes/<email>`
- **Descripción**: Este endpoint muestra los clientes por email

### Subir cliente

- **Método HTTP**: `POST`
- **URL**: `http://127.0.0.1:5000/clientes`
- **Descripción**: Subir cliente con json
  
#### Request Body (JSON)

El cuerpo de la solicitud debe ser un objeto JSON con los siguientes campos:

```json
{
  "nombre": "string",
  "apellido": "string",
  "email": "string",
  "teléfono": "string",
  "fechaRegistro": "YYYY-MM-DD"
}