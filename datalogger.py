from mysql.connector import connect, Error
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

@dataclass
class table:
    """ Class for storing a table """
    name: str
    timestamp: bool=False
    id: bool=False
    link: str=None

    columns = list("")

    def create_query(self):
        query = list("")
        if self.id:  # If this column has an ID, add it
            query.append("id INTEGER NOT NULL PRIMARY KEY")
        if self.link is not None:
            query.append(f"{self.link}_id INT NOT NULL")
        if self.timestamp:  # If this column has a timestamp, add it
            query.append("timestamp TIMESTAMP NOT NULL")

        # Get the line to create each column
        query += [i.make_sql_line() for i in self.columns]

        if self.link is not None:
            query.append(f"FOREIGN KEY ({self.link}_id) REFERENCES {self.link}(id)")



        output = f"CREATE TABLE {self.name} (" + ','.join(query) + ");"
        return output

        
    def add_column(self, name, datatype):
        """ Adds a column to the columns list
        """
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
    cursor = None

    def __init__(self, host, username, password, database, schema_file):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.schema_file = schema_file

        self.__schema_generate()
        self.connect()
        # self.schema_status = self.check_schema

    def __delete__(self):
        self.disconnect()

    def connect(self):
        """ Connects to the SQL server
        TODO: Throw error when connection fails (not there for now for testing)
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
        if not self.connection.is_connected():  # If not connected, then connect
            print("Error: Not connected to server")
            return -1

        # It's connected now, so run the query
        if self.cursor is None:
            print("Error: No cursor")
            return -1

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except Error as e:
            return e
        
        return result


    def __schema_generate(self):
        """ Generates a schema from the given .xml file
            ! Needs to be run each startup
        """
        tree = ET.parse(self.schema_file)
        root = tree.getroot()

        schema = []  # Clear the schema
        for cur_table in root:
            if "timestamp" in cur_table.attrib.keys() and cur_table.attrib['timestamp'] == "True": 
                timestamp = True
            else:
                timestamp = False

            if "id" in cur_table.attrib.keys() and cur_table.attrib['id'] == "True": 
                id = True
            else:
                id = False

            if "link" in cur_table.attrib.keys():
                link = cur_table.attrib['link']
            else:
                link = None

            self.schema.append(table(name=cur_table.attrib["name"], timestamp=timestamp, id=id, link=link))

            for cur_column in cur_table:
                self.schema[-1].add_column(cur_column.attrib['name'], cur_column.text)
    
    def schema_get_query(self):
        # Returns a query to create each table
        return [table.create_query() for table in self.schema]

    def schema_validate(self):
        # SHOW COLUMNS FROM {table}
        tables = {}
        for table in self.schema:
            self.cursor = self.connection.cursor()
            result = self.query(f"SHOW COLUMNS FROM {table.name}")

            if type(result) == list:
                tables[table.name] = {i[0]:[i[1], i[2], i[3], i[4]] for i in result}
            else:
                tables[table.name] = result
        self.cursor.close()
        print(tables)

        
    def schema_create(self, force=False):
        
        if not force:
            question = input("Drop tables and create new ones? y/(n)") + 'n'
            
            if question[0] != 'y':
                print("Schema create canceled")
        pass


if __name__ == "__main__":
    # Variable setup
    with open("credentials.txt") as file:
        cred = [i.strip() for i in file.readlines()]
        host = cred[0]
        username = cred[1]
        password = cred[2]

    database = "test1"
    schema_file = "schema.xml"

    # Start of the actual function stuff
    data = datalogger(
        host=host, 
        username=username, 
        password=password, 
        database=database, 
        schema_file=schema_file)
    
    schema = data.schema_get_query()
    print(data.schema_validate())
    data.schema_create()