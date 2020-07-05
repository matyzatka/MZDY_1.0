import os
import smtplib
import sqlite3
import sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from tkinter import *
from tkinter import messagebox
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

root = Tk()
filename = PhotoImage(file = "bg.png")
background_label = Label(root, image = filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
root.title("MZDY 1.0")
root.iconbitmap("kalku_icon.ico")
root.geometry("1150x500")
my_menu = Menu(root)
root.config(menu = my_menu)

def clearloginbutton():
    list = root.pack_slaves()
    loginbut = [list[0]]

    for loginbut in list:
        loginbut.destroy()
        break

def login_user():

    while True:
            username = var1
            password = var2
            with sqlite3.connect("databaze_loginy.db") as db:
                cursor = db.cursor()
            find_user = ("SELECT * FROM databaze_loginy WHERE username = ? AND password = ?")
            cursor.execute(find_user, [(username.get()), (password.get())])
            results = cursor.fetchall()
            if results:
                for i in results:
                    messagebox.showinfo("Dobrá zpráva!", "Přihlášení proběhlo úspěšně.")
                loginscreen.destroy()
                clearloginbutton()

                logoutbutton = Button(text="Odhlásit se", width=30, height=3, borderwidth=5,
                                      command=restartCommand).pack(side=TOP, expand=YES)

                Label(root, text = "Přihlášený uživatel: " + username.get()).pack(side = TOP)

                # VYTVOŘENÍ MENU DATABÁZE
                databaze_Menu = Menu(my_menu)
                my_menu.add_cascade(label="Databáze", menu=databaze_Menu)
                databaze_Menu.add_command(label="Vytvořit výplatní pásku", command=vyplatnice)
                databaze_Menu.add_command(label="Vyhledat zaměstnance", command=zamestnanciCommand)
                databaze_Menu.add_command(label="Přidat nového zaměstnance", command=pridatzamestnance)
                databaze_Menu.add_command(label="Zobrazit vše", command=zobrazitvse)
                databaze_Menu.add_command(label="Vymazat vše", command=vymazatVseCommand)
                break
            else:
                messagebox.showwarning("Chyba!", "Přihlášení neúspěšné! Zkuste to znovu.")
                break

def savezamestnanec():
    a = jmeno.get()
    b = prijmeni.get()
    c = email.get()
    d = telefon.get()
    e = zarazeni.get()
    f = zaklad.get()
    if len(a) < 2:
        messagebox.showerror("Chyba!", "Vyplňte prosím všechny údaje.")
    elif len(b) < 2:
        messagebox.showerror("Chyba!", "Vyplňte prosím všechny údaje.")
    elif len(c) < 2:
        messagebox.showerror("Chyba!", "Vyplňte prosím všechny údaje.")
    elif len(d) < 2:
        messagebox.showerror("Chyba!", "Vyplňte prosím všechny údaje.")
    elif len(e) < 2:
        messagebox.showerror("Chyba!", "Vyplňte prosím všechny údaje.")

    else:
        with sqlite3.connect("zamestnanci.db") as db:
            cursor = db.cursor()
            save = """INSERT INTO zamestnanci (jmeno, prijmeni, email, telefon, zarazeni, zaklad) VALUES (?,?,?,?,?,?)"""
            cursor.execute(save, [(a),(b),(c),(d),(e),(f)])
            db.commit()
            messagebox.showinfo("Dobrá zpráva!", "Záznam o zaměstnanci úspěšně vytvořen.")
            zamestnanecscreen.destroy()

def pridatzamestnance():
    global zamestnanecscreen
    global jmeno
    global prijmeni
    global email
    global telefon
    global zarazeni
    global zaklad
    jmeno = StringVar()
    prijmeni = StringVar()
    email = StringVar()
    telefon = StringVar()
    zarazeni = StringVar()
    zaklad = IntVar()
    zamestnanecscreen = Toplevel(root)
    zamestnanecscreen.title("Nový zaměstnanec")
    zamestnanecscreen.geometry("300x500")
    Label(zamestnanecscreen, text="").pack()
    Label(zamestnanecscreen, text="Zadejte údaje o zaměstanci.").pack()
    Label(zamestnanecscreen, text="").pack()
    Label(zamestnanecscreen, text="Jméno: ").pack()
    jmenoentry = Entry(zamestnanecscreen, textvariable=jmeno)
    jmenoentry.pack()  # PACK MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(zamestnanecscreen, text="").pack()
    Label(zamestnanecscreen, text="Příjmení: ").pack()
    prijmenientry = Entry(zamestnanecscreen, textvariable=prijmeni)
    prijmenientry.pack()  # PACK OPĚT MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(zamestnanecscreen, text="").pack()
    Label(zamestnanecscreen, text="Telefon: ").pack()
    telefonentry = Entry(zamestnanecscreen, textvariable=email)
    telefonentry.pack()  # PACK MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(zamestnanecscreen, text="").pack()
    Label(zamestnanecscreen, text="Email: ").pack()
    emailentry = Entry(zamestnanecscreen, textvariable=telefon)
    emailentry.pack()  # PACK OPĚT MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(zamestnanecscreen, text="").pack()
    Label(zamestnanecscreen, text="Zařazení: ").pack()
    zarazenientry = Entry(zamestnanecscreen, textvariable=zarazeni)
    zarazenientry.pack()  # PACK MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(zamestnanecscreen, text="").pack()
    Label(zamestnanecscreen, text="Základ: ").pack()
    zakladentry = Entry(zamestnanecscreen, textvariable=zaklad)
    zakladentry.pack()  # PACK OPĚT MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(zamestnanecscreen, text="").pack()
    Button(zamestnanecscreen, text="Uložit nového zaměstnance", width=30, height=3, command=savezamestnanec).pack()
    Label(zamestnanecscreen, text="").pack()

def prihlasitCommand():
    global loginscreen
    loginscreen = Toplevel(root)
    loginscreen.title("Přihlásit se")
    loginscreen.geometry("300x230")
    username = StringVar()
    password = StringVar()
    global var1
    global var2
    var1 = username
    var2 = password
    Label(loginscreen, text="").pack()
    Label(loginscreen, text="Zadejte své přihlašovací údaje.").pack()
    Label(loginscreen, text="").pack()
    Label(loginscreen, text="Uživatelské jméno: ").pack()
    username_entry = Entry(loginscreen, textvariable=username)
    username_entry.pack()  # PACK MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(loginscreen, text="Heslo: ").pack()
    password_entry = Entry(loginscreen, textvariable=password, show = "*")
    password_entry.pack()  # PACK OPĚT MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(loginscreen, text="").pack()
    Button(loginscreen, text="Přihlásit", width=10, height=2, command = login_user).pack()
    Label(loginscreen, text="").pack()

def save_user():
    found = 0
    while found == 0:
        with sqlite3.connect("databaze_loginy.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM databaze_loginy WHERE username = ?")
            cursor.execute(find_user, [(newusername.get())])
        if  cursor.fetchall():
            messagebox.showwarning("Chyba!", "Uživatelské jméno je již používáno. Vyberte jiné.")
            break
            save_user()
        else:
            found = 1

    password = newpassword.get()
    password1 = newpassword1.get()
    if password != password1:
        messagebox.showwarning("Chyba!", "Zadaná hesla se neshodují. Zkuste to znovu.")
        registrovatCommand()
    else:
        with sqlite3.connect("databaze_loginy.db") as db:
            cursor = db.cursor()
            register_user = """INSERT INTO databaze_loginy (username, password, email) VALUES (?,?,?)"""
            cursor.execute(register_user, [(newusername.get()), (newpassword.get()), (newemail.get())])
            db.commit()
            messagebox.showinfo("Dobrá zpráva!", "Registrace proběhla úspěšně. Nyní se můžete přihlásit.")
            registerscreen.destroy()
            prihlasitCommand()

def registrovatCommand():
    global registerscreen
    registerscreen = Toplevel(root)
    registerscreen.title("Zaregistrovat se")
    registerscreen.geometry("300x300")
    global newusername
    global newpassword
    global newpassword1
    global newemail
    newusername = StringVar()
    newpassword = StringVar()
    newpassword1 = StringVar()
    newemail = StringVar()
    Label(registerscreen, text = "Zadejte nové přihlašovací údaje.").pack()
    Label(registerscreen, text = "").pack()
    Label(registerscreen, text = "Uživatelské jméno: ").pack()
    username_entry = Entry(registerscreen, textvariable = newusername)
    username_entry.pack()   #PACK MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(registerscreen, text="Heslo: ").pack()
    password_entry = Entry(registerscreen, textvariable = newpassword, show = "*")
    password_entry.pack()   #PACK OPĚT MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(registerscreen, text="Heslo znovu: ").pack()
    password1_entry = Entry(registerscreen, textvariable = newpassword1, show="*")
    password1_entry.pack()  # PACK OPĚT MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(registerscreen, text="Zadejte email: ").pack()
    newemailentry = Entry(registerscreen, textvariable=newemail)
    newemailentry.pack()  # PACK OPĚT MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(registerscreen, text = "").pack()
    Button(registerscreen, text = "Zaregistrovat", width = 10, height = 2, command = save_user).pack()
    Label(registerscreen, text="").pack()

def odeslat_heslo():
    with sqlite3.connect("databaze_loginy.db") as db:
        cursor = db.cursor()
        find_user = ("SELECT * FROM databaze_loginy WHERE username = ? AND email = ?")
        cursor.execute(find_user, [(usernameforgot.get()), (email.get())])
        results = str(cursor.fetchall())
        if results != "[]":
            for i in results:
                fromaddr = "mzdy.zapomenuteheslo@seznam.cz"
                toaddr = email.get()
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Zapomenutý login a heslo"
                body = "Vaše přihlašovací údaje ('Login', 'Heslo', 'Email') k programu MZDY 1.0: " + results
                msg.attach(MIMEText(body, 'plain'))
                server = smtplib.SMTP("smtp.seznam.cz")
                server.starttls()
                server.login("mzdy.zapomenuteheslo@seznam.cz", "C4rr4n...")
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()
                messagebox.showinfo("Email odeslán.", "Vaše přihlašovací údaje byly odeslány na zadanou adresu. Nyní se můžete zkusit znovu přihlásit.")
                break
                prihlasitCommand
                forgotScreen.destroy()
        else:
            messagebox.showwarning("Chyba!", "Zadali jste nesprávné uživatelské jméno nebo email.")
            zapomenuteHesloCommand

def zapomenuteHesloCommand():
    global usernameforgot
    global email
    usernameforgot = StringVar()
    email = StringVar()
    global forgotScreen
    forgotScreen = Toplevel(root)
    forgotScreen.title("Zapomenuté heslo?")
    forgotScreen.geometry("300x200")
    Label(forgotScreen, text="Zadejte své uživatelské jméno a email.").pack()
    Label(forgotScreen, text="").pack()
    Label(forgotScreen, text="Uživatelské jméno: ").pack()
    username_entry = Entry(forgotScreen, textvariable= usernameforgot)
    username_entry.pack()  # PACK MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(forgotScreen, text="Email: ").pack()
    email_entry = Entry(forgotScreen, textvariable= email)
    email_entry.pack()  # PACK OPĚT MUSÍ BÝT NA SAMOSTATNÉM ŘÁDKU, JINAK VZNIKÁ CHYBA
    Label(forgotScreen, text="").pack()
    Button(forgotScreen, text="Odeslat zapomenuté heslo", width=30, height=2, command=odeslat_heslo).pack()
    Label(forgotScreen, text="").pack()

def restartCommand():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def quitprogram():
    sys.exit()

def vyplatnice():
    def vytvoritpasku():
        def pdfpaska():

            a = str(jmenoprijmenientry.get())
            b = str(hrubamzdaentry.get())
            c = str(pocethodinentry.get())
            d = str(premieentry.get())
            e = str(prispevekentry.get())
            f = str(superhruba)
            g = str(socialni)
            h = str(zdravotni)
            i = str(socialnidan)
            j = str(zdravotnidan)
            k = str(danzprijmu)
            l = str(slevanadite)
            m = str(cista)
            n = str(exekuceentry.get())
            o = str(stravneentry.get())
            p = str(dobirka)
            filename = "VyplatniPaska.pdf"
            pdf = canvas.Canvas(filename)
            pdf.setTitle("Výplatní páska")
            enc = 'UTF-8'
            pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf', enc))
            pdf.setFont("DejaVuSans", 7,)
            pdf.setFillColorRGB(0, 0, 1)
            ted = datetime.datetime.now()
            datum = str("Měsíc/Rok: " + ted.strftime("%m/%Y"))
            pdf.drawString(70, 800, "Jméno a příjmení: " + a)
            pdf.drawString(320, 800, datum)
            pdf.drawString(70, 750, "Základ: " + b + " Kč")
            pdf.drawString(70, 720, "Počet odpracovaných hodin: " + c + " hodin")
            pdf.drawString(70, 690, "Prémie: " + d + " Kč")
            pdf.drawString(70, 660, "Příspěvek na dopravu: " +e + " Kč")
            pdf.drawString(70, 630, "Superhrubá mzda: " +f+ " Kč")
            pdf.drawString(70, 600, "Odvody zaměstnavatele - sociální pojištění: " + g + " Kč")
            pdf.drawString(70, 570, "Odvody zaměstnavatele - zdravotní pojištění: " + h + " Kč")
            pdf.drawString(320, 750, "Odvody zaměstnance - sociální pojištění: " + i + " Kč")
            pdf.drawString(320, 720, "Odvody zaměstnance - zdravotní pojištění: " + j + " Kč")
            pdf.drawString(320, 690, "Daň z příjmu: " + k + " Kč")
            pdf.drawString(320, 660, "Sleva na dítě: " + l + " Kč")
            pdf.drawString(320, 630, "Čistá mzda: " + m + " Kč")
            pdf.drawString(320, 600, "Srážky za exekuci: " + n + " Kč")
            pdf.drawString(320, 570, "Srážky za stravné: " + o + " Kč")
            pdf.drawString(320, 540, "Dobírka na účet: " + p + " Kč")
            pdf.save()
            os.startfile("VyplatniPaska.pdf")

        if len(jmenoprijmenientry.get()) < 1:
            messagebox.showwarning("Chyba!", "Zadejte jméno zaměstnance.")
            pass
        else:
            while pocetdetientry.get() == 0:
                slevanadite = 0
                break
            while pocetdetientry.get() == 1:
                slevanadite = 1267
                break
            while pocetdetientry.get() == 2:
                slevanadite = 1617
                break
            while pocetdetientry.get() >= 3:
                slevanadite = 2017
                break
            hodinovka = IntVar()
            hodinovka = hrubamzdaentry.get() / 150
            hruba = IntVar()
            hruba = (hodinovka * pocethodinentry.get()) + premieentry.get() + prispevekentry.get()
            zdravotni = int(hrubamzdaentry.get())*0.09
            socialni = int(hrubamzdaentry.get())*0.248
            superhruba = int(hruba + zdravotni + socialni)
            danzprijmu = int(superhruba*0.15)
            socialnidan = int(hruba*0.065)
            zdravotnidan = int(hruba*0.045)
            cista = int(hruba - danzprijmu - socialnidan - zdravotnidan + prispevekentry.get() + premieentry.get() + slevanadite)
            dobirka = int(cista - exekuceentry.get() - stravneentry.get())
            global vypocetscreen
            vypocetscreen = Toplevel(root)
            vypocetscreen.title("Výplatní páska")
            Label(vypocetscreen, text = "Výplatní páska", font = "bold").pack(side=TOP)
            Label(vypocetscreen, text="").pack(side=LEFT)
            Label(vypocetscreen, text="Jméno a příjmení: " + str(jmenoprijmenientry.get())).pack(side=TOP)
            Label(vypocetscreen, text="Hrubá mzda - základ: " + str(hrubamzdaentry.get()) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Odpracované hodiny: " + str(pocethodinentry.get())).pack(side=TOP)
            Label(vypocetscreen, text="Prémie: " + str(premieentry.get()) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Příspěvek na dopravu: " + str(prispevekentry.get()) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Superhrubá mzda: " + str(superhruba) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Odvody zaměstnavatele: Sociální - " + str(socialni) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Odvody zaměstnavatele: Zdravotní - " + str(zdravotni) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Odvody zaměstnance: Sociální - " + str(socialnidan) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Odvody zaměstnance: Zdravotní - " + str(zdravotnidan) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Odvody zaměstnance: Daň z příjmu - " + str(danzprijmu) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Sleva na dítě: " + str(slevanadite) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Čistá mzda: " + str(cista) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Exekuce: " + str(exekuceentry.get()) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Stravné: " + str(stravneentry.get()) + ",-").pack(side=TOP)
            Label(vypocetscreen, text="Dobírka na účet: " + str(dobirka) + ",-").pack(side=TOP)
            Button(vypocetscreen, text = "Vytvořit PDF soubor", width = 30, height = 4, command = pdfpaska).pack(side=TOP)

    global vypscreen
    jmenoprijmenientry = StringVar()
    hrubamzdaentry = IntVar()
    pocethodinentry = IntVar()
    premieentry = IntVar()
    prispevekentry = IntVar()
    pocetdetientry = IntVar()
    exekuceentry = IntVar()
    stravneentry = IntVar()
    vypscreen = Toplevel(root)
    vypscreen.geometry("500x700")
    vypscreen.title("Vytvořit výplatní pásku")
    Label(vypscreen, text="").pack()
    Label(vypscreen, text="Zadejte informace pro vytvoření výplatní pásky:", font="bold").pack()
    Label(vypscreen, text="Potřebné údaje získáte od mistrů a nadřízených zaměstnance.").pack()
    Label(vypscreen, text=" ").pack()
    Label(vypscreen, text="Jméno a příjmení").pack()
    Entry(vypscreen, textvariable=jmenoprijmenientry).pack()
    Label(vypscreen, text=" ").pack()
    Label(vypscreen, text="Hrubá mzda - základ").pack()
    Entry(vypscreen, textvariable=hrubamzdaentry).pack()
    Label(vypscreen, text=" ").pack()
    Label(vypscreen, text="Počet odpracovaných hodin").pack()
    Entry(vypscreen, textvariable=pocethodinentry).pack()
    Label(vypscreen, text=" ").pack()
    Label(vypscreen, text="Prémie").pack()
    Entry(vypscreen, textvariable=premieentry).pack()
    Label(vypscreen, text=" ").pack()
    Label(vypscreen, text="Příspěvek na dopravu").pack()
    Entry(vypscreen, textvariable=prispevekentry).pack()
    Label(vypscreen, text=" ").pack()
    Label(vypscreen, text="Počet vyživovaných dětí").pack()
    Entry(vypscreen, textvariable=pocetdetientry).pack()
    Label(vypscreen, text=" ").pack()
    Label(vypscreen, text="Exekuce").pack()
    Entry(vypscreen, textvariable=exekuceentry).pack()
    Label(vypscreen, text=" ").pack()
    Label(vypscreen, text="Srážky za stravné").pack()
    Entry(vypscreen, textvariable=stravneentry).pack()
    Label(vypscreen, text=" ").pack()
    Button(vypscreen, text="Vytvořit pásku", width = "20", height = "5", command=vytvoritpasku).pack()

def najitzamestnance():
    global newscreen

    def smazatzamestnance():
        ok = messagebox.askokcancel("Vymazat?", "Určitě chcete zaměstnance s tímto jménem vymazat?")
        if ok == True:
            with sqlite3.connect("zamestnanci.db") as db:
                cursor = db.cursor()
                deleteuser = ("DELETE FROM zamestnanci WHERE jmeno = ?")
                cursor.execute(deleteuser, [(userfind.get())])
                db.commit()
                messagebox.showinfo("Oznámení", "Zaměstnanec byl vymazán.")

                newscreen.destroy()
        elif ok == False:
            pass

    if check1.get() == 1:
        if check2.get() or check3.get() or check4.get() or check5.get() or check6.get() == 1:
            messagebox.showerror("Chyba!", "Zvolte pouze 1 parametr!")

        else:
            with sqlite3.connect("zamestnanci.db") as db:
                cursor = db.cursor()
                finduser = ("SELECT * FROM zamestnanci WHERE jmeno = ?")
                cursor.execute(finduser, [(userfind.get())])
                results = cursor.fetchone()
                if results:
                    newscreen = Toplevel(root)
                    newscreen.title("Zaměstnanci")
                    newscreen.geometry("600x300")
                    Label(newscreen, text = "Výsledek vyhledávání", font = "bold").pack()
                    Label(newscreen, text = "").pack()


                    for i in results:
                        Label(newscreen, text = "\n".join(map(str, results))).pack()
                        Label(newscreen, text="").pack()


                        Button(newscreen, text="Smazat zaměstnance", command=smazatzamestnance).pack()
                        Button(newscreen, text="Nové hledání", command=zamestnanciCommand).pack()
                        break
                else:
                    messagebox.showwarning("Chyba!", "Zaměstnanec nenalezen!")



    if check2.get() == 1:
        def smazatzamestnance():
            ok = messagebox.askokcancel("Vymazat?", "Určitě chcete zaměstnance s tímto příjmením vymazat?")
            if ok == True:
                with sqlite3.connect("zamestnanci.db") as db:
                    cursor = db.cursor()
                    deleteuser = ("DELETE FROM zamestnanci WHERE prijmeni = ?")
                    cursor.execute(deleteuser, [(userfind.get())])
                    db.commit()
                    messagebox.showinfo("Oznámení", "Zaměstnanec byl vymazán.")

                    newscreen.destroy()
            elif ok == False:
                pass

        if check1.get() or check3.get() or check4.get() or check5.get() or check6.get() == 1:
            messagebox.showerror("Chyba!", "Zvolte pouze 1 parametr!")

        else:
            with sqlite3.connect("zamestnanci.db") as db:
                cursor = db.cursor()
                finduser = ("SELECT * FROM zamestnanci WHERE prijmeni = ?")
                cursor.execute(finduser, [(userfind.get())])
                results = cursor.fetchone()
                if results:
                    newscreen = Toplevel(root)
                    newscreen.title("Zaměstnanci")
                    newscreen.geometry("600x300")
                    Label(newscreen, text="Výsledek vyhledávání", font = "bold").pack()
                    Label(newscreen, text="").pack()


                    for i in results:
                        Label(newscreen, text="\n".join(map(str, results))).pack()
                        Label(newscreen, text="").pack()


                        Button(newscreen, text="Smazat zaměstnance", command=smazatzamestnance).pack()
                        Button(newscreen, text="Nové hledání", command=zamestnanciCommand).pack()
                        break
                else:
                    messagebox.showwarning("Chyba!", "Zaměstnanec nenalezen!")


    if check3.get() == 1:
        def smazatzamestnance():
            ok = messagebox.askokcancel("Vymazat?", "Určitě chcete zaměstnance s tímto emailem vymazat?")
            if ok == True:
                with sqlite3.connect("zamestnanci.db") as db:
                    cursor = db.cursor()
                    deleteuser = ("DELETE FROM zamestnanci WHERE email = ?")
                    cursor.execute(deleteuser, [(userfind.get())])
                    db.commit()
                    messagebox.showinfo("Oznámení", "Zaměstnanec byl vymazán.")

                    newscreen.destroy()
            elif ok == False:
                pass

        if check1.get() or check2.get() or check4.get() or check5.get() or check6.get() == 1:
            messagebox.showerror("Chyba!", "Zvolte pouze 1 parametr!")

        else:
            with sqlite3.connect("zamestnanci.db") as db:
                cursor = db.cursor()
                finduser = ("SELECT * FROM zamestnanci WHERE email = ?")
                cursor.execute(finduser, [(userfind.get())])
                results = cursor.fetchone()
                if results:
                    newscreen = Toplevel(root)
                    newscreen.title("Zaměstnanci")
                    newscreen.geometry("600x300")
                    Label(newscreen, text="Výsledek vyhledávání", font = "bold").pack()
                    Label(newscreen, text="").pack()

                    for i in results:
                        Label(newscreen, text="\n".join(map(str, results))).pack()
                        Label(newscreen, text="").pack()


                        Button(newscreen, text="Smazat zaměstnance", command=smazatzamestnance).pack()
                        Button(newscreen, text="Nové hledání", command=zamestnanciCommand).pack()
                        break
                else:
                    messagebox.showwarning("Chyba!", "Zaměstnanec nenalezen!")


    if check4.get() == 1:
        def smazatzamestnance():
            ok = messagebox.askokcancel("Vymazat?", "Určitě chcete zaměstnance s tímto telefonem vymazat?")
            if ok == True:
                with sqlite3.connect("zamestnanci.db") as db:
                    cursor = db.cursor()
                    deleteuser = ("DELETE FROM zamestnanci WHERE telefon = ?")
                    cursor.execute(deleteuser, [(userfind.get())])
                    db.commit()
                    messagebox.showinfo("Oznámení", "Zaměstnanec byl vymazán.")

                    newscreen.destroy()
            elif ok == False:
                pass

        if check2.get() or check3.get() or check1.get() or check5.get() or check6.get() == 1:
            messagebox.showerror("Chyba!", "Zvolte pouze 1 parametr!")

        else:
            with sqlite3.connect("zamestnanci.db") as db:
                cursor = db.cursor()
                finduser = ("SELECT * FROM zamestnanci WHERE telefon = ?")
                cursor.execute(finduser, [(userfind.get())])
                results = cursor.fetchone()
                if results:
                    newscreen = Toplevel(root)
                    newscreen.title("Zaměstnanci")
                    newscreen.geometry("600x300")
                    Label(newscreen, text="Výsledek vyhledávání", font = "bold").pack()
                    Label(newscreen, text="").pack()

                    for i in results:
                        Label(newscreen, text="\n".join(map(str, results))).pack()
                        Label(newscreen, text="").pack()


                        Button(newscreen, text="Smazat zaměstnance", command=smazatzamestnance).pack()
                        Button(newscreen, text="Nové hledání", command=zamestnanciCommand).pack()
                        break
                else:
                        messagebox.showwarning("Chyba!", "Zaměstnanec nenalezen!")


    if check5.get() == 1:
        def smazatzamestnance():
            ok = messagebox.askokcancel("Vymazat?", "Určitě chcete zaměstnance s tímto zařazením vymazat?")
            if ok == True:
                with sqlite3.connect("zamestnanci.db") as db:
                    cursor = db.cursor()
                    deleteuser = ("DELETE FROM zamestnanci WHERE zarazeni = ?")
                    cursor.execute(deleteuser, [(userfind.get())])
                    db.commit()
                    messagebox.showinfo("Oznámení", "Zaměstnanec byl vymazán.")
                    newscreen.destroy()
            elif ok == False:
                    pass

        if check2.get() or check3.get() or check4.get() or check1.get() or check6.get() == 1:
            messagebox.showerror("Chyba!", "Zvolte pouze 1 parametr!")

        else:
            with sqlite3.connect("zamestnanci.db") as db:
                cursor = db.cursor()
                finduser = ("SELECT * FROM zamestnanci WHERE zarazeni = ?")
                cursor.execute(finduser, [(userfind.get())])
                results = cursor.fetchone()
                if results:
                    newscreen = Toplevel(root)
                    newscreen.title("Zaměstnanci")
                    newscreen.geometry("600x300")
                    Label(newscreen, text="Výsledek vyhledávání", font = "bold").pack()
                    Label(newscreen, text="").pack()

                    for i in results:
                        Label(newscreen, text="\n".join(map(str, results))).pack()
                        Label(newscreen, text="").pack()


                        Button(newscreen, text="Smazat zaměstnance", command=smazatzamestnance).pack()
                        Button(newscreen, text="Nové hledání", command=zamestnanciCommand).pack()
                        break
                else:
                    messagebox.showwarning("Chyba!", "Zaměstnanec nenalezen!")


    if check6.get() == 1:
        def smazatzamestnance():
            ok = messagebox.askokcancel("Vymazat?", "Určitě chcete zaměstnance s tímto základem vymazat?")
            if ok == True:
                with sqlite3.connect("zamestnanci.db") as db:
                    cursor = db.cursor()
                    deleteuser = ("DELETE FROM zamestnanci WHERE zaklad = ?")
                    cursor.execute(deleteuser, [(userfind.get())])
                    db.commit()
                    messagebox.showinfo("Oznámení", "Zaměstnanec byl vymazán.")

                    newscreen.destroy()
            elif ok == False:
                pass

        if check2.get() or check3.get() or check4.get() or check5.get() or check1.get() == 1:
            messagebox.showerror("Chyba!", "Zvolte pouze 1 parametr!")


        else:
            with sqlite3.connect("zamestnanci.db") as db:
                cursor = db.cursor()
                finduser = ("SELECT * FROM zamestnanci WHERE zaklad = ?")
                cursor.execute(finduser, [(userfind.get())])
                results = cursor.fetchone()
                if results:

                    newscreen = Toplevel(root)
                    newscreen.title("Zaměstnanci")
                    newscreen.geometry("600x300")
                    Label(newscreen, text="Výsledek vyhledávání", font = "bold").pack()
                    Label(newscreen, text="").pack()


                    for i in results:
                        Label(newscreen, text="\n".join(map(str, results))).pack()
                        Label(newscreen, text="").pack()


                        Button(newscreen, text = "Smazat zaměstnance", command = smazatzamestnance).pack()
                        Button(newscreen, text = "Nové hledání", command = zamestnanciCommand).pack()
                        break

                else:
                    messagebox.showwarning("Chyba!", "Zaměstnanec nenalezen!")

def zamestnanciCommand():
    global zamestnanciScreen
    zamestnanciScreen = Toplevel(root)
    zamestnanciScreen.title("Vyhledávač zaměstaneckých údajů")
    zamestnanciScreen.geometry("400x400")
    Label(zamestnanciScreen, text="").pack()
    Label(zamestnanciScreen, text = "Vyberte 1 parametr hledání.").pack()
    Label(zamestnanciScreen, text="").pack()
    global check1
    global check2
    global check3
    global check4
    global check5
    global check6
    check1 = IntVar()
    check2 = IntVar()
    check3 = IntVar()
    check4 = IntVar()
    check5 = IntVar()
    check6 = IntVar()
    Checkbutton(zamestnanciScreen, text="Jméno", variable=check1, onvalue = 1, offvalue = 0).pack()
    Checkbutton(zamestnanciScreen, text="Příjmení", variable=check2, onvalue = 1, offvalue = 0).pack()
    Checkbutton(zamestnanciScreen, text="Email", variable=check3, onvalue = 1, offvalue = 0).pack()
    Checkbutton(zamestnanciScreen, text="Telefon", variable=check4, onvalue = 1, offvalue = 0).pack()
    Checkbutton(zamestnanciScreen, text="Zařazení", variable=check5, onvalue = 1, offvalue = 0).pack()
    Checkbutton(zamestnanciScreen, text="Základ", variable=check6, onvalue = 1, offvalue = 0).pack()
    Label(zamestnanciScreen, text="").pack()
    Label(zamestnanciScreen, text="Zadejte hledaný výraz:").pack()
    global userfind
    userfind = StringVar()
    userfindEntry = Entry(zamestnanciScreen, textvariable=userfind, width=25, borderwidth=3)
    userfindEntry.pack()
    Label(zamestnanciScreen, text="").pack()
    Button(zamestnanciScreen, text = "Vyhledat", command = najitzamestnance).pack()

def ulozeneMzdyCommand():
    pass

def zobrazitvse():
    global zobrazitvsescreen
    zobrazitvsescreen = Toplevel(root)
    with sqlite3.connect("zamestnanci.db") as db:
        cursor = db.cursor()
        showuser = ("SELECT * FROM zamestnanci")
        cursor.execute(showuser)
        vse = cursor.fetchall()
    for i in vse:
        Label(zobrazitvsescreen, text="").pack()
        Label(zobrazitvsescreen, text="\n\n".join(map(str, vse))).pack()
        break

def vymazatVseCommand():
    ok = messagebox.askokcancel("Vymazat?", "Určitě chcete všechny záznamy vymazat?")
    if ok == True:
        with sqlite3.connect("zamestnanci.db") as db:
            cursor = db.cursor()
            deleteuser = ("DELETE FROM zamestnanci")
            cursor.execute(deleteuser)
            db.commit()
            messagebox.showinfo("Oznámení", "Záznamy vymazány.")

            newscreen.destroy()
    elif ok == False:
        pass

def oAplikaciCommand():
    xscreen = Toplevel(root)
    xscreen.title("O aplikaci")
    xscreen.geometry("800x200")
    Label(xscreen, text='').pack()
    Label(xscreen, text="O Aplikaci", font = "bold").pack()
    Label(xscreen, text="").pack()
    Label(xscreen, text = "Aplikace vznikla jako napodobenina profesionálních programů pro práci s databázemi zaměstnanců, početními operacemi,\n základním uživatelským prostředím a jedná se o první software, který vznikl při samostudiu jazyka Python 3.8.\n\n Děkuji proto za tolerování mnoha nedostatků a jednoduchosti programu jako takového. Bylo ale velmi vyčerpávající řešit některé\nprobémy, které při každé příležitosti komplikovaly postupný vývoj a několikrát dokonce úplně znemožnily realizaci původního plánu.\n\nOdhadem zabral vývoj cca 50 hodin čistého času a okolo 1 kg kávy. Děkuji své přítelkyni Kristý, bráchovi Ivovi a mámě Jiřince za podporu.\n\n 27.6. 2020 \nŽádná práva nevyhrazena.").pack()

def jakPouzivatAplikaciCommand():
    helpScreen = Toplevel(root)
    helpScreen.title("Jak používat aplikaci")
    helpScreen.geometry("1000x350")
    Label(helpScreen, text = "").pack()
    Label(helpScreen, text ="Nápověda", font = "bold").pack()
    Label(helpScreen, text = "1) Pokud nemáte přihlašovací účet, můžete si jej vytvořit klepnutím na tlačíto Zaregistrovat se."
                             "\n2) Poté zadejte potřebné údaje. Váš účet bude vytvořen."
                             "\n3) Pokud již účet máte, kliknutím na tlačítko Přihlásit se tak můžete učinit. Umožní vám to přístup do databáze zaměstnanců a pracovat s ní."
                             "\n4) Pokud jste zapomněli své heslo, můžete si ho nechat zaslat na email pomocí tlačítka Zapomenuté heslo."
                             "\n\nPráce s databází zaměstnanců:"
                             "\n1) Vytvořit výplatní pásku: \nZadejte požadované údaje a po výpočtu máte možnost vytvořit pásku ve formátu PDF, kterou doporučujeme uložit na vámi vybrané místo, jinak se automaticky uloží do složky programu."
                             "\n2) Vyhledat zaměstnance: Vyberte 1 parametr a zadejte hledanou hodnotu. Vyhledávat můžete mnoha způsoby.\nZobrazen bude pouze 1 výsledek. Pokud to není ten, který hledáte, zkuste změnit zadání."
                             "\nMenu vyhledávače vám dovolí:"
                             "\nVymazat zaměstnance\nZačít hledat znovu"
                             "\n3) Přidat nového zaměstnance: Je třeba vyplnit všechny údaje a políčko Základ vyplnit číslenou hodnotou."
                             "\n4) Zobrazit vše: Vypíše všechny zaměstnanecké záznamy jeden pod druhým v databázovém formátu."
                             "\n5) Vymazat vše: Vymaže všechny záznamy o zaměstnancích.  " ).pack()

program_Menu = Menu(my_menu)
my_menu.add_cascade(label = "Program", menu = program_Menu)
program_Menu.add_command(label = "Restartovat", command = restartCommand)
program_Menu.add_separator()
program_Menu.add_command(label = "Ukončit", command = quitprogram)

napoveda_Menu = Menu(my_menu)
my_menu.add_cascade(label = "Nápověda", menu = napoveda_Menu)
napoveda_Menu.add_command(label = "O aplikaci", command = oAplikaciCommand)
napoveda_Menu.add_command(label = "Jak používat aplikaci", command = jakPouzivatAplikaciCommand)

loginbutton = Button(text = "Přihlásit se", width = 30, height = 3, borderwidth = 5, command = prihlasitCommand).pack(side=TOP, expand=YES)
registerbutton = Button(text = "Zaregistrovat se", width = 30, height = 3, borderwidth = 5, command = registrovatCommand).pack(side=TOP, expand=YES)
forgetbutton = Button(text = "Zapomenuté heslo?", width = 30, height = 3, borderwidth = 5, command = zapomenuteHesloCommand).pack(side=TOP, expand=YES)

root.mainloop()