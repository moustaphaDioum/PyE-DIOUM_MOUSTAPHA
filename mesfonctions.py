from re import compile

# fonction verifiant la validité d'un numero
def v_numero(num):
    if len(num) != 7 or not num.isupper():
        return False
    elif num.isalpha() or num.isdecimal():
        return False
    else:
        return True


# fonction verifiant la validité d'un prenom
def v_prenom(prenom):
    prenom = prenom.strip()
    if len(prenom) < 3 or not prenom[0].isalpha():
        return False
    return True


# fonction verifiant la validité d'un nom
def v_nom(nom):
    nom = nom.strip()
    if len(nom) < 2 or not nom[0].isalpha():
        return False
    return True


# fonctions verifiant les classes
def v_classe(classe):
    if classe =='':      #si la case est vide 
        return False
    if not classe[0].isdigit() or classe[-1].lower() not in ['a', 'b']:
        return False
    if int(classe[0])  > 6 or int(classe[0]) < 3:
        return False
    return True


# fonction permettant de changer le format des classes
def change_classe(format):
    if v_classe(format):
        return format[0] + 'em' + format[-1].upper()

# fonction permettant de mettre dans un dico les matieres et les notes
def recup_notes(champs_notes):
    main_dico = dict()
    averages = [] #cette liste nous permettra de calculer la moyenne gen
    if champs_notes.strip() !='':
        champs_notes = champs_notes.replace(' ', '')
        if champs_notes.startswith('#'):
            champs_notes = champs_notes.split("#")[1:]
        else:
            champs_notes = champs_notes.split("#")
        # print(champs_notes)
        for n in champs_notes:
            dico_notes = dict() #on va stcker les notes dans un dico
            k = n.split('[')
            if len(k)==2:
                matiere = k[0]
                notes = k[1][:-1]
            try:
                notes = notes.split(':')
            except Exception as e:
                continue
            devoirs = notes[0].split(';')
            devoirs = [dev.replace(',', '.') for dev in devoirs]
            try:
                devoirs = [float(dev) for dev in devoirs if dev !='']
            except Exception as e:
                return False
            for dev in devoirs:
                if dev > 20. or dev < 0.:
                    return False
            try:
                if float(notes[1]) < 0. or float(notes[1]) > 20.:
                    return False
            except Exception as e:
                return False
            # La moyenne [moyenne = (moyenne(note)+2*note_examen)/3]
            moyenne = round(((sum(devoirs)/len(devoirs)) + 2*float(notes[1].replace(']','')))/3, 2)
            dico_notes.setdefault('devoirs', devoirs)
            dico_notes.setdefault('examen', float(notes[1].replace(',', '.').replace(']','').strip()))
            dico_notes.setdefault('moyenne', moyenne)
            averages.append(moyenne)
            main_dico.setdefault(matiere, dico_notes)
        try:
            main_dico.setdefault('moyenne_generale', round(sum(averages)/len(averages),2))
        except Exception:
            return main_dico
        return main_dico
    else:
        return False

# note = "#Math[13;11:13] #PC[13;19:14]  #Francais[12;14:14]  #SVT[15;19:15] #HG[10;18:13]  #Anglais[11;12;11:20]"
# notes = 'Math[9;10,5;11;13:16] #PC[12:19]  #Francais[10;11:13]  #SVT[15;9;16;11:12] #HG[13:13]  #Anglais[13,12:15]'
# recup_notes(notes)

# this =  'SVT[00;12:12]#PC[10;15:17]#Francais[00;02:13]#SVT[13;1à:14]#Anglais[14;18:15]#HG[20;15:09]#Math[10;12:16]'

# une fonction qui est utilisee pour corriger une erreur dans une note
def change_note(note):
    new_note = []
    if note.strip() !='':
        note = note.replace(' ', '')
        if note.startswith('#'):
            note = note.split("#")[1:]
        else:
            note = note.split("#")
    for n in note:
        n = n.replace(']', '')
        k = n.split('[')
        if len(k)==2:
            matiere = k[0]
            notes = k[1][:-1]
        notes = notes.split(':')
        devoirs = notes[0].split(';')
        examen = notes[1]
        devoirs = [input(matiere + "| devoirs: " + dev + " or new value: ") for dev in devoirs]
        examen = input(matiere + "| examen: " + examen + " or new value: ")
        devoirs = ';'.join(devoirs)
        notes[0] = devoirs
        notes[1] = examen
        notes = ':'.join(notes)
        k = '['.join([matiere, notes]) + ']'
        print(k)
        new_note.append(k)
    return '#'.join(new_note)




# un dico pour les mois et leur nombre correspondant
monthabet = {
    'ja': 1,'f': 2,'mar':3,'av':4,
    'mai':5,'juin':6,'juil':7,'ao':8,
    's':9,'o':10,'n':11,'d':12
}

# fonction qui permet de matcher une date et de dispatcher ses composants
def separator(text):
    pattern_us = r'(\d{2,4})(\s|[/.-])(\w+|\d+)(\s|[/.-])(\d{1,2})' #ceci est le format des dates possibles
    pattern_fr = r'(\d{1,2})(\s|[/.-])(\w+|\d+)(\s|[/.-])(\d{2,4})' #ceci est le format des dates possibles
    dateparser_us =  compile(pattern_us)
    dateparser_fr =  compile(pattern_fr)
    date = dateparser_us.search(text)
    if date:
        return date.group(5), date.group(2), date.group(3), date.group(4),date.group(1)
    else:
        date = dateparser_fr.search(text)
        return date.group(1), date.group(2), date.group(3), date.group(4),date.group(5)



# fonction qui renvoie True si l'annee est bissextile
def bissex(year):
    year = int(year)
    if year%400 == 0 or (year%4==0 and year%100 !=0):
        return True
    return False

# fonction pour trouver la valeur en int du mois
def find_month(month):
    month = month.lower().strip()
    if month.isdigit():
        return month
    elif month.isalpha():
        for abbr in monthabet.keys():
            if month.startswith(abbr):
                return monthabet[abbr]


# fonction pour trouver l'annee avec 4 chiffres
def find_year(annee):
    if len(annee) == 4:
        return annee
    elif len(annee) == 2:
        if int(annee) > 22:
            return '19' + str(annee)
        else:
            return '20' + str(annee)

# fonctions qui verifie la validité d'une date
def valide_date(jour, mois, annee):
    valid = True
    jour, mois, annee = int(jour), int(mois), int(annee)
    if annee == 0 or jour < 1  or jour > 31 or mois > 12 or mois < 0:
        valid = False
    else:
        if bissex(annee) and mois == 2 and jour > 29:
            valid = False
        else:
            if mois == 2 and jour > 28:
                valid = False
    if mois in [4, 6, 9, 11] and jour > 30:
        valid = False
    elif mois in [1, 3, 5, 7, 8, 10, 12] and jour > 31:
        valid = False
    return valid



# la fonction qui regroupe toutes les autres fonctions pour la date
def v_date(text):
    try:
        jour, sep1, mois, sep2, annee = separator(text)
        mois = find_month(mois)
        annee = find_year(annee)
        return valide_date(jour, mois, annee)
    except Exception as e:
        return False


def change_dformat(text):
    jour, sep1, mois, sep2, annee = separator(text)
    mois = find_month(mois)
    annee = find_year(annee)

    return f"{annee}-{mois}-{jour}"


# fonction pour afficher les erreurs
def affiche_errors(mydico):
    if len(mydico) != 0:
        for k in mydico:
            if len(mydico[k]) != 0:
                print(str(k).ljust(150 ,"-"))
                for n in mydico[k]:
                        print(n, ':',  mydico[k][n])
                        print()

# headers = ['N°','CODE', 'Numero', 'Nom', 'Prenom', 'Date de naissance', 'Classe', 'Note']

# fonction affichant les elements d'un dico en ligne et colonne
def affiche_info(dico):
    print('N°'.ljust(2),'CODE'.rjust(6), 'Numero'.rjust(12), 'Nom'.rjust(6), 'Prenom'.rjust(14), 'Date de naissance'.rjust(22), 'Classe'.rjust(8), end="")
    print()
    for row in dico:
        if row == 1:
            print(str(row) + ' ', end=" ] ")
        else:
            print(row, end=" ] ")
        for line in dico[row]:
            if line == 'Note':
                print()
                print('Note: ')
                print(str(dico[row][line]))
            else:
                print(str(dico[row][line]).ljust(8), end=" | ")
        print()
        print()

# fonction affichant les donnees valides
def affiche_infov(dico):
    print('Id'.center(2),'CODE'.center(23), 'Numero'.center(15), 'Nom'.center(28), 'Prenom'.center(10), 'Date de naissance'.center(29), 'Classe'.center(15),'Note'.center(11), end="\n")
    print("_".center(140,'_'))
    for row in dico:
        if row == 1:
            print(str(row) + ' ', end=" ] ")
        else:
            print(row, end=" ] ")
        for line in dico[row]:
            if line == 'Note':
                # print('Moyenne G: ',end='')
                print(str(dico[row][line]['moyenne_generale']))
            else:
                print(str(dico[row][line]).center(18), end=" | ")
        # print()
        print("_".center(140,'_'))
        # print()
# fonction permettant d'afficher une ligne en renseignant son numero
def affiche_numero(maindico, numero):
    founded = ''
    numero =  numero.strip()
    for line in maindico:
        if maindico[line]['Numero'].strip() == numero:
            founded = line
            break
    if founded:
        print(numero.center(100, '*'))
        for info in maindico[int(founded)]:
            print(info, maindico[founded][info])

# fonction qui affiche les elemnts d'un dico
def affiche_line(line):
    n = 10
    for cell in line:
        if cell == 'Note':
            print(str(line[cell]['moyenne_generale']).center(n))
        else:
            print(line[cell].center(n + 1), end=" |")
    print("_".center(100,'_'))

# fonction qui affiche les 5 premiers eleves
def affiche_5premiers(maindico, n=5):
    peps = []
    p = 12
    for cle in maindico:
        peps.append((float(maindico[cle]['Note']['moyenne_generale']), cle))
    peps.sort(reverse=True)
    peps = peps[:n]
    print(peps)
    print('CODE'.center(p +2), 'Numero'.center(p + 3), 'Nom'.center(p), 'Prenom'.center(p-4), 'Date de naissance'.center(p + 12), 'Classe'.center(p-4),  'Moyenne'.center(p + 5), end="\n")
    print("_".center(100,'_'))
    compt = 0
    for num in peps:
        for cle in maindico:
            if cle == num[1]:
                compt +=1
                print(compt, end=" |")
                affiche_line(maindico[cle])

# fonction qui affiche un element du dico invalide en renseignant son id
def affiche_invalide(dico:dict, id:int):
    founded = ''
    for line in dico:
        if line == id:
            founded = id
            break
    if founded:
        print(str(founded).center(170, '*'))
        # affiche_line(dico[founded])
        print(dico[founded])

# fonction retournant un ligne invalide dans le dico invalide
def return_invalide(dico:dict, id:int):
    founded = ''
    for line in dico:
        if line == id:
            founded = id
            break
    if founded:
        return dico[founded]


# fonction qui permet de changer les champs ou il ya des erreurs
def modifier(dico):
    for key in dico:
        if key.lower() == 'numero':
            num = v_numero(dico[key])
            if  num == False:
                dico[key] = input("Entrer un numero valide: ").upper()
                num = v_numero(dico[key])
        elif key.lower() == 'nom'   :
            nom = v_nom(dico[key])
            if nom == False:
                dico[key] = input("Entrer un nom valide: ")
                nom = v_nom(dico[key])
        elif key.lower() == 'prenom':
            prenom = v_prenom(dico[key])
            if prenom == False:
                dico[key] = input("Entrer un prenom valide: ")
                prenom = v_prenom(dico[key])
        elif key.lower() == 'date de naissance':
            naissance = v_date(str(dico[key]))
            if naissance == False:
                dico[key] = input("Entrer une date valide: ")
                naissance = v_date(str(dico[key]))
        elif key.lower() == 'classe':
            classe = v_classe(dico[key])
            if classe == False:
                dico[key] = input("Entrer une classe valide: ")
                classe = v_classe(dico[key])
        elif key.lower() == 'note'  :
            y_note = dico[key]
            note = recup_notes(str(dico[key]))
            if note == False:
                # dico[key] = input(str(dico[key]) + "Entrer des notes valides: ")
                dico[key] = change_note(str(dico[key]))
                note = recup_notes(dico[key])
            else:
                note = y_note
    print(num, nom, prenom, naissance, classe, note)
    if num and nom and prenom and naissance and classe and note:
        return dico
    else:
        trans = input(" Il y a toujours une erreur !!!!\nVoulez vous continue à modifier yes/no: ")
        if trans.lower() == 'yes':
            modifier(dico)
        else:
            return False

  

# verifie si une ligne_invalide est valide avant de permettre de le transferer dans les lignes valides
def isvalid(numero, nom, prenom, classe, naissance, note):
    if v_numero(numero) and v_nom(nom) and v_prenom(prenom) and v_date(date) and v_note(note):
        return True
    else:
        return False

  