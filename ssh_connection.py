import paramiko
import datetime
import os.path
import time
import sys
import re

user_file = input("\n# Enter user file path and name (e.g. D:\MyApps\myfile.txt): ")

if os.path.isfile(user_file) == True:
    print("\n* Username/password file is valid :) \n")
else:
    print("\n* File {} does not exist :( Please check and try again.\n".format(user_file))
    sys.exit()
    
cmd_file = input("\n* Enter commands file path and name (e.g. D:\MyApps\myfile.txt): ")

if os.path.isfile(cmd_file) == True:
    print("\n* Command file is valid :)\n")

else:
    print("\n* File {} does not exist :( Please check and try again.\n".format(cmd_file))
    sys.exit()
 
def ssh_connection(ip):

        global user_file
        global cmd_file
        
        try:
            
            selected_user_file = open(user_file, 'r')
            
            
            selected_user_file.seek(0)
            
            username = selected_user_file.readlines()[0].split(',')[0].rstrip("\n")
            
            selected_user_file.seek(0)
            
            password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
            
            session = paramiko.SSHClient()
            
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            session.connect(ip.rstrip("\n"), username = username, password = password)
            
            connection = session.invoke_shell()
            
            connection.send("enable\n")
            connection.send("terminal length 0\n")
            time.sleep(1)
            
            connection.send("\n")
            connection.send("configure terminal\n")
            time.sleep(1)
            
            selected_cmd_file = open(cmd_file, 'r')
            
            selected_cmd_file.seek(0)
            
            for each_line in selected_cmd_file.readlines():
                connection.send(each_line + '\n')
                time.sleep(2)
                
            selected_user_file.close()
            
            selected_cmd_file.close()
            
            router_output = connection.recv(65535)
            
            if re.search(b"% Invalid input", router_output):
                print("* There was at least one IOS syntex error on device {} :(".format(ip))
            else: 
                print("\nDONE for device {}. Data sent to file at {}.\n".format(ip, str(datetime.datetime.now())))
            
            #cpu = re.search(b"%Cpu\(s\):(\s)+(.+?)(\s)* us,", router_output)
            cpu = re.search(b"%Cpu\(s\):(\s)+(.+?)(\s)* us,", router_output)
            #cpu = re.search(b"%Cpu\(s\):(\s)+(.+?)(\s)+us,", router_output)

            utilization = cpu.group(2).decode("utf-8")

            with open("E:\\Python\\Python-Network-App-2\\cpu.txt", "a") as f:

                f.write(utilization + "\n")
            # print(re.findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", str(router_output))[1])
            
            session.close()
            
        except paramiko.AuthenticationException:
            print("* Invalid username or password : ( \n* Please check the username/password file or the device configuration.")
            print("* Closing program... Bye!")