import os
import json
from datetime import datetime, timedelta
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label

# Charger le fichier kv
Builder.load_file("main.kv")

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Dictionnaire mots-clés -> fichier html à ouvrir (exemple)
MOTS_CLES = {
    "sport": "sport.html",
    "lecture": "lecture.html",
    "travail": "travail.html",
}

class TaskPopup(Popup):
    task_name = StringProperty()
    task_desc = StringProperty()
    start = StringProperty()
    end = StringProperty()
    distraction_mode = BooleanProperty(False)

    def activate_distraction_mode(self):
        if self.distraction_mode:
            print("[INFO] Mode sans distraction activé !")
            # TODO : implémenter désactivation YouTube ou autres applis
        self.dismiss()

class PlanningPopup(Popup):
    def __init__(self, main_screen, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen

    def add_task(self):
        start = self.ids.start_input.text.strip()
        end = self.ids.end_input.text.strip()
        name = self.ids.name_input.text.strip()
        desc = self.ids.desc_input.text.strip()
        distraction = self.ids.distraction_checkbox.active

        # Validation simple des horaires
        if not self.valid_time_format(start) or not self.valid_time_format(end):
            self.show_error("Format heure invalide (HH:MM)")
            return
        if not name:
            self.show_error("Le nom de la tâche est obligatoire")
            return
        if start >= end:
            self.show_error("L'heure de fin doit être après l'heure de début")
            return

        # Vérification mot-clé
        fichier_html = MOTS_CLES.get(name.lower(), None)
        if fichier_html:
            # Tâche reconnue, pas de description, on la stocke spéciale
            task = {
                "name": name,
                "desc": "",
                "start": start,
                "end": end,
                "distraction_mode": distraction,
                "special": "mot_cle",
                "file": fichier_html
            }
        else:
            task = {
                "name": name,
                "desc": desc,
                "start": start,
                "end": end,
                "distraction_mode": distraction,
            }

        # Ajouter tâche au planning du lendemain
        self.main_screen.add_task_for_tomorrow(task)
        self.dismiss()

    def valid_time_format(self, t):
        try:
            datetime.strptime(t, "%H:%M")
            return True
        except ValueError:
            return False

    def show_error(self, message):
        popup = Popup(title="Erreur",
                      content=Label(text=message),
                      size_hint=(0.6, 0.3))
        popup.open()

class BilanPopup(Popup):
    def __init__(self, main_screen, date, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = main_screen
        self.date = date

    def save_bilan(self):
        texte = self.ids.bilan_text.text.strip()
        if texte:
            filename = os.path.join(DATA_DIR, f"bilan_{self.date.strftime('%Y-%m-%d')}.json")
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({"bilan": texte}, f, ensure_ascii=False, indent=2)
            self.dismiss()
            print(f"[INFO] Bilan sauvegardé pour {self.date.strftime('%Y-%m-%d')}")
            self.main_screen.render_tasks()
        else:
            self.show_error("Le bilan ne peut pas être vide")

    def show_error(self, message):
        popup = Popup(title="Erreur",
                      content=Label(text=message),
                      size_hint=(0.6, 0.3))
        popup.open()

class TaskButton(Button):
    task = DictProperty()

class MainScreen(BoxLayout):
    date = ObjectProperty(datetime.today())
    date_str = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.date = datetime.today()
        self.update_date_str()
        self.tasks = []
        self.load_tasks()
        self.render_tasks()

    def update_date_str(self):
        self.date_str = self.date.strftime("%A %d %B %Y")

    def go_day(self, delta):
        self.date += timedelta(days=delta)
        self.update_date_str()
        self.load_tasks()
        self.render_tasks()

    def load_tasks(self):
        # Charger les tâches et bilans
        self.tasks = []
        filename = os.path.join(DATA_DIR, f"tasks_{self.date.strftime('%Y-%m-%d')}.json")
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)

        # Ajout tâche Planification du lendemain (si date = aujourd'hui et > 20h)
        now = datetime.now()
        if self.date.date() == now.date() and now.hour >= 20:
            # S'assurer qu'elle n'existe pas déjà
            if not any(t.get("special") == "planning" for t in self.tasks):
                self.tasks.append({
                    "name": "Planification du lendemain",
                    "desc": "Cliquez ici pour planifier votre journée suivante.",
                    "start": "20:00",
                    "end": "21:00",
                    "distraction_mode": False,
                    "special": "planning"
                })

        # Chargement bilan du jour précédent (pour affichage)
        bilan_file = os.path.join(DATA_DIR, f"bilan_{(self.date - timedelta(days=1)).strftime('%Y-%m-%d')}.json")
        self.bilan_text = None
        if os.path.exists(bilan_file):
            with open(bilan_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.bilan_text = data.get("bilan", None)
                if self.bilan_text:
                    # Ajouter un bloc bilan à afficher à 6h du matin (par exemple)
                    self.tasks.append({
                        "name": "Bilan d'hier",
                        "desc": self.bilan_text,
                        "start": "06:00",
                        "end": "06:30",
                        "distraction_mode": False,
                        "special": "bilan"
                    })

    def render_tasks(self):
        grid = self.ids.grid
        grid.clear_widgets()

        hours = list(range(7, 23))
        for h in hours:
            hour_str = f"{h:02d}:00"

            # Chercher tâche qui commence à cette heure
            task = None
            for t in self.tasks:
                if t["start"] == hour_str:
                    task = t
                    break

            if task:
                btn = TaskButton(text=f"{task['start']} - {task['end']} : {task['name']}",
                                 size_hint_y=None, height=40)
                btn.task = task
                btn.bind(on_release=self.on_task_click)
                grid.add_widget(btn)
            else:
                # Case vide horaire cliquable pour créer une nouvelle tâche
                btn = Button(text=f"{hour_str} - ...",
                             size_hint_y=None, height=40,
                             background_color=(0.95,0.95,0.95,1))
                btn.bind(on_release=self.on_empty_slot_click)
                btn.hour_str = hour_str
                grid.add_widget(btn)

    def on_task_click(self, button):
        task = button.task
        if task.get("special") == "planning":
            # Ouvrir planification du lendemain
            popup = PlanningPopup(main_screen=self)
            popup.open()
        elif task.get("special") == "bilan":
            # Afficher bilan simple
            popup = TaskPopup(title="Bilan de la journée",
                              task_name=task["name"],
                              task_desc=task.get("desc", ""),
                              start=task["start"],
                              end=task["end"],
                              distraction_mode=False)
            popup.open()
        elif task.get("special") == "mot_cle":
            # Ouvrir fichier html lié au mot clé (ici on simule avec un popup)
            file_html = task.get("file")
            popup = Popup(title=f"Ouverture de {file_html}",
                          content=Label(text=f"Chargement de {file_html} ... (à implémenter)"),
                          size_hint=(0.6, 0.4))
            popup.open()
        else:
            # Tâche normale : afficher détails, activer mode distraction si coché
            popup = TaskPopup(title=task["name"],
                              task_name=task["name"],
                              task_desc=task.get("desc", ""),
                              start=task["start"],
                              end=task["end"],
                              distraction_mode=task.get("distraction_mode", False))
            popup.open()

    def on_empty_slot_click(self, button):
        # Pour l'instant on ne crée pas directement, juste on peut ouvrir planification
        popup = PlanningPopup(main_screen=self)
        # Pré-remplir l'heure de début avec celle du slot vide
        popup.ids.start_input.text = button.hour_str
        # Mettre heure fin +1h
        try:
            h, m = map(int, button.hour_str.split(":"))
            h2 = h + 1 if h < 22 else 23
            popup.ids.end_input.text = f"{h2:02d}:{m:02d}"
        except:
            popup.ids.end_input.text = ""
        popup.open()

    def add_task_for_tomorrow(self, task):
        tomorrow = self.date + timedelta(days=1)
        filename = os.path.join(DATA_DIR, f"tasks_{tomorrow.strftime('%Y-%m-%d')}.json")
        tasks = []
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                tasks = json.load(f)

        tasks.append(task)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        print(f"[INFO] Tâche ajoutée pour le {tomorrow.strftime('%Y-%m-%d')}")
        if self.date.date() == tomorrow.date():
            self.load_tasks()
            self.render_tasks()

    def on_stop(self):
        # Si besoin sauvegarder automatiquement à la fermeture (optionnel)
        pass

class PlanningApp(App):
    def build(self):
        self.title = "Planning Journalier"
        return MainScreen()

if __name__ == "__main__":
    PlanningApp().run()
