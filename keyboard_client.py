import socket
import keyboard

def main():
    host = 'secus.local'  # Server IP address
    port =  5005          # Server port number

    acceptable_keybindings = ['f3'] # add your keybinding, for instance: `alt+f4`

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    def on_key_press(e):
        key = e.name
        if key in acceptable_keybindings:
            print("Sending Key to server: {}".format(key))
            s.sendall(key.encode('utf-8'))

    print("Client monitoring for keybinding...")
    keyboard.on_press(on_key_press)

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("Client stopped")

    s.close()

if __name__ == '__main__':
    main()
