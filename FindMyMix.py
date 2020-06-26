import bs4, requests, pyperclip
from tkinter import *


# GUI
window=Tk()
window.wm_title('Find My Mix')

# set default global vars
mix = pyperclip.paste()
offSet = 9



def getLatestOKMix():
    res = requests.get('http://vcatsvcg.gen.volvocars.net/qbay/Base/ZoneReports/TopFaults.asp?ZoneID=1&Zone=EOL&ReportType=vinall')
    res.raise_for_status()
    soupOK = bs4.BeautifulSoup(res.text, 'html.parser')
    return soupOK


def getLatestNOKMix():
    res = requests.get('http://vcatsvcg.gen.volvocars.net/qbay/Base/ZoneReports/TopFaults.asp?ZoneID=1&Zone=EOL&ReportType=vinall')
    res.raise_for_status()
    soupNOK = bs4.BeautifulSoup(res.text, 'html.parser')
    return soupNOK


def findMix(text):
    errorMess = 'No cars at EOL this shift.\n'
    mixRegex = re.compile(r'\d{7}')
    extractedMix = mixRegex.findall(text)
    extractedMix.sort(reverse=True)
    try:
        extractedMix[0]
    except IndexError:
        t2.delete("1.0", END)
        t2.insert(END, errorMess)
    if len(extractedMix) != 0:
        return extractedMix[0]


def validateMix():
    errorMess = 'Input mix not numeric!\n'
    try:
        int(mix) + 1
        return True
    except ValueError:
        t2.delete("1.0",END)
        t2.insert(END, errorMess)
        return False


def mixChosen():
    global mix
    mix = e2_value.get()
    if mix == '':
        mix = pyperclip.paste()
        t1.delete("1.0",END)
        t2.delete("1.0",END)
        t1.insert(END,mix)
    else:
        t1.delete("1.0", END)
        t2.delete("1.0", END)
        t1.insert(END, mix)

def getLatestMix():
    reftext = ' is last mix on EOL.'
    failtext = 'no cars'
    mixRawOK = getLatestOKMix()
    mixRawNOK = getLatestNOKMix()
    mixOK = findMix(str(mixRawOK))
    mixNOK = findMix(str(mixRawNOK))
    if mixOK is None:
        mixOK = 0
    elif mixNOK is None:
        mixNOK = 0


    if int(mixOK) <= int(mixNOK):
        mixRef = int(mixNOK)
        t2.insert(END, str(mixRef)+reftext)
    else:
        mixRef = int(mixOK)
        t2.insert(END, str(mixRef) + reftext)
    return mixRef



def calcul(mixRef, ct):
    global offSet
    mixoffset = offSet
    mixStartEOL = mixRef + mixoffset
    offline = '\nCar already past station.'
    on = '\nCar on station.'
    bf = c1_var.get()
    if bf == 1:
        mixStartEOL= mixStartEOL + 100
        mixRef = mixRef + 100

    togo = mixTogo(mixStartEOL, ct)

    if int(mix) < int(mixRef):
        t2.insert(END, offline)
    elif int(mix) > int(mixStartEOL):
        t2.insert(END, togo)
    else:
        t2.insert(END, on)

def mixTogo(mixStartEOL, ct):
    diff = int(mix) - int(mixStartEOL)
    diffSec = diff * ct
    diffHours = diffSec // 3600
    diffMinutes = (diffSec % 3600) / 60
    output = '\n' + str(diff) + ' mixnumbers or approx ' + str(diffHours) + 'h' + str(int(diffMinutes)) + 'm to go'
    return str(output)

def getct():
    ct = e3_value.get()

    if ct == '':
        return 73
    else:
        return int(ct)



def loop(event=None):
    mixChosen()
    validateMix()
    ct = getct()
    print(ct)
    if validateMix():
        mixRef = getLatestMix()
        calcul(mixRef, ct)
    else:
        t2.delete("1.0",END)
        t2.insert(END, 'Enter valid mixnumber!')



e1 = Label(window, text="Mixnummer?")
e1.grid(row=0, column=0)

e2_value = StringVar()
e2 = Entry(window, textvariable=e2_value)
e2.grid(row=0, column=1)

b1 = Button(window, text="Find My Mix", command=loop)
b1.grid(row=0, column=2)
window.bind('<Return>', loop)

c1_var = IntVar()
c1 = Checkbutton(window, text='BrakeFill?', variable= c1_var)
c1.grid(row=3, column=2)

e4 = Label(window, text="Cycletime? (default 73s)")
e4.grid(row=3, column=0)

e3_value = StringVar()
e3 = Entry(window, textvariable=e3_value)
e3.grid(row=3, column=1)

t1 = Text(window, height=1, width=8)
t1.grid(row=1, column=0)

t2 = Text(window, height=3, width=36)
t2.grid(row=1, column=1, columnspan=2)

t1.insert(END, mix)

loop()

window.mainloop()