import pyautogui
import socketserver
import threading

HOST, PORT = "0.0.0.0", 5005

acceptable_keybindings = ['f3'] # add your keybinding, for instance: `alt+f4`

def press_key(keybinding):
    keys = keybinding.split('+')
    pyautogui.hotkey(*keys)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024)
            if data:
                key = data.decode('utf-8')
                if key in acceptable_keybindings:
                    print("Received key press: {}".format(key))
                    press_key(key)
            else:
                break

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print(f"Server started on {HOST}:{PORT}")

    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
        server.server_close()
