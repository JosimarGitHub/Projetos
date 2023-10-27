#Bibliotecas importadas
import telnetlib
import os

#Informações para Acesso via Telnet
with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/IOS_LAB/Hosts_Bootcamp.txt','r') as arquivo:

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
    condicao = False
    fimArquivo = 0
    print("FAZENDO BACKUP HOST "+nomeArquivo )
    #Gerando Arquivo de Backup
    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'.txt', 'w+') as arquivo:
        arquivo.close()

    #Salvando Running config em arquivo txt
    while condicao == False :

        with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'.txt', 'a') as arquivo:
        
            saida = (tn.read_until(b" --More-- ",10).decode('ascii'))
            arquivo.write(saida)
            arquivo.close()

        with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'.txt', 'r') as arquivo:
            
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
    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'.txt', 'r') as arquivo:
            
        texto = arquivo.readlines()

    with open('/media/dev_net/Disk_2/BOOT_CAMP_ENCORE/Backups_Telnet/'+ nomeArquivo+'.txt', 'w+') as arquivo:

        
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
    print("BACKUP HOST "+nomeArquivo+" FINALIZADO" )

