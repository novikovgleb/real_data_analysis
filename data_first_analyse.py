#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 08:51:53 2024

@author: gl.novikov
"""

import os
os.chdir("/Users/gl.novikov/Work/Scripts")

# Импорт необходимых библиотек
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype
#Создание ДатаФрейма
pth = '/Users/gl.novikov/Work/Data/googleplaystore.csv' # Путь относительно рабочего каталога
GOOGLE = pd.read_csv(pth)

#Удаление строк с пропущенными значениями
GOOGLE = GOOGLE.dropna()
GOOGLE = GOOGLE.reset_index()
del GOOGLE['index']

#Присвоение перменным Category, Type, Сontent Rating, Genres типа категория
GOOGLE['Category'] = GOOGLE['Category'].astype("category")
GOOGLE['Type'] = GOOGLE['Type'].astype("category")
GOOGLE['Content Rating'] = GOOGLE['Content Rating'].astype("category")
GOOGLE['Genres'] = GOOGLE['Genres'].astype("category")



#Обработка данных переменной Price: удаление неудачных случаев, переформатирование данных ввиде $4.99 -> 4.99 и преобразование к типу float
GOOGLE.drop(GOOGLE.loc[GOOGLE['Price'] == 'Everyone'].index, inplace=True)
GOOGLE = GOOGLE.reset_index()
del GOOGLE['index']
for i in range(len(GOOGLE)):
    if GOOGLE.loc[i,'Price'] != '0':
        GOOGLE.loc[i,'Price'] = GOOGLE.loc[i,'Price'][1:]
GOOGLE['Price'] = GOOGLE['Price'].astype("float64")

#Присвоение переменной Reviews типа категории
GOOGLE['Reviews'] = GOOGLE['Reviews'].astype("int64")

#Обработка данных переменной Size: удаление неудачных случаев, переформатирование данных ввиде 1.4M >1.4, преобразование к типу float
GOOGLE.drop(GOOGLE.loc[GOOGLE['Size'] == 'Varies with device'].index, inplace=True)
GOOGLE = GOOGLE.reset_index()
del GOOGLE['index']
for i in range(len(GOOGLE)):
    if GOOGLE.loc[i,'Size'][-1] == 'k':
        GOOGLE.loc[i,'Size'] = GOOGLE.loc[i,'Size'][:-1]
        GOOGLE.loc[i,'Size'] = round(float(GOOGLE.loc[i,'Size'])/1024,3)
    elif GOOGLE.loc[i,'Size'][-1] == 'M':
        GOOGLE.loc[i,'Size'] = float(GOOGLE.loc[i,'Size'][:-1])
GOOGLE['Size'] = GOOGLE['Size'].astype("float64")
#Обработка данных переменной Last Updated: преобразование данных ввиде 13 January,2018 -> 2018, присвоение типа категория
for i in range(len(GOOGLE)):
    tmp = GOOGLE.loc[i,'Last Updated'].split()
    GOOGLE.loc[i,'Last Updated'] = (tmp[0]+tmp[2])[-4:]   
GOOGLE['Last Updated'] = GOOGLE['Last Updated'].astype("category")

#Обратботка данных переменной Installs: сужение алфавита до 10 путем логичного преобразования данных, преобразование переменной к периодическому типу
for i in range(len(GOOGLE)):
    if GOOGLE.loc[i,'Installs'] == '1+':
        GOOGLE.loc[i,'Installs'] = '0+'
    elif GOOGLE.loc[i,'Installs'] == '10+':
        GOOGLE.loc[i,'Installs'] = '5+'
    elif GOOGLE.loc[i,'Installs'] == '100+':
        GOOGLE.loc[i,'Installs'] = '50+'
    elif GOOGLE.loc[i,'Installs'] == '1,000+':
        GOOGLE.loc[i,'Installs'] = '500+'
    elif GOOGLE.loc[i,'Installs'] == '10000+':
        GOOGLE.loc[i,'Installs'] = '5000+'
    elif GOOGLE.loc[i,'Installs'] == '1,000,000,000+':
        GOOGLE.loc[i,'Installs'] = '500,000,000+'        
    elif GOOGLE.loc[i,'Installs'] == '100,000+':
        GOOGLE.loc[i,'Installs'] = '50,000+'
    elif GOOGLE.loc[i,'Installs'] == '10,000+':
        GOOGLE.loc[i,'Installs'] = '5,000+'   
    elif GOOGLE.loc[i,'Installs'] == '1,000,000+':
        GOOGLE.loc[i,'Installs'] = '500,000+' 
    elif GOOGLE.loc[i,'Installs'] == '10,000,000+':
        GOOGLE.loc[i,'Installs'] = '5,000,000+' 
    elif GOOGLE.loc[i,'Installs'] == '100,000,000+':
        GOOGLE.loc[i,'Installs'] = '500,000,000+' 
list_of_installs  = sorted(list(set(GOOGLE['Installs'])),key=len)
list_of_installs[0],list_of_installs[1]=list_of_installs[1],list_of_installs[0]
installs_type = CategoricalDtype(categories=list_of_installs,ordered = True)
GOOGLE['Installs']= GOOGLE['Installs'].astype(installs_type)


#Обработка данных переменной Android Ver: удаление неудачных случаев, переформативоние данных ввиде v.4.0.2.1 and up -> v.4 and up, сужение алфавита до 10,  преобразование переменной к периодическому типу
GOOGLE.drop(GOOGLE.loc[GOOGLE['Android Ver'] == 'Varies with device'].index, inplace=True)
GOOGLE = GOOGLE.reset_index()
del GOOGLE['index']
for i in range(len(GOOGLE)):
    GOOGLE.loc[i,'Android Ver'] = 'v.'+str(GOOGLE.loc[i,'Android Ver'])[0]+' and up'     
set_of_android_version = list(set(GOOGLE['Android Ver']))
list_of_android_version = sorted(set_of_android_version)
android_type = CategoricalDtype(categories=list_of_android_version,ordered = True)
GOOGLE['Android Ver']= GOOGLE['Android Ver'].astype(android_type)

#Обработка данных переменной Current:удаление неудачных случаев,  переформативоние данных ввиде v.4.0.2-> v.4, сужение алфавита до 10,  преобразование переменной к периодическому типу
GOOGLE.drop(GOOGLE.loc[GOOGLE['Current Ver'] == 'Varies with device'].index, inplace=True)
GOOGLE = GOOGLE.reset_index()
del GOOGLE['index']
for i in range(len(GOOGLE)):
    GOOGLE.loc[i,'Current Ver'] = str(GOOGLE.loc[i,'Current Ver'])[0]

GOOGLE.drop(GOOGLE.loc[GOOGLE['Current Ver'].str.isalpha()].index, inplace=True)
GOOGLE = GOOGLE.reset_index()
del GOOGLE['index']

for i in range(len(GOOGLE)):
    GOOGLE.loc[i,'Current Ver'] = 'v.' + str(GOOGLE.loc[i,'Current Ver'])[0]

set_of_current_version = list(set(GOOGLE['Current Ver']))
list_of_current_version = sorted(set_of_current_version)
android_cur = CategoricalDtype(categories=list_of_current_version,ordered = True)
GOOGLE['Current Ver']= GOOGLE['Current Ver'].astype(android_cur) 

# ********************** Числовой анализ *************************
# Количественный анализ количественных переменных.
GOOG = GOOGLE.select_dtypes(include=['float','int'])
# Описательная статистика всех переменных
GOOGLE_STAT = GOOG.describe()
# Медиана для всех переменных
GOOGLE_med = GOOG.median() # Получается pandas.Series
# Межквартильный размах для всех переменных
# Вычисляется по определению
GOOGLE_iqr = GOOG.quantile(q=0.75) - GOOG.quantile(q=0.25) # Получается pandas.Series
# Создаем pandas.DataFrame из новых статистик
#W = pd.DataFrame([CA_med, CA_iqr], index=['median', 'IQR'])
W = pd.DataFrame([GOOGLE_iqr], index=['IQR'])
# Объединяем CA_STAT и W
GOOGLE_STAT = pd.concat([GOOGLE_STAT, W])
import scipy as sp
# Outliers
std = np.std(GOOGLE['Price'])
mean = np.mean(GOOGLE['Price'])
sel_out = np.abs(GOOGLE['Price'] - mean) > 3*std
GOOGLE_OUT = GOOGLE.loc[sel_out, :]
# std = k*MAD, k=1.48... fof N()
mad = sp.stats.median_abs_deviation(GOOGLE['Price'])
tr_mean = sp.stats.trim_mean(proportiontocut=0.1, a = GOOGLE['Price'])
"""
dir(CB)
help(CB.xs)
CB.dtypes
"""




