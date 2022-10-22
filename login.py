import validate
import time

def loginSwitch(tn_session, hostnme, username, passwrd, server_ip, port):
    print(f'Logging into {hostnme}')
    formatted_hostnme = f'{hostnme}#'

    current_screen = f'SavedScreens/SavedScreen_{server_ip}_{port}.txt'

    tn_session.write(b'\r\n')
    tn_session.read_until(b'using this as time.sleep', 2)   

    validate.saveCurrentScreen(tn_session, server_ip, port)
    prompt = validate.getCurrentPrompt(current_screen)

    while 'Username:' not in prompt and formatted_hostnme not in prompt:
 
        validate.saveCurrentScreen(tn_session, server_ip, port) # This serves as pressing 'enter'
        prompt = validate.getCurrentPrompt(current_screen)

    if formatted_hostnme not in prompt:
        tn_session.write(username)
        validate.saveCurrentScreen(tn_session, server_ip, port)
        prompt = validate.getCurrentPrompt(current_screen)

        tn_session.write(passwrd)
        validate.saveCurrentScreen(tn_session, server_ip, port)
        prompt = validate.getCurrentPrompt(current_screen)

        print(f'Logged into {hostnme} successfully')
    else:
        print(f'Already logged into {hostnme}')
    
