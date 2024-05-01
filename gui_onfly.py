import os,sys
import tkinter as tk
import random
import numpy as np
from tkinter import ttk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import kalman

#List and dict(obtain them from other file separated in the future)

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

        #Variables of class GUI
        self.previousText=""

        # Create frames for subdividing window


        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew")

        upper_frame = tk.Frame(left_frame)
        upper_frame.pack(side="top", fill="both", expand=True)

        bottom_frame = tk.Frame(left_frame)
        bottom_frame.pack(side="bottom", fill="both", expand=True)
        
        right_frame = tk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew")

        #Creation of widgets for each subwindow
        '''
        self.text_box = scrolledtext.ScrolledText(left_frame,wrap=tk.WORD, 
                                      width=40, height=8, 
                                      font=("Times New Roman", 15)) 
        #self.text_box.grid(column=0, row=2, pady=10, padx=10) 
        self.text_box.focus()
        '''
        self.text_box = ttk.Entry(upper_frame)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_box.bind("<KeyRelease>", self.calculate_model)
        
        
        self.fig, self.ax = plt.subplots(figsize=(7,5)) #Adjust plot size 
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.plot_canvas.get_tk_widget().pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #Test widgets in botton part
        self.letters_count = tk.Text(bottom_frame)
        self.letters_count.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #Make frames resizable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
        self.calculate_model()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def update_plot(self,text,probabilistic_list, event=None):
        # Clear previous plot
        self.ax.clear()
        
        if len(probabilistic_list) != len(languages):
            raise ValueError("Length of probabilistic_list does not match the length of languages")
        
        #Create dict to associate each percentage to it
        lan_dict = {}
        i=0
        for value in languages:
                lan_dict[value] = probabilistic_list[i]
                i += 1
        
        sorted_assoc = sorted(lan_dict.items(), key=lambda x: x[1], reverse=True)

        # Plot based on putuation of languages
        if text.isdigit() and int(text) > 0:
            self.flag.set(True)
            self.ax.bar([x[0] for x in sorted_assoc[:4]], [x[1] for x in sorted_assoc[:4]])
            self.ax.set_xlabel('Values')
            self.ax.set_ylabel('Random Numbers')
            self.ax.set_title('Language example output')
            self.letters_count.delete(1.0, tk.END)
            self.letters_count.insert(tk.END, "Random numbers generated:\n")
            for idx, rnd in enumerate(sorted_assoc):
                self.letters_count.insert(tk.END, f"{rnd[0]}: {rnd[1]:.2f}\n")
            
        else:
            self.flag.set(False)
        
        # Redraw canvas
        self.plot_canvas.draw()
    
    def calculate_model(self,event=None):
        # Get the text from the text box & check is not the same as before
        text = self.text_box.get()
        
        if text == self.previousText:
            return   
        
        self.previousText = text

        kalman_filter = kalman.KalmanFilter()
#####   observation = model_output
        kalman_filter.update(observation=observation) 
        current_language_probabilities = kalman_filter.state
        
        #################################
        #Use model to obtain percentages for each class (temporarly random number)
        rnd_number = [random.random() for i in range(3)]
        last_number = 1- sum(rnd_number)
        rnd_number.append(last_number)
        #################################

        self.update_plot(text,rnd_number)

    def on_close(self):
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
    
    
