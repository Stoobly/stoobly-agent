import os
import pdb
import sys

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
    file_path = '/etc/hosts'
    if not os.path.exists(file_path):
      print(f"Error: File {file_path} not found.", file=sys.stderr)
      sys.exit(1)
    return file_path

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

    self.__add_lines_between_markers(
      hosts_file_path, SCAFFOLD_HOSTS_DELIMITTER_BEGIN, SCAFFOLD_HOSTS_DELIMITTER_END, hostnames
    )

  def uninstall_hostnames(self, hostnames: list[str] = []) -> None:
    hosts_file_path = self.__get_hosts_file_path()

    self.__remove_lines_between_markers(
      hosts_file_path, SCAFFOLD_HOSTS_DELIMITTER_BEGIN, SCAFFOLD_HOSTS_DELIMITTER_END, hostnames
    ) 

  def __remove_lines_between_markers(self, file_path, start_marker, end_marker, hostnames = []):
    with open(file_path, "r") as file:
      lines = file.readlines()

    filtered_lines = []
    index = 0

    # Continue until we reach start_marker
    for line in lines:
      index += 1

      if start_marker in line:
        break

      filtered_lines.append(line)

    # Continue until we reach end_marker
    found_hostnames = {}
    section = []
    for line in lines[index:]:
      index += 1

      if end_marker in line:
        break
        
      found = False
      for hostname in hostnames:
        if hostname in line:
          if hostname not in found_hostnames:
            print(f"Removing hostname {hostname}")

          found_hostnames[hostname] = True
          found = True

      if not found: 
        section.append(line)

    # If there are still lines in the section
    if len(section):
      filtered_lines.append(start_marker)
      section.append(end_marker)    
      filtered_lines += section

    for line in lines[index:]:
      filtered_lines.append(line)

    with open(file_path, "w") as file:
      file.writelines(filtered_lines)

  def __add_lines_between_markers(self, file_path, start_marker, end_marker, hostnames = []):
    with open(file_path, "r") as file:
      lines = file.readlines()

    filtered_lines = []
    index = 0

    # Continue until we reach start_marker
    for line in lines:
      index += 1
      if start_marker in line:
        break

      filtered_lines.append(line)

    # If no empty line before start_marker, add one
    if len(filtered_lines):
      last_line = filtered_lines[-1]

      if last_line != "\n":
        filtered_lines.append("\n")

    filtered_lines.append(start_marker)

    # Continue until we reach end_marker
    found_hostnames = {}
    for line in lines[index:]:
      index += 1

      if end_marker in line:
        break
        
      found = False
      for hostname in hostnames:
        if hostname in line:
          filtered_lines.append(line)
          found_hostnames[hostname] = True
          found = True

      if not found:
        filtered_lines.append(line)
      
    for hostname in hostnames:
      if hostname in found_hostnames:
        continue

      print(f"Installing hostname {hostname}")
      filtered_lines.append(f"127.0.0.1 {hostname}\n")
      filtered_lines.append(f"::1       {hostname}\n")

    filtered_lines.append(end_marker)    

    for line in lines[index:]:
      filtered_lines.append(line)

    with open(file_path, "w") as file:
      file.writelines(filtered_lines)