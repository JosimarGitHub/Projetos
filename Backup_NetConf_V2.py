#!/usr/bin/env python

# import the ncclient library and xml libraries 
from ncclient import manager
import xml.dom.minidom
import os
import getpass
from bs4 import BeautifulSoup
from datetime import datetime

now = datetime.now()

dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
#print("date and time =", dt_string)

#Informações para Acesso via Netconf
hosts = open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/IOS_LAB/BOOT_CAMP_NETCONF_2.txt','r')
USER = input("Enter your telnet username: ")
PASS = getpass.getpass()


for HOST in hosts:
    HOST = HOST.replace('\n','')
    # Establish connection to the device
    netconf_connection = manager.connect(host=HOST, 
                    port=830, 
                    username=USER,
                    password=PASS, 
                    hostkey_verify=False,
                    look_for_keys=False,
                    allow_agent=False
                        )
    
     # XML filter para pegar hostname 
    hostname_filter =   """
                        <filter>
                            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                                <hostname></hostname>
                            </native>
                        </filter>
                        """
    
    # Use the <get-config> NETCONF Operation to retrieve full configuration
    result = netconf_connection.get_config('running',hostname_filter)
    data_aux = xml.dom.minidom.parseString(result.xml).toprettyxml()

    with open('data_aux.xml', 'w') as f:
        f.write(data_aux)
        f.close()

    data = open('data_aux.xml')
    Bs_data = BeautifulSoup(data, "xml")
    b_hostname = Bs_data.find_all('hostname')
    hostname = str(b_hostname)
    hostname = hostname.replace("[","")
    hostname = hostname.replace("<","")
    hostname = hostname.replace("hostname","")
    hostname = hostname.replace(">","")
    hostname = hostname.replace("/]","")

    #apagando arquivo auxiliar
    os.remove('data_aux.xml')

    # Use the <get-config> NETCONF Operation to retrieve full configuration
    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backup_NETCONF/'+hostname+'_'+dt_string+'.xml' ,'w') as f:
        config = netconf_connection.get_config("running")
        config_xml = xml.dom.minidom.parseString(config.xml).toprettyxml()
        f.write(config_xml)
        f.close()

    netconf_connection.close_session()