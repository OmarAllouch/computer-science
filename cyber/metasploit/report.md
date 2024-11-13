# Rapport TP `metasploit`

## Task 1: Verify connectivity between attacker and victim
First we check if we can ping the victim from the attacker by simply pinging the victim's IP address.
```bash
ping 192.168.1.2
```

## Task 2: Get a list of vulnerable services on the victim
It's typical to use nmap to scan for open ports on a target machine in order to identify potential vulnerabilities.
```bash
nmap -p0-65535 192.168.1.2
```
To show more information about the services running on the open ports, we can use the `-sV` flag.
```bash
nmap -sV -p0-65535 192.168.1.2
```

## Task 3: Vulnerably configured rlogin service (port 513)
The `rlogin` service is vulnerable to a buffer overflow attack. We can use Metasploit to exploit this vulnerability.
After running the exploit we can display the root file, we get the string: `d768dbce41c0f8bd0ad6b69f3b5469f7`.
And here's the whole file:
```
# Filename: filetoview.txt
#
# Description: This is a pre-created file for each student (victim) container 

# This file is modified when container is created
# The string below will be replaced with a keyed hash
My string is: d768dbce41c0f8bd0ad6b69f3b5469f7
```

## Task 4: Vulnerable ingreslock service (port 1524)

## Task 5: Vulnerable distccd service (port 3632)

## Task 6: Vulnerable IRC daemon (port 6667)

## Task 7: Vulnerable VSFtpd service (port 21)

## Task 8: Vulnerable Samba service (port 139)

## Task 9: Vulnerable HTTP (php) service (port 80)

## Task 10: Vulnerable Postgres service (port 5432)

