from pickle import dump, load
import os
from collections import UserDict


class NoteBook(UserDict):

    __instance = None

    def __new__(cls):
        """Singltone????"""
        if not isinstance(cls.__instance, cls):
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, file_path=os.path.join("node_book")):
        super().__init__()
        self.file_path = f"{file_path}.bin"

    def create_new_note(self, name: str, info: list) -> str:
        if name in self.data:
            raise KeyError(f"Note with name {name} already exist.")
        elif not name:
            return "You can't create empty note."
        else:
            tags = []
            for piece in info:  # Search tags in all text
                if piece.startswith("#"):
                    tags.append(piece)
            info_new = " ".join(info)
            self.data[name] = Note(name, tags, info_new)
            return f"Note with name {name} successfully create."

    def add_note(self, name: str, info: list) -> str:
        tags = []
        for piece in info:  # Ищем теги в тексте, именно так они добавляются изначально
            if piece.startswith("#"):
                tags.append(piece)
        info = " ".join(info)
        self.data[name].add_content(tags, info)
        return f"Information successfully added to {name}."

    def clear_note(self, name: str) -> str:
        self.data[name].clear_tags()
        self.data[name].clear_text()
        return f"Note named {name} successfully cleared."

    def clear_text(self, name: str) -> str:
        self.data[name].clear_text()
        return f"Text in {name} cleared."

    def clear_tags(self, name: str) -> str:
        self.data[name].clear_tags()
        return f"Tags in {name} cleared."

    def del_note(self, name: str) -> str:
        del self.data[name]
        return f"Note named {name} successfully deleted."

    def search_in_text(self, info: str) -> list:
        result = []
        for note in self.data.values():
            if info in note.text or info == note.name:
                if not result:
                    result = [f"Search results for {info} in text:\n"]
                result.append(f"Name: {note.name}\n"
                              f"\tTags: {note.tags}\n"
                              f"\tText: {note.text}\n")
        return result if result else [f"Search results for {info} in text:\nEmpty"]

    def search_in_tags(self, info: str) -> list:
        result = []
        for note in self.data.values():
            if info in note.tags or info == note.name:
                if not result:
                    result = [f"Search results for {info} in text:\n"]
                result.append(f"Name: {note.name}\n"
                              f"\tTags: {note.tags}\n"
                              f"\tText: {note.text}\n")
        return result if result else [f"Search results for {info} in text:\nEmpty"]

    def show_note(self, name: str) -> str:
        note = self.data[name]
        return f" Name: {note.name}\n" \
               f"\tTags: {note.tags}\n" \
               f"\tText: {note.text}\n"

    def show_all(self) -> list:
        result = []
        for name, note in self.data.items():
            result.append(f"Name: {note.name}\n"
                          f"\tTags: {note.tags}\n"
                          f"\tText: {note.text}\n")
        return result

    def sort_by_tags(self, tags: list) -> list:
        result = []
        for note in self.data.values():
            cnt = 0
            for tag in tags:  # Считаем сколько раз сумарно встречается каждый элемент из списка тегов в тегах записи
                if tag in note.tags:
                    cnt += 1 if tag in note.tags else 0
            result.append(f"Coincidences with tags {[i for i in tags if i]}: {cnt}\n" 
                          f"Name: {note.name}\n"
                          f"\tTags: {note.tags}\n"
                          f"\tText: {note.text}\n")
        return sorted(result, reverse=True)

    def save_to_file(self) -> str:
        with open(self.file_path, "wb") as file:
            dump(self.data, file)
        return f"Successfully save NoteBook to file {self.file_path}"

    def load_from_file(self) -> str:
        with open(self.file_path, "rb") as file:
            self.data = load(file)
        return f"Successfully load NoteBook from file {self.file_path}"


class Note:

    def __init__(self, name: str, tags: list, text: str):
        self.name = name
        self._tags = None
        self.tags = tags
        self.text = text

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if len(value) < 1:
            self._tags = []
        else:
            self._tags = [*value]

    def add_content(self, tags, text):
        if tags:
            self.tags.extend(tags)
        if text:
            self.text += text + " "

    def clear_text(self):
        self.text = ""

    def clear_tags(self):
        self._tags = []
