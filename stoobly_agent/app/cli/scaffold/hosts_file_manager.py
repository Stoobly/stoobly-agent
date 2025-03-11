import pdb
import platform

from dataclasses import dataclass
from typing import Union

SCAFFOLD_HOSTS_DELIMITTER_BEGIN = "##### STOOBLY SCAFFOLD HOSTS BEGIN #####\n"
SCAFFOLD_HOSTS_DELIMITTER_END = "##### STOOBLY SCAFFOLD HOSTS END #####\n"

class HostsFileManager():

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

  def install_hostnames(self, hostnames: list[str]) -> None:
    hosts_file_path = self.__get_hosts_file_path()

    self.remove_lines_between_markers(
      hosts_file_path, SCAFFOLD_HOSTS_DELIMITTER_BEGIN, SCAFFOLD_HOSTS_DELIMITTER_END
    )

    with open(hosts_file_path, 'a+') as f:
      if SCAFFOLD_HOSTS_DELIMITTER_BEGIN not in f.read():
        f.write(SCAFFOLD_HOSTS_DELIMITTER_BEGIN)

      for hostname in hostnames:
        print(f"Installing hostname {hostname} to {hosts_file_path}")
        f.write(f"127.0.0.1 {hostname}\n")
        f.write(f"::1       {hostname}\n")

      if SCAFFOLD_HOSTS_DELIMITTER_END not in f.read():
        f.write(SCAFFOLD_HOSTS_DELIMITTER_END)

  def uninstall_hostnames(self) -> None:
    hosts_file_path = self.__get_hosts_file_path()

    self.remove_lines_between_markers(
      hosts_file_path, SCAFFOLD_HOSTS_DELIMITTER_BEGIN, SCAFFOLD_HOSTS_DELIMITTER_END
    ) 

    print(f"Uninstalled hostnames from {hosts_file_path}")

  def remove_lines_between_markers(self, file_path, start_marker, end_marker):
    with open(file_path, "r") as file:
      lines = file.readlines()
    
    inside_block = False
    filtered_lines = []

    for line in lines:
      if start_marker in line:
        inside_block = True
        continue  # Skip the start marker line
      if end_marker in line:
        inside_block = False
        continue  # Skip the end marker line
      if not inside_block:
        filtered_lines.append(line)

    with open(file_path, "w") as file:
      file.writelines(filtered_lines)