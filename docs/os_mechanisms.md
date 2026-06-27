# OS Mechanisms and Technical Specifications
### **Component: Smart Registration & Check-In**
**Team B:** `Smart Registration & Check-In`

## Introduction
Our group is responsible for the digital check-in ecosystem of the Smart Fun Run. To ensure the system remains stable and data integrity is maintained when approximately 20 runners scan their tags simultaneously, we implemented core Operating System concepts within our concurrent Python backend.

---

# 1. Handling Concurrency (Multithreading in `server.py`)

## Overview

The Smart Fun Run backend receives participant check-in requests from multiple Android devices over a local Wi-Fi network. Since several runners may scan their QR/Profile IDs simultaneously, the server must process multiple requests at the same time without delaying other users.

To achieve this, the backend uses **multithreading**, allowing each incoming client connection to run in its own execution thread.

---

## Implementation

Whenever a participant's Profile ID is sent to the server:

1. The server accepts the client connection.
2. A new thread is created.
3. The thread independently processes the participant's request.
4. The main server immediately returns to listening for new connections.

This prevents one participant's request from blocking others.

### Example

```python
import socket
import threading

def handle_client(client_socket, address):
    data = client_socket.recv(1024).decode()
    print(f"[{address}] Received: {data}")

    # Process participant verification
    verify_participant(data)

    client_socket.send(b"Check-in Successful")
    client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5000))
server.listen()

print("Server is running...")

while True:
    client, addr = server.accept()

    # Create a new thread for each participant
    client_thread = threading.Thread(
        target=handle_client,
        args=(client, addr)
    )

    client_thread.start()
```

---

## How It Works

```
Android Device A ─┐
Android Device B ─┼──► Server Socket
Android Device C ─┘
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
 Thread 1         Thread 2        Thread 3
 Verify A         Verify B        Verify C
      │               │               │
      └───────────────┼───────────────┘
                      ▼
              Send Response
```

---

## Benefits

- Handles multiple participant check-ins simultaneously.
- Prevents the server from becoming blocked by a single request.
- Improves response time during peak event traffic.
- Ensures smooth real-time participant verification.
- Provides better scalability for large numbers of runners.

---

## Why Multithreading?

Without multithreading, the server would process requests one at a time. During busy periods, participants would experience delays while waiting for previous requests to finish.

With multithreading, every participant receives a dedicated execution thread, allowing the system to process many check-ins concurrently while maintaining fast response times.

---

## Files

| File | Responsibility |
|------|----------------|
| `server.py` | Creates the server socket and accepts client connections. |
| `handle_client()` | Processes participant verification for one client. |
| `threading.Thread` | Creates a new execution thread for each incoming request. |

---

## Summary

The Smart Fun Run backend uses Python's **threading** module to implement concurrency. Each participant connection is processed independently in its own thread, ensuring efficient multitasking, low response latency, and reliable real-time check-in even when many participants connect simultaneously.
## 2. Synchronization and Resource Locking Handle (Implemented in `server.py`)
Because multiple execution threads attempt to write to the shared **event registration logs on disk** simultaneously, there is a significant risk of **race conditions** or data corruption. 

*   **The Mutual Exclusion (Mutex) Lock:** We implemented a synchronization lock—referred to as **locking the "data lane"**—using Python’s synchronization primitives within `server.py`.
*   **The Critical Section:** This mechanism is overseen by our **Synchronization & Resource Locking Handler**. When a thread is ready to commit a check-in sequence to the log, it must first acquire the lock. This ensures that only one thread can access and write to the log file at any given moment.
*   **Result:** By enforcing this strict mutual exclusion, we guarantee that every participant's data is recorded safely and accurately, preventing the registration database from becoming corrupted during the live event.

---

## 3. File Management System
The backend is designed for high **data persistence** and reliability, managed by our **File Management Specialist**. The system specifically manages the storage of check-in data to ensure it is logged safely on the disk for post-event review.

---

## 4. System Monitoring and Fault Tolerance
Our core server logic includes several features to ensure system-wide stability:
*   **Identity Tracking:** The server observes the incoming data to verify successful transmissions from the mobile interface.
*   **Robustness:** By using synchronization locks and multithreading, the system is ruggedized to handle the "Micro-Run" environment where high-speed data entry is required.
