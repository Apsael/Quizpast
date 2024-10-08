import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
import json
import pygame
import os
from pathlib import Path
from PIL import Image, ImageTk

class Trivia:
    def __init__(self):
        self.q_no = 0
        self.display_title() 
        self.display_start_screen()
        self.opt_selected = IntVar()
        self.data_size = len(question)
        self.correct = 0
        self.wrong = 0
        self.user_answers = []  # Para almacenar las respuestas del usuario
        self.answer = answer  # Definir answer como atributo de la clase

    def play_background_music(self, file_path):
        pygame.init()
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(loops=-1)
        except pygame.error as e:
            mb.showerror("Error occurred while playing music:", e)

    def bg_music(self):
        music_file = Path(__file__).parent / 'Sounds' / 'bg_music.wav'
        self.play_background_music(music_file)

    def play_sound_effect(self, file_name):
        sound_file = Path(__file__).parent / 'Sounds' / file_name
        sound = pygame.mixer.Sound(sound_file)
        sound.play()

    def display_background(self, bg_file):
        bg_image = Image.open(bg_file)
        bg_image = ImageTk.PhotoImage(bg_image)
        bg_label = Label(gui, image=bg_image)
        bg_label.image = bg_image  # Mantener referencia para evitar coleccion de basura
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def display_result(self):
        score = int(self.correct / self.data_size * 100)
        result = f"Score: {score}%"
        
        correct_answers = [f"Question {i + 1}: Correct" for i in range(self.data_size) if self.user_answers[i] == self.answer[i]]
        wrong_answers = [f"Question {i + 1}: Wrong" for i in range(self.data_size) if self.user_answers[i] != self.answer[i]]

        # Crear una nueva ventana para mostrar los resultados
        result_window = Toplevel(gui)
        result_window.geometry("400x500")
        result_window.resizable(False, False)
        result_window.title("Resultados")
        result_window.config(bg="lightblue")

        # Etiqueta de título
        title_label = Label(result_window, text="Resultados del Quiz", font=("Arial", 20, "bold"), bg="lightblue")
        title_label.pack(pady=10)

        # Etiqueta de puntuación
        score_label = Label(result_window, text=result, font=("Arial", 16), bg="lightblue")
        score_label.pack(pady=5)

        # Etiquetas para las respuestas correctas
        if correct_answers:
            correct_label = Label(result_window, text="Respuestas correctas:", font=("Arial", 14, "bold"), bg="lightblue")
            correct_label.pack(pady=5)
            for answer in correct_answers:
                answer_label = Label(result_window, text=answer, font=("Arial", 12), bg="lightblue")
                answer_label.pack()

        # Etiquetas para las respuestas incorrectas
        if wrong_answers:
            wrong_label = Label(result_window, text="Respuestas incorrectas:", font=("Arial", 14, "bold"), bg="lightblue")
            wrong_label.pack(pady=5)
            for answer in wrong_answers:
                answer_label = Label(result_window, text=answer, font=("Arial", 12), bg="lightblue")
                answer_label.pack()

        # Botón de cerrar
        close_button = Button(result_window, text="Cerrar", command=gui.quit, bg="red", fg="white", font=("Arial", 12))
        close_button.pack(pady=20)

        result_window.mainloop()

    def check_ans(self, q_no):
        if self.opt_selected.get() == self.answer[q_no]:
            return True
        else:
            return False

    def next_btn(self):
        # Almacenar la respuesta del usuario
        self.user_answers.append(self.opt_selected.get())
        
        if self.check_ans(self.q_no):
            self.correct += 1
            self.play_sound_effect('correct_sound.wav')
        else:
            self.wrong += 1
            self.play_sound_effect('incorrect_sound.wav')

        self.q_no += 1
        if self.q_no == self.data_size:
            self.display_result()
            gui.destroy()
        else:
            # Change the background depending on the question number
            bg_file = Path(__file__).parent / 'Background' / f'bg_{(self.q_no % 3) + 1}.png'
            self.display_background(bg_file)
            self.display_question()
            self.display_options()

    def buttons(self):
        next_button = Button(gui, text="Next", command=self.next_btn,
                             width=10, bg="green", fg="white", font=("ariel", 16, "bold"))
        next_button.place(x=350, y=380)

        quit_button = Button(gui, text="Quit", command=gui.destroy,
                             width=5, bg="red", fg="white", font=("ariel", 16, "bold"))
        quit_button.place(x=700, y=50)

    def display_options(self):
        val = 0
        self.opt_selected.set(0)
        for option in options[self.q_no]:
            self.opts[val]['text'] = option
            val += 1

    def display_question(self):
        for widget in gui.winfo_children():
            widget.destroy()

        # Change the background depending on the question number
        bg_file = Path(__file__).parent / 'Background' / f'bg_{(self.q_no % 3) + 1}.png'
        self.display_background(bg_file)

        q_no = Label(gui, text=question[self.q_no], width=60,
                     font=('ariel', 16, 'bold'), anchor='w', bg='lightyellow')
        q_no.place(x=70, y=100)
        self.opts = self.radio_buttons()
        self.display_options()
        self.buttons()

    def display_title(self):
        title = Label(gui, text="Quizpast", width=50, bg="gray", fg="white", font=("ariel", 20, "bold"))
        title.place(x=0, y=2)

    def radio_buttons(self):
        q_list = []
        y_pos = 150
        while len(q_list) < 4:
            radio_btn = Radiobutton(gui, text=" ", variable=self.opt_selected, value=len(q_list) + 1,
                                    font=("ariel", 14), bg='lightyellow')
            q_list.append(radio_btn)
            radio_btn.place(x=100, y=y_pos)
            y_pos += 40
        return q_list

    def display_start_screen(self):
        for widget in gui.winfo_children():
            widget.destroy()

        # Display the first background on the start screen
        bg_file = Path(__file__).parent / 'Background' / 'bg_1.png'
        self.display_background(bg_file)

        self.display_title()
        start_button = Button(gui, text="Play", command=self.start_game,
                             width=10, bg="green", fg="white", font=("ariel", 16, "bold"))
        start_button.place(x=350, y=200)

    def start_game(self):
        self.display_question()

# create a GUI Window
gui = Tk()
gui.geometry("800x450")
gui.resizable(False, False)
gui.title("Quizpast")

# get the data from the json file with utf-8 encoding
data_file = Path(__file__).parent / 'data.json'
with open(data_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# set the question, options, and answer
question = data['question']
options = data['options']
answer = data['answer']

# create an object of the Quiz Class.
trivia = Trivia()
# start the music
trivia.bg_music()
# start the GUI
gui.mainloop()
