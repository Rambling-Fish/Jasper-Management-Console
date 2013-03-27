#! /usr/bin/env python
#####################################################
#  Test script for detecting JSB and add Zabbix     #
#  Host, Log items, screens                         #
#####################################################
import logging
import zabbix_api
import socket
import os
import sys
import json
import socket
from zabbix_api import ZabbixAPI, ZabbixAPIException
import jmp_zabbix
import jta_checker

#####################################################
#Set the log level and log file name
#####################################################
a = logging.basicConfig(format='%(asctime)s %(message)s',filename='auto_discoverlog.log',level=logging.ERROR)
logging.getLogger(__name__)
logging.debug('Auto-discovery started running')

#####################################################
#  Log onto Zabbix                                  #
#####################################################
zabbix_info = jmp_zabbix.jmp_info('jmp.properties')
logging.debug("##########Zabbix_info#########")
logging.debug(zabbix_info)
logging.debug(zabbix_info['jtaHostName'])
try:
    z = jmp_zabbix.z_logging()
except Exception as e:
    logging.error(logging.ERROR, "No connection to Zabbix. Error: "+str(e))
    sys.exit(-1)

hostgroup='JasperServers'
jasper_groupid = jmp_zabbix.get_jasper_groupid(z,hostgroup)
jta_list_hosts = jmp_zabbix.get_jasperhosts(z,jasper_groupid)

logging.debug('###################HostList########################')    
logging.debug(jta_list_hosts)   

deployed_jta_list = jta_checker.get_apps_diff()
logging.debug('###################deployed_apps########################')
logging.debug(deployed_jta_list['deployed_apps'])

#####################################################
# Get the list of JTA applications under           #
# JTA server host == JTA-jasperServer-a             #
#####################################################
host_jta_server = z.host.get(
        {
        'filter': { 'host': zabbix_info['jtaHostName']}, 
        'output': 'extend'
        })
jta_server_hostID=host_jta_server[0]['hostid']
host_interface = jmp_zabbix.get_interface(z,jta_server_hostID)
log_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
logging.debug("list of interfaces \n")
logging.debug(log_interfaceID)
#####################################################
#  Check for the JTA's and add the missing ones     #
#####################################################
deployed_jta_application_list = jmp_zabbix.get_jta_application_list(z,jta_server_hostID,"jta")
logging.debug(deployed_jta_application_list)
if not deployed_jta_list['deployed_apps']:
    logging.debug("list empty noting to update")
else: 
    #start adding JTA hosts
    for item in deployed_jta_list['deployed_apps']:
        if item in deployed_jta_application_list:
            logging.debug('Item (%s) is already added',item)
            continue 
        else:
            #####################################################
            # Add items and the screens to display
            # get host id
            #####################################################
            information = jmp_zabbix.z_info(zabbix_info['jta_z_agent_conf'])
            logging.debug("##############Information####################")
            logging.debug(information)
            #####################################################
            # Add log item for the JTA-Log application
            #####################################################
            jta_log_applicationID = jmp_zabbix.get_jta_log_applicationID(z,jta_server_hostID)
            logging.debug("######LOG-applicationID##############")
            logging.debug(jta_log_applicationID)
                    
            #####################################################
            #Get interface ID
            #####################################################
            jta_interfaceID = jmp_zabbix.get_interface(z,jta_server_hostID)
            logging.debug("######Interface ID##############")
            logging.debug(jta_interfaceID)
            logging.debug(jta_interfaceID[0]['interfaceid'])
            #####################################################
            #Add log item to JTA_log applicaiotn in jasperServer-a
            #####################################################
            item_log_name = item + "-log"
            key_value = "log[{$JTA_SVR_PATH}/logs/" + item + ".log]"
            logging.debug("######Key value##############")
            logging.debug(key_value)
            try:
                jasper_itemID = z.item.create({
                    'name':item_log_name,
                    'key_':key_value,
                    'type':'7',
                    'interfaceid':jta_interfaceID[0]['interfaceid'],
                    'applications':[jta_log_applicationID],
                    'hostid':jta_server_hostID,
                    'value_type':'2',
                    'delay':'10'
                    })
            except Exception as e:
                logging.debug(logging.ERROR, "Zabbix. Log Item: "+str(e))
                    
            #####################################################
            #Add management item to JTA_management applicaiotn in jasperServer-a
            #####################################################
            jta_management_applicationID = jmp_zabbix.get_jta_management_applicationID(z,jta_server_hostID)
            logging.debug("###### MANAGEMENT-applicationID ##############")
            logging.debug(jta_management_applicationID)

            item_mgt_name = item + " - Status"
            key_value = "jasper.management[jtastatus," + item + "]"
            logging.debug("######Key value##############")
            logging.debug(key_value)
            try:
                jasper_itemID = z.item.create({
                    'name':item_mgt_name,
                    'key_':key_value,
                    'type':'7',
                    'interfaceid':jta_interfaceID[0]['interfaceid'],
                    'applications':[jta_management_applicationID],
                    'hostid':jta_server_hostID,
                    'value_type':'3',
                    'delay':'10',
                    'valuemapid':'12'
                    })
            except Exception as e:
                logging.debug(logging.ERROR, "Zabbix. Management Item: "+str(e))
                    
            #####################################################
            # Add new application to JTA-jasperServer-a host
            #####################################################
            jta_jmx_application_name = item+"-JMX"
            try:
                new_jta_application = z.application.create({
                    'name':jta_jmx_application_name,
                    'hostid':jta_server_hostID
                    })
                logging.debug("###### NEW application id##############")
                logging.debug(new_jta_application)

                new_jta_application['applicationids'] = [s.encode('utf-8') for s in new_jta_application['applicationids']]
                new_jta_applicationID = new_jta_application['applicationids'][0]
                logging.debug(new_jta_applicationID)
                logging.debug(jta_interfaceID[1]['interfaceid'])
                jta_jmx_interfaceID = jta_interfaceID[1]['interfaceid']
                jmp_zabbix.add_jta_jmx_items(z,item,jta_jmx_interfaceID,new_jta_applicationID,jta_server_hostID)
            except Exception as e:
                logging.debug(logging.ERROR, "Zabbix. JMX Item: "+str(e))
