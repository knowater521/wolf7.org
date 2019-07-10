#!/usr/bin/python
# -*- coding: utf-8 -*-
# aws bill cost alert
import json
import os
import sys
import argparse
import commands
import datetime
import logging
import time
from AWS_SendEmail import SendMail
from DingDing import SendMessage

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)
tomorrow = datetime.date.today() + datetime.timedelta(days=1)

Today_nyr = int(datetime.datetime.strftime(today, '%Y%m%d'))
Yesterday_nyr = int(datetime.datetime.strftime(yesterday, '%Y%m%d'))
Tomorrow_nyr = int(datetime.datetime.strftime(tomorrow, '%Y%m%d'))

# defined code director
code_dir = '.'
json_dir = 'template'
def SERVICE_ALERT_INFO():
    SERVICE_LIST = jsonData['ResultsByTime'][0]['Groups']
    START_TIME = jsonData['ResultsByTime'][0]['TimePeriod']['Start']
    END_TIME = jsonData['ResultsByTime'][0]['TimePeriod']['End']
    # Amount MAP { Defined AWS Service USD (dev,test,prod) }
    AMOUNT_MAP_DEVELOP = {
        "Amazon API Gateway": 1,
        "Amazon Simple Notification Service": 1,
        "AWS Lambda": 1,
        "Amazon Elasticsearch Service": 1,
        "Amazon Redshift": 1,
        "Amazon DynamoDB": 1,
        "Amazon ElastiCache": 1,
        "EC2 - Other": 5,
        "Amazon Elastic Compute Cloud - Compute": 5,
        "Amazon Elastic Load Balancing": 3,
        "Amazon MQ": 1,
        "Amazon Relational Database Service": 3,
        "Amazon Route 53": 3,
        "Amazon Simple Queue Service": 1,
        "Amazon Simple Storage Service": 3,
        "AmazonCloudWatch": 1,
        "AWS Cost Explorer": 1,
        "AWS Direct Connect": 1,
        "AWS Directory Service": 1,
        "AWS Glue": 1,
        "AWS Key Management Service": 1,
        "Amazon CloudFront": 1,
        "Amazon Elastic MapReduce": 1,
        "Amazon Kinesis Firehose": 1,
        "Amazon Simple Email Service": 1,
        "Matillion ETL for Amazon Redshift": 1,
        "AWS Elemental MediaStore": 5
    }
    AMOUNT_MAP_TESTING = {
        "Amazon API Gateway": 3,
        "Amazon Simple Notification Service": 3,
        "AWS Lambda": 5,
        "Amazon Elasticsearch Service": 3,
        "Amazon Redshift": 5,
        "Amazon DynamoDB": 3,
        "Amazon ElastiCache": 3,
        "EC2 - Other": 3,
        "Amazon Elastic Compute Cloud - Compute": 5,
        "Amazon Elastic Load Balancing": 5,
        "Amazon MQ": 3,
        "Amazon Relational Database Service": 5,
        "Amazon Route 53": 3,
        "Amazon Simple Queue Service": 3,
        "Amazon Simple Storage Service": 3,
        "AmazonCloudWatch": 3,
        "AWS Cost Explorer": 3,
        "AWS Direct Connect": 3,
        "AWS Directory Service": 3,
        "AWS Glue": 3,
        "AWS Key Management Service": 3,
        "Amazon CloudFront": 3,
        "Amazon Elastic MapReduce": 3,
        "Amazon Kinesis Firehose": 3,
        "Amazon Simple Email Service": 3,
        "Matillion ETL for Amazon Redshift": 13,
        "AWS Elemental MediaStore": 5
    }
    AMOUNT_MAP_PRODUCTION = {
        "Amazon API Gateway": 10,
        "Amazon Simple Notification Service": 3,
        "AWS Lambda": 10,
        "Amazon Elasticsearch Service": 5,
        "Amazon Redshift": 30,
        "Amazon DynamoDB": 3,
        "Amazon ElastiCache": 10,
        "EC2 - Other": 30,
        "Amazon Elastic Compute Cloud - Compute": 70,
        "Amazon Elastic Load Balancing": 20,
        "Amazon MQ": 3,
        "Amazon Relational Database Service": 80,
        "Amazon Route 53": 5,
        "Amazon Simple Queue Service": 5,
        "Amazon Simple Storage Service": 20,
        "AmazonCloudWatch": 7,
        "AWS Cost Explorer": 3,
        "AWS Direct Connect": 3,
        "AWS Directory Service": 10,
        "AWS Glue": 1,
        "AWS Key Management Service": 1,
        "Amazon CloudFront": 5,
        "Amazon Elastic MapReduce": 5,
        "Amazon Kinesis Firehose": 5,
        "Amazon Simple Email Service": 3,
        "Matillion ETL for Amazon Redshift": 30,
        "AWS Elemental MediaStore": 5
    }
    # defined send email information
    ENV_MAP = {
        "aws-dev": AMOUNT_MAP_DEVELOP,
        "aws-test": AMOUNT_MAP_TESTING,
        "aws-prod": AMOUNT_MAP_PRODUCTION
    }

    if account not in ENV_MAP:
        print "No parameters, please use " + (os.path.basename(__file__)) + "{prod,test,dev}"
        return

    target_map = ENV_MAP[account]
    print ">>>>>>AWS Account Name: " + account
    mail_msg = ''
    dingding_msg = ''
    for k in SERVICE_LIST:
        SERVICE = k['Keys'][0]
        UNIT = k['Metrics']['UnblendedCost']['Unit']
        AMOUNT = k['Metrics']['UnblendedCost']['Amount']
        if SERVICE in target_map:
            if float(AMOUNT) > target_map[SERVICE]:
                # Join Information
                mail_msg += "Service: " + SERVICE + "<br>Start Time: " + START_TIME + " " + "End Time: " + END_TIME + "<br>" + "<span style='color:red'>%s : %s</span>" % (
                UNIT, AMOUNT) + "<br>"
                dingding_msg += "Service: " + SERVICE + "\nStart Time: " + START_TIME + " " + "End Time: " + END_TIME + "\n" + UNIT + ": " + AMOUNT + "\n"
        else:
            print(" >>>>> ", SERVICE)
    if mail_msg == "":
        write_log(account, " is no loss.")
        print account, " is no loss."
    else:
        print (mail_msg)
        SendMail("Account: " + account + "<br>", mail_msg)
        print (dingding_msg)
        SendMessage("Account: " + account + "\n" + dingding_msg)

def write_log(log_file,log_text):
    THISFILEPATH = os.path.dirname(os.path.realpath(__file__))
    logfile = '{path}/logs/{log_file}.log'.format(path=THISFILEPATH, log_file=log_file)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s - [line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S %p',
                        filename=logfile,
                        # level=10,
                        filemode='a')
    logging.info(log_file + log_text.format(time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
if __name__ == '__main__':
    # input parameters {dev,test,prod}
    if len(sys.argv) < 2:
        print "No parameters, please use: \n", \
            os.path.abspath(os.path.dirname(__file__)) + (os.path.basename(__file__)), "aws-dev\n", \
            os.path.abspath(os.path.dirname(__file__)) + (os.path.basename(__file__)), "aws-test\n", \
            os.path.abspath(os.path.dirname(__file__)) + (os.path.basename(__file__)), "aws-prod"
        sys.exit()
    elif sys.argv[1]:
        account = sys.argv[1]
        # use input parameters get aws account last 24 hour billing json files
        if os.path.exists(code_dir):
            get_billing_info = commands.getstatusoutput('bash ' + code_dir + "/" + 'get_last_24_hour_bill.sh %s %s' % (account,json_dir))
            #get_billing_info = commands.getstatusoutput('pwd')
            if get_billing_info[0]  == 0:
                write_log(account,"get biling is success.")
            else:
                write_log(account,"get biling is failed.")
        # use input parameters variable open json file
        if os.path.exists(json_dir + "/" + account + '-bill.json'):
            with open(json_dir + "/" + account + '-bill.json', 'r') as f:
                jsonData = json.load(f)
                f.close()
                SERVICE_ALERT_INFO()
        else:
            print json_dir + "/" + account + '-bill.json is not exists'
            sys.exit(1)
