import difflib
import tkinter
from tkinter import messagebox

class plagiarism_checker:
    def root_quit(self):
        self.root.destroy()
    def quit_plagiarised_window(self):
        self.plagiarised_window.destroy()
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Plagiarism Checker')
        self.root.geometry('650x600')
        self.root.iconbitmap('plagiar_icon.ico')
        self.root.state('zoomed')

        def_x = 50
        def_y = 25

        lbl_root_title = tkinter.Label(self.root, text='Plagiarism Checker')
        lbl_root_title.config(font=('TkDefaultFont, '))
        lbl_root_title.place(x=def_x, y=def_y)

        lbl_for_checking = tkinter.Label(self.root, text='Entry text to check',font='TkDefaultFont, 10')
        lbl_for_checking.place(x=def_x, y=def_y+90)
        self.ent_for_checking = tkinter.Text(self.root, height=16, width=62)
        self.ent_for_checking.place(x=def_x, y=def_y+120)

        lbl_website_for_checking = tkinter.Label(self.root, text='Enter website to compare')
        lbl_website_for_checking.place(x=def_x, y=def_y+410)
        self.ent_website_for_checking = tkinter.Entry(self.root, width=90)
        self.ent_website_for_checking.place(x=def_x, y=def_y+440, height=30)

        self.btn_calc_plagiarisedness = tkinter.Button(self.root, text='Calculate', command=self.calc_plagiarisedness,
                                                       borderwidth=10, height=2, width=16)
        self.btn_calc_plagiarisedness.place(x=def_x + 180, y=def_y + 510)

        self.btn_exit_win = tkinter.Button(self.root, text='Quit', command=self.root_quit,
                                           height=2, width=9, borderwidth=5)
        self.btn_exit_win.place(x=def_x+430, y=def_y+510)

        self.root.mainloop()

    def calc_plagiarisedness(self):
        try:
            user_text_entry = self.ent_for_checking.get('1.0', tkinter.END)
            website_for_compare = requests.get(self.ent_website_for_checking.get()).text
            soup = bs4.BeautifulSoup(website_for_compare, 'lxml')
            soup_text = soup.findAll(text=True)

            visible_text = ''
            for each_char in soup_text:
                visible_text = visible_text + each_char
            web_text_for_compare = visible_text

            compare_sequences = difflib.SequenceMatcher(None, user_text_entry, web_text_for_compare)
            amount_plagiarised = compare_sequences.ratio()
            amount_plagiarised_percentage = float(amount_plagiarised*100)
            amount_plagiarised_percentage = round(amount_plagiarised_percentage, 2)

            self.ent_for_checking.delete('1.0', tkinter.END)
            self.ent_website_for_checking.delete('0', tkinter.END)

            self.plagiarised_window = tkinter.Toplevel()
            self.plagiarised_window.geometry('256x170')
            self.plagiarised_window.iconbitmap('plagiar_icon.ico')

            btn_exit_plagiarised_window = tkinter.Button(self.plagiarised_window, text='Quit', borderwidth=5,command=self.quit_plagiarised_window, height=1, width=8)
            btn_exit_plagiarised_window.place(x=93, y=120)

            if amount_plagiarised_percentage > .5:  
                plagiarism_info_text = str(amount_plagiarised_percentage)\
                                       + '% Plagiarised'
                plagiarism_info_text.format(amount_plagiarised_percentage)
                lbl_plagiarism_info = tkinter.Label(self.plagiarised_window, text=plagiarism_info_text,fg='red')
                lbl_plagiarism_info.config(font=('TkDefaultFont, 16'))
                lbl_plagiarism_info.place(x=32, y=39)
            else:  
                plagiarism_info_text = 'Not Plagiarised-' + '\n' +\
                        str(amount_plagiarised_percentage) + '% plagiarised'
                lbl_plagiarism_info = tkinter.Label(self.plagiarised_window, text=plagiarism_info_text,fg='green')
                lbl_plagiarism_info.config(font=('TkDefaultFont, 16'))
                lbl_plagiarism_info.place(x=49, y=28)

        except BaseException:
            messagebox.showerror('User Error', 'Invalid URL')

plagiarism_checker()
