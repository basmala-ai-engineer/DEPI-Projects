"""
Hospital Management System - Main Execution

This script provides a comprehensive CLI for managing different branches of a hospital.
It integrates both the Room Management System and the Staff Attendance System.

Dependencies:
    - 'Rooms.py' containing NormalRoom, ICURoom, and NurseryRoom.
    - 'staff.py' containing Staff, Doctor, Nurse, Receptionist, Engineer, and Manager.
"""

from Rooms import NormalRoom, ICURoom, NurseryRoom
from staff import Staff, Doctor, Nurse, Receptionist, Engineer, Manager

# ==========================================
# STAFF ATTENDANCE MANAGER
# ==========================================

class StaffManager:
    """
    Manages hospital staff attendance.
    Stores daily attendance records in a list and provides methods to log and view them.
    """
    def __init__(self):
        # The list that holds all attendance data throughout the program's lifecycle
        self.daily_attendance = []

    def staff_menu(self):
        """Displays the Staff Attendance sub-menu and handles user input."""
        while True:
            print("\n==================================")
            print("      STAFF ATTENDANCE SYSTEM     ")
            print("==================================")
            print("1. Log Staff Attendance (Assign Staff)")
            print("2. View Current Attendance List")
            print("3. Back to Main Menu")
            print("==================================")
            
            choice = input("Choose an option (1-3): ").strip()
            
            if choice == '1':
                self.log_attendance()
            elif choice == '2':
                self.view_attendance()
            elif choice == '3':
                print("Returning to Main Menu...")
                break
            else:
                print("\n[ERROR] Invalid choice. Please select 1, 2, or 3.\n")

    def attended(self, staff_member):
        """Extracts core details from a staff object and logs them."""
        record = {
            "id": staff_member.id,
            "name": staff_member.name,
            "position": staff_member.position
        }
        self.daily_attendance.append(record)
        print(f"\n[SUCCESS] Attendance recorded for {staff_member.name} ({staff_member.position}).\n")

    def log_attendance(self):
        """Prompts for staff details, instantiates the correct class, and logs attendance."""
        try:
            emp_id = int(input("\nEnter your ID (numeric): "))
            name = input("Enter your Name: ")
            position = input("Enter your Position (Doctor/Nurse/Receptionist/Engineer/Manager/Other): ").strip()
            
            position_lower = position.lower()
            
            if position_lower == "doctor":
                specialty = input("Enter your Specialty: ")
                staff_user = Doctor(emp_id, name, position, specialty)
                
            elif position_lower == "nurse":
                department = input("Enter your Department: ")
                staff_user = Nurse(emp_id, name, position, department)
                
            elif position_lower == "receptionist":
                shift = input("Enter your Shift (e.g., Morning/Night): ")
                staff_user = Receptionist(emp_id, name, position, shift)
                
            elif position_lower == "engineer":
                field = input("Enter your Field (e.g., maintenance, installation, sales): ")
                staff_user = Engineer(emp_id, name, position, field)
                
            elif position_lower == "manager":
                department = input("Enter your Department: ")
                staff_user = Manager(emp_id, name, position, department)
                
            else:
                staff_user = Staff(emp_id, name, position)

            self.attended(staff_user)
            
        except ValueError:
            print("\n[ERROR] Invalid ID format! Please enter a numeric ID.\n")

    def view_attendance(self):
        """Displays all logged records for the current session."""
        print("\n--- Today's Attendance Records ---")
        if not self.daily_attendance:
            print("No one has logged attendance yet.")
        else:
            for entry in self.daily_attendance:
                print(entry)
        print("----------------------------------\n")


# ==========================================
# ROOM MANAGER
# ==========================================

class RoomManager:
    """
    Manages all hospital rooms. 
    Stores room objects in a list and provides methods to interact with them.
    """
    def __init__(self):
        self.rooms = []

    def room_menu(self):
        while True:
            print("\n==================================")
            print("        ROOM MANAGEMENT SYSTEM    ")
            print("==================================")
            print("1. Add Normal Room")
            print("2. Add ICU Room")
            print("3. Add Nursery Room")
            print("4. View All Rooms")
            print("5. Assign Patient to Room")
            print("6. Release Patient from Room")
            print("7. Back to Main Menu")
            print("==================================")
            
            choice = input("Enter choice (1-7): ").strip()

            if choice == "1":
                self.add_normal_room()
            elif choice == "2":
                self.add_icu_room()
            elif choice == "3":
                self.add_nursery_room()
            elif choice == "4":
                self.view_all_rooms()
            elif choice == "5":
                self.assign_patient()
            elif choice == "6":
                self.release_patient()
            elif choice == "7":
                print("Returning to Main Menu...")
                break
            else:
                print("[ERROR] Invalid choice! Try again.")

    def _get_base_inputs(self):
        room_id = int(input("Enter Room ID (numeric): "))
        capacity = int(input("Enter Capacity (numeric): "))
        name = input("Enter Room Name: ")
        description = input("Enter Description: ")
        return room_id, capacity, name, description

    def add_normal_room(self):
        print("\n--- Add Normal Room ---")
        try:
            room_id, capacity, name, description = self._get_base_inputs()
            floor = int(input("Enter Floor Number: "))
            room = NormalRoom(room_id, capacity, "available", name, description, floor)
            self.rooms.append(room)
            print(f"[SUCCESS] Room '{name}' added! Total rooms in memory: {len(self.rooms)}")
        except ValueError:
            print("[ERROR] ID, Capacity, and Floor must be valid numbers!")

    def add_icu_room(self):
        print("\n--- Add ICU Room ---")
        try:
            room_id, capacity, name, description = self._get_base_inputs()
            equip_str = input("Enter Equipment (comma separated): ")
            equipment = [e.strip() for e in equip_str.split(",") if e.strip()]
            room = ICURoom(room_id, capacity, "available", name, description, equipment)
            self.rooms.append(room)
            print(f"[SUCCESS] ICU Room '{name}' added! Total rooms in memory: {len(self.rooms)}")
        except ValueError:
            print("[ERROR] ID and Capacity must be valid numbers!")

    def add_nursery_room(self):
        print("\n--- Add Nursery Room ---")
        try:
            room_id, capacity, name, description = self._get_base_inputs()
            incubators = int(input("Enter Incubator Count: "))
            room = NurseryRoom(room_id, capacity, "available", name, description, incubators)
            self.rooms.append(room)
            print(f"[SUCCESS] Nursery Room '{name}' added! Total rooms in memory: {len(self.rooms)}")
        except ValueError:
            print("[ERROR] ID, Capacity, and Incubators must be valid numbers!")

    def view_all_rooms(self):
        print("\n--- Displaying All Rooms ---")
        if not self.rooms:
            print("No rooms registered yet in the system.")
            return
        for index, room in enumerate(self.rooms, start=1):
            print(f"\n[Room #{index}]")
            room.display_room()
            print("-" * 30)

    def find_room_by_id(self, room_id):
        for room in self.rooms:
            if room.room_id == int(room_id):
                return room
        return None

    def assign_patient(self):
        print("\n--- Assign Patient ---")
        try:
            room_id = int(input("Enter Room ID: "))
            room = self.find_room_by_id(room_id)
            if room:
                patient_name = input("Enter Patient Name: ")
                room.assign_patient(patient_name)
            else:
                print(f"[ERROR] Room ID {room_id} not found!")
        except ValueError:
            print("[ERROR] Room ID must be a number!")

    def release_patient(self):
        print("\n--- Release Patient ---")
        try:
            room_id = int(input("Enter Room ID: "))
            room = self.find_room_by_id(room_id)
            if room:
                patient_name = input("Enter Patient Name: ")
                room.release_patient(patient_name)
            else:
                print(f"[ERROR] Room ID {room_id} not found!")
        except ValueError:
            print("[ERROR] Room ID must be a number!")


# ==========================================
# MAIN SYSTEM EXECUTION
# ==========================================

if __name__ == "__main__":
    # Initialize both managers outside the loop to persist data in memory
    global_room_manager = RoomManager()
    global_staff_manager = StaffManager()

    while True:
        print("\n==================================")
        print("    HOSPITAL MANAGEMENT SYSTEM    ")
        print("==================================")
        print("1. Add Department (Under Construction)")
        print("2. Add Patient (Under Construction)")
        print("3. View Departments (Under Construction)")
        print("4. View Patients (Under Construction)")
        print("5. Assign/Manage Staff Attendance")
        print("6. Manage Rooms")
        print("7. Exit")
        print("==================================")

        choice = input("Enter choice (1-7): ").strip()

        if choice == "5":
            # Pass control to the StaffManager instance
            global_staff_manager.staff_menu()

        elif choice == "6":
            # Pass control to the RoomManager instance
            global_room_manager.room_menu()
            
        elif choice == "7":
            print("Exiting System... Goodbye!")
            break
            
        elif choice in ["1", "2", "3", "4"]:
            print(f"\n[INFO] Option {choice} is selected (Feature coming soon).")
            
        else:
            print("[ERROR] Invalid choice! Please select a number from 1-7.")