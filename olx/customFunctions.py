import numpy as np
import re 
import requests
from unidecode import unidecode
import pandas as pd


class HomeMadeStats:
    
    def __init__(self, dataframe):
        """Instancia um conjunto de dados atribuindo os respectivos quartis e intervalo interquartil"""
        self.data = dataframe
        self.Q1 = self.data.quantile(0.25)
        self.Q2 = self.data.quantile(0.5)
        self.Q3 = self.data.quantile(0.75)
        self.IQ = self.Q3 - self.Q1
        
    def outliers(self):
        """retorna uma tupla com os valores limítrofes que definem um outlier"""
        outlier_i = self.Q1 - (1.5 * self.IQ)
        outlier_f = self.Q3 + (1.5 * self.IQ)
        return({
            'min':outlier_i,
            'max': outlier_f
        })
    
    
    
def CEPconditionals(row):
    out ="CEP NÃO CADASTRADO"
    if row is not None:
        if (len(row) == 6) | (len(row) ==9):
            out = row[:-1]
        elif (len(row)==7) | (len(row)==10):
            out= row[:-2]
        else:
            pass
    else:
        pass
    return out
     
    
def prettyCEP(dataframe, column_cep, column_result):
    """Formata o campo de CEP"""
    #no_cep = dataframe[column_cep].isnull()
    dataframe[column_result] = dataframe[column_cep].apply(lambda x: ( "0" + re.sub("\D", "", x) ) if pd.isnull(x) == False else None)
    dataframe[column_result] = dataframe[column_result].map(CEPconditionals)
    #dataframe[column_result] = dataframe[column_result].map(lambda x : x[:5]+"-"+x[5:])
    return dataframe.copy()


def PreparaCEP(row):
    """ Exclui o tipo de endereço. Rua, Aveninda, etc.."""
    row[0] = unidecode(row[0].upper())
    row[1] = unidecode(row[1].upper())
    try:
        new = row[1].replace(row[0],"")
    except:
        pass
    return new



def comparaCEP(row):
    if (row[0] is None) | (row[1] is None):
        return None
    elif row[0] == row[1]:
        return True
    else:
        return False

    