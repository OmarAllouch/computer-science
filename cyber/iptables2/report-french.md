# Rapport TP `iptables2`

## Tâche 1 : Exploration

Dans cette première tâche, nous allons utiliser quelques outils pour explorer le réseau et les règles du pare-feu.

### Wireshark

Nous allons commencer par utiliser Wireshark pour capturer le trafic réseau en lançant la commande `wireshark &`. Le symbole `&` permet de lancer la commande en arrière-plan.

### nmap

Ensuite, nous allons scanner les ports ouverts sur le serveur à l'aide de la commande `nmap server`. Voici le résultat :
```
...
PORT     STATE SERVICE
22/tcp   open  ssh
23/tcp   open  telnet
80/tcp   open  http
...
```

On constate que les ports 22, 23 et 80 sont ouverts sur le serveur. Nous allons vérifier s'ils sont accessibles depuis le client. Pour chaque port, nous utilisons la commande correspondante :
- `ssh server` pour le port 22
- `telnet server` pour le port 23
- `wget server` pour le port 80

Nous confirmons que tous les ports sont bien accessibles depuis le client. Pendant ce processus, nous laissons Wireshark en fonctionnement pour capturer le trafic réseau et noter les adresses IP des sources et les ports destinations utilisés. L'adresse IP du client est `172.24.0.3`, celle du serveur est `172.25.0.3`, et les ports de destination correspondent à ceux indiqués par `nmap` (22 pour SSH, 23 pour Telnet et 80 pour HTTP).

## Tâche 2 : Utiliser iptables pour limiter le trafic

L'objectif est d'utiliser le pare-feu pour bloquer tout trafic à destination du serveur, à l'exception des services SSH et HTTP. Nous disposons déjà d'un script shell qui définit certaines règles de pare-feu :

```bash
#!/bin/bash
#
# This example IPTABLES firewall will only allow SSH traffic
# to be forwarded.
#
IPTABLES=/sbin/iptables

# start and flush
$IPTABLES -F
$IPTABLES -t nat -F
$IPTABLES -X
#
# By default, do not allow any forwarding or accept any traffic
# destined for the firewall.
#
$IPTABLES -P FORWARD DROP
$IPTABLES -P INPUT   DROP
$IPTABLES -P OUTPUT  DROP

# Allow forwarding of traffic associated with any established session
$IPTABLES -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow ssh traffic on port 22
$IPTABLES -A FORWARD -p tcp --dport 22 -j ACCEPT

# loopback device (internal traffic)
iptables -A INPUT -i lo -p all -j ACCEPT

# log IPTABLES filtering actions
iptables -A FORWARD -j NFLOG -m limit --limit 2/min --nflog-prefix "IPTABLES DROPPED"
```

Nous allons modifier ce script pour également autoriser le trafic HTTP sur le port 80 :

```bash
...
# Allow ssh traffic on port 22
$IPTABLES -A FORWARD -p tcp --dport 22 -j ACCEPT

# Allow ssh traffic on port 80
$IPTABLES -A FORWARD -p tcp --dport 80 -j ACCEPT
...
```

Nous exécutons ensuite le script avec la commande `sudo ./example_fw.sh` et vérifions que les règles sont bien appliquées en essayant de nous reconnecter via Telnet et en surveillant les logs dans `/var/log/syslog` avec la commande `tail -f /var/log/syslog`.

Lors de la tentative de connexion via Telnet, la connexion échoue après un certain temps et nous pouvons observer des messages dans le fichier de log. Voici un exemple de message de journal :
```
Oct 13 12:04:12 firewall IPTABLES DROPPED IN=eth0 OUT=eth1 MAC=xx SRC=172.24.0.3 DST=172.25.0.3
LEN=60 TOS=00 PREC=0x00 TTL=63 ID=47644 DF PROTO=TCP SPT=52484 DPT=3389 SEQ=81298835 ACK=0 WINDOW=32120 SYN URGP=0 MARK=0
```

Nous pouvons aussi constater que le résultat de la commande `nmap` a changé, le port 23 n'est plus accessible :
```
...
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
...
```

## Tâche 3 : Ouverture d'un nouveau port pour un service

L'ordinateur client dispose d'un programme appelé `wizbang`, et nous souhaitons permettre à ce programme d'envoyer du trafic vers le serveur.

Nous exécutons le programme et analysons le trafic avec Wireshark pour identifier le port de destination utilisé. Il s'agit du port `10039`. Nous allons alors ajouter une règle dans le script de pare-feu pour autoriser le trafic sur ce port :

```bash
...
# Allow ssh traffic on port 22
$IPTABLES -A FORWARD -p tcp --dport 22 -j ACCEPT

# Allow ssh traffic on port 80
$IPTABLES -A FORWARD -p tcp --dport 80 -j ACCEPT

# Allow ssh traffic on port 10039
$IPTABLES -A FORWARD -p tcp --dport 10039 -j ACCEPT
...
```

Nous relançons le script avec `sudo ./example_fw.sh` et vérifions si la règle est appliquée en réexécutant le programme `wizbang`. Nous constatons que le programme fonctionne et que le trafic est autorisé. Voici un exemple de sortie :
```
$ ./wizbang ls
Sending instruction ls
bye
```

Un nouveau scan de ports avec `nmap -p- server` montre que le port 10039 est désormais ouvert :
```
...
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
10039/tcp open  unknown
...
```

## Conclusion

Dans ce TP, nous avons exploré le réseau et les règles de pare-feu à l'aide d'outils comme Wireshark et nmap. Nous avons utilisé `iptables` pour limiter le trafic uniquement aux services SSH et HTTP, puis ouvert un nouveau port pour le programme `wizbang`. Grâce à ces manipulations, nous avons réussi à contrôler le trafic et à autoriser uniquement les services souhaités à communiquer avec le serveur.
