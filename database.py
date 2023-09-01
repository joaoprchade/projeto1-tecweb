import sqlite3
from dataclasses import dataclass


@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''


class Database:
    def __init__(self, name) -> None:
        self.name = name
        self.conn = sqlite3.connect(name + '.db')
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS note(id INTEGER PRIMARY KEY, title STRING, content STRING NOT NULL)")

    def add(self, note):
        self.title = note.title
        self.content = note.content

        self.conn.execute(
            f"INSERT INTO note (title, content) VALUES ('{self.title}', '{self.content}')")

        self.conn.commit()

    def get_all(self):
        notes = []
        cursor = self.conn.execute(
            "SELECT id, title, content FROM note")
        for row in cursor:
            note = Note(id=row[0], title=row[1], content=row[2])
            notes.append(note)

        return notes

    def update(self, entry):
        self.id = entry.id
        self.title = entry.title
        self.content = entry.content
        self.conn.execute(
            f"UPDATE note SET (title, content) = ('{self.title}', '{self.content}') WHERE id = '{self.id}'")
        self.conn.commit()

    def delete(self, note_id):
        self.note_id = note_id
        self.conn.execute(f"DELETE FROM note WHERE id = {self.note_id}")
        self.conn.commit()
