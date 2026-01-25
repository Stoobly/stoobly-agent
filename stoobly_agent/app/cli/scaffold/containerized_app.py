from .app import App

# Intention is to not pass kwargs to ContainerizedApp to avoid overriding path options e.g. --context-dir-path
# In a containerized environment, the context-dir-path is the cwd
# However, passing kwargs is still allowed if needed
class ContainerizedApp(App):
  def __init__(self, path: str, **kwargs):
    super().__init__(path, **kwargs)