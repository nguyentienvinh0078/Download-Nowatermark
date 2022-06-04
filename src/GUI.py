from tkinter import *
from tkinter.ttk import Progressbar, Style
from tkinter import messagebox
from turtle import title

class GUI:
    def __init__(self):
        # self.window = self.windowInit()
        pass
        
    def msg(self, msgs, titles='ERROR'):
        if 'ERROR' in titles or 'error' in titles:
            messagebox.showerror(f'{titles}', f'😥😣 BUG 😥😣\n{msgs}')
        elif 'quit' in titles or 'Quit' in titles:
            messagebox.askokcancel(f'{titles}', f'{msgs}')
        else:
            messagebox.showinfo(f'{titles}', f'{msgs}')

    def windowInit(self, title='™✅ V I N G ✅™', bgColor='#1B9AAA'):
        window = Tk()
        window.title(title)
        window.resizable(False, False)
        window.configure(bg=bgColor)
        return window

    def createFrame(self, window, layout, frameName, bgColor='#1B9AAA', borderFrame=False):
        frame = LabelFrame(window, bg=bgColor)
        if not borderFrame:
            frame.configure(relief='flat')
        else:
            frame.configure(text=frameName)
        row, col = dict(layout.items())[frameName]
        frame.grid(row=row, column=col, sticky=NSEW)
        frame.grid_configure(padx=5, pady=5)
        return frame
    
    def createNoneFrame(self, window):
        frame = LabelFrame(window)
        return frame

    def createLabel(self, labelMsg, layout, frameName, labelName, bgColor='#1B9AAA', fgColor='white', fonts='Arial 13 bold'):
        labelText = StringVar()
        label = Label(frameName, textvariable=labelText, borderwidth=0, bg=bgColor, fg=fgColor, justify=CENTER, font=fonts)
        labelText.set(labelMsg)
        row, col = dict(layout.items())[labelName]
        label.grid(row=row, column=col, sticky=NSEW)
        label.grid_configure(padx=5, pady=5)
        frameName.columnconfigure(1, weight=1)
        return label, labelText

    def createEntry(self, layout, frameName, entryName, entryWidth=60, entryHeight=8, borderWidth=1, fonts='Arial 13 bold'):
        entry = Entry(frameName, width=entryWidth, borderwidth=borderWidth, justify=CENTER, font=fonts)
        row, col = dict(layout.items())[entryName]
        entry.grid(row=row, column=col, ipady=entryHeight, sticky=NSEW)
        entry.grid_configure(padx=5, pady=5)
        return entry

    def insertEntryText(self, entry, textInsert):
        entry.delete(0, END)
        entry.insert(0, textInsert)
    
    def deleteEntryext(self, entry):
        entry.delete(0, END)
        entry.insert(END, '')
    
    def getEntryText(self, entry):
        return entry.get()

    def configEntryState(self, entry, state=1):
        if state == 1:
            entry.configure(state='normal')
        elif state == 0:
            entry.configure(state='disabled')
        else:
            pass

    def createButton(self, layout, frameName, buttonName, callbackFuntion, bgColor='#06D6A0', fgColor='black', borderWidth=1, buttonWidth=10, fonts='Arial 13 bold'):
        button = Button(frameName, text=buttonName, justify=CENTER, command=callbackFuntion)
        button.configure(font=fonts, borderwidth=borderWidth, width=buttonWidth, bg=bgColor, fg=fgColor)
        row, col = dict(layout.items())[buttonName]
        button.grid(row=row, column=col, sticky=NSEW)
        button.grid_configure(padx=5, pady=5)
        return button

    def configActiveButton(self, button, texts, bgColor='#06D6A0', fgColor='black'):
        button.configure(state='active', bg=bgColor, fg=fgColor, text=texts)
        button.configure(activebackground=bgColor, activeforeground=fgColor)
    
    def configDisableButton(self, button, texts, bgColor='lightcoral', fgColor='white'):
        button.configure(state='disabled', bg=bgColor, fg=fgColor, text=texts)
        button.configure(activebackground=bgColor, activeforeground=fgColor)

    def createProgress(self, layout, frameName, progressName, progressHeight=6):
        style = Style(self.window)
        style.layout('text.Horizontal.TProgressbar',
            [('Horizontal.Progressbar.trough',
            {'children': [('Horizontal.Progressbar.pbar',{'side': 'left', 'sticky': 'ns'})],
            'sticky': 'nswe'}),
            ('Horizontal.Progressbar.label', {'sticky': ''})])

        # 
        progress = Progressbar(frameName, style='text.Horizontal.TProgressbar', value=0)
        row, col = dict(layout.items())[progressName]
        progress.grid(row=row, column=col, ipady=progressHeight, sticky=NSEW)
        progress.grid_configure(padx=5, pady=5)
        frameName.columnconfigure(1, weight=1)
        return style, progress
    
    def progressDefault(self, texts, style, fonts='Arial 13 bold'):
        style.configure('text.Horizontal.TProgressbar', text=texts, font=fonts)

    def progressPercent(self, percentage, texts, frame, style, progress, fonts='Arial 13 bold'):
        style.configure('text.Horizontal.TProgressbar', text=texts, font=fonts)
        frame.update_idletasks()
        progress['value'] = percentage

    def run(self):
        self.window.mainloop()

def main():
    try:
        gui = GUI()
        gui.run()
    except Exception as bug:
        messagebox.showinfo('ERROR', '😥😣 BUG 😥😣\n{}'.format(bug))

if __name__ == '__main__':
    main()
