import telnetlib
import login
import cleanup
import time
import pandas as pd
import parser_mainloop

begin = time.perf_counter()


def recursiveBackup(args_array):
    if len(args_array) == 0:
        print('Base case reached!')
        return
    
    current_input = args_array[0]

    consoleServerIP = current_input[0]
    portNumber = current_input[1]
    hostnme = current_input[2]
    usrname = current_input[3]
    passwrd = current_input[4]

    endLine = f'{hostnme}# !!!!!!!!!!'

    
    tn = telnetlib.Telnet(consoleServerIP, portNumber)


    login.loginSwitch(tn, hostnme, usrname, passwrd, consoleServerIP, portNumber)

    print(f'Writing backup commands to {hostnme}')

    tn.write(b'terminal length 0\r\n show run\r\n show environment all\r\n show version\r\n show module\r\n show interface transceiver\r\n show interface transceiver detail\r\n show inventory\r\n !!!!!!!!!!\r\n write memory\r\n')


    recursiveBackup(args_array[1:])

    print(f'Waiting until commands finish for {hostnme}')
    output = tn.read_until(endLine.encode('ascii')).decode('ascii')
    print(f'Endline match for {hostnme}, starting to write to file unprocessed')

    with open(f'BackupOutput/Unprocessed/{hostnme}_{consoleServerIP}_{portNumber}_Backup.txt', 'w') as backup_file:
        backup_file.write(output)
        backup_file.close()

    print(f'Unprocessed file created for {hostnme}, begin removing empty lines')

    cleanup.removeSpaces(f'BackupOutput/Unprocessed/{hostnme}_{consoleServerIP}_{portNumber}_Backup.txt', hostnme)
    
    print(f'Empty lines removed from {hostnme} file')

    parser_mainloop.parseConfigFile(f'BackupOutput/{hostnme}_Staged.txt')

    tn.close()



df_inputs = pd.read_excel('Cisco9300_Data_Inputs.xlsx')

args = []

for data_row in range(len(df_inputs)):

    console_server_IP = df_inputs.iloc[data_row]['SERVER IP']

    ### PORT is a numby.int64 data type, must convert to native pyton type with the item() method from numpy
    port = df_inputs.iloc[data_row]['PORT'].item()
    hostname = f'{df_inputs.iloc[data_row]["HOSTNAME"]}'
    username = f'{df_inputs.iloc[data_row]["USERNAME"]}'.encode('ascii')
    password = f'{df_inputs.iloc[data_row]["PASSWORD"]}'.encode('ascii')

    inputs = [console_server_IP, port, hostname, username, password]

    args.append(inputs)


recursiveBackup(args)



end = time.perf_counter()
time_in_seconds = end - begin
time_in_minutes = time_in_seconds / 60

print(f'Code takes: {time_in_seconds} seconds')
print(f'Code takes: {time_in_minutes} minutes')