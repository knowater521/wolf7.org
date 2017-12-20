#!/bin/bash
# Deniss.wang
# Check 4xx and 5xx in logs and send to Email
# Add own filter url file list and Assign error url directory 
# Date: 2017-11-20 00:30
#
log_file='/var/log/httpd/access_log'
now_time=`date -d "2 minute ago" +%d/%b/%Y:%H:%M`
#log_file='./access_log'
#now_time='19/Dec/2017:23:23'
project='example'
email_add='deniss.wang@example.com'
statuscode_list=(404 401 403 400 500 501 503 504)
web_filter_list='robot.txt|favicon.ico|testproxy.php|device_description.xml'
directory_list=(agency advertiser manager)
# If 4xx/5xx and sendEmail function
web_code_sendemail(){
    for code_list in ${statuscode_list[*]}
    do
        for dir_list in ${directory_list[*]}
        do
        statuscode=`tail -n 50 $log_file|grep -w $dir_list|grep -w $code_list|egrep -v $web_filter_list|awk 'END {print}'|awk '{print $10}'`
        status_time=`tail -n 50 $log_file|grep -w $dir_list|grep -w $code_list|egrep -v $web_filter_list|awk  'END {print}'|awk -F' ' '{print $5}'|awk -F'[' '{print $2}'|cut -c 1-17`
        detail=`tail -n 50 $log_file|grep -w $dir_list|grep -w $code_list| egrep -v $web_filter_list|awk 'END {print}'`
        check_dir_list=`tail -n 50 $log_file|grep -w $dir_list|grep -w $code_list|egrep -v $web_filter_list|awk 'END {print}'|awk '{print $8}' |awk -F'/' '{print $2}'`
            if [[ $dir_list == $check_dir_list && $statuscode == $code_list &&  $status_time == $now_time ]];then
            # print log detail send to Email
                echo "Logs Detail: $detail " | mail -s "$code_list error of $project" $email_add
            else
                echo "no error in logs" > /dev/null 2>&1
            fi
        done
    done
}
# check log directory exists and exec web_code_sendemail function
check_log(){
    if [[ -f $log_file ]];then
        web_code_sendemail
        exit 0
    else
        echo "logs file is not found."
        exit 1
    fi
}
# exec
check_log
