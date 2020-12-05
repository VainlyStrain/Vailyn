import sys

colors = True # Output should be colored
machine = sys.platform # Detecting the os of current system
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False # Colors shouldn't be displayed in mac & windows
if not colors:
    end = red = white = green = yellow = run = bad = good = info = que = ''
else:
    white = '\033[0m'
    green = '\033[0m'
    red = '\033[0m\033[38;2;58;49;58m'
    yellow = '\033[0m'
    end = '\033[0m'
    back = '\033[7;0m'
    info = '\033[0m\033[38;2;58;49;58m[!]\033[0m'
    que = '\033[0m\033[38;2;58;49;58m[?]\033[0m'
    bad = '\033[0m\033[38;2;58;49;58m[-]\033[0m'
    good = '\033[0m[+]\033[0m'
    run = '\033[0m[~]\033[0m'
