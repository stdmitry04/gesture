import tkinter as tk
import subprocess
import sys
class ToggleButtonApp:
    def __init__(self, master):
        self.master = master
        self.master.config(bg='#A9A9A9')  # Discord grey background color

        # Use a more modern font, make it bold and larger
        self.font_style = ('Verdana', 10, 'bold')

        # Initialize the button in the 'Off' state with Discord red color
        self.state = False
        self.process = None  # Placeholder for the subprocess
        self.button = tk.Button(master, text='OFF', bg='#FF0000', fg='white',
                                command=self.toggle_state, font=self.font_style,
                                relief='flat', padx=20, pady=10)
        self.button.pack(pady=20)

        # Add a shadow effect for depth (optional)
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)

    def toggle_state(self):
        if self.state:
            self.button.config(text='OFF', bg='#FF0000')  # Red for 'Off'
            if self.process:
                self.process.terminate()  # Terminate the subprocess
                self.process = None
        else:
            self.button.config(text='ON', bg='#008000')  # Green for 'On'
            if not self.process:
                main_script_path = '/Users/stdmitry/Desktop/yolo9/main.py'  # Replace with actual path
                self.process = subprocess.Popen([sys.executable, main_script_path], shell=False)  # Start the subprocess
        self.state = not self.state

    def on_enter(self, e):
        self.button['bg'] = '#FFA07A'  # Lighten the button on hover for a subtle effect

    def on_leave(self, e):
        if self.state:
            self.button.config(bg='#008000')  # Reset to green if On
        else:
            self.button.config(bg='#FF0000')  # Reset to red if Off


def main():
    root = tk.Tk()
    root.title('Button')
    app = ToggleButtonApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
