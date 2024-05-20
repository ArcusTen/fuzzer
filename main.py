import dns.resolver
import os
import subprocess
import argparse
import socket 

def fuzz_dns(domain):
    # Function to perform basic DNS queries for a given domain
    try:
        # A record query:
        a_record = dns.resolver.resolve(domain, 'A')
        print("\nA Record:", a_record.response.answer, "\n")

        # AAAA record query:
        aaaa_record = dns.resolver.resolve(domain, 'AAAA')
        print("AAAA Record:", aaaa_record.response.answer, "\n")

        # MX record query:
        mx_record = dns.resolver.resolve(domain, 'MX')
        print("MX Record:", mx_record.response.answer, "\n")

        # NS record query:
        ns_record = dns.resolver.resolve(domain, 'NS')
        print("NS Record:", ns_record.response.answer, "\n")

        # TXT record query:
        txt_record = dns.resolver.resolve(domain, 'TXT')
        print("TXT Record:", txt_record.response.answer, "\n")

        # SRV record query:
        srv_record = dns.resolver.resolve(domain, 'SRV')
        print("SRV Record:", srv_record.response.answer,"\n")

    except dns.resolver.NoAnswer:
        print("No DNS records found.\n")
    except dns.resolver.NXDOMAIN:
        print("Domain does not exist.\n")
    except dns.resolver.Timeout:
        print("DNS query timed out.\n")
    except dns.resolver.NoNameservers:
        print("No nameservers found.\n")

def check_subdomains(domain, subdomains_file):
    # Function to check existence of subdomains of a given domain
    try:
        with open(subdomains_file, 'r') as f:
            subdomains = f.readlines()
            for subdomain in subdomains:
                subdomain = subdomain.strip()
                target = subdomain + '.' + domain
                # Capture the output of the ping command
                response = subprocess.run(['ping', '-c', '1', target], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                # Check if the return code is 0 (indicating success)
                if response.returncode == 0:
                    print(f"{target} \t\t[YES]")
                else:
                    print(f"{target} \t\t[NO]")
    except FileNotFoundError:
        print("Subdomains file not found.\n Exiting....")

def reverse_dns_lookup(ip_address):
    # Function to perform reverse DNS lookup for an IP address
    try:
        hostname = socket.gethostbyaddr(ip_address)
        print(f"Reverse DNS Lookup: {ip_address} -> {hostname}")
    except socket.herror:
        print(f"No reverse DNS entry found for {ip_address}")

def brute_force_subdomain(domain, wordlist):
    # Function to brute force subdomains using a wordlist
    try:
        with open(wordlist, 'r') as f:
            subdomains = f.readlines()
            for subdomain in subdomains:
                subdomain = subdomain.strip()
                target = subdomain + '.' + domain
                try:
                    # Perform a DNS query for the subdomain
                    dns.resolver.resolve(target)
                    print(f"{target} \t\t[FOUND]")
                except dns.resolver.NXDOMAIN:
                    print(f"{target} \t\t[NOT FOUND]")
    except FileNotFoundError:
        print("Wordlist file not found.")


def main():
    # Main function to parse command-line arguments and execute appropriate functions
    parser = argparse.ArgumentParser(description="\tPerform DNS queries and check subdomains.")
    parser.add_argument("-d", "--domain", help="\tDomain to perform DNS queries on")
    parser.add_argument("-s", "--subdomains", help="\tFile containing list of subdomains")
    parser.add_argument("-w", "--wordlist", help="\tWordlist for brute force subdomain enumeration")
    # parser.add_argument("-n", "--nameserver", help="\tNameserver for DNS zone transfer")
    parser.add_argument("-i", "--ip", help="\tIP address for reverse DNS lookup")
    args = parser.parse_args()

    if args.ip:
        ip_address = args.ip
        reverse_dns_lookup(ip_address)
        return

    if args.domain:
        domain = args.domain
        fuzz_dns(domain)

        if args.subdomains:
            subdomains_file = args.subdomains
            check_subdomains(domain, subdomains_file)

        if args.wordlist:
            wordlist = args.wordlist
            brute_force_subdomain(domain, wordlist)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
