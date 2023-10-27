#Bibliotecas importadas
import telnetlib

#Informações para Acesso via Telnet
with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/IOS_LAB/Switchs_Bootcamp.txt','r') as arquivo:
    hosts = arquivo.readlines()
    arquivo.close()

nLinhas1 = len(hosts)-1
linhaAtual = 0
ultimaLInha = 0

while ultimaLInha != nLinhas1:

    lido = False

    while lido == False :

        for i in range(ultimaLInha,nLinhas1):

            if hosts[i].startswith("Host"):
                hosts[i] = hosts[i].replace("Host","")
                hosts[i] = hosts[i].replace("=","")
                hosts[i] = hosts[i].replace("\n","")
                hosts[i] = hosts[i].lstrip()
                HOST = hosts[i]

            if hosts[i].startswith("user"):
                hosts[i] = hosts[i].replace("user","")
                hosts[i] = hosts[i].replace("=","")
                hosts[i] = hosts[i].replace("\n","")
                hosts[i] = hosts[i].lstrip()
                user = hosts[i]

            if hosts[i].startswith("password"):
                hosts[i] = hosts[i].replace("password","")
                hosts[i] = hosts[i].replace("=","")
                hosts[i] = hosts[i].replace("\n","")
                hosts[i] = hosts[i].lstrip()
                password = hosts[i]
                ultimaLInha = i+1
                lido = True
                break
            linhaAtual = linhaAtual+1

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Username: ")

    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    
    print("Configurando host "+HOST+"\n")

    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Scripts/VLAN_Config','r') as arquivo:
        script_str = arquivo.readlines()
        arquivo.close()

    nLinhas_2 = len(script_str)
    linhaAtual_2 = 0
    ltimaLInha_2= 0

    tn.write(b"configure terminal\n")

    for i in range (60,121):
        for y in range (nLinhas_2):
            j = str(i)
            script_bytes = script_str[y] % j
            tn.write(bytes(script_bytes,encoding='utf-8'))
        tn.write(b"exit\n")

    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Scripts/interface_Config','r') as arquivo:
        script_str = arquivo.readlines()
        arquivo.close()
    
    nLinhas_2 = len(script_str)
    linhaAtual_2 = 0
    ltimaLInha_2= 0

    for y in range (nLinhas_2):
        tn.write(bytes(script_str[y],encoding='utf-8')) 
    
    tn.write(b"end\n")

    saida = tn.read_until(b"end")

    print("Host "+HOST+" configurado\n")

    tn.close