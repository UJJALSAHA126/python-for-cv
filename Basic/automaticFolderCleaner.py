import os
import datetime
from tkinter import Button, Tk, filedialog

imgExts = ['.png', '.jpg', '.jpeg']
docExts = ['.doc', '.txt', '.docx', '.pdf', '.pptx']
medExts = ['.mp4', '.mp3', '.m4a', 'mkv', '.3gp']
programExts = ['.c', '.cpp', '.c++', '.java', '.class', '.kt', '.py', '.js']

thisName = 'automaticFolderCleaner.py'

changePath = ''
cancled = False


def chooseFolder():
    global root
    root = Tk()
    root.title('Select Folder')
    root.eval('tk::PlaceWindow . center')
    # root.withdraw()
    root.attributes('-topmost', True)

    button1 = Button(root, text='Done', command=root.destroy)
    button1.pack(anchor='center')

    button2 = Button(root, text='Choose Again', command=getFolder)
    button2.pack(anchor='center')

    button3 = Button(root, text='Cancle', command=cancle)
    button3.pack(anchor='center')

    getFolder()
    root.mainloop()


def cancle():
    global cancled
    cancled = True
    root.destroy()


def getFolder():
    global changePath
    changePath = filedialog.askdirectory()
    return changePath


def main():
    # os.chdir(r'C:\Users\PURNIMA SAHA\Desktop\VS Code\Python\Mini Prjects\CleaningDemo')
    files = os.listdir()
    try:
        files.remove(thisName)
    except:
        pass

    try:
        files.remove('ReadMe.txt')
    except:
        pass

    images = getFilesFromExtentions(files, imgExts)

    docs = getFilesFromExtentions(files, docExts)

    media = getFilesFromExtentions(files, medExts)

    programs = getFilesFromExtentions(files, programExts)

    others = []
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if (ext not in imgExts) and (ext not in docExts) and (ext not in medExts) and os.path.isfile(file):
            others.append(file)

    # print(others)
    moveFilesInFolders(images, 'Image')
    moveFilesInFolders(docs, 'Document')
    moveFilesInFolders(media, 'Media')
    moveFilesInFolders(programs, 'Programming')


def getFilesFromExtentions(files, extenTion):
    allFiles = [file for file in files if os.path.splitext(file)[
        1].lower() in extenTion]

    return allFiles


def moveFilesInFolders(files, folder):
    if len(files) == 0:
        return
    createFolder(folder)

    count = 0
    for file in files:
        try:
            newName = renameFile(file, folder)
            os.replace(file, f'{folder}/{newName}')
        except:
            pass
        else:
            count = count+1

    createReadMeTxt(folder, count)


def renameFile(file, folder):
    if not (os.path.exists(f'{folder}/{file}')):
        return file

    fDetails = os.path.splitext(file)
    fName = fDetails[0]
    fExt = fDetails[1]

    newName = ''
    i = 0

    while True:
        newName = f'{fName}({i}){fExt}'
        if not (os.path.exists(f'{folder}/{newName}')):
            break
        i = i+1

    return newName


def createFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def createReadMeTxt(type, total):
    c_time = datetime.datetime.now().strftime('%d/%m/%Y  %I:%M:%S %p')
    with open('ReadMe.txt', 'a') as fp:
        fp.write(
            f'Total {total} {type} files is/are Moved To {type}; Time = {c_time}\n')


if __name__ == '__main__':
    chooseFolder()
    if cancled:
        exit()

    while changePath == '':
        print('Please Enter A Valid Path !!!')
        chooseFolder()
        if cancled:
            exit()

    os.chdir(changePath)
    main()
