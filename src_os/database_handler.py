 # database_handler.py
import threading
import os
import time

# OS CONCEPT: Initialize a Mutual Exclusion (Mutex) Lock
# This ensures only ONE thread can write to the registration log file at a time.
db_lock = threading.Lock()

REG_FILE = "registration_database.txt"

def initialize_database():
    """Creates a sample database file with mock runners if it doesn't exist."""
    if not os.path.exists(REG_FILE):
        with open(REG_FILE, "w") as f:
            f.write("RUNNER_ID,TIMESTAMP,STATUS,BOOTH_ID\n")
            f.write("RUN-2026-001,0,REGISTERED,NONE\n")
            f.write("RUN-2026-002,0,REGISTERED,NONE\n")
            f.write("RUN-2026-003,0,REGISTERED,NONE\n")
        print(f"[OS FILE MANAGEMENT] Initialized persistent registry tracker: {REG_FILE}")

def process_check_in(runner_id, scan_time, booth_id):
    """
    Critical Section: Reads and updates the runner status safely using Mutex Locks.
    """
    # OS CONCEPT: Acquire the Mutex Lock before entering the Critical Section
    db_lock.acquire()
    
    try:
        print(f"\n[LOCK ACQUIRED] Thread {threading.current_thread().name} is processing {runner_id}...")
        
        # Simulate a slight processing lag (Reading from Disk/I/O operation)
        time.sleep(0.5) 
        
        # Read the file contents
        if not os.path.exists(REG_FILE):
            return "ERROR: Database file missing"
            
        with open(REG_FILE, "r") as f:
            lines = f.readlines()
            
        updated = False
        already_checked_in = False
        new_lines = [lines[0]] # Keep the CSV header
        
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) < 4:
                continue
                
            curr_id, curr_time, curr_status, curr_booth = parts[0], parts[1], parts[2], parts[3]
            
            if curr_id == runner_id:
                if curr_status == "CHECKED_IN":
                    already_checked_in = True
                    new_lines.append(line)
                else:
                    # OS CONCEPT: Atomically update state inside the locked critical section
                    new_lines.append(f"{runner_id},{scan_time},CHECKED_IN,{booth_id}\n")
                    updated = True
            else:
                new_lines.append(line)
                
        if already_checked_in:
            print(f"[RACE CONDITION PREVENTED] {runner_id} rejected! Already checked in at booth: {curr_booth}")
            return f"REJECTED: Already checked in at {curr_booth}"
            
        if updated:
            # Save the updated lines back to the file
            with open(REG_FILE, "w") as f:
                f.writelines(new_lines)
            print(f"[OS FILE MANAGEMENT] Successfully committed status shift for {runner_id} to disk.")
            return "SUCCESS: Check-In Approved"
        else:
            # If runner isn't in the system, append them as a new walk-in registration
            with open(REG_FILE, "a") as f:
                f.write(f"{runner_id},{scan_time},CHECKED_IN,{booth_id}\n")
            print(f"[OS FILE MANAGEMENT] New runner {runner_id} registered and checked in successfully.")
            return "SUCCESS: Walk-in Registration Approved"
            
    finally:
        # OS CONCEPT: CRUCIAL - Always release the lock to prevent deadlocks!
        db_lock.release()
        print(f"[LOCK RELEASED] Thread {threading.current_thread().name} freed the database.")
