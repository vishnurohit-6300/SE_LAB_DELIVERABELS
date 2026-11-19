
import pytest

from museum_admission import (
    ticket_price,
    group_discount,
    gallery_entry
)


# TICKET PRICE - BRANCH TESTS

def test_ticket_invalid_category():
    with pytest.raises(ValueError):
        ticket_price("invalid", 25, "tuesday", False)


def test_ticket_negative_age():
    with pytest.raises(ValueError):
        ticket_price("adult", -1, "tuesday", False)


def test_ticket_age_below_five():
    assert ticket_price("adult", 4, "tuesday", False) == 0


def test_ticket_age_five():
    assert ticket_price("adult", 5, "tuesday", False) == 300


def test_ticket_monday():
    assert ticket_price("adult", 30, "monday", False) == 150


def test_ticket_saturday():
    assert ticket_price("adult", 30, "saturday", False) == 350


def test_ticket_sunday():
    assert ticket_price("adult", 30, "sunday", False) == 350


def test_ticket_normal_weekday():
    assert ticket_price("adult", 30, "wednesday", False) == 300


def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200


def test_non_student_guided_tour():
    assert ticket_price("adult", 30, "tuesday", True) == 400


def test_no_guided_tour():
    assert ticket_price("adult", 30, "tuesday", False) == 300


# GROUP DISCOUNT - BRANCH TESTS

def test_invalid_group():
    with pytest.raises(ValueError):
        group_discount(0, False)


def test_school_group_twenty():
    assert group_discount(20, True) == 40


def test_school_group_nineteen():
    assert group_discount(19, True) == 25


def test_non_school_group_fifteen():
    assert group_discount(15, False) == 20


def test_non_school_group_eight():
    assert group_discount(8, False) == 10


def test_non_school_group_seven():
    assert group_discount(7, False) == 0


# GALLERY ENTRY - BRANCH TESTS

def test_gallery_full():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_over_capacity():
    assert gallery_entry(110, 100, False) == "wait"


def test_gallery_ninety_percent_without_slot():
    assert gallery_entry(90, 100, False) == "queue"


def test_gallery_ninety_percent_with_slot():
    assert gallery_entry(90, 100, True) == "enter"


def test_gallery_below_ninety_percent():
    assert gallery_entry(89, 100, False) == "enter"
