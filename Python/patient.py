from person import Person

class Patient(Person):
    '''
    Represents a patient in the hospital
    '''
    def __init__(self, name, age,patient_id, medical_record):
        super().__init__(name, age)
        self.patient_id = patient_id
        self.medical_record = medical_record

    def view_record(self):
        ''' 
        Displays the patient's medical record
        '''
        return f"Patient Record: {self.medical_record}"

    def view_info(self):
        ''' 
        Displays the patient's information
        '''
        return (
            f"Patient Name: {self.name}, "
            f"Age: {self.age}, "
            f"Patient ID: {self.patient_id}, "
            f"Medical Record: {self.medical_record}"
        )