class Department:
    

    def __init__(self, name):
        self.name = name
        self.patients = []   
        self.staff = []      
        self.appointments = [] 
        self.rooms = [] 

    def add_patient(self, patient):
        """Add a patient to the department."""
        self.patients.append(patient)
        print(f"Patient '{patient.name}' added to {self.name} department.")

    def add_staff(self, staff_member):
        """Add staff member to the department."""
        self.staff.append(staff_member)
        print(f"Staff '{staff_member.name}' added to {self.name} department.")

    def add_appointment(self, appointment):
       
        self.appointments.append(appointment)
        print(f"Appointment scheduled in {self.name} department: "
              f"{appointment.patient.name} with {appointment.staff_member.name}.")
        
    def add_room(self, room):
        """Add a room to the department."""
        self.rooms.append(room)
        print(f"Room '{room.name}' added to {self.name} department.")

    def list_patients(self):
        
        if not self.patients:
            return f"No patients currently in {self.name} department."
        return "\n".join(f"- {p.name} (Age: {p.age})" for p in self.patients)

    def list_staff(self):
        
        if not self.staff:
            return f"No staff currently in {self.name} department."
        return "\n".join(f"- {s.name} ({s.position})" for s in self.staff)

    def list_appointments(self):
        
        if not self.appointments:
            return f"No appointments scheduled in {self.name} department."
        return "\n".join(a.view_details() for a in self.appointments)
