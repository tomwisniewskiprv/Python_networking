# Python networking (scripts)

Done:

* validate IP - Regex IP number validation.
* banner grabber - Tries to grab banner from running services at given IP.
* Port Scanner - Enter an IP address and port numbers the program will then attempt to find open ports on the given computer by connecting to each of them. On any successful connections mark the port as open.
* simple FTP - A file transfer program which can transfer files back and forth from a remote machine. Acts as both server and client.
* traceroute - (alpha) trace routes to destination using UDP and ICMP response

TODO:

*remote shell - (working on this now) execute system commands on remote machine
*udp scanner - sends UDP packets and checks if remote machine responds with ICMP
*proxy - redirects connections 

##Memo:
Most of the scripts here require validate_ip.py for IP validation and
IPv4_Header.py for low level binary operations.
