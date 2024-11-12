import pandas as pd
class ExtractData:
    def __init__(self, file_path, file_type):
        """
        Constructor de la clase que inicializa la ruta del archivo y el tipo de archivo.
        :param file_path: Ruta al archivo.
        :param file_type: Tipo de formato del archivo (e.g., 'csv', 'excel', 'json').
        """
        self.file_path = file_path
        self.file_type = file_type.lower()

    def readFile(self):
        """
        Lee el archivo en función del tipo de formato especificado y devuelve un DataFrame de pandas.
        :return: DataFrame con el contenido del archivo.
        """
        try:
            if self.file_type == '.csv':
                return pd.read_csv(self.file_path)
            elif self.file_type == '.xls' or self.file_type == '.xlsx':
                return pd.read_excel(self.file_path)
            else:
                raise ValueError(f"Tipo de archivo '{self.file_type}' no soportado.")
        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo '{self.file_path}' no fue encontrado.")
        except Exception as e:
            raise Exception(f"Error al leer el archivo: {e}")

    def save_to_csv(self,dataFrame, filename="../output/clientes_normalizados.csv"):
        try:
            dataFrame.to_csv(filename, index=False)
            print(f"El archivo ha sido guardado como {filename}")
        except Exception as e:
            print(f"Hubo un error al guardar el archivo: {e}")




