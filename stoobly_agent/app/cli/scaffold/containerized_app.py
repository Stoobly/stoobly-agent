from .app import App

class ContainerizedApp(App):
  def __init__(self, path: str, scaffold_namespace: str, **kwargs):
    super().__init__(path, scaffold_namespace, **kwargs)