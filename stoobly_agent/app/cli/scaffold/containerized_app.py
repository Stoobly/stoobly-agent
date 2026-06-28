from .app import App

# Host paths (app-dir-path, context-dir-path, etc.) are passed via kwargs for compose env.
# Operational paths resolve under STOOBLY_HOME_DIR inside the container.
class ContainerizedApp(App):
  def __init__(self, **kwargs):
    kwargs['containerized'] = True
    super().__init__(None, **kwargs)
