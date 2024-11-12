import re
import sqlite3

from TechnicalTestPy.Controllers.db.ConnectDb import ConnectDb

import pandas as pd

class Client:
    def __init__(self, client):
        self.client = client
    ''' Normaliza el archivo .csv de clientes en los cuales
        Capitaliza los nombres apellidos
        Valida el email
        Valida un formato estandar de telefonia
    '''
    def normalization(self):
        try:
            self._capitalize(columns=['Nombre','Apellido'])
            self._formatEmail(column='Email')
            self._formatPhone(column='Teléfono')

            return True,self.client, None
        except Exception as e:
            return False,None, e

    def _capitalize(self,columns):
        missing_columns = [col for col in columns if col not in self.client.columns]

        if missing_columns:
            raise ValueError(f"Las columnas {missing_columns} no se han encontrado en el DataFrame.")

        for col in columns:
            if col in self.client.columns:
                self.client[col] = self.client[col].apply(lambda x: x.title() if isinstance(x, str) else x)

    def _formatEmail(self, column):
        if column in self.client.columns:
            # Define el patrón para el correo electrónico
            pattern = r'^[0-9]*[A-Za-z.]+[0-9]*@[A-Za-z.]+\.[A-Za-z]{2,}$'

            # Filtramos las filas con valores no válidos o NaN en la columna de correo
            self.client[column] = self.client[column].apply(
                lambda email: email if pd.notna(email) and re.match(pattern, str(email)) else None)

            # Filtramos las filas donde la columna de correo electrónico sea NaN (no válido)
            self.client = self.client.dropna(subset=[column])

        else:
            raise ValueError(f"La columna '{column}' no se ha encontrado.")

    def _formatPhone(self, column):
        if column in self.client.columns:
            # Define el patrón para un número de teléfono limpio (solo números y longitud válida)
            pattern = r'^\d{9,11}$'

            # Recorre cada fila del dataframe
            for i in range(len(self.client)):
                phone = self.client.iloc[i][column]

                # Si el valor es NaN o 'NaN' lo ignoramos
                if pd.isna(phone) or phone == 'NaN':
                    continue

                # Limpia el número, eliminando caracteres no numéricos
                clear_phone = re.sub(r'[^0-9]', '', phone)

                # Si el teléfono no cumple con el patrón (9-11 dígitos), lo reportamos
                if not re.match(pattern, clear_phone):
                    print(f"El teléfono {phone} no cumple con el formato especificado. Limpiado: {clear_phone}")

            # Aplicamos la validación y filtramos las filas que no cumplen con el formato correcto
            self.client = self.client[self.client[column].apply(
                lambda phone: bool(re.match(pattern, re.sub(r'[^0-9]', '', phone)))
            )]

            print(self.client)
        else:
            raise ValueError(f"Las columna '{column}' no se ha encontrado.")

    ''' Realiza un insert del archivo .csb normailizado a la tabla de cliente'''
    def addClients(self):
        db_connection = ConnectDb(dbPath='../TechnicalTestPy/SQL/sql.db')  # Instancia de la clase ConnectDb
        conn = db_connection.connect_sqlite()  # Obtener la conexión a la base de datos
        if conn:
            try:
                self.client.to_sql('clientes', con=conn, if_exists='replace', index=False)

                query_result = conn.execute("SELECT * FROM clientes").fetchall()
                print(query_result)
                return True, query_result, None
            except sqlite3.Error as e:
                print(f"Error al insertar datos: {e}")
                return False, None, e
            finally:
                db_connection.close_connection(conn)

    ''' Selecciona los clientes de la base de datos'''
    def getClients(self):
        db_connection = ConnectDb(dbPath='../TechnicalTestPy/SQL/sql.db')  # Instancia de la clase ConnectDb
        conn = db_connection.connect_sqlite()  # Obtener la conexión a la base de datos
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM clientes")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            client_df = pd.DataFrame(rows, columns=columns)
            return client_df
        except sqlite3.Error as err:
            print(f"Error al consultar los datos: {err}")
        finally:
            db_connection.close_connection(conn)

    ''' Cuenta los clientes por año segun la columna fechaRegistro en una vista de base de datos previamente creada.'''
    def getClientsbyYear(self=None):
        db_connection = ConnectDb(dbPath='../TechnicalTestPy/SQL/sql.db')
        conn = db_connection.connect_sqlite()

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientByYear_view;")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            print(f"{', '.join(columns)}")

            for row in rows:
                print(f"{', '.join(map(str, row))}")

            client_df = pd.DataFrame(rows, columns=columns)
            return client_df

        except sqlite3.Error as e:
            return False, None, str(e)
        finally:
            db_connection.close_connection(conn)

    ''' Busca clientes por correo electronico'''
    def getClientsbyEmail(self, email):
        db_connection = ConnectDb(dbPath='../TechnicalTestPy/SQL/sql.db')  # Instancia de la clase ConnectDb
        conn = db_connection.connect_sqlite()  # Obtener la conexión a la base de datos
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM clientes WHERE email LIKE ?",(f'%{email}%',))
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            client_df = pd.DataFrame(rows, columns=columns)
            return client_df
        except sqlite3.Error as err:
            print(f"Error al consultar los datos: {err}")
        finally:
            db_connection.close_connection(conn)

    ''' Crea clientes por una entrada JSON del cliente'''
    def createClient(newClient):
        db_connection = ConnectDb(dbPath='../TechnicalTestPy/SQL/sql.db')  # Instancia de la clase ConnectDb
        conn = db_connection.connect_sqlite()  # Obtener la conexión a la base de datos
        cursor = conn.cursor()
        try:
            cursor.execute('''
                  INSERT INTO clientes (nombre, apellido, email, teléfono,fechaRegistro)
                  VALUES (?, ?, ?, ?, ?)
              ''', (newClient['nombre'], newClient['apellido'], newClient['email'], newClient['teléfono'],newClient['fechaRegistro']))

            conn.commit()
            return True, None
        except sqlite3.Error as e:
            print(f"Error al insertar en la base de datos: {e}")
            return False, str(e)
        finally:
            conn.close()

