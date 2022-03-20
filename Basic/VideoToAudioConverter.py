import os
from threading import Thread
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from typing import List
import moviepy.editor

# videosFolder = r"G:\7U Video\Songs Video\HINDI SONGS"
videoExts = ['.mp4', '.mkv', '.3gp']
folderPath = ''
converTing = True

allVideos = []
selectedVid = []
wWidth, wHeight = 1000, 600
fWidth, fHeight = 400, 450


def getFilesFromExtentions(files, extenTion):
    allFiles = [file for file in files
                if str(os.path.splitext(file)[1]).lower() in extenTion]

    return allFiles


def getSelectedVideos():
    try:
        sItem = listBox.curselection()
        selectedVideos = [v for i, v in enumerate(allVideos) if i in sItem]
        return selectedVideos
    except:
        return None


def convertToAudio(file: str):
    try:
        print('Start')
        videoEngine = moviepy.editor.VideoFileClip(file)
        audioEngine = videoEngine.audio
        audioName = str(file)
        audioName = audioName[:audioName.rindex('.')]
        if not os.path.isdir('7U Music'):
            os.mkdir('7U Music')
        audioEngine.write_audiofile(f"7U Music/{audioName}.mp3")
        return True
    except:
        return False


def backPressed():
    global folderPath
    try:
        fr.destroy()
        fr1.destroy()
        folderPath = ''
        allVideos.clear()
        addingChooseFolder()
    except:
        pass


def nextPressed():
    global selectedVid
    selectedVid = getSelectedVideos()
    if selectedVid and len(selectedVid) > 0:
        # x=messagebox.showinfo(title="Total Files Selected",
        #                     message=f'Total Vides To Be Converted = {len(selectedVid)}')
        ans = messagebox.askyesno('Total Files Selected',
                                  f'Total Vides To Be Converted = {len(selectedVid)}')
        ans = bool(ans)
        if ans:
            # print('Yes')
            continueProcessing()
        else:
            pass
            # print('No')
    else:
        messagebox.showerror('Items Not Selected',
                             'Please Select Some Items To Proceed')


def startConverting():
    global selectedVid
    count = 0
    # allVideos=allVideos[:5]
    for vid in selectedVid:
        if converTing:
            success = convertToAudio(vid)
            if success:
                count += 1
                print('End')
                try:
                    counterLabel.config(
                        text=f'{count}/{len(selectedVid)} Converted')
                    pgBar.config(value=count/len(selectedVid)*100)
                except:
                    break
                # pgBar.update_idletasks()
                # counterLabel.update_idletasks()
            else:
                print('Failed')
        else:
            break
    else:
        cancleBtn['text'] = 'Done'

    print('Finished')


def startThread():
    global t1
    t1 = Thread(target=startConverting)
    t1.start()
    # startConverting()


def continueProcessing():
    global counterLabel, pgBar, cancleBtn
    newRoot = Toplevel()

    newRoot.title('Converting !!')
    newRoot.geometry(f'300x100')
    newRoot.resizable(False, False)

    pgBar = ttk.Progressbar(newRoot, orient=HORIZONTAL, maximum=100, length=250,
                            mode='determinate', value=0)
    counterLabel = Label(newRoot, text=f'0/{len(selectedVid)} Converted',
                         font=('Algerian', 13),)

    counterLabel.pack(padx=5, pady=5)
    pgBar.pack(pady=5, padx=10)

    cancleBtn = Button(newRoot, text='Cancle', font=('Segoe UI Black', 13),
                       command=lambda: newRoot.destroy())
    cancleBtn.pack(pady=5)

    newRoot.after(100, startThread)
    newRoot.mainloop()


def addingChooseFolder():
    global chooseBtn
    chooseBtn = Button(root, text='Choose A Folder Containing Videos', command=chooseFolder,
                       font=('comic san', 14))
    chooseBtn.place(relx=0.5, rely=0.5, anchor=CENTER)


def selectAll():
    listBox.selection_set(0, END)


def deSelectAll():
    listBox.selection_clear(0, END)


def allVideosFound(videos: List):
    global listBox, fr, btnBack, btnNext, fr1
    chooseBtn.destroy()

    fr = Frame(root, relief=RAISED)
    fr.pack(padx=10, pady=10, expand=True, fill=BOTH)

    fr1 = Frame(root, bg='red', width=wWidth, height=50)
    fr1.pack(padx=10, pady=5, expand=True, fill=X, anchor='s')
    # fr1.place(relx=0.1, rely=1,anchor=CENTER)
    bWidth = 10

    btnBack = Button(fr1, width=bWidth, text='Back', font=('comic-san', 16),
                     relief=SUNKEN, command=backPressed)

    sAll = Button(fr1, width=bWidth, text='Select All', font=('comic-san', 16),
                  relief=SUNKEN, command=selectAll)

    disAll = Button(fr1, width=bWidth, text='DeSelect All', font=('comic-san', 16),
                    relief=SUNKEN, command=deSelectAll)

    btnNext = Button(fr1, width=bWidth, text='Next', font=('comic-san', 16),
                     relief=SUNKEN, command=nextPressed)

    rY = 0.3
    btnBack.place(relx=0.2, rely=rY, anchor=CENTER)
    sAll.place(relx=0.4, rely=rY, anchor=CENTER)
    disAll.place(relx=0.6, rely=rY, anchor=CENTER)
    btnNext.place(relx=0.8, rely=rY, anchor=CENTER)
    # btnBack.grid(row=0,column=0,padx=30,sticky='w')
    # sAll.grid(row=0,column=2,padx=30,sticky='w')
    # disAll.grid(row=0,column=3,padx=30,sticky='e')
    # btnNext.grid(row=0,column=1,padx=30,sticky='e')

    sBar = Scrollbar(fr)
    sBar.pack(side=RIGHT, fill=Y)

    bBar = Scrollbar(fr, orient=HORIZONTAL)
    bBar.pack(side=BOTTOM, fill=X)

    listBox = Listbox(fr, height=20, width=53, activestyle='none',
                      font=('Lucida Sans Unicode', 13), selectmode=MULTIPLE, relief=SUNKEN)
    listBox.pack(fill=BOTH, expand=True)

    for i, vid in enumerate(videos):
        listBox.insert(i, f'  {vid}')

    # listBox.selection_set(0, i)

    # Setting Up ScrollBars
    sBar.config(command=listBox.yview)
    listBox.config(yscrollcommand=sBar.set)

    bBar.config(command=listBox.xview)
    listBox.config(xscrollcommand=bBar.set)


def pathFound(path):
    global allVideos
    allFiles = os.listdir(path)
    if allFiles and len(allFiles):
        allVideos = getFilesFromExtentions(allFiles, videoExts)
        if allVideos and len(allVideos):
            allVideosFound(allVideos)
        else:
            messagebox.showerror(
                'Missing Videos',
                '''No Videos Found In This Folder !!!\nExtes Supported {}'''.format(str(videoExts)))
    else:
        messagebox.showerror(
            'Missing Files', 'No Files Found In This Folder !!!')


def chooseFolder():
    global folderPath
    path = filedialog.askdirectory()
    if path:
        # print(path)
        folderPath = path
        os.chdir(path)
        pathFound(path)


def createStartingWindow():
    global root
    root = Tk()
    root.title('7U Audio Converter')
    root.geometry(f'{wWidth}x{wHeight}')
    root.minsize(width=650, height=wHeight)
    # root.resizable(False, False)
    root.config(bg='red')

    addingChooseFolder()

    return root


def main():
    global root
    os.system('cls')
    root = createStartingWindow()

    root.mainloop()


if __name__ == '__main__':
    main()
