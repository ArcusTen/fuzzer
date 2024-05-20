# DNS Fuzzer

A Python script for performing DNS queries, checking subdomains, brute forcing subdomains, attempting DNS zone transfer and conducting reverse DNS lookups.

## Requirements

- Python 3.x
- `dnspython` library (install via `pip install dnspython` or use `pip install -r requirements.txt`)

## Usage

```bash
python main.py [-h] [-d DOMAIN] [-s SUBDOMAINS_FILE] [-w WORDLIST] [-n NAMESERVER] [-i IP_ADDRESS]
```

## Options

- `-h, --help`: Show the help message and exit.
- `-d DOMAIN`, `--domain DOMAIN`: Domain to perform DNS queries on.
- `-s SUBDOMAINS_FILE`, `--subdomains SUBDOMAINS_FILE`: File containing a list of subdomains.
- `-w WORDLIST`, `--wordlist WORDLIST`: Wordlist for brute force subdomain enumeration.
- `-n NAMESERVER`, `--nameserver NAMESERVER`: Nameserver for DNS zone transfer.
- `-i IP_ADDRESS`, `--ip IP_ADDRESS`: IP address for reverse DNS lookup.

## Features

- **Basic DNS Queries:** Perform basic DNS queries (A, AAAA, MX, NS, TXT, SRV) for a given domain.
- **Check Subdomains:** Check the existence of subdomains of a given domain using a provided subdomains file.
- **Brute Force Subdomains:** Brute force subdomains using a wordlist.
- **Attempt DNS Zone Transfer:** Attempt DNS zone transfer using a specified nameserver.
- **Reverse DNS Lookup:** Perform reverse DNS lookup for a given IP address.

## Sample Command

```bash
python3 dns_fuzzer.py -d thecyberthesis.com -s domains.txt -w wordlist.txt -n ns1.thecyberthesis.com -i 89.117.139.205
```

## Dependencies

- `dns.resolver`: Python library for DNS resolution.
- `argparse`: Python library for parsing command-line arguments.
- `socket`: Standard Python library for socket operations.
- `subprocess`: Standard Python library for subprocess management.