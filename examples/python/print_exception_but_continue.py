import traceback

print("running\n\n")

try:
    raise TypeError("Oups!")
except Exception:
    print("oh no... about to print(my exception")
    traceback.print_exc()

print("still alive")

print("running again\n\n")

try:
    raise TypeError("Oups!")
except Exception:
    s = traceback.format_exc()
    print("oh no... here is the exception")
    print(s)

print("still alive here")
