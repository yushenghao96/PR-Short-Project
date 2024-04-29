import os,sys
import tkinter as tk
import random
import numpy as np
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


languages = [
    'Spanish',
    'English',
    'German',
    'French'
]

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language detector on fly")
        
        self.flag = tk.BooleanVar()
        self.flag.set(False)
        self.geometry("900x600")

        # Create frames for subdividing window


        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew")

        upper_frame = tk.Frame(left_frame)
        upper_frame.pack(side="top", fill="both", expand=True)

        bottom_frame = tk.Frame(left_frame)
        bottom_frame.pack(side="bottom", fill="both", expand=True)
        
        right_frame = tk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew")


        self.text_box = ttk.Entry(left_frame)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_box.bind("<KeyRelease>", self.update_plot)
    
        self.fig, self.ax = plt.subplots(figsize=(2,2)) #Adjust plot size 
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.plot_canvas.get_tk_widget().pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #Test widgets in botton part
        self.letters_count = tk.Text(bottom_frame)
        self.letters_count.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #Make frames resizable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
        self.update_plot()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def update_plot(self, event=None):
        # Clear previous plot
        self.ax.clear()
        
        # Get the text from the text box
        text = self.text_box.get()


        # Plot based on putuation of languages
        if text.isdigit() and int(text) > 0:
            self.flag.set(True)
            rnd_number = [random.random() for i in range(3)]
            last_number = 1- sum(rnd_number)
            rnd_number.append(last_number)
            print(rnd_number)
            self.ax.bar(languages,rnd_number)
            self.ax.set_xlabel('Values')
            self.ax.set_ylabel('Random Numbers')
            self.ax.set_title('Language example output')
            self.letters_count.delete(1.0, tk.END)
            self.letters_count.insert(tk.END, "Random numbers generated:\n")
            for idx, rnd in enumerate(rnd_number):
                self.letters_count.insert(tk.END, f"{languages[idx]}: {rnd:.2f}\n")
            
        else:
            self.flag.set(False)
        
        # Redraw canvas
        self.plot_canvas.draw()
    
    def on_close(self):
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
    
    
