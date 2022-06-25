#!/bin/sh

sleep 5s

mavproxy.py --master=/dev/ttyACM0 --out=udpin:0.0.0.0:14550 --out=udpout:10.27.0.13:14551 --out=udpin:0.0.0.0:14552
