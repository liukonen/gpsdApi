# GPS API Flask App

This is a Flask application that interacts with a GPS device using the `gpspipe` command-line tool to retrieve GPS data and check the device's connection status.

If anyone has a better way of calling the GPSD service, please feel free to update, clone, or fork this project. The goal was to create a simple REST API for indicating the system's availability.

## Background

I have a cheap USB device that gathers time signals from satellites, which is crucial for GPS positioning. To set up the GPS device and utilize it as a time server, I followed the directions provided in the following resources:

- [Building a GPS-Based Time Server](https://www.jacobdeane.com/iot/2020/building-a-gps-based-time-server/)
- [Raspberry Pi Stretch GPS Dongle as a Time Source with Chrony Timedatectl](https://photobyte.org/raspberry-pi-stretch-gps-dongle-as-a-time-source-with-chrony-timedatectl/)

Since I already had Python running on my machine for the GPS tools, I decided to build an API and user interface around the GPSD project.

## Usage

1. Start the Flask application using Gunicorn:
``` bash
start.sh
``` 
2. Access the application in your browser at `http://localhost:9999`.

## Endpoints

The following endpoints are available:

### GET /

- Renders the index.html template.

### GET /gps

- Retrieves GPS data from the connected GPS device.
- Returns a JSON response with the GPS data.
- Please note that due to the 2-second call to the `gpspipe` command, the time values may be up to 2 seconds off as we wait for the API to return the values.

### GET /health

- Checks the health status of the GPS device.
- Returns a JSON response with the device's status (OK if connected, an error message if not connected).

## Error Handling

The application includes error handlers for the following status codes:

- 400 Bad Request
- 500 Internal Server Error

If any of these errors occur, a JSON response with an appropriate error message will be returned.

## Logging

The application utilizes the Python `logging` module and SeqLog for logging messages. By default, the logs are sent to the console for ease of setup and demonstration. However, for a production setup, the logs can be configured to be sent to a Seq server for centralized logging and monitoring.

## Configuration

- The IP address and port of the Flask application can be modified in the Gunicorn command or through Gunicorn configuration options.

Feel free to customize the README further to include any other relevant information or instructions specific to your use case.
