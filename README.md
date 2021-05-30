# Testing datalogger (For MySQL)

- [Testing datalogger (For MySQL)](#testing-datalogger-for-mysql)
  - [Introduction - What even is this?](#introduction---what-even-is-this)
    - [TLDR](#tldr)
    - [Have time to read a story?](#have-time-to-read-a-story)
  - [For logging data to databases without all the stuff around it](#for-logging-data-to-databases-without-all-the-stuff-around-it)
  - [Use of the lib](#use-of-the-lib)
  - [The schema used in this lib](#the-schema-used-in-this-lib)
    - [+Test](#test)
    - [+Point](#point)
    - [+Data_{Type}](#data_type)
  - [To do list](#to-do-list)

## Introduction - What even is this?

### TLDR

I want an easy way to log data to a database using quickly thrown together Python scripts.

The data is separated into tables to make storing it more intuitive. The basic structure is outlined below

- **Test Name** - Stores a test name, starting timestamp and an ID
- **Data Point** - Stores the time elapsed, the source of the data, the ID of the related Test Name and it's own ID
- **Data (Int, String etc.)** - A series of tables which relate to a data point. They contain the ID of the related data point and an int or a string or whatever they're setup to store

### Have time to read a story?

In my work, I do product testing, which involves logging data every few seconds for days on end. I'm usually doing multiple tests with multiple computers. I currently log to a .csv file, cause it's really easy. It doesn't matter what computer I log onto, as it's just a file on the hard drive which gets made on the fly.

The .csv files come with some advantages and disadvantages

- Advantages
  - File gets made in the folder the script is
  - Easy to delete false starts for tests
  - 
- Disadvantages
  - If I block the file by reading or writing at the wrong time it can crash python scripts
  - It's hard to get live data from my work compter
  - Large text files can be cumbersome to move around


I've been using National Instruments Test Stand and have grown to love the code-less-ness of how they manage logging to a database. 

I want to make something similarly simple in python to both make my life easier when setting up quick tests and also allow others to have a go at seeing the absolute power of a well made database.

My primary goals for this project are the following

- Make a very simple database wrapper
  - Simple enough for a completely new database user to use a database
  - Complex enough to show the power of joining tables
  - Customisable enough to allow logging of non-standard data
- Learn how to manage a programming project to allow it to be completed
  - limit scope to have multiple releases
  - Manage releases with detailed changelogs

My secondary goals for this project are the following

- Learn how to use Git Hub (I've used it for ages, but never well)
- Learn how to make a Python library (I wanna go pip install thislib)
- Be featured somewhere because someone liked my library


## For logging data to databases without all the stuff around it

1. Setup the .xml (or just use the built in one)
2. Follow the starting guide
3. Make some data
4. Query the data back not using this, cause I haven't got that far

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

## The schema used in this lib

The schema used in this list separates a lot of the data out into separate tables. To get the data back, joins will be needed to get everything back into an easy to read and process list.

### +Test

This list is the heart of the database. It simply contains all of the started tests with a start time

- ID - INT primary key
  - Unique identifier for each item in this table
- Test - String
  - Name of the test
- Details - String Nullable
  - Details to explain the test (if the user wants to)
- START_TIME - Integer
  - The unix timestamp in milliseconds when the test started

### +Point

A point doesn't actually contain the data. It's designed to allow the user to give the user flexibility to log data with heaps of individual points, which may not be in sync with each other, while also having the ability to assign a lot of diffent bits of data to a single data point.

For example. If you have an instrument which gives data every 2 seconds and one which gives data every 3 seconds. You can either buffer the slower instrument, which could introduce error, or just log data as it comes in and use a tool to plot the data by time later.

- ID - INT primary key
  - Unique identifier for each item in this table
- TEST_ID - INT foriegn key
  - Unique identifier of the test this data point belongs to
- ELAPSED_TIME - Integer
  - How many milliseconds that have elapsed since the test started
- DESCRIPTION - String Nullable
  - A string to label the data point (if the user wants to)

### +Data_{Type}

Actually stores data which you're wanting to store. Links back to a data point, which then links back to the test.

Planned data types are as follows:

- String
- Int
- Float (probably gonna end up being a double)
- Boolean

This table isn't given it's own ID, as I don't think it's necassary.

- POINT_ID - INT foriegn key
  - Unique identifier which this data belongs to
- Identifier - String
  - What this data point relates to
- Data - Variable
  - FINALLY! The actual data to be stored. There will be a table for each type of data

## To do list

- [ ] **Needed functions to get database ready**
  - [x] Connect to database
  - [ ] Get schema from database
    - [x] Query function
  - [ ] Compare collected database schema with wanted schema
    - [ ] Fix schema (might need a user prompt for this)
      - [ ] Nuclear method: Drop all non compliant tables and remake
      - [ ] Safe method: Adjust tables to try to preserve data

- [ ] **Log data function**
  - [ ] Log data (MAYBE with an overloaded function)
    - I'm thinking of using an overloaded function (or a function which doesn't care what type of data you're throwing at it) to make it simpler to log data. It *may* be better to give the user control. Possibly give both options.
    - [ ] Integer
    - [ ] Floating point (probably a double)
    - [ ] String
    - [ ] Bool

Thoughts of stuff I want to add in the future

- [ ] **Error management**
  - Still trying to decide whether to try and handle errors on the fly as much as possible without crashing the script. I don't want logging of tests to stop because something minor went wrong, but on the other hand some of the issues could become a real problem if not handled properly by the user..
  - [ ] Handle failed connections to servers (buffer queries somehow?)
    - [ ] Buffer failed queries even if the script ends?

- [ ] **Bonus Points**
  - [ ] A way to manage tests on the database
    - This may work better as a separate class, as grabbing data usually won't be used at the same time as logging
    - [ ] List
    - [ ] Download to file
    - [ ] Delete
    - [ ] Clear all data?
  - [ ] Different timestamp formats
    - The UNIX timestamp is quite useful, but it isn't the end all be all of timestamps
    - [ ] datetime (BONUS with timezone offset)
  - [ ] Have a separate, user configurable table for test details
    - To allow a user to build their own system of identifying tests
  - [ ] Use a dynamically updating ENUM to save space in some places
    - Some of the fields will only have a few options, but be repeated a massive amount of times. It will be far more efficient to store as an enum
    - [ ] On the Point table
      - [ ] Description - There will only be a few point descriptions
    - [ ] On the Data table - Most important one (in my mind)
      - [ ] Identifier - These will say which instrument/channel 
