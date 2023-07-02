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
        self.mouse_press_time = None
        self.keyboard_controller = keyboard.Controller()

    def on_mouse_click(self, x, y, button, pressed):
        click_duration_threshold = 0.13  # Threshold duration in seconds
        if self.recording:
            if pressed:
                self.mouse_press_time = time.perf_counter()
            else:
                mouse_release_time = time.perf_counter()
                duration = mouse_release_time - self.mouse_press_time
                if duration < click_duration_threshold:
                    action = f"Mouse Click: ({x}, {y}), {button}, {mouse_release_time}"
                else:
                    action = f"Mouse Hold: ({x}, {y}), {button}, {self.mouse_press_time}, {duration}"
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
        self.actions = []
        print("Recording actions... Press ESC to stop recording.")

    def save_actions(self):
        filename = self.generate_filename()
        filename = f"recordings/{filename}.macro"

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
            filename = f"recordings/{filename}"

            with open(filename, "r") as file:
                actions = file.readlines()
            self.actions = [action.strip() for action in actions]
            print(f"Actions loaded from '{filename}'.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError:
            print(f"Error: Unable to load actions from '{filename}'.")

    def replay_actions(self, loop_count):
        print(f"Replaying actions... Loop count: {loop_count}")
        print(f"Number of actions: {len(self.actions)}")

        self.stop_replay = False
        for _ in range(loop_count):
            prev_action_time = None
            for action in self.actions:
                if self.stop_replay:
                    print("Replay interrupted by user.")
                    return
                if "Mouse Click" in action:
                    x, y, button, click_time = action.split(": ")[1].split(", ")
                    x, y = int(x.strip("()")), int(y.strip("()"))
                    button = button.strip()
                    click_time = float(click_time.strip())
                    if prev_action_time is not None:
                        delay = click_time - prev_action_time
                        time.sleep(delay)
                    self.perform_mouse_click(x, y, button)
                    prev_action_time = click_time
                elif "Mouse Hold" in action:
                    x, y, button, press_time, duration = action.split(": ")[1].split(", ")
                    x, y = int(x.strip("()")), int(y.strip("()"))
                    button = button.strip()
                    press_time = float(press_time.strip())
                    duration = float(duration.strip())
                    if prev_action_time is not None:
                        delay = press_time - prev_action_time
                        time.sleep(delay)
                    self.perform_mouse_press(x, y, button)
                    time.sleep(duration)
                    self.perform_mouse_release(x, y, button)
                    prev_action_time = press_time + duration
                elif "Keyboard Press" in action:
                    key_name, press_time = action.split(": ")[1].split(", ")
                    key_name = key_name.strip()
                    press_time = float(press_time.strip())
                    if prev_action_time is not None:
                        delay = press_time - prev_action_time
                        time.sleep(delay)
                    self.perform_keyboard_press(key_name)
                    prev_action_time = press_time
                elif "Keyboard Release" in action:
                    key_name, release_time = action.split(": ")[1].split(", ")
                    key_name = key_name.strip()
                    release_time = float(release_time.strip())
                    if 'press_time' in locals():
                        duration = release_time - press_time
                        if duration > 0:
                            time.sleep(duration)
                        if prev_action_time is not None:
                            delay = release_time - prev_action_time
                            time.sleep(delay)
                        self.perform_keyboard_release(key_name)
                        prev_action_time = release_time

                # Check if F4 key was pressed during replay
                with keyboard.Events() as events:
                    try:
                        event = events.get(0.1)  # Check for key events every 0.1 seconds
                        if event and event.key == keyboard.Key.f4:
                            print("Returning to main menu...")
                            return
                    except KeyboardInterrupt:
                        return

        print("Replay complete.")

    def perform_mouse_press(self, x, y, button_name):
        button_mapping = {
            'Button.left': 'left',
            'Button.right': 'right',
            'Button.middle': 'middle',
            'Button.forward': 'forward',
            'Button.backward': 'backward'
        }
        button = button_mapping.get(button_name, None)
        if button is not None:
            pyautogui.mouseDown(x=x, y=y, button=button)
        else:
            print(f"Invalid mouse button name: {button_name}")

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
            pyautogui.click(x=x, y=y, button=button)
        else:
            print(f"Invalid mouse button name: {button_name}")

    def perform_mouse_release(self, x, y, button_name):
        button_mapping = {
            'Button.left': 'left',
            'Button.right': 'right',
            'Button.middle': 'middle',
            'Button.forward': 'forward',
            'Button.backward': 'backward'
        }
        button = button_mapping.get(button_name, None)
        if button is not None:
            pyautogui.mouseUp(x=x, y=y, button=button)
        else:
            print(f"Invalid mouse button name: {button_name}")

    def perform_keyboard_press(self, key):
        if hasattr(keyboard.Key, key):
            key = getattr(keyboard.Key, key)
        elif key.startswith("Key."):
            key = getattr(keyboard.Key, key.split(".")[1])
        else:
            key = key.strip("'")
        self.keyboard_controller.press(key)

    def perform_keyboard_release(self, key):
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
    print("During recording, press ESC to stop recording.\nDuring replay, press F4 to stop the replay.\nRecodings are automaticly stored and loaded from the recordings folder.")

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

def three_second_countdown_before_start():
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

def main():
    recorder = MacroRecorder()
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            three_second_countdown_before_start()
            record_actions(recorder)
        elif choice == "2":
            load_actions(recorder)
        elif choice == "3":
            while True:
                try:
                    number_of_loops = int(input("Enter number of loops: "))
                    if number_of_loops < 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Invalid number of loops. Please try again.")

            three_second_countdown_before_start()
            recorder.replay_actions(number_of_loops)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

    print("Exiting program...")
    time.sleep(1)
    
if __name__ == "__main__":
    main()