from mysql.connector import connect, Error
import xml

class datalogger():
    connection = None
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

        self.connect()
        # self.schema_status = self.check_schema

    def __delete__(self):
        self.disconnect()

    def connect(self):
        """ Connects to the SQL server
        """
        try:
            self.connection = connect(
                host=self.host,
                user=self.username,
                password=self.password)
        except Error as e:
            print(e)
            self.connected = False
            return e.errno

        self.connected = True
        return 0
        

    def disconnect(self):
        self.connection.close()
        self.connection = None
        self.connected = False

    def query(self, query):
        """ Checks if currently connected, if not connects. Then sends query
        """
        if not self.connected:  # If not connected, then connect
            self.connect()

        # It's connected now, so run the query
        self.__run_query(query)

        if not self.connected:  # Disconnect after to clean up the connection
            self.disconnect()


    def __run_query(self, query):
        """ Actually runs the query
        """
        

    def check_schema(self):
        """ Checks that the schema is valid to the .xml file
        """
        pass


if __name__ == "__main__":
    with open("credentials.txt") as file:
        cred = [i.strip() for i in file.readlines()]
        host = cred[0]
        username = cred[1]
        password = cred[2]

    database = "Test_data"
    data = datalogger(host, username, password, database)
    print(data.connection_status)