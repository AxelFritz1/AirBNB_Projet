import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import Data
import datetime as dt

def intervalle(prop, date_min, date_max): 
    """Cette fonction permet d'obtenir un dataframe contenant les logements répondants aux critères de date
    prop = subset de la base de données calendar (nettoyée avec la fonction Data.clean_cal_price)
    date_min = date d'arrivée, format string
    date_max = date de départ, format string """
    prop = prop.reset_index()
    B = pd.DataFrame()
    min = dt.datetime.strptime(date_min, '%Y-%m-%d')
    max = dt.datetime.strptime(date_max, '%Y-%m-%d')
    nbr_jours = max-min #On calcule le time delta entre les deux dates
    nbr_jours = nbr_jours.days # On récupère le nbr de jours demandé par l'utilisateur
    for i in prop.index[prop.date == date_min]:
        if i + nbr_jours in prop.index[prop.date == date_max]: 
            B = pd.concat([B,prop.iloc[i:i+1]])
    return(B)
#si l'index de chaque logement pour la date date_min + le nbr de jours ne correspond pas à l'index de la date date_max, 
#alors le logement n'est pas disponible sur toute la plage demandée. Ainsi, on récupère seulement les logements satisfaisant cette condition

def rech(lis, cal, price_min, price_max, loc_type, quartier, date_min, date_max, options, review_note):
    """Cette fonction permet d'effectuer une recherche de logement selon différents critères.
    lis = base de données listings (nettoyée avec Data.clean_lis)
    cal = base de données calendar (nettoyée avec Data.clean_cal_price)
    price_min = prix minimum des logements, type = int
    price_max = prix maximum des logements, type = int
    loc_type = liste des types de propriétés désirés, type = list
    quartier = liste des quartiers désirés, type = list
    date_min = date d'arrivée, format string
    date_max = date de départ, format string
    options = liste des options désirées, type = list
    review_note = note minimale du logement (/100), type = int
    """
    prop = lis.loc[
        (lis.property_type.isin(loc_type)==True)
        &(lis.apply(lambda x: all(item in x.amenities for item in options), axis=1))
        &(lis.review>review_note)
        &(lis.neighbourhood_group_cleansed.isin(quartier)==True) ]
    #On récupère l'ensemble des locations répondants aux caractéristiques demandées par l'utilisateur
    
    prop_price = cal.loc[
        (cal.price>price_min)&
        (cal.price<price_max)]
    #On récupère l'ensemble des locations disponibles répondants aux contraintes de prix

    results = pd.merge(prop, prop_price, how='inner', on='id')
    #On merge les deux dataframe

    if results.empty: #si le dataframe est vide, pas besoin de vérifier les dates, on renvoie le message d'erreur
        return("Aucune location ne correspond à votre selection")
    
    prop_cal = cal[cal.id.isin(results.id)] #on récupère un subset de calendar contenant seulements les id correspondant aux id de results
    prop_date = intervalle(prop_cal, date_min, date_max)
    #on récupère le dataframe contenant les logements répondant aux critères de date
    
    results = pd.merge(results, prop_date, how = 'inner', on = 'id')
    #On fusionne selon l'id afin de récupérer les locations répondant à tous les critères

    if results.empty:
        return("Aucune location ne correspond à votre selection")

    results.drop_duplicates(subset = 'id', keep = 'first', inplace=True)

    results.sort_values(by='price_y',inplace=True) 
    #On trie les locations par prix croissant

    results=results[['name','summary','property_type','neighbourhood_group_cleansed','price_y','host_name','bedrooms','amenities','review']]

    return(results)

def rech_all(lis, cal, price_min, price_max, loc_type, quartier, date_min, date_max, options, review_note):
    """Cette fonction permet d'effectuer une recherche de logement selon différents critères.
    lis = base de données listings (nettoyée avec Data.clean_lis)
    cal = base de données calendar (nettoyée avec Data.clean_cal_price)
    price_min = prix minimum des logements, type = int
    price_max = prix maximum des logements, type = int
    loc_type = liste des types de propriétés désirés, type = list
    quartier = liste des quartiers désirés, type = list
    date_min = date d'arrivée, format string
    date_max = date de départ, format string
    options = liste des options désirées, type = list
    review_note = note minimale du logement (/100), type = int
    """
    prop = lis.loc[
        (lis.property_type.isin(loc_type)==True)
        &(lis.apply(lambda x: all(item in x.amenities for item in options), axis=1))
        &(lis.review>review_note)
        &(lis.neighbourhood_group_cleansed.isin(quartier)==True) ]
    #On récupère l'ensemble des locations répondants aux caractéristiques demandées par l'utilisateur
    
    prop_price = cal.loc[
        (cal.price>price_min)&
        (cal.price<price_max)]
    #On récupère l'ensemble des locations disponibles répondants aux contraintes de prix

    results = pd.merge(prop, prop_price, how='inner', on='id')
    #On merge les deux dataframe

    if results.empty: #si le dataframe est vide, pas besoin de vérifier les dates, on renvoie le message d'erreur
        return("Aucune location ne correspond à votre selection")
    
    prop_cal = cal[cal.id.isin(results.id)] #on récupère un subset de calendar contenant seulements les id correspondant aux id de results
    prop_date = intervalle(prop_cal, date_min, date_max)
    #on récupère le dataframe contenant les logements répondant aux critères de date
    
    results = pd.merge(results, prop_date, how = 'inner', on = 'id')
    #On fusionne selon l'id afin de récupérer les locations répondant à tous les critères

    if results.empty:
        return("Aucune location ne correspond à votre selection")

    results.drop_duplicates(subset = 'id', keep = 'first', inplace=True)

    results.sort_values(by='price_y',inplace=True) 
    #On trie les locations par prix croissant

    return(results)