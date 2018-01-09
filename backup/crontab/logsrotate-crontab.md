# 1.airflowapp.log app部署日志
Step 1:
```
touch /etc/logrotate.d/airflowapp-log
```
Step 2:
```
vim /etc/logrotate.d/airflowapp-log 
 
/data/airflow/logs/airflowapp.log/
{
daily
dateext
copytruncate
nocompress
rotate 7 
}
``` 

Step 3:.add to system job  
``` 
crontab -e 
#选择/usr/bin/vim.basic
#change logfile at 0:00 Sunday 
SHELL=/bin/bash
00  0  *  *  6  logrotate -f /etc/logrotate.d/airflowapp-log  
```
Step 4:Testing   
使用命令crontab -u root -l 可以查看当前定时任务  
测试： 
`logrotate -f /etc/logrotate.d/airflowapp-log >/dev/null 2>&1`


# 2.webserver,scheduler日志
airflow-scheduler.err.log  
airflow-scheduler.out.log  
airflow-webserver.err.log  
airflow-webserver.out.log  

同1的处理方式
## 2.1 airflow-scheduler.err.log
 
Step 1:touch /etc/logrotate.d/airflow-scheduler-err-log 
```
Step 2:.vim /etc/logrotate.d/airflow-scheduler-err-log  
/data/airflow/logs/airflow-scheduler.err.log/
{
daily
dateext
copytruncate
nocompress
rotate 7 
}
```
## 2.2 airflow-scheduler.out.log
touch /etc/logrotate.d/airflow-scheduler-out-log   
```
vim /etc/logrotate.d/airflow-scheduler-out-log    
/data/airflow/logs/airflow-scheduler.out.log/
{
daily
dateext
copytruncate
nocompress
rotate 7 
}
```
## 2.3 airflow-webserver.err.log
touch /etc/logrotate.d/airflow-webserver-err-log
```
vim /etc/logrotate.d/airflow-webserver-err-log  
/data/airflow/logs/airflow-webserver.err.log/
{
daily
dateext
copytruncate
nocompress
rotate 7 
}
```
## 2.4 airflow-webserver.out.log
touch /etc/logrotate.d/airflow-webserver-out-log 
```
vim /etc/logrotate.d/airflow-webserver-out-log  
/data/airflow/logs/airflow-webserver.out.log/
{
daily
dateext
copytruncate
nocompress
rotate 7 
}
```

## 2.5 加入crontab
```
crontab -e 
#选择/usr/bin/vim.basic
#change logfile at 0:00 Sunday 
SHELL=/bin/bash
00  0  *  *  6  logrotate -f /etc/logrotate.d/airflow-applog   
00  0  *  *  6  logrotate -f /etc/logrotate.d/airflow-scheduler-err-log  
00  0  *  *  6  logrotate -f /etc/logrotate.d/airflow-scheduler-out-log  
00  0  *  *  6  logrotate -f /etc/logrotate.d/airflow-webserver-err-log  
00  0  *  *  6  logrotate -f /etc/logrotate.d/airflow-webserver-out-log  
```


Step 4:Testing
使用命令crontab -u root -l 可以查看当前定时任务
测试：
```
logrotate -f /etc/logrotate.d/airflow-scheduler-err-log  
logrotate -f /etc/logrotate.d/airflow-scheduler-out-log  
logrotate -f /etc/logrotate.d/airflow-webserver-err-log  
logrotate -f /etc/logrotate.d/airflow-webserver-out-log  
```


# 3.dags运行日志  /data/airflow/logs/dags      
auto-del-7-days-ago-log  

Step1:删除文件命令：
```
find 对应目录 -mtime +天数 -name "文件名" -exec rm -rf {} \; 
find /opt/soft/log/ -mtime +30 -name "*.log" -exec rm -rf {} \;
```
```
说明：
将/opt/soft/log/目录下所有30天前带".log"的文件删除。具体参数说明如下：  
find：linux的查找命令，用户查找指定条件的文件；  
/opt/soft/log/：想要进行清理的任意目录；  
-mtime：标准语句写法；  
+30：查找30天前的文件，这里用数字代表天数；
"*.log"：希望查找的数据类型，"*.jpg"表示查找扩展名为jpg的所有文件，"*"表示查找所有文件，这个可以灵活运用，举一反三；
-exec：固定写法；
rm -rf：强制删除文件，包括目录；
{} \; ：固定写法，一对大括号+空格+\+; 
```
```
find /data/airflow/logs/dags -name `date +%Y`*; 
find /data/airflow/logs/dags -mtime +7 -name `date +%Y`* -exec rm -rf {} \;
```
 
Step2.add to system job  
```
#crontab -e
#change logfile at 0:00 every Sunday 
SHELL=/bin/bash
00  0  *  *  6  find /data/airflow/logs/dags -mtime +7 -name `date +%Y`* -exec rm -rf {} \ 
``` 
 


# 4.scheduler运行日志  /data/airflow/logs/scheduler     
auto-del-7-days-ago-log
```
find /data/airflow/logs/scheduler/ -name *.log  
find /data/airflow/logs/scheduler/ -mtime +7 -name *.log -exec rm -rf {} \ 

crontab -e 
00  0  *  *  6  find /data/airflow/logs/scheduler/ -mtime +7 -name *.log -exec rm -rf {} \  
```




