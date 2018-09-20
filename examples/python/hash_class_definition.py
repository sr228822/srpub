import hashlib; print hashlib.md5(str(User.__dict__.keys() + [type(getattr(User, k)) for k in User.__dict__.keys()])).digest()
