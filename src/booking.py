from util import util_func, util_text_process
from reservation_management import Reservation
import sqlite3

# INTENT MATCHING: check if user is trying to book a transportation
def check(user_input):
    id, content, confidence = util_text_process.process_query_with_matrix(user_input.lower(), "booking", ".csv", 0.75)

    if (id != None):
        return content["AnswerID"].iloc[id], confidence

    return None, 0

# starts transaction for transportation booking
def startTransaction(user_input, name):
    transport_types = ["xl taxi", "taxi", "train", "coach"]

    print("\n>> Start Transportation Reservation")
    print("   Please only type the prompted response, and nothing more!")
    print("   Type \"cancel\" to cancel this reservation at any time.")
    reservation = Reservation(transport_types)

    # set name for reservation if name is set
    if name != None:
        reservation.set_data("name", name, False)
        print("\n>> Name detected: ")
        print(f">> Reservation information added: name - {name}")

    # set possible transportation type from initial input
    for transport in transport_types:
        if transport in user_input.lower():
            reservation.set_data("transport", transport, False)
            print("\n>> Transportation detected: ")
            print(f">> Reservation information added: transport - {transport}")

    # set possible date from initial input
    for word in user_input.split():
        if reservation.set_data("date", word, False):
            print("\n>> Date detected: ")
            print(f">> Reservation information added: date - {word}")
            break

    # set possible time from initial input
    for word in user_input.split():
        if reservation.set_data("time", word, False):
            print("\n>> Time detected: ")
            print(f">> Reservation information added: time - {word}")
            break

    # set possible time from initial input
    for word in user_input.split():
        if reservation.set_data("email", word, False):
            print("\n>> Email detected: ")
            print(f">> Reservation information added: email - {word}")
            break

    # find any missing data for information
    for key in reservation.data:
        if reservation.data[key] == "":
            while True:
                # information prompt
                prompt = f"What is the {key} for the reservation?"
                # check for timeline conversational marker, and whether the marker starts the sentence
                marker, stater = reservation.get_marker()
                if stater:
                    prompt = prompt.lower()
                prompt = marker + prompt
                # print the prompt
                print("\nHadley: " + prompt)

                # get user input for missing data
                new_input = util_func.get_input(name)

                # check cancellation
                if new_input.lower() == "cancel":
                    print("Hadley: Are you sure you want to cancel the reservation? This action cannot be undone. (y/n)")

                    check_cancel = util_func.get_confirmation(name)
                    if isinstance(check_cancel, bool) and check_cancel:
                        cancel_reservation()
                        return False
                    continue

                # try to set data to reservation
                if reservation.set_data(key, new_input, True):
                    print(f"\n>> Reservation information added: {key} - {reservation.data[key]}")
                    # break from loop
                    break

            # update reservation to check if all data is filled
            reservation.update_completed()

    # ask for confirmation
    print("Hadley: All information entered successfully!\n")
    for key in reservation.data:
        print(f"        {key}: {reservation.data[key]}")
    print("\nHadley: Please confirm that this information is correct. (y/n)")
    print("        Note that the reservation will have discarded if confirmation not approved")
    if util_func.get_confirmation(name):
        # Save reservation into a database
        id = save_reservation(reservation)
        if id != None:
            print(f"\nHadley: Your reservation for {reservation.data["transport"]} is successfully recorded!")
            print(f"        Your reservation ID is {id:04}. Please note this down, as it will be needed to access your reservation later!")
            return True
        return False
    cancel_reservation()
    return False

# visible marker for transaction cancellation
def cancel_reservation():
    print("\n>> Reservation cancelled")
    print(">> Switching out of reservation system...")
    print("\nHadley: I have successfully cancelled your reservation. If you want to start another reservation, just let me know!")

# save reservation to database
def save_reservation(reservation):
    # double check that all reservation information is present
    if not reservation.update_completed():
        print(
            "\n>> Unexpected error occurred: Missing information in the reservation prevents its ability to be saved.")
        return None

    print("\n>> Reservation saving in progress, please do not close the program...")

    # connect to database
    conn = sqlite3.connect("data/database.db")
    c = conn.cursor()

    # create table if table doesn't exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            transport TEXT,
            date TEXT,
            time TEXT,
            email TEXT
        );
    """
    c.execute(create_table_query)

    # save reservation
    insert_query = """
        INSERT INTO reservations (name, transport, date, time, email)
        VALUES (?, ?, ?, ?, ?);
    """
    c.execute(insert_query, (reservation.data["name"], reservation.data["transport"],
                             reservation.data["date"], reservation.data["time"], reservation.data["email"]))

    # commit changes
    conn.commit()
    id = c.lastrowid
    conn.close()

    print(">> Reservation saving completed.")
    return id

# view transaction for transportation booking
def viewTransaction(user_input, name):
    print("\n>> Start Reservation Viewing")
    print("   Please only type the prompted response, and nothing more!")
    print("   Type \"cancel\" to cancel this reservation at any time.\n")

    # check if name is set
    if name != None:
        print(">> Name detected: ")
        print(f">> Reservation information: name - {name}\n")
    # check for possible reservation value from initial input
    reservation_id = check_reservationID(user_input)
    if reservation_id != None:
        print(">> Reservation ID detected: ")
        print(f">> Reservation information: name - {reservation_id}\n")

    # get name if not set
    if name == None:
        print("Hadley: Can I please get your name for this reservation?")
    while name == None:
        # get user input for missing data
        name = util_func.get_input(name)

        # check cancellation
        if name.lower() == "cancel":
            print("Hadley: Are you sure you want to cancel? This action cannot be undone. (y/n)")

            check_cancel = util_func.get_confirmation(name)
            if isinstance(check_cancel, bool) and check_cancel:
                cancel_reservation_view()
                return False
            print("Hadley: Can I please get your name for this reservation?")
            continue

        # prompt to get reservation name
        if name == None:
            print("Hadley: Sorry, I didn't quite get that. Please try again.")
            print("        What is the name for the reservation?")

    # get ID if not set
    if reservation_id == None:
        print("Hadley: Can I please get your reservation ID?")
    while reservation_id == None:
        # get user input for missing data
        user_input = util_func.get_input(name)

        # check cancellation
        if user_input.lower() == "cancel":
            print("Hadley: Are you sure you want to cancel? This action cannot be undone. (y/n)")

            check_cancel = util_func.get_confirmation(name)
            if isinstance(check_cancel, bool) and check_cancel:
                cancel_reservation_view()
                return False
            print("Hadley: Can I please get your reservation ID?")
            continue

        # prompt to get reservation ID
        reservation_id = check_reservationID(user_input)
        if reservation_id == None:
            print("Hadley: Sorry, Please ensure your reservation ID is in the correct four digit format.")
            print("        What is the reservation ID for your booking?")

    # try to get reservation
    # connect to database
    conn = sqlite3.connect("data/database.db")
    c = conn.cursor()

    select_query = """
        SELECT * FROM reservations
        WHERE id = ? AND name = ?
    """

    c.execute(select_query, (reservation_id, name))
    reservation = c.fetchone()
    # return false if reservation not found
    if not reservation:
        print("Hadley: Sorry! No reservation found for the reservation name and ID given...")
        return False
    # print reservation information if found
    fields = ['id', 'name', 'transport', 'date', 'time', 'email']
    reservation_data = dict(zip(fields, reservation))
    print("Hadley: I found your reservation information!")
    print("\n>> Reservation information:")
    for field, value in reservation_data.items():
        if field == "id":
            print(f">> {field}: {value: 04}")
        else:
            print(f">> {field}: {value}")
    return True

# visible marker for transaction viewing cancellation
def cancel_reservation_view():
    print("\n>> Reservation viewing cancelled")
    print(">> Switching out of reservation system...")
    print("\nHadley: I have successfully cancelled your reservation viewing. If you want to view another reservation, just let me know!")

# ensure reservation format is correct
def check_reservationID(user_input):
    for word in user_input.split():
        if word.isdigit() and (len(word) == 4):
            return word
    return None