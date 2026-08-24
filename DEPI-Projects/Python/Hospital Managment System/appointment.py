class Appointment:
    

    _id_counter = 1  

    def __init__(self, patient, staff_member, date, time, reason=""):
        self.appointment_id = Appointment._id_counter
        Appointment._id_counter += 1

        self.patient = patient          
        self.staff_member = staff_member  
        self.date = date                
        self.time = time                
        self.reason = reason
        self.status = "Scheduled"       

    def view_details(self):
        """Return a formatted summary of the appointment."""
        return (f"[#{self.appointment_id}] {self.patient.name} with "
                f"{self.staff_member.name} ({self.staff_member.position}) "
                f"on {self.date} at {self.time} - Reason: {self.reason or 'N/A'} "
                f"- Status: {self.status}")

    def complete(self):
        
        self.status = "Completed"
        print(f"Appointment #{self.appointment_id} marked as completed.")

    def cancel(self):
        
        self.status = "Cancelled"
        print(f"Appointment #{self.appointment_id} has been cancelled.")



