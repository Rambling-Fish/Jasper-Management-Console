Zabbix start|stop scripts
===================================================================
The content of this folder complements zabbix installation with startup
Scripts to start|stop the following:

1. Zabbix server 
2. JTA Zabbix agent
3. JSB Zabbix agent  
4. Zabbix java-gateway 

Sample of the instructions are taken from this post on Zabbix forums:
http://www.zabbix.com/forum/showthread.php?p=123241

Scripts Location:

* etc/init.d

Copy the corresponding script into /etc/init.d/

After copying the script files into /etc/init.d/ execute the following: 
#sudo chmod 755 /etc/init.d/<<script_file_name>>

For starting Zabbix when the machine boots execute the following command: 
#sudo update-rc.d <<script_file_name>> defaults

Ref: http://www.zabbix.com/wiki/howto/ins.../ubuntuinstall
