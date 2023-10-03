import mysql.connector


class DatabaseConnection:
    _connection = None
    _config = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            cls._connection = mysql.connector.connect(
                host=cls._config['DATABASE_HOST'],
                user=cls._config['DATABASE_USERNAME'],
                port=cls._config['DATABASE_PORT'],
                password=cls._config['DATABASE_PASSWORD'],
                database=cls._config['DATABASE_NAME']
            )

        return cls._connection

    @classmethod
    def set_config(cls, config):
        cls._config = config

    @classmethod
    def execute_query(cls, query, params=None):
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        cls._connection.commit()

        return cursor

    @classmethod
    def fetch_all(cls, query, params=None):
        with cls.get_connection().cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    @classmethod
    def fetch_one(cls, query, params=None):
        with cls.get_connection().cursor(buffered=True) as cursor:  # Uso del cursor bufferizado
            cursor.execute(query, params)
            result = cursor.fetchone()  # Recuperar el resultado antes de que el cursor se cierre
            cursor.fetchall()  # Asegurarse de que se han leído todos los resultados
        return result

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
