import mesfonctions as ms #importer toutes nos fonctions
from csv import reader
from csv import DictReader  
import mysql.connector as mc



dicoprinc = dict()   #le dico qui va contenir toutes nos données
compt = 0

with open('data.csv', 'r') as data:
    data_reader = DictReader(data)
    for ligne in data_reader:
        dicoprinc.setdefault(compt, ligne)
        compt +=1



lignes_valides = dict()  #on y stockera nos données valides
lignes_non_valides = dict()
erreurs = dict()

# separation des données valides et invalides qui seront mises dans des dicos
for k in dicoprinc.keys():
    dico_erreurs = dict()
    for kk in dicoprinc[k].keys():
        if kk.lower()   == 'numero':
            numero = ms.v_numero(dicoprinc[k][kk])
            if numero == False:
                dico_erreurs.setdefault('numero', dicoprinc[k][kk])
        elif kk.lower() == 'nom'   :
            nom = ms.v_nom(dicoprinc[k][kk])
            if nom == False:
                dico_erreurs.setdefault('nom', dicoprinc[k][kk])
        elif kk.lower() == 'prenom':
            prenom = ms.v_prenom(dicoprinc[k][kk])
            if prenom == False:
                dico_erreurs.setdefault('prenom', dicoprinc[k][kk])
        elif kk.lower() == 'date de naissance':
            naissance = ms.v_date(str(dicoprinc[k][kk]))
            if naissance == False:
                dico_erreurs.setdefault('date de naissance', dicoprinc[k][kk])
        elif kk.lower() == 'classe':
            classe = ms.v_classe(dicoprinc[k][kk])
            if classe == False:
                dico_erreurs.setdefault('classe', dicoprinc[k][kk])
        elif kk.lower() == 'note'  :
            # avant_bool = str(dicoprinc[k][kk])
            notes = ms.recup_notes(str(dicoprinc[k][kk]))
            # dicoprinc[k][kk] = notes
            if notes == False:
                dico_erreurs.setdefault('notes', str(dicoprinc[k][kk]))
            else:
                dicoprinc[k][kk] = notes
    erreurs.setdefault(k, dico_erreurs)

    if numero and nom  and naissance and classe and notes:
        #on change le format de classe avant d'inserrer dans les lignes valides
        dicoprinc[k]['Classe'] = ms.change_classe(dicoprinc[k]['Classe'])
        # mettre ici le formatage des naissances
        dicoprinc[k]['Date de naissance'] = ms.change_dformat(dicoprinc[k]['Date de naissance'])
        lignes_valides.setdefault(k, dicoprinc[k])
    else:
        lignes_non_valides.setdefault(k, dicoprinc[k])

#print(lignes_valides)

# fonction pour remplir notre base de données
def insert_to_base():
    # connection a la base de donnees
    print("Connection  à la base de donnees....")
    mabase = mc.connect(
        option_files = "mon.ini"
    )
    cursor = mabase.cursor()
    #on vide toujours la base
    cursor.execute("DELETE FROM eleves")
    cursor.execute("DELETE FROM classes")
    cursor.execute("DELETE FROM notes")
    cursor.execute("DELETE FROM matieres")
    #on recommence l incrementation tjrs à 1 apres chak compilation
    cursor.execute("ALTER TABLE eleves AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE classes AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE notes AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE matieres AUTO_INCREMENT = 1")


    
    for key in lignes_valides:
        ligne           = lignes_valides[key]
        #pour chaque ligne on recupere le num nom prenom date .......
        numero         = ligne.get('Numero')
        nom            = ligne.get('Nom')
        prenom         = ligne.get('Prenom')
        date_naissance = ligne.get('Date de naissance')
        classe         = ligne.get('Classe')
        notes          = ligne.get('Note')
        try:
            cursor.execute(f"INSERT INTO classes (nom_classe) VALUES ('{classe}')")
        except:
            pass
        cursor.execute(f"SELECT id_classe FROM classes WHERE nom_classe = '{classe}'")
        id_classe = cursor.fetchone()[0]
        
        insert_eleve = f"""INSERT INTO eleves (numero, nom, prenom, date_naissance, id_classe)
                           VALUES ('{numero}', '{nom}', '{prenom}', '{date_naissance}', '{id_classe}')
                        """
        cursor.execute(insert_eleve)

        # recuperation de l'id_eleve
        cursor.execute(f"SELECT id_eleve FROM eleves WHERE numero = '{numero}'")
        id_eleve = cursor.fetchone()[0]
        
        #remplir la table moyennes
        moyen_gen=notes['moyenne_generale']
        print(moyen_gen)
        
        insert_moy=f"""INSERT INTO moyennes (id_eleve,id_classe, value) VALUES ('{id_eleve}', '{id_classe}', '{moyen_gen}')"""
        cursor.execute(insert_moy)
        for matiere in notes:
            if matiere != 'moyenne_generale':
                try:
                    cursor.execute(f"INSERT INTO matieres (nom_matiere) VALUES ('{matiere}')")
                except:
                    pass
                cursor.execute(f"SELECT id_matiere FROM matieres WHERE nom_matiere = '{matiere}'")
                id_matiere = cursor.fetchone()[0]

                for type in notes[matiere]:
                    if type == 'examen':
                        value = notes[matiere][type]
                        insert_note = f"""INSERT INTO notes (value, type, id_matiere, id_eleve)
                                          VALUES ('{value}', '{type}', '{id_matiere}', '{id_eleve}')
                                       """
                        #print(insert_note)
                        cursor.execute(insert_note)
                    elif type=='devoir':
                        value = notes[matiere][type]
                        
                        # insertion des devoirs dans la table notes
                        #devoirs = notes[matiere][type]
                        #for value in devoirs:
                        insert_note = f"""INSERT INTO notes (value, type, id_matiere, id_eleve)
                                              VALUES ('{value}', '{type}', '{id_matiere}', '{id_eleve}')
                                           """
                        cursor.execute(insert_note)

    mabase.commit()
    mabase.close()


def menu():
    try:
        print("""
            1. Afficher les données valides
            2. Afficher les données  invalides
            3. Afficher un etudiant  par numero
            4. Afficher les 5 premiers des donnees valides
            5. Modifier une information invalides
            6. Mettre les lignes valides dans la base de donnees
            Ps: Mettez 0 ou un autre chiffre pour quitter
        """)
        try:
            choix = int(input("Faites votre choix: "))
        except Exception as e:
            menu()

        if choix == 1:
            print("Affichage des lignes valides".center(140, '-'))
            ms.affiche_infov(lignes_valides)
            menu()
        elif choix == 2:
            print("Affichage des lignes invalides".center(138, '-'))
            ms.affiche_info(lignes_non_valides)
            menu()
        elif choix == 3:
            print("Affichage d'une information par numero".center(130, '-'))
            numero = input("Entrer le numero à afficher: ").upper().strip()
            ms.affiche_numero(lignes_valides, numero)
            menu()
        elif choix == 4:
            print("Affichage des cinq premiers".center(140, '-'))
            ms.affiche_5premiers(lignes_valides)
            menu()
        elif choix == 5:
            print("Modification des elements invalides".center(140, '-'))
        elif choix == 6:
            insert_to_base()
            menu()
        else:
            print("Merci de votre visite".center(183, '*'))
            exit()
    except KeyboardInterrupt:
        print()
        print("Merci de votre visite".center(183, '*'))
        print()
        exit()



print(""" 
      **                     **
      **  *                * **
      **    *           *    **
      **       *     *       **
      **          *          **
      **                     **
      **                     **
      **                     ** 
      **                     **
      """)

menu()

# print(lignes_valides)