# Rapport TP `snort`

## Tâche 1 : Ajout d'une règle pour le contenu "CONFIDENTIEL"
Pour ajouter une règle personnalisée détectant la présence du mot "CONFIDENTIEL", nous devons modifier le fichier `/etc/snort/rules/local.rules` et y ajouter la ligne suivante :
```
alert tcp any any -> any any (msg:"CONFIDENTIAL detected"; content:"CONFIDENTIAL"; sid:00003;)
```
Cette règle permet de détecter tout paquet contenant la chaîne de caractères "CONFIDENTIEL" et génère une alerte lorsque ce contenu est trouvé.

## Tâche 2 : Effets du chiffrement
Lorsqu’un contenu est chiffré, cette règle ne pourra pas détecter la chaîne de caractères "CONFIDENTIEL" dans le paquet. En effet, la règle recherche cette chaîne en texte clair, et non sous forme chiffrée. Cela signifie que l'alerte ne sera pas déclenchée et que le contenu restera indétectable par la règle. Ce cas démontre l'une des limitations des règles basées sur le contenu lorsqu'il s'agit de détecter des informations sensibles dans un trafic chiffré.

## Tâche 3 : Surveillance du trafic interne
Lorsque nous exécutons `nmap` depuis le réseau interne, le trafic n'est pas détecté par Snort, car celui-ci ne surveille pas l'interface réseau interne. Snort surveille par défaut l'interface externe, ce qui limite la détection au trafic passant par cette interface uniquement. Pour surveiller le trafic interne, nous pouvons dupliquer le trafic interne vers le composant Snort. Cette duplication peut se faire en ajoutant la ligne suivante dans le fichier `/etc/rc.local` :
```bash
iptables -t mangle -A PREROUTING -i $lan2 -j TEE --gateway 192.168.3.1
```
Ensuite, nous exécutons la commande `sudo /etc/rc.local` pour appliquer les modifications. Cela dupliquera le trafic interne vers Snort, permettant ainsi de surveiller ce trafic également.

## Tâche 4 : Différenciation du trafic selon l'adresse
L'objectif final est d’atteindre les conditions suivantes :
- Un accès externe au plan d'entreprise génère une alerte.
- Un accès interne au plan d'entreprise ne génère pas d'alerte.
- Toute utilisation de `nmap`, interne ou externe, génère une alerte "ICMP NMAP PINK".

Pour cela, nous pouvons modifier notre règle pour spécifier les adresses IP source et destination. Par exemple :
```plaintext
alert tcp 192.168.1.2/24 any -> 192.168.1.10 any (msg:"CONFIDENTIAL detected"; content:"CONFIDENTIAL"; sid:00003;)
```
Les adresses IP `192.168.1.2/24` correspondent au réseau interne, que nous pouvons déterminer à l'aide de la commande `ifconfig`. L'adresse IP `192.168.1.10` correspond à la passerelle, qui est donnée.

Ainsi, en tentant d'accéder au contenu confidentiel depuis le réseau externe, nous déclenchons une alerte, alors que cet accès depuis le réseau interne ne génère aucune alerte. Quant à l'utilisation de `nmap`, une alerte est déclenchée indépendamment du réseau depuis lequel il est utilisé.
