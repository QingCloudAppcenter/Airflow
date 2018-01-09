 
在Linux中ftp服务器的全名叫 vsftpd，我们需要利用相关命令来开启安装ftp服务器，然后再在vsftpd.conf中进行相关配置，
下面我来介绍在Ubuntu中vsftpd安装与配置增加用户的方法。
1、apt-get update


2、首先用命令检查是否安装了vsftpd 
vsftpd -version
如果未安装用一下命令安装 
sudo apt-get install vsftpd
安装完成后，再次输入vsftpd -version命令查看是否安装成功

3、新建一个文件夹用于FTP的工作目录 ,对于airflow来说，是指/data/airflow/目录
 
4、新建FTP用户并设置密码以及工作目录 
dags为你为该ftp创建的用户名  
sudo useradd -d /data/airflow/ -s /bin/bash dags

为新建的用户设置密码  
passwd dags
password是dags.2018!
【注释：用cat etc/passwd可以查看当前系统用户】 


5、修改vsftpd配置文件 
vim /etc/vsftpd.conf 
设置属性值 
anonymous_enable=NO #禁止匿名访问 
local_enable=YES 
write_enable =YES 
保存返回 

pam_service_name=ftp 

如果登录ftp总是出现密码错误，可以将/etc/vsftpd.conf配置文件的pam_service_name=vsftpd改为pam_service_name=ftp，即可解决。

6、启动vsftpd服务
 service vsftpd start
 service vsftpd restart
 
7、在资源管理器，或者浏览器中ftp服务器 
输入账号，密码登录即可 
 

***********************************************************************************************************************
 

安装ftp客户端
apt-get update
apt-get install ftp

ftp客户端命令使用
0、修改密码 -- not work
quote site pswd dags.2018! dags.2018@

1、登录ftp server
---testing
ftp 192.168.100.14
dags/dags.2018!
ls
exit

2.wget
wget ftp://192.168.100.14//data/airflow/dags/hello_world.py --ftp-user=dags --ftp-password=dags.2018!
wget ftp://192.168.100.14//data/airflow/logs/airflowapp.log --ftp-user=dags --ftp-password=dags.2018!

3.删除文件
ftp 192.168.100.14
ls
cd logs 
delete airflowapp.log
mdelete a*

4.上传文件
ftp> !      -- 退出当前的窗口，返回Linux 终端，当我们退出终端的时候，又会返回到FTP上。

ls  -- 显示当前目录下的文件
cd dags
touch testdag
exit  -- 退出终端，返回FTP命令行

ftp> lcd
Local directory now /root
ftp> put testdag tesetdag
mput *

 
5. 下载文件
同样也有2个命令： get 和 mget。 Mget 用户批量下载。
                   格式：get [remote-file] [local-file]
                              mget [remote-files]
                  同样，mget 是将文件下载到本地的当前目录下。
                  
6.断开FTP 连接
Bye命令或者quit命令：中断与服务器的连接。
ftp> bye 
 





