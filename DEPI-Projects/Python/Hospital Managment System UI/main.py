"""
Hospital Management System - Main Execution

This script provides a comprehensive CLI for managing different branches of a hospital.
It integrates both the Room Management System and the Staff Attendance System.

Dependencies:
    - 'Rooms.py' containing NormalRoom, ICURoom, and NurseryRoom.
    - 'staff.py' containing Staff, Doctor, Nurse, Receptionist, Engineer, and Manager.
"""
from hospital import Hospital
from department import Department
from patient import Patient
from staff import Staff, Doctor, Nurse, Receptionist, Engineer, Manager
from appointment import Appointment
from Rooms import NormalRoom, ICURoom, NurseryRoom

def main():
    hospital_name = input("Enter Hospital Name: ")
    hospital_location = input("Enter Hospital Location: ")
    my_hospital = Hospital(hospital_name, hospital_location)
    
    while True:
        print("\n==================================")
        print("    HOSPITAL MANAGEMENT SYSTEM    ")
        print("==================================")
        print("1. Add Department")
        print("2. Add Room to Department")
        print("3. Add Staff to Department")
        print("4. Add Patient to Department")
        print("5. Schedule Appointment")
        print("6. View Hospital Details")
        print("7. Exit")
        
        choice = input("Select an option (1-7): ")
        
        if choice == '1':
            dept_name = input("Enter Department Name: ")
            new_dept = Department(dept_name)
            my_hospital.add_department(new_dept)
            print(f"Department '{dept_name}' added successfully.")
            
        elif choice == '2':
            if not my_hospital.departments:
                print("No departments available. Please add a department first.")
                continue
            
            print("Available Departments:")
            for i, dept in enumerate(my_hospital.departments):
                print(f"{i}. {dept.name}")
                
            dept_choice = int(input("Select a department by number: ")) 
            if 0 <= dept_choice < len(my_hospital.departments):
                selected_dept = my_hospital.departments[dept_choice]
                
                room_type = input("Enter Room Type (Normal/ICU/Nursery): ").strip().lower()
                room_id = int(input("Enter Room ID: "))
                capacity = int(input("Enter Room Capacity: "))
                name = input("Enter Room Name: ")
                description = input("Enter Room Description: ")
                
                if room_type == "normal":
                    floor = int(input("Enter Floor Number: "))
                    room = NormalRoom(room_id, capacity, "available", name, description, floor)
                elif room_type == "icu":
                    equipment = input("Enter Equipment (comma separated): ").split(',')
                    room = ICURoom(room_id, capacity, "available", name, description, [e.strip() for e in equipment])
                elif room_type == "nursery":
                    incubators = int(input("Enter Incubator Count: "))
                    room = NurseryRoom(room_id, capacity, "available", name, description, incubators)
                else:
                    print("Invalid room type. Please try again.")
                    continue
                
                selected_dept.add_room(room)
                print(f"Room '{name}' added to department '{selected_dept.name}'.")
            else:
                print("Invalid department selection.")
                
        elif choice == '3':
            if not my_hospital.departments:
                print("No departments available. Please add a department first.")
                continue
            
            print("Available Departments:")
            for i, dept in enumerate(my_hospital.departments):
                print(f"{i}. {dept.name}")
                
            dept_choice = int(input("Select a department by number: ")) 
            if 0 <= dept_choice < len(my_hospital.departments):
                selected_dept = my_hospital.departments[dept_choice]
                
                emp_id = int(input("Enter Staff ID: "))
                name = input("Enter Staff Name: ")
                position = input("Enter Staff Position (Doctor/Nurse/Receptionist/Engineer/Manager): ").strip()
                
                if position.lower() == "doctor":
                    specialty = input("Enter Specialty: ")
                    staff_member = Doctor(emp_id, name, position, specialty)
                elif position.lower() == "nurse":
                    department = input("Enter Department: ")
                    staff_member = Nurse(emp_id, name, position, department)
                elif position.lower() == "receptionist":
                    shift = input("Enter Shift (e.g., Morning/Night): ")
                    staff_member = Receptionist(emp_id, name, position, shift)
                elif position.lower() == "engineer":
                    field = input("Enter Field (e.g., maintenance, installation, sales): ")
                    staff_member = Engineer(emp_id, name, position, field)
                elif position.lower() == "manager":
                    department = input("Enter Department: ")
                    staff_member = Manager(emp_id, name, position, department)
                else:
                    staff_member = Staff(emp_id, name, position)
                
                selected_dept.add_staff(staff_member)
                print(f"Staff '{name}' added to department '{selected_dept.name}'.")
            else:
                print("Invalid department selection.")
                
        elif choice == '4':
            if not my_hospital.departments:
                print("No departments available. Please add a department first.")
                continue
            
            print("Available Departments:")
            for i, dept in enumerate(my_hospital.departments):
                print(f"{i}. {dept.name}")
                
            dept_choice = int(input("Select a department by number: ")) 
            if 0 <= dept_choice < len(my_hospital.departments):
                selected_dept = my_hospital.departments[dept_choice]
                
                name = input("Enter Patient Name: ")
                age = int(input("Enter Patient Age: "))
                patient_id = input("Enter Patient ID: ")
                medical_record = input("Enter Medical Record Details: ")
                
                patient = Patient(name, age, patient_id, medical_record)
                selected_dept.add_patient(patient)
                print(f"Patient '{name}' added to department '{selected_dept.name}'.")
            else:
                print("Invalid department selection.")
                
        elif choice == '5':
            if not my_hospital.departments:
                print("No departments available. Please add a department first.")
                continue
            
            print("Available Departments:")
            for i, dept in enumerate(my_hospital.departments):
                print(f"{i}. {dept.name}")
                
            dept_choice = int(input("Select a department by number: ")) 
            if 0 <= dept_choice < len(my_hospital.departments):
                selected_dept = my_hospital.departments[dept_choice]
                
                if not selected_dept.patients or not selected_dept.staff:
                    print("Both patients and staff must be present in the department to schedule an appointment.")
                    continue
                
                print("Available Patients:")
                for i, patient in enumerate(selected_dept.patients):
                    print(f"{i}. {patient.name}")
                    
                patient_choice = int(input("Select a patient by number: ")) 
                if 0 <= patient_choice < len(selected_dept.patients):
                    selected_patient = selected_dept.patients[patient_choice]
                    
                    print("Available Staff:")
                    for i, staff_member in enumerate(selected_dept.staff):
                        print(f"{i}. {staff_member.name} ({staff_member.position})")
                        
                    staff_choice = int(input("Select a staff member by number: ")) 
                    if 0 <= staff_choice < len(selected_dept.staff):
                        selected_staff = selected_dept.staff[staff_choice]
                        
                        date = input("Enter Appointment Date (YYYY-MM-DD): ")
                        time = input("Enter Appointment Time (HH:MM): ")
                        appointment = Appointment(selected_patient, selected_staff, date, time)
                        selected_dept.add_appointment(appointment)
                        print(f"Appointment scheduled for patient '{selected_patient.name}' with staff '{selected_staff.name}' on {date} at {time}.")
                    else:
                        print("Invalid staff selection.")
                else:
                    print("Invalid patient selection.")
            else:
                print("Invalid department selection.")
                
        elif choice == '6':
            my_hospital.display_hospital_info()
            
        elif choice == '7':
            print("Exiting the Hospital Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option (1-7).")
            
if __name__ == "__main__":
    main()