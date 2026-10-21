from time import sleep
import json
from pathlib import Path
from pynput import keyboard

from core import game
from assets.UI import *
from lib.pytermkit import Term
from lib.pytermkit import Cursor
from lib.pytermkit import Colors

# File paths
BASE_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = BASE_DIR / "config" / "settings.json"
DATA_FILE = BASE_DIR / "data" / "data.json"


# Load settings
settings = {}

def load_json():
    with open(SETTINGS_FILE, "r") as s:
        global settings, up_key, down_key, right_key, left_key, wall, food, head, body, mode, modes, frame_delay_x, frame_delay_y, speed_factor, mode, data, max_score
        settings = json.load(s)
        # Keys
        up_key = settings["keys"]["up"]
        down_key = settings["keys"]["down"]
        right_key = settings["keys"]["right"]
        left_key = settings["keys"]["left"]
        # Images
        wall = settings["game"]["wall"]
        food = settings["game"]["food"]
        head = settings["snake"]["head"]
        body = settings["snake"]["body"]
        # Game
        modes = settings["game"]["mode"]
        mode = settings["game"]["current mode"]
        frame_delay_x = modes[mode]["frame delay x"]
        frame_delay_y = modes[mode]["frame delay y"]
        speed_factor = modes["0"]["speed factor"]

    # Get data
    with open(DATA_FILE, "r") as d:
        data = json.load(d)
        max_score = data["max score"]

def dump_json(obj, file):
    with open(file, "w") as s:
        json.dump(obj=obj, fp=s, indent=4)

new_game = game.Game()

def game_over(text, score):
    Cursor.down(5)
    Term.set_color("red")
    print(text)
    sleep(1.5)
    Term.clear()
    Term.typewriter("GAME OVER!", delay=0.05)
    sleep(0.5)
    Term.set_color("green")
    Term.typewriter(f"Your score: {score}")
    sleep(1.6)
    Term.set_color("reset")

def alert(message):
    Term.clear()
    Term.set_color("red")
    Term.typewriter(message)
    sleep(1.2)
    Term.clear()
    Term.set_color("reset")

def start_animaton():
    pass

def draw_game(obj: game.Game,):
    game = ""
    for y, row in enumerate(obj.game_area):
        line = ""
        for x, col in enumerate(row):
            if col == 0:
                if obj.snake[0] == [y, x]:
                    line += Colors.fg["green"]
                    line += head
                    line += Colors.fg["purple"]

                elif [y, x] in obj.snake:
                    line += Colors.fg["green"]
                    line += body
                    line += Colors.fg["purple"]

                else:
                    line += " "

            elif col == 1:
                line += Colors.fg["red"]
                line += food
                line += Colors.fg["purple"]

            elif col == 2:
                line += Colors.fg["purple"]
                line += wall

        game += line + "\n"
        Term.set_color("reset")
    print(game)

pressed = None            
def on_press(key):
    global pressed
    try:
        pressed = key.char
    except:
        pressed = key


def main():
    while True:
        load_json()
        Term.clear()
        Cursor.show()
        Term.add_lines(10)
        print(main_menu)
        option = input("\n==> ")
        option = option.strip()

        if option == "0": # Exit
            Term.clear()
            Term.typewriter("Goodbye!")
            sleep(1.5)
            Term.clear()
            Term.set_color("reset")
            exit()
        
        elif option == "1": # Start
            global mode
            Cursor.hide()
            load_json()
            new_game.snake = [new_game.generate_position()]
            if not any(1 in row for row in new_game.game_area):
                new_game.add_food()
            new_game.score = 0
            new_game.snake_going = ""
            frame_delay_x = modes[mode]["frame delay x"]
            frame_delay_y = modes[mode]["frame delay y"]
            Term.clear()
            Term.set_color("blue")
            listener = keyboard.Listener(on_press=on_press)
            listener.start()

            while True:
                Term.set_color("blue", "gray")
                print(" " * len(f"     Score: {new_game.score}     Best: {max_score[mode]}     "))
                print(f"     Score: {new_game.score}     Best: {max_score[mode]}     ")
                print(" " * len(f"     Score: {new_game.score}     Best: {max_score[mode]}     "))
                draw_game(new_game)
                Term.add_lines()
                while pressed == None:
                    continue
                Cursor.to_column(1)
                print(" " * len("Press any key to start"), end="")
                Cursor.to_column(1)
                print(" " * len("Press any key to start "))

                # Snake control.
                if pressed == up_key:
                    if new_game.snake_going != "down":
                        new_game.snake_go_up()
                    else:
                        new_game.snake_go_down()

                elif pressed == left_key:
                    if new_game.snake_going != "right":
                        new_game.snake_go_left()
                    else:
                        new_game.snake_go_right()

                elif pressed == down_key:
                    if new_game.snake_going != "up":
                        new_game.snake_go_down()
                    else:
                        new_game.snake_go_up()

                elif pressed == right_key:
                    if new_game.snake_going != "left":
                        new_game.snake_go_right()
                    else:
                        new_game.snake_go_left()

                elif pressed == "q": # Exit.
                    Term.set_color("reset")
                    break
                
                else:
                    if new_game.snake_going == "down":
                        new_game.snake_go_down()

                    elif new_game.snake_going == "up":
                        new_game.snake_go_up()
                    
                    elif new_game.snake_going == "right":
                        new_game.snake_go_right()
                    
                    elif new_game.snake_going == "left":
                        new_game.snake_go_left()
                
                # Game over check
                if new_game.is_snake_hit_wall():
                    game_over("Oops, you hit the wall :(", new_game.score)
                    if new_game.score > max_score[mode]:
                        max_score[mode] = new_game.score
                        data["max score"][mode] = new_game.score
                        dump_json(data, DATA_FILE)
                    Term.clear()
                    break
                
                if new_game.is_snake_ate_itself():
                    game_over("Oops, you ate yourself :(", new_game.score)
                    if new_game.score > max_score[mode]:
                        max_score[mode] = new_game.score
                        data["max score"][mode] = new_game.score
                        dump_json(data, DATA_FILE)
                    Term.clear()
                    break
                
                # Food check
                if new_game.is_snake_ate_food():
                    last_body = new_game.snake[-1]
                    if new_game.snake_going == "right":
                        new_game.snake.append([last_body[0], last_body[1] - 1])
                    
                    elif new_game.snake_going == "left":
                        new_game.snake.append([last_body[0], last_body[1] + 1])
                    
                    elif new_game.snake_going == "up":
                        new_game.snake.append([last_body[0] + 1, last_body[1]])
                    
                    elif new_game.snake_going == "down":
                        new_game.snake.append([last_body[0] - 1, last_body[1]])
                    
                    new_game.score += 1
                    new_game.add_food()
                    
                    if mode == "0":
                        frame_delay_x -= frame_delay_x / speed_factor
                        frame_delay_y -= frame_delay_y / speed_factor

                if new_game.snake_going in ("up", "down"):
                    sleep(frame_delay_y)
                else:    
                    sleep(frame_delay_x)
                Cursor.up(len(new_game.game_area) + 10)
                Cursor.to_column(1)

        elif option == "2": # Change game mode
            Term.clear()
            Term.typewriter(f"Current mode is: {modes[mode]["name"]}")
            sleep(1.2)
            print(game_mode_menu)
            mode_option = input("==> ")
            mode_option = mode_option.strip()
            if mode_option not in ["0", "1", "2", "3", "4", "5"]:
                alert(f"Unknown option: {mode_option}")
            
            else:
                settings["game"]["current mode"] = mode_option
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"Game mode set: {modes[mode]["name"]}")
                sleep(1.2)
                Term.clear()

        elif option == "3":
            Term.clear()
            print(settings_menu)
            settings_option = input("==> ")
            settings_option = settings_option.strip()
            if settings_option == "1":
                Term.clear()
                Term.typewriter("Set new up key: ", end="")
                new_key = input()
                new_key = new_key.strip()
                if new_key in [right_key, left_key, down_key, "q"]:
                    alert(f"Another action is already using tihs key: {new_key}")
                    continue
                elif len(new_key) != 1:
                    alert(f"The key must be 1 letter.")
                    continue
                settings["keys"]["up"] = new_key
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"New up key set: {up_key}")
                sleep(1.2)
                Term.clear()

            if settings_option == "2":
                Term.clear()
                Term.typewriter("Set new down key: ", end="")
                new_key = input()
                new_key = new_key.strip()
                if new_key in [right_key, left_key, up_key, "q"]:
                    alert(f"Another action is already using tihs key: {new_key}")
                    continue
                elif len(new_key) != 1:
                    alert(f"The key must be 1 letter.")
                    continue
                settings["keys"]["down"] = new_key
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"New down key set: {down_key}")
                sleep(1.2)
                Term.clear()

            if settings_option == "3":
                Term.clear()
                Term.typewriter("Set new right key: ", end="")
                new_key = input()
                new_key = new_key.strip()
                if new_key in [up_key, left_key, down_key, "q"]:
                    alert(f"Another action is already using tihs key: {new_key}")
                    continue
                elif len(new_key) != 1:
                    alert(f"The key must be 1 letter.")
                    continue
                settings["keys"]["right"] = new_key
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"New right key set: {right_key}")
                sleep(1.2)
                Term.clear()

            if settings_option == "4":
                Term.clear()
                Term.typewriter("Set new left key: ", end="")
                new_key = input()
                new_key = new_key.strip()
                if new_key in [up_key, right_key, down_key, "q"]:
                    alert(f"Another action is already using tihs key: {new_key}")
                    continue
                elif len(new_key) != 1:
                    alert(f"The key must be 1 letter.")
                    continue
                settings["keys"]["left"] = new_key
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"New left key set: {left_key}")
                sleep(1.2)
                Term.clear()

            if settings_option == "5":
                Term.clear()
                Term.typewriter("Set snakes head image: ", end="")
                new_key = input()
                new_key = new_key.strip()
                if len(new_key) != 1:
                    alert(f"The image must be 1 letter.")
                    continue
                settings["snake"]["head"] = new_key
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"New snakes head set: {head}")
                sleep(1.2)
                Term.clear()

            if settings_option == "6":
                Term.clear()
                Term.typewriter("Set snakes body image: ", end="")
                new_key = input()
                new_key = new_key.strip()
                if len(new_key) != 1:
                    alert(f"The image must be 1 letter.")
                    continue
                settings["snake"]["body"] = new_key
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"New snakes body set: {body}")
                sleep(1.2)
                Term.clear()

            if settings_option == "7":
                Term.clear()
                Term.typewriter("Set food image: ", end="")
                new_key = input()
                new_key = new_key.strip()
                if len(new_key) != 1:
                    alert(f"The image must be 1 letter.")
                    continue
                settings["game"]["food"] = new_key
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"New food set: {food}")
                sleep(1.2)
                Term.clear()

            if settings_option == "8":
                Term.clear()
                Term.typewriter("Set food image: ", end="")
                new_key = input()
                new_key = new_key.strip()
                if len(new_key) != 1:
                    alert(f"The image must be 1 letter.")
                    continue
                settings["game"]["wall"] = new_key
                dump_json(settings, SETTINGS_FILE)
                load_json()
                Term.clear()
                Term.typewriter(f"New wall set: {wall}")
                sleep(1.2)
                Term.clear()


        else:
            Term.clear()
            Term.set_color("red")
            Term.typewriter("Unknown option: ", end="")
            print(option)
            sleep(1.2)
            Term.clear()
            Term.set_color("reset")
            main()
    
    listener.stop()
    Term.clear()

if __name__ == "__main__":
    main()
