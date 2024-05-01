import os,sys
import tkinter as tk
import random
import numpy as np
from tkinter import ttk
from tkinter import scrolledtext
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import kalman
import pickle


#List and dict(obtain them from other file separated in the future)

languages = []
color_map = {'German': 'red', 'English': 'green', 'Spanish': 'blue', 'French': 'yellow'}

n_languages = 4

model_filename = "./Trained_model.sav"
cv_filename = "./cv.sav"
le_filename = "./le.sav"


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language detector on fly")
        
        self.flag = tk.BooleanVar()
        self.flag.set(False)
        self.geometry("900x600")

        #Initialize model and kalman
        

        self.loaded_model = pickle.load(open(model_filename,'rb'))
        self.loaded_cv = pickle.load(open(cv_filename,'rb'))
        self.loaded_le = pickle.load(open(le_filename,'rb'))
        
        #Create languages list
        for i in range(n_languages):
            lan = self.loaded_le.inverse_transform([i])
            languages.append(lan[0])

        self.kalman_filter = kalman.KalmanFilter(n_languages=n_languages)

        #Variables of class GUI
        self.previousText=""

        # Create frames for subdividing window


        left_frame = tk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew")

        upper_frame = tk.Frame(left_frame)
        upper_frame.pack(side="top", fill="both", expand=True)

        bottom_frame = tk.Frame(left_frame)
        bottom_frame.pack(side="bottom", fill="both", expand=True)
        
        mid_left_frame = tk.Frame(bottom_frame)
        mid_left_frame.pack(side="top",fill="both",expand=True)
        
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
        #Text Box widget
        self.text_box = ttk.Entry(upper_frame)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.text_box.insert(0,'Enter your text here...')
        self.text_box.config(foreground='grey')  # Set text color to grey
        self.text_box.bind("<KeyRelease>", self.calculate_model)
        #self.text_box.bind("<FocusOut>", self.on_focus_out(self.text_box))
        self.text_box.bind("<FocusIn>",self.on_entry_click)       
        
        self.fig, self.ax = plt.subplots(figsize=(7,5)) #Adjust plot size 
        self.plot_canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.plot_canvas.get_tk_widget().pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #Mid widget
        self.finalPrediction = tk.Entry(mid_left_frame,state='readonly')
        self.finalPrediction.pack(padx=10,pady=10,fill=tk.BOTH,expand=True)

        #Test widgets in botton part
        self.letters_count = tk.Text(bottom_frame)
        self.letters_count.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #Make frames resizable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
        self.calculate_model()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_entry_click(self,event=None):
        entry = self.text_box
        if entry.get() == 'Enter your text here...':
            entry.delete(0, tk.END)
            entry.config(foreground='black')

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
        
        bars = self.ax.bar([x[0] for x in sorted_assoc[:4]], [x[1] for x in sorted_assoc[:4]],
                   color=[color_map[x[0]] for x in sorted_assoc[:4]])

        self.ax.set_xlabel('Languages')
        self.ax.set_ylabel('Languages probabilities')
        self.ax.set_title('Probabilities of Languages')

        self.finalPrediction.config(state='normal')
        self.finalPrediction.delete(0,tk.END)
        self.finalPrediction.insert(tk.END, "The input language is likely to be: ")
        self.finalPrediction.insert(tk.END,sorted_assoc[0][0])
        self.finalPrediction.config(state='readonly')

        self.letters_count.delete(1.0, tk.END)
        self.letters_count.insert(tk.END, "Random numbers generated:\n")
        for idx, rnd in enumerate(sorted_assoc):
            self.letters_count.insert(tk.END, f"{rnd[0]}: {rnd[1]:.2f}\n")

        self.ax.legend(bars, [x[0] for x in sorted_assoc[:4]])
        self.plot_canvas.draw()
    
    def calculate_model(self,event=None):
        # Get the text from the text box & check is not the same as before
        text = self.text_box.get()
        
        if text == self.previousText:
            return   
        
        self.previousText = text

        x = self.loaded_cv.transform([text]).toarray()
        lang = self.loaded_model.predict(x)
        lang_string = self.loaded_le.inverse_transform(lang)

        index_language = languages.index(lang_string[0])
        observation = [0] * len(languages)
        observation[index_language] = 1


        self.kalman_filter.update(observation=observation) 
        current_language_probabilities = self.kalman_filter.state
        
        #################################
        #Use model to obtain percentages for each class (temporarly random number)
        rnd_number = [random.random() for i in range(3)]
        last_number = 1- sum(rnd_number)
        rnd_number.append(last_number)
        #################################

        self.update_plot(text,current_language_probabilities)

    def on_close(self):
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
    
    
