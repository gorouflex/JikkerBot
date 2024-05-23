import json, time, threading, keyboard, sys, os, win32api, webbrowser, urllib.request
from ctypes import WinDLL
import numpy as np
from mss import mss as mss_module
from configparser import ConfigParser

LOCAL_VERSION = "0.0.3"
LATEST_VERSION_URL = "https://github.com/gorouflex/JikkerBot/releases/latest"
GITHUB_API_URL = "https://api.github.com/repos/gorouflex/JikkerBot/releases/latest"
current_dir = os.path.dirname(os.path.realpath(__file__))

CONFIG_PATH = current_dir + '\\config.ini'
cfg = ConfigParser()
cfg.read(CONFIG_PATH)
user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)

shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

ZONE = 5
GRAB_ZONE = (
    int(WIDTH / 2 - ZONE),
    int(HEIGHT / 2 - ZONE),
    int(WIDTH / 2 + ZONE),
    int(HEIGHT / 2 + ZONE),
)

sct = mss_module()
jikkerbot = False
jikkerbot_toggle = True
exit_program = False 
toggle_lock = threading.Lock()

def clear():
    os.system('cls')
    print(r"""
      _ _ _    _             ____        _   
     | (_) | _| | _____ _ __| __ )  ___ | |_ 
  _  | | | |/ / |/ / _ \ '__|  _ \ / _ \| __|
 | |_| | |   <|   <  __/ |  | |_) | (_) | |_ 
  \___/|_|_|\_\_|\_\___|_|  |____/ \___/ \__|""")
    print()
    print(f"  Version: {LOCAL_VERSION} by GorouFlex (Alpha Dev Preview - Project SimpleTool)")
    print()

def welcome_tutorial():
    if not cfg.has_section('Settings'):
        cfg.add_section('Settings')
    clear()
    print()
    print("Welcome to JikkerBot - help you aim better")
    print("Support FPS game from a Music Company")
    print()
    trigger = input("Enter your trigger hotkey (virtual key code) (default is 0xA0): ")
    base = input("Enter your base delay (default is 0.01): ")
    delay = input("Enter your trigger delay (default is 40): ")
    color = input("Enter your color tolerance (max: 100, default: 70): ")
    always = input("Do you want use Toggle mode? (no need to hold trigger key) (y/n): ")
    if always.lower() == 'y':
       hold = '1'
    else:
       hold = '0'
    cfg.set('Settings', 'TriggerKey', trigger)
    cfg.set('Settings', 'BaseDelay', base)
    cfg.set('Settings', 'TriggerDelay', delay)
    cfg.set('Settings', 'Tolerance', color)
    cfg.set('Settings', 'HoldMode', hold)
    cfg.set('Settings', 'SoftwareUpdate', '1')
    cfg.set('Settings', 'ApplyOnStart', '0')
    with open(CONFIG_PATH, 'w') as config_file:
        cfg.write(config_file)

def settings():
    options = {
        "1": trigger_cfg,
        "2": base_cfg,
        "3": delay_cfg,
        "4": tolerance_cfg,
        "5": holdmode_cfg,
        "6": cfu_cfg,
        "7": applystart_cfg,
        "r": reset,
        "b": "break"
    }
    while True:
        clear()
        print("--------------- Settings ---------------")
        print("1. Trigger hotkey\n2. Base delay")
        print("3. Trigger delay")
        print("4. Color tolerance\n5. Hold mode")
        print("6. Software Updates\n7. Run on start")
        print("")
        print("R. Reset all saved settings")
        print("B. Back")
        settings_choice = input("Option: ").lower().strip()
        action = options.get(settings_choice, None)
        if action is None:
            print("Invalid option.")
            input("Press Enter to continue...")
        elif action == "break":
            break
        else:
            action()

def trigger_cfg():
    while True:
        clear()
        print("--------------- Trigger hotkey ---------------")
        print("(Trigger hotkey to hold)")
        trigger = cfg.get('Settings', 'TriggerKey', fallback='0xA0')
        print(f"Current setting: {trigger}")
        print("\n1. Change Trigger hotkey")
        print("\nB. Back")
        choice = input("Option: ").strip()
        if choice == "1":
            new = input("Enter your value: ")
            cfg.set('Settings', 'TriggerKey', new)
        elif choice.lower() == "b":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)

def base_cfg():
    while True:
        clear()
        print("--------------- Base delay ---------------")
        print("(Base delay)")
        base = cfg.get('Settings', 'BaseDelay', fallback='0.01')
        print(f"Current setting: {base}")
        print("\n1. Change Base delay")
        print("\nB. Back")
        choice = input("Option: ").strip()
        if choice == "1":
            new = input("Enter your value (default is 0.01): ")
            cfg.set('Settings', 'BaseDelay', new)
        elif choice.lower() == "b":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)

def delay_cfg():
    while True:
        clear()
        print("--------------- Trigger delay ---------------")
        print("(Trigger delay)")
        delay = cfg.get('Settings', 'TriggerDelay', fallback='40')
        print(f"Current setting: {delay}")
        print("\n1. Change Trigger delay")
        print("\nB. Back")
        choice = input("Option: ").strip()
        if choice == "1":
            new = input("Enter your value (default is 40): ")
            cfg.set('Settings', 'TriggerDelay', new)
        elif choice.lower() == "b":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)

def tolerance_cfg():
    while True:
        clear()
        print("--------------- Color tolerance ---------------")
        print("(Color detect sensitive - Min: 0 Max: 100)")
        tolerance = cfg.get('Settings', 'Tolerance', fallback='70')
        print(f"Current setting: {tolerance}")
        print("\n1. Change color tolerance")
        print("\nB. Back")
        choice = input("Option: ").strip()
        if choice == "1":
            new = input("Enter your value (default is 70): ")
            cfg.set('Settings', 'Tolerance', new)
        elif choice.lower() == "b":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)

def holdmode_cfg():
    while True:
        clear()
        print("--------------- Hold mode ---------------")
        print("(Hold trigger key to tracking)")
        hold_enabled = cfg.get('Settings', 'HoldMode', fallback='1') == '1'
        print("Status: Enabled" if hold_enabled else "Status: Disabled")
        print("\n1. Enable Hold mode\n2. Disable Hold mode")
        print("\nB. Back")
        choice = input("Option: ").strip()
        if choice == "1":
            cfg.set('Settings', 'HoldMode', '1')
        elif choice == "2":
            cfg.set('Settings', 'HoldMode', '0')
        elif choice.lower() == "b":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)

def applystart_cfg():
    while True:
        clear()
        print("--------------- Apply on start ---------------")
        print("(Apply when start)")
        start_enabled = cfg.get('Settings', 'ApplyOnStart', fallback='1') == '1'
        print("Status: Enabled" if start_enabled else "Status: Disabled")
        print("\n1. Enable Apply on start\n2. Disable Apply on start")
        print("\nB. Back")
        choice = input("Option: ").strip()
        if choice == "1":
            cfg.set('Settings', 'ApplyOnStart', '1')
        elif choice == "2":
            cfg.set('Settings', 'ApplyOnStart', '0')
        elif choice.lower() == "b":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue...")
        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)

def cfu_cfg():
    while True:
        clear()
        cfu_enabled = cfg.get('Settings', 'SoftwareUpdate', fallback='1') == '1'
        print("--------------- Software update ---------------")
        print(f"Status: {'Enabled' if cfu_enabled else 'Disabled'}")
        print("\n1. Enable Software update\n2. Disable Software update\n\nB. Back")
        choice = input("Option: ").strip()
        if choice == "1":
            cfg.set('Settings', 'SoftwareUpdate', '1')
        elif choice == "2":
            cfg.set('Settings', 'SoftwareUpdate', '0')
        elif choice.lower() == "b":
            break
        else:
            print("Invalid option.")
            input("Press Enter to continue.")
        with open(CONFIG_PATH, 'w') as config_file:
            cfg.write(config_file)


def check_cfg_integrity() -> None:
    if not os.path.isfile(CONFIG_PATH) or os.stat(CONFIG_PATH).st_size == 0:
        welcome_tutorial()
        return
    required_keys_settings = ['TriggerKey', 'BaseDelay', 'TriggerDelay', 'Tolerance', 'HoldMode', 'SoftwareUpdate', 'ApplyOnStart']
    if not cfg.has_section('Settings') or any(key not in cfg['Settings'] for key in required_keys_settings): 
       reset()

def reset():
    os.remove(CONFIG_PATH)
    welcome_tutorial()

def get_latest_ver():
    latest_version = urllib.request.urlopen(LATEST_VERSION_URL).geturl()
    return latest_version.split("/")[-1]

def get_changelog():
    request = urllib.request.Request(GITHUB_API_URL)
    response = urllib.request.urlopen(request)
    data = json.loads(response.read())
    return data['body']

def check_updates():
    clear()
    max_retries = 10
    skip_update_check = False
    for i in range(max_retries):
        try:
            latest_version = get_latest_ver()
        except:
            if i < max_retries - 1:
                print(f"Failed to fetch latest version. Retrying {i+1}/{max_retries}...")
                time.sleep(5)
            else:
                clear()
                print("Failed to fetch latest version. Please check if your Python is installed with SSL cert or not?")
                result = input("Do you want to skip the check for updates? (y/n): ").lower().strip()
                if result == "y":
                    skip_update_check = True
                else:
                    print("Quitting...")
                    raise SystemExit
    if not skip_update_check:
        if LOCAL_VERSION < latest_version:
            updater()
        elif LOCAL_VERSION > latest_version:
            clear()
            print("Welcome to the JikkerBot Beta Program")
            print("This beta build may not work as expected and is only for testing purposes!")
            result = input("Do you want to continue (y/n): ").lower().strip()
            if result == "y":
                pass
            else:
                print("Quitting...")
                raise SystemExit

def cooldown():
    global jikkerbot_toggle, toggle_lock, jikkerbot
    time.sleep(0.1)
    with toggle_lock:
        jikkerbot_toggle = True
        kernel32.Beep(440, 75), kernel32.Beep(700, 100) if jikkerbot else kernel32.Beep(440, 75), kernel32.Beep(200, 100)

def searcherino():
    global jikkerbot, sct
    R, G, B = (250, 100, 250)  # purple
    img = np.array(sct.grab(GRAB_ZONE))
    pmap = np.array(img)
    pixels = pmap.reshape(-1, 4)
    color_tolerance = int(cfg.get('Settings', 'Tolerance', fallback='70'))
    color_mask = (
        (pixels[:, 0] > R -  color_tolerance) & (pixels[:, 0] < R +  color_tolerance) &
        (pixels[:, 1] > G -  color_tolerance) & (pixels[:, 1] < G +  color_tolerance) &
        (pixels[:, 2] > B -  color_tolerance) & (pixels[:, 2] < B +  color_tolerance)
    )
    matching_pixels = pixels[color_mask]
    trigger_delay = cfg.get('Settings', 'TriggerDelay', fallback='40')
    base_delay = cfg.get('Settings', 'BaseDelay', fallback='0.01')
    if jikkerbot and len(matching_pixels) > 0: 
        delay_percentage = float(trigger_delay) / 100.0
        actual_delay = float(base_delay) + float(base_delay) * delay_percentage
        time.sleep(actual_delay)
        keyboard.press_and_release("k")

def toggle():
    global jikkerbot, jikkerbot_toggle, exit_program, toggle_lock
    print("Start tracking, to active/deactive press F10 or Fn + F10")
    print("Ctrl + Shift + X to exit")
    while True:
        if keyboard.is_pressed("f10"):  
            with toggle_lock:
                if jikkerbot_toggle:
                    jikkerbot = not jikkerbot
                    print(jikkerbot)
                    jikkerbot_toggle = False
                    threading.Thread(target=cooldown).start()
        if keyboard.is_pressed("ctrl+shift+x"):
            exit_program = True
            sys.exit() 
        time.sleep(0.1) 

def hold():
    global jikkerbot, exit_program
    trigger_hotkey = cfg.get('Settings', 'TriggerKey', fallback="0xA0")
    trigger_hotkey = int(trigger_hotkey, 16)
    clear()
    print("Start tracking, please hold your hotkey to active")
    print("Ctrl + Shift + X to exit")
    while True:
        while win32api.GetAsyncKeyState(trigger_hotkey) < 0:
            jikkerbot = True
            searcherino()
        else:
            time.sleep(0.1)
        if keyboard.is_pressed("ctrl+shift+x"):  
            exit_program = True
            sys.exit()

def starterino():
    global exit_program, jikkerbot
    always_enabled = cfg.get('Settings', 'HoldMode', fallback='0')
    while not exit_program: 
        if always_enabled == '1':
            toggle()
            searcherino() if jikkerbot else time.sleep(0.1)
        else:
            hold()

def about():
    options = {
        "1": lambda: webbrowser.open("https://www.github.com/AppleOSX/UXTU4Unix"),
    #    "f": updater,
        "b": "break",
    }
    while True:
        clear()
        print("About JikkerBot")
        print("The L2T Dream (AlphaL2TDreamNV1)")
        print("----------------------------")
        print("Maintainer: GorouFlex\nCLI: GorouFlex")
        print("----------------------------")
        try:
          print(f"F. Force update to the latest version ({get_latest_ver()})")
        except:
           pass
        print("")
        print("GG! GitHub!")
        print("Thanks GitHub for suspended me for no reason")
        print("\nB. Back")
        choice = input("Option: ").lower().strip()
        action = options.get(choice, None)
        if action is None:
            print("Invalid option.")
            input("Press Enter to continue...")
        elif action == "break":
            break
        else:
            action()

def main():
    check_cfg_integrity()
   # if cfg.get('Settings', 'SoftwareUpdate', fallback='0') == '1':
  #      check_updates()
    if cfg.get('Settings', 'ApplyOnStart', fallback='1') == '1':  
        starterino()
    while True:
        clear()
        options = {
            "1": starterino,
            "2": settings,
            "a": about,
            "q": lambda: sys.exit("\nThanks for using JikkerBot\nHave a nice day!"),
        }
        print("1. Start tracking\n2. Settings")
        print("")
        print("A. About JikkerBot")
        print("Q. Quit")
        choice = input("Option: ").lower().strip()
        if action := options.get(choice):
            action()
        else:
            print("Invalid option.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
