# Prague Public Transport App
Mobile app for searching public traffic connections within Prague Integrated Transport System.
Internet connection is not necessary to search for the transportation data.

Provider of the open traffic data: <a href="https://pid.cz/">PID</a>.

## Compatibility
Compatible with Python 3.7. Tested on Windows 10.

## Version
This is version 0.0.1. Development is ongoing.
Pull requests with improvements are welcome.

## Before running the script
Following file needs to be downloaded:

`PID_GTFS.zip` - can be downloaded from the <a href="http://data.pid.cz/PID_GTFS.zip">PID Open Data server</a>. Store it in the `data` folder.

## Run the script

1. download the file mentioned above

2. install `gtfspy` from my forked repo: `pip install -e git+git@github.com:evelyn9191/gtfspy.git@master#egg=gtfspy`

3. install dependencies from `requirements.txt`

4. Run `import_gtfs_data.py` to create the database and import the data

5. Run `search_trip_screen.py` to run the app.
