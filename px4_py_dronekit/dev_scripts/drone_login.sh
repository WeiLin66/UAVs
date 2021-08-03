#!/bin/bash

curl --location --request POST 'http://mdrone.southeastasia.cloudapp.azure.com/apis/drone/checkin/' \
--header 'APIKey: om2bjq4Xqqd2ImMhwlJSxw' \
--header 'Content-Type: application/json' \
--data-raw '{
    "IP": "192.168.3.139",
    "RTSPURL": "null",
    "SerialNo": "oring-000001"
}'