import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, scrolledtext
import threading
import logging
import sys
import io

import LSBSteg
import WavSteg
import StegDetect
from MP3hide import hide_file_in_mp3, reveal_file_from_mp3

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


class RedirectedIO(io.StringIO):
    """Custom class to redirect stdout and stderr to a Tkinter widget."""
    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = widget

    def write(self, msg):
        self.widget.config(state="normal")
        self.widget.insert(tk.END, msg)
        self.widget.see(tk.END)
        self.widget.config(state="disabled")

    def flush(self):
        pass  # For compatibility with Python's flush calls


class StegApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography GUI")
        self.root.geometry("800x600")

        self.progress_var = tk.DoubleVar()

        self.create_main_menu()
        self.create_console()

    def create_main_menu(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.main_frame, text="Steganography Tool", font=("Helvetica", 18)).pack(pady=10)

        buttons = [
            ("MP3 Steganography", self.mp3_steg_ui),
            ("Image Steganography (LSB)", self.image_steg_ui),
            ("WAV Steganography", self.wav_steg_ui),
            ("Detect LSB in Images", self.steg_detect_ui),
        ]

        for text, command in buttons:
            tk.Button(self.main_frame, text=text, command=command, width=30, pady=5).pack(pady=5)

    def create_console(self):
        self.console_frame = tk.Frame(self.root)
        self.console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        tk.Label(self.console_frame, text="Console Output:", anchor="w").pack(fill=tk.X)

        self.console_text = scrolledtext.ScrolledText(self.console_frame, height=10, state="disabled")
        self.console_text.pack(fill=tk.BOTH, expand=True)

        self.progress_bar = ttk.Progressbar(self.console_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)

        # Redirect stdout and stderr to console
        sys.stdout = RedirectedIO(self.console_text)
        sys.stderr = RedirectedIO(self.console_text)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()

    def clear_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def reset_ui(self):
        self.clear_ui()
        self.create_main_menu()

    def file_dialog(self, title, file_type):
        return filedialog.askopenfilename(title=title, filetypes=[("Files", file_type)])

    def save_dialog(self, title, default_ext):
        return filedialog.asksaveasfilename(title=title, defaultextension=default_ext)

    def run_in_thread(self, func):
        thread = threading.Thread(target=func, daemon=True)
        thread.start()

    # MP3 Menu
    def mp3_steg_ui(self):
        self.clear_ui()
        tk.Label(self.main_frame, text="MP3 Steganography", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Hide Data", command=self.mp3_hide_ui, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Reveal Data", command=self.mp3_reveal_ui, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.reset_ui, width=20).pack(pady=20)

    def mp3_hide_ui(self):
        input_file = self.file_dialog("Select MP3 File to Hide Data In", "*.mp3")
        if not input_file:
            return
        secret_file = self.file_dialog("Select File to Hide", "*")
        if not secret_file:
            return
        output_file = self.save_dialog("Save Steganographed MP3 File", ".mp3")
        if not output_file:
            return

        def task():
            try:
                self.update_progress(10)
                print("Hiding data in MP3 file...")
                hide_file_in_mp3(input_file, secret_file, output_file)
                self.update_progress(100)
                print(f"Data hidden successfully in {output_file}")
                messagebox.showinfo("Success", f"Data hidden successfully in {output_file}")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.update_progress(0)

        self.run_in_thread(task)

    def mp3_reveal_ui(self):
        input_file = self.file_dialog("Select Steganographed MP3 File", "*.mp3")
        if not input_file:
            return
        output_file = self.save_dialog("Save Extracted Data", "*")
        if not output_file:
            return

        def task():
            try:
                self.update_progress(10)
                print("Revealing hidden data from MP3 file...")
                reveal_file_from_mp3(input_file, output_file)
                self.update_progress(100)
                print(f"Data extracted successfully to {output_file}")
                messagebox.showinfo("Success", f"Data extracted successfully to {output_file}")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.update_progress(0)

        self.run_in_thread(task)

    # Image Menu
    def image_steg_ui(self):
        self.clear_ui()
        tk.Label(self.main_frame, text="Image Steganography", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Hide Data", command=self.image_hide_ui, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Reveal Data", command=self.image_reveal_ui, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Analyze Capacity", command=self.image_analyze_ui, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.reset_ui, width=20).pack(pady=20)

    def image_hide_ui(self):
        input_file = self.file_dialog("Select Image File to Hide Data In", "*.png *.bmp")
        if not input_file:
            return
        secret_file = self.file_dialog("Select File to Hide", "*")
        if not secret_file:
            return
        output_file = self.save_dialog("Save Steganographed Image File", ".png")
        if not output_file:
            return
        lsb_count = simpledialog.askinteger("LSB Count", "Enter number of LSBs to use (1-8):", minvalue=1, maxvalue=8)
        if lsb_count is None:
            return

        def task():
            try:
                self.update_progress(10)
                LSBSteg.hide_data(input_file, secret_file, output_file, lsb_count, compression_level=1)
                self.update_progress(100)
                print(f"Data hidden successfully in {output_file}")
                messagebox.showinfo("Success", f"Data hidden successfully in {output_file}")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.update_progress(0)

        self.run_in_thread(task)

    def image_reveal_ui(self):
        input_file = self.file_dialog("Select Steganographed Image File", "*.png *.bmp")
        if not input_file:
            return
        output_file = self.save_dialog("Save Extracted Data", "*")
        if not output_file:
            return
        lsb_count = simpledialog.askinteger("LSB Count", "Enter number of LSBs used during hiding (1-8):", minvalue=1, maxvalue=8)
        if lsb_count is None:
            return

        def task():
            try:
                self.update_progress(10)
                LSBSteg.recover_data(input_file, output_file, lsb_count)
                self.update_progress(100)
                print(f"Data extracted successfully to {output_file}")
                messagebox.showinfo("Success", f"Data extracted successfully to {output_file}")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.update_progress(0)

        self.run_in_thread(task)

    def image_analyze_ui(self):
        input_file = self.file_dialog("Select Image File for Analysis", "*.png *.bmp")
        if not input_file:
            return
        lsb_count = simpledialog.askinteger("LSB Count", "Enter number of LSBs to analyze (1-8):", minvalue=1, maxvalue=8)
        if lsb_count is None:
            return

        def task():
            try:
                StegDetect.show_lsb(input_file, lsb_count)
                print("Image analysis completed. Check the generated image.")
                messagebox.showinfo("Success", "Image analysis completed. Check the generated image.")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))

        self.run_in_thread(task)

    # WAV Menu
    def wav_steg_ui(self):
        self.clear_ui()
        tk.Label(self.main_frame, text="WAV Steganography", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Hide Data", command=self.wav_hide_ui, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Reveal Data", command=self.wav_reveal_ui, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.reset_ui, width=20).pack(pady=20)

    def wav_hide_ui(self):
        input_file = self.file_dialog("Select WAV File to Hide Data In", "*.wav")
        if not input_file:
            return
        secret_file = self.file_dialog("Select File to Hide", "*")
        if not secret_file:
            return
        output_file = self.save_dialog("Save Steganographed WAV File", ".wav")
        if not output_file:
            return
        lsb_count = simpledialog.askinteger("LSB Count", "Enter number of LSBs to use (1-8):", minvalue=1, maxvalue=8)
        if lsb_count is None:
            return

        def task():
            try:
                self.update_progress(10)
                WavSteg.hide_data(input_file, secret_file, output_file, lsb_count)
                self.update_progress(100)
                print(f"Data hidden successfully in {output_file}")
                messagebox.showinfo("Success", f"Data hidden successfully in {output_file}")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.update_progress(0)

        self.run_in_thread(task)

    def wav_reveal_ui(self):
        input_file = self.file_dialog("Select Steganographed WAV File", "*.wav")
        if not input_file:
            return
        output_file = self.save_dialog("Save Extracted Data", "*")
        if not output_file:
            return
        lsb_count = simpledialog.askinteger("LSB Count", "Enter number of LSBs used during hiding (1-8):", minvalue=1, maxvalue=8)
        if lsb_count is None:
            return
        bytes_to_recover = simpledialog.askinteger("Bytes to Recover", "Enter the number of bytes to recover:")
        if bytes_to_recover is None:
            return

        def task():
            try:
                self.update_progress(10)
                WavSteg.recover_data(input_file, output_file, lsb_count, bytes_to_recover)
                self.update_progress(100)
                print(f"Data extracted successfully to {output_file}")
                messagebox.showinfo("Success", f"Data extracted successfully to {output_file}")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self.update_progress(0)

        self.run_in_thread(task)

    # Detection Menu
    def steg_detect_ui(self):
        self.clear_ui()
        tk.Label(self.main_frame, text="Detect LSB in Images", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.main_frame, text="Analyze Image", command=self.analyze_image_ui, width=20).pack(pady=5)
        tk.Button(self.main_frame, text="Back", command=self.reset_ui, width=20).pack(pady=20)

    def analyze_image_ui(self):
        input_file = self.file_dialog("Select Image File for Detection", "*.png *.bmp")
        if not input_file:
            return
        lsb_count = simpledialog.askinteger("LSB Count", "Enter number of LSBs to display (1-8):", minvalue=1, maxvalue=8)
        if lsb_count is None:
            return

        def task():
            try:
                print(f"Analyzing image {input_file} with {lsb_count} LSBs...")
                StegDetect.show_lsb(input_file, lsb_count)
                print("Image analysis completed. Check the generated image.")
                messagebox.showinfo("Success", "Image analysis completed. Check the generated image.")
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", str(e))

        self.run_in_thread(task)


if __name__ == "__main__":
    root = tk.Tk()
    app = StegApp(root)
    root.mainloop()
