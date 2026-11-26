import tkinter as tk
from tkinter import ttk             # nodig voor extra venster te kunnen aanmaken
import random                       # nodig voor snake
from tkinter import colorchooser    # eigen themakleuren kunnen kiezen

# ----------------- File's -----------------
login_bestandpad = "D:\snake app\login.txt"
score_bestandpad = "D:\snake app\score.txt"
instellingen_bestandpad = "D:\snake app\instellingen.txt"

# ----------------- Venster aanmaken -----------------
venster = tk.Tk()
venster.title("Snake")

# ----------------- Snake -----------------
ROWS = 25
COLS = 25
TILE_SIZE = 25

VENSTER_WIDTH = TILE_SIZE * COLS    #25*25 = 625
VENSTER_HEIGT = TILE_SIZE * ROWS    #25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ----------------- versleutelen -----------------
encryptie_lijst = [
    "a", "b", "c", "d", "e", "f", "g","h", "i", "j",
    "k", "l", "m", "n","o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z", 
    ".", "?", "!", "+", "-", "*", "/", "=", "&", "é",
    "è", ";", ",", ":", " ",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
]

# vercijfert de tekst die het gegeven krijgt
#
# parameters: tekst die moet worden vercijfert worden
# return: vercijferde tekst
def vergrendel(password):           # wat je wilt vergrendelen neemt de plaats van password in
    encryptie_index = -1            # plaats van de letter in de lijst 
    shift = 10                      # aantal plaatsen dat het opschuift
    element_index = 0               # plaats van de letter in het woord
    versleuteld = ""

    # zorgt voor de versleuteling
    for letter in password:         # haalt de karakters 1 voor 1 uit het password
        if letter in encryptie_lijst:       # checkt of ze in de lijst zitten 
            encryptie_index = (encryptie_lijst.index(letter) + shift + element_index) % len(encryptie_lijst)
            element_index += 1
            versleuteld += encryptie_lijst[encryptie_index]
        else: 
            versleuteld += letter   # zorgt ervoor dat er geen data verloren gaat

    return versleuteld

# ontcijfer de tekst die het gegeven krijgt
#
# parameters: tekst die moet worden ontcijfert worden
# return: ontcijferde tekst
def ontcijfer(password):            # password neemt de plaats in van wat je wilt ontcijferen
    vergrendeld = password          # password vanuit bestand ontgrendelen
    encryptie_index = -1            # plaats van de letter in de lijst
    shift = 10                      # aantal plaatsen dat het opschuift
    element_index = 0               # plaats van de letter in het woord

    ontcijferd = ""

    # zorgt voor het ontcijferen
    for letter in vergrendeld:      # haalt de karakters 1 voor 1 uit het password
        if letter in encryptie_lijst:       # checkt of ze in de lijst zitten
            originele_index = (encryptie_lijst.index(letter) - shift - element_index) % len(encryptie_lijst)
            element_index += 1
            ontcijferd += encryptie_lijst[originele_index]
        else:
            ontcijferd += letter    # zorgt ervoor dat er geen data verloren gaat
    return ontcijferd

# ----------------- Navigatie -----------------
# login pagina
def toon_login():
    login.tkraise()

# nieuw account aanmaken
def toon_account():
    account.tkraise()

# inloggen
def toon_snake():
    reset_snake()                   # voert de functie reset_snake op
    snake_frame.tkraise()

# scorebord tonen
def toon_scorebord():
    scoretabel()                    # roept de functie scoretabel op
    scorebord.tkraise()

#instellingen tonen
def toon_instellingen():
    instellingen.tkraise()

# ----------------- Bericht nieuw account -----------------
# account aangemaakt bericht
def toon_bericht():
    account_bericht.config(text="Account aangemaakt! \n gelieve nu in te loggen")

    # verwijderen na 2 sec
    # lambda zorgt ervoor dat functie niet direct wordt uitgevoerd
    account.after(2000, lambda: verberg_bericht())

def verberg_bericht():
    account_bericht.config(text="") # zorgt dat het bericht weg is al er nog eens een nieuw account wordt aangemaakt
    login.tkraise()

# ----------------- Aanmelden -----------------
# deze functie zorgt voor het aanmaken van een nieuw account
# zorgt dat deze gehasht wordt en in het inlogbestand komt te staan 
def aanmelden_nieuw_account():
    # Inloggegevens ophalen
    # check_entry kijkt of er geen lege velden zijn
    # vergrendel() roept de functie op die zorgt voor de hashing
    gebruikersnaam = check_entry(account_gebruikersnaam_entry.get())
    versleuteld_gebruikersnaam = vergrendel(gebruikersnaam)
    wachtwoord = check_entry(account_wachtwoord_entry.get())
    versleuteld_wachtwoord = vergrendel(wachtwoord)

    # Inloggegevens in bestand zetten
    # Eerst controleren of er geen lege velden in zitten
    if gebruikersnaam == "" and wachtwoord == "":
        account_foutmelding_label.config(text="Gelieve je gegevens in te vullen")

    elif gebruikersnaam == "":
        account_foutmelding_label.config(text="Gelieve een gebruikersnaam ingeven")

    elif wachtwoord == "":
        account_foutmelding_label.config(text="Gelieve een wachtwoord in te vullen")

    else:
        with open(login_bestandpad, "r") as login_gegevens:
            for regel in login_gegevens:
                try:
                    username, password = regel.strip().split("|")
                except ValueError:
                    continue
        
                if versleuteld_gebruikersnaam == username:
                    account_foutmelding_label.config(text="gebruikersnaam bestaat al!")
                    break
                    
                else:
                    account_foutmelding_label.config(text="")

                    # zet de nieuwe inloggevens op de laatste rij van het .txt bestand
                    with open(login_bestandpad, "a") as login_gegevens:
                        login_gegevens.write(f"{versleuteld_gebruikersnaam}|{versleuteld_wachtwoord}\n")

                    # entry velden leegmaken voor volgende login
                    account_gebruikersnaam_entry.delete(0, tk.END)
                    account_wachtwoord_entry.delete(0, tk.END)

                    #bericht tonen
                    toon_bericht()

                    # zorgt ervoor dat het er maar een keer in komt te staan
                    break

# ----------------- Inloggen -----------------
# Kijkt of je gegevens ergens in het loginbestand staan
def inloggen():
    global ingelogde_gebruiker
    gebruikersnaam = login_gebruikersnaam_entry.get()
    wachtwoord = login_wachtwoord_entry.get()

    with open(login_bestandpad, "r") as login_gegevens:
        for regel in login_gegevens:
            # try except zorgt dat als er een ongeldige regel in zit die wordt overgeslaan zodat je inloggen niet crasht
            try:
                username, password = regel.strip().split("|")
            except ValueError:
                continue

            gebruikersnaam_bestand = ontcijfer(username)
            wachtwoord_bestand = ontcijfer(password)

            if (gebruikersnaam == gebruikersnaam_bestand and 
                wachtwoord == wachtwoord_bestand):

                # entry velden leegmaken voor volgende login
                login_gebruikersnaam_entry.delete(0, tk.END)
                login_wachtwoord_entry.delete(0, tk.END)

                ingelogde_gebruiker = gebruikersnaam_bestand
                reset_snake()
                snake_frame.tkraise()
                break

            elif (gebruikersnaam != gebruikersnaam_bestand and 
                  wachtwoord == wachtwoord_bestand):

                login_foutmelding_label.config(text="Gebruikersnaam incorrect!")
                break

            elif (gebruikersnaam == gebruikersnaam_bestand and 
                  wachtwoord != wachtwoord_bestand):

                login_foutmelding_label.config(text="Wachtwoord incorrect!")
                break

            elif (gebruikersnaam != gebruikersnaam_bestand and 
                  wachtwoord != wachtwoord_bestand):
                login_foutmelding_label.config(text="Je gegevens kloppen niet!")

# ----------------- Uitloggen -----------------
# Logt je uit en zorgt dat de game wordt gereset
def uitloggen():
    reset_snake()                   # zorgt dat snake gerest wordt bij opnieuw inloggen
    login.tkraise()

# ----------------- Entry's checken -----------------
def check_entry(tekst):
    if not tekst:
        return ""
    else:
        return tekst

# ----------------- Snake -----------------
# Snake game resetten
def reset_snake():
    global snake, food, velocityX, velocityY, snake_body, game_over, score
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) #single tile, snake's head
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = [] #multiple snake tiles
    game_over = False
    score = 0

# Snake game resetten als je op de 'R' toets drukt
def reset_snake_key(event):
    global snake, food, velocityX, velocityY, snake_body, game_over, score
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) #single tile, snake's head
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
    velocityX = 0
    velocityY = 0
    snake_body = [] #multiple snake tiles
    game_over = False
    score = 0

# ----------------- Scorebord maken -----------------
ingelogde_gebruiker = ""
behaalde_score = -1

# Kijkt welke score's en namen er al in het bestand zitten
def score_inlezen():
    score_data_unsorted ={}
    
    try:
        with open("score.txt", "r") as score:
            for regel in score:
                regel = regel.strip()
                if not regel:
                    continue
                naam, score = regel.split(":")
                score_data_unsorted[naam] = int(score)
    except FileNotFoundError:
        score_data_unsorted[0] = str("Geen data gevonden")
    
    return score_data_unsorted

score_unsorted = score_inlezen()
score_data_sorted = ""

# Kijkt of de gebruiker al in de dictionary staat zo ja voegt hij direct de score erbij
# Als de gebruiker al bestaat kijkt hij eerst of zijn behaalde score groter is
#
# Parameters: naam van de gebruiker en de bepaalde score
# return: / 
def high_score(gebruiker, score): 
    if gebruiker not in score_unsorted or score > score_unsorted[gebruiker]:
        score_unsorted[gebruiker] = score

# Maakt de scoretabel en zet deze op het scherm
def scoretabel():
    global score_unsorted, behaalde_score, game_over, score_data_sorted

    # kijkt of de gebruiker heeft gespeeld zo ja dan roept hij de highscore functie op
    if behaalde_score != -1:
        high_score(ingelogde_gebruiker, behaalde_score)

    # lijst sorteren
    score_data_sorted = sorted(score_unsorted.items(), key=lambda x: x[1], reverse=True)

    tekst = "--- SCORE'S ---\n"

    # enumerate zorgt voor het ranggetal
    for index, (speler, score) in enumerate(score_data_sorted, start=1):
        if index > 10:
            break
        tekst += f"{index}. {speler}: {score}ptn\n"

    scorebord_label.config(text=tekst)

# Opent een apart scherm waar je alle scores kunt zien
def scoretabel_full():
    global score_unsorted, behaalde_score, game_over, score_data_sorted

    # extra venster voor scoretabel aanmaken
    scoretabel_venster = tk.Toplevel(venster)
    scoretabel_venster.title("Scorebord")
    scoretabel_venster.geometry("250x500")

    bg = kleuren[huidige_thema]["bg"]
    fg = kleuren[huidige_thema]["fg"]
    # thema ook hier toepassen 
    thema_toepassen(scoretabel_venster,bg, fg)
    

    # ----------------- Scrollbar -----------------
    def update_scrollregio(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # canvas + scrollbar
    canvas = tk.Canvas(scoretabel_venster)
    scrollbar = tk.Scrollbar(scoretabel_venster, orient="vertical", command=canvas.yview)

    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", update_scrollregio)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    #layout
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    scoretabel_venster.grid_rowconfigure(0, weight=1)
    scoretabel_venster.grid_columnconfigure(0, weight=1)

    # inhoud venster
    scoretabel_titel = tk.Label(scrollable_frame, text="Scorebord", font=30)
    scoretabel_titel.grid(row=1, column=0)

    tekst = "--- SCORE'S ---\n"

    # tekent nu de volledige scoretabel
    for index, (speler, score) in enumerate(score_data_sorted, start=1):
        tekst += f"{index}. {speler}: {score}ptn\n"

    scorebord_label_full = tk.Label(scrollable_frame, text=tekst, font=5)
    scorebord_label_full.grid(row=2, column=0)

# ----------------- Afsluiten -----------------
# Zorgt ervoor dat zeker alle gegevens worden opgeslaan
def bij_afsluiten():
    global score_unsorted
    with open("score.txt", "w") as score_bestand:
        for naam, score in score_unsorted.items(): 
            score_bestand.write(f"{naam}: {score}\n")
    venster.destroy()

# ----------------- Instellingen -----------------
# thema kiezer
huidige_thema = "lichte mode"
vorig_thema = "lichte mode"
gekozen_thema = tk.StringVar(value="lichte mode")

thema_lijst = [
        "lichte mode",
        "donkere mode", 
        "retro", 
        "hoog contrast",
        "aangepast"
    ]

kleuren = {
    "lichte mode": {
            "bg": "#F5F5F5", 
            "canvas": "#E8E8E8",
            "fg": "#1A1A1A",
            "snake": "#2E7D32",
            "food": "#D32F2F"
        },
    
    "donkere mode": {
            "bg": "#1E1E1E",
            "canvas": "#0D0D0D",
            "fg": "#FFFFFF",
            "snake": "#32CD32",
            "food": "#FF0000"
        },

    "retro": {
            "bg": "#0C0C0C",
            "canvas": "#1F1F1F",
            "fg": "#33FF33",
            "snake": "#00FF00",
            "food": "#FF3B3B"
        },

    "hoog contrast": {
            "bg": "#000000",
            "canvas": "#000000",
            "border": "#2DA5EA",
            "fg": "#FFFFFF",
            "snake": "#BFFF00",
            "food": "#FF0000"
        },

    "aangepast": {
            "bg": None,
            "canvas": None,
            "border": None,
            "fg": None,
            "snake": None,
            "food": None
        }

    }

# Gaat het thema gaan veranderen naar het gekozen thema
#
# Parameters: gekozen thema
# Return: /
def verander_thema(thema):
    global huidige_thema, vorig_thema

    # Alleen vorig_thema aanpassen als we NIET naar aangepast gaan
    if thema != "aangepast":
        vorig_thema = huidige_thema

    huidige_thema = thema

    if thema == "aangepast":
        kleur_kiezen_frame.tkraise()

        bg = kleuren["aangepast"]["bg"] or kleuren[vorig_thema]["bg"]
        fg = kleuren["aangepast"]["fg"] or kleuren[vorig_thema]["fg"]
        canvas = kleuren["aangepast"]["canvas"] or kleuren[vorig_thema]["canvas"]
        border = kleuren["aangepast"]["border"]
        
        
        snake_canvas.config(
            bg=canvas,
            highlightthickness=3 if border != None else 0,
            highlightbackground=border
        )

    else:
        bg = kleuren[thema]["bg"]
        fg = kleuren[thema]["fg"]
        canvas = kleuren[thema]["canvas"]

        border = kleuren[thema].get("border", bg)

        snake_canvas.config(
            bg=canvas,
            highlightthickness=0 if thema != "hoog contrast" else 3,
            highlightbackground=border
        )

    thema_toepassen(venster, bg, fg)

# Zorgt ervoor dat alle pagina's de juiste styling krijgen
#
# Parameters: welk scherm er moet worden verander, kleur van de achtergrond, kleur van de voorgrond 
# Return: /
def thema_toepassen(widget, bg, fg):
    global huidige_thema
    if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.OptionMenu)):
        widget.config(bg=bg, fg=fg)

        # cursor entry aanpassen
        if isinstance(widget, tk.Entry):
            widget.config(bg=bg)
    
    elif isinstance(widget, (tk.Frame, tk.Tk)):
        widget.config(bg=bg)

    for child in widget.winfo_children():
        thema_toepassen(child, bg, fg)

    if huidige_thema == "aangepast":
        canvas_kleur = (
            kleuren["aangepast"]["canvas"]
            or kleuren[vorig_thema]["canvas"]
        )
    else:
        canvas_kleur = kleuren[huidige_thema]["canvas"]

        snake_canvas.config(bg=canvas_kleur)


geklikte_knop = ""

# Kijkt welke knop er is ingedrukt
#
# Parameters: tekst van welk item de knop voostelt
# Return: /
def welke_knop(button_text):
    global geklikte_knop
    geklikte_knop = button_text
    controleer()

# Gaat de kleuren in de dictionary zetten om dan te worden toegepast
def controleer():
    global huidige_thema 

    if geklikte_knop == "bg":
        color_bg = colorchooser.askcolor(title="achtergrondkleur")[1]
        kleuren["aangepast"]["bg"] = color_bg

    elif geklikte_knop == "canvas":
        color_canvas = colorchooser.askcolor(title="canvaskleur")[1]
        kleuren["aangepast"]["canvas"] = color_canvas

    elif geklikte_knop == "border":
        color_border = colorchooser.askcolor(title="borderkleur")[1]
        kleuren["aangepast"]["border"] = color_border

    elif geklikte_knop == "fg":
        color_fg = colorchooser.askcolor(title="tekstkleur")[1]
        kleuren["aangepast"]["fg"] = color_fg

    elif geklikte_knop == "snake":
        color_snake = colorchooser.askcolor(title="snakekleur")[1]
        kleuren["aangepast"]["snake"] = color_snake

    elif geklikte_knop == "food":
        color_food = colorchooser.askcolor(title="etenkleur")[1]
        kleuren["aangepast"]["food"] = color_food

    elif geklikte_knop == "toepassen":
        gekozen_thema.set("aangepast")
        verander_thema("aangepast")
        instellingen.tkraise()

# ----------------- Snelheid ------------------
gekozen_snelheid = tk.StringVar(value="normaal")
snelheid_optie = [
    "traag",    # 150
    "normaal",  # 100
    "snel",     # 75
    "zeer snel",# 50
    "god mode"  # 25
]

snelheden = {
    "traag": 150,
    "normaal": 100,
    "snel": 75,
    "zeer snel": 50,
    "god mode": 25
}

# Zorgt dat de snelheid word aangepast
# Wordt uitgedrukt in fps hoe kleiner het getal hoe sneller
def verander_snelheid(snelheid):
    global speed
    speed = snelheden[snelheid]

# ----------------- Appels ------------------
gekozen_aantal_appels = tk.StringVar(value="1")
appels_optie = [
    1,
    2,
    3,
    4,
    5
]

aantal_appels = 1
appels = []

appels.append(
    Tile(
        10 * TILE_SIZE,
        10 * TILE_SIZE
    )
)

plaats_appels = {
    0: {
        0:(10, 10)
    },

    1: {
        0: (9, 11),
        1: (11, 9)
    },

    2:{ 
        0: (10, 10),
        1: (11, 9),
        2: (9, 11)

    },

    3:{ 
        0: (9, 9),
        1: (9, 11),
        2: (11, 11),
        3: (11, 9)

    },

    4:{ 
        0: (10, 10),
        1: (9, 11),
        2: (11, 9),
        3: (11, 11),
        4: (9, 9)
    }
}

# Tekent de geselecteert aantal appels op de startplaats
#
# Parameters: aantal appels
# Return: /
def aantal_appels_tekenen(appel):
    global aantal_appels, appels

    appels = []
    aantal_appels = appels_optie[appel-1]

    snake_canvas.delete("all")

    level_data = plaats_appels[aantal_appels-1]

    for x, y in level_data.values():
        appels.append(
            Tile(
                x * TILE_SIZE,
                y * TILE_SIZE
            )
        )
            
# ----------------- Container -----------------
container = tk.Frame(venster)
container.pack(fill="both", expand=True)

# frame's mee laten groeien met venster
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# frame's aanmaken
login = tk.Frame(container, bg="white")
account = tk.Frame(container, bg="red")
snake_frame = tk.Frame(container)
scorebord = tk.Frame(container, bg="green")
instellingen = tk.Frame(container, bg="black")
kleur_kiezen_frame = tk.Frame(container, bg="yellow")

# frame's in grid plaatsen
login.grid(row=0, column=0, sticky="nsew")
account.grid(row=0, column=0, sticky="nsew")
snake_frame.grid(row=0, column=0, sticky="nsew")
scorebord.grid(row=0, column=0, sticky="nsew")
instellingen.grid(row=0, column=0, sticky="nsew")
kleur_kiezen_frame.grid(row=0, column=0, sticky="nsew")

# ----------------- Menubalk -----------------
def menu_toevoegen(target_frame):
    menubalk = tk.Frame(target_frame)
    menubalk.pack(side="top", fill="x")

    snake_knop = tk.Button(menubalk, text="Snake", command=toon_snake)
    snake_knop.pack(side="left", padx=5, pady=5)
    scorebord_knop = tk.Button(menubalk, text="Scorebord", command=toon_scorebord)
    scorebord_knop.pack(side="left", padx=5, pady=5)
    instellingen_knop = tk.Button(menubalk, text="instellingen", command=toon_instellingen)
    instellingen_knop.pack(side="left", padx=5, pady=5)

# ----------------- Invullen van frame's -----------------

# ----------------- LOGIN -----------------
login_titel = tk.Label(login, text="Login")
login_titel.pack()
login_gebruikersnaam_label = tk.Label(login, text="Gebruikersnaam")
login_gebruikersnaam_label.pack()
login_gebruikersnaam_entry = tk.Entry(login)
login_gebruikersnaam_entry.pack()
login_wachtwoord_label = tk.Label(login, text="Wachtwoord")
login_wachtwoord_label.pack()
login_wachtwoord_entry = tk.Entry(login, show="*")
login_wachtwoord_entry.pack()
login_login_button = tk.Button(login, text="Inloggen.", command=inloggen)
login_login_button.pack()
account_button = tk.Button(login, text="Geen account?", command=toon_account)
account_button.pack()
login_foutmelding_label = tk.Label(login, text="")
login_foutmelding_label.pack()

# ----------------- ACCOUNT -----------------
account_titel = tk.Label(account, text="Account aanmaken")
account_titel.pack()
account_gebruikersnaam_label = tk.Label(account, text="Gebruikersnaam")
account_gebruikersnaam_label.pack()
account_gebruikersnaam_entry = tk.Entry(account)
account_gebruikersnaam_entry.pack()
account_wachtwoord_label = tk.Label(account, text="Wachtwoord")
account_wachtwoord_label.pack()
account_wachtwoord_entry = tk.Entry(account, show="*")
account_wachtwoord_entry.pack()
account_login_button = tk.Button(account, text="Inloggen.", command=aanmelden_nieuw_account)
account_login_button.pack()
account_bericht = tk.Label(account, text="", bg="red")
account_bericht.pack()
account_foutmelding_label = tk.Label(account, text="")
account_foutmelding_label.pack()

# ----------------- Snake -----------------
menu_toevoegen(snake_frame)

snake_frame_control_label = tk.Label(snake_frame, text="controls='wasd', 'zqsd', ⬅️⬆️⬇️➡️")
snake_frame_control_label.pack()
snake_canvas = tk.Canvas(snake_frame, bg="black", width=VENSTER_WIDTH, height=VENSTER_HEIGT, borderwidth=0, highlightthickness=0)
snake_canvas.pack()
snake_frame_reset_label = tk.Label(snake_frame, text="Press r to restart.")
snake_frame_reset_label.pack()
snake_frame_reset = tk.Button(snake_frame, text="reset", command=reset_snake)
snake_frame_reset.pack()
venster.update()

#initialize game
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) # single tile, snake's head
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = [] # multiple snake tiles
game_over = False
score = 0
speed = 100

#game loop
def change_direction(e): #e = event
    global velocityX, velocityY, game_over
    if (game_over):
        return #edit this code to reset game variables to play again

    if (e.keysym == "Up" and velocityY != 1 or 
          e.keysym == "w" and velocityY != 1 or 
          e.keysym == "z" and velocityY != 1
        ):
        velocityX = 0
        velocityY = -1
        
    elif (e.keysym == "Down" and velocityY != -1 or 
          e.keysym == "s" and velocityY != -1
        ):
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" and velocityX != 1 or 
          e.keysym == "a" and velocityX != 1 or 
          e.keysym == "q" and velocityX != 1
        ):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1 or 
          e.keysym == "d" and velocityX != -1
        ):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score, appels
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= VENSTER_WIDTH or snake.y < 0 or snake.y >= VENSTER_HEIGT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    #collision
    for food in appels:
        if (snake.x == food.x and snake.y == food.y): 
            snake_body.append(Tile(food.x, food.y))
        
            food.x = random.randint(0, COLS-1) * TILE_SIZE
            food.y = random.randint(0, ROWS-1) * TILE_SIZE

            score += 1
            break
    
    #update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score, behaalde_score
    move()

    snake_canvas.delete("all")

    color_food = kleuren[gekozen_thema.get()]["food"]
    color_snake = kleuren[gekozen_thema.get()]["snake"]
    color_tekst = kleuren[gekozen_thema.get()]["fg"]

    for food in appels:
        food_canvas = snake_canvas.create_rectangle(
            food.x, 
            food.y, 
            food.x + TILE_SIZE, 
            food.y + TILE_SIZE, 
            fill = color_food
        )

    #draw snake
    snake_canvas_var = snake_canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = color_snake)

    for tile in snake_body:
        snake_canvas_var = snake_canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = color_snake)

    if (game_over):
        tekst_canvas = snake_canvas.create_text(VENSTER_WIDTH/2, VENSTER_HEIGT/2, font = "Arial 20", text = f"Game Over: {score}", fill = color_tekst)
        behaalde_score = score
    else:
        tekst_canvas = snake_canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = color_tekst)
    
    venster.after(speed, draw) #call draw again every 100ms (1/10 of a second) = 10 frames per second

draw()
venster.bind("<KeyPress>", change_direction)    # when you press on any key
venster.bind("r", reset_snake_key)              # restart snake als er op R wordt gedrukt

# ----------------- Scorebord -----------------
menu_toevoegen(scorebord)
scorebord_label = tk.Label(scorebord, text="", bg="green", font=5)
scorebord_label.pack(pady=20)

scorebord_full_button = tk.Button(scorebord, text="volledig scorebord", command=scoretabel_full)
scorebord_full_button.pack()

# ----------------- Instellingen -----------------
menu_toevoegen(instellingen)

# --------- Mode's menu ---------
optie_menu = tk.OptionMenu(
    instellingen, 
    gekozen_thema,
    *thema_lijst, 
    command=verander_thema
)

optie_menu.pack()
# --------- Snelheid aanpassen ---------
instellingen_speed_label = tk.Label(instellingen, text="snelheid")
instellingen_speed_label.pack()
instellingen_speed_menu = tk.OptionMenu(
    instellingen,
    gekozen_snelheid,
    *snelheid_optie,
    command=verander_snelheid
)
instellingen_speed_menu.pack()

# --------- Appels aanpassen ---------
instellingen_appel_label = tk.Label(instellingen, text="aantal appelen")
instellingen_appel_label.pack()
instellingen_appel_menu = tk.OptionMenu(
    instellingen, 
    gekozen_aantal_appels,
    *appels_optie,
    command=aantal_appels_tekenen
)
instellingen_appel_menu.pack()

instellingen_uitloggen_button = tk.Button(instellingen, text="log uit", command=uitloggen)
instellingen_uitloggen_button.pack()

# --------- Aangepast thema ---------
snake_kleur_label = tk.Label(kleur_kiezen_frame, text="snakekleur kiezen.")
snake_kleur_label.pack()
snake_kleur_button = tk.Button(kleur_kiezen_frame, text="kies je kleur!", command=lambda: welke_knop("snake"))
snake_kleur_button.pack()

bg_kleur_label = tk.Label(kleur_kiezen_frame, text="achtergrondkleur kiezen.")
bg_kleur_label.pack()
bg_kleur_button = tk.Button(kleur_kiezen_frame, text="kies je kleur!", command=lambda: welke_knop("bg"))
bg_kleur_button.pack()

fg_kleur_label = tk.Label(kleur_kiezen_frame, text="tekstkleur kiezen.")
fg_kleur_label.pack()
fg_kleur_button = tk.Button(kleur_kiezen_frame, text="kies je kleur!", command=lambda: welke_knop("fg"))
fg_kleur_button.pack()

border_kleur_label = tk.Label(kleur_kiezen_frame, text="borderkleur kiezen.")
border_kleur_label.pack()
border_kleur_button = tk.Button(kleur_kiezen_frame, text="kies je kleur!", command=lambda: welke_knop("border"))
border_kleur_button.pack()

canvas_kleur_label = tk.Label(kleur_kiezen_frame, text="canvaskleur kiezen.")
canvas_kleur_label.pack()
canvas_kleur_button = tk.Button(kleur_kiezen_frame, text="kies je kleur!", command=lambda: welke_knop("canvas"))
canvas_kleur_button.pack()

food_kleur_label = tk.Label(kleur_kiezen_frame, text="etenkleur kiezen.")
food_kleur_label.pack()
food_kleur_button = tk.Button(kleur_kiezen_frame, text="kies je kleur!", command=lambda: welke_knop("food"))
food_kleur_button.pack()

thema_toepassen_button = tk.Button(kleur_kiezen_frame, text="toepassen!", command=lambda: welke_knop("toepassen"))
thema_toepassen_button.pack()
# ----------------- Venster afsluiten -----------------
venster.protocol("WM_DELETE_WINDOW", bij_afsluiten)

# ----------------- Venster starten -----------------
login.tkraise()
verander_thema("lichte mode")
venster.resizable(width=False, height=False)
venster.geometry(f"{VENSTER_WIDTH}x{VENSTER_HEIGT + 80}")
venster.mainloop()