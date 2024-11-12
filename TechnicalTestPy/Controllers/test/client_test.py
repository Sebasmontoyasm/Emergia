import pytest
import pandas as pd
from TechnicalTestPy.Controllers.client.Client import Client  # Asegúrate de importar correctamente tu clase Cliente


# Fixture para crear un DataFrame de ejemplo
@pytest.fixture
def example_client():
    data = {
        'nombre': ['juan', 'maria', 'pedro'],
        'apellido': ['perez', 'garcia', 'lopez'],
        'email': ['juan@example.com', 'maria@example.com', 'pedro@example.com'],
        'FechaRegistro':['2023-11-11','2024-10-09','2021-05-03']
    }
    df = pd.DataFrame(data)
    return Client(df)

# Test para verificar la capitalización correcta de las columnas
def test_capitalize_columns(example_client):
    # Capitalizar las columnas 'nombre' y 'apellido'
    example_client._capitalize(['nombre', 'apellido'])

    # Verificar que las columnas 'nombre' y 'apellido' estén capitalizadas correctamente
    assert example_client.client['nombre'][0] == 'Juan'
    assert example_client.client['apellido'][0] == 'Perez'
    assert example_client.client['nombre'][1] == 'Maria'
    assert example_client.client['apellido'][1] == 'Garcia'
    assert example_client.client['nombre'][2] == 'Pedro'
    assert example_client.client['apellido'][2] == 'Lopez'


# Test para verificar que se lanza un error si una columna no existe
def test_capitalize_column_not_found(example_client):
    with pytest.raises(ValueError) as exc_info:
        example_client._capitalize(['nombre', 'non_existent_column'])

    # Verificar que se lanzó el error con el mensaje esperado
    assert "Las columnas ['non_existent_column'] no se han encontrado en el DataFrame." in str(exc_info.value)


# Test para verificar que las columnas que no contienen cadenas no se ven afectadas
def test_capitalize_non_string_column(example_client):
    # Agregar una columna con valores numéricos
    example_client.client['edad'] = [20, 25, 30]

    # Capitalizar solo 'nombre' y 'apellido'
    example_client._capitalize(['nombre', 'apellido'])

    # Verificar que la columna 'edad' no se vea afectada
    assert example_client.client['edad'][0] == 20
    assert example_client.client['edad'][1] == 25
    assert example_client.client['edad'][2] == 30