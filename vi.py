import os
import sys

def text_editor(file_path):
    # Load file or create new content
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
    else:
        lines = [""]

    cursor_x = 0
    cursor_y = 0

    def render_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
        for i, line in enumerate(lines):
            prefix = "> " if i == cursor_y else "  "
            print(prefix + line.rstrip())
        print(f"\nCTRL+S to save, CTRL+Q to quit. Current Line: {cursor_y + 1}, Cursor: {cursor_x}")

    def save_file():
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print("File saved!")

    try:
        import termios, tty

        def get_key():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # Escape sequence
                    seq = sys.stdin.read(2)
                    ch += seq
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    except ImportError:
        raise RuntimeError("This editor requires a Unix-like environment.")

    while True:
        render_screen()
        key = get_key()

        if key == '\x1b[A':  # Up arrow
            cursor_y = max(0, cursor_y - 1)
            cursor_x = min(cursor_x, len(lines[cursor_y]))

        elif key == '\x1b[B':  # Down arrow
            cursor_y = min(len(lines) - 1, cursor_y + 1)
            cursor_x = min(cursor_x, len(lines[cursor_y]))

        elif key == '\x1b[C':  # Right arrow
            if cursor_x < len(lines[cursor_y]):
                cursor_x += 1
            elif cursor_y < len(lines) - 1:
                cursor_y += 1
                cursor_x = 0

        elif key == '\x1b[D':  # Left arrow
            if cursor_x > 0:
                cursor_x -= 1
            elif cursor_y > 0:
                cursor_y -= 1
                cursor_x = len(lines[cursor_y])

        elif key == '\x7f':  # Backspace
            if cursor_x > 0:
                lines[cursor_y] = lines[cursor_y][:cursor_x - 1] + lines[cursor_y][cursor_x:]
                cursor_x -= 1
            elif cursor_y > 0:
                cursor_x = len(lines[cursor_y - 1])
                lines[cursor_y - 1] += lines.pop(cursor_y)
                cursor_y -= 1

        elif key == '\r':  # Enter
            new_line = lines[cursor_y][cursor_x:]
            lines[cursor_y] = lines[cursor_y][:cursor_x]
            lines.insert(cursor_y + 1, new_line)
            cursor_y += 1
            cursor_x = 0

        elif key == '\x13':  # CTRL+S
            save_file()

        elif key == '\x11':  # CTRL+Q
            break

        elif len(key) == 1 and 32 <= ord(key) <= 126:  # Printable characters
            lines[cursor_y] = lines[cursor_y][:cursor_x] + key + lines[cursor_y][cursor_x:]
            cursor_x += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python editor.py <file_path>")
    else:
        text_editor(sys.argv[1])
