"""
pytermkit - A lightweight terminal toolkit for Python.

Provide terminal color, font styling, cursor control
and utility functions using ANSI escape codes.
No dependencies required except standard library.

Classes:
    Colors: ANSI color codes for foreground and background.
    Fonts: ANSI font style codes with activate/deactivate support.
    Term: Terminal utilities (clear, typewriter, color/font management).
    Cursor: Cursor movement and visibility control.

Example:
    from pytermkit import Term, Colors, Cursor

    Term.set_color("red", "blue")
    Term.set_font(("bold", True))
    Term.typewriter("Hello World!")
    Term.clear()
"""

#!######## TODO LIST #########
# TODO: Remove the fg and bg setter functions in v2, since set_color can set both.
# TODO: In v2, make set_color select a color from either RGB values or a string and validate it automatically.
# TODO: Add terminal UI helper functions, such as typewriter-style output.


import ast
from time import sleep
from getpass import getpass

class Colors:
    """ANSI color codes for terminal output.

    Example:
        Colors.fg["red"]
        Colors.bg["blue"]
        print(Colors.get_color_rgb((255, 255, 255), (10, 10, 10)))
    """
    fg = {
        "reset": "\x1b[39m",
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "purple": "\x1b[35m",
        "cyan": "\x1b[36m",
        "gray": "\x1b[90m",
        "light_red": "\x1b[91m",
        "light_green": "\x1b[92m",
        "light_yellow": "\x1b[93m",
        "light_blue": "\x1b[94m",
        "light_purple": "\x1b[95m",
        "light_cyan": "\x1b[96m",
        "light_gray": "\x1b[37m"
        }
    bg = {
        "reset": "\x1b[49m",
        "red": "\x1b[41m",
        "green": "\x1b[42m",
        "yellow": "\x1b[43m",
        "blue": "\x1b[44m",
        "purple": "\x1b[45m",
        "cyan": "\x1b[46m",
        "gray": "\x1b[47m"
        }
    
    @staticmethod
    def get_color_rgb(fg: tuple=(255, 255, 255), bg: tuple=(0, 0, 0)) -> dict:
        """Return ANSI color code from rgb codes.
        
        Args:
            fg: Foreground color rgb code, gets a tuple. (Default: (255, 255, 255))
            bg: Background color rgb code, gets a tuple. (Default: (0, 0, 0))
        
        Example:
            Colors.get_color_rgb((255, 20, 20), (20, 0, 255)) (Returns color ANSI code, print to use.)
            Colors.get_color_rgb(fg=(100, 150, 70), bg=(10, 100, 110)) (Returns color ANSI code, print to use.)
        """
        if len(fg)!=3 or len(bg)!=3:
            raise ValueError("RGB colors must contain exactly 3 values.")

        for value in fg + bg:            
            if not isinstance(value, int):
                raise TypeError("RGB values must be integers.")
            elif not 0 <= value <= 255:
                raise ValueError(f"RGB must be 0-255, got {value}")

        rgb = {}
        rgb["fg"] = f"\x1b[38;2;{fg[0]};{fg[1]};{fg[2]}m"
        rgb["bg"] = f"\x1b[48;2;{bg[0]};{bg[1]};{bg[2]}m"
        return rgb


class Fonts:
    """ANSI font codes for terminal output.
    
    Example:
        Fonts.font["bold"][True] # activate bold
        Fonts.font["bold"][False] # deactivate bold
    """
    font = {
        "reset": {True:"\x1b[0m",
                  False: "\x1b[0m"},
        
        "bold": {True: "\x1b[1m",
                 False: "\x1b[22m"},

        "italic": {True: "\x1b[3m",
                   False: "\x1b[23m"},

        "underline": {True: "\x1b[4m",
                      False: "\x1b[24m"},
        "double_underline": {
            True: "\x1b[21m",
            False: "\x1b[24m"},

        "blink": {True: "\x1b[5m",
                  False: "\x1b[25m"},

        "reverse": {True: "\x1b[7m",
                    False: "\x1b[27m"},

        "hidden": {True: "\x1b[8m",
                   False: "\x1b[28m"},

        "strike": {True: "\x1b[9m",
                   False: "\x1b[29m"}
    }


class Term:
    """Useful methods for the terminal.
    
    Methods:
        clear
        clear_line
        typewriter
        add_lines
        set_fg_color
        set_bg_color
        set_font
        set_color
        set_color_rgb
    """
    @staticmethod
    def set_color(fg: str="reset", bg: str="reset") -> None:
        """Set the terminal color.
        
        Args:
            fg: Foreground color, gets a string. (Default: "reset")
            bg: Background color, gets a string. (Default: "reset")
        
        Example:
            term.set_color("red", "blue")
        """
        if fg.lower() not in Colors.fg.keys() or bg.lower() not in Colors.bg.keys():
            raise ValueError(f"Unknown color:{fg} or {bg}")
        fg = Colors.fg[fg.lower()]
        bg = Colors.bg[bg.lower()]
        print(fg + bg, end="")

    @staticmethod
    def set_fg_color(color: str) -> None:
        """
        Set terminal foreground color.
        
        Args:
            color: New color of the terminal, gets a string.
        
        Example:
            Term.set_fg_color("green")
        """
        if color.lower() not in Colors.fg:
            raise ValueError(f"Unknown foreground color: {color}")
        
        print(Colors.fg[color.lower()], end="")

    @staticmethod
    def set_bg_color(color: str) -> None:
        """
        Set terminal background color.
        
        Args:
            color: New color of the terminal, gets a string.
        
        Example:
            Term.set_bg_color("green")
        """
        if color.lower() not in Colors.bg:
            raise ValueError(f"Unknown background color: {color}")
                
        print(Colors.bg[color.lower()], end="")        

    @staticmethod
    def set_color_rgb(fg: tuple=(255, 255, 255), bg: tuple=(0, 0, 0)) -> None:
        """Set terminal color with rgb.
        
        Args:
            fg: Foreground color rgb codes, gets a tuple. (Default: (255, 255, 255))
            bg: Background color rgb codes, gets a tuple. (Default: (0, 0, 0))
        
        Example:
            term.set_color_rgb((255, 20, 20), (20, 0, 255))
            term.set_color_rgb(fg=(100, 150, 70), bg=(10, 100, 110))
        """
        if not (len(fg)==3 and len(bg)==3):
            raise ValueError(f"RGB must contain exactly 3 values, got ({len(fg)}, {len(bg)}).")

        for value in fg + bg: 
            if not isinstance(value, int):
                raise TypeError(f"RGB values must be integers.")

            elif not 0 <= value <= 255:
                raise ValueError(f"RGB must be 0-255, got {value}")
        

        fg = f"\x1b[38;2;{fg[0]};{fg[1]};{fg[2]}m"
        bg = f"\x1b[48;2;{bg[0]};{bg[1]};{bg[2]}m"
        print(fg+bg, end="")

    @staticmethod
    def set_font(fnt: tuple) -> None:
        """Set terminal font style.
        
        Args:
            fnt: tuple of (font_name, bool)
        
        Example:
            Term.set_font(("bold", True))
            Term.set_font(("italic", False))
        """
        if len(fnt) != 2:
            raise IndexError("Font setter requires a tuple of (font_name, bool).")
        
        elif not isinstance(fnt[0], str):
            raise TypeError(f"Font name must be string, got {type(fnt[0])}")
        
        elif fnt[0].lower() not in Fonts.font.keys():
            raise ValueError(f"Unknown font name: {fnt[0]}")
        
        elif not isinstance(fnt[1], bool):
            raise TypeError(f"Font status must be bool. Got: {fnt[1]}")

        print(Fonts.font[fnt[0].lower()][fnt[1]], end="")

    @staticmethod
    def clear() -> None:
        """Clear the terminal screen."""
        print("\x1b[2J\x1b[H\x1b[3J", end="")
    
    @staticmethod
    def clear_line() -> None:
        """Clear the entire line."""
        print("\x1b[2K", end="")

    @staticmethod
    def typewriter(*args, delay: float=0.05, sep=" ", end="\n") -> None:
        """
        Print text with a typewriter effect.
        
        Args:
            args: The text to print.
            delay: Seconds between each characters, gets a float. (Default: 0.05)
            sep: Separator between arguments, gets any type. (Default: " ")
            end: End character after all text, gets any type. (Default: "\n")
        
        Example:
            Term.typewriter("Hello", "World", delay=0.3, sep="-", end="")
        """
        if delay < 0:
            raise ValueError(f"Delay value cannot be less than 0, got {delay}.")
        
        text = [] # Contain the args items.
        for arg in args:
            arg = str(arg)
            text.append(arg)

        for i, txt in enumerate(text): # Iterate over the words in the list: text.
            for letter in txt: # Iterate over the letters in the word: txt.
                print(letter, end="", flush=True)
                sleep(delay) # Typerwriter effect.

            if i < len(text) - 1: # If the loop is not on the last word.
                print(sep, end="", flush=True)

        print(end=end, flush=True)


    @staticmethod
    def add_lines(n: int=1) -> None:
        """Add new void line.
        
        Args:
            n: Number of lines, gets int. (Default: 1)
        
        Example:
            Term.add_lines(10)
        """
        if n < 0:
            raise ValueError(f"Number of lines cannot be less than 0, got {n}.")
        print(n * "\n", end="")
    

class Cursor:
    """Useful methods for the cursor.
    
    Methods:
        up
        down
        right
        left
        to_column
        save
        restore
        hide
        show
    """
    @staticmethod
    def up(n: int = 1) -> None:
        """ Print ANSI code to move the cursor up.
        Args:
            n: Number of lines to move. (Default: 1)
        
        Example:
            Cursor.up(3)
        """
        if n < 0:
            raise ValueError(f"Number of lines cannot be less than 0, got {n}.")
        print(f"\x1b[{n}A", end="")
    
    @staticmethod
    def down(n: int = 1) -> None:
        """Print ANSI code to move the cursor down.
        
        Args:
            n: Number of lines to move.
        
        Example:
            Cursor.down(1)
        """
        if n < 0:
            raise ValueError(f"Number of lines cannot be less than 0, got {n}.")
        print(f"\x1b[{n}B", end="")
    
    @staticmethod
    def right(n: int = 1) -> None:
        """Print ANSI code to move the cursor right.
        
        Args:
            n: Number of columns to move.
        
        Example:
            Cursor.right(5)
        """ 
        if n < 0:
            raise ValueError(f"Number of column cannot be less than 0, got {n}.")
        print(f"\x1b[{n}C", end="")
    
    @staticmethod
    def left(n: int = 1) -> None:
        """Print ANSI code to move the cursor left.
        
        Args:
            n: Number of columns to move.
        
        Example:
            Cursor.left(3)
        """
        if n < 0:
            raise ValueError(f"Number of column cannot be less than 0, got {n}.")
        print(f"\x1b[{n}D", end="")
    
    @staticmethod
    def to_column(n: int) -> None:
        """Print ANSI code to move the cursor to column number.
        
        Args:
            n: Column number.
        
        Example:
            Cursor.to_column(10)
        """
        if n < 1:
            raise ValueError(f"Number of column cannot be less than 1, got {n}.")
        print(f"\x1b[{n}G", end="")
    
    @staticmethod
    def save() -> None:
        """Save the current cursor position."""
        print("\x1b[s", end="")
    
    @staticmethod
    def restore() -> None:
        """Move the cursor to last saved position."""
        print("\x1b[u", end="")
    
    @staticmethod
    def hide() -> None:
        """Hide the cursor."""
        print("\x1b[?25l", end="")


    @staticmethod
    def show() -> None:
        """Show the cursor."""
        print("\x1b[?25h", end="")


class Test:
    """Interactive test interface for pytermkit.

    Provides menus to test colors, font styles, terminal utilities,
    cursor controls, and class/method information.

    Used to demonstrate and verify the functionality of pytermkit.
    """

    pytermkit = f"{Colors.get_color_rgb((0, 140, 255))["fg"]}pyterm{Colors.get_color_rgb((10, 230, 110))["fg"]}kit"

    banner = f"""
    {Colors.get_color_rgb((0, 140, 255))["fg"]}______  __      __    ______________ ________ ______                        {Colors.get_color_rgb((10, 230, 110))["fg"]}__  ____________
    {Colors.get_color_rgb((0, 140, 255))["fg"]}|#####\\ \\#\\    /#/    |############| |#######||#####\\  |\\        /|{Colors.get_color_rgb((10, 230, 110))["fg"]}|#|  /#/|##||############|
    {Colors.get_color_rgb((0, 140, 255))["fg"]}|##  ##\\ \\#\\  /#/     |----|  |----| |##|-----|##  ##\\ |#\\      /#|{Colors.get_color_rgb((10, 230, 110))["fg"]}|#| /#/ |##||----|  |----|
    {Colors.get_color_rgb((0, 140, 255))["fg"]}|##  ##/  \\#\\/#/           |##|      |##|____ |##  ##/ |##\\    /##|{Colors.get_color_rgb((10, 230, 110))["fg"]}|#|/#/  |##|     |##|
    {Colors.get_color_rgb((0, 140, 255))["fg"]}|##__#/    |##|            |##|      |#######||##__#/  |###\\  /###|{Colors.get_color_rgb((10, 230, 110))["fg"]}|###|   |##|     |##|
    {Colors.get_color_rgb((0, 140, 255))["fg"]}|##|       |##|            |##|      |##|-----|##|\\#\\  |#|\\#\\/#/|#|{Colors.get_color_rgb((10, 230, 110))["fg"]}|#|\\#\\  |##|     |##|
    {Colors.get_color_rgb((0, 140, 255))["fg"]}|##|       |##|            |##|      |##|____ |##| \\#\\ |#|      |#|{Colors.get_color_rgb((10, 230, 110))["fg"]}|#| \\#\\ |##|     |##|
    {Colors.get_color_rgb((0, 140, 255))["fg"]}|##|       |##|            |##|      |#######||##|  \\#\\|#|      |#|{Colors.get_color_rgb((10, 230, 110))["fg"]}|#|  \\#\\|##|     |##|{Colors.fg["reset"]}
          """

    main_menu = """
    1) Test Colors 
    2) Test Fonts
    3) Class / Method Documentation
    4) Class / Method Test

    0) Quit
    """
    
    colors_menu = """
    1) Foreground Colors
    2) Background Colors
    3) RGB
    
    0) Back
    Q) Quit
    """
    
    fg_colors_menu = """
    1) reset
    2) red
    3) green
    4) yellow
    5) blue
    6) purple
    7) cyan
    8) gray
    9) light_red
    10) light_green
    11) light_yellow
    12) light_blue
    13) light_purple
    14) light_cyan
    15) light_gray

    0) Back
    Q) Quit
    """

    bg_colors_menu = """
    1) reset
    2) red
    3) green
    4) yellow
    5) blue
    6) purple
    7) cyan
    8) gray

    0) Back
    Q) Quit
    """
    
    fonts_menu = """
    1) bold
    2) italic
    3) underline
    4) double_underline
    5) blink
    6) reverse
    7) hidden
    8) strike
    
    0) Back
    Q) Quit
    """

    class_methods_menu = """
    1) Colors
    2) Fonts
    3) Term:
        Methods:
        3.1) set_color
        3.2) set_fg_color
        3.3) set_bg_color
        3.4) set_color_rgb
        3.5) set_font
        3.6) clear
        3.7) clear_line
        3.8) typewriter
        3.9) add_lines
    4) Cursor:
        Methods:
        4.1) up
        4.2) down
        4.3) right
        4.4) left
        4.5) to_column
        4.6) save
        4.7) restore
        4.8) hide
        4.9) show

    0) Back
    Q) Quit
    """

    colors_methods_menu = """
    1) get_color_rgb

    0) Back
    Q) Quit
    """

    fonts_methods_menu = """
    Fonts has no public methods to test.

    0) Back
    Q) Quit
    """
    
    test_term_methods_menu = """
    1) set_color
    2) set_fg_color
    3) set_bg_color
    4) set_color_rgb
    5) set_font
    6) clear
    7) clear_line
    8) typewriter
    9) add_lines

    0) Back
    Q) Quit
    """
    
    test_cursor_methods_menu = """
    1) up
    2) down
    3) right
    4) left
    5) to_column
    6) save
    7) restore
    8) hide
    9) show

    0) Back
    Q) Quit
    """

    @staticmethod
    def print_banner(typewriter: bool = True):
        """Print the banner for the test interface."""
        Cursor.hide()
        if typewriter:
            Term.typewriter(Test.banner, delay=0.001, end="\n\n")
        else:
            print(Test.banner + "\n\n")
        Cursor.show()

    @staticmethod
    def invalid_option():
        """Print an invalid option message."""
        Term.clear()
        Term.set_color("red")
        Term.typewriter("Invalid option. Please try again.", delay=0.03)
        sleep(1)
        Term.set_color("reset")
        Term.clear()
    
    @staticmethod
    def error(text):
        Term.clear()
        Term.set_color("red")
        Term.typewriter(text, delay=0.03)
        sleep(1)
        Term.set_color("reset")
        Term.clear()
    
    @staticmethod
    def bye():
        """Print a goodbye message."""
        Term.clear()
        Term.set_color("reset")
        Term.set_font(("reset", True))
        Cursor.show()
        Term.typewriter(f"Bye! Thanks for using {Test.pytermkit}.", delay=0.03)
        sleep(1.5)
        Term.clear()

    @staticmethod
    def run_method_test(method, qualified_name, document: bool, test: bool):
        """Optionally show method documentation and test it with literal arguments."""
        if not isinstance(document, bool) or not isinstance(test, bool):
            print("Warning: document and test must be bool values.")
            return False
        if not document and not test:
            print("Warning: document or test must be True; method was not run.")
            return False

        if document:
            Term.clear()
            print(f"Documentation for {qualified_name}:")
            print(method.__doc__ or "No documentation available.")
            if not test:
                input("Press enter to continue")
                return False
            input("Press enter to continue to the test")

        if test:
            Term.clear()
            print("Enter arguments only; the closing parenthesis is optional.")
            print("Type 'back' to return or 'quit' to exit.")

        while True:
            try:
                arguments = input(f"{qualified_name}(").strip()
            except EOFError:
                return True

            command = arguments.lower()
            if command == "back":
                Term.set_color("reset")
                Term.set_font(("reset", True))
                Cursor.show()
                return False
            if command in ("q", "quit"):
                return True

            try:
                try:
                    call = ast.parse(f"{qualified_name}({arguments})", mode="eval").body
                except SyntaxError:
                    if not arguments.endswith(")"):
                        raise
                    call = ast.parse(f"{qualified_name}({arguments[:-1]})", mode="eval").body
                if not isinstance(call, ast.Call):
                    raise ValueError("Input must contain method arguments only.")
                expected_function = ast.parse(qualified_name, mode="eval").body
                if ast.dump(call.func) != ast.dump(expected_function):
                    raise ValueError("Input must contain arguments for the selected method only.")

                positional_args = [ast.literal_eval(argument) for argument in call.args]
                keyword_args = {}
                for keyword in call.keywords:
                    if keyword.arg is None:
                        raise ValueError("Keyword unpacking is not supported.")
                    keyword_args[keyword.arg] = ast.literal_eval(keyword.value)

                result = method(*positional_args, **keyword_args)
                if result is not None:
                    print(result)
                print("Method call completed.")
            except Exception as error:
                print(f"Method call failed: {type(error).__name__}: {error}")


def main():
    """Main function to run the interactive test interface."""
    Term.clear()
    while True:
        Test.print_banner()
        sleep(0.7)
        print(Test.main_menu)
        Term.add_lines(2)
        choice = input("Select an option: ")
        match choice.strip():
            case "1":
                # Test colors
                Term.clear()
                while True:
                    Test.print_banner(typewriter=False)
                    print(Test.colors_menu)
                    Term.add_lines(2)
                    color_choice = input("Select an option: ")
                    match color_choice.lower().strip():
                        case "1":
                            # Test foreground colors
                            Term.clear()
                            while True:
                                Term.set_color("reset")
                                Term.clear()
                                Test.print_banner(typewriter=False)
                                print(Test.fg_colors_menu)
                                Term.add_lines(2)
                                fg_choice = input("Select an option: ").strip().lower()
                                match fg_choice:
                                    case "1":
                                        Term.set_color("reset")
                                    case "2":
                                        Term.set_color("red")
                                    case "3":
                                        Term.set_color("green")
                                    case "4":
                                        Term.set_color("yellow")
                                    case "5":
                                        Term.set_color("blue")
                                    case "6":
                                        Term.set_color("purple")
                                    case "7":
                                        Term.set_color("cyan")
                                    case "8":
                                        Term.set_color("gray")
                                    case "9":
                                        Term.set_color("light_red")
                                    case "10":
                                        Term.set_color("light_green")
                                    case "11":
                                        Term.set_color("light_yellow")
                                    case "12":
                                        Term.set_color("light_blue")
                                    case "13":
                                        Term.set_color("light_purple")
                                    case "14":
                                        Term.set_color("light_cyan")
                                    case "15":
                                        Term.set_color("light_gray")
                                    case "0":
                                        Term.set_color("reset")
                                        Term.clear()
                                        break
                                    case "q":
                                        Term.set_color("reset")
                                        Test.bye()
                                        return
                                    case _:
                                        Test.invalid_option()
                                        continue
                                
                                Term.clear()
                                print("Type something to see the color effect ('back' to return, 'quit' to quit)")
                                while True:
                                    input_text = input("=> ")
                                    if input_text.lower().strip() == "quit":
                                        Term.set_color("reset")
                                        Term.clear()
                                        Test.bye()
                                        return
                                    elif input_text.lower().strip() == "back":
                                        Term.set_color("reset")
                                        Term.clear()
                                        break

                        case "2":
                            # Test background colors
                            Term.clear()
                            while True:
                                Term.set_color("reset")
                                Term.clear()
                                Test.print_banner(typewriter=False)
                                print(Test.bg_colors_menu)
                                Term.add_lines(2)
                                bg_choice = input("Select an option: ")
                                match bg_choice.lower().strip():
                                    case "1":
                                        Term.set_color(bg="reset")
                                    case "2":
                                        Term.set_color(bg="red")
                                    case "3":
                                        Term.set_color(bg="green")
                                    case "4":
                                        Term.set_color(bg="yellow")
                                    case "5":
                                        Term.set_color(bg="blue")
                                    case "6":
                                        Term.set_color(bg="purple")
                                    case "7":
                                        Term.set_color(bg="cyan")
                                    case "8":
                                        Term.set_color(bg="gray")
                                    case "0":
                                        Term.set_color("reset")
                                        Term.clear()
                                        break
                                    case "q":
                                        Term.set_color("reset")
                                        Test.bye()
                                        return
                                    case _:
                                        Test.invalid_option()
                                        continue
                                Term.clear()
                                print("Type something to see the color effect ('back' to return, 'quit' to quit)")
                                while True:
                                    input_text = input("=> ")
                                    if input_text.lower().strip() == "quit":
                                        Term.set_color("reset")
                                        Term.clear()
                                        Test.bye()
                                        return
                                    elif input_text.lower().strip() == "back":
                                        Term.set_color("reset")
                                        Term.clear()
                                        break
                        case "3":
                            while True:
                                try:
                                    Term.set_color("reset")
                                    Term.clear()
                                    Test.print_banner()
                                    rgb = input("Enter RGB values as 'r g b r g b' (foreground first, then background). Enter 'quit' to quit or 'back' to go back: ")
                                    if rgb.strip().lower() == "quit":
                                        Term.set_color("reset")
                                        Test.bye()
                                        return
                                    elif rgb.strip().lower() == "back":
                                        Term.set_color("reset")
                                        Term.clear()
                                        break
                                    rgb = tuple(rgb.split())
                                    if len(rgb) != 6:
                                        raise ValueError("Exactly six RGB values are required.")
                                    fg_rgb = tuple([int(i) for i in rgb][:3])
                                    bg_rgb = tuple([int(i) for i in rgb][3:])
                                    Term.set_color_rgb(fg_rgb, bg_rgb)
                                    print("This is how your text will look in the selected colors.")
                                    getpass("Press enter to continue")
                                    Term.set_color("reset")
                                    Term.clear()
                                except (TypeError, ValueError):
                                    Test.error("The format must be: r g b r g b")
                                

                        case "0":
                            Term.clear()
                            break
                        case "q":
                            Test.bye()
                            return
                        case _:
                            Test.invalid_option()
                            continue
                    
            case "2":
                # Test fonts
                font_names = (
                    "bold",
                    "italic",
                    "underline",
                    "double_underline",
                    "blink",
                    "reverse",
                    "hidden",
                    "strike",
                )
                Term.clear()
                while True:
                    Test.print_banner(typewriter=False)
                    print(Test.fonts_menu)
                    Term.add_lines(2)
                    font_choice = input("Select an option: ").lower().strip()
                    if font_choice in (str(index) for index in range(1, len(font_names) + 1)):
                        Term.set_font((font_names[int(font_choice) - 1], True))
                    elif font_choice == "0":
                        Term.set_font(("reset", True))
                        Term.clear()
                        break
                    elif font_choice == "q":
                        Term.set_font(("reset", True))
                        Test.bye()
                        return
                    else:
                        Test.invalid_option()
                        continue

                    Term.clear()
                    print("Type something to see the font effect ('back' to return, 'q' to quit)")
                    while True:
                        input_text = input("=> ")
                        if input_text.lower().strip() == "q":
                            Term.set_font(("reset", True))
                            Term.clear()
                            Test.bye()
                            return
                        elif input_text.lower().strip() == "back":
                            Term.set_font(("reset", True))
                            Term.clear()
                            break
            case "3" | "4":
                document_mode = choice.strip() == "3"
                Term.clear()
                while True:
                    Test.print_banner(typewriter=False)
                    print(Test.class_methods_menu)
                    Term.add_lines(2)
                    class_method_choice = input("Select a class (You must select a class before selecting a method; do not enter values like 3.2.): ").lower().strip()
                    match class_method_choice:
                        case "1":
                            while True:
                                Term.clear()
                                Test.print_banner(typewriter=False)
                                print(Test.colors_methods_menu)
                                Term.add_lines(2)
                                colors_method_choice = input("Select a method: ").lower().strip()
                                match colors_method_choice:
                                    case "1":
                                        if Test.run_method_test(Colors.get_color_rgb, "Colors.get_color_rgb", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "0":
                                        Term.clear()
                                        break
                                    case "q":
                                        Test.bye()
                                        return
                                    case _:
                                        Test.invalid_option()
                        case "2":
                            while True:
                                Term.clear()
                                Test.print_banner(typewriter=False)
                                print(Test.fonts_methods_menu)
                                Term.add_lines(2)
                                fonts_method_choice = input("Select an option: ").lower().strip()
                                match fonts_method_choice:
                                    case "0":
                                        Term.clear()
                                        break
                                    case "q":
                                        Test.bye()
                                        return
                                    case _:
                                        Test.invalid_option()
                        case "3":
                            Term.clear()
                            while True:
                                Term.clear()
                                Test.print_banner(typewriter=False)
                                print(Test.test_term_methods_menu)
                                Term.add_lines(2)
                                term_method_choice = input("Select a method: ").lower().strip()
                                match term_method_choice:
                                    case "1":
                                        if Test.run_method_test(Term.set_color, "Term.set_color", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "2":
                                        if Test.run_method_test(Term.set_fg_color, "Term.set_fg_color", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "3":
                                        if Test.run_method_test(Term.set_bg_color, "Term.set_bg_color", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "4":
                                        if Test.run_method_test(Term.set_color_rgb, "Term.set_color_rgb", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "5":
                                        if Test.run_method_test(Term.set_font, "Term.set_font", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "6":
                                        if Test.run_method_test(Term.clear, "Term.clear", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "7":
                                        if Test.run_method_test(Term.clear_line, "Term.clear_line", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "8":
                                        if Test.run_method_test(Term.typewriter, "Term.typewriter", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "9":
                                        if Test.run_method_test(Term.add_lines, "Term.add_lines", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "0":
                                        Term.clear()
                                        break
                                    case "q":
                                        Test.bye()
                                        return
                                    case _:
                                        Test.invalid_option()
                        case "4":
                            while True:
                                Term.clear()
                                Test.print_banner(typewriter=False)
                                print(Test.test_cursor_methods_menu)
                                Term.add_lines(2)
                                cursor_method_choice = input("Select a method: ").lower().strip()
                                match cursor_method_choice:
                                    case "1":
                                        if Test.run_method_test(Cursor.up, "Cursor.up", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "2":
                                        if Test.run_method_test(Cursor.down, "Cursor.down", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "3":
                                        if Test.run_method_test(Cursor.right, "Cursor.right", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "4":
                                        if Test.run_method_test(Cursor.left, "Cursor.left", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "5":
                                        if Test.run_method_test(Cursor.to_column, "Cursor.to_column", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "6":
                                        if Test.run_method_test(Cursor.save, "Cursor.save", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "7":
                                        if Test.run_method_test(Cursor.restore, "Cursor.restore", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "8":
                                        if Test.run_method_test(Cursor.hide, "Cursor.hide", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "9":
                                        if Test.run_method_test(Cursor.show, "Cursor.show", document=document_mode, test=not document_mode):
                                            Test.bye()
                                            return
                                    case "0":
                                        Term.clear()
                                        break
                                    case "q":
                                        Test.bye()
                                        return
                                    case _:
                                        Test.invalid_option()
                        case "0":
                            Term.clear()
                            break
                        case "q":
                            Test.bye()
                            return
                        case _:
                            Test.invalid_option()
                
            case "0":
                Test.bye()
                break
            case _:
                Test.invalid_option()
    
    
    Term.set_color("reset")

if __name__ == "__main__":
    main()