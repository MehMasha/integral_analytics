import unittest
import datetime
from main import Worker, find_mutual_slots


class TestSchedule(unittest.TestCase):

    p1 = Worker('08:00', '20:00', 'Mary', 'developer')
    p2 = Worker('07:00', '21:00', 'Kate', 'teamlead')
    p2.book_slot('9:00', '12:00') # not empty
    p2.book_slot('12:45', '13:30')
    p3 = Worker('08:00', '22:00', 'John', 'manager')
    p3.book_slot('9:00', '12:00') 
    p3.book_slot('15:00', '16:00')
    p3.book_slot('21:00', '21:30')

    def test_booking_success(self):
        self.assertEqual(self.p1.book_slot('9:00', '12:00'), 'Slot is booked', 'Slot should be booked')

    def test_booking_fail(self):
        self.assertEqual(self.p1.book_slot('07:00', '12:00'), 'Slot is not empty', 'Slot should be unavailable')

    def test_work_time(self):
        self.assertEqual(self.p1.get_work_time(), ('08:00', '20:00'), 'Incorrect work time')

    def test_empty_slots(self):
        self.assertEqual(self.p1.get_empty_slots(), [[datetime.time(hour=8, minute=0), datetime.time(hour=9, minute=0)],
                                                    [datetime.time(hour=12, minute=0), datetime.time(hour=20, minute=0)]], 
                                                    'Incorrect empty slots')
    def test_mutual_slots(self):
        real_slots = [[datetime.time(hour=8, minute=0), datetime.time(hour=9, minute=0)],
                    [datetime.time(hour=12, minute=0), datetime.time(hour=12, minute=45)],
                    [datetime.time(hour=13, minute=30), datetime.time(hour=15, minute=0)],
                    [datetime.time(hour=16, minute=0), datetime.time(hour=20, minute=0)]]
        self.assertEqual(find_mutual_slots([self.p1, self.p2, self.p3]), real_slots, 'Incorrect mutual slots')


if __name__ == '__main__':
    unittest.main()