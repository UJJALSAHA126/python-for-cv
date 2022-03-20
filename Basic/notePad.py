from tkinter import *
from tkinter import messagebox
from tkinter import colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

allFonts = ['Bahnschrift Light SemiCondensed', 'Bahnschrift SemiBold',
            'Arial', 'Comic Sans MS', 'Constantia', 'Algerian', 'Calisto MT',
            'Georgia', 'Calibri', 'lucida', 'Mangal', 'Bahnschrift',
            'Bookman Old Style', 'Segoe UI Black', 'Lucida Console',
            'Lucida Sans Unicode', 'Times New Roman']
currFont = 1

appName = '7U NotePad'
appVersion = '1.0.0'

height = 400
width = 500

menuSize = 10
menuFont = allFonts[3]

fo_nt = allFonts[currFont]
si_ze = 15
st_yle = ' '


def saveFile():
    global file, filePath
    if filePath == None:
        temp = asksaveasfilename(initialdir=os.getcwd(),
                                 initialfile='Untitled', defaultextension=',txt',
                                 filetypes=(('Text Files', '*.txt'), ('HTML Files', '.html')))
        if temp == '':
            messagebox.showerror(title='No File Found',
                                 message='You Have Not Chhosen A File !!')
            return
        else:
            filePath = temp

            with open(filePath, 'w') as file:
                file.write(textArea.get(1.0, END))
    else:
        with open(filePath, 'w') as file:
            file.write(textArea.get(1.0, END))


def openFile():
    global file, filePath
    temp = askopenfilename(initialdir=os.getcwd(), defaultextension='.txt',
                           filetypes=[('Text Files', '*.txt')])
    if temp == '':
        return
    newFile()
    nFileName = os.path.basename(temp)+f' - {appName}'
    root.title(nFileName)
    filePath = temp
    file = open(filePath, 'r')
    allData = file.read()
    file.close()
    textArea.insert(1.0, allData)


def newFile():
    global file, filePath
    file = None
    filePath = None
    textArea.delete('1.0', END)
    root.title(f'Untitled - {appName}')


def chooseColor():
    color = colorchooser.askcolor()
    hex = color[1]
    print(hex)
    textArea.config(fg=hex)


def chooseSize():
    global newWindow, scale
    newWindow = Toplevel(bg='#fcff6c')
    newWindow.maxsize(500, 90)
    newWindow.minsize(500, 90)
    newWindow.title('Select Text Size')

    scale = Scale(newWindow, from_=5, to=100, tickinterval=5,
                  orient=HORIZONTAL, length=500, bg='#b472fc')
    scale.pack(expand=True, fill=X)
    scale.set(si_ze)

    Button(newWindow, text='Submit', font='Arial 10 bold',
           bg='#0cfc54', command=setSize).pack()

    newWindow.mainloop()


def cooseFont():
    global newFontWindow, num
    nWidth = 250
    nHeight = 190
    newFontWindow = Toplevel()
    newFontWindow.title('Fonts')
    newFontWindow.geometry(f'{nWidth}x{nHeight}')
    # newFontWindow.resizable(False, False)

    frame = Frame(newFontWindow)
    frame.pack(expand=True, fill=BOTH)

    myCanvas = Canvas(frame, width=0, height=0)
    myCanvas.pack(side=LEFT, expand=True, fill=BOTH)

    myScrollbar = Scrollbar(frame, orient=VERTICAL, command=myCanvas.yview)
    myScrollbar.pack(side=RIGHT, fill=Y)

    myCanvas.config(yscrollcommand=myScrollbar.set)
    myCanvas.bind('<Configure>', lambda e: myCanvas.configure(
        scrollregion=myCanvas.bbox('all')))

    secFrame = Frame(myCanvas, bg='#87c4e4')
    myCanvas.create_window((0, 0), window=secFrame, anchor='nw')

    num = IntVar(value=currFont)
    for i, item in enumerate(allFonts):
        radBtn = Radiobutton(secFrame, text=str(item), bg='#87c4e4',
                             variable=num, value=i, command=fontClicked,
                             font=(f'{item}', 15), relief=SUNKEN)
        radBtn.pack(anchor='w')

    secFrame.update()
    nWidth = int(secFrame.winfo_width())+20
    # print(nWidth,nHeight)
    newFontWindow.geometry(f'{nWidth}x{nHeight}')
    # newFontWindow.update()
    # print(newFontWindow.winfo_width())
    newFontWindow.resizable(False, False)


def fontClicked():
    global currFont
    currFont = int(num.get())
    _font = allFonts[currFont]
    textArea.config(font=(_font, si_ze, st_yle))


def setSize(s_z=None, st_le=None):
    global si_ze
    if s_z is None and st_le is None:
        try:
            s_z = str(scale.get())
            si_ze = int(s_z)
            st_yle = " "
        except:
            s_z = str(20)
            si_ze = int(s_z)
            st_yle = " "

    textArea.config(font=f'{fo_nt} {s_z} {st_yle}')
    newWindow.destroy()


def main():
    global root, textArea, file, filePath

    filePath = None
    file = None

    root = Tk()
    root.title(f'Untitled - {appName}')
    root.geometry(f'{width}x{height}')
    # root.eval('tk::PlaceWindow . center')

    createMenu()

    textArea = Text(root, bg='#ffffae', font=(f'{fo_nt}', si_ze, st_yle))
    textArea.pack(expand=True, fill=BOTH)

    addScrollBar(textArea)

    root.mainloop()


def createMenu():
    global menuBar, fileMenu, editMenu, helpMenu

    menuBar = Menu(root)
    root.config(menu=menuBar)

    # Creating File Menu
    fileMenu = Menu(menuBar, tearoff=0)
    fileMenu.add_command(label='Save', command=saveFile,
                         font=(f'{menuFont}', f'{menuSize}'))
    fileMenu.add_command(label='Open', command=openFile,
                         font=(f'{menuFont}', f'{menuSize}'))
    fileMenu.add_command(label='New', command=newFile,
                         font=(f'{menuFont}', f'{menuSize}'))
    fileMenu.add_separator()
    fileMenu.add_command(label='Close', command=close,
                         font=(f'{menuFont}', f'{menuSize}'))

    # Creating Edit Menu
    editMenu = Menu(menuBar, tearoff=0)
    editMenu.add_command(label='Copy', command=copyTxt,
                         font=(f'{menuFont}', f'{menuSize}'))
    editMenu.add_command(label='Cut', command=cutTxt,
                         font=(f'{menuFont}', f'{menuSize}'))
    editMenu.add_command(label='Paste', command=pasteTxt,
                         font=(f'{menuFont}', f'{menuSize}'))

    # Creating Font Menu
    fontMenu = Menu(menuBar, tearoff=0)
    fontMenu.add_command(label='Text Size', command=chooseSize,
                         font=(f'{menuFont}', f'{menuSize}'))
    fontMenu.add_command(label='Text Font', command=cooseFont,
                         font=(f'{menuFont}', f'{menuSize}'))
    fontMenu.add_command(label='Text Colour', command=chooseColor,
                         font=(f'{menuFont}', f'{menuSize}'))

    # Creating Help Menu
    helpMenu = Menu(menuBar, tearoff=0)
    helpMenu.add_command(label=f'About {appName} !', command=helpBtn,
                         font=(f'{menuFont}', f'{menuSize}'))

    menuBar.add_cascade(label='File', menu=fileMenu)
    menuBar.add_cascade(label='Edit', menu=editMenu)
    menuBar.add_cascade(label='Font', menu=fontMenu)
    menuBar.add_cascade(label='Help', menu=helpMenu)


def addScrollBar(txtArea=Text | None, frame=Frame | None):
    # Adding Scrollbar
    if txtArea is not None:
        scrollBar = Scrollbar(txtArea)
        scrollBar.pack(side=RIGHT, fill=Y)
        scrollBar.config(command=txtArea.yview)
        txtArea.config(yscrollcommand=scrollBar.set)
    elif frame is not None:
        myCanvas = Canvas(frame)
        myCanvas.pack(expand=True, fill=BOTH)
        scrollBar = Scrollbar(frame, orient=VERTICAL, command=myCanvas.yview)
        scrollBar.pack(expand=True, fill=Y)


def copyTxt():
    textArea.event_generate(("<<Copy>>"))


def cutTxt():
    textArea.event_generate(("<<Cut>>"))


def pasteTxt():
    textArea.event_generate(("<<Paste>>"))


def close():
    root.destroy()
    exit()


def helpBtn():
    messagebox.showinfo(title=f'About {appName}',
                        message=f'Current Version {appVersion}')


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except:
    #     exit()
