from mysql.connector import connect, Error
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

@dataclass
class table:
    """ Class for storing a table """
    name: str
    datetime: bool
    id: bool

    columns = list("")

    def create_query(self):
        pass

    def add_column(self, name, datatype):
        self.columns.append(column(name=name, datatype=datatype))

    def make_query(self):
        [i.make_sql_line() for i in self.columns]

@dataclass
class column:
    """ Class for storing a column """
    name: str
    datatype: str 

    def make_sql_line(self):
        """ Generates the SQL line to create this column
        """
        return f"{self.name} {self.datatype}"


class datalogger():
    connection = None
    schema = []
    def __init__(self, host, username, password, database, schema_file):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.schema_file = schema_file

        self.generate_schema()
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
                password=self.password,
                database=self.database)
        except Error as e:
            print(e)
            self.connected = False
            return e.errno

        self.connected = True
        return 0
        

    def disconnect(self):
        if self.connection is not None:
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

    def generate_schema(self):
        """ Generates a schema from the given .xml file
            ! Needs to be run each startup
        """
        tree = ET.parse(self.schema_file)
        root = tree.getroot()

        schema = []  # Clear the schema
        for cur_table in root:
            if "datetime" in cur_table.attrib.keys() and cur_table.attrib['datetime'] == "True": 
                datetime = True
            else: 
                datetime = False
            if "id" in cur_table.attrib.keys() and cur_table.attrib['id'] == "True": 
                id = True
            else: 
                id = False

            self.schema.append(table(name=cur_table.attrib["name"], datetime=datetime, id=id))

            for cur_column in cur_table:
                self.schema[-1].add_column(cur_column.attrib['name'], cur_column.text)
        


    def __run_query(self, query):
        """ Actually runs the query
        """
        pass
        
    def create_database(self):
        pass
    
    def create_schema(self):
        pass

    def create_schema(self):
        pass

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
    schema_file = "data_type.xml"
    data = datalogger(
        host=host, 
        username=username, 
        password=password, 
        database=database, 
        schema_file=schema_file)
    print(data.connection_status)