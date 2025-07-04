# 📅 PlanningApp – Organisateur personnel intelligent

Bienvenue dans **PlanningApp**, une application de planification journalière que je développe pour améliorer ma productivité pendant mes vacances (application pour le moment bancale car c'est mon premier projet dans lequel je crée une appli mobile). J'utilise GitHub car sur mon PC Windows, je ne peux pas utiliser Buildozer, donc je vais tout faire depuis Google Colab (Linux virtuel gratuit) et importer ce dépôt GitHub.

## 🎯 Objectif du projet

Créer une application mobile (APK Android) simple, intuitive et **esthétiquement agréable**, qui me permette de :

- Visualiser mon **emploi du temps** heure par heure
- Cliquer sur une tâche pour voir ses **détails**
- Activer automatiquement un **mode sans distraction** selon l'horaire
- **Planifier ma journée du lendemain** facilement
- Gérer un **carnet de bord quotidien** avec bilan journalier
- Reconnaître des tâches récurrentes (ex : "sport" → ouvre `sport.html`)

## 🔧 Technologies utilisées

Ce projet est développé avec :

- **Python** & **Kivy** pour l'interface mobile
- **Buildozer** pour la compilation en APK Android

## 📱 Finalité

À la fin, je souhaite générer un **APK** installable sur Android, sans dépendre d’un navigateur web.

---

## ⚙️ Réalisation

### 💻 Sur PC :
- Création du fichier `main.kv`
- Création du fichier `main.py`

### 🌐 Sur Internet :
- Import dans **GitHub**
- Utilisation de [Google Colab](https://colab.research.google.com/)
- Installation des packages avec :

<code>bash
!apt update
!apt install -y git zip unzip openjdk-17-jdk python3-pip \
  build-essential libssl-dev libffi-dev python3-dev \
  libncurses5-dev libncursesw5-dev libtinfo5 cmake

!pip install kivy buildozer cython==0.29.21
</code>

- Clone du projet GitHub avec :

<code>bash
!git clone https://github.com/timotheaoun/AppMobilePlanning.git app
%cd app
</code>

- Initialisation du projet avec Buildozer (optionnel si tu as déjà un fichier `buildozer.spec`) :

<code>
!buildozer init
</code>

- Modification du fichier `buildozer.spec` selon besoin
- Compilation en APK Android avec :

<code>
!buildozer -v android debug
</code>

> Cette étape peut être très longue 😴

- Récupération de l'APK généré (par défaut dans `bin/PlanningApp-0.1-debug.apk`)

- Copie et téléchargement de l’APK avec :

<code>
!cp bin/*.apk /content/
from google.colab import files
files.download('/content/PlanningApp-0.1-debug.apk')
</code>

---

## Résumé du code à placer dans le notebook Google Colab :

<code>
!apt update
!apt install -y git zip unzip openjdk-17-jdk python3-pip \
  build-essential libssl-dev libffi-dev python3-dev \
  libncurses5-dev libncursesw5-dev libtinfo5 cmake

!pip install kivy buildozer cython==0.29.21

!git clone https://github.com/timotheaoun/AppMobilePlanning.git app
%cd app

!buildozer -v android debug

!cp bin/*.apk /content/
from google.colab import files
files.download('/content/PlanningApp-0.1-debug.apk')
</code>

---

💡 *Projet personnel, évolutif, et orienté vers une meilleure gestion du temps et du focus.*
