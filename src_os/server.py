# server.py
import socket
import threading
import json
from database_handler import initialize_database, process_check_in

# Server Configuration
HOST = "0.0.0.0"  # "0.0.0.0" allows listening to any device on the local network
PORT = 8080       # The communication port matching your MIT App configuration

def client_worker_thread(client_socket, client_address):
    """
    OS CONCEPT: Worker thread function designed to handle a single 
    incoming network connection request independently.
    """
    print(f"[CONCURRENCY] Launched background thread: {threading.current_thread().name} for {client_address}")
    
    try:
        # Receive the transmission data sent by the MIT App (up to 2048 bytes)
        request = client_socket.recv(2048).decode("utf-8")
        
        if not request:
            return

        print(f"[NETWORK] Received Raw Data:\n{request}")
        
        # Parse the HTTP Request Body (MIT App Inventor Web component transmits via POST/GET)
        # We look for the JSON payload at the end of the HTTP request header
        if "{" in request:
            json_payload_str = request[request.find("{"):]
            data = json.loads(json_payload_str)
            
            # Extract keys matching the src_iot/payload_format.json standard
            runner_id = data.get("runner_id", "UNKNOWN")
            timestamp = data.get("timestamp", "N/A")
            booth_id = data.get("booth_id", "UNKNOWN_BOOTH")
            
            # Forward data out to the safe synchronization lock handler
            status_reply = process_check_in(runner_id, timestamp, booth_id)
        else:
            status_reply = "ERROR: Invalid HTTP/JSON data payload packet received"

        # Construct a standardized clean HTTP response back to the MIT App Inventor front-end
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            "Access-Control-Allow-Origin: *\r\n" # Solves CORS blocking issues
            f"Content-Length: {len(status_reply)}\r\n"
            "\r\n"
            f"{status_reply}"
        )
        client_socket.sendall(http_response.encode("utf-8"))
        
    except Exception as e:
        print(f"[ERROR] Thread malfunction encountered: {e}")
    finally:
        # Cleanly shut down communication channels for this thread
        client_socket.close()
        print(f"[CONCURRENCY] Thread {threading.current_thread().name} terminated cleanly.")

def main():
    print("=== SMART FUN RUN: CENTRAL BACKEND ENGINE (REGISTRATION) ===")
    initialize_database()
    
    # Establish standard IPv4 TCP Streaming Sockets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow instant socket reuse to bypass OS timeout locks during debugging reboots
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((HOST, PORT))
    server_socket.listen(10) # Socket back-log queue set to hold up to 10 waiting connections
    
    # Find your local network IP to easily type it into your MIT App
    local_ip = socket.gethostbyname(socket.gethostname())
    print(f"[SERVER STARTED] Listening actively on Port: {PORT}")
    print(f"[NETWORK INFO] Tell your MIT App to send Web requests to: http://{local_ip}:{PORT}")
    print("Awaiting scan signals from MIT App Inventor devices...\n")
    
    thread_counter = 1
    while True:
        try:
            # Accept a connection from an active phone on the network
            client_sock, client_addr = server_socket.accept()
            
            # OS CONCEPT: Dynamic Multi-threading Creation
            # Instead of handling it on the main execution line, assign a new background thread.
            worker = threading.Thread(
                target=client_worker_thread, 
                args=(client_sock, client_addr),
                name=f"CheckInWorker-{thread_counter}"
            )
            thread_counter += 1
            
            # Fire up the background thread execution path
            worker.start()
            
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Terminating server operations dynamically.")
            break
            
    server_socket.close()

if __name__ == "__main__":
    main()
