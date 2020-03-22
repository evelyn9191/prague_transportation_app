# Prague Public Transport App
Mobile app for searching public traffic connections within Prague Integrated Transport System.
Internet connection is not necessary to search for the transportation data.

Provider of the open traffic data: <a href="https://pid.cz/">PID</a>.

## Compatibility
Compatible with Python 3.7 (due to pypiwin32 library). Tested on Windows 10.

## Version
This is version 0.0.1. Development is ongoing.
Pull requests with improvements are welcome.

## Before running the script
Following file needs to be downloaded:

`PID_GTFS.zip` - can be downloaded from the <a href="http://data.pid.cz/PID_GTFS.zip">PID Open Data server</a>. Store it in the `data` folder.

## Run the script

1. Install dependencies from `requirements.txt`


2. Run `transport_app/import_gtfs_data.py` to import the latest transport data.


3. Run `transport_app/gui/search_trip_screen.py` to run the app.
