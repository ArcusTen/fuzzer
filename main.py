# Importing necessary libraries for DNS resolution, OS operations, subprocess management, argument parsing, and socket operations
import dns.resolver
import os
import subprocess
import argparse
import socket

# Function to perform various DNS queries for a given domain
def fuzz_dns(domain):
    try:
        # Resolving and printing the A record (IPv4 address) for the domain
        a_record = dns.resolver.resolve(domain, 'A')
        for rdata in a_record:
            print(f"{domain} has address {rdata.to_text()}\n")

        # Resolving and printing the NS record (name servers) for the domain
        ns_record = dns.resolver.resolve(domain, 'NS')
        for rdata in ns_record:
            print(f"Name Server: {domain} name server {rdata.to_text()}")

        # Resolving and printing the MX record (mail servers) for the domain
        mx_record = dns.resolver.resolve(domain, 'MX')
        print("\n")
        for rdata in mx_record:
            print(f"Mail Server: {domain} mail is handled by {rdata.preference} {rdata.exchange.to_text()}")
        
        # Resolving and printing the AAAA record (IPv6 address) for the domain
        aaaa_record = dns.resolver.resolve(domain, 'AAAA')
        print("\nAAAA Record:", aaaa_record.response.answer, "\n")

        # Resolving and printing the TXT record (text records) for the domain
        txt_record = dns.resolver.resolve(domain, 'TXT')
        print("TXT Record:", txt_record.response.answer, "\n")

    # Handling exceptions for various DNS resolution errors
    except dns.resolver.NoAnswer:
        print("No DNS records found.\n")
    except dns.resolver.NXDOMAIN:
        print("Domain does not exist.\n")
    except dns.resolver.Timeout:
        print("DNS query timed out.\n")
    except dns.resolver.NoNameservers:
        print("No nameservers found.\n")

# Function to check subdomains for a given domain from a file containing subdomain list
def check_subdomains(domain, subdomains_file):
    try:
        # Opening the file containing the list of subdomains
        with open(subdomains_file, 'r') as f:
            subdomains = f.readlines()
            for subdomain in subdomains:
                subdomain = subdomain.strip()
                target = subdomain + '.' + domain
                # Pinging the subdomain to check its availability
                response = subprocess.run(['ping', '-c', '1', target], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                if response.returncode == 0:
                    print(f"{target} \t\t[YES]")
                else:
                    print(f"{target} \t\t[NO]")
    # Handling the case where the subdomain file is not found
    except FileNotFoundError:
        print("Subdomains file not found.\n Exiting....")

# Function to perform a reverse DNS lookup for a given IP address
def reverse_dns_lookup(ip_address):
    try:
        # Performing the reverse DNS lookup and printing the associated hostname
        hostname = socket.gethostbyaddr(ip_address)
        print(f"Reverse DNS Lookup: {ip_address} -> {hostname}")
    # Handling the case where no reverse DNS entry is found
    except socket.herror:
        print(f"No reverse DNS entry found for {ip_address}")

# Function to query and print SRV records for a given service, protocol, and domain
def srv_records(service, protocol, domain):
    query = f"_{service}._{protocol}.{domain}"
    try:
        # Resolving the SRV records and printing the details
        answers = dns.resolver.resolve(query, 'SRV')
        for rdata in answers:
            print(f"Priority: {rdata.priority}, Weight: {rdata.weight}, Port: {rdata.port}, Target: {rdata.target}")
    # Handling exceptions for various DNS resolution errors
    except dns.resolver.NoAnswer:
        print("No SRV records found.")
    except dns.resolver.NXDOMAIN:
        print("Domain does not exist.")
    except dns.resolver.Timeout:
        print("Query timed out.")
    except dns.exception.DNSException as e:
        print(f"An error occurred: {e}")

# Main function to parse command-line arguments and call the appropriate functions
def main():
    parser = argparse.ArgumentParser(description="\tPerform DNS queries and check subdomains.")
    parser.add_argument("-d", "--domain", help="\tDomain to perform DNS queries on")
    parser.add_argument("-s", "--subdomains", help="\tFile containing list of subdomains")
    parser.add_argument("--srv", help="\tTo get SRV Record in the format 'service:protocol:domain'")
    parser.add_argument("-i", "--ip", help="\tIP address for reverse DNS lookup")
    args = parser.parse_args()

    # If an IP address is provided, perform reverse DNS lookup
    if args.ip:
        ip_address = args.ip
        reverse_dns_lookup(ip_address)
        return

    # If a domain is provided, perform DNS queries
    if args.domain:
        domain = args.domain
        fuzz_dns(domain)

        # If a subdomains file is provided, check subdomains
        if args.subdomains:
            subdomains_file = args.subdomains
            check_subdomains(domain, subdomains_file)
        return

    # If SRV record arguments are provided, query SRV records
    if args.srv:
        srv_parts = args.srv.split(':')
        if len(srv_parts) == 3:
            service, protocol, domain = srv_parts
            srv_records(service, protocol, domain)
        else:
            print("SRV record argument must be in the format 'service:protocol:domain'")
        return

    # If no arguments are provided, print the help message
    else:
        parser.print_help()

# If this script is executed directly, run the main function
if __name__ == "__main__":
    main()
