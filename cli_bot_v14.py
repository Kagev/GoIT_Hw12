
import pickle
import sys
from collections import UserDict
from datetime import datetime, timedelta
from pathlib import Path


class Field:
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self.value = self._validate(value)
    
    def _validate (self, value):
        if not isinstance(value, str):
            raise ValueError(f'Phone bumber must be a string, not {type(value)}')
        value = value.strip()
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        return value
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.value!r})'

class Brirthday(Field):
    def __init__(self, value=None):
        super().__init__()
        self.value = self._validate(value)

    def _validate(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f'Birthday must be a string in the format "DD-MM-YYYY", not {type(value)}')
        try:
            value = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError(f"Birthday must be in the format 'DD-MM-YYYY'")
        today = datetime.now().date()
        if value.replace(year=today.year) < today:
            value = value.replace(year=today.year + 1)
        return value
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.value!r})'


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.add_phone(phone)
        self.birthday = Brirthday(birthday)

    def add_phone(self, phone):
        if phone is not None:
            p = Phone(phone)
            self.phones.append(p)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone.value:
                p.value = new_phone
                return

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name!r}, phones={self.phones!r})'

    def days_to_birthday(self):
        if not self.birthday.value:
            return None
        today = datetime.now().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
    
    def get_record(self, name):
        return self.data[name]
    
    def iterator(self, n=1):
        record = list(self.data.values())
        for i in range(0, len(record), n):
            yield record[i:i+n]
    
    def save(self, file_path):
        with open(file_path, "wb") as file:
            pickle.dump(self.data, file)

    def load(self, file_path):
        with open(file_path, "rb") as file:
            self.data = pickle.load(file)

    def search(self, query):
        query = query.lower()
        results = []
        for record in self.data.values():
            if query in record.name.value.lower():
                results.append(record)
            else:
                for phone in record.phones:
                    if query in phone.value.lower():
                        results.append(record)
                        break
        return results



# class AddressBook:
#     def __init__(self, filename):
#         self.records = {}
#         self.last_record_id = 0
#         self.file = Path(filename)
#         self.deserialize()
        
#     def add(self, record: Record):
#         self.records[self.last_record_id] = record
#         record.id = self.last_record_id
#         self.last_record_id += 1
        
#     def search(self, search_str):
#         result = []
#         for record_id, record in self.records.items():
#             if search_str in record:
#                 result.append(record_id)
#         return result
    
#     def serialize(self):
#         with open(self.file, "wb") as file:
#             pickle.dump((self.last_record_id, self.records), file)
            
#     def deserialize(self):
#         if not self.file.exists():
#             return None
#         with open(self.file, "rb") as file:
#             self.last_record_id, self.records = pickle.load(file)
            
#     def show_record(self, rec_id):
#         return f'{self.records[rec_id]}\n'
    
#     def show_records(self, size: int):
#         counter = 0
#         result = ""
#         for record in self.records.values():
#             result += str(record)
#             counter += 1
#             if counter == size:
#                 yield result
#                 counter = 0
#                 result = ""
#         yield result