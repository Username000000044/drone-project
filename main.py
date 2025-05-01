import curses

from objectives.path import run_path
from objectives.swarm import run_swarm


def swarm(): # Swarm function
    run_swarm()

def path(): # Path function
    run_path()

def show_menu(stdscr, selected_idx):
    stdscr.clear()
    menu = ["Swarm", "Path"]
    for idx, item in enumerate(menu):
        if idx == selected_idx:
            stdscr.addstr(idx, 0, f"> {item}", curses.A_REVERSE)  # Highlight selected item
        else:
            stdscr.addstr(idx, 0, f"  {item}")
    
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    selected_idx = 0

    while True:
        show_menu(stdscr, selected_idx)
        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            selected_idx = (selected_idx + 1) % 2  # Wrap around to the first option
        elif key == curses.KEY_UP:
            selected_idx = (selected_idx - 1) % 2  # Wrap around to the last option
        elif key == 10:  # Enter key
            if selected_idx == 0:
                swarm()
            elif selected_idx == 1:
                path()
            break  # Exit after selecting

        # Add a small delay for smooth navigation
        curses.napms(100) # wtf does this even do

if __name__ == "__main__":
    curses.wrapper(main)
