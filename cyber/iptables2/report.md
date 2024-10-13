# Rapport TP `iptables2`

## Task 1: Explore
In this first task we'll use some tools to explore the network and the firewall rules.

### Wireshark
We'll start Wireshark to capture the network traffic using the command `wireshark &`. The `&` is used to run the command in the background.

### nmap
Next, we'll scan the server ports using the command `nmap server`. The output is as follows:
```
...
PORT     STATE SERVICE
22/tcp   open  ssh
23/tcp   open  telnet
80/tcp   open  http
...
```
We can see that the server has the ports 22, 23 and 80 open. We'll check if they are accessible from the client.
For each port, we'll use the appropriate command:
- `ssh server`
- `telnet server`
- `wget server`
We can confirm that all ports are accessible from the client.
Throughout the process, we'll keep Wireshark running to capture the network traffic, and take note of the IP addresses of the source and the destination ports used by the client.
The IP address of the client is `172.24.0.3`, and the IP address of the server is `172.25.0.3`, and the destination port when using the appropriate commands are the same as the shown in the nmap output (22 for ssh, 23 for telnet, and 80 for http).

## Task 2: Use iptables to limit traffic
The goal is to use the firewall to prevent any traffic other than SSH and HTTP from reaching the server.
For that, we already have a shell script that sets certain rules for the firewall:
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

We'll modify the script to allow HTTP traffic on port 80 as well:
```bash
...
# Allow ssh traffic on port 22
$IPTABLES -A FORWARD -p tcp --dport 22 -j ACCEPT

# Allow http traffic on port 80
$IPTABLES -A FORWARD -p tcp --dport 80 -j ACCEPT
...
```

We'll run the script using `sudo ./example_fw.sh` and check if the rules are applied by trying to reconnect using `telnet` and monitoring the log file `/var/log/syslog` using the command `tail -f /var/log/syslog`.

When trying to connect using `telnet`, we can see that it takes a long time and eventually times out. We can also see the log messages in the syslog file.
Here's an example of the log messages:
```
Oct 13 12:04:12 firewall IPTABLES DROPPED IN=eth0 OUT=eth1 MAC=xx SRC=172.24.0.3 DST=172.25.0.3
LEN=60 TOS=00 PREC=0x00 TTL=63 ID=47644 DF PROTO=TCP SPT=52484 DPT=3389 SEQ=81298835 ACK=0 WINDOW=32120 SYN URGP=0 MARK=0
```

We can also see that the output of the `nmap` command has changed and we no longer have the port 23 open:
```
...
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
...
```

## Task 3: Open new service port
The client computer has a `wizbang` program that we want to allow to send traffic to the server.
We'll first run it and look on Wireshark to see the destination port used by the program.
We can see that the destination port is `10039`.
Now we'll simply add a rule to the firewall script to allow traffic on that port:
```bash
...
# Allow ssh traffic on port 22
$IPTABLES -A FORWARD -p tcp --dport 22 -j ACCEPT

# Allow http traffic on port 80
$IPTABLES -A FORWARD -p tcp --dport 80 -j ACCEPT

# Allow wizbang traffic on port 10039
$IPTABLES -A FORWARD -p tcp --dport 10039 -j ACCEPT
...
```

We'll run the script again using `sudo ./example_fw.sh` and check if the rule is applied by running the `wizbang` program.
We can see that the program is run successfully and the traffic is allowed. Here's an example of the output:
```
$ ./wizbang ls
Sending instruction ls
bye
```

A port scan on all ports using `nmap -p- server` shows that the port 10039 is open:
```
...
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
10039/tcp open  unknown
...
```

## Conclusion
In this TP, we explored the network and the firewall rules using tools like Wireshark and nmap. We used iptables to limit the traffic to only SSH and HTTP, and then opened a new port for the `wizbang` program. We successfully managed to control the traffic and allow only the desired services to communicate with the server.
