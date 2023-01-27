import tkinter as tk
from tkinter import ttk
from pandastable import *
from tkcalendar import Calendar
from datetime import date
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
from functools import partial
import webbrowser
import os
import Search
import plotly.express as px

def link(B1, i):
    """Cette fonction permet d'ouvrir les liens de chaque airbnb disponibles dans la base de données calendar.
    B1 = résultats de la fonction de recherche Search.rech_all
    i = numéro de ligne souhaité, type = int """

    filename = B1.iloc[i,1]
    webbrowser.open(filename)

def affichage(frame, B1, A1): 
    """Cette fonction permet, pour une frame donnée, d'insérer l'ensemble des résultats de la recherche.
    frame = frame sur laquelle insérer les résultats
    B1 = résultats de la fonction de recherche Search.rech_all
    A1 = résultats de la fonction de recherche Search.rech"""

    legend = ['Nom','Résumé','Type de\npropriété','Quartier','Prix','Hôte','Chambres','Options','Note','Lien']
    for i in range(len(legend)) : #On affiche les titres de chaque colonne sur la frame
        label = tk.Label(frame, text = legend[i],font=('Helvetica',16),bg='#bcbcbc', fg = 'White', wraplength=280)
        label.grid(row=0, column = i+1, sticky='nsew')
    for i in range(B1.shape[0]):
        Image_url = B1.iloc[i,0] #On récupère l'url de l'image  
        u = urlopen(Image_url) #On ouvre l'url 
        raw = u.read() #puis on récupère l'information
        u.close()

        im = Image.open(BytesIO(raw)) #On traduit l'information en image
        im = im.resize((120,120),Image.ANTIALIAS)  #On redimensionne la photo 
        photo = ImageTk.PhotoImage(im) #On transforme l'image en photo lisible par Tkinter
        label = tk.Label(frame, image=photo, bg='#bcbcbc') #On créé un label utilisant la photo
        label.image=photo
        label.grid(row=i+1, column=0,sticky = 'nse') #on affiche l'image

    for j in range (0,A1.shape[0]):
        for i in range (0,A1.shape[1]):
            label = tk.Label(frame, text = A1.iloc[j,i],font=('Helvetica',12),bg='#bcbcbc',wraplength=300)
            label.grid(row = j+1, column = i+1, sticky = 'nse') # On affiche toutes les informations : nom, résumé, prix, ...
        globals()[f'link{j}'] = partial(link,B1,j) #On crée un partial de la fonction lien 
        globals()[f'lien{j}'] = tk.Button(frame, text='lien', command= globals()[f'link{j}'],highlightbackground='#bcbcbc') #On crée un bouton permettant d'ouvrir le lien grâce à la fonction link
        globals()[f'lien{j}'].grid(row = j+1, column = 11)
            
def page(i, pages): 
    """Cette fonction permet de naviguer entre les pages de résultats 
    i = numéro de la page que l'on veut afficher, type = int 
    pages = liste de l'ensemble des pages, type = list"""

    for p in pages :
        p.pack_forget() #On cache l'ensemble des pages 
    pages[i-1].pack() #Puis on affiche la page qui nous intéresse

def carto(lis, results_all): 
    """Fonction permettant d'afficher la carte contenant les résultats de la recherche
    lis = base de données listings
    results_all = dataframe obtenu en faisant la recherche avec la fonction Search.rech_all"""
    
    lismed=lis.median(numeric_only=True)
    fig = px.scatter_mapbox(results_all, lat="latitude",lon="longitude" ,hover_name="name",color="price_y", color_continuous_scale = "OrRd",
                        mapbox_style="carto-positron", 
                        zoom=10, center = {"lat": lismed["latitude"], "lon": lismed["longitude"]},
                        opacity= 1) #On crée la carte qui contient l'ensemble des résultats de la recherche
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    if os.path.exists("./données/file.html"): #on vérifie qu'il n'y a pas déjà un fichier "file.html" provenant d'une précédente recherche
        os.remove("./données/file.html") #Si c'est le cas, on le supprime
    fig.write_html("./données/file.html") #On crée le fichier html dans le dossiers "données"
    filename = 'file:///'+os.getcwd()+'/données/file.html' #On récupère le nom complet du fichier file.html
    webbrowser.open(filename) #on ouvre une page web permetttant d'afficher la carte


def Interface(lis,cal):
    """Fonction permettant d'afficher l'interface du moteur de recherche
    lis = base de données listings (nettoyée avec clean_lis)
    cal = base de données calendar (nettoyée avec clean_cal_price) """
    
    #On récupère l'ensemble des quartiers, des types de propriétés et des options sous forme de liste pour les intégrer aux listbox
    prop_type = list(set(lis.property_type.values))
    quartiers = list(set(lis.neighbourhood_group_cleansed.values))
    prop_type = [x for x in prop_type if str(x) != 'nan'] #on enlève les potentiels "NaN" présents
    prop_type.sort()
    quartiers = [x for x in quartiers if str(x) != 'nan']
    quartiers.sort()
    amenities_list = ["TV","Internet","Washer","Kitchen","Air Conditionning","Pets Allowed","Heating","Smoking Allowed","Wheelchair accesible","Essentials"]
    amenities_list.sort()

    #On définit le cadre principal de notre interface : le titre, le fond et la taille
    root = tk.Tk()
    root.title("AirBNB")
    root.config(bg='#bcbcbc')
    root.geometry("1250x1000")

    #On crée une frame qui va contenir le titre 
    frame_tittle = tk.Frame()
    frame_tittle.pack(expand=True)
    lab_tittle = tk.Label(frame_tittle,text="Moteur de Recherche : AirBNB",bg='#bcbcbc', fg = 'white', font=('Helvetica',45,'bold') )
    lab_tittle.grid(row = 0, column = 1, sticky='nse')    

    #On crée une frame qui contiendra la cellule d'entrée de prix min et max
    frame_price = tk.Frame(root, width=100)
    frame_price.pack(expand=True)
    lab_price_min = tk.Label(frame_price, text="Prix minimum :",bg='#bcbcbc', font=('Helvetica',18,'bold'))
    lab_price_max = tk.Label(frame_price, text="Prix maximum :",bg='#bcbcbc', font=('Helvetica',18,'bold'))

    entry_price_min = tk.Entry(frame_price, highlightbackground='#bcbcbc')
    entry_price_max = tk.Entry(frame_price, highlightbackground='#bcbcbc')

    lab_price_min.grid(row = 0, column = 0, sticky = 'nse')
    entry_price_min.grid(row = 0,column=1, sticky = 'nse')
    lab_price_max.grid(row = 0,column = 2, sticky = 'nse')
    entry_price_max.grid(row = 0,column=3, sticky = 'nse')

    #On crée une frame contenant le curseur de note minimale
    frame_curseur = tk.Frame(root)
    frame_curseur.pack()

    lab_review = tk.Label(frame_curseur, text="Note minimale : ",bg='#bcbcbc', font=('Helvetica',18,'bold'))
    curseur1 = Scale(frame_curseur, orient='horizontal', from_ = 0, to = 100, bg = '#bcbcbc')

    lab_review.grid(row = 0,column = 0, sticky = 'nse')
    curseur1.grid(row=0, column=1, sticky='nse')

    #On crée une  frame contenant les trois listes déroulantes permettant de choisir le quartier, le type de propriété et les options
    frame_list = tk.Frame()
    frame_list.pack(expand=True)

    #Listbox et scrollbar pour les types de propriété
    Scroll_p = tk.Scrollbar(frame_list) #On crée une scrollbar permettant de naviguer à travers la listbox 
    Scroll_p.grid(row = 0, column = 2) #On affiche cette scrollbar

    lab_lis_p = tk.Label(frame_list, text='Choissisez votre \ntype de propriété :',bg='#bcbcbc', font=('Helvetica',18,'bold'))
    liste_prop = Listbox(frame_list, selectmode = "multiple", exportselection=False, yscrollcommand=Scroll_p.set )
    for i in range(len(prop_type)):
            liste_prop.insert(i,prop_type[i]) #On insère les types de propriété depuis la liste définie précédemment

    Scroll_p.config(command = liste_prop.yview)#On affecte la scrollbar à la listbox des types de propriétés

    lab_lis_p.grid(row=0, column=0, sticky='nse')
    liste_prop.grid(row = 0, column = 1, sticky = 'e')

    #Listbox et scrollbar pour les quartiers
    Scroll_q = tk.Scrollbar(frame_list)
    Scroll_q.grid(row = 0, column = 5)

    lab_lis_q = tk.Label(frame_list, text='Choissisez votre\nquartier :',bg='#bcbcbc', font=('Helvetica',18,'bold'))
    liste_quar = Listbox(frame_list, selectmode = "multiple", exportselection=False, yscrollcommand= Scroll_q.set)
    for i in range(len(quartiers)):
            liste_quar.insert(i,quartiers[i])

    Scroll_q.config(command = liste_quar.yview)

    #listbox pour les options
    lab_lis_q.grid(row=0, column=3, sticky='nse')
    liste_quar.grid(row = 0, column = 4, sticky = 'e')

    lab_lis_o = tk.Label(frame_list, text='Choissisez vos\noptions :',bg='#bcbcbc', font=('Helvetica',18,'bold'))
    liste_opt = Listbox(frame_list, selectmode = "multiple", exportselection=False)
    for i in range(len(amenities_list)):
            liste_opt.insert(i,amenities_list[i])

    lab_lis_o.grid(row=0, column=6, sticky='nse')
    liste_opt.grid(row = 0, column = 7, sticky = 'e')

    #On crée un choix permettant à l'utilisateur de trier par ordre croissant ou décroissant
    frame_check = tk.Frame(root, background='#bcbcbc')
    frame_check.pack(expand=True)

    check_cr = tk.IntVar() #On crée les variables qui prendront les choix des checkbuttons
    check_de = tk.IntVar()

    check_croissant = tk.Checkbutton(frame_check, text = "Croissant",  font = ('Helvetica'), bg='#bcbcbc', variable=check_cr)
    check_décroissant = tk.Checkbutton(frame_check, text = "Décroissant",  font = ('Helvetica'), bg='#bcbcbc', variable=check_de)
    check_croissant.grid(row = 0, column = 1)
    check_décroissant.grid(row = 0, column = 2) #On affiche les 2 checkbuttons

    lab_check = tk.Label(frame_check, text='Trier par prix :',bg='#bcbcbc', font=('Helvetica',18,'bold'))
    lab_check.grid(row=0, column = 0)
    
    #Enfin on crée une frame pour les dates voulues par l'utilisateur 
    frame_date = ttk.Frame()
    frame_date.pack(expand=True)

    lab_datemin = tk.Label(frame_date, text = "Date de départ",bg='#bcbcbc', font=('Helvetica',18,'bold'))
    lab_datemin.grid(row=0, column = 1, sticky='nsew')
    lab_datemax = tk.Label(frame_date, text = "Date d'arrivée",bg='#bcbcbc', font=('Helvetica',18,'bold'))
    lab_datemax.grid(row=0, column = 2, sticky='nsew')

    calendrier1 = Calendar(frame_date, selectmode = 'day',date_pattern = 'y-mm-dd', year= 16, day = 1, month = 1,mindate=date(2016,1,1), maxdate = date(2017,1,1),selectforeground='red', foreground='Black', normalforeground='black', headersforeground='black')
    calendrier1.grid(row = 1, column = 1, padx=20)

    calendrier2 = Calendar(frame_date, selectmode = 'day',date_pattern = 'y-mm-dd',year= 16, day = 1, month = 1, mindate=date(2016,1,1), maxdate = date(2017,1,1), selectforeground='red', foreground='Black', normalforeground='black', headersforeground='black' )
    calendrier2.grid(row = 1, column = 2, padx = 20)


    #on définit la fonction qui permettra de lancer la recherche et d'afficher les résultats
    def get_entry():
        global price_min, price_max, prop_type1, quartier1, datemax, datemin, results, options1, review

        #on récupère les valeurs prix et date rentrées par l'utilisateur
        price_min = int(entry_price_min.get())
        price_max = int(entry_price_max.get())
        datemin = calendrier1.get_date()
        datemax = calendrier2.get_date()
        review = int(curseur1.get())

        #on récupère les valeurs séléctionnées dans les listbox
        line_p = liste_prop.curselection()
        if len(line_p) > 0: #Cette condition if permet de résoudre le problème de plusieurs selections succésives
            prop_type1 = [] 
            for i in range(len(line_p)): #On fait une boucle pour avoir chaque élément séléctionné dans la liste
                line_p=int(liste_prop.curselection()[i])   
                prop_type1.append(liste_prop.get(line_p)) #On ajoute la selection de l'utilisateur dans une liste
        
        line_q = liste_quar.curselection()
        if len(line_q) > 0:
            quartier1 = []
            for i in range(len(line_q)):
                line_q=int(liste_quar.curselection()[i])    
                quartier1.append(liste_quar.get(line_q))
        
        line_o = liste_opt.curselection()
        if len(line_o) > 0:
            options1 = []
            for i in range(len(line_o)):
                line_o=int(liste_opt.curselection()[i])   
                options1.append(liste_opt.get(line_o))
        
        #on vide les boîtes de dialogue ainsi que les listbox pour une potentielle nouvelle recherche
        entry_price_max.delete(0, tk.END)
        entry_price_min.delete(0, tk.END)
        liste_prop.selection_clear(0,tk.END)
        liste_quar.selection_clear(0,tk.END)
        liste_opt.selection_clear(0,tk.END)

        #On effectue la recherche avec les valeurs spécifiées par l'utilisateur
        results = Search.rech(lis, cal, price_min, price_max, prop_type1, quartier1, datemin, datemax, options1,review)
        results_all = Search.rech_all(lis, cal, price_min, price_max, prop_type1, quartier1, datemin, datemax, options1,review)

        #On met une condition sur l'affichage du résultat : 
        if type(results)==str: #si results est de type string, càd s'il est vide, on affiche un message temporaire spécifiant de changer de critères
            frame_df = tk.Frame(root,bg='#bcbcbc')
            frame_df.pack(fill='x', expand=True)
            lab_res = tk.Label(frame_df,text='Aucune location ne correspond à vos critères.\nVeuillez entrer de nouveaux critères', bg='#bcbcbc', font=('Helvetica',16))
            lab_res.pack()
            root.after(8000, frame_df.destroy)
            
        else : #Sinon, le dataframe n'est pas vide, on affiche les résultats 
            #On trie selon le choix de l'utilisateur 
            if check_de.get()==1 : #Comme les résultats sont déjà triés par prix croissants, on vérfie simplement s'il choisit décroissant
                results.sort_values(by='price_y',inplace=True, ascending=False)
                results_all.sort_values(by='price_y', inplace = True, ascending=False)

            image = results_all[["picture_url","listing_url"]] #On récupère un dataframe contenant l'ensemble des images ainsi que les url
            disp = tk.Toplevel(root) #On crée une nouvelle fenêtre qui permettra d'afficher les résultats
            disp.config(bg='#bcbcbc')
            disp.title("Résultats")
            disp.geometry("1500x1250")

            A1 = results.head(5)
            B1 = image.head(5)

            frame_df = tk.Frame(disp,bg='#bcbcbc') #On crée la frame qui contiendra les résultats
            frame_button1 = tk.Frame(disp, height=100) #On crée la frame qui contiendra les boutons permettant de naviguer entre les pages
            frame_button1.pack(expand = True)
            
            if results.shape[0] > 40 : #Pour éviter des temps de chargement trop long, on limite l'affichage avec image à 40
                pages=[] #On définit la liste qui contiendra toutes les pages
                for i in range(1,9):
                    globals()[f'frame_page{i}'] = tk.Frame(frame_df, bg='#bcbcbc') #on crée la frame i qui sera la page i
                    A1 = results[(i-1)*5:i*5] #on récupère les informations...
                    B1 = image[(i-1)*5:i*5] #...ainsi que les images par groupe de 5
                    affichage(globals()[f'frame_page{i}'], B1, A1) #On introduit toutes les information dans la page i 
                    pages.append(globals()[f'frame_page{i}']) #On ajoute la page i à la liste des pages
                    globals()[f'page{i}'] = partial(page,i, pages) # on crée une fonction qui permettra d'appeler la fonction page et donc afficher la page i
                    globals()[f'b{i}'] = tk.Button(frame_button1, text=i, command=globals()[f'page{i}'],highlightbackground='#bcbcbc')
                    globals()[f'b{i}'].grid(row = 0, column = i+1, sticky = 'nse')

                frame_plus = tk.Frame(frame_df,width=1000, height=1000) #on crée une frame supplémentaire qui contiendra l'ensemble des résultats sous forme de dataframe
                pt = Table(frame_plus, dataframe=results, bg = '#bcbcbc') #On utilise la fonction Table de PandasTable
                pt.show() #On affiche le data frame
                pages.append(frame_plus) 
                page_plus = partial(page,9, pages) #on crée la fonction partial qui affichera la dernière page

                DF = tk.Button(frame_button1, text='Plus de Résultats', command = page_plus, highlightbackground='#bcbcbc') #On crée le bouton permettant d'afficher le dataframe
                DF.grid(row=0, column=10)       

                frame_page1.pack()
                frame_df.pack()
            
            else : #Sinon, il y a moins de 40 résultats, on affiche les résultats exactement de la même manière sans afficher le dataframe à la fin
                pages=[]
                for i in range(1,(results.shape[0]//5+2)):
                        globals()[f'frame_page{i}'] = tk.Frame(frame_df, bg='#bcbcbc')
                        A1 = results[(i-1)*5:i*5]
                        B1 = image[(i-1)*5:i*5]
                        affichage(globals()[f'frame_page{i}'], B1, A1)
                        pages.append(globals()[f'frame_page{i}'])
                        globals()[f'page{i}'] = partial(page,i, pages)
                        globals()[f'b{i}'] = tk.Button(frame_button1, text=i, command=globals()[f'page{i}'],highlightbackground='#bcbcbc')
                        globals()[f'b{i}'].grid(row = 0, column = i+1, sticky = 'nse')
                frame_page1.pack()
                frame_df.pack()
            
            carto1 = partial(carto, lis, results_all)
            carte = tk.Button(frame_button1, text='carte', command = carto1, highlightbackground='#bcbcbc') #On ajoute le bouton permettant d'afficher le résultat sous forme de carte
            carte.grid(row=0, column=1)

    #On crée un bouton permettant de lancer la recherche en lui assignant la fonction get_entry définie précédemment 
    frame_button = tk.Frame()
    frame_button.pack(expand = True)
    recherche = tk.Button(frame_button, text = 'Lancer la recherche',command = get_entry,highlightbackground='#bcbcbc')
    recherche.grid(row = 0, column = 0, sticky = 'nse')

    root.mainloop()