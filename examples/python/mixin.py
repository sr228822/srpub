class BaseClass:
    def __init__(self, name):
        print(f"BaseClass init {name}")

        self.name = name


class MyMixin:
    def __init__(self, *args, **kwargs):
        print("MyMixin init")
        self.mixer = 1


class SuperClass(BaseClass, MyMixin):
    def __init__(self, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)
        MyMixin.__init__(self, *args, **kwargs)


sc = SuperClass("hello")
print(sc.__class__)
