import datetime


class Schedule:
    def __init__(self, start_time, end_time) -> None:
        self.start_time = self._transform_time(start_time)
        self.end_time = self._transform_time(end_time)
        self.booked_slots = []
        self.booked_slots.append([self._transform_time('00:00'), self.start_time])
        self.booked_slots.append([self.end_time, self._transform_time('00:00')])
        self._register_booked_slot(self.booked_slots[0])
        self._register_booked_slot(self.booked_slots[1])

    def _transform_time(self, time):
        return datetime.datetime.strptime(time, '%H:%M').time()

    def _register_booked_slot(self, slot):
        # register slot in db
        pass

    def _update_booked_slot(self, *args):
        # update slot in db
        pass

    def _book_slot(self, start_interval, end_interval):
        start_interval = self._transform_time(start_interval)
        end_interval = self._transform_time(end_interval)
        if start_interval < self.start_time:
            return False
        if end_interval > self.end_time:
            return False
        for i in range(len(self.booked_slots) - 1):
            if start_interval >= self.booked_slots[i][1] and end_interval <= self.booked_slots[i + 1][0]:
                if start_interval == self.booked_slots[i][1] and end_interval == self.booked_slots[i + 1][0]:
                    self._update_booked_slot()
                    self.booked_slots[i:i+2] = [[self.booked_slots[i][0], self.booked_slots[i + 1][1]]]
                elif start_interval == self.booked_slots[i][1]:
                    self._update_booked_slot()
                    self.booked_slots[i][1] = end_interval
                elif end_interval == self.booked_slots[i + 1][0]:
                    self._update_booked_slot()
                    self.booked_slots[i + 1][0] = start_interval
                else:
                    self.booked_slots.insert(i + 1, [start_interval, end_interval])
                    self._register_booked_slot([start_interval, end_interval])
                return True

            if end_interval < self.booked_slots[i][0]:
                break
        return False

    def _get_empty_slots(self):
        empty_slots = []
        for i in range(len(self.booked_slots) - 1):
            empty_slots.append([self.booked_slots[i][1], self.booked_slots[i + 1][0]])
        return empty_slots


class Worker:
    def __init__(self, start_time, end_time, name, position) -> None:
        self.schedule = Schedule(start_time, end_time)
        self.name = name
        self.position = position
        self._db_register_worker()
    
    def _db_register_worker(self):
        # add new person in database
        pass

    def get_work_time(self):
        return self.schedule.start_time.strftime('%H:%M'), self.schedule.end_time.strftime('%H:%M')

    def get_empty_slots(self):
        empty_slots = self.schedule._get_empty_slots()
        # for slot in empty_slots:
        #     print(f'С {slot[0].strftime("%H:%M")} по {slot[1].strftime("%H:%M")}')
        return empty_slots

    def book_slot(self, start_interval, end_interval):
        booking = self.schedule._book_slot(start_interval, end_interval)
        if booking:
            return 'Slot is booked'
        return 'Slot is not empty'
        

def find_mutual_slots(workers):
    if len(workers) == 1:
        return workers[0].get_empty_slots()
    mutual_slots = []
    for worker in workers:
        slots = [slot for slot in worker.schedule.booked_slots if slot[0] != datetime.time(hour=0, minute=0) or slot[1] != datetime.time(hour=0, minute=0) ]
        mutual_slots += slots
    
    mutual_slots.sort()


    final_slots = [mutual_slots[0]]
    for slot in mutual_slots[1:]:
        if final_slots[-1][1] != datetime.time(hour=0, minute=0): 
            if slot[0] <= final_slots[-1][1] and slot[1] > final_slots[-1][1]:
                final_slots[-1][1] = slot[1]
            elif slot[0] > final_slots[-1][1]:
                final_slots.append(slot)
    
    empty_slots = []
    if final_slots[0][0] != datetime.time(hour=0, minute=0):
        empty_slots.append([datetime.time(hour=0, minute=0), final_slots[0][0]])
    for i in range(len(final_slots) - 1):
        empty_slots.append([final_slots[i][1], final_slots[i + 1][0]])
    return empty_slots


        

def main():
    p1 = Worker('08:00', '20:00', 'Mary', 'developer')
    print(p1.book_slot('9:00', '12:00'))
    print(p1.book_slot('10:00', '12:00')) # not empty
    # print(p1.get_empty_slots)
    p2 = Worker('10:00', '21:00', 'Kate', 'teamlead')
    print(p2.book_slot('9:00', '12:00')) # not empty
    print(p2.book_slot('12:45', '13:30'))
    # print(p2.schedule.booked_slots)
    p3 = Worker('10:00', '22:00', 'John', 'manager')
    print(p3.book_slot('9:00', '12:00'))  # not empty
    print(p3.book_slot('15:00', '16:00'))
    print(p3.book_slot('21:00', '21:30'))
    # print(p3.schedule.booked_slots)
    workers = [p1, p2, p3]
    print(find_mutual_slots(workers))


if __name__ == '__main__':
    main()