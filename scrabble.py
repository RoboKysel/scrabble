import tkinter, random

class Pismeno:
    
    def __init__(self, pismeno, hodnota):
        self.pismeno = pismeno
        self.hodnota = hodnota

    def vykresli(self, g, x, y):
        g.create_rectangle(x, y, x+Program.ROZMER_POLICKA, y+Program.ROZMER_POLICKA)
        g.create_text(x+Program.ROZMER_POLICKA/2, y+Program.ROZMER_POLICKA/2, text=self.pismeno)

    def __repr__(self):
        return str((self.pismeno, self.hodnota))


class Policko:
    
    def __init__(self, farba, nasobok_slova=1, nasobok_pismena=1):
        self.farba = farba
        self.nasobok_slova = nasobok_slova
        self.nasobok_pismena = nasobok_pismena

    def vykresli(self, g, x, y):
        g.create_rectangle(x, y, x+Program.ROZMER_POLICKA, y+Program.ROZMER_POLICKA, fill=self.farba)
    

class Vrecko:
    POLOMER_VRECKA = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sada_pismen = None

    def nacitaj_sadu(self, nazov_suboru='sada.txt'):
        self.sada_pismen = []
        with open(nazov_suboru, 'r') as subor:
            for riadok in subor:
                if not riadok.strip():
                    continue
                pismenko, hodnota, pocet = riadok.strip().split()
                for i in range(int(pocet)):
                    nove_pismeno = Pismeno(pismenko, int(hodnota))
                    self.sada_pismen.append(nove_pismeno)

        random.shuffle(self.sada_pismen)

    def pocet_pismen(self):
        return len(self.sada_pismen)

    def vyber_pismeno(self):
        return self.sada_pismen.pop()

    def vyber_pismena(self, pocet=7):
        pismena = []
        for i in range(pocet):
            pismena.append(self.vyber_pismeno())
        return pismena

    def vykresli(self, g):
        g.create_oval(self.x, self.y, self.x+self.POLOMER_VRECKA, self.y+self.POLOMER_VRECKA, fill="Orange")
        g.create_text(self.x + self.POLOMER_VRECKA/2, self.y+self.POLOMER_VRECKA/3, font='arial 12 bold', text="POCKET", anchor = tkinter.CENTER)
        g.create_text(self.x + self.POLOMER_VRECKA/2, self.y+self.POLOMER_VRECKA/2, text="Available:", anchor = tkinter.CENTER)
        g.create_text(self.x + self.POLOMER_VRECKA/2, self.y+self.POLOMER_VRECKA/1.5, text=self.pocet_pismen(), anchor = tkinter.CENTER)


class Skore:
    
    def __init__(self, x, y, skore):
        self.x = x
        self.y = y
        self.skore = skore

    def vykresli(self, g):
        g.create_text(self.x + Vrecko.POLOMER_VRECKA/2, self.y, font='arial 12 bold', text="Your score is:", anchor = tkinter.CENTER)
        g.create_text(self.x + Vrecko.POLOMER_VRECKA/2, self.y + Vrecko.POLOMER_VRECKA/3, text=self.skore, anchor = tkinter.CENTER)


class Zasobnik:

    def __init__(self, x, y, zasobnik):
        self.x = x
        self.y = y
        self.zasobnik = zasobnik

    def vykresli(self, g):
         for i in range(len(self.zasobnik)):
            xi = self.x + i*Program.ROZMER_POLICKA
            yi = self.y
            self.zasobnik[i].vykresli(g, xi, yi)

    def je_klik(self, x, y):
        sirka = len(self.zasobnik) * Program.ROZMER_POLICKA
        vyska = Program.ROZMER_POLICKA
        return self.x <= x <= self.x + sirka and self.y <= y <= self.y + vyska

    def aky_utvar(self, x, y):
        if not self.je_klik(x, y):
            return None

        relativne_x = x - self.x
        index = relativne_x // Program.ROZMER_POLICKA
        pismeno = self.zasobnik[index]
        return pismeno
           

class Plocha:
    HODNOTY_POLICOK = {
        'T': {
            'farba': 'Red',
            'nasobok_pismena': 1,
            'nasobok_slova': 3,
            'legenda': 'Triple word score',
        },
        'D': {
            'farba': 'Pink',
            'nasobok_pismena': 1,
            'nasobok_slova': 2,
            'legenda': 'Double word score',
        },
        't': {
            'farba': 'DarkBlue',
            'nasobok_pismena': 3,
            'nasobok_slova': 1,
            'legenda': 'Triple letter score',
        },
        'd': {
            'farba': 'LightBlue',
            'nasobok_pismena': 2,
            'nasobok_slova': 1,
            'legenda': 'Double letter score',
        },
        '.': {
            'farba': 'White',
            'nasobok_pismena': 1,
            'nasobok_slova': 1,
            'legenda': ' ',
        },
    }
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.policka = None

    def nacitaj_sa(self, nazov_suboru="board.txt"):
        self.policka = []
        with open(nazov_suboru) as subor:
            for riadok_suboru in subor:
                novy_riadok = []
                for pismeno in riadok_suboru.split():
                    farba = self.HODNOTY_POLICOK[pismeno]['farba']
                    nasobok_pismena = self.HODNOTY_POLICOK[pismeno]['nasobok_pismena']
                    nasobok_slova = self.HODNOTY_POLICOK[pismeno]['nasobok_slova']
                    
                    nove_policko = Policko(farba, nasobok_slova, nasobok_pismena)
                    novy_riadok.append(nove_policko)
                self.policka.append(novy_riadok)

    def vykresli(self, g):
       for riadok in range(len(self.policka)):     
            for stlpec in range(len(self.policka[riadok])):
                xi = self.x + riadok*Program.ROZMER_POLICKA
                yi = self.y + stlpec*Program.ROZMER_POLICKA
                self.policka[riadok][stlpec].vykresli(g, xi, yi)

    def je_klik(self, x, y):
        sirka = len(self.policka[0]) * Program.ROZMER_POLICKA
        vyska = len(self.policka) *Program.ROZMER_POLICKA
        return self.x <= x <= self.x + sirka and self.y <= y <= self.y + vyska

    def aky_utvar(self, x, y):
        if not self.je_klik(x, y):
            return None

        relativne_x = x - self.x
        index = relativne_x // Program.ROZMER_POLICKA
        pismeno = self.zasobnik[index]
        return pismeno


class Legenda:
    ODSADENIE = 10
    FONT = 'arial 10 bold'

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.double_pismeno = Policko(Plocha.HODNOTY_POLICOK['d']['farba'])
        self.triple_pismeno = Policko(Plocha.HODNOTY_POLICOK['t']['farba'])
        self.double_slovo = Policko(Plocha.HODNOTY_POLICOK['D']['farba'])
        self.triple_slovo = Policko(Plocha.HODNOTY_POLICOK['T']['farba'])
        
    def vykresli(self, g):
        self.vykresli_legendu_policka(
            g,
            self.double_pismeno, 
            'd',
            self.x,
            self.y
        )

        self.vykresli_legendu_policka(
            g,
            self.triple_pismeno, 
            't',
            self.x,
            self.y + self.ODSADENIE + Program.ROZMER_POLICKA
        )

        self.vykresli_legendu_policka(
            g,
            self.double_slovo,
            'T',
            self.x + self.ODSADENIE + Program.ROZMER_POLICKA + 140,
            self.y
        )
        
        self.vykresli_legendu_policka(
            g,
            self.triple_slovo, 
            'D',
            self.x + self.ODSADENIE + Program.ROZMER_POLICKA + 140,
            self.y + self.ODSADENIE + Program.ROZMER_POLICKA
        )


    def vykresli_legendu_policka(self, g, policko, pismeno, x, y):
        policko.vykresli(g, x, y)
        text = Plocha.HODNOTY_POLICOK[pismeno]['legenda']
        g.create_text(
            x + self.ODSADENIE + Program.ROZMER_POLICKA,
            y,
            text=text,
            fill=policko.farba,
            font=self.FONT,
            anchor = tkinter.NW,
        )


class Program:
    ROZMER_POLICKA = 25
    
    def __init__(self):
        self.g = tkinter.Canvas(bg='white', width=800, height=700)
        self.g.pack()
        self.g.master.title("Scrabble")

        self.plocha = Plocha(300, 100)
        self.plocha.nacitaj_sa()

        self.legenda = Legenda(300, 30)

        self.vrecko = Vrecko(100, 100)
        self.vrecko.nacitaj_sadu()   

        self.skore = Skore(100, 250, 50)

        self.zasobnik = Zasobnik(400, 600, self.vrecko.vyber_pismena(7))

        self.g.bind("<Button-1>", self.udalost_kliknutie)
        self.g.bind("<B1-Motion>", self.udalost_pohyb)
        self.g.bind("<ButtonRelease-1>", self.udalost_uvolnenie)

        self.vykresli()

        self.dragovane = None

        tkinter.mainloop()
   
    def vykresli(self):
        self.plocha.vykresli(self.g)
        self.legenda.vykresli(self.g)
        self.vrecko.vykresli(self.g)
        self.skore.vykresli(self.g)
        self.zasobnik.vykresli(self.g)
                      
     
    def udalost_kliknutie(self, event):
        print(self.zasobnik.je_klik(event.x, event.y))
        print(self.zasobnik.aky_utvar(event.x, event.y))
        print(event.x, event.y)
        self.dragovane = self.zasobnik.aky_utvar(event.x, event.y)
        #self.dragovane = {
        #    'pismeno': self.zasobnik.aky_utvar(event.x, event.y),
        #    'obrazok': tkinter.PhotoImage(file='A.png'),
        #}

    def udalost_pohyb(self, event):
        if self.dragovane:
            filename = 'obrazky/' + self.dragovane.pismeno.upper() + '.png'
            self.obr = tkinter.PhotoImage(file=filename)
            self.g.create_image(event.x, event.y, image=self.obr) #image=self.dragovane['obrazok'])

    def udalost_uvolnenie(self, event):
        if self.dragovane:
            #self.na_ploche.append(self.dragovane['obrazok'])
            
            self.dragovane = None
            self.obr = None
        
t = Program()
