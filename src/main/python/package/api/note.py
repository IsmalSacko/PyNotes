import os  # Methode de concatenation
import json  # Ecrire de fichiers json
from uuid import uuid4  # identifiant unique
from glob import glob  # fonction pour boucler sur les données
from package.api.constants import NOTES_DIR


def get_notes():
    liste_notes = []
    fichiers = glob(os.path.join(NOTES_DIR, "*.json"))
    for fichier in fichiers:
        with open(fichier, "r") as f:
            notes_data = json.load(f)  # on reccupère la data ds f
            # l'identifiant de fichier sans l'extention json
            note_uuid = os.path.splitext(os.path.basename(fichier))[0]
            note_title = notes_data.get("title")
            note_content = notes_data.get("content")
            note = Note(uuid=note_uuid, title=note_title, content=note_content)
            liste_notes.append(note)

    return liste_notes


class Note:
    def __init__(self, title="", content="", uuid=None):
        if uuid: # vérification si id uniq est présent
          self.uuid = uuid
        else:
            self.uuid = str(uuid4())

        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.title} ({self.uuid})"

    def __str__(self):
        return self.title

    @property
    def path(self):
        return os.path.join(NOTES_DIR, self.uuid + ".json")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            raise TabError("Valeur invalide: il faut une chaîne de caractère.")

    def save(self):  # sauvegarder
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)

        data = {"title": self.title, "content": self.content}
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def delete(self):  # Suppression
        os.remove(self.path)
        if os.path.exists(self.path):
            return False
        return "Le fichier espécifié n'exite plus !"


if __name__ == '__main__':
    notes = get_notes()
    print(notes)
