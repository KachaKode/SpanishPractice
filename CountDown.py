import time
import keyboard

class CountDown:
    def __init__(self, time_limit):
        self.paused = False
        self.done = False
        self.limit = time_limit
        self.global_I = 0
        self.user_input = []
        self.last_keypress_time = None  # Track the last time a key was pressed
        # Bind the spacebar key to the toggle_pause function
        keyboard.hook_key('control', self.toggle_pause)
        keyboard.hook(self.key_event)

    def start(self):
        # For the reset
        self.user_input = []
        self.paused = False
        self.done = False

        for i in range(self.limit, 0, -1):
            self.global_I = i
            while self.paused:
                # Check if more than 0.3 seconds have passed since the last keypress
                if self.last_keypress_time and time.time() - self.last_keypress_time > 0.3:
                    self.paused = False
                time.sleep(0.1)  # Wait a short time to reduce CPU usage
            print(f"\rTime Left: {self.global_I}\tYou typed:{''.join(self.user_input)}", end="")
            # So that if the user presses enter
            if self.done:
                break
            time.sleep(1)

        # Return the user's input
        return ''.join(self.user_input)

    def toggle_pause(self, e):
        if e.event_type == 'down':  # Only act on keydown event
            self.last_keypress_time = None
            self.paused = not self.paused
            if self.paused:
                print(f"\rTime Left: {self.global_I} (paused)\tYou typed:{''.join(self.user_input)}", end="")

    def key_event(self, e):
        if e.event_type == 'down':
            if e.name == 'enter':
                self.done = True
            elif e.name == 'backspace' and self.user_input:
                self.user_input.pop()
                self.paused = True
                self.last_keypress_time = time.time()  # Update the timestamp of the last keypress
            elif  len(e.name) == 1:  # Ensure only single characters are added
                self.paused = True
                self.user_input.append(e.name)
                self.last_keypress_time = time.time()  # Update the timestamp of the last keypress
            elif e.name == 'space':  # Ensure only single characters are added
                self.paused = True
                self.user_input.append(' ')
                self.last_keypress_time = time.time()  # Update the timestamp of the last keypress

cd = CountDown(10)
cd.start()