#!/usr/bin/python
# -*- coding: utf-8 -*-
#GIT_REPO = 'git@git.wolf7.org:wolf7-business/'
GIT_REPO = 'git@git.wolf7.org:wolf7/'
EB_COMMAND = '/usr/local/bin/eb'
AWS_COMMAND = '/usr/local/bin/aws'
#EB_COMMAND = '/var/lib/jenkins/.local/bin/eb'
#AWS_COMMAND = '/var/lib/jenkins/.local/bin/aws'
CODE_PATH = '/data/code'
import os
import tarfile
import sys
import shutil
import time

# clone repository code
def ADD_ENV_OF_ELB():
    code_name = raw_input('Input your gitlab repository name: ')
    print 'Your code name is %s ' % (code_name)
    # Clone code for git repo
    if os.path.isdir(CODE_PATH):
        print "OK , code director check success, Start clone code...."
        os.chdir(CODE_PATH)
        os.system('git clone ' + (GIT_REPO) + (code_name) + ".git")
        # AWS CLI COMMAND
        code_dir = CODE_PATH + '/' + (code_name)
        if os.path.isdir(code_dir):
            print "code_dir: %s exist exec AWS command..." % (code_dir)
            aws_profile_name = raw_input("Input Your AWS env name: ")
            os.system('%s configure --profile %s ' % (AWS_COMMAND,aws_profile_name))
        else:
            print "code_dir is not exist."
            sys.exit()
        # EB CLI COMMAND
        if os.path.isdir(code_dir):
            print "code_dir: %s is OK exec EB command..." % (code_dir)
            os.chdir(code_dir)
            os.system(EB_COMMAND + ' init --profile %s ' % (aws_profile_name))
            os.system(EB_COMMAND + ' list --profile  %s ' % (aws_profile_name))
        else:
            print "code_dir is not exist."
#ADD_ENV_OF_ELB()

def ADD_ENV_OF_EC2():
    code_name = raw_input('Input your environment name: ')
    # Clone code for git repo
    if os.path.isdir(CODE_PATH):
        print "OK code director check success, Start clone code...."
        os.chdir(CODE_PATH)
        os.system('git clone ' + (GIT_REPO) + (GIT_REPO) + ".git")
        code_dir = (CODE_PATH) + '/' + (code_name)
        if os.path.isdir(code_dir):
            print "code clone success."
        else:
            print "code clone failed."
        HOST_IP = raw_input("input your server ip or domain name: ")
        HOST_USER = raw_input("input your server user name: ")
        print "Using User: %s Login to SERVER HOST: %s." % (HOST_USER,HOST_IP)
        print "Copy The Jenkins-SSH-KEY to Login User %s ~/.ssh/authorized_keys." % (HOST_USER)
        print "Use Command: chmod 600 ~/.ssh/authorized_keys."
        print "Jenkins-SSH-KEY: "
        os.system('cat ~/.ssh/id_rsa.pub')
#ADD_ENV_OF_EC2()

#
def list_op():
    while len(sys.argv):
        if sys > 0:
            print "Input number 1'  ADD EC2 ENV."
            print "Input number 2'  ADD ELB ENV."
            print "Input 'q' to EXIT."
            INPUT = raw_input("Plase Input : ")
            # EC2
            if INPUT == '1':
                print 'OK , EXEC ADD EC2 ENV'
                ADD_ENV_OF_EC2()
                print 'OK,ADD EC2 ENV DONE'
                break
            # ELB
            if INPUT == '2':
                print 'OK , EXEC ADD ELB ENV'
                ADD_ENV_OF_ELB()
                print 'OK,ADD ELB ENV DONE'
                break
            # EXIT
            if INPUT == 'q':
                print 'QUIT'
                break
            else:
                print "plase Enter Your Input: "
                pass

#参数
if len(sys.argv) < 2:
    print "input wrong. please usage: \n" \
          "./" + (os.path.basename(__file__)),"1 add EC2 env.\n" \
          "./" + (os.path.basename(__file__)),"2 add ELB env.\n" \
          "./" + (os.path.basename(__file__)),"3 list operation."
    sys.exit()
elif sys.argv[1] == '1':
    print 'input 1 right，exec add EC2 environment.'
    ADD_ENV_OF_EC2()
elif sys.argv[1] == '2':
    print 'input 2 right，exec add ELB environment.'
    ADD_ENV_OF_ELB()
elif sys.argv[1] == '3':
    print 'input 3 right，usage list operation add environment.'
    list_op()
    sys.exit(0)
else:
    print "input wrong. please usage: \n" \
          "./" + (os.path.basename(__file__)),"1 add EC2 env.\n" \
          "./" + (os.path.basename(__file__)),"2 add ELB env.\n" \
          "./" + (os.path.basename(__file__)),"3 list operation."

