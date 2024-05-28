# Text Attributes
A_NORMAL = curses.A_NORMAL           # Normal display (no highlight)
A_STANDOUT = curses.A_STANDOUT       # Best highlighting mode available
A_UNDERLINE = curses.A_UNDERLINE     # Underlined text
A_REVERSE = curses.A_REVERSE         # Reverse-video mode
A_BLINK = curses.A_BLINK             # Blinking text
A_DIM = curses.A_DIM                 # Half-bright mode
A_BOLD = curses.A_BOLD               # Extra bright or bold text
A_PROTECT = curses.A_PROTECT         # Protected mode
A_INVIS = curses.A_INVIS             # Invisible or blank mode
A_ALTCHARSET = curses.A_ALTCHARSET   # Alternate character set
A_CHARTEXT = curses.A_CHARTEXT       # Bit-mask to extract a character

# Color Attributes
COLOR_BLACK = curses.COLOR_BLACK     # Black color
COLOR_RED = curses.COLOR_RED         # Red color
COLOR_GREEN = curses.COLOR_GREEN     # Green color
COLOR_YELLOW = curses.COLOR_YELLOW   # Yellow color
COLOR_BLUE = curses.COLOR_BLUE       # Blue color
COLOR_MAGENTA = curses.COLOR_MAGENTA # Magenta color
COLOR_CYAN = curses.COLOR_CYAN       # Cyan color
COLOR_WHITE = curses.COLOR_WHITE     # White color

# Color Pair Attributes
# Note: To use COLOR_PAIR(n), initialize color pairs using curses.init_pair(n, fg, bg)
COLOR_PAIR = curses.COLOR_PAIR       # Macro to generate color pair number

# Window and Input Attributes
# Window manipulation and input handling methods
def window_methods(win):
    win.addch()        # Add a character at the current cursor position
    win.addstr()       # Add a string at the current cursor position
    win.attroff()      # Turn off the specified attributes
    win.attron()       # Turn on the specified attributes
    win.attrset()      # Set the specified attributes
    win.bkgd()         # Set the background property of the window
    win.clear()        # Clear the window
    win.clrtobot()     # Clear the window from the current line to the bottom
    win.clrtoeol()     # Clear the window from the current cursor position to the end of the line
    win.getch()        # Get a character from the window
    win.getstr()       # Get a string from the window
    win.refresh()      # Refresh the window to apply changes
