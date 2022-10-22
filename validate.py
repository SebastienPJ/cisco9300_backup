import time

def saveCurrentScreen(session, server_IP, port_number):
    session.write(b'\r\n')
    screenOutput = session.read_until(b'using this as time.sleep', 2)

    with open(f'SavedScreens/SavedScreen_{server_IP}_{port_number}.txt', 'w') as savedScreenFile:
        savedScreenFile.write(screenOutput.decode('ascii'))
        savedScreenFile.close()

def getCurrentPrompt(filePath):
    endArray = []
    
    with open(filePath) as file:
        for line in file:
            endArray.append(line.replace('\n', ''))
        file.close()

    print(f'Current Prompt: {endArray[-1]}')
    return endArray[-1]