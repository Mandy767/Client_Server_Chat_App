import socket
import threading
import tkinter as tk

ADDRESS = '127.0.0.1'
PORT = 12345

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                if message.startswith('Server:'):
                    chat_window.insert(tk.END, message + '\n')
                    chat_window.see(tk.END)
        except ConnectionResetError:
            break

def send_message(event=None):
    message = my_message.get()
    if message:
        my_message.set("")
        chat_window.insert(tk.END, f"client2: {message}\n")
        chat_window.see(tk.END)  
        client_socket.send(message.encode())

def start_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ADDRESS, PORT))

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()


root = tk.Tk()
root.title(f"Client2")


chat_window = tk.Text(root, height=20, width=50)
chat_window.pack(padx=10, pady=10)

my_message = tk.StringVar()
message_entry = tk.Entry(root, textvariable=my_message, width=40)
message_entry.bind("<Return>", send_message)
message_entry.pack(padx=10, pady=5)


send_button = tk.Button(root, text="Send", width=10, command=send_message)
send_button.pack(padx=10, pady=5)

start_client()


root.mainloop()
