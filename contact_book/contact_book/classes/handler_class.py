from contact_book.classes.class_contact_book import ContactBook
from contact_book.classes.class_notes import NoteBook
from contact_book.classes.file_checker import FileSorter
from contact_book.classes.decorators import bug_catcher
from os import path


class Handler:
    def __init__(self):
        self.book = ContactBook()
        self.notes = NoteBook()
        try:
            self.book.load_from_file()
            self.notes.load_from_file()
        except FileNotFoundError:
            self.book.save_to_file()
            self.notes.save_to_file()

        self.commands = {"help": self.__help_me,
                         "instruction": self.__instructions,

                         "create": self.__create_contact,
                         "add_phone": self.__add_phone_to_contact,
                         "add_email": self.__add_email_to_contact,
                         "add_address": self.__add_address_to_contact,
                         "set_birthday": self.__set_birthday,
                         "show_birthdays": self.__show_nearest_birthdays,
                         "days_to": self.__days_to_birthday,
                         "birthday_for_all": self.__days_to_birthday_for_all,
                         "edit_contact": self.__edit_contact_information,
                         "edit_name": self.__edit_name,
                         "search": self.__search_contact,
                         "search_info": self.__search_in_all_information,
                         "show": self.__show_contacts,
                         "clear_book": self.__clear_book,

                         "create_note": self.__create_note,
                         "add_note": self.__add_note_information,
                         "clear_note": self.__clear_one_note,
                         "clear_tags": self.__clear_tags,
                         "clear_text": self.__clear_text,
                         "delete_note": self.__del_one_note,
                         "search_in_text": self.__search_in_text,
                         "search_in_tags": self.__search_in_tags,
                         "sorted_by_tags": self.__sorted_by_tags,
                         "show_note": self.__show_one_note,
                         "show_note_book": self.__show_note_book,

                         "file_sorter": self.__file_sorter,

                         "exit": self.__good_bye}

    def main(self):
        while True:
            print("\nCommand 'help' will help you.")
            data = self.__input_user_text()
            command, name, data = self.__parse_user_text(data)
            result = self.__handler(command, name, data)
            self.__show_results(result)

    """MAIN"""

    @staticmethod
    @bug_catcher
    def __parse_user_text(text: str) -> list:
        """Search command and other information in user input."""

        data = text.split()
        if len(data) == 1:
            command, name, information = data[0], "", ""
        else:
            command = data[0]
            name = data[1]
            information = data[2:]
        return [command, name, information]

    @bug_catcher
    def __handler(self, command: str, name: str, data: list) -> str | list:
        """Here we find signatures and call functions"""
        if command in self.commands:
            return self.commands[command](name, data)
        else:
            raise Warning(command)

    @staticmethod
    @bug_catcher
    def __input_user_text() -> str:
        """User input."""
        data = input("Please enter what do you want to do: ")
        return data

    @staticmethod
    @bug_catcher
    def __show_results(result: str | list):
        """Print all results and information which functions return to us."""
        if isinstance(result, list):
            for row in result:
                print(row)
        else:
            print(result)

    @bug_catcher
    def __good_bye(self, *_):
        print(self.book.save_to_file())
        print(self.notes.save_to_file())
        exit("Bye")

    """END MAIN"""

    """CONTACT BOOK"""

    @bug_catcher
    def __create_contact(self, name: str, *_) -> str:
        return self.book.create_new_contact(name)

    @bug_catcher
    def __add_phone_to_contact(self, name: str, data: list) -> str:
        record = self.book[name]  # Check if this record exists
        return record.add_phone(data[0])

    @bug_catcher
    def __add_email_to_contact(self, name: str, data: list) -> str:
        record = self.book[name]  # Check if this record exists
        return record.add_email(data[0])

    @bug_catcher
    def __add_address_to_contact(self, name: str, data: list) -> str:
        record = self.book[name]  # Check if this record exists
        return record.add_address(" ".join(data))

    @bug_catcher
    def __set_birthday(self, name: str, data: list) -> str:
        record = self.book[name]  # Check if this record exists
        return record.set_birthday(data[0])

    @bug_catcher
    def __edit_contact_information(self, name: str, data: list) -> str:
        record = self.book[name]  # Check if this record exists
        field, old, new = data[0], data[1], data[2]
        return record.edit_contact_information(field, old, new)

    @bug_catcher
    def __edit_name(self, old_name: str, new_name: list) -> str:
        return self.book.edit_contact(old_name, new_name[0])

    @bug_catcher
    def __search_contact(self, name, *_) -> str:
        return self.book.search_contact(name)

    @bug_catcher
    def __search_in_all_information(self, name: str, data: list) -> list:
        data = " ".join(
            [name, *data])  # In function handler() all our functions take in 2 arguments, so all our other functions will take in 2 argument
        # and if we need to transform data type - we can do it in every function where we need it
        return self.book.search_in_all_contact_information(data)

    @bug_catcher
    def __show_nearest_birthdays(self, days: str, *_) -> list:
        """Here we call information about birthdays which will happen within the next DAYS days.
        If DAYS argument is empty - default DAYS in show_upcoming_birthday() == 7"""

        if days:
            n = int(days)  # Check isinstance(days, int) and also our class method waiting for type(int)
            return self.book.show_upcoming_birthdays(n=n)
        else:
            return self.book.show_upcoming_birthdays()

    @bug_catcher
    def __days_to_birthday(self, name: str, *_) -> str:
        record = self.book[name]  # Check if this record exists
        return record.days_to_birthday()

    @bug_catcher
    def __days_to_birthday_for_all(self, *_) -> list:
        return self.book.days_to_birthdays_all_contacts()

    @bug_catcher
    def __show_contacts(self, *_) -> list:
        return self.book.show_all_contacts()

    @bug_catcher
    def __clear_book(self, *_) -> str:
        answer = input("You want to delete all your contacts. Are you sure? Y/N: ")
        if answer == "Y":
            return self.book.clear_all_book()
        else:
            return "Operation 'delete all contacts' canceled."

    """END CONTACTBOOK"""

    """NOTEBOOK"""

    @bug_catcher
    def __create_note(self, name: str, info: list) -> str:
        return self.notes.create_new_note(name, info)

    @bug_catcher
    def __add_note_information(self, name, info):
        return self.notes.add_note(name, info)

    @bug_catcher
    def __clear_one_note(self, name, *_):
        return self.notes.clear_note(name)

    @bug_catcher
    def __clear_tags(self, name, *_):
        return self.notes.clear_tags(name)

    @bug_catcher
    def __clear_text(self, name, *_):
        return self.notes.clear_text(name)

    @bug_catcher
    def __del_one_note(self, name, *_):
        return self.notes.del_note(name)

    @bug_catcher
    def __search_in_text(self, text, *_):
        return self.notes.search_in_text(text)

    @bug_catcher
    def __search_in_tags(self, tags, *_):
        return self.notes.search_in_tags(tags)

    @bug_catcher
    def __sorted_by_tags(self, name, info):
        final_info = [name, *info]
        return self.notes.sort_by_tags(final_info)

    @bug_catcher
    def __show_one_note(self, name, *_):
        return self.notes.show_note(name)

    @bug_catcher
    def __show_note_book(self, *_):
        return self.notes.show_all()

    """END NOTEBOOK"""

    """FILE SORTER"""

    @staticmethod
    @bug_catcher
    def __file_sorter(path_for_sorting, *_):
        one_time = FileSorter(path_for_sorting)
        one_time.job()

    """END FILE SORTER"""

    """HELP and FINAL"""

    @staticmethod
    @bug_catcher
    def __help_me(*_):
        return "If you want to know how to use this script - use command 'instruction' with:\n" \
               "'contacts' - to read about ContactBook commands.\n" \
               "'notes' - to read about NoteBook.\n" \
               "'file' - to read about FileSorter."

    @staticmethod
    @bug_catcher
    def __instructions(category, *_):
        if category == "contacts":
            main_path = path.join("instructions", "contact_book.txt")
        elif category == "notes":
            main_path = path.join("instructions", "note_book.txt")
        elif category == "file":
            main_path = path.join("instructions", "file_sorter.txt")
        else:
            raise ValueError(f"I can't find instruction for {category}.")
        with open(main_path, "r") as file:
            result = file.read()
        return result

    """END HELP an FINAL"""

if __name__ == "__main__":
    free_man = Handler()
    free_man.main()
