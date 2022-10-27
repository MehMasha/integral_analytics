import datetime



class Schedule:
    def __init__(self, start_time, end_time) -> None:
        self.start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
        self.end_time = datetime.datetime.strptime(end_time, '%H:%M').time()
        self.free_time = [[self.start_time, self.end_time]]

    def __book_slot(self, start_interval, end_interval):
        start_interval = datetime.datetime.strptime(start_interval, '%H:%M').time()
        end_interval = datetime.datetime.strptime(end_interval, '%H:%M').time()
        for i in range(len(self.free_time)):
            if start_interval < self.free_time[i][0]:
                break
            if start_interval >= self.free_time[i][0] and end_interval <= self.free_time[i][1]:
                if start_interval == self.free_time[i][0] and end_interval == self.free_time[i][1]:
                    del self.free_time[i]
                elif start_interval == self.free_time[i][0]:
                    self.free_time[i][0] = end_interval
                elif end_interval == self.free_time[i][1]:
                    self.free_time[i][1] = start_interval
                else:
                    self.free_time[i:i+1] = [[self.free_time[i][0], start_interval], [end_interval, self.free_time[i][1]]]
                return True
        return False



class Worker:
    def __init__(self, start_time, end_time, name) -> None:
        self.schedule = Schedule(start_time, end_time)
        self.name = name
    

    def get_work_time(self):
        return self.schedule.start_time, self.schedule.end_time

    def get_empty_slots(self):
        return self.schedule.free_time

    def book_slot(self, start_interval, end_interval):
        booking = self.schedule.__book_slot(start_interval, end_interval)
        if booking:
            return 'Slot is booked'
        return 'Slot is not empty'
        
        
        

def main():
    p1 = Worker('08:00', '20:00', 'Mary')
    for i in range(10):
        s = input('start')
        e = input('end')
        print(p1.book_slot(s, e))
        print(p1.get_empty_slots())


if __name__ == '__main__':
    main()