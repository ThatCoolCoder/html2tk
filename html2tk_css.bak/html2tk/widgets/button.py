import tkinter as tk
import tkinter.ttk as ttk

import html2tk.widgets

class Button(html2tk.widgets.Widget)::
    def __init__(self, master, html_soup_element, font):
        super().__init__(master, html_soup_element)
        
        text = self.get_text_from_element(html_soup_element)

        style_name = self.create_unique_ttk_style_name('TButton')
        style = ttk.Style(self.master)
        style.configure(style_name, font=font)
        self.tk_widget = ttk.Button(self.master, text=text, style=style_name)

    @property
    def command(self):
        return self.tk_widget.cget('command')

    @command.setter
    def command(self, callback):
        self.tk_widget.configure(command=callback)