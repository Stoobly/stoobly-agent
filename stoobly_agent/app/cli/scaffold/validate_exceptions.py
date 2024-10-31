

class ScaffoldValidateException(Exception):
  pass

class ScaffoldValidateGatewayMissingException(ScaffoldValidateException):
  pass

class ScaffoldValidateGatewayFoundException(ScaffoldValidateException):
  pass

class ScaffoldValidateStooblyUiMissingException(ScaffoldValidateException):
  pass

class ScaffoldValidateStooblyUiFoundException(ScaffoldValidateException):
  pass

class ScaffoldValidateNotDetachedException(ScaffoldValidateException):
  pass

class ScaffoldValidateEntrypointMissingException(ScaffoldValidateException):
  pass



