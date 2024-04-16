from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def is_valid(phone_number):
        return len(phone_number) == 10 and phone_number.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        if not Phone.is_valid(new_phone):
            raise ValueError("Invalid phone number format")
        for idx, phone in enumerate(self.phones):
            if str(phone) == old_phone:
                self.phones[idx] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        info = f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
        if self.birthday:
            info += f", birthday: {self.birthday.value}"
        return info

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today()
        for record in self.data.values():
            if record.birthday:
                birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                next_birthday_year = today.year if today.month < birthday_date.month or (today.month == birthday_date.month and today.day <= birthday_date.day) else today.year + 1
                next_birthday = datetime(next_birthday_year, birthday_date.month, birthday_date.day)
                days_until_birthday = (next_birthday - today).days
                if days_until_birthday <= 7 and days_until_birthday >= 0:
                    upcoming_birthdays.append((record, days_until_birthday))
        return upcoming_birthdays

def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

def change_phone(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        old_phones = [str(p) for p in record.phones]
        record.edit_phone(old_phones[0], phone)
        return f"Phone number updated for {name}"
    else:
        return f"Contact {name} not found"

def show_all(book):
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "Address book is empty"

def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record and record.phones:
        return f"{name}'s phone number: {', '.join(str(p) for p in record.phones)}"
    elif record and not record.phones:
        return f"No phone number set for {name}"
    else:
        return f"Contact {name} not found"

def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        return f"Contact {name} not found"

def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    elif record and not record.birthday:
        return f"No birthday set for {name}"
    else:
        return f"Contact {name} not found"

def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{record.name.value}'s birthday in {days+1} days" for record, days in upcoming_birthdays])
    else:
        return "No upcoming birthdays"

def parse_input(user_input):
    return user_input.split(None, 2)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
