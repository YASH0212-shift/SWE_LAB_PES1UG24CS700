
import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# Existing example tests
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0


def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100


# toll_for: invalid axle count
def test_invalid_axle_count():
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)


def test_zero_axles():
    with pytest.raises(ValueError):
        toll_for(0, False, False)


# toll_for: all base toll categories
def test_three_axle_base_toll():
    assert toll_for(3, False, False) == 150


def test_four_axle_base_toll():
    assert toll_for(4, False, False) == 250


def test_unknown_axle_count_uses_default_toll():
    assert toll_for(5, False, False) == 400


# toll_for: peak-hour charges
def test_peak_hour_two_axle():
    assert toll_for(2, True, False) == 125


def test_non_peak_hour():
    assert toll_for(3, False, False) == 150


# toll_for: FASTag discounts
def test_fastag_two_axle():
    assert toll_for(2, False, True) == 90


def test_fastag_non_two_axle():
    assert toll_for(3, False, True) == 142.5


# toll_for: peak hour combined with FASTag
def test_peak_and_fastag_two_axle():
    assert toll_for(2, True, True) == 112.5


def test_peak_and_fastag_three_axle():
    assert toll_for(3, True, True) == 178.12


# toll_charge: exempt and non-exempt vehicles
def test_fire_engine_is_exempt():
    assert toll_charge("fire_engine", 3, True, True) == 0


def test_car_is_charged():
    assert toll_charge("car", 2, False, False) == 100


def test_non_exempt_invalid_axles_raise_error():
    with pytest.raises(ValueError):
        toll_charge("car", 1, False, False)


# pass_advice: all return outcomes
def test_buy_pass_when_cost_exceeds_price():
    assert pass_advice([(False, False)], 2, 99) == "buy_pass"


def test_either_when_cost_equals_price():
    assert pass_advice([(False, False)], 2, 100) == "either"


def test_pay_per_trip_when_cost_is_below_price():
    assert pass_advice([(False, False)], 2, 101) == "pay_per_trip"


# pass_advice: multiple and empty trips
def test_multiple_trips():
    trips = [(False, False), (True, False)]
    assert pass_advice(trips, 2, 200) == "buy_pass"


def test_empty_trip_list():
    assert pass_advice([], 2, 0) == "either"


def test_empty_trip_list_with_positive_pass_price():
    assert pass_advice([], 2, 1) == "pay_per_trip"
