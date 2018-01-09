#! /bin/bash 
rm -r /data  
mkdir -p /data/airflow/logs/
touch /data/airflow/logs/airflowapp.log
mkdir -p /data/airflow/dags/
cp /root/airflow/dags/*  /data/airflow/dags/

#grant access to ftp user
chmod  777  /data/airflow/dags/
chmod  777  /data/airflow/logs/

echo `date '+%Y-%m-%d %H:%M:%S'`,000 - initdatapath.sh - INFO - Action is init data path.******************************************************************************************************** \(L7\)>>/data/airflow/logs/airflowapp.log
 

 
