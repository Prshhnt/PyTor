import os
import sys
import shutil
import subprocess
import ctypes
import winreg
import zipfile
import tempfile
from pathlib import Path

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print('[+] Installing colorama...')
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'colorama'], check=True)
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

try:
    import requests
except ImportError:
    print('[+] Installing requests...')
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests'], check=True)
    import requests

# Constants
PYTOR_VERSION = "1.2"
TOR_DOWNLOAD_URL = "https://archive.torproject.org/tor-package-archive/torbrowser/13.5.7/tor-expert-bundle-windows-x86_64-13.5.7.tar.gz"

def is_admin():
    """Check if script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def print_header():
    """Print stylish installer header"""
    os.system("cls")
    print("\n")
    print(Fore.CYAN + Style.BRIGHT + "    ═══════════════════════════════════════════════════════════════════" + Style.RESET_ALL)
    print()
    print(Fore.YELLOW + Style.BRIGHT + """
              ██████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ 
              ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔═══██╗██╔══██╗
              ██████╔╝ ╚████╔╝    ██║   ██║   ██║██████╔╝
              ██╔═══╝   ╚██╔╝     ██║   ██║   ██║██╔══██╗
              ██║        ██║      ██║   ╚██████╔╝██║  ██║
              ╚═╝        ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    """ + Style.RESET_ALL)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}                     ⚙  INSTALLATION MANAGER  ⚙{Style.RESET_ALL}")
    print(f"{Fore.CYAN}                         Version {PYTOR_VERSION}{Style.RESET_ALL}")
    print()
    print(Fore.CYAN + Style.BRIGHT + "    ═══════════════════════════════════════════════════════════════════" + Style.RESET_ALL)
    print()

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

def print_status(message, status="info"):
    """Print formatted status messages"""
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
    
    print(f"{color}{Style.BRIGHT}  {icon} {message}{Style.RESET_ALL}")

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

def find_tor_windows():
    """Locate Tor executable on Windows system"""
    common_paths = [
        r"C:\Program Files\Tor Browser\Browser\TorBrowser\Tor\tor.exe",
        r"C:\Program Files (x86)\Tor Browser\Browser\TorBrowser\Tor\tor.exe",
        r"C:\Users\{}\AppData\Local\Tor Browser\Browser\TorBrowser\Tor\tor.exe".format(os.getenv('USERNAME')),
        r"C:\Tor\tor.exe",
        r"C:\Program Files\Tor\tor.exe",
        os.path.join(os.path.expanduser('~'), 'PyTor', 'tor', 'tor.exe')
    ]
    
    # Check if tor is in PATH
    tor_in_path = shutil.which('tor')
    if tor_in_path:
        return tor_in_path
    
    # Check common installation paths
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # Search in Downloads folder
    downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
    if os.path.exists(downloads):
        for root, dirs, files in os.walk(downloads):
            if 'tor.exe' in files and 'tor' in root.lower():
                return os.path.join(root, 'tor.exe')
    
    return None

def download_tor():
    """Download and extract Tor Expert Bundle"""
    print_status("Preparing to download Tor Expert Bundle...", "info")
    print(f"{Fore.YELLOW}Download URL: {TOR_DOWNLOAD_URL}{Style.RESET_ALL}")
    
    install_dir = os.path.join(os.path.expanduser('~'), 'PyTor', 'tor')
    os.makedirs(install_dir, exist_ok=True)
    
    temp_file = os.path.join(tempfile.gettempdir(), 'tor-expert-bundle.tar.gz')
    
    try:
        print_status("Downloading Tor Expert Bundle (this may take a few minutes)...", "info")
        response = requests.get(TOR_DOWNLOAD_URL, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        downloaded = 0
        
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        print_progress_bar(downloaded, total_size, prefix='Downloading:', suffix='Complete')
        
        print_status("Download completed successfully!", "success")
        
        # Extract the tar.gz file
        print_status("Extracting Tor files...", "info")
        import tarfile
        with tarfile.open(temp_file, 'r:gz') as tar:
            tar.extractall(install_dir)
        
        # Find tor.exe in extracted files
        tor_exe = None
        for root, dirs, files in os.walk(install_dir):
            if 'tor.exe' in files:
                tor_exe = os.path.join(root, 'tor.exe')
                break
        
        if tor_exe:
            print_status(f"Tor installed successfully at: {tor_exe}", "success")
            os.remove(temp_file)
            return tor_exe
        else:
            print_status("Tor executable not found in extracted files", "error")
            return None
            
    except Exception as e:
        print_status(f"Download failed: {e}", "error")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return None

def check_tor_installation():
    """Check for Tor installation and offer download if not found"""
    print_separator()
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Step 1: Checking Tor Installation{Style.RESET_ALL}\n")
    
    tor_path = find_tor_windows()
    
    if tor_path:
        print_status(f"Tor found at: {tor_path}", "success")
        return tor_path
    else:
        print_status("Tor not found on your system", "warning")
        print(f"{Fore.YELLOW}Tor is required for PyTor to function. You have several options:{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Options:{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}[1]{Style.RESET_ALL} Download Tor Expert Bundle automatically")
        print(f"  {Fore.YELLOW}[2]{Style.RESET_ALL} Provide path to existing tor.exe")
        print(f"  {Fore.YELLOW}[3]{Style.RESET_ALL} Open Tor Project website to download manually")
        print(f"  {Fore.YELLOW}[4]{Style.RESET_ALL} Skip Tor installation (not recommended)")
        
        choice = input(f"\n{Fore.CYAN}  → Select option [1-4]: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            tor_path = download_tor()
            if tor_path:
                return tor_path
            else:
                print_status("Automatic download failed. Please try manual installation.", "error")
                return None
                
        elif choice == "2":
            manual_path = input(f"\n{Fore.CYAN}  → Enter full path to tor.exe: {Style.RESET_ALL}").strip().strip('"')
            if os.path.exists(manual_path):
                print_status(f"Tor found at: {manual_path}", "success")
                return manual_path
            else:
                print_status("Invalid path. File not found.", "error")
                return None
                
        elif choice == "3":
            print_status("Opening Tor Project website...", "info")
            import webbrowser
            webbrowser.open("https://www.torproject.org/download/")
            print(f"{Fore.YELLOW}Please download Tor Browser or Tor Expert Bundle, then run this installer again.{Style.RESET_ALL}")
            return None
            
        else:
            print_status("Tor installation skipped", "warning")
            return None

def install_pytor():
    """Install PyTor script"""
    print_separator()
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Step 2: Installing PyTor{Style.RESET_ALL}\n")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pytor_script = os.path.join(current_dir, 'pytor.py')
    
    if not os.path.exists(pytor_script):
        print_status("pytor.py not found in current directory!", "error")
        return None
    
    try:
        install_dir = os.path.join(os.path.expanduser('~'), 'PyTor')
        os.makedirs(install_dir, exist_ok=True)
        
        # Copy pytor.py
        shutil.copy(pytor_script, os.path.join(install_dir, 'pytor.py'))
        print_status(f"Copied pytor.py to {install_dir}", "success")
        
        # Create batch file
        batch_content = f'@echo off\n"{sys.executable}" "{os.path.join(install_dir, "pytor.py")}" %*'
        batch_file = os.path.join(install_dir, 'pyt.bat')
        
        with open(batch_file, 'w') as f:
            f.write(batch_content)
        
        print_status("Created pyt.bat launcher", "success")
        
        return install_dir
        
    except Exception as e:
        print_status(f"Installation failed: {e}", "error")
        return None

def add_to_path(install_dir):
    """Add PyTor to system PATH"""
    print_separator()
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Step 3: PATH Configuration{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Adding PyTor to PATH allows you to run 'pyt' from any location in the command prompt.{Style.RESET_ALL}\n")
    
    add_path = input(f"{Fore.YELLOW}  → Add PyTor to PATH? (Y/N): {Style.RESET_ALL}").strip().upper()
    
    if add_path != 'Y':
        print_status("Skipped PATH configuration", "info")
        print(f"{Fore.YELLOW}To run PyTor, use: {os.path.join(install_dir, 'pyt.bat')}{Style.RESET_ALL}")
        return False
    
    try:
        # Check if already in PATH
        current_path = os.environ.get('PATH', '')
        if install_dir.lower() in current_path.lower():
            print_status("PyTor is already in PATH", "success")
            return True
        
        if not is_admin():
            print_status("Administrator privileges required to modify PATH", "warning")
            print(f"\n{Fore.YELLOW}Please choose an option:{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}[1]{Style.RESET_ALL} Restart installer as Administrator")
            print(f"  {Fore.YELLOW}[2]{Style.RESET_ALL} Add to PATH manually")
            print(f"  {Fore.YELLOW}[3]{Style.RESET_ALL} Skip PATH addition")
            
            choice = input(f"\n{Fore.CYAN}  → Select option [1-3]: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                print_status("Restarting with administrator privileges...", "info")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)
            elif choice == "2":
                print(f"\n{Fore.CYAN}To add PyTor to PATH manually:{Style.RESET_ALL}")
                print(f"  1. Press Win + X, select 'System'")
                print(f"  2. Click 'Advanced system settings'")
                print(f"  3. Click 'Environment Variables'")
                print(f"  4. Under 'User variables', select 'Path'")
                print(f"  5. Click 'Edit' then 'New'")
                print(f"  6. Add: {install_dir}")
                print(f"  7. Click 'OK' to save")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                return False
            else:
                return False
        
        # Add to user PATH (requires admin for system-wide)
        print_status("Adding to user PATH environment variable...", "info")
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_ALL_ACCESS)
        try:
            path_value, _ = winreg.QueryValueEx(key, 'Path')
        except FileNotFoundError:
            path_value = ''
        
        if install_dir not in path_value:
            new_path = path_value + ';' + install_dir if path_value else install_dir
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            print_status("Successfully added to PATH", "success")
            
            # Notify system of environment change
            try:
                import win32gui
                import win32con
                win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
            except:
                pass
            
            print_status("Please restart your terminal for changes to take effect", "warning")
        
        winreg.CloseKey(key)
        return True
        
    except Exception as e:
        print_status(f"Failed to add to PATH: {e}", "error")
        print(f"\n{Fore.YELLOW}To add manually:{Style.RESET_ALL}")
        print(f"  1. Open System Properties > Environment Variables")
        print(f"  2. Edit PATH variable")
        print(f"  3. Add: {install_dir}")
        return False

def uninstall_pytor():
    """Uninstall PyTor"""
    print_separator()
    print(f"\n{Fore.YELLOW}This will remove PyTor from your system. Tor installation will NOT be removed.{Style.RESET_ALL}\n")
    
    confirm = input(f"\n{Fore.RED}  → Are you sure you want to uninstall? (Y/N): {Style.RESET_ALL}").strip().upper()
    
    if confirm != 'Y':
        print_status("Uninstallation cancelled", "info")
        return
    
    install_dir = os.path.join(os.path.expanduser('~'), 'PyTor')
    
    try:
        if os.path.exists(install_dir):
            shutil.rmtree(install_dir)
            print_status(f"Removed: {install_dir}", "success")
        else:
            print_status("PyTor installation not found", "warning")
        
        # Try to remove from PATH
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_ALL_ACCESS)
            path_value, _ = winreg.QueryValueEx(key, 'Path')
            
            if install_dir in path_value:
                new_path = path_value.replace(';' + install_dir, '').replace(install_dir + ';', '').replace(install_dir, '')
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
                print_status("Removed from PATH", "success")
            
            winreg.CloseKey(key)
        except:
            print_status("Could not modify PATH (manual removal may be needed)", "warning")
        
        print(f"\n{Fore.GREEN}PyTor has been uninstalled successfully! Thank you for using PyTor.{Style.RESET_ALL}\n")
        
    except Exception as e:
        print_status(f"Uninstallation failed: {e}", "error")

def main():
    """Main installer function"""
    print_header()
    
    print(f"\n{Fore.CYAN}═══════════════════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}  Welcome to PyTor Installation Manager!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}═══════════════════════════════════════════════════════════════════{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}This installer will help you set up {Fore.GREEN}{Style.BRIGHT}PyTor{Style.RESET_ALL}{Fore.CYAN} and all required dependencies.{Style.RESET_ALL}\n")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}What would you like to do?{Style.RESET_ALL}\n")
    print(f"  {Fore.GREEN}[I]{Style.RESET_ALL} Install PyTor")
    print(f"  {Fore.RED}[U]{Style.RESET_ALL} Uninstall PyTor")
    print(f"  {Fore.YELLOW}[Q]{Style.RESET_ALL} Quit")
    
    choice = input(f"\n{Fore.CYAN}  → Select option: {Style.RESET_ALL}").strip().upper()
    
    if choice == 'U':
        uninstall_pytor()
        
    elif choice == 'I':
        # Check Tor
        tor_path = check_tor_installation()
        
        if not tor_path:
            print_status("Tor installation required. Please install Tor and run this installer again.", "error")
            return
        
        # Install PyTor
        install_dir = install_pytor()
        
        if not install_dir:
            print_status("PyTor installation failed", "error")
            return
        
        # Add to PATH
        add_to_path(install_dir)
        
        # Final summary
        print_separator("═")
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'═' * 70}")
        print(f"{'Installation Complete!':^70}")
        print(f"{'═' * 70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}{Style.BRIGHT}PyTor v{PYTOR_VERSION} is now installed!{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}To start using PyTor:{Style.RESET_ALL}")
        print(f"  1. Open a new terminal")
        print(f"  2. Run: {Fore.GREEN}pyt{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Or run directly:{Style.RESET_ALL}")
        print(f"  {os.path.join(install_dir, 'pyt.bat')}\n")
        
        print(f"\n{Fore.CYAN}Installed Components:{Style.RESET_ALL}")
        print_status(f"PyTor: {install_dir}", "success")
        print_status(f"Tor: {tor_path}", "success")
        
        print(f"\n{Fore.YELLOW}Note: If you added PyTor to PATH, restart your terminal!{Style.RESET_ALL}\n")
        
    else:
        print_status("Installation cancelled", "info")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Installation interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print_status(f"Unexpected error: {e}", "error")
    
    input(f"\n{Fore.CYAN}Press Enter to exit...{Style.RESET_ALL}")
