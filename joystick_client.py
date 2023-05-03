import socket
import argparse
import pyglet

# Configuration dictionary
joystick_config = {
    "VIRPIL Controls 20220720 R-VPC Stick MT-50CM2": {
        18: "f3",  # Map button 18 to the key "f3"
    },
    "VIRPIL Controls 20220208 VPC Throttle MT-50CM3": {
        666: "alt+f4",
    },
    "VIRPIL Controls 20230328 L-VPC Stick MT-50CM2": {
        18: "alt+f4",
    }
}

HOST, PORT = "secus.local", 5005

joysticks = pyglet.input.get_joysticks()
if not joysticks:
    print("No joysticks found")
    exit(1)

# Set up the connection to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


def list_joysticks():
    print("Connected Joysticks:")
    for i, joystick in enumerate(joysticks):
        print(f"{i}: {joystick.device.name}")

def on_joybutton_press(joystick, button):
    joystick_name = joystick.device.name
    if joystick_name in joystick_config and button in joystick_config[joystick_name]:
        key_to_send = joystick_config[joystick_name][button]
        print(f"Sending key '{key_to_send}' for joystick '{joystick_name}' button {button}")

        # Send the key to the server
        try:
            s.sendall(key_to_send.encode('utf-8'))
        except BrokenPipeError as e:
            print("Error sending data to the server:", e)

def main():
    parser = argparse.ArgumentParser(description="Joystick button press detector")
    parser.add_argument("--list", dest="list_joysticks", action="store_true",
                        help="List all connected joysticks and exit")

    args = parser.parse_args()

    if args.list_joysticks:
        list_joysticks()
        return

    for temp_joystick in joysticks:
        if temp_joystick.device.name in joystick_config:
            temp_joystick.open()
            temp_joystick.push_handlers(on_joybutton_press)

    print("Monitoring joysticks for button presses...")

    pyglet.app.run()
    s.close()


if __name__ == '__main__':
    main()
