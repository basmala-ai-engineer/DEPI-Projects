from department import Department
class Hospital:
    """Class for managing hospital operations."""
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.departments = []
        
    def add_department(self, department):
        """Add a department to the hospital."""
        self.departments.append(department)
        print(f"Department '{department.name}' added to {self.name}.")
        
    def display_hospital_info(self):
        """Display hospital information."""
        print(f"Hospital Name: {self.name}, Location: {self.location}")
        if not self.departments:
            print("No departments available.")
        for dept in self.departments:
            print(f"- Department: {dept.name}")
            
    def hospital_menu(self):
        """Display the hospital management menu."""
        print("=== Hospital Setup Interface ===")
        h_name = input("Enter Hospital Name: ")
        h_location = input("Enter Hospital Location: ")
        
        my_hospital = Hospital(h_name, h_location)
        while True:
            print("\n" + "="*30)
            print(f"--- {my_hospital.name} Menu ---")
            print("1. Add New Department")
            print("2. View Hospital Details")
            print("3. Exit")
            choice = input("Select an option (1-3): ")
            if choice == "1":
                dept_name = input("Enter Department Name: ")
                new_dept = Department(dept_name)
                my_hospital.add_department(new_dept)
            elif choice == "2":
                my_hospital.display_hospital_info()
            elif choice == "3":
                print("Exiting the Hospital Setup Interface.")
                break
            else:
                print("Invalid choice! Please select a valid option (1-3).")
if __name__ == "__main__":
    hospital = Hospital("City Hospital", "Downtown")
    hospital.hospital_menu()