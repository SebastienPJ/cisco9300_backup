# cisco9300_backup



Two methods of backing up Cisco switch configurations using a console server and telnet. One uses a linear methodology and the other recursively traverses through the Data Inputs file. Programs, logs into switch using information from Data-Inputs excel file and executes various backup commands, saving the output in the BackupOutput folder.

Program also includes a parser functionality that takes the resulting .txt backup file, extracts the serial numbers of the parts (currently Switch members, Power-supply, DAC cabels, Uplink Module) and saves them to an Excel Sheet for easy viewing.

Functionality will be expanded.