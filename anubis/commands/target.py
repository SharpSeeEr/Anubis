"""The target command."""
import os
import re
import socket
import sys
import threading
from urllib.parse import urlsplit

from anubis.scanners.anubis_db import search_anubisdb, send_to_anubisdb
from anubis.scanners.crt import search_crtsh
from anubis.scanners.dnsdumpster import search_dnsdumpster
from anubis.scanners.dnssec import dnssecc_subdomain_enum
from anubis.scanners.hackertarget import subdomain_hackertarget
from anubis.scanners.netcraft import search_netcraft
from anubis.scanners.nmap import scan_host
from anubis.scanners.recursive import recursive_search
from anubis.scanners.shodan import search_shodan
from anubis.scanners.spyse import search_spyse
from anubis.scanners.ssl import search_subject_alt_name
from anubis.scanners.sublist3r import search_sublist3r
from anubis.scanners.zonetransfer import dns_zonetransfer
from anubis.utils.color_print import ColorPrint
from .base import Base


class Target(Base):
  """Main enumeration module"""
  domains = list()
  dedupe = set()

  stdout = sys.stdout

  def handle_exception(self, e, message=""):
    if self.options["--verbose"]:
      print(e)
    if message:
      ColorPrint.red(message)

  def init(self):
    if self.options["FILE"]:
      full_path = os.path.join(os.getcwd(), self.options["FILE"])
      with open(full_path) as file:
        self.options["TARGET"] = list(filter(None, file.read().split('\n')))
    else:
      self.options["TARGET"] = list(
        filter(None, self.options["TARGET"].split(",")))
    # Clean up targets
    for i in range(len(self.options["TARGET"])):
      url = self.options["TARGET"][i]
      # Inject protocol if not there
      if not re.match(r'http(s?):', url):
        url = 'http://' + url

      parsed = urlsplit(url)
      host = parsed.netloc

      self.options["TARGET"][i] = host

      try:
        ip_str = socket.gethostbyname(host)
        ColorPrint.green(f"Searching for subdomains for {ip_str} ({host})")
      except Exception as e:
        self.handle_exception(e,
                              "Error connecting to target! Make sure you spelled it correctly and it is a resolvable address")

  def run(self):
    # Retrieve IP of target and run initial configurations
    self.init()
    # If multiple targets, create scans for each
    for i in range(len(self.options["TARGET"])):
      # Default scans that run every time
      target = self.options["TARGET"][i]
      ColorPrint.green(f"Working on target: {target}")
      threads = [threading.Thread(target=dns_zonetransfer, args=(self, target)),
                 threading.Thread(target=search_sublist3r,
                                  args=(self, target)),
                 threading.Thread(target=subdomain_hackertarget,
                                  args=(self, target)),
                 threading.Thread(target=search_subject_alt_name,
                                  args=(self, target)),
                 threading.Thread(target=search_netcraft, args=(self, target)),
                 threading.Thread(target=search_crtsh, args=(self, target)),
                 threading.Thread(target=search_dnsdumpster,
                                  args=(self, target)),
                 threading.Thread(target=search_spyse,
                                  args=(self, target)),
                 threading.Thread(target=search_anubisdb, args=(self, target))]

      # Additional options - shodan.io scan
      if self.options["--additional-info"]:
        threads.append(threading.Thread(target=search_shodan, args=(self,)))

      # Additional options - nmap scan of dnssec script and a host/port scan
      if self.options["--with-nmap"]:
        threads.append(
          threading.Thread(target=dnssecc_subdomain_enum, args=(self, target)))
        threads.append(threading.Thread(target=scan_host, args=(self, target)))

      # Start all threads and wait for them to finish
      with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda thread: thread.run(), threads)


      # Run a recursive search on each subdomain - rarely useful, but nice to have
      # just in case
      if self.options["--recursive"]:
        recursive_search(self)

      # remove duplicates and clean up
      self.domains = self.clean_domains(self.domains)
      self.dedupe = set(self.domains)

      print("Found", len(self.dedupe), "subdomains")
      print("----------------")

      if self.options["--ip"]:
        self.resolve_ips()
      else:
        for domain in self.dedupe:
          cleaned_domain = domain.strip()
          ColorPrint.green(cleaned_domain)
          if self.options['--silent']:
            sys.stdout.write(cleaned_domain + '\n', override=True)

      if not self.options["--dont-send-to-anubis-db"]:
        send_to_anubisdb(self, [target])
      # reset per domain
      self.domains = list()

  def resolve_ips(self):
    unique_ips = set()
    for domain in self.dedupe:
      try:
        # Attempt to get IP
        resolved_ip = socket.gethostbyname(domain)
      except Exception as e:
        # If getting IP fails, fallback to empty string
        resolved_ip = ""
      # TODO - Align domains and ips in stdout
      ColorPrint.green(domain + ": " + resolved_ip)
      if self.options['--silent']:
        sys.stdout.write(domain + '\n', override=True)

      if resolved_ip:
        unique_ips.add(resolved_ip)
    print("Found %s unique IPs" % len(unique_ips))
    for ip in unique_ips:
      # Ignore empty strings, final sanity check
      if ip:
        ColorPrint.green(ip)

@staticmethod
def clean_domains(domains):
    """
    Cleans and normalizes a list of domain strings.

    Args:
        domains (list): List of raw subdomain strings.

    Returns:
        list: Cleaned and normalized subdomain strings.
    """
    cleaned = []
    for subdomain in domains:
        subdomain = subdomain.lower()

        # Remove protocol prefix (http:// or https://)
        if "//" in subdomain:
            subdomain = subdomain.split("//", 1)[-1]

        # Remove trailing dot (e.g., 'example.com.')
        if subdomain.endswith('.'):
            subdomain = subdomain[:-1]

        # Remove leading special characters (e.g., '/www.example.com')
        while subdomain and subdomain[0] in ["\\", ".", "/", "#", "$", "%"]:
            subdomain = subdomain[1:]

        # Handle email addresses (e.g., 'user@example.com')
        if "@" in subdomain:
            subdomain = subdomain.split("@")[-1]

        cleaned.append(subdomain.strip())
    return cleaned

