import json
import os
import argparse

text = 'Для разбора лог файла можно выбрать директорию --paht указав полный путь и увзвть имя файла --name, если путь и имя не указывать то будет разбор всех файтов с расширение .log в дериктории где лежит скрипт'

parser = argparse.ArgumentParser(description=text)
parser.add_argument("--path", help="'пример --path /home/user/")
parser.add_argument("--name", help="'пример --name access.log")

args = parser.parse_args()

def read_file_line(logs_files):
    with open(logs_files, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            yield line

def log_to_json(path, nam_file):
    file_line = read_file_line(f"{path}/{nam_file}")
    all_requests = 0
    methods = {"GET": 0, "HEAD": 0, "POST": 0, "PUT": 0, "DELETE": 0, "CONNECT": 0, "OPTIONS": 0, "TRACE": 0, "PATCH": 0}
    name_hosts = {}
    hosts_top = {}
    linst_top_1 = []
    linst_top_2 = []
    linst_top_3 = []

    for i in file_line:
        all_requests += 1
        list_one_line = i.split()
        if linst_top_1 == []:
            linst_top_1 = list_one_line
        else:
            if int(linst_top_1[-1]) < int(list_one_line[-1]):
                linst_top_2 = linst_top_1
                linst_top_1 = list_one_line
            else:
                if linst_top_2 == []:
                    linst_top_2 = list_one_line
                if int(linst_top_2[-1]) < int(list_one_line[-1]):
                    linst_top_3 = linst_top_2
                    linst_top_2 = list_one_line
                else:
                    if linst_top_3 == []:
                        linst_top_3 = list_one_line
                    if int(linst_top_3[-1]) < int(list_one_line[-1]):
                        linst_top_3 = list_one_line

        name_request = list_one_line[5][1:]
        hosts = list_one_line[0]
        if name_request in methods.keys():
            methods[name_request] += 1
        if hosts in name_hosts.keys():
            name_hosts[hosts] +=1
        else:
            name_hosts.setdefault(hosts, 1)

    for i in range(3):
        pass
        name_hosts_top_1 = max(name_hosts, key=name_hosts.get)
        hosts_top[name_hosts_top_1] = name_hosts[name_hosts_top_1]
        del name_hosts[name_hosts_top_1]

    lin_top_1 = {"method": linst_top_1[5][1:], "url": linst_top_1[6], "ip": linst_top_1[0], "duration_sec": linst_top_1[-1], "data":linst_top_1[3][1:]}
    lin_top_2 = {"method": linst_top_2[5][1:], "url": linst_top_2[6], "ip": linst_top_2[0], "duration_sec": linst_top_2[-1], "data":linst_top_2[3][1:]}
    lin_top_3 = {"method": linst_top_3[5][1:], "url": linst_top_3[6], "ip": linst_top_3[0], "duration_sec": linst_top_3[-1], "data":linst_top_3[3][1:]}

    res = {"all_requests": all_requests, "methods": [methods], "3_hosts_top": [hosts_top], "3_lin_top": [lin_top_1, lin_top_2, lin_top_3]}

    with open("result.json", "w") as f:
        json.dump(res, f)

    res_json = json.dumps(res, indent=4)
    print(res_json)
    print("---"*10)

def file_logs(path, name=False):
    list_files = sorted(os.listdir(path))
    if name:
        log_to_json(path, name)
    else:
        for file in list_files:
            if ".log" in file:
                print(f"file = {file}")
                log_to_json(path, file)



if args.path:
    path = args.path
    path_files = args.path
else:
    path_files = os.path.abspath(os.curdir)


if args.name:
    name = args.name
    file_logs(path_files, name)
else:
    file_logs(path_files)


