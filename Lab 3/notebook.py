import sys
import datetime

id = 0

class Note:

    def __init__(self, memo, tags=''):
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        global id
        id += 1
        self.id = id

    def match(self, filter):
        return filter in self.memo or filter in self.tags

class Notebook:

    def __init__(self):
        self.notes = []

    def new_note(self, memo, tags=''):
        self.notes.append(Note(memo, tags))

    def find_note(self, note_id):
        for note in self.notes:
            if str(note.id) == str(note_id):
                return note
        return None

    def modify_memo(self, note_id, memo):
        note = self.find_note(note_id)
        if note:
            note.memo = memo
            return True
        return False

    def modify_tags(self, note_id, tags):
        note = self.find_note(note_id)
        if note:
            note.tags = tags
            return True
        return False

    def search(self, filter):
        return [note for note in self.notes if
                note.match(filter)]

class Menu:
    
    def __init__(self):
        self.notebook = Notebook()
        self.choices = {
                "1": self.show_notes,
                "2": self.search_notes,
                "3": self.add_note,
                "4": self.modify_note,
                "5": self.exit
                }

    def display_menu(self):
        print("""
Notebook Menu
1. Show all Notes
2. Search Notes
3. Add Note
4. Modify Note
5. exit
""")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def show_notes(self, notes=None):
        if not notes:
            notes = self.notebook.notes
        for note in notes:
            print("{0}: {1}\n{2}".format(
                note.id, note.tags, note.memo))

    def search_notes(self):
        filter = input("Search for: ")
        notes = self.notebook.search(filter)
        self.show_notes(notes)

    def add_note(self):
        memo = input("Enter a memo: ")
        self.notebook.new_note(memo)
        print("added successfully.")

    def modify_note(self):
        id = input("Enter a note id: ")
        memo = input("Enter a memo: ")
        tags = input("Enter tags: ")
        if memo:
            self.notebook.modify_memo(id, memo)
        if tags:
            self.notebook.modify_tags(id, tags)

    def exit(self):
        sys.exit(0)

if __name__ == "__main__":
    Menu().run()