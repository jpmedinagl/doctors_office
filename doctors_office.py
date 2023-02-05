"""
Feb, 2023

Authors: Juan Pablo Medina.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Juan Pablo Medina.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

DOCTOR = 0
PATIENT = 1


class Doctor:
    """

    === Public Attributes ===
    name: Name of the doctor.

    === Private Attributes ===
    _id_doctor: The doctor's id.

    === Representation Invariants ===

    """
    name: str
    _id_doctor: int

    def __init__(self, name: str, id_doc: int) -> None:
        """Initialize a doctor with <name> and <id_doc>.

        """
        self.name = name
        self._id_doctor = id_doc

    def get_id(self) -> int:
        """Get a doctor's private id.

        >>> jp = Doctor('Jp', 1, 2)
        >>> jp.get_id()
        1
        """
        return self._id_doctor


class Patient:
    """A patient in a doctors office.

    === Public Attributes ===
    name: Name of the patient

    === Private Attributes ===
    _id_patient: The id of a specific patient.
    _primary_doctor_id: The primary doctor's id.
    _cancellations: The number of times this patient has cancelled an
        appointment.

    === Representation Invariants ===
    """
    name: str
    _id_patient: int
    _primary_doctor_id: int
    _cancellations: int

    def __init__(self, name: str, id_patient: int, primary_doctor_id: int) \
            -> None:
        """Initialize a patient with a <name>, id of <_id_patient>, and a
        primary doctor's id of <_primary_doctor_id>.

        >>> jp = Patient('Jp', 1, 2)
        >>> jp.name
        'Jp'
        """
        self.name = name
        self._id_patient = id_patient
        self._primary_doctor_id = primary_doctor_id
        self._cancellations = 0

    def get_id(self) -> int:
        """Return a patients private id.

        >>> jp = Patient('Jp', 1, 2)
        >>> jp.get_id()
        1
        """
        return self._id_patient

    def get_primary_doctor(self) -> int:
        """Return this patient's primary doctor's id.
        """
        return self._primary_doctor_id

    def get_cancellation_num(self) -> int:
        """Return this patients number of times they have cancelled an
        appointment.

        """
        return self._cancellations

    def change_primary_doctor(self, new_primary_doctor: int) -> None:
        """Change a patients primary doctor id with <new_primary_doctor>.

        >>> jp = Patient('Jp', 1, 2)
        >>> jp._primary_doctor_id
        2
        >>> jp.change_primary_doctor(4)
        >>> jp._primary_doctor_id
        4
        """
        self._primary_doctor_id = new_primary_doctor


class DoctorOffice:
    """

    === Public Attributes ===
    name: The name of the Doctor Office.

    === Private Attributes ===
    _doctors: The doctors that are part of this office.
        Each key is a doctor's ID and its value is the Doctor object
        representing them.
    _patients: The patients that are part of this office.
        Each key is a patient's ID and its value is the Patient object
        representing them.
    _schedule: The schedule of appointments at this office.
        Each key is a date and time and its value is a nested dictionary
        describing the appointments that start then. In the nested dictionary,
        the key describes the room a doctor is available in and the value
        corresponds to a tuple of:
            - doctor with an appointment
            - patient with an appointment

    === Representation Invariants ===

    """
    name: str
    _doctors: dict[int, Doctor]
    _patients: dict[int, Patient]
    _schedule: dict[datetime, dict[str, list[Doctor, Optional[Patient]]]]

    def __init__(self, name: str) -> None:
        """Initialize a Doctor's Office.

        >>> office = DoctorOffice('Medina Inc.')
        >>> office.name
        'Medina Inc.'
        """
        self.name = name
        self._doctors = {}
        self._schedule = {}

    def add_doctor(self, doctor: Doctor) -> bool:
        """Add a new <doctor> to this office iff the <doctor> does not have
        the same id as another doctor in this office.

        Return True iff the doctor has been added to the office.

        """
        new_id = doctor.get_id()
        if new_id not in self._doctors:
            self._doctors[new_id] = doctor
            return True
        return False

    def _is_doc_available(self, time_point: datetime, doctor_id: int) -> bool:
        """Return whether doctor with <doctor_id> is available at <time_point>.

        A doctor is available at <time_point> iff: the doctor is not in any
        other appointments at this time.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1)
        >>> office.add_doctor(nick)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office._is_doc_available(feb_3_2023_12_00, 1)
        True
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1, 'A')
        True
        >>> office._is_doc_available(feb_3_2023_12_00, 1)
        False
        """
        if time_point not in self._schedule:
            return True

        appointments = self._schedule[time_point]
        for room in appointments:
            doctor = self._schedule[time_point][room][DOCTOR]
            if doctor_id == doctor.get_id():
                return False
        return True

    def schedule_doctor_availability(self, time_point: datetime,
                                     doctor_id: int, room_name: str) -> bool:
        """Add a doctors availability to this office at <time_point> iff:
        the doctor with <doctor_id> is not already in an appointment at this
        time, and the room with <room_name> is not already being used for
        another appointment at this time.

        Preconditions:
            - The Doctor with doctor_id is a doctor in this office.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1)
        >>> office.add_doctor(nick)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1, 'A101')
        True
        """
        doctor = self._doctors[doctor_id]

        if time_point not in self._schedule:
            self._schedule[time_point] = {}

        if room_name not in self._schedule[time_point] \
                and self._is_doc_available(time_point, doctor_id):
            app = [doctor, None]
            self._schedule[time_point][room_name] = app
            return True

        if len(self._schedule[time_point]) == 0:
            self._schedule.pop(time_point)
        return False

    def _is_doc_scheduled(self, time_point: datetime, doctor_id: int) -> None:
        """Return whether a doctor with <doctor_id> has an appointment at
        <time_point>.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1)
        >>> jp = Patient('Jp', 1, 1)
        >>> office.add_doctor(nick)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office._is_doc_scheduled(feb_3_2023_12_00, 1)
        False
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1, 'A101')
        True
        >>> office._is_doc_scheduled(feb_3_2023_12_00, 1)
        True
        """
        pass

    def book_patient(self, time_point: datetime, patient: Patient) -> bool:
        """Book a <patient> at <time_point> iff: there is a doctor available
        at this <time_point> and <patient> is not already booked into another
        appointment at <time_point>.

        A patient will preferably be booked with their primary doctor, if their
        primary doctor is not available, they will see another doctor available
        at this time.

        Return False if no doctors are available at this <time_point>.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1)
        >>> jp = Patient('Jp', 1, 1)
        >>> office.add_doctor(nick)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office.book_patient(feb_3_2023_12_00, jp)
        False
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1, 'A')
        True
        >>> office.book_patient(feb_3_2023_12_00, jp)
        True
        """
        primary_id = patient.get_primary_doctor()
        doc_availability = self._is_doc_scheduled(time_point, primary_id)
        available_appointment_rooms = {}

        if time_point not in self._schedule:
            return False

        for room, info in self._schedule[time_point].items():
            doctor_id = info[DOCTOR].get_id()
            app_patient = info[PATIENT]

            if patient != app_patient:
                available_appointment_rooms[doctor_id] = room

        if doc_availability:
            room = available_appointment_rooms[primary_id]
        else:
            doctors = list(available_appointment_rooms.keys())
            room = available_appointment_rooms[doctors[0]]

        if len(available_appointment_rooms) > 0:
            self._schedule[time_point][room][PATIENT] = patient
            return True
        return False

