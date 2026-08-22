class HospitalRoom:
    '''
    A class representing a hospital room with attributes for room ID, capacity, status, name, description, and a list of patients.
    
    '''
    def __init__(self, room_id: int, capacity: int, status: str, name: str, description: str):
        '''
        Initializes a HospitalRoom instance with the provided attributes.
        
        Args:
            room_id (int): Unique identifier for the room.
            capacity (int): Maximum number of patients the room can hold.
            status (str): Current status of the room.
            name (str): Name of the room.
            description (str): Description of the room.
        '''
        self.room_id = room_id
        self.capacity = int(capacity)
        self.status = status.lower()
        self.name = name
        self.description = description
        self.patients = []  

    def display_room(self):
        '''
        Displays the details of the hospital room.
        '''

        print(f"--- {self.name} (ID: {self.room_id}) ---")
        print(f"Status: {self.status.capitalize()}")
        print(f"Capacity: {len(self.patients)}/{self.capacity}")
        print(f"Description: {self.description}")
        print(f"Patients: {', '.join(self.patients) if self.patients else 'None'}")

    def update_room(self, name=None, capacity=None, status=None, description=None):

        """
        Updates room details directly using arguments instead of console input.

        """
        if name: self.name = name
        if capacity is not None: self.capacity = int(capacity)
        if status: self.status = status.lower()
        if description: self.description = description

    def check_availability(self) -> bool:
        """
        Checks if the room is available for patient assignment.
        Returns:
            bool: True if the room is available, False otherwise.
        """
        available = self.status == "available" and len(self.patients) < self.capacity
        print(f"Room '{self.name}' is {'available' if available else 'not available'}.")
        return available

    def assign_patient(self, patient_name: str):
        """
        Assigns a patient to the room if the room is available.
        Args:
            patient_name (str): Name of the patient to assign.
        """
        if len(self.patients) >= self.capacity:
            print(f"Cannot assign {patient_name}: Room '{self.name}' is at full capacity.")
            return

        if self.status in ["under maintenance", "cleaning"]:
            print(f"Cannot assign {patient_name}: Room '{self.name}' status is '{self.status}'.")
            return

        self.patients.append(patient_name)
        if len(self.patients) == self.capacity:
            self.status = "occupied"
        print(f"Patient {patient_name} assigned to room '{self.name}'.")

    def release_patient(self, patient_name: str):
        """
        Releases a patient from the room.
        Args:
            patient_name (str): Name of the patient to release.
        """
        if patient_name in self.patients:
            self.patients.remove(patient_name)
            self.status = "available"
            print(f"Patient {patient_name} released from room '{self.name}'.")
        else:
            print(f"Patient {patient_name} not found in room '{self.name}'.")


class NormalRoom(HospitalRoom):
    """
    Represents a normal hospital room.
    args:
        room_id (int): Unique identifier for the room.
        capacity (int): Maximum number of patients the room can hold.
        status (str): Current status of the room.
        name (str): Name of the room.
        description (str): Description of the room.
        floor (int): Floor number where the room is located.
    """

    def __init__(self, room_id, capacity, status, name, description, floor: int):
        '''
        Initializes a NormalRoom instance with the provided attributes.
        
        Args:
            room_id (int): Unique identifier for the room.
            capacity (int): Maximum number of patients the room can hold.
            status (str): Current status of the room.
            name (str): Name of the room.
            description (str): Description of the room.
            floor (int): Floor number where the room is located.
        '''
        super().__init__(room_id, capacity, status, name, description)
        self.floor = floor

    def display_room(self):
        '''
        Displays the details of the normal hospital room, including floor information.
        
        '''
        super().display_room()
        print(f"Floor: {self.floor}")


class ICURoom(HospitalRoom):
    """
    Represents an ICU hospital room.

    args:
        room_id (int): Unique identifier for the room.
        capacity (int): Maximum number of patients the room can hold.
        status (str): Current status of the room.
        name (str): Name of the room.
        description (str): Description of the room.
        equipment (list): List of medical equipment in the ICU room.
    """

    def __init__(self, room_id, capacity, status, name, description, equipment: list):
        '''
        Initializes an ICURoom instance with the provided attributes.
        
        Args:
            room_id (int): Unique identifier for the room.
            capacity (int): Maximum number of patients the room can hold.
            status (str): Current status of the room.
            name (str): Name of the room.
            description (str): Description of the room.
            equipment (list): List of medical equipment in the ICU room.
        '''
        super().__init__(room_id, capacity, status, name, description)
        self.equipment = equipment if equipment else []

    def check_equipment(self):
        """
        Checks the equipment in the ICU room.
        """
        print(f"ICU Equipment in {self.name}: {', '.join(self.equipment)}")

    def display_room(self):
        """
        Displays the details of the ICU hospital room, including equipment information.
        """
        super().display_room()
        print(f"Equipment: {', '.join(self.equipment)}")


class NurseryRoom(HospitalRoom):
    """
    Represents a nursery hospital room.

    args:
        room_id (int): Unique identifier for the room.
        capacity (int): Maximum number of patients the room can hold.
        status (str): Current status of the room.
        name (str): Name of the room.
        description (str): Description of the room.
        incubator_count (int): Number of incubators available in the nursery room.
    """

    def __init__(self, room_id, capacity, status, name, description, incubator_count: int):
        """
        Initializes a NurseryRoom instance with the provided attributes.

        Args:
            room_id (int): Unique identifier for the room.
            capacity (int): Maximum number of patients the room can hold.
            status (str): Current status of the room.
            name (str): Name of the room.
            description (str): Description of the room.
            incubator_count (int): Number of incubators available in the nursery room.
        """
        super().__init__(room_id, capacity, status, name, description)
        self.incubator_count = incubator_count

    def display_room(self):
        """
        Displays the details of the nursery hospital room, including incubator information.
        """
        super().display_room()
        print(f"Incubators Available: {self.incubator_count}")
