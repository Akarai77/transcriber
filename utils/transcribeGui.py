import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
from tkinter import font as tkfont
import os,re

class TranscribeGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Transcriber")

        # Variables
        self.input_file_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.output_filename_var = tk.StringVar()
        self.font_var = tk.StringVar()
        self.font_size_var = tk.StringVar()
        self.color_var = tk.StringVar()
        self.valid = False

        # Input File
        tk.Label(root, text="Input Video File:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.input_file_var, width=75).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10, pady=10)

        # Output Directory
        tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.output_dir_var, width=75).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=self.browse_output_directory).grid(row=1, column=2, padx=10, pady=10)

        # Output Filename
        tk.Label(root, text="Output Filename:").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.output_filename_var, width=25).grid(row=2, column=1, padx=10, pady=10)

        # Font
        self.font_var = tk.StringVar(value="Arial")
        self.font_combobox = ttk.Combobox(root, textvariable=self.font_var)
        self.font_combobox.grid(row=3, column=1, padx=10, pady=10)
        fonts = tkfont.families()
        self.font_combobox['values'] = fonts
        self.font_combobox.bind("<<ComboboxSelected>>", self.update_font)

        # Font Size
        tk.Label(root, text="Font Size:").grid(row=4, column=0, padx=10, pady=10)
        validate_cmd = root.register(self.validate_input)
        self.font_size_field = tk.Entry(root, textvariable=self.font_size_var, validate="key", width=20, validatecommand=(validate_cmd, "%P"))
        self.font_size_field.grid(row=4, column=1, padx=10, pady=10)
        self.font_size_field.bind("<KeyRelease>",self.update_font)

        # Color
        tk.Label(root, text="Subtitle Color:").grid(row=5, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.color_var, width=20).grid(row=5, column=1, padx=10, pady=10)
        tk.Button(root, text="Choose Color", command=self.choose_color).grid(row=5, column=2, padx=10, pady=10)
        
        # Font Preview Label
        self.font_label = tk.Label(root, text="Hello World!", bg="white", fg="black", font=("Arial", 12))
        self.font_label.grid(row=6, column=1, padx=20, pady=10)

        # Process Button
        tk.Button(root, text="Process Video", command=self.process_video).grid(row=7, column=1, padx=10, pady=10)
        
        # Bind the close window event
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def validate_input(self, P):
        if P == "" or P.isdigit():
            return True
        else:
            return False

    def update_font(self, event=None):
        try:
            font_size = int(self.font_size_var.get())
        except ValueError:
            font_size = 12
        font_name = self.font_var.get()
        self.font_label.config(font=(font_name, font_size))

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.color_var.set(color_code[1])
            self.font_label.config(fg=self.color_var.get())

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.mkv;*.avi;*.mov;*.wmv;*.flv;*.webm;*.mpeg;*.mpg;*.m4v")])
        if file_path:
            self.input_file_var.set(file_path)

    def browse_output_directory(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_dir_var.set(folder_path)

    def process_video(self):
        self.input_file = self.input_file_var.get()
        self.output_dir = self.output_dir_var.get()
        self.output_filename = self.output_filename_var.get()
        self.output_file = self.output_dir+'/'+self.output_filename+os.path.splitext(self.input_file)[1]
        self.font = self.font_var.get()
        self.font_size = self.font_size_var.get()
        self.color = self.color_var.get()
        
        if not self.input_file:
            messagebox.showwarning("Input Error", "Please select an input video file.")
            return
        if not os.path.isfile(self.input_file):
            messagebox.showwarning("Input Error", "Input Is Not A File.")
            return
        if os.path.splitext(self.input_file)[1] not in ['.mp4','.mkv','.avi','.mov','.wmv','.flv','.webm','.mpeg','.mpg','.m4v']:
            messagebox.showwarning("Input Error", "Invalid Input File Format.")
            return
        if not self.output_dir:
            messagebox.showwarning("Output Error", "Please select an output directory.")
            return
        if not os.path.isdir(self.output_dir):
            messagebox.showwarning("Output Error", "Output Directory Does Not Exist.")
            return
        if not re.match(r'^[a-zA-Z0-9_\-()]+$',self.output_filename):
            messagebox.showwarning("Output Error", "Invalid Output Filename. Special Characters are not allowed.")
            return
        if not self.font:
            messagebox.showwarning("Font Error", "Please choose a font.")
            return
        if self.font not in list(tkfont.families()):
            messagebox.showwarning("Font Error", "Invalid Font.")
            return
        if not self.font_size:
            messagebox.showwarning("Font Size Error", "Please enter a font size.")
            return
        if not self.color:
            messagebox.showwarning("Color Error", "Please choose a subtitle color.")
            return
        if not re.match(r'^#[0-9a-fA-F]{6}$', self.color):
            messagebox.showwarning("Color Error", "Invalid Color.")
            return
        self.valid = True
        print(f"Processing {self.input_file} with font {self.font}, size {self.font_size}, color {self.color}...")
        self.root.destroy()

    def on_close(self):
        print("Window closed.")
        self.root.destroy()