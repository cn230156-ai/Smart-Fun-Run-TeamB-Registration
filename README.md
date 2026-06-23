# Team B: Smart Registration & Check-In

## 1. Project Title & Component Name
* **Project:** The Smart Fun Run Project 
* **Component:** Smart Registration & Check-In (Team B) 

## 2. Team Members & Roles
* **MUHAMMAD AIDID BIN IBRAHIM (AN230016):** IoT & OS Student — Lead Engineer & OS Developer 
* **INSYIRA BINTI ISMAIL (AN230041):** IoT & OS Student — Hardware Configuration & OS Developer 
* **MUHAIMIN ASYRAF BIN MUSRIN (CN230156):** OS Student — Backend Systems Architect 
* **MUHAMMAD RAZIQ AZFAR BIN SHAMSUL AZMAN (CN240249):** OS Student — Concurrency Specialist 
* **AHMAD HAKIMI BIN AHMAD SHUKRI (CN240326):** OS Student — Synchronization & Resource Locking Handler 
* **EMYLIA AININ SOFIA BINTI MOHAMAD LOZI (CN240289):** OS Student — File Management & Data Persistence Specialist 
* **HAZWANI BINTI MOHD THARMIZI (CN240315):** OS Student — Technical Documenter & QA Tester 

## 3. Component Overview
Our system delivers a seamless digital check-in ecosystem using an Android application interface built via MIT App Inventor. 
When a participant arrives at the registration booth, the app scans their unique profile identification. The mobile interface translates this data into a standardized JSON payload and transmits it wirelessly across the local Wi-Fi network to our concurrent Python backend server. The backend handles incoming connections dynamically using multithreading, running them through mutual exclusion synchronization locks to safely update the event registration logs on disk without race conditions or database corruption.

## 4. Quick Start Guide
To deploy and initialize the system components, execute these steps:
1. **Host Setup:** Navigate to your terminal on the server machine, move into the backend repository, and change directory into the OS workspace: `cd src_os`
2. **Launch Server:** Boot up the Python engine by running: `python server.py`. Note the local network IP printed by the script.
3. **App Linkage:** Ensure the Android testing smartphone and the server machine are paired to the same local Wi-Fi router network. Open the MIT App Inventor program or compiled app, and update its Target Web URL configuration property to match the server IP and port (e.g., `http://<YOUR_LOCAL_IP>:8080`).
4. **Active Verification:** Scan a test participant code via the mobile application. Observe the backend python server terminal window to verify that it successfully creates a new execution thread, locks the data lane, and commits the check-in logging sequence safely.
