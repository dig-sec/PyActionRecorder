import time
import random
import string
import pyautogui
from pynput import mouse, keyboard


class MacroRecorder:
    def __init__(self):
        self.actions = []
        self.recording = False
        self.stop_replay = False
        self.keyboard_controller = keyboard.Controller()

    def on_mouse_click(self, x, y, button, pressed):
        if pressed and self.recording:
            action = f"Mouse Click: ({x}, {y}), {button}, {time.perf_counter()}"
            self.actions.append(action)

    def on_keyboard_press(self, key):
        if key == keyboard.Key.esc:
            self.recording = False
            return False
        elif self.recording:
            action = f"Keyboard Press: {key}, {time.perf_counter()}"
            self.actions.append(action)
        elif not self.recording and key == keyboard.Key.f4:
            print_menu()

    def on_keyboard_release(self, key):
        if self.recording:
            action = f"Keyboard Release: {key}, {time.perf_counter()}"
            self.actions.append(action)

    def start_recording(self):
        self.recording = True
        print("Recording actions... Press ESC to stop recording.")

    def save_actions(self):
        filename = self.generate_filename()
        try:
            with open(filename, "w") as file:
                file.write("\n".join(self.actions))
            print(f"Actions saved to '{filename}'.")
        except IOError:
            print(f"Error: Unable to save actions to '{filename}'.")

        try:
            self.load_actions(filename)
        except IOError:
            print(f"Error: Unable to load actions from '{filename}'.")

    def generate_filename(self):
        random_string = ''.join(random.choices(string.ascii_lowercase, k=4))
        return random_string

    def load_actions(self, filename):
        try:
            with open(filename, "r") as file:
                actions = file.readlines()
            self.actions = [action.strip() for action in actions]
            print(f"Actions loaded from '{filename}'.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError:
            print(f"Error: Unable to load actions from '{filename}'.")

    def replay_actions(self, delay, loop_count):
        print(f"Replaying actions... Loop count: {loop_count}")
        self.stop_replay = False
        for _ in range(loop_count):
            start_time = time.perf_counter()
            for action in self.actions:
                if self.stop_replay:
                    print("Replay interrupted by user.")
                    return
                if "Mouse Click" in action:
                    x, y, button, _ = action.split(": ")[1].split(", ")
                    x, y = int(x.strip("()")), int(y.strip("()"))
                    button = button.strip()
                    self.perform_mouse_click(x, y, button)
                    print(f"Performed Mouse Click at ({x}, {y}) with button '{button}'")
                elif "Keyboard Press" in action:
                    key_name, press_time = action.split(": ")[1].split(", ")
                    key_name = key_name.strip()
                    press_time = float(press_time.strip())
                    self.perform_keyboard_press(key_name)
                    print(f"Performed Keyboard Press: '{key_name}'")
                elif "Keyboard Release" in action:
                    key_name, press_time = action.split(": ")[1].split(", ")
                    key_name = key_name.strip()
                    press_time = float(press_time.strip())
                    self.perform_keyboard_release(key_name)
                    print(f"Performed Keyboard Release: '{key_name}'")

                time.sleep(delay)

                # Check if F4 key was pressed during replay
                with keyboard.Events() as events:
                    try:
                        event = events.get(0.1)  # Check for key events every 0.1 seconds
                        if event and event.key == keyboard.Key.f4:
                            print("Returning to main menu...")
                            return
                    except KeyboardInterrupt:
                        return

            elapsed_time = time.perf_counter() - start_time
            if elapsed_time < delay:
                time.sleep(delay - elapsed_time)

        print("Replay complete.")

    def perform_mouse_click(self, x, y, button_name):
        button_mapping = {
            'Button.left': 'left',
            'Button.right': 'right',
            'Button.middle': 'middle',
            'Button.forward': 'forward',
            'Button.backward': 'backward'
        }
        button = button_mapping.get(button_name, None)
        if button is not None:
            pyautogui.click(x, y, button=button)
        else:
            print(f"Invalid mouse button name: {button_name}")

    def perform_keyboard_press(self, key):
        print(f"Performing keyboard press: {key}")
        if hasattr(keyboard.Key, key):
            key = getattr(keyboard.Key, key)
        elif key.startswith("Key."):
            key = getattr(keyboard.Key, key.split(".")[1])
        else:
            key = key.strip("'")
        self.keyboard_controller.press(key)

    def perform_keyboard_release(self, key):
        print(f"Performing keyboard release: {key}")
        if hasattr(keyboard.Key, key):
            key = getattr(keyboard.Key, key)
        elif key.startswith("Key."):
            key = getattr(keyboard.Key, key.split(".")[1])
        else:
            key = key.strip("'")
        self.keyboard_controller.release(key)


def print_menu():
    print("\n===== Macro Recorder Menu =====")
    print("1. Record Actions")
    print("2. Load Actions from File")
    print("3. Replay Actions")
    print("4. Exit")
    print("==============================")
    print("During recording, press ESC to stop recording.")
    print("During replay, press F4 to stop the replay.")

def record_actions(recorder):
    recorder.start_recording()
    with mouse.Listener(on_click=recorder.on_mouse_click) as mouse_listener:
        with keyboard.Listener(on_press=recorder.on_keyboard_press, on_release=recorder.on_keyboard_release) as keyboard_listener:
            while recorder.recording:
                pass
    recorder.save_actions()


def load_actions(recorder):
    filename = input("Enter the filename to load actions: ")
    recorder.load_actions(filename)


def replay_actions(recorder, delay, loop_count):
    recorder.replay_actions(delay, loop_count)


# Used for countdown before starting to record or replay actions.
def countdown_before_start():
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)


def main():
    recorder = MacroRecorder()

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            countdown_before_start()
            record_actions(recorder)
        elif choice == "2":
            load_actions(recorder)
        elif choice == "3":
            # Input number of loops as int
            number_of_loops = input("Enter number of loops: ")
            if not int(number_of_loops):
                number_of_loops = 1
                print("Bad value setting number of loops to default value of 1.")

            # Input delay as float
            delay_time = input("Enter delay between actions (in seconds 0.1 to 0.15): ")
            if not float(delay_time):
                delay_time = 0.13
                print("Bad value setting delay to default value of 0.13 seconds.")
                
            countdown_before_start()
            replay_actions(recorder, delay=float(delay_time), loop_count=int(number_of_loops))
            break
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

    print("Exiting program...")
    time.sleep(1)
    
if __name__ == "__main__":
    main()