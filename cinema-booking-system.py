import string
import sys

class CinemaBookingSystem:
    def __init__(self, title, rows, seats_per_row):
        self.title = title
        self.rows = min(rows, 26)  
        self.seats_per_row = min(seats_per_row, 50) 
        self.seating = {row: ['.'] * self.seats_per_row for row in string.ascii_uppercase[:self.rows]}
        self.bookings = {}
        self.booking_counter = 1

    # Game logic methods for the system

    def display_menu(self):
        while True:
            available_seats = sum(row.count('.') for row in self.seating.values())
            print(f"\nWelcome to GIC Cinemas")
            print(f"[1] Book tickets for {self.title} ({available_seats} seats available)")
            print("[2] Check bookings")
            print("[3] Exit")
            choice = input("Please enter your selection:\n> ")
            
            if choice == '1':
                self.book_tickets()
            elif choice == '2':
                self.check_bookings()
            elif choice == '3':
                print("Thank you for using GIC Cinemas system. Bye!")
                sys.exit()
            else:
                print("Invalid selection. Please try again.")

    def book_tickets(self):
        while True:
            num_tickets = input("\nEnter number of tickets to book, or enter blank to go back to main menu:\n> ")

            if num_tickets == "":
                return

            if not num_tickets.isdigit() or int(num_tickets) <= 0:
                print("Invalid input. Enter a valid number.")
                continue
            
            num_tickets = int(num_tickets)
            available_seats = sum(row.count('.') for row in self.seating.values())
            if num_tickets > available_seats:
                print(f"Sorry, there are only {available_seats} seats available.")
                continue
            
            booking_id = f"GIC{self.booking_counter:04}"
            self.booking_counter += 1

            seats = self.allocate_default_seats(num_tickets)
            self.bookings[booking_id] = seats
            print(f"\nSuccessfully reserved {num_tickets} {self.title} tickets.")
            print(f"Booking id: {booking_id}")
            print("Selected seats:")
            self.display_seating(seats)

            while True:
                new_position = input("\nEnter blank to accept seat selection, or enter new seating position:\n> ")
                if new_position == "":
                    print(f"\nBooking id: {booking_id} confirmed.")
                    return

                # revert previously reserved seats to make way for new ones 
                # in case of clashes
                for row, seat in self.bookings[booking_id]:
                    self.seating[row][seat - 1] = '.'

                if self.manual_allocate_seats(booking_id, new_position.upper(), num_tickets):
                    print(f"\nBooking id: {booking_id}")
                    print("Selected seats:")
                    self.display_seating(self.bookings[booking_id])
                else:
                    print("Invalid position. Try again.")
       
    def allocate_default_seats(self, num_tickets, starting_row="A"):
        start_allocation = False
        allocated_seats = []
        
        for row in self.seating: 
            if row == starting_row:
                start_allocation = True

            if start_allocation is False:
                continue
    
            if num_tickets == 0:
                break
                
            empty_seats_in_row = [i for i, seat in enumerate(self.seating[row]) if seat == '.']

            if empty_seats_in_row:
                while empty_seats_in_row and num_tickets > 0:
                    closest_to_mid_index = self.find_closest_to_middle_col(empty_seats_in_row)
                    empty_seats_in_row.remove(closest_to_mid_index)
                    self.seating[row][closest_to_mid_index] = '#'
                    allocated_seats.append((row, closest_to_mid_index + 1))
                    num_tickets -= 1

        return allocated_seats
        
    def manual_allocate_seats(self, booking_id, start_position, num_tickets):
        row_letter, seat_num = start_position[0], start_position[1:]
        if row_letter not in self.seating or not seat_num.isdigit():
            return False
        seat_num = int(seat_num)
        if seat_num < 1 or seat_num > self.seats_per_row:
            return False
        
        seat_index = seat_num-1
        available_seats = self.count_available_seats(self.seating, row_letter, seat_index)
        if available_seats < num_tickets:
            return False

        row_index = list(self.seating.keys()).index(row_letter)
        allocated_seats = []

        # allocate empty seats from a starting position in specified row 
        for i in range(seat_num - 1, self.seats_per_row):    
            if self.seating[row_letter][i] == '.' and num_tickets > 0:
                self.seating[row_letter][i] = '#'
                allocated_seats.append((row_letter, i + 1))
                num_tickets -= 1

        # allocate default seats for tickets that can't fit in same row
        # from the next row onwards
        if num_tickets > 0:
            allocated_seats += self.allocate_default_seats(num_tickets, self.next_capital_letter(row_letter))
        
        self.bookings[booking_id] = allocated_seats
        return True

    def display_seating(self, selected_seats=None):
        print("\n          S C R E E N")
        print("--------------------------------")
        for row in reversed(self.seating):
            row_display = ["o" if (row, i + 1) in selected_seats else seat for i, seat in enumerate(self.seating[row])]
            print(row, " ".join(row_display))
        print(" ", " ".join(str(i + 1) for i in range(self.seats_per_row)))
            
    def check_bookings(self):
        while True:
            booking_id = input("\nEnter booking id, or enter blank to go back to main menu:\n> ")
            if booking_id == "":
                return
            if booking_id in self.bookings:
                print(f"\nBooking id: {booking_id}")
                print("Selected seats:")
                self.display_seating(self.bookings[booking_id])
            else:
                print("Invalid booking id. Try again.")

    # Helper methods for the system

    def count_available_seats(self, seating, start_row, start_seat):
        count = 0
        rows = list(seating.keys())  
        start_index = rows.index(start_row)  
        
        for i in range(start_index, len(rows)): 
            row = rows[i]
            if i == start_index:
                count += seating[row][start_seat:].count('.')  
            else:
                count += seating[row].count('.') 
                
        return count

    def find_closest_to_middle_col(self, numbers):
        if not numbers:
            return None 
        
        min_value, max_value = min(numbers), max(numbers)
        middle = (min_value + max_value) / 2
        closest = min(numbers, key=lambda x: abs(x - middle))
        
        return closest

    def next_capital_letter(self, letter):
        if letter == 'Z':
            return 'A'  
        if 'A' <= letter < 'Z':
            return chr(ord(letter) + 1)
        raise ValueError("Input must be a capital letter (A-Z)")

if __name__ == "__main__":
    while True:
        user_input = input("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n> ")
        parts = user_input.split()
        if len(parts) < 3 or not parts[-2].isdigit() or not parts[-1].isdigit():
            print("Invalid format. Try again.")
            continue
        title = " ".join(parts[:-2])
        rows, seats_per_row = int(parts[-2]), int(parts[-1])
        if rows < 1 or seats_per_row < 1:
            print("Rows and seats per row must be at least 1.")
            continue
        break

    system = CinemaBookingSystem(title, rows, seats_per_row)
    system.display_menu()
