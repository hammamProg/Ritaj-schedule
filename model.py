import json


class Course:
    def __init__(self,title,start_end_time:list,isLab,days,instructor,slot_color) -> None:
        self.title = title
        self.start_end_time = start_end_time # [start: Hour,Min],[end: Hour,Min]
        self.days = days
        self.instructor = instructor
        self.slot_color = slot_color
        self.isLab = isLab

    def __str__(self):
        lab_text = "Lab" if self.isLab else "Lecture"
        days_text = ", ".join(self.days)
        return f"Course: {self.title}\nType: {lab_text}\nTime: {self.start_end_time}\nDays: {days_text}\nInstructor: {self.instructor}\nSlot Color: {self.slot_color}"

     
    