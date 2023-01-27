import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def clean_cal():
    """ Cette fonction permet de nettoyer la base de données calendar, aucun attribut n'est attendu"""
    cal = pd.read_csv("./données/calendar.csv")

    cal.rename(columns = {'listing_id': 'id'}, inplace = True) #on prépare les futurs merge en renommant par id

    cal["date"] = pd.to_datetime(cal["date"]) #on transforme la colonne date en type date
    cal['month'] = cal['date'].dt.strftime('%m') #on crée une nouvelle colonne avec le mois 

    cal = cal.drop(cal[cal.date >= "2017-01-01"].index)

    return(cal)

def clean_cal_price():
    """ Cette fonction permet de nettoyer la base de données calendar ainsi que la colonne prix, aucun attribut n'est attendu"""
    cal = pd.read_csv("./données/calendar.csv")

    cal.rename(columns = {'listing_id': 'id'}, inplace = True) # on prépare le merge en renommant par id

    cal["date"] = pd.to_datetime(cal["date"]) #on transforme la colonne date en type date

    cal = cal.dropna(axis = 0) #On supprime l'ensemble des lignes contenant un NaN car ce sont des dates où le logement n'est pas disponible
    cal['month'] = cal['date'].dt.strftime('%m')
    
    cal["price"]=cal["price"].replace('\,','',regex=True).astype(str)
    cal["price"]=cal["price"].replace('\$','',regex=True).astype(str)
    cal["price"]=pd.to_numeric(cal["price"])

    return(cal)

def clean_lis():
    """ Cette fonction permet de nettoyer la base de données listings, aucun attribut n'est attendu"""
    lis = pd.read_csv("./données/listings.csv")

    lis["price"]=lis["price"].replace('\,','',regex=True).astype(str)
    lis["price"]=lis["price"].replace('\$','',regex=True).astype(str)
    lis["price"]=pd.to_numeric(lis["price"])

    lis.drop(columns=['license'],inplace=True)
    lis.drop(columns=['scrape_id'],inplace=True)

    lis.amenities=lis.amenities.replace('\{','',regex=True).astype(str)
    lis.amenities=lis.amenities.replace('\}','',regex=True).astype(str)
    lis.amenities=lis.amenities.replace('\'','',regex=True).astype(str)
    lis.amenities=lis.amenities.replace('\"','',regex=True).astype(str)
    lis.amenities = lis.amenities.str.split(",")

    lis['review'] = lis['review_scores_rating'].fillna(0) #On remplit les review manquantes par des 0 
    lis["review"]=round(pd.to_numeric(lis.review, downcast='integer'),0)

    return(lis)