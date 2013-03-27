#! /usr/bin/env python
#####################################################
#  Zabbix rleated operations: login, check hosts,   #
#  update hosts, update applications                #
#####################################################

import zabbix_api
import socket
import os
import sys
import json
import socket
import logging
#import jmp_constants
from zabbix_api import ZabbixAPI, ZabbixAPIException

#####################################################
#  Function reads the jmp.properties file and       #
#  returns username,password, agent.conf path       #
# input:  path to jmp.properties file               #
# output:  list [username, password, path ]         #
#####################################################
def jmp_info(name):
        datafile = file(name)
        if not datafile:
            logging.error('jmp.properties file was not found')
        else:
            z_data = {}
            logging.info('jmp.properties file was found')
            for line in datafile:
                if "#" in line:
                    continue
                elif "jmpEnabled" in line:
                    line = line.strip('\n')
                    line = line.split("jmpEnabled=")
                    z_data['jmpEnabled'] = line[1]
                elif "username" in line:
                    line = line.strip('\n')
                    line = line.split("username=")
                    z_data['username'] = line[1]
                elif "password=" in line:
                    line = line.strip('\n')
                    line = line.split("password=")
                    z_data['password'] = line[1]
                elif "jsb_z_agent_conf" in line:
                    line = line.strip('\n')
                    line = line.split("jsb_z_agent_conf=")
                    z_data['jsb_z_agent_conf'] = line[1]
                elif "jta_z_agent_conf" in line:
                    line = line.strip('\n')
                    line = line.split("jta_z_agent_conf=")
                    z_data['jta_z_agent_conf'] = line[1]
                elif "jmp_template" in line:
                    line = line.strip('\n')
                    line = line.split("jmp_template=")
                    z_data['jmp_template'] = line[1]
                elif "jasper_home" in line:
                    line = line.strip('\n')
                    line = line.split("jasper_home=")
                    z_data['jasper_home'] = line[1]
                elif "jsb.jmxremote" in line:
                    line = line.strip('\n')
                    line = line.split("jsb.jmxremote=")
                    z_data['jsb.jmxremote'] = line[1]
                elif "jsbHostGroup" in line:
                    line = line.strip('\n')
                    line = line.split("jsbHostGroup=")
                    z_data['jsbHostGroup'] = line[1]
                elif "jtaHostGroup" in line:
                    line = line.strip('\n')
                    line = line.split("jtaHostGroup=")
                    z_data['jtaHostGroup'] = line[1]
                elif "jtaHostName" in line:
                    line = line.strip('\n')
                    line = line.split("jtaHostName=")
                    z_data['jtaHostName'] = line[1]
                elif "jsbHostName" in line:
                    line = line.strip('\n')
                    line = line.split("jsbHostName=")
                    z_data['jsbHostName'] = line[1]
        return z_data
#####################End#############################
#####################################################
#  Function reads the agentd.conf file and returns  #
#  Server, ServerActive, Hostname                   #
# input:  path to zabbix_agentd.conf file           #
# output:  list [Server, ServerActive, Hostname ]   #
#####################################################
def z_info(name):
        datafile = file(name)
        z_data = {}
        for line in datafile:
            if "#" in line:
                continue  
            elif "Server=" in line:
                line = line.strip('\n')
                line = line.split("Server=")
                z_data['Server'] = line[1]
            elif "ServerActive=" in line:
                line = line.strip('\n')
                line = line.split("ServerActive=")
                z_data['ServerActive'] = line[1]
            elif "Hostname=" in line:
                line = line.strip('\n')
                line = line.split("Hostname=")
                z_data['Hostname'] = line[1]
        return z_data
#####################End#############################
#####################################################
#  Function connects to Zabbix Server               #
# input:  void                                      #
# output:  Boolean                                  #
#####################################################
def z_logging():        
        status = None
        zabbix_info = {}
        zagent_info = {}
        zabbix_info = jmp_info('jmp.properties')
        #print zabbix_info
        logging.debug(zabbix_info)
        zagent_info = z_info(zabbix_info['jta_z_agent_conf'])
        #print zagent_info
        logging.debug(zagent_info)
        zabbix_server_username=zabbix_info['username']
        zabbix_server_password=zabbix_info['password']
        zabbix_server_url='http://'+ zagent_info['Server'] + '/zabbix'
        #print zabbix_server_url
        logging.debug(zabbix_server_url)
        z=zabbix_api.ZabbixAPI(server=zabbix_server_url)
        z.login(user=zabbix_server_username, password=zabbix_server_password)
        return z
#####################End#############################
#####################################################
#  Function Check for the JapserServer Hostgroup    #
# input:  Zabbix Handle                             #
# output:  True or false                            #
#####################################################
def z_checkHostgroup(zabbix_handler, hostGroupName):        
        hostgroups = zabbix_handler.hostgroup.get(
        {
        #'filter': { 'name': hostgroup}, 
        'output': 'extend'
        })
        logging.debug(hostgroups)
        for item in hostgroup:
                if hostGroupName:
                    logging.debug("JasperServers exist")
                    return True
                else:
                    logging.debug("JasperServer hostgroup not found, talk to your system Administrator")
                    return False
#####################End#############################
#####################################################
#  Function Check for JTA JMX Template templateid   #
# input:  Zabbix Handle , Template name             #
# output:  TemplateID if template exist             #
#####################################################
def get_jta_templateid(zabbix_handler, template_name):
        jta_template = zabbix_handler.template.get(
            {
            'filter': { 'name': template_name}, 
            'output': 'extend'
            })
        logging.info("JTA Template id is for"+ template_name)
        logging.info(jta_template[0]['templateid'])
        return jta_template[0]['templateid']
#####################End#############################
#####################################################
#  Function Check for zabbix \   version            #
# input:  Zabbix Handle , Template name             #
# output:  Zabbix verison                           #
#####################################################
def get_zabbix_api_version(zabbix_handler):
            print zabbix_handler.api_version()
            logging.debug(zabbix_handler.api_version())
#####################End#############################

#####################################################
#  Function Check for JasperServer group            #
# input:  Zabbix Handle , HostGroupName             #
# output:  GroupID                                  #
#####################################################
#Check for HostGroup JasperServer or what ever the name is for JTA hosts
def get_jasper_groupid(zabbix_handler,groupName):
        hostgroups = zabbix_handler.hostgroup.get(
            {
            'output': 'extend'
            })
        logging.debug(hostgroups)
        for item in hostgroups:
            logging.debug(item['name'])
            if item['name'] == "JasperServers":
                logging.debug(item['groupid'])
                logging.debug('group found')
                return item['groupid']
            else:
                continue    
        print "Can't find JasperServers Group"
        logging.error('Cannot find JasperServers Group please check your Zabbix installation')
        return 0
#####################End#############################
#####################################################
#  Function get the hosts list for jTA's group      #
# input:  Zabbix Handle , HostGroupName             #
# output:  GroupID                                  #
##################################################### 
def get_jasperhosts(zabbix_handler,hostsgroupID):
        jta_apps_hosts = []
        hosts = zabbix_handler.host.get(
            {
            'filter': { 'groupid': hostsgroupID}, 
            'output': 'extend'
            })
        for item in hosts:
            if "jta" in item['host']:
                jta_apps_hosts.append(item['host'].strip('\n'))
        jta_apps_hosts = [s.encode('utf-8') for s in jta_apps_hosts]
        logging.debug('JTA_APPS_HOST')
        logging.debug(jta_apps_hosts)
        return jta_apps_hosts
#####################End#############################
#####################################################
#  Function retrive the host interface info for JTA #
# input:  Zabbix Handle , HostGroupName             #
# output:  Interface object                         #
##################################################### 
def get_hostinterface(zabbix_handler,hostsgroupID):
        hosts = zabbix_handler.host.get(
            {
            'filter': { 'groupid': hostsgroupID}, 
            'output': 'extend'
            })
        for item in hosts:
            if "jta" in item['host']:
                interface = zabbix_handler.hostinterface.get(
                {
                'filter': { 'hostid': item['hostid']}, 
                'output': 'extend'
                })
        logging.debug('INTERFACE for host')
        logging.debug(interface)
        return interface
#####################End#############################
#####################################################
#  Function retrive the host interface info for     #
#  any host                                         #
# input:  Zabbix Handle , HostID                    #
# output:  interface object                         #
##################################################### 
def get_interface(zabbix_handler,hostID):
        interface = zabbix_handler.hostinterface.get(
                {
                'filter': { 'hostid': hostID}, 
                'output': 'extend'
                })
        logging.debug('INTERFACE for host(s)')
        logging.debug(interface)
        return interface
#####################End#############################
#####################################################
#  Function retrive the Application ID for JTA-Logs #
#  any host                                         #
# input:  Zabbix Handle , HostID                    #
# output:  interface object                         #
##################################################### 
def get_jta_log_applicationID(zabbix_handler,HostID):
        applicationID = zabbix_handler.application.get(
        {
        'hostids':HostID,
        'filter': { 'name': 'JTA-Logs'}, 
        'output': 'extend'
        })
        logging.debug("Application id ")
        logging.debug(applicationID)
        logging.debug(applicationID[0]['applicationid'])
        return applicationID[0]['applicationid']
#####################End#############################
#####################################################
#  Function retrive the Application ID for JTA-Logs #
#  any host                                         #
# input:  Zabbix Handle , HostID                    #
# output:  interface object                         #
##################################################### 
def get_jta_application_list(zabbix_handler,HostID,keyword):
        jta_application_list=[]
        applications = zabbix_handler.application.get(
        {
        'hostids':HostID,
        'output': 'extend'
        })
        for item in applications:
             if keyword in item['name']:
                jta_application_list.append(item['name'].strip('\n'))
        jta_application_list = [s.encode('utf-8') for s in jta_application_list]
        logging.debug("JTA application List for JTA-Logs")
        logging.debug(jta_application_list)
        return jta_application_list
#####################End#############################
#####################################################
#  Function retrive the Application ID for          #
#  jasper.jta.management                            #
# input:  Zabbix Handle , HostID                    #
# output:  interface object                         #
##################################################### 
def get_jta_management_applicationID(zabbix_handler,HostID):
        applicationID = zabbix_handler.application.get(
        {
        'hostids':HostID,
        'filter': { 'name': 'jasper.jta.management'},
        'output': 'extend'
        })
        logging.debug("Application id for jta.management ")
        logging.debug(applicationID)
        logging.debug(applicationID[0]['applicationid'])
        return applicationID[0]['applicationid']
#####################################################
#  Function to add items for the JTA application #
# input:  Zabbix Handle , HostGroupName             #
# output:  Interface object                         #
##################################################### 
def add_jta_jmx_items(zabbix_handler,jmx_item,jmx_interface, jmx_applicationID, jasper_hostID): 
            #####################################################
            #Create items for the JTA-JMX - JTA-JEC Connector Status
            #####################################################
            logging.debug("Jasper_HostID ")
            logging.debug(jasper_hostID)
            item_name = "JTA-JEC Connector Status"
            key_value = 'jmx["Mule.' + jmx_item + ':type=Connector,name=\\"JEC.1\\"",Started]'
            logging.debug("keyvalue ")
            logging.debug(key_value)
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'3',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            
            logging.debug(" Jasper_itemID JTA-JEC Connector Status")
            logging.debug(jasper_itemID)
            
            #####################################################
            #Create items for the JTA-JMX - JTA AsyncEventsReceived
            #####################################################
            item_name = "JTA AsyncEventsReceived"
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",AsyncEventsReceived]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA AsyncEventsReceived")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA AverageProcessingTime
            #####################################################
            item_name = "JTA AverageProcessingTime"
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",AverageProcessingTime]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA AverageProcessingTime")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA ExecutionErrors
            #####################################################
            item_name = "JTA ExecutionErrors"
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",ExecutionErrors]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
               'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA ExecutionErrors")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA FatalErrors
            #####################################################
            item_name = "JTA FatalErrors"
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",FatalErrors]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA FatalErrors")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA Free Memory
            #####################################################
            item_name = "JTA Free Memory"
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,FreeMemory]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'units':'M Bytes',
                'formula':'0.000001',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA Free Memory")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA Host IP
            #####################################################
            item_name = "JTA Host IP"
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,HostIp]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'4',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA Host IP")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX JTA InstanceId
            #####################################################
            item_name = "JTA InstanceId"
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,InstanceId]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'4',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA-JEC Connector Status")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX JTA JdkVersion
            #####################################################
            item_name = "JTA JdkVersion"
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,JdkVersion]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'4',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA JdkVersion")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX JTA Max Memory
            #####################################################
            item_name = "JTA Max Memory"
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,MaxMemory]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'units':'M Bytes',
                'formula':'0.000001',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA Max Memory")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA MaxProcessingTime
            #####################################################
            item_name = "JTA MaxProcessingTime"
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",MaxProcessingTime]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'units':'Micro Second per event',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA MaxProcessingTime")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX JTA MinProcessingTime
            #####################################################
            item_name = "JTA MinProcessingTime"
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",MinProcessingTime]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA MinProcessingTime")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA SyncEventsReceived
            #####################################################
            item_name = "JTA SyncEventsReceived"
            key_value = 'jmx["Mule.' + jmx_item + ':type=Application,name=\\"application totals\\"",SyncEventsReceived]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'formula':'1',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA SyncEventsReceived")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA TotalEventsReceived
            #####################################################
            item_name = "JTA TotalEventsReceived"
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",TotalEventsReceived]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA TotalEventsReceived")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA Total Memory
            #####################################################
            item_name = "JTA Total Memory"
            key_value = 'jmx[Mule.' + jmx_item + ':name=MuleContext,TotalMemory]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'data_type':'0',
                'formula':'0.000001',
                'units':'M Bytes',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA Total Memory")
            logging.debug(jasper_itemID)
            #####################################################
            #Create items for the JTA-JMX - JTA TotalProcessingTime
            #####################################################
            item_name = "JTA TotalProcessingTime"
            key_value = 'jmx["Mule.' + jmx_item + ':type=org.mule.Statistics,Application=application totals",TotalProcessingTime]'
            jasper_itemID = zabbix_handler.item.create({
                'name':item_name,
                'type':'16',
                'key_':key_value,
                'delay':'15',
                'history':'90',
                'trends':'365',
                'value_type':'3',
                'units':'sec',
                'formula':'0.000001',
                'data_type':'0',
                'authtype':'0',
                'username':'{$JMX_USERNAME}',
                'password': '{$JMX_PASSWORD}',
                'status':'0',
                'interfaceid': jmx_interface,
                'applications': [jmx_applicationID],
                'hostid': jasper_hostID
                })
            logging.debug(" Jasper_itemID JTA TotalProcessingTime")
            logging.debug(jasper_itemID)
            
            return True
#####################End#############################





