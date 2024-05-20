# DNS Fuzzer

This Python script enables you to perform DNS queries, check subdomains, perform reverse DNS lookups, and query SRV records.

## Requirements

- Python 3.x
- `dnspython` library (install via `pip install dnspython` or use `pip install -r requirements.txt`)

## Features

- **DNS Queries:** Resolve and print various DNS records for a given domain.
- **Subdomain Checking:** Check the availability of subdomains from a provided list.
- **Reverse DNS Lookup:** Perform a reverse DNS lookup for a given IP address.
- **SRV Record Querying:** Query and print SRV records for a specific service, protocol, and domain.

## Command Line Arguments
- `-d`, `--domain`: Domain to perform DNS queries on.
- `-s`, `--subdomains`: File containing a list of subdomains to check.
- `--srv`: To get SRV Record in the format 'service:protocol:domain'.
- `-i`, `--ip`: IP address for reverse DNS lookup.

## Example Usage
1. Perform DNS queries on a domain:
   ```bash
   python main.py -d google.com
   ```

2. Check subdomains for a domain:
   ```bash
   python main.py -d thecyberthesis.com -s subdomains.txt
   ```

3. Perform a reverse DNS lookup for an IP address:
   ```bash
   python main.py -i 8.8.4.4
   ```

4. Query SRV records:
   ```bash
   python main.py --srv service:protocol:example.com
   ```


## Dependencies

- `dns.resolver`: Python library for DNS resolution.
- `argparse`: Python library for parsing command-line arguments.
- `socket`: Standard Python library for socket operations.
- `subprocess`: Standard Python library for subprocess management.
- `os`: Operating system's library to make syscalls.
