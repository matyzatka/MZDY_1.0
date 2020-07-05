import sqlite3

conn = sqlite3.connect('zamestnanci.db')

c = conn.cursor()

#c.execute("""CREATE TABLE Zamestnanci (
#            jmeno text,
#            prijmeni text,
#            email text,
#            telefon text,
#            zarazeni text,
#            zaklad integer
#            )""")

"""
c.execute("INSERT INTO zamestnanci VALUES ('Matouš', 'Zátka', 'matous.zatka@seznam.cz', '777322556', 'SW Developer', 95000)")
c.execute("INSERT INTO zamestnanci VALUES ('Ivo', 'Zátka', 'ivo.zatt@seznam.cz', '775799000', 'Marketing', 67000)")
c.execute("INSERT INTO zamestnanci VALUES ('Jiřina', 'Zátková', 'jirina.zatkova@seznam.cz', '778990876', '', 42400)")
c.execute("INSERT INTO zamestnanci VALUES ('Roman', 'Eliáš', 'roman.elias@gmail.com', '777302323', 'Údržba', 48800)")
c.execute("INSERT INTO zamestnanci VALUES ('Jiří', 'Tajč', 'jirtajc@seznam.cz', '737022300', 'Nákupčí', 52800)")
c.execute("INSERT INTO zamestnanci VALUES ('Josef', 'Viták', 'choseantonio@seznam.cz', '607624595', 'Údržba', 48800)")
c.execute("INSERT INTO zamestnanci VALUES ('Božena', 'Zátková', 'bozenazatokovic@seznam.cz', '607212990', 'Uklízečka', 21200)")
c.execute("INSERT INTO zamestnanci VALUES ('Kristýna', 'Kosková', 'kikinka.koskova@gmail.com', '778023727', 'Dozorčí', 46000)")
c.execute("INSERT INTO zamestnanci VALUES ('Jaroslav', 'Kosek', 'jardakosek@seznam.cz', '602182129', 'Zásobování', 33000)")
c.execute("INSERT INTO zamestnanci VALUES ('Lukáš', 'Kosek', 'lucaskosec@seznam.cz', '777338856', 'Prodejce', 35200)")
c.execute("INSERT INTO zamestnanci VALUES ('Kristýna', 'Novotná', 'tyna.novotna@seznam.cz', '732991020', 'Zdravotnice', 39600)")
c.execute("INSERT INTO zamestnanci VALUES ('Monika', 'Kosková', 'monikoskova@seznam.cz', '721332346', 'Administrativa', 42400)")
c.execute("INSERT INTO zamestnanci VALUES ('Dalibor', 'Bartoš', 'dalibortos@seznam.cz', '777932221', 'Údržba', 48800)")
"""


c.execute("SELECT * FROM Zamestnanci")
conn.commit()
print(c.fetchall())

#conn.close()



