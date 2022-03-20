from tkinter import *
from tkinter import colorchooser
from time import strftime
from tkinter.font import ITALIC
from tkinter.messagebox import showerror
import pickle
import os

appName = '7U Digital Clock'
appVersion = '1.0.5'
pickleFilePath = f'c:\\{appName}\\clockDetails.pkl'

doubleClickedOnce = False

clockSize = 65
clockColor = 'red'
currFont = 2
allFonts = ['Bahnschrift Light SemiCondensed', 'Bahnschrift SemiBold', 'ds-digital',
            'Arial', 'Comic Sans MS', 'Constantia', 'Algerian', 'Calisto MT',
            'Georgia', 'Calibri', 'lucida', 'Mangal', 'Bahnschrift',
            'Bookman Old Style', 'Segoe UI Black', 'Lucida Console',
            'Lucida Sans Unicode', 'Times New Roman']


def changeTime():
    sTime = strftime('%I:%M:%S %p')
    label.config(text=sTime)
    label.after(1000, changeTime)


def main():
    global root, label
    root = Tk()
    try:
        # icon = PhotoImage(file=r'C:\Users\PURNIMA SAHA\Desktop\VS Code\Python\Mini Prjects\DownloadedVideos\DigitalClockIcon.ico')
        root.iconbitmap(r'C:\Users\PURNIMA SAHA\Desktop\VS Code\Python\Mini Prjects\DownloadedVideos\DigitalClockIcon.ico')
    except:
        pass
    root.title("7U Digital Clock")
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)

    label = Label(root, font=(allFonts[currFont], clockSize),
                  background='black', foreground=clockColor)
    label.pack(fill=BOTH)
    label.bind('<Double-Button-1>', doubleClicked)
    changeTime()

    root.mainloop()



def doubleClicked(e):

    global newWindow, colorLabel, sizeText, sFont, doubleClickedOnce

    if doubleClickedOnce:
        return

    doubleClickedOnce = True
    newWindow = Toplevel(bg='#ffb36c')
    newWindow.protocol('WM_DELETE_WINDOW', win_closed)
    newWindow.resizable(False, False)

    Label(newWindow, text='Clock Size', bd=2, relief=RAISED,
          font=('Bahnschrift SemiBold', 17)).grid(row=0, column=0, pady=10)
    # Label(newWindow, text='          ', font=(15)).grid(row=0, column=1)
    Label(newWindow, text='Clock Font', bd=2, relief=RAISED,
          font=('Bahnschrift SemiBold', 17)).grid(row=0, column=2, pady=10)
    # Label(newWindow, text='          ', font=(15)).grid(row=0, column=3)
    Label(newWindow, text='Clock Color', bd=2, relief=RAISED,
          font=('Bahnschrift SemiBold', 17)).grid(row=0, column=4, pady=10)
    # Label(newWindow, text='          ', font=(15)).grid(row=0, column=5)

    sizeText = Entry(newWindow, font=(20), justify=CENTER, bd=2, relief=SUNKEN)
    sizeText.insert(0, clockSize)
    sizeText.grid(row=1, column=0, padx=5, pady=5)

    sFont = StringVar(value=allFonts[currFont])

    fontDrop = OptionMenu(newWindow, sFont, *allFonts)
    fontDrop.grid(row=1, column=2, padx=5, pady=5)
    newWindow.update()

    colorLabel = Label(newWindow, text=' '*50, bd=2,
                       relief=SUNKEN, background=clockColor)
    colorLabel.bind('<Button-1>', chooseClockColor)
    colorLabel.grid(row=1, column=4, padx=5, pady=5)

    btn = Button(newWindow, text='Submit', font=('Georgia', 17, ITALIC),
                 bg='#a6ffff', activebackground='#6aff6a', command=valuesSelected)
    btn.grid(row=2, column=2, columnspan=2)

    newWindow.mainloop()


def win_closed():
    global doubleClickedOnce
    newWindow.destroy()
    doubleClickedOnce = False


def chooseClockColor(e):
    global clockColor
    hex = colorchooser.askcolor()[1]
    print(hex)
    if hex is None:
        return
    colorLabel.config(background=hex)
    clockColor = hex


def valuesSelected():
    global currFont, clockSize, doubleClickedOnce
    currFont = allFonts.index(sFont.get())

    temp = sizeText.get()
    if temp == '':
        showerror(title='Empty Value',
                  message='Please Enter A Value For Clock Size')
        sizeText.insert(0, clockSize)
        return

    if int(temp) < 5 or int(temp) > 200:
        showerror(title='Invalid Clock Size',
                  message='Please Choose A Size Between 5 to 200')
        sizeText.delete(0, END)
        sizeText.insert(0, clockSize)
        return

    clockSize = str(temp)
    temp = None

    label.config(font=(allFonts[currFont], clockSize),
                 foreground=clockColor)
    newWindow.destroy()
    doubleClickedOnce = False
    saveToPickle()


def saveToPickle():
    cwh = os.getcwd()
    os.chdir('c:/')

    if not os.path.isdir(appName):
        os.mkdir(appName)

    os.chdir(cwh)

    values = [str(clockSize), str(clockColor), str(currFont)]
    with open(pickleFilePath, 'wb') as pf:
        pickle.dump(values, pf)


def retrieveFromPickle():
    global clockSize, clockColor, currFont
    try:
        with open(pickleFilePath, 'rb') as pf:
            values = pickle.load(pf)
        clockSize = values[0]
        clockColor = values[1]
        currFont = int(values[2])
    except:
        saveToPickle()


if __name__ == '__main__':
    # ctypes.windll.user32.ShowWindow(
    #     ctypes.windll.kernel32.GetConsoleWindow(), 0)
    # hide = win32gui.GetForegroundWindow()
    # win32gui.ShowWindow(hide, win32con.SW_HIDE)

    retrieveFromPickle()
    main()
