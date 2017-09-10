# -*- coding: utf-8 -*-

import unittest
import datetime

import officehours


new_years_eve = datetime.date(2015, 12, 31)
new_year = datetime.date(2016, 1, 1)
saturday = datetime.date(2016, 1, 2)
sunday = datetime.date(2016, 1, 3)
monday = datetime.date(2016, 1, 4)
tuesday = datetime.date(2016, 1, 5)
new_years_eve_early = datetime.datetime(2015, 12, 31, 6, 10)
new_years_eve_morning = datetime.datetime(2015, 12, 31, 9, 30)
new_years_eve_late = datetime.datetime(2015, 12, 31, 20, 40)
sunday_morning = datetime.datetime(2016, 1, 3, 9, 0)
sunday_afternoon = datetime.datetime(2016, 1, 3, 17, 0)
monday_early = datetime.datetime(2016, 1, 4, 5, 0)
monday_morning = datetime.datetime(2016, 1, 4, 9, 0)
monday_noon = datetime.datetime(2016, 1, 4, 12, 0)
monday_late = datetime.datetime(2016, 1, 4, 18, 0)
tuesday_early = datetime.datetime(2016, 1, 5, 8, 0)


class TestDate(unittest.TestCase):
    def setUp(self):
        self.calculator = officehours.Calculator(start='9:00', close='17:00')
        self.calculator.add_holidays(new_year)

    def set_time(self):
        self.assertEqual(monday_noon, self.calculator.set_time(monday, '12:00'))
        self.assertEqual(monday_noon, self.calculator.set_time(monday_early, monday_noon))
        self.assertEqual(monday_morning, self.calculator.set_time(monday_early, self.calculator.start))

    def test_add_holidays(self):
        self.assertEqual({new_year}, self.calculator.holidays)
        with self.assertRaises(TypeError):
            self.calculator.add_holidays([0])

    def test_seconds(self):
        self.assertEqual(0, self.calculator.seconds(monday))
        self.assertEqual(32400, self.calculator.seconds('9:00'))
        self.assertEqual(32400, self.calculator.seconds(monday_morning))
        with self.assertRaises(TypeError):
            self.calculator.seconds(self.calculator)

    def test_validate(self):
        self.assertEqual((0, 0), self.calculator.validate('0:00'))
        self.assertEqual((12, 30), self.calculator.validate('12:30'))
        with self.assertRaises(officehours.TimeFormatError):
            self.calculator.validate('24:00')

    def test_work_day(self):
        self.assertEqual(8, self.calculator.work_day)

    def test_date(self):
        self.assertEqual(monday, self.calculator.date(monday_morning))
        with self.assertRaises(TypeError):
            self.calculator.date(0)

    def test_is_weekend(self):
        self.assertTrue(self.calculator.is_weekend(saturday))
        self.assertTrue(self.calculator.is_weekend(sunday))
        self.assertFalse(self.calculator.is_weekend(monday))

    def test_is_bank_holiday(self):
        self.assertTrue(self.calculator.is_holiday(new_year))
        self.assertFalse(self.calculator.is_holiday(sunday))
        self.assertFalse(self.calculator.is_holiday(monday))

    def test_is_working_day(self):
        self.assertTrue(self.calculator.is_working_day(monday))
        self.assertFalse(self.calculator.is_working_day(new_year))
        self.assertFalse(self.calculator.is_working_day(saturday))

    def test_is_working_time(self):
        self.assertFalse(self.calculator.is_working_time(monday))
        self.assertFalse(self.calculator.is_working_time(monday_early))
        self.assertTrue(self.calculator.is_working_time(monday_morning))
        self.assertFalse(self.calculator.is_working_time(sunday_morning))

    def test_normalize(self):
        self.assertEqual(32400, self.calculator.normalize(monday_early))
        self.assertEqual(32400, self.calculator.normalize(monday_morning))
        self.assertEqual(32400, self.calculator.normalize(monday))
        self.assertEqual(34200, self.calculator.normalize(new_years_eve_morning))
        self.assertEqual(61200, self.calculator.normalize(new_years_eve_late))

    def test_previous_office_close(self):
        self.assertEqual(datetime.datetime(2015, 12, 31, 17, 0), self.calculator.previous_office_close(sunday_afternoon))
        self.assertEqual(datetime.datetime(2015, 12, 31, 17, 0), self.calculator.previous_office_close(monday_noon))
        self.assertEqual(datetime.datetime(2016, 1, 4, 17, 0), self.calculator.previous_office_close(monday_late))

    def test_next_office_open(self):
        self.assertEqual(monday_morning, self.calculator.next_office_open(new_years_eve_morning))
        self.assertEqual(monday_morning, self.calculator.next_office_open(new_year))
        self.assertEqual(monday_morning, self.calculator.next_office_open(monday_early))

    def test_count(self):
        self.assertEqual(7.75, self.calculator.count('8:00', '16:45'))
        self.assertEqual(7.5, self.calculator.count(new_years_eve_morning, new_years_eve_late))

    def test_working_days(self):
        self.assertEqual(1, self.calculator.working_days(new_years_eve, sunday))
        self.assertEqual(1, self.calculator.working_days(new_years_eve, monday))
        self.assertEqual(0, self.calculator.working_days(monday, monday))
        self.assertEqual(1, self.calculator.working_days(monday, tuesday))

    def test_working_hours(self):
        self.assertEqual(0.5, self.calculator.working_hours(new_years_eve_early, new_years_eve_morning))
        self.assertEqual(8, self.calculator.working_hours(new_years_eve_early, new_years_eve_late))
        self.assertEqual(0, self.calculator.working_hours(new_years_eve_late, monday_early))
        self.assertEqual(8, self.calculator.working_hours(new_years_eve_late, monday_late))
        self.assertEqual(8, self.calculator.working_hours(new_years_eve_early, monday_morning))
        self.assertEqual(0, self.calculator.working_hours(saturday, sunday))
        self.assertEqual(0, self.calculator.working_hours(sunday, sunday))
        self.assertEqual(0, self.calculator.working_hours(sunday, saturday))
        self.assertEqual(0, self.calculator.working_hours(sunday_morning, sunday_afternoon))
        self.assertEqual(8, self.calculator.working_hours(new_years_eve_late, tuesday_early))

    def test_due_date(self):
        self.assertEqual(new_years_eve_morning, self.calculator.due_date(0.5, new_years_eve_early))
        self.assertEqual(monday_noon, self.calculator.due_date(10.5, new_years_eve_morning))

    def test_start_time(self):
        self.assertEqual(new_years_eve_morning, self.calculator.start_time(10.5, monday_noon))
        self.assertEqual(monday_noon, self.calculator.start_time(5, tuesday_early))

    def test_find_date(self):
        self.assertEqual(monday_noon, self.calculator.find_date(-5, tuesday_early))
        self.assertEqual(monday_noon, self.calculator.find_date(0, monday_noon))
        self.assertEqual(monday_morning, self.calculator.find_date(0, monday_early))


if __name__ == "__main__":
    unittest.main()
