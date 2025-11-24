import time
import os
import subprocess
import shutil
import socket
import sys
from datetime import datetime

try:
    import requests
except ImportError:
    print('[+] Installing required package: requests')
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', 'requests[socks]'], check=True)
    import requests

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print('[+] Installing required package: colorama')
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'colorama'], check=True)
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

tor_path = None
tor_process = None
tor_data_dir = None

# UI Helper Functions
def print_box(text, color=Fore.CYAN, width=70):
    """Print text in a colored box"""
    import re
    print(color + "╔" + "═" * (width - 2) + "╗" + Style.RESET_ALL)
    lines = text.split('\n')
    for line in lines:
        # Calculate visible length without ANSI codes
        visible_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
        padding = width - len(visible_line) - 4  # -4 for "║ " and " ║"
        if padding < 0:
            padding = 0
        print(color + "║ " + line + " " * padding + " ║" + Style.RESET_ALL)
    print(color + "╚" + "═" * (width - 2) + "╝" + Style.RESET_ALL)

def print_header():
    """Print stylish header"""
    os.system("cls")
    print("\n")
    print(Fore.CYAN + Style.BRIGHT + "    ═══════════════════════════════════════════════════════════════════" + Style.RESET_ALL)
    print()
    print(Fore.GREEN + Style.BRIGHT + """
                ██████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ 
                ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔═══██╗██╔══██╗
                ██████╔╝ ╚████╔╝    ██║   ██║   ██║██████╔╝
                ██╔═══╝   ╚██╔╝     ██║   ██║   ██║██╔══██╗
                ██║        ██║      ██║   ╚██████╔╝██║  ██║
                ╚═╝        ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    """ + Style.RESET_ALL)
    print(f"{Fore.YELLOW}{Style.BRIGHT}                         Version 1.2{Style.RESET_ALL}")
    print(f"{Fore.CYAN}                    Automatic IP Rotator{Style.RESET_ALL}")
    print()
    print(f"{Fore.MAGENTA}                   Created by: prshhnt{Style.RESET_ALL}")
    print(f"{Fore.BLUE}              https://github.com/prshhnt/PyTor{Style.RESET_ALL}")
    print()
    print(Fore.CYAN + Style.BRIGHT + "    ═══════════════════════════════════════════════════════════════════" + Style.RESET_ALL)
    print()

def print_status(message, status="info"):
    """Print formatted status messages"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if status == "success":
        icon = "✓"
        color = Fore.GREEN
    elif status == "error":
        icon = "✗"
        color = Fore.RED
    elif status == "warning":
        icon = "⚠"
        color = Fore.YELLOW
    else:
        icon = "ℹ"
        color = Fore.CYAN
    
    print(f"{Fore.WHITE}[{timestamp}] {color}{Style.BRIGHT}{icon}{Style.RESET_ALL} {color}{message}{Style.RESET_ALL}")

def print_separator(char="─", width=70, color=Fore.CYAN):
    """Print a separator line"""
    print(color + char * width + Style.RESET_ALL)

def print_progress_bar(iteration, total, prefix='', suffix='', length=40, fill='█'):
    """Print a progress bar"""
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '░' * (length - filled_length)
    print(f'\r{Fore.CYAN}{prefix} {Fore.GREEN}|{bar}| {Fore.YELLOW}{percent}% {Fore.CYAN}{suffix}', end='\r')
    if iteration == total:
        print()

def create_torrc():
    """Generate Tor configuration file with control port enabled"""
    global tor_data_dir
    tor_data_dir = os.path.join(os.path.expanduser('~'), '.pytor_data')
    if not os.path.exists(tor_data_dir):
        os.makedirs(tor_data_dir)
    
    torrc_path = os.path.join(tor_data_dir, 'torrc')
    torrc_content = f'''SocksPort 9050
ControlPort 9051
DataDirectory {tor_data_dir.replace(os.sep, '/')}
CookieAuthentication 0
'''
    
    with open(torrc_path, 'w') as f:
        f.write(torrc_content)
    
    return torrc_path

def find_tor_windows():
    """Locate Tor executable on Windows system"""
    common_paths = [
        r"C:\Program Files\Tor Browser\Browser\TorBrowser\Tor\tor.exe",
        r"C:\Program Files (x86)\Tor Browser\Browser\TorBrowser\Tor\tor.exe",
        r"C:\Users\{}\AppData\Local\Tor Browser\Browser\TorBrowser\Tor\tor.exe".format(os.getenv('USERNAME')),
        r"C:\Tor\tor.exe",
        r"C:\Program Files\Tor\tor.exe"
    ]
    
    tor_in_path = shutil.which('tor')
    if tor_in_path:
        return tor_in_path
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
    if os.path.exists(downloads):
        for root, dirs, files in os.walk(downloads):
            if 'tor.exe' in files and 'tor' in root.lower():
                return os.path.join(root, 'tor.exe')
    
    return None

print_header()

try:
    print_status("Searching for Tor installation...", "info")
    tor_path = find_tor_windows()
    if not tor_path:
        print_status("Tor not found on system!", "error")
        print_box("Tor is required to run PyTor.\nPlease run install.py to set up Tor.", Fore.YELLOW)
        print(f"\n{Fore.CYAN}Or specify tor.exe path manually:{Style.RESET_ALL}")
        manual_path = input(f'{Fore.YELLOW}  → Enter path to tor.exe (or press Enter to exit): {Style.RESET_ALL}').strip()
        if manual_path and os.path.exists(manual_path):
            tor_path = manual_path
            print_status(f"Tor located at: {tor_path}", "success")
        else:
            print_status("Tor not found. Exiting.", "error")
            exit(1)
    else:
        print_status(f"Tor located: {tor_path}", "success")
except Exception as e:
    print_status(f"Error: {e}", "error")
    exit(1)

print_separator()

def get_current_ip():
    """Fetch current IP address through Tor proxy"""
    url = 'http://checkip.amazonaws.com'
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    for attempt in range(3):
        try:
            response = requests.get(url, proxies=proxies, timeout=15)
            return response.text.strip()
        except:
            if attempt < 2:
                time.sleep(2)
    return None

def change_identity():
    """Request new Tor identity to change IP address"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect(('127.0.0.1', 9051))
            
            sock.sendall(b'AUTHENTICATE ""\r\n')
            response = sock.recv(1024)
            
            if b'250 OK' in response:
                sock.sendall(b'SIGNAL NEWNYM\r\n')
                response = sock.recv(1024)
                
                if b'250 OK' in response:
                    print(f"{Fore.CYAN}  ⟳ Requesting new identity...{Style.RESET_ALL}", end='', flush=True)
                    time.sleep(5)
                    new_ip = get_current_ip()
                    if new_ip:
                        print(f"\r{Fore.GREEN}  ✓ New IP: {Style.BRIGHT}{new_ip}{Style.RESET_ALL}                    ")
                    else:
                        print(f"\r{Fore.YELLOW}  ⚠ IP rotated (Tor proxy busy)                    {Style.RESET_ALL}")
                    return
            else:
                raise Exception("Authentication failed")
    except Exception as control_error:
        print(f"\r{Fore.YELLOW}  ⚠ Control port failed, restarting Tor...{Style.RESET_ALL}")
        global tor_process
        if tor_process and tor_process.poll() is None:
            tor_process.terminate()
            time.sleep(2)
        
        torrc_path = os.path.join(tor_data_dir, 'torrc')
        tor_process = subprocess.Popen(
            [tor_path, '-f', torrc_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        time.sleep(8)
        new_ip = get_current_ip()
        if new_ip:
            print(f"{Fore.GREEN}  ✓ Tor restarted - New IP: {Style.BRIGHT}{new_ip}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}  ⚠ Tor restarted (verification failed){Style.RESET_ALL}")

print_status("Initializing Tor service...", "info")

try:
    subprocess.run('taskkill /F /IM tor.exe', shell=True, capture_output=True, timeout=5)
    time.sleep(1)
    print_status("Cleared existing Tor processes", "success")
except:
    pass

try:
    torrc_path = create_torrc()
    print_status(f"Configuration file created", "success")
    
    print_status("Starting Tor daemon...", "info")
    tor_process = subprocess.Popen(
        [tor_path, '-f', torrc_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    )
    
    print(f"\n{Fore.CYAN}Establishing Tor connection...{Style.RESET_ALL}")
    for i in range(150):
        time.sleep(0.1)
        print_progress_bar(i + 1, 150, prefix='Connecting:', suffix='Complete')
    
    current_ip = get_current_ip()
    if current_ip:
        print_status(f"Connected successfully! Your IP: {Fore.GREEN}{Style.BRIGHT}{current_ip}", "success")
    else:
        print_status("Tor started but connection verification failed", "warning")
        print_status("Waiting for bootstrap to complete...", "info")
        time.sleep(5)
        current_ip = get_current_ip()
        if current_ip:
            print_status(f"Connected! Your IP: {Fore.GREEN}{Style.BRIGHT}{current_ip}", "success")
        
except Exception as e:
    print_status(f"Tor initialization failed: {e}", "error")
    print_status("Ensure ports 9050/9051 are available", "warning")
    exit(1)

print_separator()
print_box("Configure your browser to use SOCKS5 proxy:\n  Host: 127.0.0.1\n  Port: 9050", Fore.GREEN)
print_separator()

print(f"\n{Fore.CYAN}{Style.BRIGHT}Configuration:{Style.RESET_ALL}\n")
interval = input(f"  {Fore.YELLOW}→ IP change interval in seconds {Fore.WHITE}[default: 60]: {Style.RESET_ALL}") or "60"
count = input(f"  {Fore.YELLOW}→ Number of changes {Fore.WHITE}[0 = infinite]: {Style.RESET_ALL}") or "0"

try:
    interval = int(interval)
    count = int(count)

    print_separator()
    if count == 0:
        print_box(f"Starting infinite IP rotation\nInterval: {interval} seconds\nPress Ctrl+C to stop", Fore.GREEN)
        print_separator()
        
        rotation_count = 0
        while True:
            try:
                print(f"\n{Fore.CYAN}Waiting {interval} seconds until next rotation...{Style.RESET_ALL}")
                for i in range(interval):
                    time.sleep(1)
                    remaining = interval - i - 1
                    print(f"\r{Fore.YELLOW}  Next change in: {Fore.WHITE}{Style.BRIGHT}{remaining:3d}{Style.RESET_ALL}{Fore.YELLOW} seconds{Style.RESET_ALL}", end='')
                
                print(f"\n\n{Fore.CYAN}{Style.BRIGHT}═══ Rotation #{rotation_count + 1} ═══{Style.RESET_ALL}")
                change_identity()
                rotation_count += 1
                print_separator()
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}{'═' * 70}{Style.RESET_ALL}")
                print_status(f"IP rotation stopped. Total rotations: {rotation_count}", "success")
                
                keep_tor = input(f"\n{Fore.CYAN}Keep Tor running in background? (Y/N): {Style.RESET_ALL}").strip().upper()
                if keep_tor != 'Y':
                    if tor_process and tor_process.poll() is None:
                        tor_process.terminate()
                        print_status("Tor service stopped", "success")
                else:
                    print_status("Tor service still running - Use Task Manager to stop if needed", "info")
                
                print_status("Thank you for using PyTor!", "info")
                print(f"{Fore.YELLOW}{'═' * 70}{Style.RESET_ALL}\n")
                break
    else:
        print_box(f"Starting IP rotation\nTotal changes: {count}\nInterval: {interval} seconds", Fore.GREEN)
        print_separator()
        
        for i in range(count):
            print(f"\n{Fore.CYAN}Waiting {interval} seconds until next rotation...{Style.RESET_ALL}")
            for j in range(interval):
                time.sleep(1)
                remaining = interval - j - 1
                print(f"\r{Fore.YELLOW}  Next change in: {Fore.WHITE}{Style.BRIGHT}{remaining:3d}{Style.RESET_ALL}{Fore.YELLOW} seconds{Style.RESET_ALL}", end='')
            
            print(f"\n\n{Fore.CYAN}{Style.BRIGHT}═══ Rotation {i + 1}/{count} ═══{Style.RESET_ALL}")
            change_identity()
            print_separator()
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'═' * 70}{Style.RESET_ALL}")
        print_status(f"All {count} IP rotations completed successfully!", "success")
        
        keep_tor = input(f"\n{Fore.CYAN}Keep Tor running in background? (Y/N): {Style.RESET_ALL}").strip().upper()
        if keep_tor != 'Y':
            if tor_process and tor_process.poll() is None:
                tor_process.terminate()
                print_status("Tor service stopped", "success")
        else:
            print_status("Tor service still running - Use Task Manager to stop if needed", "info")
        
        print_status("Thank you for using PyTor!", "info")
        print(f"{Fore.GREEN}{Style.BRIGHT}{'═' * 70}{Style.RESET_ALL}\n")
        
except ValueError:
    print_status("Invalid input! Please enter valid numbers.", "error")
except Exception as e:
    print_status(f"Error: {e}", "error")
