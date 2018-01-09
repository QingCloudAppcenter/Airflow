#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import subprocess
import sys  

def exec_cmd(cmd):
    """
    :param cmd: the command you want to call
    :return: ret_code, output
    """
    try:
        ret = subprocess.check_output(cmd, shell=True)
        return 0, ret
    except subprocess.CalledProcessError as e:
        return e.returncode, e.output 

def help():
    print 'Guide: ./airflowapp.py [init,start,restart,stop,monitor]'

class AirflowError(Exception):
    pass

class AirflowCluster:   
    LOGS_PATH = "/data/airflow/logs/"
    DAGS_PATH = "/data/airflow/dags/" 
    LOGGER_LEVEL = logging.DEBUG
    #LOGGER_LEVEL = logging.INFO
    EXPEVN_CMD = "export PATH=${PATH}:/usr/local/bin/:/bin;"
    
    INITDB_CMD = EXPEVN_CMD+"airflow initdb" 
    RESETDB_CMD = EXPEVN_CMD+"echo y|airflow resetdb" 
    INIT_USER_CMD = EXPEVN_CMD+"python /root/airflow/airflowscripts/adduser.py"
    
    START_CMD_SUOERVISORD = EXPEVN_CMD+"supervisord -c /etc/supervisord.conf "
    
    START_CMD_WEBSERVER = EXPEVN_CMD+"supervisorctl start airflow-webserver"
    STOP_CMD_WEBSERVER = EXPEVN_CMD+"supervisorctl stop airflow-webserver"
    RESTART_CMD_WEBSERVER = EXPEVN_CMD+"supervisorctl restart airflow-webserver"
    
    START_CMD_SCHEDULER = EXPEVN_CMD+"supervisorctl start airflow-scheduler"
    STOP_CMD_SCHEDULER = EXPEVN_CMD+"supervisorctl stop airflow-scheduler"
    RESTART_CMD_SCHEDULER = EXPEVN_CMD+"supervisorctl restart airflow-scheduler"
    
    CHECK_CMD_WEBSERVER = EXPEVN_CMD+"supervisorctl status airflow-webserver|grep RUNNING"
    CHECK_CMD_SCHEDULER = EXPEVN_CMD+"supervisorctl status airflow-scheduler|grep RUNNING"
    
    def __init__(self):  
        self.logger = self.init_logger()
  
    
    def init_logger(self):
        # 创建一个handler,用于写入日志文件 
        fh = logging.FileHandler(self.LOGS_PATH+"airflowapp.log")   
        # 再创建一个handler,用于输出到控制台 
        ch = logging.StreamHandler() 
        ch.setLevel(logging.DEBUG)  
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s  (L%(lineno)d) ')    
        fh.setFormatter(formatter) 
        ch.setFormatter(formatter) 
        
        logger = logging.getLogger('airflow') 
        logger.addHandler(fh) 
        logger.addHandler(ch) 
        logger.setLevel(self.LOGGER_LEVEL)
        return logger 
    
    def exec_cmd(self, cmd):
        ret = exec_cmd(cmd)
        self.logger.info('exec cmd: [%s], got ret: [%s]', cmd, ret)
        return ret
    
    def init(self):    
        self.resetdb()
        self.initdb()
        self.init_user() 
    
    def resetdb(self):   
        cmd = self.RESETDB_CMD
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow resetdb.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('airflow resetdb failed: [%s]' % ( output))
        
    def initdb(self):   
        cmd = self.INITDB_CMD
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow initdb.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('airflow initdb failed: [%s]' % ( output))
        
    def init_user(self):   
        cmd = self.INIT_USER_CMD
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow app init webserver user.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('airflow init user failed: [%s]' % ( output))  
    
    def start(self):
        self.start_supervisord() 
        
    def start_webserver(self): 
        cmd = self.START_CMD_WEBSERVER
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow app start webserver service.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('start airflow webserver failed: [%s]' % ( output))    
        
    def start_scheduler(self): 
        cmd = self.START_CMD_SCHEDULER
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow app start scheduler service.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('start airflow scheduler failed: [%s]' % ( output)) 
          
    def start_supervisord(self): 
        cmd = self.START_CMD_SUOERVISORD
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow app start supervisord service.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('start airflow supervisord failed: [%s]' % ( output))
        
    def restart(self):
        self.restart_webserver() 
        self.restart_scheduler()
        
    def restart_webserver(self): 
        cmd = self.RESTART_CMD_WEBSERVER
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow app restart webserver service.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('restart airflow webserver failed: [%s]' % ( output))    
        
    def restart_scheduler(self): 
        cmd = self.RESTART_CMD_SCHEDULER
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow app restart scheduler service.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('restart airflow scheduler failed: [%s]' % ( output)) 
        
    def stop(self):
        self.stop_webserver()
        self.stop_scheduler()
    
    def stop_webserver(self): 
        cmd = self.STOP_CMD_WEBSERVER
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow app stop webserver service.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('stop airflow webserver failed: [%s]' % ( output)) 
        
    def stop_scheduler(self): 
        cmd = self.STOP_CMD_SCHEDULER
        ret_code, output = self.exec_cmd(cmd)
        self.logger.info("-----Info：airflow app stop scheduler service.")
        if ret_code != 0 and ret_code != 48:
            raise AirflowError('stop airflow scheduler failed: [%s]' % ( output))   
    
    
    def healthcheck(self):  
        if not self.__check_process_alive("airflow-webserver"):
            self.logger.warn("====Warning：airflow webserver service process is down.")
            return False

        if not self.__check_process_alive("airflow-scheduler"):
            self.logger.warn("====Warning：airflow scheduler service process is down.")
            return False  
        
        return True
    
    def __check_process_alive(self, proc_name): 
        if proc_name == "airflow-webserver": 
            cmd = self.CHECK_CMD_WEBSERVER 
            
        if proc_name == "airflow-scheduler": 
            cmd = self.CHECK_CMD_SCHEDULER 
        ret_code, output = self.exec_cmd(cmd) 
         
        if ret_code == 0 and output != "":
            return True

        return False
    
    def initairflow(self):    
        self.resetdb() 
        self.init_user()
    
    def action(self):
        if not self.__check_process_alive("airflow-webserver"):
            self.start_webserver()

        if not self.__check_process_alive("airflow-scheduler"):
            self.start_scheduler()
       
def main():  
    airflowCluster = AirflowCluster() 
    cmd = sys.argv[1]   
    airflowCluster.logger.info("Action is "+cmd+".********************************************************************************************************") 
   
    if cmd == "init": 
        return airflowCluster.init() 
    elif cmd == "start": 
        return airflowCluster.start()
    elif cmd == "restart": 
        return airflowCluster.restart()
    elif cmd == "initairflow": 
        return airflowCluster.initairflow()
    elif cmd == "stop": 
        return airflowCluster.stop()
    elif cmd == "check":  
        if airflowCluster.healthcheck():
            sys.exit(0)
        else:
            sys.exit(1)
    elif cmd == "action": 
        return airflowCluster.action()
    else:
        return help() 
    
   
if __name__ == "__main__":
    main()
   
   
   
      
 