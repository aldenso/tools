"""My notes to remember decorators."""
VALIDUSER = "aldenso"
NOTVALIDUSER = "nobody"


def upperme(func):
    """Deco to change the output to uppercase."""
    def applyupper(name):
        return "{}".format(func(name).upper())
    return applyupper


def tagme(tag):
    """Deco to wrap the output with some string."""
    def tag_decorator(func):
        def func_wrapper(name):
            return "{} {} {}".format(tag, func(name), tag)
        return func_wrapper
    return tag_decorator


def only_aldenso(func):
    """Deco to check that only aldenso can run the desired function."""
    def checkaldenso(name):
        if name == VALIDUSER:
            return func(name)
        else:
            exit("Not Authorized!")
    return checkaldenso


@only_aldenso
@tagme("<h1>")
@upperme
def saymyname(name):
    """Say your name."""
    message = "My Name is {}".format(name)
    return message


if __name__ == "__main__":
    print("Running with valid user:")
    print(saymyname(VALIDUSER))
    print("Running with not valid user:")
    print(saymyname(NOTVALIDUSER))

# Output:
# Running with valid user:
# <h1> MY NAME IS ALDENSO <h1>
# Running with not valid user:
# Not Authorized!
