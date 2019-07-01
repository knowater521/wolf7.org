#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import argparse
import boto3
import datetime

json_demo1 = """
    {
    "ResultsByTime": [
        {
            "Estimated": true,
            "Total": {},
            "TimePeriod": {
                "Start": "2019-06-30",
                "End": "2019-07-01"
            },
            "Groups": [
                {
                    "Keys": [
                        "EC2 - Other"
                    ],
                    "Metrics": {
                        "UnblendedCost": {
                            "Unit": "USD",
                            "Amount": "1.9862157612"
                        }
                    }
                },
                {
                    "Keys": [
                        "Amazon Elastic Compute Cloud - Compute"
                    ],
                    "Metrics": {
                        "UnblendedCost": {
                            "Unit": "USD",
                            "Amount": "5.5587805146"
                        }
                    }
                }
            ]
        }
    ],
    "GroupDefinitions": [
        {
            "Key": "SERVICE",
            "Type": "DIMENSION"
        }
    ]
    }
"""
jsonData = json.loads(json_demo1)
#print jsonData
START_TIME = jsonData['ResultsByTime'][0]['TimePeriod']['Start']
END_TIME = jsonData['ResultsByTime'][0]['TimePeriod']['End']
EC2_OTHER_KEYS = jsonData['ResultsByTime'][0]['Groups'][0]['Keys'][0]
EC2_OTHER_AMOUNT = jsonData['ResultsByTime'][0]['Groups'][0]['Metrics']['UnblendedCost']['Amount']
EC2_KEYS = jsonData['ResultsByTime'][0]['Groups'][1]['Keys'][0]
EC2_AMOUNT = jsonData['ResultsByTime'][0]['Groups'][1]['Metrics']['UnblendedCost']['Amount']
if EC2_OTHER_KEYS == "EC2 - Other":
	if float(EC2_OTHER_AMOUNT) > 1:
		print ("Service: %s, Start_time: %s End_time: %s, Billing Detail: %s " % (EC2_OTHER_KEYS,START_TIME,END_TIME,EC2_OTHER_AMOUNT))
if (EC2_KEYS) == "Amazon Elastic Compute Cloud - Compute":
	if float(EC2_AMOUNT) > 6:
		print ("Service: %s, Start_time: %s End_time: %s, Billing Detail %s" % (EC2_KEYS,START_TIME,END_TIME,EC2_AMOUNT))
