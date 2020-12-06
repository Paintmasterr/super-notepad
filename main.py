from tkinter import *
from tkinter import filedialog, font, ttk, scrolledtext
from gtts import gTTS
import os
from textblob import TextBlob
import speech_recognition as sr

root = Tk()
root.title("NotePad")
root.geometry('800x500')
root.resizable(0, 0)
root.iconbitmap(default='notepad.ico')
language = 'en'
current_open_file = 'no file'
font_ = 'Consoles'
size = 10
weight = 'normal'

try:
    def speech_to_text():
        p = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            print('Speak: ')
            audio = p.listen(source)
            try:
                text = p.recognize_google(audio)

                text_area.insert(END, text.capitalize())

                s = text.split()
                if s[0] in ('are', 'is', 'have', 'has', 'where',
                            'how', 'what', 'when', 'do', "don't", 'does', "doesn't"):
                    text_area.insert(END, '? ')
                else:
                    text_area.insert(END, '. ')
            except:
                print("Cannot hear you")
except:
    pass


def font_combobox(event):
    global font_
    font_ = font_box.get()


def size_combobox(event):
    global size
    size = size_box.get()


def style_combobox(event):
    global weight
    weight = style_box.get()


def font_window():
    global font_box
    global size_box
    global style_box

    window = Toplevel(root)
    window.geometry('455x435')
    window.title('Font')

    font_tuple = font.families()
    font_label = Label(window, text='Font:').place(x=5, y=2)
    font_family = StringVar()
    font_box = ttk.Combobox(window, width=22,
                            textvariable=font_family,
                            state='readonly',
                            height=12)
    font_box['values'] = font_tuple
    font_box.current(font_tuple.index('Arial'))
    font_box.grid(row=0, column=0, padx=5, pady=5)
    font_box.bind('<<ComboboxSelected>>', font_combobox)

    style_label = Label(window, text='Font style:').place(x=170, y=2)
    font_style = ('bold', 'normal')
    font_style_var = StringVar()
    style_box = ttk.Combobox(window, width=20,
                             textvariable=font_style_var,
                             state='readonly')
    style_box['values'] = font_style
    style_box.grid(row=0, column=1, padx=5, pady=5)
    style_box.bind('<<ComboboxSelected>>', style_combobox)

    size_label = Label(window, text='Size:').place(x=325, y=2)
    size_tuple = (8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72)
    size_ = IntVar()
    size_box = ttk.Combobox(window, width=15,
                            textvariable=size_,
                            state='readonly',
                            height=12)
    size_box['values'] = size_tuple
    size_box.grid(row=0, column=2, padx=5, pady=20)
    size_box.bind('<<ComboboxSelected>>', size_combobox)

    def OK():
        text_area.config(font=(font_, size, weight))

    OK = Button(window, text='OK', command=OK).place(x=280, y=400, width=70)

    Cancel = Button(window, text='Cancel', command=window.destroy)
    Cancel.place(x=360, y=400, width=70)


def play():
    try:
        text_ = text_area.get(1.0, END)
        audio = gTTS(text=text_, lang=language, slow=False)
        audio.save('T22S.wav')
        os.system('T22S.wav')
    except AssertionError:
        pass


def spell_check():
    text_ = text_area.get(1.0, END)
    corrected_text = TextBlob(text_)
    text_area.delete(1.0, END)
    for line in str(corrected_text.correct()):
        text_area.insert(END, line)


def new_file():
    global current_open_file
    text_area.delete(1.0, END)
    current_open_file = 'no_file'


def open_file():
    global current_open_file
    open_return = filedialog.askopenfile(initialdir='/',
                                         title='select file to open',
                                         filetypes=(('text files',
                                                     '*.txt'),
                                                    ('all files',
                                                     '*.*')))
    if open_return is not None:
        text_area.delete(1.0, END)
        for line in open_return:
            text_area.insert(END, line)
        current_open_file = open_return.name
        open_return.close()


def save():
    if current_open_file == 'no file':
        save_as_file()
    else:
        with open(current_open_file, 'w+') as file:
            file.write(text_area.get(1.0, END))


def save_as_file():
    global current_open_file
    file = filedialog.asksaveasfile(mode='w',
                                    defaultextension='.txt')
    if file is None:
        return
    text_to_save = text_area.get(1.0, END)
    current_open_file = file.name
    file.write(text_to_save)
    file.close()


def copy_():
    text_area.clipboard_clear()
    text_area.clipboard_append(text_area.get(1.0, END))


def cut_():
    text_area.delete(1.0, END)


def paste():
    text_area.insert(INSERT, text_area.clipboard_get())


def redo():
    try:
        text_area.edit_redo()
    except:
        pass


text_area = scrolledtext.ScrolledText(root, undo=True,
                                      wrap=WORD, relief=FLAT,
                                      width=600, height=400)
text_area.pack(fill=Y, expand=1)

main_menu = Menu()
root.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save as...', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.destroy)

edit_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Undo', command=text_area.edit_undo)
edit_menu.add_separator()
edit_menu.add_command(label='Redo', command=redo)

edit_menu.add_command(label='Copy', command=copy_)
edit_menu.add_command(label='Cut', command=cut_)
edit_menu.add_command(label='Paste', command=paste)

text_to_speech = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label='Features', menu=text_to_speech)
text_to_speech.add_command(label='Text to Speech', command=play)
text_to_speech.add_separator()
text_to_speech.add_command(label='Spell Check', command=spell_check)
text_to_speech.add_separator()
text_to_speech.add_command(label='Speech to Text', command=speech_to_text)

font_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Format", menu=font_menu)
font_menu.add_command(label='Font...', command=font_window)

root.mainloop()
