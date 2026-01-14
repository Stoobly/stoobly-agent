from .app import App

class ContainerizedApp(App):
  def __init__(self, path: str, **kwargs):
    super().__init__(path, **kwargs)