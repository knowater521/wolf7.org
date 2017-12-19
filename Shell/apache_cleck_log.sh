#!/bin/bash
# Deniss.wang
# Check 4xx and 5xx in logs
# Add your own filter url file list and Assign error url directory 
# Date: 2017-11-20
#
#log_file='/var/log/httpd/access_log'
#now_time=`date -d "2 minute ago" +%d/%b/%Y:%H:%M`
log_file='./access_log'
now_time='18/Dec/2017:09:41'
project='example'
email_add='deniss.wang@example.com'
statuscode_list=(404 401 403 400 500 501 503 504)
web_filter_list='robot.txt|favicon.ico|testproxy.php|device_description.xml'
directory_list=(agency advertiser manager)
# If 4xx/5xx and sendEmail  function
web_code_sendemail(){
    for code_list in ${statuscode_list[*]}
    do
        for dir_list in ${directory_list[*]}
        do
        statuscode=`tail -n 50 $log_file|grep -w $dir_list|grep -w $code_list|egrep -v $web_filter_list|awk 'END {print}'|awk '{print $10}'`
        status_time=`tail -n 50 $log_file|grep -w $dir_list|grep -w $code_list|egrep -v $web_filter_list|awk  'END {print}'|awk -F' ' '{print $5}'|awk -F'[' '{print $2}'|cut -c 1-17`
        detail=`tail -n 50 $log_file|grep -w $code_list|grep -w $dir_list|egrep -v $web_filter_list |awk 'NR==1 {print}'`
        check_dir_list=`tail -n 50 $log_file|grep -w $code_list|grep -w $dir_list|awk '{print $8}'|awk -F'/' '{print $2}'`
            if [[ $dir_list == $check_dir_list && $statuscode == $code_list &&  $status_time == $now_time ]];then
            # 打印code发送Email
                echo "Los Detail: $detail " #| mail -s "$code_list error of $project" $email_add
                #echo $statuscode=$code_list,$status_time=$now_time,$dir_list=$check_dir_list
            else
            #date -d "2 minute ago" +%d/%b/%Y:%H:%M >> /tmp/status_code.txt
                echo "no error in logs" > /dev/null 2>&1
            fi
        continue
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
