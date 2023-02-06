"""
Feb, 2023

Authors: Juan Pablo Medina.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Juan Pablo Medina.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from doctors_office_utilities import create_appointment_dict, in_week

DOCTOR = 0
PATIENT = 1


class Doctor:
    """A Doctor in the office.

    === Public Attributes ===
    name: Name of the doctor.

    === Private Attributes ===
    _id_doctor: The doctor's id.
    _office: The doctor's office room name.

    === Representation Invariants ===

    """
    name: str
    _id_doctor: int
    _office: str

    def __init__(self, name: str, id_doc: int, office: str) -> None:
        """Initialize a doctor with <name> and <id_doc>.

        """
        self.name = name
        self._id_doctor = id_doc
        self._office = office

    def get_id(self) -> int:
        """Return a doctor's private id.

        >>> jp = Doctor('Jp', 1, '201')
        >>> jp.get_id()
        1
        """
        return self._id_doctor

    def get_office(self) -> str:
        """Return the doctor's office.

        >>> jp = Doctor('Jp', 1, '201')
        >>> jp.get_office()
        '201'
        """
        return self._office


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

    def update_cancellations(self) -> None:
        """Update the number of cancellations this patient has made.

        >>> jp = Patient('Jp', 1, 2)
        >>> jp.get_cancellation_num()
        0
        >>> jp.update_cancellations()
        >>> jp.get_cancellation_num()
        1
        """
        self._cancellations += 1

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
    """A Doctor Office.

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
    _schedule: dict[datetime, dict[str, tuple[Doctor, Optional[Patient]]]]

    def __init__(self, name: str) -> None:
        """Initialize a Doctor's Office.

        >>> office = DoctorOffice('Medina Inc.')
        >>> office.name
        'Medina Inc.'
        """
        self.name = name
        self._doctors = {}
        self._patients = {}
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

    def add_patient(self, patient: Patient) -> bool:
        """Add a new <patient> to this office iff the <patient> does not have
        the same id as another patient in this office.

        Return True iff the patient has been added to the office.
        """
        new_id = patient.get_id()
        if new_id not in self._patients:
            self._patients[new_id] = patient
            return True
        return False

    def _is_doc_available(self, time_point: datetime, doctor_id: int) -> bool:
        """Return whether doctor with <doctor_id> is available at <time_point>.

        A doctor is available at <time_point> iff: the doctor is not in any
        other appointments at this time.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1, 'A')
        >>> office.add_doctor(nick)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office._is_doc_available(feb_3_2023_12_00, 1)
        True
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1)
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
                                     doctor_id: int) -> bool:
        """Add a doctors availability to this office at <time_point> iff:
        the doctor with <doctor_id> is not already in an appointment at this
        time.

        Preconditions:
            - The Doctor with doctor_id is a doctor in this office.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1, 'A')
        >>> office.add_doctor(nick)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1)
        True
        """
        doctor = self._doctors[doctor_id]
        office_name = doctor.get_office()

        if time_point not in self._schedule:
            self._schedule[time_point] = {}

        if self._is_doc_available(time_point, doctor_id):
            app = (doctor, None)
            self._schedule[time_point][office_name] = app
            return True

        if len(self._schedule[time_point]) == 0:
            self._schedule.pop(time_point)
        return False

    def _schedule_with_other_doctor(
            self, time_point: datetime, available_app: list, patient: Patient) \
            -> None:
        """Schedule <patient> with another doctor at <time_point> that is not
        their primary doctor.

        Precondition:
            - available_app must be a list of available appointment rooms and
            must be greater than 0

        """
        room = available_app[0]
        doctor = self._schedule[time_point][room][DOCTOR]
        app_tuple = (doctor, patient)
        self._schedule[time_point][room] = app_tuple

    def book_patient(self, time_point: datetime, patient: Patient) -> bool:
        """Book a <patient> at <time_point> iff: there is a doctor available
        at this <time_point>, <patient> is not already booked into another
        appointment at <time_point>, and <patient> is a patient registered in
        this office.

        A patient will preferably be booked with their primary doctor, if their
        primary doctor is not available, they will see another doctor available
        at this time.

        Return False if no doctors are available at this <time_point>.

        Preconditions: a single doctor is available at this <time_point>

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1, '202')
        >>> jp = Patient('Jp', 1, 1)
        >>> office.add_patient(jp)
        True
        >>> office.add_doctor(nick)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office.book_patient(feb_3_2023_12_00, jp)
        False
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1)
        True
        >>> office.book_patient(feb_3_2023_12_00, jp)
        True
        """
        primary_id = patient.get_primary_doctor()
        available_appointments = []

        if time_point not in self._schedule:
            return False

        for room, info in self._schedule[time_point].items():
            doctor_id = info[DOCTOR].get_id()

            if doctor_id == primary_id and info[PATIENT] is None and \
                    patient in self._patients:
                doctor = info[DOCTOR]
                app_tuple = (doctor, patient)
                self._schedule[time_point][room] = app_tuple
                return True

            if info[PATIENT] is None:
                available_appointments.append(room)

        if len(available_appointments) > 0:
            self._schedule_with_other_doctor(
                time_point, available_appointments, patient)
            return True
        return False

    def cancel_appointment_patient(self,
                                   time_point: datetime,
                                   patient: Patient) -> bool:
        """Cancel a <patient>'s appointment at <time_point>.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1, '202')
        >>> jp = Patient('Jp', 1, 1)
        >>> office.add_doctor(nick)
        True
        >>> office.add_patient(jp)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1)
        True
        >>> office.book_patient(feb_3_2023_12_00, jp)
        True
        >>> jp.get_cancellation_num()
        0
        >>> office.cancel_appointment_patient(feb_3_2023_12_00, jp)
        True
        >>> jp.get_cancellation_num()
        1
        >>> office.book_patient(feb_3_2023_12_00, jp)
        True
        """
        if time_point not in self._schedule:
            return False

        for room in self._schedule[time_point]:
            info = self._schedule[time_point][room]
            if info[PATIENT].get_id() == patient.get_id():
                doctor = info[DOCTOR]
                app_tuple = (doctor, None)
                self._schedule[time_point][room] = app_tuple
                patient.update_cancellations()

                if patient.get_cancellation_num() == 10:
                    self._patients.pop(patient.get_id())
                return True
        return False

    def _book_cancelled_patient(self, time_point: datetime,
                                patient: Patient) -> bool:
        """Return True if patient who has had appointment cancelled by a doctor
        is booked at the earliest time possible with any doctor available.

        Return False if patient is not able to be booked.

        >>> office = DoctorOffice('Medina Inc.')
        >>> sara = Doctor('Sara', 2, '202')
        >>> jp = Patient('Jp', 1, 1)
        >>> office.add_doctor(sara)
        True
        >>> office.add_patient(jp)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> feb_4_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office.schedule_doctor_availability(feb_4_2023_12_00, 2)
        True
        >>> office._book_cancelled_patient(feb_3_2023_12_00, jp)
        True
        """
        dates = sorted([date for date in self._schedule.keys()
                        if time_point <= date])

        for date in dates:
            for room, info in self._schedule[date].items():
                if info[PATIENT] is None and patient.get_id() in self._patients:
                    doctor = info[DOCTOR]
                    app_tuple = (doctor, patient)
                    self._schedule[time_point][room] = app_tuple
                    return True
        return False

    def cancel_appointment_doctor(self, time_point: datetime, doctor: Doctor) \
            -> bool:
        """Cancel a <doctor>'s appointment at <time_point>.

        Return True if the patient has been succesfully booked with another
        doctor at the next available time.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1, '202')
        >>> jp = Patient('Jp', 1, 1)
        >>> office.add_doctor(nick)
        True
        >>> office.add_patient(jp)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1)
        True
        >>> office.book_patient(feb_3_2023_12_00, jp)
        True
        >>> office.cancel_appointment_doctor(feb_3_2023_12_00, nick)
        False
        """
        if time_point not in self._schedule:
            return False

        for room in self._schedule[time_point]:
            info = self._schedule[time_point][room]
            if doctor.get_id() == info[DOCTOR].get_id():
                self._schedule[time_point].pop(room)
                if len(self._schedule[time_point]) == 0:
                    self._schedule.pop(time_point)

                booked_other_doctor = \
                    self._book_cancelled_patient(time_point, info[PATIENT])
                return booked_other_doctor

    def _is_doctor_name_unique(self, doctor: Doctor) -> bool:
        """Return True iff the name of <doctor> is used by <= 1 doctor
        in the Office.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick_1 = Doctor('Nick', 1, '202')
        >>> office.add_doctor(nick_1)
        True
        >>> office._is_doctor_name_unique(nick_1)
        True
        >>> nick_2 = Doctor('Nick', 2, '203')
        >>> office.add_doctor(nick_2)
        True
        >>> office._is_doctor_name_unique(nick_1)
        False
        """
        doc_name = doctor.name
        doc_id = doctor.get_id()
        for ids in self._doctors:
            if doc_id != ids and self._doctors[ids].name == doc_name:
                return False
        return True

    def appointments_at(self, time_point: datetime) -> \
            list[dict[str, str | int]]:
        """Return a list of dictionaries, each representing an available
        appointment at <time_point>.

        Each dictionary must have the following keys and values:
            'Date': the weekday and date of the class as a string, in the format
                'Weekday, year-month-day' (e.g., 'Monday, 2022-11-07')
            'Time': the time of the class, in the format 'HH:MM' where
                HH uses 24-hour time (e.g., '15:00')
            'Room': the name of the room
            'Doctor': the name of the doctor
                If there are multiple doctors with the same name, the name
                should be followed by the doctor ID in parentheses
                e.g., "Nick (1)"
            'Patient': the patient's name or None if there is no booked patient

        The appointments should be sorted by room name, in alphabetical
        ascending order.

        If there are no offerings, return empty list.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1, 'A10')
        >>> sara = Doctor('Sara', 2, 'A11')
        >>> office.add_doctor(nick)
        True
        >>> office.add_doctor(sara)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1)
        True
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 2)
        True
        >>> jp = Patient('Jp', 2, 1)
        >>> lauren = Patient('Lauren', 3, 2)
        >>> office.add_patient(jp)
        True
        >>> office.add_patient(lauren)
        True
        >>> office.book_patient(feb_3_2023_12_00, jp)
        True
        >>> office.book_patient(feb_3_2023_12_00, lauren)
        True
        >>> office.appointments_at(feb_3_2023_12_00) == [
        ... {'Date': 'Friday, 2023-02-03', 'Time': '12:00', 'Room': 'A10',
        ... 'Doctor': 'Nick', 'Patient': 'Jp'},
        ... {'Date': 'Friday, 2023-02-03', 'Time': '12:00', 'Room': 'A11',
        ... 'Doctor': 'Sara', 'Patient': 'Lauren'}
        ... ]
        True
        """
        if time_point not in self._schedule:
            return []

        date = time_point.strftime('%A, %Y-%m-%d')
        time = time_point.strftime('%H:%M')
        appointments_of_day = self._schedule[time_point]
        appointments = []

        for room, info in appointments_of_day.items():
            unique = self._is_doctor_name_unique(info[DOCTOR])
            doc_name = info[DOCTOR].name
            patient_name = info[PATIENT].name

            if not unique:
                doc_name += ' (' + str(info[DOCTOR].get_id()) + ')'

            appointment = create_appointment_dict(
                date, time, room, doc_name, patient_name)
            appointments.append(appointment)

        appointments = sorted(appointments, key=lambda k: k['Room'])
        return appointments

    def to_schedule_list(self, week: datetime = None) -> \
            list[dict[str, str | int]]:
        """Return a list of dictionaries for the Office's entire schedule, with
        each dictionary representing an appointment.

        The dictionaries should be in the list in ascending order by their date
        and time (not the string representation of the date and time).
        Appointments occurring at exactly the same date and time should
        be in alphabetical order based on their room names.

        If <week> is specified, only return the events that occur between the
        date interval (between a Monday 0:00 and Sunday 23:59) that contains
        <week>.

        >>> office = DoctorOffice('Medina Inc.')
        >>> nick = Doctor('Nick', 1, 'A10')
        >>> sara = Doctor('Sara', 2, 'A11')
        >>> office.add_doctor(nick)
        True
        >>> office.add_doctor(sara)
        True
        >>> feb_3_2023_12_00 = datetime(2023, 2, 3, 12, 0)
        >>> feb_2_2023_12_00 = datetime(2023, 2, 2, 12, 0)
        >>> office.schedule_doctor_availability(feb_3_2023_12_00, 1)
        True
        >>> office.schedule_doctor_availability(feb_2_2023_12_00, 2)
        True
        >>> jp = Patient('Jp', 2, 1)
        >>> lauren = Patient('Lauren', 3, 2)
        >>> office.add_patient(jp)
        True
        >>> office.add_patient(lauren)
        True
        >>> office.book_patient(feb_3_2023_12_00, jp)
        True
        >>> office.book_patient(feb_2_2023_12_00, lauren)
        True
        >>> office.to_schedule_list() == [
        ... {'Date': 'Thursday, 2023-02-02', 'Time': '12:00', 'Room': 'A11',
        ... 'Doctor': 'Sara', 'Patient': 'Lauren'},
        ... {'Date': 'Friday, 2023-02-03', 'Time': '12:00', 'Room': 'A10',
        ... 'Doctor': 'Nick', 'Patient': 'Jp'}
        ... ]
        True
        """
        full_schedule = []
        time_points = sorted(list(self._schedule.keys()))

        for time_point in time_points:
            if in_week(time_point, week):
                full_schedule.extend(self.appointments_at(time_point))
        return full_schedule


if __name__ == '__main__':
    import doctest
    doctest.testmod()
