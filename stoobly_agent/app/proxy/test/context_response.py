class TestContextResponse():

  def __init__(self):
    self.content = ''
    self.status_code = None

  def with_content(self, content):
    self.content = content
    return self

  def with_status_code(self, status_code):
    self.status_code = status_code
    return self
