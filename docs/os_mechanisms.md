# OS Mechanisms and Technical Specifications
### **Component: Smart Registration & Check-In**
**Team B:** `Smart Registration & Check-In`

## Introduction
Our group is responsible for the digital check-in ecosystem of the Smart Fun Run. To ensure the system remains stable and data integrity is maintained when approximately 20 runners scan their tags simultaneously, we implemented core Operating System concepts within our concurrent Python backend.

---

## 1. Handling Concurrency (Multithreading in `server.py`)
For the Smart Fun Run, the backend must process high volumes of participant data sent from the Android mobile interface via the local Wi-Fi network. To prevent the server from becoming a bottleneck, we utilized a **multithreaded architecture**.

*   **Implementation:** Every time a participant's unique profile ID is scanned and transmitted to the server, the OS backend in `src_os/server.py` creates a **new execution thread** to handle the request. This allows the server to handle incoming connections dynamically and remain non-blocking.
*   **Role Responsibilities:** Managed by our **Concurrency Specialist**, the code ensures that the OS manages multitasking efficiently, allowing for real-time verification of scanned codes in the server terminal.
*   **Purpose:** This multithreading approach is essential for handling the peak load of multiple runners checking in at the exact same time without system lag or failure.

---

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
