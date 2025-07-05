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
```
!apt update
!apt install -y git zip unzip openjdk-17-jdk python3-pip \
  build-essential libssl-dev libffi-dev python3-dev \
  libncurses5-dev libncursesw5-dev libtinfo5 cmake

!pip install kivy buildozer cython==0.29.21
```
- Clone du projet GitHub avec :
```
!git clone https://github.com/timotheaoun/AppMobilePlanning.git app
%cd app
```
- Initialisation du projet avec ```Buildozer init ```(cette partie marche sur windows mais il faut installer buildozer donc pas besoin)
- Modification du fichier `buildozer.spec` 
- Compilation en APK Android avec :
```
!buildozer -v android debug
```
> Cette étape peut être très longue 😴
- Récupération de l'APK généré (par défaut dans `bin/PlanningApp-0.1-debug.apk`)
- Copie et téléchargement de l’APK avec :
```
!cp bin/*.apk /content/
from google.colab import files
files.download('/content/PlanningApp-0.1-debug.apk')
```

---

## Résumé du code à placer dans le notebook Google Colab :

```
!apt update
!apt install -y git zip unzip openjdk-17-jdk python3-pip \
  build-essential libssl-dev libffi-dev python3-dev \
  libncurses5-dev libncursesw5-dev libtinfo5 cmake

!pip install kivy buildozer cython==0.29.21

!git clone https://github.com/timotheaoun/AppMobilePlanning.git app
%cd app
!buildozer init
!buildozer -v android debug

!cp bin/*.apk /content/
from google.colab import files
files.download('/content/PlanningApp-0.1-debug.apk')
```
---

💡 *Projet personnel, évolutif, et orienté vers une meilleure gestion du temps et du focus.*

---

---
#Modification code
Les étapes que j'ai faites ont générées une erreur, actualisation :
```
!apt update
!apt install -y git zip unzip openjdk-8-jdk python3-pip \
  build-essential libssl-dev libffi-dev python3-dev \
  libncurses5-dev libncursesw5-dev libtinfo5 cmake

# Installer cython compatible et buildozer/kivy
!pip install --upgrade pip
!pip install cython==0.29.21 buildozer kivy

# Cloner ton repo
!git clone https://github.com/timotheaoun/AppMobilePlanning.git app
%cd app

# Nettoyer si build précédente
!buildozer android clean
!rm -rf ~/.buildozer/android/platform

# Initialiser buildozer.spec (s’il n’existe pas)
!buildozer init

# Modifier buildozer.spec pour forcer ndk21e (optionnel mais conseillé)
!sed -i 's/android.ndk = .*/android.ndk = 21e/' buildozer.spec
!sed -i 's/android.arch = .*/android.arch = armeabi-v7a/' buildozer.spec
!sed -i 's/# (int) Android API to use/android.api = 31/' buildozer.spec
!sed -i 's/# (int) Minimum API android.minapi = 21/' buildozer.spec

# Builder apk debug
!buildozer -v android debug

# Copier apk et proposer téléchargement
!cp bin/*.apk /content/
from google.colab import files
files.download('/content/PlanningApp-0.1-debug.apk')
```


