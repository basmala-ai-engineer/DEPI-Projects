class Staff:
    def __init__(self, id:int, name:str, position:str):
        """
        Initializes a Staff object with the given id, name, and position.
        :param id: Unique identifier for the staff member.
        :param name: Name of the staff member.
        :param position: Position of the staff member.
        """
        self.id = id
        self.name = name
        self.position = position

    def __disp__(self):

        """
        Displays the staff member's details.
        """
        print(f"Staff ID: {self.id}, Name: {self.name}, Position: {self.position}")

    def __update__(self, name:str=None, position:str=None):
        """
        Updates the staff member's details.
        :param name: New name for the staff member.
        :param position: New position for the staff member.
        """
        if name:
            self.name = name
        if position:
            self.position = position        

class Doctor(Staff):
    def __init__(self, id:int, name:str, position:str, specialty:str):
        """
        Initializes a Doctor object with the given id, name, position, and specialty.
        :param id: Unique identifier for the doctor.
        :param name: Name of the doctor.
        :param position: Position of the doctor.
        :param specialty: Specialty of the doctor.
        """
        super().__init__(id, name, position)
        self.specialty = specialty

    def __disp__(self):
        """
        Displays the doctor's details including specialty.
        """
        super().__disp__()
        print(f"Specialty: {self.specialty}")

    def __update__(self, name:str=None, position:str=None, specialty:str=None):
        """
        Updates the doctor's details.
        :param name: New name for the doctor.
        :param position: New position for the doctor.
        :param specialty: New specialty for the doctor.
        """
        super().__update__(name, position)
        if specialty:
            self.specialty = specialty

    def __disp__(self):
        """
        Displays the doctor's details including specialty.
        """
        super().__disp__()
        print(f"Specialty: {self.specialty}")


class Nurse(Staff):
    def __init__(self, id:int, name:str, position:str, department:str):
        """
        Initializes a Nurse object with the given id, name, position, and department.
        :param id: Unique identifier for the nurse.
        :param name: Name of the nurse.
        :param position: Position of the nurse.
        :param department: Department of the nurse.
        """
        super().__init__(id, name, position)
        self.department = department

    def __disp__(self):
        """
        Displays the nurse's details including department.
        """
        super().__disp__()
        print(f"Department: {self.department}")

    def __update__(self, name:str=None, position:str=None, department:str=None):
        """
        Updates the nurse's details.
        :param name: New name for the nurse.
        :param position: New position for the nurse.
        :param department: New department for the nurse.
        """
        super().__update__(name, position)
        if department:
            self.department = department


class Receptionist(Staff):
    def __init__(self, id:int, name:str, position:str, shift:str):
        """
        Initializes a Receptionist object with the given id, name, position, and shift.
        :param id: Unique identifier for the receptionist.
        :param name: Name of the receptionist.
        :param position: Position of the receptionist.
        :param shift: Shift of the receptionist.
        """
        super().__init__(id, name, position)
        self.shift = shift

    def __disp__(self):
        """
        Displays the receptionist's details including shift.
        """
        super().__disp__()
        print(f"Shift: {self.shift}")

    def __update__(self, name:str=None, position:str=None, shift:str=None):
        """
        Updates the receptionist's details.
        :param name: New name for the receptionist.
        :param position: New position for the receptionist.
        :param shift: New shift for the receptionist.
        """
        super().__update__(name, position)
        if shift:
            self.shift = shift

class Engineer(Staff):
    def __init__(self, id:int, name:str, position:str, field:str):
        """
        Initializes an Engineer object with the given id, name, position, and field.
        :param id: Unique identifier for the engineer.
        :param name: Name of the engineer.
        :param position: Position of the engineer.
        :param field: Field of the engineer whatever it is maintenance, installation and sales.
        """
        super().__init__(id, name, position)
        self.field = field

    def __disp__(self):
        """
        Displays the engineer's details including field.
        """
        super().__disp__()
        print(f"Field: {self.field}")

    def __update__(self, name:str=None, position:str=None, field:str=None):
        """
        Updates the engineer's details.
        :param name: New name for the engineer.
        :param position: New position for the engineer.
        :param field: New field for the engineer.
        """
        super().__update__(name, position)
        if field:
            self.field = field


class Manager(Staff):
    def __init__(self, id:int, name:str, position:str, department:str):
        """
        Initializes a Manager object with the given id, name, position, and department.
        :param id: Unique identifier for the manager.
        :param name: Name of the manager.
        :param position: Position of the manager.
        :param department: Department of the manager.
        """
        super().__init__(id, name, position)
        self.department = department

    def __disp__(self):
        """
        Displays the manager's details including department.
        """
        super().__disp__()
        print(f"Department: {self.department}")

    def __update__(self, name:str=None, position:str=None, department:str=None):
        """
        Updates the manager's details.
        :param name: New name for the manager.
        :param position: New position for the manager.
        :param department: New department for the manager.
        """
        super().__update__(name, position)
        if department:
            self.department = department

                        