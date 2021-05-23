# Testing datalogger (For MySQL)

## For logging data to databases without all the stuff around it

1. Setup the .xml (or just use the built in one)
2. Follow the starting guide
3. Make some data
4. Query the data back not using this, cause I haven't got that far

1.0 TODO

- [x] Database: Connect to database
- [x] Database: Make queries
- [x] Database: Get schema
- [ ] Database: Compare schema with schema.xml (somehow)
  - [ ] Return true or false if the current schema is correct
  - [ ] Warn user if it's incorrect without them having to check
- [x] Schema file : schema.xml file
- [x] Schema file : Turn schema.xml into some sort of python structure
- [ ] Data: Make a log function
- [ ] Detect what data type is coming into the log function and put it into relevant tables

2.0 TODO?? (Maybe?)

- [ ] Restrict the test name and data point tables to simplify the concept of this function
- [ ] Error when schema file is invalid (path)
- [ ] Get data back

## Use of the lib

1. Create the class with the following database parameters and path (relative or absolute) to the schema.xml

```Python
data = datalogger(
    host=host,
    username=username,
    password=password,
    database=database,
    schema_file=schema_file)
```

2. After that, verify if the database has a matching schema using schema_validate(), which returns a True or a desctiption of which tables are incorrect

```Python
data.schema_validate()
```

**NOTE**: Does not check for auto indexing or other features, just table name and type

3. If the current schema is incorrect, either manually correct it, or use schema_create, which drops any existing named tables and creates new ones in place of them. (Use force=True to not be prompted if you're sure)

```Python
data.schema_create(force=True)
```

## Functions
