# Rapport TP `snort`

## Task 1: Adding custom rule for CONFIDENTIAL content
To add such a rule, we have to edit the `/etc/snort/rules/local.rules` file and add the following line:
```
alert tcp any any -> any any (msg:"CONFIDENTIAL detected"; content:"CONFIDENTIAL"; sid:00003;)
```
This rule will detect any packet containing the string "CONFIDENTIAL" and will generate an alert.

## Task 2: Effects of encryption
When the content is encrypted, the rule will not be able to detect the string "CONFIDENTIAL" in the packet. This is because the content is encrypted and the rule is looking for the string in plain text. Therefore, the rule will not be triggered and the content will not be detected. This is one of the limitations of using content-based rules for detecting sensitive information in encrypted traffic.

## Task 3: Watching internal traffic
When running nmap from the internal network, the traffic is not detected by Snort because the traffic is not passing through the network interface that Snort is monitoring. Snort is monitoring the external interface, so it will only detect traffic that is passing through that interface. To monitor internal traffic, we can mirror the internal traffic to the Snort component. This can be done by adding the following line to `/etc/rc.local`:
```
iptables -t mangle -A PREROUTING -i $lan2 -j TEE --gateway 192.168.3.1
```
We then run the `sudo /etc/rc.local` command to apply the changes. This will mirror the internal traffic to the Snort component, allowing it to monitor internal traffic as well.

## Task 4: Distinguishing traffic by address
The ultimate goal is to:
- External access to the business plan generates an alert.
- Internal access to the business plan does not generate an alert.
- External or internal use of nmap generates ICMP NMAP PINK alert.

To achieve this, we can simply alter our rule to specify the source and destination IP addresses. For example:
```
alert tcp 192.168.1.2/24 any -> 192.168.1.10 any (msg:"CONFIDENTIAL detected"; content:"CONFIDENTIAL"; sid:00003;)
```

The ip addresses `192.168.1.2/24` are the internal network, and we can get those by running the `ifconfig` command.
The ip address `192.168.1.10` is the gateway, and this was a given.

Now if try to access the confidential content from the external network, we will get an alert, unlike when we access it from the internal network. As for `nmap` we will get an alert regardless of the network we are in.
