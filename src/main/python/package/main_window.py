from PySide2 import QtWidgets, QtGui
from PySide2.QtWidgets import QAbstractItemView

from package.api.note import Note, get_notes


# partie API

class MainWindow(QtWidgets.QWidget):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.setWindowTitle("PyNotes")

        self.setup_ui()
        self.populate_note()

    def setup_ui(self):
        self.create_widgets()  # ajouter un widget
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    # END UI

    def add_note_to_listwidget(self, note):
        lw_item = QtWidgets.QListWidgetItem(note.title)
        lw_item.note = note
        self.lw_notes.addItem(lw_item)

    def create_widgets(self):
        self.btn_createNote = QtWidgets.QPushButton("Créer une note")
        self.lw_notes = QtWidgets.QListWidget()
        self.textEdit = QtWidgets.QTextEdit()

    def modify_widgets(self):
        css_file = self.ctx.get_resource("style.css")
        with open(css_file, "r") as f:
            self.setStyleSheet(f.read())

    # Création d'une fenêtre de vue
    def create_layouts(self):
        self.main_layout = QtWidgets.QGridLayout(self)

    # On ajoute cette fenêtre à notre de f add_wedget
    def add_widgets_to_layouts(self):
        self.main_layout.addWidget(self.btn_createNote, 0, 0, 1, 1)
        self.main_layout.addWidget(self.lw_notes, 1, 0, 1, 1)
        self.main_layout.addWidget(self.textEdit, 0, 1, 2, 1)

    def setup_connections(self):
        self.btn_createNote.clicked.connect(self.create_note)
        self.textEdit.textChanged.connect(self.save_note)
        self.lw_notes.itemSelectionChanged.connect(self.populate_note_content)
        QtWidgets.QShortcut(QtGui.QKeySequence("Backspace"), self.lw_notes, self.delete_selected_note)
        self.lw_notes.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def create_note(self):
        titre, resultat = QtWidgets.QInputDialog.getText(self, "Ajouter une note", "Titre: ")
        if resultat and titre:
            note = Note(title=titre)
            note.save()
            self.add_note_to_listwidget(note)

    def delete_selected_note(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            resulat = selected_item.note.delete()
            if resulat:
                self.lw_notes.takeItem(self.lw_notes.row(selected_item))

    def get_selected_lw_item(self):
        selected_items = self.lw_notes.selectedItems()
        if selected_items:
            return selected_items[0]
        return None

    def populate_note(self):
        notes = get_notes()
        for note in notes:
            self.add_note_to_listwidget(note)

    def populate_note_content(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            self.textEdit.setText(selected_item.note.content)
        else:
            self.textEdit.clear()

    def save_note(self):
        selected_item = self.get_selected_lw_item()
        if selected_item:
            selected_item.note.content = self.textEdit.toPlainText()
            selected_item.note.save()
