import telnetlib
import login
import time
import cleanup
import pandas as pd
import parser_mainloop

begin = time.perf_counter()

def createBackup(hostname, usrname, passwrd, saved_screen, consoleServerIP, portNumber):
    endLine = f'{hostname}# !!!!!!!!!!'

    tn = telnetlib.Telnet(consoleServerIP, portNumber)
    login.loginSwitch(tn, hostname, usrname, passwrd, saved_screen, consoleServerIP, portNumber)
    
    print(f'Writing backup commands to {hostname}')

    tn.write('\r\n'.encode('ascii'))


    tn.write(b'terminal length 0\r\n show run\r\n show environment all\r\n show version\r\n show module\r\n show interface transceiver\r\n show interface transceiver detail\r\n show inventory\r\n write memory\r\n !!!!!!!!!!\r\n')



    print(f'Waiting until commands finish for {hostname}')
    output = tn.read_until(endLine.encode('ascii')).decode('ascii')
    print(f'Endline match for {hostname}, starting to write to file unprocessed')


    with open(f'BackupOutput/Unprocessed/{hostname}_{consoleServerIP}_{portNumber}_Backup.txt', 'w') as backup_file:
        backup_file.write(output)
        backup_file.close()
    

    print(f'Unprocessed file created for {hostname}, begin removing empty lines')
    cleanup.removeSpaces(f'BackupOutput/Unprocessed/{hostname}_{consoleServerIP}_{portNumber}_Backup.txt', hostname)
    print(f'Empty lines removed from {hostname} file')



df_inputs = pd.read_excel('Cisco9300_Data_Inputs.xlsx')


for data_row in range(len(df_inputs)):

    CONSOLE_SERVER = df_inputs.iloc[data_row]['SERVER IP']
    ### PORT is a numby.int64 data type, must convert to native pyton type with the item() method from numpy
    PORT = df_inputs.iloc[data_row]['PORT'].item()
    HOSTNAME = f'{df_inputs.iloc[data_row]["HOSTNAME"]}'
    USRNAME = f'{df_inputs.iloc[data_row]["USERNAME"]}\n'.encode('ascii')
    PASSWORD = f'{df_inputs.iloc[data_row]["PASSWORD"]}\n'.encode('ascii')


    if PASSWORD == b' \n':
        PASSWORD = '\n'.encode('ascii')


    SAVED_SCREEN = f'SavedScreens/SavedScreen_{CONSOLE_SERVER}_{PORT}.txt'


    createBackup(HOSTNAME, USRNAME, PASSWORD, SAVED_SCREEN, CONSOLE_SERVER, PORT)
    parser_mainloop.parseConfigFile(f'BackupOutput/{HOSTNAME}_Staged.txt')


end = time.perf_counter()
print(f'Code takes: {end - begin} seconds')