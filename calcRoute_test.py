import pytest
import calcRoute
import argparse


# Test inputs
def test_argument_parsing():
    test_result = calcRoute.parse_arguments()
    assert test_result.__contains__('OK')


@pytest.mark.parametrize("origin, destination, hour, expected", [
    ('A', 3, '12:00', 'Error'),
    (3.4, 3, '12:00', 'Error'),
    ((0, 2), 3, '12:00', 'Error'),
    (None, 3, '12:00', 'Error'),
    (1, 'r', '12:00', 'Error'),
    (1, 5.5, '12:00', 'Error'),
    (1, (1, 76), '12:00', 'Error'),
    (1, None, '12:00', 'Error'),
    (10, 6, '12:A', 'Error'),
    (10, 6, '12', 'Error'),
    (10, 6, '12,2', 'Error'),
    (0, 3, '12:00', 'Error'),
    (15, 3, '12:00', 'Error'),
    (-3, 3, '12:00', 'Error'),
    (1, 67, '12:00', 'Error'),
    (1, -6, '12:00', 'Error'),
    (1, 0, '12:00', 'Error'),
    (14, 6, '23:55', 'Error'),
    (10, 6, '00:00', 'Error'),
    (10, 6, '01:23', 'Error'),
    (10, 6, '04:30', 'Error'),
    (10, 10, '12:30', 'Error'),
    (4, 4, '15:00', 'Error'),
    (14, 5, '22:00', 'OK'),
    (12, 5, '22:00', 'OK'),
])
def test_arguments(origin, destination, hour, expected):
    test_input = argparse.Namespace(o=origin, d=destination, h=hour)
    result = calcRoute.check_input(test_input)
    assert result.__contains__(expected)
