"""
Feb, 2023

Authors: Juan Pablo Medina.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Juan Pablo Medina.
"""
import pytest
from doctors_office import Doctor, Patient, DoctorOffice


class TestDoctor:
    """Test cases for the Doctor class."""

    def test_name(self) -> None:
        """Test Doctor.__init__ with its name.
        """
        nick = Doctor('Nick', 1, 'A1')
        assert nick.name == 'Nick'

    def test_get_id_simple(self) -> None:
        """Test Doctor.get_id with a random id.
        """
        nick = Doctor('Nick', 1, 'A1')
        assert nick.get_id() == 1

    def test_get_office_simple(self) -> None:
        """Test Doctor.get_office with a random room.
        """
        nick = Doctor('Nick', 1, 'A1')
        assert nick.get_office() == 'A1'


class TestPatient:
    """Test cases for the Patient class."""

    def test_name(self) -> None:
        """Test Patient.__init__ with its name.
        """
        jp = Patient('JP', 1, 1)
        assert jp.name == 'JP'

    def test_get_id_simple(self) -> None:
        """Test Patient.get_id with a random id.
        """
        jp = Patient('JP', 1, 1)
        assert jp.get_id() == 1

    def test_get_primary_doctor_simple(self) -> None:
        """Test Patient.get_primary_doctor with a random doctor id.
        """
        jp = Patient('JP', 1, 2)
        assert jp.get_primary_doctor() == 2

    def test_get_cancellation_num_initially(self) -> None:
        """Test Patient.get_cancellation_num initially.
        """
        jp = Patient('JP', 1, 2)
        assert jp._cancellations == 0
        assert jp.get_cancellation_num() == 0

    def test_update_cancellations_simple(self) -> None:
        """Test Patient.update_cancellations for multiple cancellations.
        """
        jp = Patient('JP', 1, 1)
        assert jp.get_cancellation_num() == 0
        jp.update_cancellations()
        jp.update_cancellations()
        assert jp.get_cancellation_num() == 2


class TestDoctorOffice:
    """Test cases for the DoctorOffice class."""

    def test_init_name(self) -> None:
        """Test DoctorOffice.__init__ with its name.
        """
        office = DoctorOffice('Medina Inc.')
        assert office.name == 'Medina Inc.'

    def test_add_doctor_one(self) -> None:
        """Test DoctorOffice.add_doctor with one doctor.
        """
        office = DoctorOffice('Medina Inc.')
        nick = Doctor('Nick', 2, 'A1')
        assert office.add_doctor(nick) is True
        assert len(office._doctors) == 1

    def test_add_doctor_same_id(self) -> None:
        """Test DoctorOffice.add_doctor with same id.
        """
        office = DoctorOffice('Medina Inc.')
        nick = Doctor('Nick', 2, 'A1')
        sara = Doctor('Sara', 2, 'A3')
        assert office.add_doctor(nick) is True
        assert office.add_doctor(sara) is False


if __name__ == '__main__':
    pytest.main(['doctors_office.py'])
