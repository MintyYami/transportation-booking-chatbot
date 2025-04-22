from datetime import datetime
import re
from util import util_func


# class to manage a reservation
class Reservation:
    # initialise all booking information as None
    def __init__(self, transport_types):
        # set up data for reservation
        self.transport_types = transport_types
        self.data = {
            'name': "",
            'transport': "",
            'date': "",
            'time': "",
            'email': ""
        }
        # set reservation tracker
        self.completed = False
        self.steps_to_complete = len(self.data)

    # set name
    def set_name(self, name, respond):
        # check only one name is given
        if len(name.split(" ")) > 1:
            if respond:
                print("\n>> Input name error: Please only enter your first name for the booking")
            return False
        # check name is appropriate
        if not isinstance(name, str) or util_func.is_swear(name):
            if respond:
                print("\n>> Input name error: Please enter a valid name")
            return False

        self.data['name'] = name
        return True

    # set transportation
    def set_transport(self, transport, respond):
        # check transport is in list of available types
        if transport not in self.transport_types:
            if respond:
                print("\n>> Input transport error: Unknown transport type")
                print(f">> List of available transportation type:")
                for type in self.transport_types:
                    print(f"    - {type}")
            return False

        self.data['transport'] = transport
        return True

    # set date with format DD/MM/YYYY
    def set_date(self, date, respond):
        # check date formatting is correct
        if len(date.split("/")) != 3:
            if respond:
                print("\n>> Input data error: Please provide a date in the correct format (DD/MM/YYYY)")
            return False
        day, month, year = date.split("/")
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            if respond:
                print("\n>> Input data error: Please provide a numbered date in the format DD/MM/YYYY")
            return False

        # check date validity
        try:
            datetime.strptime(date, "%d/%m/%Y")
        except:
            if respond:
                print("\n>> Input date error: Please ensure the date given is valid, and in the format DD/MM/YYYY")
            return False
        if datetime.strptime(date, "%d/%m/%Y") < datetime.now():
            if respond:
                print("\n>> Input date error: Reservation date must be from tomorrow onwards")
            return False
        if datetime.strptime(date, "%d/%m/%Y") > datetime.strptime(f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year + 1}", "%d/%m/%Y"):
            if respond:
                print("\n>> Input date error: Reservation date cannot be more than a year in advance")
            return False

        self.data['date'] = date
        return True

    # set time with format HH:MM
    def set_time(self, time, respond):
        # check time formatting
        if len(time.split(":")) != 2:
            if respond:
                print("\n>> Reservation time error: Please provide a time in the correct format (HH:MM)")
            return False
        hour, minute = time.split(":")
        if not (hour.isdigit() and minute.isdigit()):
            if respond:
                print("\n>> Reservation time error: Please only provide numbers in your time. Remember that the time should be in HH:MM format.")
            return False
        if len(hour) > 2 or len(minute) != 2:
            if respond:
                print("\n>> Reservation time error: Please provide a time in the format HH:MM")
            return False

        # check time validity
        hour = int(hour)
        minute = int(minute)
        if (hour < 0 or hour > 23 or minute < 0 or minute > 59):
            if respond:
                print("\n>> Reservation time error: Please ensure the time given is valid")
            return False

        # ensure time is in HH:MM format
        if len(str(hour)) == 1:
            time = "0"+time
        self.data['time'] = time
        return True

    # set email
    def set_email(self, email, respond):
        # check email formatting
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z.]{2,}", email):
            if respond:
                print("\n>> Reservation email error: Please provide valid email address")
            return False

        self.data['email'] = email
        return True

    # set data to the correct type of information
    def set_data(self, data_type, data, respond):
        match data_type:
            case "name":
                return self.set_name(data, respond)
            case "transport":
                return self.set_transport(data.lower(), respond)
            case "date":
                return self.set_date(data, respond)
            case "time":
                return self.set_time(data, respond)
            case "email":
                return self.set_email(data, respond)
        return False

    # update variable if completed
    def update_completed(self):
        for information in self.data:
            if information == "":
                self.completed = False
                return False
        # change completed to true if all data is filled
        self.completed = True
        return True

    # get the number of data that has been entered in the reservation
    def get_steps(self):
        steps = 0
        for key in self.data:
            if self.data[key] != "":
                steps += 1
        return steps

    # get (if any) conversational markers, and whether the marker changes the sentence
    def get_marker(self):
        # conversational marker: first step
        steps = self.get_steps()
        if steps == 0:
            return "Firstly, ", True
        # conversational marker: halfway mark
        if self.steps_to_complete % 2 == 0:
            if steps == (self.steps_to_complete // 2):
                return "You're halfway done with the reservation! ", False
        else:
            if steps == (self.steps_to_complete // 2) + 1:
                return "Over halfway done! ", False
        # conversational marker: last step
        if steps == (self.steps_to_complete - 1):
            return "And lastly, ", True
        return "", False