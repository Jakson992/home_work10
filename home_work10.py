from collections import UserDict
import re


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.__class__.__name__}: {self.value}"


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name can not be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    def validate(self):
        if not re.match(r"^\+?\d{9,15}$", self.value):
            raise ValueError("Invalid phone number")

    def __str__(self):
        return f"{self.__class__.__name__}: {self.value}"


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        phone_obj.validate()
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                p.validate()
                return True
        return False

    def __str__(self):
        return f"{self.name}\n{', '.join(str(p) for p in self.phones)}"


my_contacts = {}


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Contact with that name not found."
        except ValueError:
            return "Please enter a valid command."
        except IndexError:
            return "Please enter both name and phone number, separated by a space."

    return wrapper


@input_error
def hello(*args):
    return "How can I help you?"


@input_error
def add(*args):
    _, name, phone = args[0].split()
    record = Record(name)
    record.add_phone(phone)
    my_contacts[name] = record
    return f"Contact {name} with phone {phone} has been added."


@input_error
def change(*args):
    _, name, phone = args[0].split()
    if name in my_contacts:
        record = my_contacts[name]
        record.edit_phone(record.phones[0].value, phone)
        return f"Phone number for contact {name} changed."
    else:
        return f"Contact with name {name} not found."


@input_error
def phone(*args):
    _, name = args[0].split()
    if name in my_contacts:
        return f"Phone number for contact {name} is {my_contacts[name]}."
    else:
        return f"Contact with name {name} is not defined."


@input_error
def show_all(*args):
    if my_contacts:
        contacts_str = ""
        for name, record in my_contacts.items():
            contacts_str += f"{record}\n"
        return contacts_str
    else:
        return "You have no contacts."


@input_error
def exit(*args):
    return "Goodbye!"


COMMANDS = {
    hello: "hello",
    add: "add",
    change: "change",
    phone: "phone",
    show_all: "show all",
    exit: "exit"
}


def command_handler(text):
    for command, keywords in COMMANDS.items():
        if text.lower().startswith(keywords):
            return command, text
    return None, ''


def main():
    while True:
        user_input = input('>>> ')
        command, data = command_handler(user_input)
        if not command:
            print("Unknown command, try again.")
            continue
        print(command(data))
        if command == exit:
            break


if __name__ == '__main__':
    main()
