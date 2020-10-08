# packages
try:
    import os
    from paramiko import client
    from datetime import datetime, timedelta
except Exception as e:
    print(e)


# classes
class SSH:

    def __init__(self, address, user, secret):
        self.client = client.SSHClient()
        self.client.set_missing_host_key_policy(client.AutoAddPolicy())
        self.client.connect(address, username=user, password=secret, look_for_keys=False)

    def output(self, command):
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            while not stdout.channel.exit_status_ready():
                # Print data when available
                if stdout.channel.recv_ready():
                    alldata = stdout.channel.recv(1024)
                    prevdata = b"1"

                    while prevdata:
                        prevdata = stdout.channel.recv(1024)
                        alldata += prevdata

                    for data in str(alldata, 'utf-8').splitlines():
                        file_data.append(data.split('|')[1])

        else:
            print("Connection not opened.")

    def close_session(self):
        self.client.close()


# credentials
username = 'xxxxx'
password = 'xxxxx'
server = 'xxxxx'
file_data = []

# check_date = input("Input date YYYYMMDD: ")
check_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d") # backdate
filename = "uvc_errors_" + check_date
file_directory = os.getcwd() + '\\'
completeFileName = file_directory + filename + ".txt"

# connecting to server
try:
    send_command = "cd cdr/outbak/uvc/recharge/" + check_date + " ; cat uvc_abr*.unl"
    connection = SSH(server, username, password)
    connection.output(send_command)
    connection.close_session()
except Exception as e:
    print(e)

# open and write data into file
f = open(completeFileName, "w")
for data in file_data:
    f.write(data + '\n')
f.write('\n\n')
for data in file_data:
    f.write('\'' + data + '\',\n')
f.close()


print("Finished")

