import socket
import threading
import tkinter as tk

def receive_messages(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Received message from {addr}: {message}")
                update_server_chat(f"Client {addr}: {message}")
                broadcast(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except ConnectionResetError:
            remove_client(client_socket)
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        update_clients_list()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 12345))

    s.listen(5)
    print("Server is listening...")

    while True:
        client_socket, addr = s.accept()
        print(f"Connection established with {addr}")
        update_server_chat(f"Connection established with {addr}")
        clients.append(client_socket)
        update_clients_list()
        client_thread = threading.Thread(target=receive_messages, args=(client_socket, addr))
        client_thread.start()

def send_message():
    selected_client_index = clients_listbox.curselection()
    message = server_message.get()
    server_message.set("")

    if selected_client_index:  # Send to selected client
        selected_client_socket = clients[selected_client_index[0]]
        selected_client_socket.send(("Server: " + message).encode())
        update_server_chat(f"Server: {message} to Client {selected_client_index[0] + 1}")
    else:  # Broadcast to all clients
        broadcast("Server: " + message, None)
        update_server_chat("Server: " + message + " to all clients")

def update_server_chat(message):
    server_chat.config(state=tk.NORMAL)
    server_chat.insert(tk.END, message + '\n')
    server_chat.config(state=tk.DISABLED)

def update_clients_list():
    clients_listbox.delete(0, tk.END)
    for index, client in enumerate(clients):
        clients_listbox.insert(tk.END, f"Client {index + 1}")

clients = []

server_ui = tk.Tk()
server_ui.title("Server UI")


input_frame = tk.Frame(server_ui)
input_frame.pack(pady=10)

server_message = tk.StringVar()
message_entry = tk.Entry(input_frame, textvariable=server_message, width=30)
message_entry.pack(side=tk.LEFT, padx=5)

send_button = tk.Button(input_frame, text="Send to Selected Client", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

send_all_button = tk.Button(input_frame, text="Send to All Clients", command=send_message)
send_all_button.pack(side=tk.LEFT, padx=5)


clients_frame = tk.Frame(server_ui)
clients_frame.pack()

clients_label = tk.Label(clients_frame, text="Connected Clients:")
clients_label.pack()

clients_listbox = tk.Listbox(clients_frame, height=5, width=30)
clients_listbox.pack(padx=10, pady=5)

chat_frame = tk.Frame(server_ui)
chat_frame.pack()

server_chat = tk.Text(chat_frame, height=15, width=50, state=tk.DISABLED)
server_chat.pack(padx=10, pady=10)

server_thread = threading.Thread(target=start_server)
server_thread.start()

server_ui.mainloop()
