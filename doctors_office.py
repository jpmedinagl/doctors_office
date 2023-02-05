"""
Feb, 2023

Authors: Juan Pablo Medina.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Juan Pablo Medina.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any


class Doctor:
    """

    === Public Attributes ===

    === Private Attributes ===

    === Representation Invariants ===

    """
    pass


class Patient:
    """A patient in a doctors office.

    === Public Attributes ===
    name: Name of the patient

    === Private Attributes ===
    _id_patient: The id of a specific patient.
    _primary_doctor_id: The primary doctors id.

    === Representation Invariants ===
    """
    name: str
    _id_patient: int
    _primary_doctor_id: int

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

    def get_id(self) -> int:
        """Get a patients private id.

        >>> jp = Patient('Jp', 1, 2)
        >>> jp.get_id()
        1
        """
        return self._id_patient

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

    === Private Attributes ===

    === Representation Invariants ===

    """
    pass
