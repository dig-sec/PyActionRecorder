import time
import random
import string
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

import pyautogui
from pynput import mouse, keyboard

class MacroRecorder:
    def __init__(self):
        self.actions: List[Dict] = []
        self.recording: bool = False
        self.stop_replay: bool = False
        self.mouse_press_time: Optional[float] = None
        self.keyboard_controller = keyboard.Controller()

        self.recordings_dir = "recordings"
        self.click_duration_threshold = 0.1

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01

    def on_mouse_click(self, x: int, y: int, button, pressed: bool) -> None:
        if not self.recording:
            return

        current_time = time.perf_counter()
        if pressed:
            self.mouse_press_time = current_time
        else:
            duration = current_time - self.mouse_press_time
            action_type = "mouse_hold" if duration >= self.click_duration_threshold else "mouse_click"
            action = {
                "type": action_type,
                "x": x,
                "y": y,
                "button": str(button),
                "timestamp": current_time,
                "duration": duration if action_type == "mouse_hold" else None
            }
            self.actions.append(action)

    def on_keyboard_press(self, key) -> Optional[bool]:
        if key == keyboard.Key.esc:
            self.recording = False
            return False
        if self.recording:
            self.actions.append({
                "type": "keyboard_press",
                "key": str(key),
                "timestamp": time.perf_counter()
            })

    def on_keyboard_release(self, key) -> None:
        if self.recording:
            self.actions.append({
                "type": "keyboard_release",
                "key": str(key),
                "timestamp": time.perf_counter()
            })

    def start_recording(self) -> None:
        self.recording = True
        self.actions = []
        print("Recording... Press ESC to stop.")

    def save_actions(self) -> None:
        os.makedirs(self.recordings_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"macro_{timestamp}_{''.join(random.choices(string.ascii_lowercase, k=4))}.json"
        filepath = os.path.join(self.recordings_dir, filename)

        try:
            with open(filepath, "w") as file:
                json.dump(self.actions, file, indent=2)
            print(f"Actions saved to '{filename}'")
        except IOError as e:
            print(f"Error saving actions: {e}")

    def load_actions(self, filename: str) -> None:
        filepath = os.path.join(self.recordings_dir, filename)
        try:
            with open(filepath, "r") as file:
                self.actions = json.load(file)
            print(f"Loaded actions from '{filename}'")
        except FileNotFoundError:
            print(f"File not found: '{filename}'")
        except json.JSONDecodeError:
            print("Invalid macro file format.")
        except IOError as e:
            print(f"Error loading actions: {e}")

    def replay_actions(self, loop_count: int, speed_factor: float = 1.0) -> None:
        print(f"Replaying {len(self.actions)} actions {loop_count} time(s) at {speed_factor}x speed")
        print("Press F4 to stop replay at any time")

        # Set up a listener to detect F4 key to stop replay
        stop_key_listener = keyboard.Listener(on_press=self._check_stop_key)
        stop_key_listener.start()
        
        self.stop_replay = False
        for loop in range(loop_count):
            if self.stop_replay:
                print("Replay stopped by user.")
                break

            prev_time = None
            for action in self.actions:
                if self.stop_replay:
                    break

                current_time = action["timestamp"]
                if prev_time is not None:
                    delay = (current_time - prev_time) / speed_factor
                    if delay > 0:
                        time.sleep(delay)

                try:
                    action_type = action["type"]
                    if action_type == "mouse_click":
                        self.perform_mouse_click(action["x"], action["y"], action["button"])
                    elif action_type == "mouse_hold":
                        self.perform_mouse_hold(action["x"], action["y"], action["button"], action["duration"])
                    elif action_type == "keyboard_press":
                        self.perform_keyboard_press(action["key"])
                    elif action_type == "keyboard_release":
                        self.perform_keyboard_release(action["key"])
                except Exception as e:
                    print(f"Error during replay: {e}")

                prev_time = current_time

            print(f"Loop {loop+1}/{loop_count} complete.")

        stop_key_listener.stop()
        print("Replay complete.")

    def _check_stop_key(self, key) -> None:
        if key == keyboard.Key.f4:
            self.stop_replay = True
            print("Replay will stop after current action...")

    def perform_mouse_click(self, x: int, y: int, button: str) -> None:
        pyautogui.click(x=x, y=y, button=self._map_button(button))

    def perform_mouse_hold(self, x: int, y: int, button: str, duration: float) -> None:
        mapped_button = self._map_button(button)
        pyautogui.mouseDown(x=x, y=y, button=mapped_button)
        time.sleep(duration)
        pyautogui.mouseUp(x=x, y=y, button=mapped_button)

    def perform_keyboard_press(self, key: str) -> None:
        try:
            key_obj = self._parse_key(key)
            self.keyboard_controller.press(key_obj)
        except Exception as e:
            print(f"Failed to press key {key}: {e}")

    def perform_keyboard_release(self, key: str) -> None:
        try:
            key_obj = self._parse_key(key)
            self.keyboard_controller.release(key_obj)
        except Exception as e:
            print(f"Failed to release key {key}: {e}")

    def _map_button(self, button: str) -> str:
        return {
            "Button.left": "left",
            "Button.right": "right",
            "Button.middle": "middle"
        }.get(button, "left")

    def _parse_key(self, key: str):
        if key.startswith("Key."):
            return getattr(keyboard.Key, key.split(".", 1)[1])
        return key.strip("'")

def print_menu() -> None:
    print("\n===== Macro Recorder Menu =====")
    print("1. Record New Macro")
    print("2. Load Macro")
    print("3. List Available Macros")
    print("4. Replay Macro")
    print("5. Exit")

def list_macros(directory: str) -> None:
    try:
        files = [f for f in os.listdir(directory) if f.endswith(".json")]
        if files:
            print("\nAvailable macros:")
            for idx, file in enumerate(files, 1):
                print(f"{idx}. {file}")
        else:
            print("No macros found.")
    except OSError as e:
        print(f"Error listing macros: {e}")

def three_second_countdown() -> None:
    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)
    print("Go!")

def record_actions(recorder: MacroRecorder) -> None:
    try:
        recorder.start_recording()
        with mouse.Listener(on_click=recorder.on_mouse_click):
            with keyboard.Listener(
                on_press=recorder.on_keyboard_press,
                on_release=recorder.on_keyboard_release
            ) as keyboard_listener:
                keyboard_listener.join()
        recorder.save_actions()
    except Exception as e:
        print(f"Error during recording: {e}")


def main() -> None:
    recorder = MacroRecorder()

    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            three_second_countdown()
            record_actions(recorder)
        elif choice == "2":
            list_macros(recorder.recordings_dir)
            filename = input("Enter filename to load (or 'cancel' to return): ").strip()
            if filename.lower() != "cancel":
                recorder.load_actions(filename)
        elif choice == "3":
            list_macros(recorder.recordings_dir)
        elif choice == "4":
            if not recorder.actions:
                print("No actions loaded. Please load or record a macro first.")
                continue

            try:
                loops = int(input("Enter number of loops: ").strip())
                speed = float(input("Enter speed factor (0.5–2.0, 1.0 = normal): ").strip())
                if not (1 <= loops <= 100 and 0.5 <= speed <= 2.0):
                    raise ValueError
            except ValueError:
                print("Invalid input. Using defaults: 1 loop, 1.0 speed.")
                loops, speed = 1, 1.0

            three_second_countdown()
            recorder.replay_actions(loops, speed)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select from the menu.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Exiting...")
