#!/usr/bin/python

import serial
import string
import sys
import json
import traceback
import subprocess
from datetime import datetime, timedelta
from statistics import mean
from db import *
from ml import *
from dotenv import load_dotenv
import os

load_dotenv()

def get_telemetry_irrigation(tel, port):
    output = " "
    jlist = []

    ser_level = serial.Serial(port, 9600, 8, 'N', 1, timeout=1)

    end_time = datetime.now() + timedelta(minutes=5)
    while end_time >= datetime.now():
        output = ser_level.readline()
        if (str(output).find("Read") != -1):
            ser_level.write(json.dumps(tel).encode())
            continue

        if((str(output) != "") & (str(output) != "b''") & (str(output).find("{}") == -1) & (output != "\r\n") & (str(output).find("kohm") == -1)):
            try:
                new_telemetry = json.loads(output)
                jlist.append(new_telemetry);
                #print(new_telemetry)
                if (len(jlist) == 2):
                    break;

            except Exception:
                # traceback.print_exc()
                output = " "
                continue

        output = " "
    
    return jlist

def get_telemetry(tel, port):
    output = " "
    jlist = []
    ser_level = serial.Serial(port, 9600, 8, 'N', 1, timeout=1)

    end_time = datetime.now() + timedelta(minutes=5)
    while end_time >= datetime.now():
        output = ser_level.readline()
        if (str(output).find("Read") != -1):
            ser_level.write(json.dumps(tel).encode())
            continue

        if((str(output) != "") & (str(output) != "b''") & (str(output).find("{}") == -1) & (output != "\r\n") & (str(output).find("kohm") == -1)):
            try:
                new_telemetry = json.loads(output)
                jlist.append(new_telemetry)
                if (len(jlist) == 2):
                    break;

            except Exception:
                # traceback.print_exc()
                output = " "
                continue

        output = " "
    
    return jlist


def insert_telemetry(jlist, records):
    print(records.insert_many(jlist))

def get_threshold_irrigation(jlist, outfile):

    threshold = mean(model_from_joblib.predict(jlist))
    f = open(outfile, "w")
    f.write(str(threshold))
    f.close()
