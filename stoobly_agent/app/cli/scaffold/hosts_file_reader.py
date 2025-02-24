import pdb
import platform
from dataclasses import dataclass
from typing import Union


class HostsFileReader():

  @dataclass
  class IpAddressToHostnames:
    ip_address: str
    hostnames: list[str]

  def __get_hosts_file_path(self) -> str:
    system = platform.system()
    if system == 'Linux' or system == 'Darwin':
      return '/etc/hosts'
    else:
      print(f"Unsupported system: {system}, for hosts file validation, skipping")

    return ''

  # Split IP address and hostnames. Don't include inline comments
  def __split_hosts_line(self, line: str) -> list[str]:
    ip_addr_hosts_split = line.split('#')[0].split()
    return ip_addr_hosts_split


  # Parses hosts file and returns a mapping of IP address to hostnames in a list.
  def get_hosts(self) -> list[IpAddressToHostnames]:
    hosts_file_path = self.__get_hosts_file_path()

    if not hosts_file_path:
      return []

    with open(hosts_file_path, 'r') as f:
      hostlines = f.readlines()

    # Skip comments and empty lines
    hostlines = [line.strip() for line in hostlines
                 if not line.startswith('#') and line.strip() != '']

    hosts = []
    for line in hostlines:
      ip_addr_hosts_split = self.__split_hosts_line(line)
      ip_address = ip_addr_hosts_split[0]
      hostnames = ip_addr_hosts_split[1:]
      ipAddressToHostnames = self.IpAddressToHostnames(ip_address, hostnames)

      hosts.append(ipAddressToHostnames)

    return hosts

  def find_host(self, hostname) -> Union[IpAddressToHostnames, None]:
    hosts = self.get_hosts()

    for mapping in hosts:
      if ((mapping.ip_address == '0.0.0.0' or mapping.ip_address == '127.0.0.1') and
        hostname in mapping.hostnames):

        return mapping

    return None


