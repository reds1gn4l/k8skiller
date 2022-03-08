import socket, requests

def vuln_verify(host):
    portas_padroes = [443, 10250, 6443, 8443, 42387]
    porta_kubelet = 0
    porta_api = 0
    porta_encontrada_kubelet = False
    porta_encontrada_apiserver = False

    print()
    print("*** SEARCHING VULNERABILITIES IN DEFAULT KUBERNETES PORTS ***")
    print()
    
    
    for i in range(len(portas_padroes)):
        if porta_encontrada_apiserver == True and porta_encontrada_kubelet == True:
            break
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            result = sock.connect_ex((host, portas_padroes[i]))
        except socket.gaierror:
            continue
        if result == 0:
            if porta_encontrada_kubelet == True:
                pass
            hostFull = "https://" + host
            # Será Kubelet ou API SERVER?
            try:
                r = requests.get(hostFull + ":" + str(portas_padroes[i]) + "/runningpods/", verify=False)
            except ConnectionRefusedError:
                continue

            if r.status_code == 200:
                porta_encontrada_kubelet = True
                porta_kubelet = portas_padroes[i]
            else:
                hostFull = "https://" + host
                
                r = requests.get(hostFull + ":" + str(portas_padroes[i]) + "/api/v1/secrets", verify=False)
                
                if r.status_code == 200:
                    porta_encontrada_apiserver = True
                    porta_api = portas_padroes[i]


    if (porta_encontrada_kubelet == False and porta_encontrada_apiserver == False):
            print()
            print("*** SEARCHING VULNERABILITIES IN ALL KUBERNETES PORTS ***")
            print()
            for i in range(80, 65536):
                if i in portas_padroes:
                    continue

                if porta_encontrada_apiserver == True and porta_encontrada_kubelet == True:
                    break
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    try:
                        result = sock.connect_ex((host, i))
                    except socket.gaierror:
                        continue
                    if result == 0:
                        if porta_encontrada_kubelet == True:
                            continue
                        hostFull = "https://" + host
                        # Será Kubelet ou API SERVER?
                        try:
                            r = requests.get(hostFull + ":" + str(i) + "/runningpods/", verify=False)
                        except ConnectionRefusedError:
                            continue

                        if r.status_code == 200:
                            porta_encontrada_kubelet = True
                            porta_kubelet = i
                            break
                        elif porta_encontrada_apiserver == True:
                            hostFull = "https://" + host
                            r = requests.get(hostFull + ":" + str(i) + "/api/v1/secrets", verify=False)
                            if r.status_code == 200:
                                porta_encontrada_apiserver = True
                                porta_api = i
                                break
                        else:
                            print("--- CLUSTER NOT VULNERABLE IN OTHER PORTS! ---")
        

    if porta_encontrada_apiserver == True and porta_encontrada_kubelet == True:
        while True:
            qual = int(input("Host may be vulnerable to all available attacks. What to choose? (1 = Kubelet ou 2 = API Server): "))
            if qual == 1:
                hostFull = "https://" + host + ":" + str(porta_kubelet)
                break
            elif qual == 2:
                hostFull = "https://" +  host + ":" + (porta_api)
                break
            else:
                continue
    elif porta_encontrada_apiserver == True and porta_encontrada_kubelet == False:
        hostFull = "https://" +  host + ":" + str(porta_api)
    elif porta_encontrada_kubelet == True and porta_encontrada_apiserver == False:
        hostFull = "https://" +  host + ":" + str(porta_kubelet)

    return porta_encontrada_kubelet, porta_encontrada_apiserver, hostFull