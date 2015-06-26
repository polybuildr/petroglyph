class tcolors:
    BLUE = '\033[38;5;4m'
    GREEN = '\033[38;5;2m'
    ORANGE = '\033[38;5;3m'
    RED = '\033[38;5;1m'
    END = '\033[0m'

INFO, SUCCESS, WARNING, ERROR = range(4)


def log(message, type=INFO):
    if type is INFO:
        print tcolors.BLUE + message + tcolors.END
    elif type is SUCCESS:
        print tcolors.GREEN + message + tcolors.END
    elif type is WARNING:
        print tcolors.ORANGE + message + tcolors.END
    elif type is ERROR:
        print tcolors.RED + message + tcolors.END
    else:
        print message
