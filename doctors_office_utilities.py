"""
Feb, 2023

Authors: Juan Pablo Medina.

All of the files in this directory and all subdirectories are:
Copyright (c) 2023 Juan Pablo Medina.
"""

from datetime import datetime, timedelta


def create_appointment_dict(date: str,
                            time: str,
                            room_name: str,
                            doctor_name: str,
                            patient_name: str) -> dict[str, str | int]:
    """Return a dictionary that represents all the given attributes of a
    doctor's appointment.
    """
    return {
        'Date': date,
        'Time': time,
        'Room': room_name,
        'Doctor': doctor_name,
        'Patient': patient_name,
    }


def in_week(date: datetime, week: datetime = None) -> bool:
    """Return True iff <date> is in the same week as <week>.

    A week is defined as the period from Monday 0:00 to Sunday 23:59.
    Return True if no week is provided.

    Hint: You may find this helper function useful in your own code.

    >>> # Note: You can create a datetime that has only year, month, day, or
    >>> # you can optionally specify hour, minute, etc.
    >>> in_week(datetime(2022, 9, 1, 12, 0), datetime(2022, 8, 31))
    True
    >>> in_week(datetime(2022, 9, 1, 12, 0), datetime(2022, 9, 7))
    False
    >>> in_week(datetime(2022, 9, 1, 12, 0), datetime(202, 9, 8))
    False
    >>> in_week(datetime(2023, 1, 1), datetime(2022, 12, 31))
    True
    >>> in_week(datetime(2023, 1, 1))
    True
    """
    if not week:
        return True
    # find the first and last day of the calendar week containing <week>.
    week = week.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = week - timedelta(days=week.weekday())
    week_end = week_start + timedelta(days=6)
    week_end = week_end.replace(hour=23, minute=59, second=59, microsecond=0)
    # return True iff <date> is between <week_start> and <week_end>
    # return (week_start <= date) and (date <= week_end)  # pyTA complains
    return week_start <= date <= week_end
