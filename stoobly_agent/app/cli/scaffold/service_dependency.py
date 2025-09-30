import pdb
import re

from typing import Optional

class ServiceDependency():
    def __init__(self, s: str):
      parts = s.rsplit(":", 2)  # split from the right, at most twice
      if len(parts) != 3:
          raise ValueError(f"Invalid format: {s}. Expected 'IMAGE:HOSTNAME:PORT'")
      
      self.image, self.hostname, self.port = parts
      
      # Basic validation
      if not self.image:
          raise ValueError("Image name cannot be empty")
      if not self.hostname:
          raise ValueError("Hostname cannot be empty")
      if not self.port.isdigit():
          raise ValueError(f"Port must be a number, got: {self.port}")
      
      self.port = int(self.port)
    
    def __repr__(self):
        return f"ImageHostPort(image='{self.image}', hostname='{self.hostname}', port={self.port})"

    @property
    def image_name(self):
        return DockerImage(self.image).name

class DockerImage:
    def __init__(self, ref: str):
        # Regex based on Docker image spec
        pattern = r"""
            ^(?:(?P<registry>[^/]+?)/)?     # optional registry (no slash)
            (?P<name>[^:@]+(?:/[^:@]+)*)    # image name (can have slashes)
            (?::(?P<tag>[^@]+))?             # optional :tag
            (?:@(?P<digest>.+))?             # optional @digest
        """
        match = re.fullmatch(pattern, ref, re.VERBOSE)
        if not match:
            raise ValueError(f"Invalid Docker image reference: {ref}")
        
        self.registry: Optional[str] = match.group("registry")
        self.name: str = match.group("name")
        self.tag: Optional[str] = match.group("tag")
        self.digest: Optional[str] = match.group("digest")

    def __repr__(self):
        return (f"DockerImage(registry={self.registry!r}, "
                f"name={self.name!r}, tag={self.tag!r}, digest={self.digest!r})")
