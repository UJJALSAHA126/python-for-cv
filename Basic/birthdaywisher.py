from typing import cast
import pandas as pd
import datetime
import os
import smtplib
from twilio.rest import Client

# Have To Use Own Email And Password To Send Email
EMAIL_ID = ''
EMAIL_PASSWORD = ''

# To Send SMS To Any Phone Number Use Twilio
account_sid = ''
auth_token = ''
my_Number = ''

# Today's Ocation
ocation = ''


def getDetails():
    global EMAIL_ID
    global EMAIL_PASSWORD
    global account_sid
    global auth_token
    global my_Number
    with open("details.txt") as fp:
        list = fp.read().split('\n')
        EMAIL_ID = list[0].replace('emailId:', '')
        EMAIL_PASSWORD = list[1].replace('password:', '')
        account_sid = list[2].replace('twilioAccountSid:', '')
        auth_token = list[3].replace('twilioAuthToken:', '')
        my_Number = list[4].replace('MyTwilioNumber:', '')


def sendEmail(to, sub, msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL_ID, EMAIL_PASSWORD)
    s.sendmail(from_addr=EMAIL_ID, to_addrs=to, msg=f'Subject: {sub}\n\n{msg}')
    s.quit()


def sendMessageToMobile(to, sub, msg):
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=msg, from_=my_Number, to=to)


def main():
    global ocation
    try:
        df = pd.read_excel("data.xlsx")
    except:
        print("Source File Not Found !!!")
        exit()

    currTime = datetime.datetime.now()
    today = currTime.strftime("%d-%m")
    yearNow = currTime.strftime("%Y")
    # today='25-12'
    if(today == '25-12'):
        ocation = 'Christmas'
    elif (today == '01-01'):
        ocation = 'NewYear'

    writeIntex = []
    for index, item in df.iterrows():
        decideGreeting(today, yearNow, item, index, writeIntex)

    saveCangesToExcelSeet(writeIntex, df)


def decideGreeting(today, yearNow, item, index, writeIntex):
    sub = ''
    wish = ''

    occurance = str(item['Year']).split(',')
    x = f'{yearNow}-{ocation}'
    if(x in occurance):
        return
    
    name = item['Name']

    if (ocation == 'Christmas'):
        sub = 'Christmas Greetings'
        wish = f"Merry Christmas To My Dear {name} :))\n\n\n\t\t\t\t\t\t---- Ujjal"
    elif (ocation == 'NewYear'):
        sub = 'Best Wishes For New Year'
        wish = f"Happy New Year To My Dear  {name} :))\n\n\n\t\t\t\t\t\t---- Ujjal"

    if(len(sub) != 0 or len(wish) != 0):
        greetMembers(item=item, index=index, sub=sub, wish=wish,
                     ocation=ocation, writeIndex=writeIntex, today=today, yearNow=yearNow)

    bday = item['Birthday'].strftime("%d-%m")
    # print(item['Name'], bday, today)

    x = f'{yearNow}-Birthday'
    if (today == bday) and x not in occurance:
        e_body = item['Dialogue']
        relation = item['Relationship']
        sub = f'Happy Birthday To My Dear {relation}'
        wish = e_body

        greetMembers(item=item, index=index, sub=sub, wish=wish,
                     ocation='Birthday', writeIndex=writeIntex, today=today, yearNow=yearNow)


def greetMembers(item, index, sub, wish, ocation, writeIndex: list, today, yearNow):
    if(str(item['Status']) == 'Off'):
        return
    name = item['Name']
    mode = item['Mode']
    e_mail = item['Email']
    p_hone = '+91'+str(item['Mobile'])

    try:
        if(mode == 'Email'):
            sendEmail(e_mail, sub, wish)
            print(f'Email id = {e_mail}\nSub : {sub}\nBody : {wish}')
            # pass
        elif(mode == 'Mobile'):
            # sendMessageToMobile(p_hone, sub, wish)
            print(p_hone)
            pass
    except:
        print('Some Error Occured !')
    else:
        print(f'Greeting Sent To {name} For {ocation}\n')
        writeIndex.append([index, f'{yearNow}-{ocation}'])
        try:
            with open('Sent_Messages_List.txt', 'a') as fp:
                fp.write(
                    f"Greeting For {ocation} Sent To {name} at {datetime.datetime.now()}\n")
        except:
            pass


def saveCangesToExcelSeet(writeIndex, df):
    if len(writeIndex) == 0:
        return
    for i, ocation in writeIndex:
        pre = df.loc[i, 'Year']
        pre = f'{pre},' if(str(pre) != 'nan') else ''
        df.loc[i, 'Year'] = str(pre)+str(ocation)

    convertMobileToStr(df)
    df.to_excel('data.xlsx', index=False)


def convertMobileToStr(df):
    for index, item in df.iterrows():
        df.loc[index, 'Mobile'] = str(df.loc[index, 'Mobile'])


if __name__ == '__main__':
    os.chdir(r'C:\Users\PURNIMA SAHA\Desktop\VS Code\Python\Mini Prjects')
    # os.mkdir('Testing')
    getDetails()
    main()
    # x=input('Hello :')
    # exit()
