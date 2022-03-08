from terminaltables import AsciiTable

def pod_table_kubelet(pod, namespace, container):
    table_data = [
                ["ID", "POD", "NAMESPACE", "CONTAINER"],
            ]
    for i in range(len(pod)):
        table_data.append([(i+1), pod[i], namespace[i], container[i]])
            
    table = AsciiTable(table_data)
        
    return table.table