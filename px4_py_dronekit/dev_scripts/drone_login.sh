#!/bin/bash

curl -k -X POST "https://10.1.181.230/apis/drone/checkin/" -H "accept: application/json" -H "APIKey: AWFJ1hYT4r8XRsxUOKXpcA" -H "Content-Type: application/json" -d "{\"IP\":\"10.27.0.13\",\"RTSPURL\":\"rtsp://10.27.0.13:554/test.mp4\",\"SerialNo\":\"oring-000001\"}"
