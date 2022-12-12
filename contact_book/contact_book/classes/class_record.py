import re
from datetime import date, timedelta


class Record:
    """Contain all information about contact"""

    def __init__(self, name, phone=None, email=None, address=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.emails = [Email(email)] if email else []
        self.address = [Address(address)] if address else []
        self.birthday = Birthday(birthday) if birthday else "Birthday not set"

    def add_phone(self, phone: str) -> str:
        self.phones.append(Phone(phone))
        return f"Phone number {phone} successfully added to contact: {self.name.value}"

    def add_email(self, email: str) -> str:
        self.emails.append(Email(email))
        return f"Email {email} successfully added to contact: {self.name.value}"

    def add_address(self, address: str) -> str:
        """Add one more address to the Record address list."""
        self.address.append(Address(address))
        return f"Address {address} successfully added to contact {self.name.value}"

    def set_birthday(self, date_b: str) -> str:
        self.birthday = Birthday(date_b)
        return f"Date {date_b} successfully set as birthday for contact {self.name.value}"

    def edit_contact_information(self, field: str, old: str, new: str) -> str:
        point = self.__dict__[field]
        if field == "phones":
            old_phone = Phone(old).value
        for entry in point:
            if old == entry.value:
                entry.value = new
                return f"{old} successfully changed to {new}"
        raise KeyError(f"I can't find old value {old}")

    def days_to_birthday(self):
        next_birthday = date(year=date.today().year, month=self.birthday.value.month, day=self.birthday.value.day)
        if next_birthday - date.today() <= timedelta(0):
            next_birthday = date(year=date.today().year + 1, month=self.birthday.value.month, day=self.birthday.value.day)
        return f"Days to {self.name.value}'s birthday {(next_birthday - date.today()).days}."


class Field:
    """Class for setting values in other fields of Record."""

    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Email(Field):

    @Field.value.setter
    def value(self, value):
        data = re.findall(r"^[a-zA-Z][a-zA-Z1-9._]+@[a-z.]+[a-z]{2,3}$", value)
        if data:
            self._value = data[0]
        else:
            raise ValueError(f"Email {value} incorrect.")


class Phone(Field):
    """Contain ONE phone number. Instance fo this class stored in Record.phones."""

    @Field.value.setter
    def value(self, value):
        data = re.findall(r"[+]{1}\d{12}|[+]{1}38.\d{3}.\d{3}-\d{2}-\d{2}|[+]{1}38-\d{5}-\d{2}-\d{2}-\d", value)
        if data:
            data = re.findall(r"\d+", data[0])
            self._value = "+"+"".join(data)
        else:
            raise ValueError(f"Incorrect number {value}. Please enter the number in th format\n"
                             f"+AA-YYY-XXX-XX-XX or +AAYYYXXXXXXX or +AA-YYYYY-XX-XX-X\n"
                             f"where A = country code, Y = operator/city code, X = phone numbers.")


class Birthday(Field):
    """Contain ONE birthday date. Instance stored in Record.birthday."""

    @Field.value.setter
    def value(self, new_value: str):
        try:
            parsed_data = re.findall(r"\d+", new_value)
            new_value = [int(i) for i in parsed_data]
            birthday_date = date(*new_value)
        except ValueError:
            raise ValueError("Incorrect date format. Expected only numbers in the format yyyy.mm.dd")
        except TypeError:
            raise TypeError("Incorrect date format. Expected only numbers in the format yyyy.mm.dd")

        if birthday_date <= date.today():
            self._value = birthday_date
        else:
            raise ValueError("Birthday can not be in the future. We don't know future.")


class Address(Field):
    pass
