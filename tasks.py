import subprocess
import time


server_script = "server.py"
client_script = "client.py"
client_script_2 = "client2.py"

server_process = subprocess.Popen(["python", server_script])

time.sleep(2)  
client_process = subprocess.Popen(["python", client_script])

time.sleep(2)  
client_process_2= subprocess.Popen(["python", client_script_2])


client_process.wait()
client_process_2.wait()

while True:
    try:

        pass
    except KeyboardInterrupt:
       
        print("\nExiting...")
        break
