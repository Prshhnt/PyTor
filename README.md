# PyTor v1.2

🔄 **Automatic IP rotation through Tor network**

> Inspired by [Auto_Tor_IP_changer](https://github.com/FDX100/Auto_Tor_IP_changer)

## ✨ Features

- 🔍 **Automatic Tor detection** - Finds your Tor installation
- 🎯 **Easy installation** - Interactive installer with PATH setup
- ⚡ **Configurable intervals** - Set custom rotation times
- 🔄 **Infinite or limited** - Choose number of IP changes
- 📊 **Real-time display** - See your current IP and progress
- 🎨 **Modern UI** - Clean, colorful terminal interface

## 📋 Requirements

- Python 3.x
- Tor (auto-downloadable via installer)

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Prshhnt/PyTor.git
cd PyTor
python install.py
```

The installer will:
- Check for Tor (or download it automatically)
- Install PyTor to your system
- Optionally add to PATH

### Running

```bash
pyt
```

Or directly:
```bash
python pytor.py
```

## 🌐 Browser Configuration

Configure your browser to use SOCKS5 proxy:
- **Host:** `127.0.0.1`
- **Port:** `9050`

**Firefox:** Settings → Network Settings → Manual proxy configuration  
**Chrome:** Use [Proxy SwitchyOmega](https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif) extension

## 💡 Usage

1. Run `pyt` or `python pytor.py`
2. Set rotation interval (seconds)
3. Set number of changes (0 = infinite)
4. Configure your browser proxy
5. Browse with automatic IP rotation

**Stop:** Press `Ctrl+C`

## 🔧 Configuration

PyTor creates its configuration at: `~/.pytor_data/torrc`

## ✅ Verify Connection

Visit [check.torproject.org](https://check.torproject.org) to verify your Tor connection.

## 🗑️ Uninstall

```bash
python install.py
```
Select uninstall option and follow prompts.

## 📝 Notes

- First connection may take 10-30 seconds
- Tor runs in background
- Currently supports Windows (Linux/Mac support coming soon)

## 👨‍💻 Author

**prshhnt**  
GitHub: [github.com/Prshhnt](https://github.com/Prshhnt)

## 📄 License

Open source - Free to use

---

⭐ Star this repo if you find it helpful!
