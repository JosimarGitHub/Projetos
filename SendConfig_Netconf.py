from ncclient import manager
import xml.dom.minidom
import os
from bs4 import BeautifulSoup

#Informações para Acesso via Netconf
with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/IOS_LAB/BOOT_CAMP_NETCONF.txt','r') as arquivo:

    hosts = arquivo.readlines()
    arquivo.close()

nLinhas1 = len(hosts)-1
linhaAtual = 0
ultimaLInha = 0

while ultimaLInha != nLinhas1:

    lido = False

    while lido == False :

        for i in range(ultimaLInha,nLinhas1):

            if hosts[i].startswith("HOST"):
                hosts[i] = hosts[i].replace("HOST","")
                hosts[i] = hosts[i].replace("=","")
                hosts[i] = hosts[i].replace("\n","")
                hosts[i] = hosts[i].lstrip()
                HOST = hosts[i]

            if hosts[i].startswith("PORT"):
                hosts[i] = hosts[i].replace("PORT","")
                hosts[i] = hosts[i].replace("=","")
                hosts[i] = hosts[i].replace("\n","")
                hosts[i] = hosts[i].lstrip()
                PORT = hosts[i]

            if hosts[i].startswith("USER"):
                hosts[i] = hosts[i].replace("USER","")
                hosts[i] = hosts[i].replace("=","")
                hosts[i] = hosts[i].replace("\n","")
                hosts[i] = hosts[i].lstrip()
                USER = hosts[i]
                
            if hosts[i].startswith("PASS"):
                hosts[i] = hosts[i].replace("PASS","")
                hosts[i] = hosts[i].replace("=","")
                hosts[i] = hosts[i].replace("\n","")
                hosts[i] = hosts[i].lstrip()
                PASS = hosts[i]
                ultimaLInha = i+1
                lido = True
                break
            linhaAtual = linhaAtual+1

    # Establish connection to the device
    netconf_connection = manager.connect(host=HOST, 
                        port=PORT, 
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

    with open('data_aux.xml', 'r') as f:
        data = f.read()
        Bs_data = BeautifulSoup(data, "xml")
        b_hostname = Bs_data.find_all('hostname')
        hostname = str(b_hostname)
        hostname = hostname.replace("[","")
        hostname = hostname.replace("<","")
        hostname = hostname.replace("hostname","")
        hostname = hostname.replace(">","")
        hostname = hostname.replace("/]","")
        #hostname = hostname.lstrip
        f.close()

     #apagando arquivo auxiliar
    os.remove('data_aux.xml')

    print("Configurando host "+hostname +"\n")

    standard_config = open("/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Config_NETCONF/Config_Int_Interface.xml")

    # Read in the standard config, and push to "running"
    push = netconf_connection.edit_config(standard_config.read(), target="running")

    # Print out the XML Data to the screen 
    print(xml.dom.minidom.parseString(push.xml).toprettyxml())

    print("\nHost "+hostname +" configurado\n")

    netconf_connection.close_session()