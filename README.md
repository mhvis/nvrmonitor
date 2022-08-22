# NVR monitor

Health check endpoint to monitor NVR recordings.

I use [tiny-nvr](https://github.com/hpaolini/tiny-nvr)
to store a continuous recording of our IP cameras to a Linux server. To monitor these recordings, this tool
checks the destination folder and exposes a health check endpoint that returns a HTTP error when a recording becomes stale.
I use Uptime Robot to monitor the endpoint, this way I receive a push notification whenever the endpoint returns
an error or is offline for whatever reason (power outage, misconfiguration, ..).

## Configuration

This image looks for subfolders under `/recordings` and assumes each subfolder is a separate camera.
It checks for each subfolder that the most recent recording is fresh.
For instance if you have two cameras in the folders `cam1` and `cam2`, mount them under `/recordings/cam1`
and `/recordings/cam2`.
This tool finds the most recent recording in each folder and checks that the modification time is recent.

Configuration environment variables:

* `NVR_MAX_AGE`: Maximum age of the last modified file in seconds. Default: 60.



## Docker Compose

```yaml
services:
  monitor:
    image: mhvis/nvrmonitor
    restart: unless-stopped
    environment:
      NVR_MAX_AGE: 60
    volumes:
      - /path/to/cam1:/recordings/cam1:ro
      - /path/to/cam2:/recordings/cam2:ro
    ports:
      - 8000:8000
