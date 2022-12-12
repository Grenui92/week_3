from collections import UserDict
from datetime import date, timedelta
from pickle import dump, load
import os
from contact_book.classes.class_record import Record, Birthday


class ContactBook(UserDict):

    __instance = None

    def __new__(cls):
        if not isinstance(cls.__instance, cls):
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, file_path=os.path.join("contact_book")):
        super().__init__()
        self.file_path = f"{file_path}.bin"

    def create_new_contact(self, name: str) -> str:
        if name in self.data.keys():
            return f"Contact with name {name} already exist. Try another name."
        elif not name:
            return "You can't create empty name contact."
        else:
            self.data[name] = Record(name)
            return f"Contact {name} successfully created."

    def show_all_contacts(self) -> list:
        result = []
        for k, v in self.data.items():
            result.append(f"Contact {k} has information:\n"
                          f"\tphones: {[num.value for num in v.phones] if v.phones else v.phones}\n"
                          f"\temails: {[mail.value for mail in v.emails] if v.emails else v.emails}\n"
                          f"\taddress: {[adr.value for adr in v.address] if v.address else v.address}\n"
                          f"\tbirthday: {v.birthday.value if isinstance(v.birthday, Birthday) else v.birthday}\n")
        return result

    def show_upcoming_birthdays(self, n=7) -> list:
        result = []
        for k, v in self.data.items():
            if isinstance(v.birthday, Birthday):
                # Проверяем произошел ли День Рождения в этом году, но ДО сегодняшней даты, или еще предстоит в этом году. Если уже произошел в
                # этом году, то добавляем еще один год
                next_birthday = date(year=date.today().year, month=v.birthday.value.month, day=v.birthday.value.day)
                if next_birthday - date.today() <= timedelta(0):
                    next_birthday = date(year=date.today().year+1, month=v.birthday.value.month, day=v.birthday.value.day)
                # Проверяем входит ли дата следующего дня рождения в ближайште Н дней
                if next_birthday - date.today() < timedelta(n):
                    result.append(f"{k} birthday in {v.birthday.value}.")
        return result

    def days_to_birthdays_all_contacts(self) -> list:
        result = []
        for k, v in self.data.items():
            if isinstance(v.birthday, str):
                result.append(f"Days to {v.name.value}'s birthday UNKNOWN.")
            else:
                next_birthday = date(year=date.today().year, month=v.birthday.value.month, day=v.birthday.value.day)
                if next_birthday - date.today() <= timedelta(0):
                    next_birthday = date(year=date.today().year + 1, month=v.birthday.value.month, day=v.birthday.value.day)
                result.append(f"Days to {v.name.value}'s birthday {(next_birthday - date.today()).days}.")
        return result

    def search_contact(self, name: str) -> str:
        if name in self.data.keys():
            v = self.data[name]
            return f"Contact {name} has information:\n" \
                     f"\tphones: {[num.value for num in v.phones] if v.phones else v.phones}\n" \
                     f"\temails: {[mail.value for mail in v.emails] if v.emails else v.emails}\n" \
                     f"\taddress: {[adr.value for adr in v.address] if v.address else v.address}\n" \
                     f"\tbirthday: {v.birthday.value if isinstance(v.birthday, Birthday) else v.birthday}\n"
        else:
            return f"I can't find name '{name}' in contact book"

    def search_in_all_contact_information(self, search: str) -> list:
        result = []
        for key, record in self.data.items():
            if search in key:
                result.append(f"Combination {search} find in contact name {key}.")
            for number in record.phones:
                if search in number.value:
                    result.append(f"Combination {search} find in telephone number {number.value} named {key}.")
            for email in record.emails:
                if search in email.value:
                    result.append(f"Combination {search} find in email {email.value} named {key}.")
            for address in record.address:
                if search in address.value:
                    result.append(f"Combination {search} find in address {address.value} named {key}.")
        return result

    def edit_contact(self, old_name: str, new_name: str) -> str:
        if old_name == new_name:
            return f"Old name ({old_name}) == New name ({new_name}). I don't understand."
        else:
            self.data[old_name].name.value = new_name
            self.data[new_name] = self.data[old_name]
            del self.data[old_name]
            return f"Old name {old_name} successfully changed to {new_name}."

    def save_to_file(self) -> str:
        with open(self.file_path, "wb") as file:
            dump(self.data, file)
        return f"Successfully save ContactBook to file {self.file_path}"

    def load_from_file(self) -> str:
        with open(self.file_path, "rb") as file:
            self.data = load(file)
        return f"Successfully load ContactBook from file {self.file_path}"

    def clear_all_book(self) -> str:
        self.data.clear()
        return "Book is clear."

