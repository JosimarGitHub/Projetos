#Bibliotecas importadas
import telnetlib
import os
import getpass
from datetime import datetime

#DATA e Hora para Criação do Arquivo
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")



#Informações para Acesso via Telnet
hosts = open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/IOS_LAB/Hosts_Bootcamp_2.txt','r')
user = input("Enter your telnet username: ")
password = getpass.getpass()

for HOST in hosts :

    HOST = HOST.replace('\n','')

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    #Pegando Nome do Host para gerar arquivo de config
    with open('nome.txt','w') as aux:
        tn.write(b"sh run | s hostname\n")
        nomeArquivoAux1 = (tn.read_until(b"aaaa",10).decode('ascii'))
        aux.write(nomeArquivoAux1)
        aux.close()
    with open('nome.txt','r') as aux:
        nomeArquivoAux2 = aux.readlines()
        nomeArquivo=nomeArquivoAux2[2].replace("hostname","")
        nomeArquivo=nomeArquivo.replace('\n','')
        nomeArquivo=nomeArquivo.lstrip()
        aux.close

    #apagando arquivo de nome
    os.remove("nome.txt")

    #Comando para obter Running-config
    tn.write(b"show Run\n")    
    
    dt = datetime.now()
    dt_backup = dt.strftime("%d/%m/%Y %H:%M:%S")
    print("FAZENDO BACKUP HOST "+nomeArquivo+" as "+dt_backup)
    #Gerando Arquivo de Backup
    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'_'+dt_string+'.txt', 'w+') as arquivo:
        arquivo.close()

    condicao = False
    fimArquivo = 0

    #Salvando Running config em arquivo txt
    while condicao == False :

        with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'_'+dt_string+'.txt', 'a') as arquivo:
        
            saida = (tn.read_until(b" --More-- ",10).decode('ascii'))
            arquivo.write(saida)
            arquivo.close()

        with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'_'+dt_string+'.txt', 'r') as arquivo:
            
            nlinhas = (len(arquivo.readlines()))-1

            if nlinhas != fimArquivo :
                tn.write(b" ")
                fimArquivo = nlinhas
                arquivo.close()

            else :
                condicao = True
                arquivo.close()

    tn.write(b"exit\n")
    
    #Limpando informações desnecessárias
    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'_'+dt_string+'.txt', 'r') as arquivo:
            
        texto = arquivo.readlines()

    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'_'+dt_string+'.txt', 'w+') as arquivo:

        
        nlinhas = (len(texto))-2
        for count in range(1,nlinhas):
            texto[count] = texto[count].replace("--More--","")
            texto[count] = texto[count].replace("show Run","")
            texto[count] = texto[count].replace("#","")
            texto[count] = texto[count].replace("\x08","")
            texto[count] = texto[count].strip()
            arquivo.writelines(texto[count]+"\n")
        arquivo.close()
    tn.close()
    dt = datetime.now()
    dt_backup = dt.strftime("%d/%m/%Y %H:%M:%S")
    print("BACKUP HOST "+nomeArquivo+" FINALIZADO"+" as "+dt_backup )

