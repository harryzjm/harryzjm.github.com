---  
layout: post  
title: How To Secure Your Linux Server In 7 Easy Steps  
category: Linux  
tags: Linux  
keywords: Linux  
---  

__Posted by [Brian Mutende](https://medium.com/servers-101/how-to-secure-your-linux-server-6026cfcdefd8)__  


*A lot of servers are being hacked every *[*now *](https://thehackernews.com/2019/02/vfemail-cyber-attack.html)*and *[*then*](https://thehackernews.com/2018/09/apple-server-hack.html)*. So I decided to write a short tutorial that shows you how you can easily secure your Linux server.*

This is not meant to be a comprehensive security guide.

However, it can help you prevent almost 90% of the popular backend attacks such as **brute force** login attempts and **DDoS.**

The best part is that you can implement them within an hour or two.

### Before You Begin.

1. You need a Linux server.
2. You need a basic understanding of the command line. [Here is a cheat sheet](https://learncodethehardway.org/unix/bash_cheat_sheet.pdf)you can use.

If you have the above requirements all set up, let us move on to the first step.

### 1\. Configure SSH Keys

To access a remote server, you will either have to log in with a password or use SSH keys.

The problem with passwords is that they are easy to brute force (*You will learn how to prevent this further below*). In addition, you will have to type them down anytime you need to access your server.

To avoid the above drawbacks, you will have to set up **SSH keys authentication**. It is more [secure than a password](https://security.stackexchange.com/a/69408) since hackers cannot brute force them.

It is also easier and faster to connect to the server as you do not need to enter a password.

Here is how to set up SSH authentication for your server.

* On your local computer, generate an SSH key pair by typing:

```bash  
ssh-keygen
```  

The above command will take you through a few steps to generate your SSH keys. Take note of the files where the keys will be stored.

* Add your public key to your server with the command:

```bash
ssh-copy-id username@remote_host
```

Be sure to replace *username *and *remote_host *with your real username and your server’s IP address. You will be prompted for a password.

* Try logging into your server with the command:

```bash
ssh username@remote_host
```

Don’t forget to replace *username *and *remote_host *with your server’s details. You should notice that this time you will not be prompted for a password.

### 2\. Keep Your System Time Up To Date

Many security protocols leverage your system time to run cron jobs, date logs and perform other critical tasks.

If your system time is incorrect, it could have negative impacts on your server. To prevent that from happening, you can install an NTP client. This client will keep your system time in-sync with [global NTP servers](https://en.wikipedia.org/wiki/Network_Time_Protocol).

Use the command below to install the NTP client:

```bash  
sudo apt install ntp
```  

You no longer have to worry about setting system dates again.

### 3\. View Active Ports

Applications on your server expose certain ports so that other applications within the network can access them.

Hackers can also [install a backdoor on your server](https://security.stackexchange.com/a/160410) and expose a port through which they can control the server.

For this reason, we don’t want your server listening for requests on ports we don’t know about.

To view active ports, use the following command:

```bash  
sudo ss -lntup
```  

Take a look at the output and investigate any port or process that does not seem familiar to you.

Try to spot and track down potentially harmful services and processes.

To get you started, check out this list of [“bad” TCP/UDP ports](https://www.garykessler.net/library/bad_ports.html).

### 4\. Set up a firewall

Firewalls allow you to stop/allow traffic to/from specific ports on your server. For this, I usually use UFW (*uncomplicated firewall).*

UFW works by letting you configure rules that:

* allow or deny
* incoming or outgoing traffic
* to or from
* specific or all ports

In this section, you will block all network traffic except those that you explicitly allow. As you install other programs, remember to enable the necessary ports required for it to run.

#### Setting up UFW

* Install ufw.

```bash
sudo apt-get install ufw
```

* You can either deny all outgoing traffic…

```bash  
sudo ufw default deny outgoing comment 'deny all outgoing traffic'
```  

* … or allow all outgoing traffic.

```bash  
sudo ufw default allow outgoing comment 'allow all outgoing traffic'
```  

* Next, we want to deny all incoming traffic…

```bash  
sudo ufw default deny incoming comment 'deny all incoming traffic'
```  

* …except SSH connections so that we can access the system.

```bash  
sudo ufw limit in ssh comment 'allow SSH connections in'
```  

* If you configured UFW to deny all outgoing traffic, do not forget to allow specific traffic as per your needs. Below are some examples:

```bash  
# allow traffic out on port 53 -- DNS
sudo ufw allow out 53 comment 'allow DNS calls out'

# allow traffic out on port 123 -- NTP
sudo ufw allow out 123 comment 'allow NTP out'

# allow traffic out for HTTP, HTTPS, or FTP
# apt might needs these depending on which sources you're using
sudo ufw allow out http comment 'allow HTTP traffic out'
sudo ufw allow out https comment 'allow HTTPS traffic out'
sudo ufw allow out ftp comment 'allow FTP traffic out'

# allow whois
sudo ufw allow out whois comment 'allow whois'

# allow traffic out on port 68 -- the DHCP client
# you only need this if you're using DHCP
sudo ufw allow out 68 comment 'allow the DHCP client to update'
```  

* To deny any traffic on port 99, use the command below:

```bash
sudo ufw deny 99
```

* Finally, start UFW using the command below:

```bash  
sudo ufw enable
```  

* You can also use the following command to view UFW status:

```bash  
sudo ufw status
```  

### 5\. Prevent Automated Attacks

There are two utilities that you can use to prevent most of the automated attacks:

* [PSAD](http://www.cipherdyne.org/psad/).
* [Fail2Ban](https://www.fail2ban.org/).

#### Difference between PSAD and Fail2Ban

We learned that ports provide access to the applications on your server.

An attacker may decide to scan your server for open ports that they may then use to access the server.

**PSAD **monitors network activity to detect and optionally block such scans and other types of suspect traffic such as DDoS or OS fingerprinting attempts.

**Fail2Ban,** on the other hand, scans log files of various applications such as FTP and automatically bans IPs that show malicious signs such as automated login attempts.

The following guides will show you how to install and configure PSAD and Fail2Ban so that they work with UFW.

* [Install Fail2Ban](https://zaiste.net/intro_fail2ban_with_ufw/).
* [Install PSAD](https://gist.github.com/netson/c45b2dc4e835761fbccc).

### 6\. Install logwatch

Applications on your server will often save log messages to log files. Unless you intend to manually monitor your log files, you need to install logwatch.

logwatch scans system log files and summarizes them.

You can run it directly from the command line or schedule it to run on a recurring schedule.For example, you can configure logwatch to email you a daily summary of your log files. Note that your server will need to be [able to send e-mails](https://gist.github.com/adamstac/7462202) for this to work.

logwatch uses service files to know how to read and summarize a log file. You can see all of the stock service files in `/usr/share/logwatch/scripts/services`.

logwatch’s configuration file `/usr/share/logwatch/default.conf/logwatch.conf` specifies default options. You can override them via command line arguments.

To install logwatch on Ubuntu or Debian, run the following command:

```bash
apt-get install logwatch
```

For users on other Linux distros, check out this [epic guide](https://www.linode.com/docs/uptime/monitoring/monitor-systems-logwatch/) by Linode.

You can try running logwatch directly in case you need to see a sample of what it collects.

```bash  
sudo /usr/sbin/logwatch --output stdout --format text --range yesterday --service all
```  

Finally, tell logwatch to send us a daily email containing a summary of our log files. To do this, open the file */etc/cron.daily/00logwatch* and find the *execute*line then change it to the following:

```bash
/usr/sbin/logwatch --output mail --format html --mailto root --range yesterday --service all
```

### 7\. Perform Security Audits

After securing your Linux server, you should perform security audits so as to spot any security loopholes that you may have missed.

To do this, you can use **Lynis**, an open source software that can perform:

* Security audits.
* Compliance testing (e.g. PCI, HIPAA, SOx).
* Penetration testing.
* Vulnerability detection.
* System Hardening.

#### How to use Lynis

First of all, Install Lynis by cloning their Github repository. This ensures that you install the latest version of Lynis.

```bash  
git clone [https://github.com/CISOfy/lynis](https://github.com/CISOfy/lynis)
```  

Switch to the directory that we cloned Lynis into:

```bash  
cd lynis
```  

Finally, use the following command to run your first audit:

```bash  
lynis audit system
```  

You can learn more about Lynis on their [official website](https://cisofy.com/lynis/).

### Conclusion

Congratulations on reading another how-to guide on hardening your Linux server. I hope you learned something new.



