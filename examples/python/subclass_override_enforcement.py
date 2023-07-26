class MyBase:
    def __init__(self):
        pass


    def mustoverride(self):
        raise NotImplementedError("oh no")

class SubClass(MyBase):
    def __init__(self):
        super().__init__()

    def mustoverride(self):
        print("neat")

class MissingOverride(MyBase):
    def __init__(self):
        super().__init__()

good_sub = SubClass()
good_sub.mustoverride()

bad_sub = MissingOverride()
bad_sub.mustoverride()
