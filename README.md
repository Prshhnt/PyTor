# PyTor 🔄

**Automatic IP rotation through the Tor network**

> Inspired by [Auto_Tor_IP_changer](https://github.com/FDX100/Auto_Tor_IP_changer)

## Overview

PyTor is a Python-based tool that automates IP address rotation using the Tor network. It provides a clean command-line interface for configuring and managing automatic IP changes at custom intervals.

## ✨ Features

- **Automatic Tor Detection** - Locates existing Tor installations or downloads Tor Expert Bundle
- **Configurable Rotation** - Set custom time intervals between IP changes
- **Flexible Operation** - Run infinite rotations or specify exact number of changes
- **Real-time Monitoring** - Display current IP address and rotation status
- **Interactive Installer** - Guided setup with optional PATH integration
- **Clean Interface** - Professional terminal UI with color-coded status messages

## 📋 Requirements

- Python 3.7 or higher
- Tor (can be auto-downloaded via installer)
- Windows (Linux/macOS support planned)

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/Prshhnt/PyTor.git
cd PyTor
```

### Run Installer

```bash
python install.py
```

The installer will:
- Detect or download Tor Expert Bundle
- Install required Python dependencies
- Configure PyTor for your system
- Optionally add PyTor to system PATH

### Manual Installation

```bash
pip install -r requirements.txt
```

## 💻 Usage

### Basic Usage

```bash
python pytor.py
```

Or if added to PATH:

```bash
pyt
```

### Configuration Prompts

1. **Rotation Interval** - Specify time in seconds between IP changes (default: 60)
2. **Number of Changes** - Enter count or 0 for infinite rotation
3. **Tor Control** - Choose whether to keep Tor running on exit

### Browser Configuration

Configure your browser to route traffic through Tor:

**SOCKS5 Proxy Settings:**
- Host: `127.0.0.1`
- Port: `9050`

**Firefox:**  
Settings → Network Settings → Manual proxy configuration → SOCKS5: 127.0.0.1:9050

**Chrome/Edge:**  
Install [Proxy SwitchyOmega](https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif) extension and configure SOCKS5 proxy

## 🔧 Technical Details

### How It Works

1. PyTor starts a local Tor daemon with control port enabled
2. Establishes SOCKS5 proxy on port 9050
3. Sends NEWNYM signals to Tor control port (9051) to request new circuits
4. Verifies IP changes through external IP checking service

### Configuration Files

- **Tor Config:** `~/.pytor_data/torrc` (auto-generated)
- **Tor Data:** `~/.pytor_data/` (Tor state and circuit information)

### Dependencies

- `requests` - HTTP requests through SOCKS proxy
- `requests[socks]` - SOCKS5 proxy support
- `colorama` - Cross-platform colored terminal output

## Verification

Verify your Tor connection:
- Visit [check.torproject.org](https://check.torproject.org)
- Check IP: [icanhazip.com](https://icanhazip.com)

## ⚠️ Troubleshooting

**Connection Issues:**
- Ensure ports 9050 and 9051 are available
- Check firewall settings allow Tor connections
- First connection may take up to 30 seconds for circuit establishment

**Tor Not Found:**
- Run `python install.py` to download Tor Expert Bundle
- Manually specify Tor path when prompted

**Permission Errors:**
- PATH modification requires administrator privileges
- Run installer as administrator for system-wide installation

## 🗑️ Uninstallation

```bash
python install.py
```

Select the uninstall option and follow the prompts to remove PyTor from your system.

## 👨‍💻 Development

### Project Structure

```
PyTor/
├── pytor.py          # Main application
├── install.py        # Interactive installer
├── requirements.txt  # Python dependencies
└── README.md         # Documentation
```

### Contributing

Contributions are welcome. Please ensure code follows existing style and includes appropriate documentation.

## 📄 License

This project is open source and available for free use.

## 👤 Author

**prshhnt**  
GitHub: [@Prshhnt](https://github.com/Prshhnt)

## Acknowledgments

Inspired by [Auto_Tor_IP_changer](https://github.com/FDX100/Auto_Tor_IP_changer) by FDX100

---

**Version:** 1.2  
**Status:** Active Development
