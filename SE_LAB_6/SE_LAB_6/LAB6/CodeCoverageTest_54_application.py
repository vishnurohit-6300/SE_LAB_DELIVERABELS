
import pytest

from museum_admission import (
    ticket_price,
    group_discount,
    gallery_entry
)


# TICKET PRICE TEST CASES

def test_all_ticket_categories():
    assert ticket_price("adult", 30, "tuesday", False) == 300
    assert ticket_price("student", 20, "tuesday", False) == 150
    assert ticket_price("child", 8, "tuesday", False) == 100
    assert ticket_price("senior", 65, "tuesday", False) == 200


def test_invalid_category():
    with pytest.raises(ValueError):
        ticket_price("vip", 30, "tuesday", False)


def test_negative_age():
    with pytest.raises(ValueError):
        ticket_price("adult", -1, "tuesday", False)


def test_free_entry_below_five():
    assert ticket_price("adult", 4, "sunday", True) == 0


def test_monday_discount():
    assert ticket_price("adult", 30, "monday", False) == 150


def test_saturday_price():
    assert ticket_price("adult", 30, "saturday", False) == 350


def test_sunday_price():
    assert ticket_price("adult", 30, "sunday", False) == 350


def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200


def test_adult_guided_tour():
    assert ticket_price("adult", 30, "tuesday", True) == 400


# GROUP DISCOUNT TEST CASES

def test_invalid_group_size():
    with pytest.raises(ValueError):
        group_discount(0, False)


def test_school_group_above_twenty():
    assert group_discount(20, True) == 40


def test_school_group_below_twenty():
    assert group_discount(19, True) == 25


def test_non_school_group_above_fifteen():
    assert group_discount(15, False) == 20


def test_non_school_group_between_eight_and_fourteen():
    assert group_discount(10, False) == 10


def test_non_school_group_below_eight():
    assert group_discount(7, False) == 0


# GALLERY ENTRY TEST CASES

def test_gallery_full_capacity():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_above_capacity():
    assert gallery_entry(110, 100, False) == "wait"


def test_gallery_queue_without_timed_slot():
    assert gallery_entry(90, 100, False) == "queue"


def test_gallery_entry_with_timed_slot():
    assert gallery_entry(90, 100, True) == "enter"


def test_gallery_below_ninety_percent():
    assert gallery_entry(89, 100, False) == "enter"
