# Rapport TP `Metasploit`

## Tâche 1 : Vérification de la connectivité entre l'attaquant et la victime
Pour commencer, nous devons vérifier si l'attaquant peut atteindre la victime en utilisant une simple commande `ping` vers l'adresse IP de la victime.
```bash
ping 192.168.1.2
```

## Tâche 2 : Récupérer la liste des services vulnérables sur la victime
```bash
nmap -p0-65535 192.168.1.2
```
Pour obtenir des informations plus détaillées sur les services actifs sur ces ports ouverts, nous ajoutons l’option `-sV`, qui nous indique les versions des services.
```bash
nmap -sV -p0-65535 192.168.1.2
```
Suite à l'exécution de ces commandes, nous obtenons une liste des services actifs sur la machine de la victime, avec des informations sur les versions et les vulnérabilités potentielles.

**Service rlogin vulnérable (port 513)**
Le service `rlogin`, qui s'exécute sur le port 513, est un service d'authentification à distance.

**Service ingreslock vulnérable (port 1524)**
Le service `ingreslock`, qui écoute sur le port 1524, est utilisé pour la gestion des verrous dans le système de base de données Ingres.

**Service distccd vulnérable (port 3632)**
Le service `distccd`, fonctionnant sur le port 3632, est un compilateur C/C++ distribué.

**Service IRC daemon vulnérable (port 6667)**
Le service `IRC daemon`, qui écoute sur le port 6667, est un serveur IRC (Internet Relay Chat) qui permet la communication en temps réel entre les utilisateurs.

**Service VSFtpd vulnérable (port 21)**
Le service `VSFtpd`, sur le port 21, est simplement un serveur FTP.

**Service Samba vulnérable (port 139)**
Le service `Samba`, qui écoute sur le port 139, est un service de partage de fichiers et d'imprimantes pour les systèmes d'exploitation Windows.

**Service HTTP (PHP) vulnérable (port 80)**
Le port 80 héberge un serveur web qui exécute des scripts PHP.

**Service Postgres vulnérable (port 5432)**
Le service `Postgres`, qui écoute sur le port 5432, est un système de gestion de base de données relationnelle.

## Exploitation des services vulnérables
Chacun de ces services présente des vulnérabilités spécifiques qui peuvent être exploitées pour obtenir un accès non autorisé à la machine de la victime. Ces vulnérabilités vont d'un dépassement de tampon à l'exécution de code arbitraire, en passant par l'authentification par défaut et les erreurs de configuration. Metasploit est un outil puissant qui permet d'exploiter ces vulnérabilités pour obtenir un accès à distance à la machine cible.

Après avoir exploité les vulnérabilités des services `rlogin`, `ingreslock`, `distccd`, `IRC daemon`, `VSFtpd`, `Samba`, `HTTP (PHP)` et `Postgres`, nous avons pu obtenir un accès non autorisé à la machine de la victime et afficher le contenu du fichier `filetoview.txt`.

Voici le contenu du fichier :
```
# Filename: filetoview.txt
#
# Description: This is a pre-created file for each student (victim) container 

# This file is modified when container is created
# The string below will be replaced with a keyed hash
My string is: d768dbce41c0f8bd0ad6b69f3b5469f7
```

## Conclusion
Dans ce TP, nous avons utilisé Metasploit pour cibler et exploiter des services vulnérables sur la machine de la victime, en identifiant plusieurs failles de sécurité. Chaque tâche a permis de montrer comment Metasploit peut tirer parti des configurations vulnérables pour obtenir des accès non autorisés aux systèmes. Ce TP met en évidence l'importance de sécuriser les services réseau et de maintenir les logiciels à jour pour prévenir des attaques similaires.

