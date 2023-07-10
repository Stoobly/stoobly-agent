import uuid

class LocalDBAdapter():

  def success(self, d):
    return d, 200

  def bad_request(self, d = ''):
    return d, 400

  def not_found(self, d = 'Not Found'):
    return d, 404

  def internal_error(self, d = 'Internal Error'):
    return d, 500

  def validate_uuid(self, id: str):
    try:
      uuid.UUID(id)
      return True
    except Exception:
      return False