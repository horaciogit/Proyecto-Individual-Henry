#proyecto 1
import pandas as pd
import numpy as np
import talib as ta                # !pip install talib-binary
import matplotlib.pylab as plt
from matplotlib.pyplot import figure
import sys
import requests as req
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

#editar variables globales
#grado  1-regresion lineal  2-polinomica,  periodo en dias, fecha formato YY-MM-DD
grado=2
periodo=365
inputfecha= '2022-9-30'


urls={
      'usd_oficial' : 'https://api.estadisticasbcra.com/usd_of',
      'usd_blue' : 'https://api.estadisticasbcra.com/usd',
      'var_usd_vs_usd_of' :'https://api.estadisticasbcra.com/var_usd_vs_usd_of',
      'inflación_mensual' : 'https://api.estadisticasbcra.com/inflacion_mensual_oficial',
      'leliq_usd':  'https://api.estadisticasbcra.com/leliq_usd' ,
      'CER' :  'https://api.estadisticasbcra.com/cer',
      'milestones':'https://api.estadisticasbcra.com/milestones'
      }

my_headers = {'Authorization' : 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTExMjI2NTIsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJjaWVuc2lhbm8zNkBob3RtYWlsLmNvbSJ9.hcxJOJt094r9qiZz6V85w7jB_IRFO18aTxDg1J6wI8nHWV84oXp2OyNBFeiMddJrbErEq5wFd4ZVVHyMHPUK5g'}
#my_headers = {'Authorization' : 'BEARER eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTA4OTYzMzEsInR5cGUiOiJleHRlcm5hbCIsInVzZXIiOiJvbm9mcmVfcmV5QGhvdG1haWwuY29tIn0._R78Uq40P1S6KmEsxYYanInAEh3F9R39Ln3vjpDqC88pk0o_ArvwvZXE_qT4n5ngvnNmwrLTqABPKL_O_MvcuQ'}



def end_point (u):
   
    response = req.get (u,  headers=my_headers )
    if response.status_code == 200:
    
        data = response.json()
        data = pd.json_normalize(data)
        return data
    else: 
        print(response.status_code)
        sys.exit()
   

#var_usd = end_point(urls['var_usd_vs_usd_of'])
#inflación_mensual = end_point(urls['inflación_mensual'])
#leliq_usd = end_point(urls['leliq_usd'])


df_usd_oficial = end_point(urls['usd_oficial'])
df_usd_blue = end_point(urls['usd_blue'])
df_milestones = end_point(urls['milestones'])
#df_inflación_mensual = end_point(urls['inflación_mensual'])   
df_CER = end_point(urls['CER'])

    
df_usd_oficial.to_csv('usd_oficial.csv', index=False)
df_usd_blue.to_csv('usd_blue.csv',  index=False)
df_milestones.to_csv('milestones.csv', index=False)
df_CER.to_csv('CER.csv',  index=False)

#FIN CONSULTA API



usd_oficial= pd.read_csv('usd_oficial.csv')
usd_blue= pd.read_csv('usd_blue.csv')
milestones = pd.read_csv('milestones.csv')
CER = pd.read_csv('CER.csv')

  
dolars=  pd.merge(usd_oficial, usd_blue, on='d')
dolars_1 = pd.merge(dolars, milestones, on='d'  )

dolars['d'] = pd.to_datetime(dolars['d'], format='%Y-%m-%d')
dolars= dolars[dolars.d > datetime.now() - timedelta(days=periodo) ]
dolars.reset_index(inplace=True, drop=True)

dolars['VarBrecha'] = dolars.apply(lambda x:( x['v_y'] / x['v_x'] -1 )*100 , axis=1)

 #--------fila de la maxima variacion brecha------
fecha_max= dolars.iloc[dolars.VarBrecha.idxmax(), :]  
print('------ ')
print(f'fecha de máxima brecha: {fecha_max[0]}, Variac. brecha %: {round(fecha_max[3], 2)}')
print(f'cotizacion oficial: {fecha_max[1]}, cotizac. blue: {fecha_max[2]}')
print('------ \n')


#------------agregar columna dia de la semana 
dolars['day_name'] =dolars.apply(lambda x: x['d'].day_name(), axis = 1)

#dia de la semana con mayor variacion en la brecha
dias_semana =dolars.groupby(['day_name']).mean()
dia_semana_max_brecha= dias_semana.VarBrecha.idxmax()
print()
print(f' dia de la semana donde ocurren mayores variaciones de brecha: {dia_semana_max_brecha}' )
print('\n')


#-------agregar columnoa SMA (media movil simple) y volatilidad
dolars['SMA'] = ta.SMA(dolars.v_y, 12) #agregar media movil simple, periodo 12 dias
dolars['Volatil'] = dolars.apply(lambda x:( x['v_y'] / x['SMA'] -1)*100 , axis = 1)


#-----agregar columna datetime
dolars['datetime'] =  pd.to_datetime(dolars['d'], format='%Y-%m-%d')
dates = dolars.datetime.values

#-----agregar columna index
dolars['newindex'] = dolars.index


#obtener los 5 dias de maxima volatilidad 
df_volatil = dolars[['d', 'v_x', 'v_y', 'VarBrecha' , 'Volatil' ] ]
df_2 =df_volatil.sort_values(by=['Volatil'], ascending=False, )

df_2= df_2.iloc[0:5, :]
df_2 = df_2.rename(columns={'d': 'Fecha', 'v_x':' Dolar oficial', 'v_y':'Dolar blue',
                     'VarBrecha':'Variacion brecha %', 'Volatil':'Volatilidad %'}     )
df_2.reset_index(drop=True, inplace=True)
print(f' 5 dias maxima volatilidad:\n{ df_2} \n'   )

#------------agregar CER
CER['d'] = pd.to_datetime(CER['d'], format='%Y-%m-%d')
CER= CER[CER.d > datetime.now() - timedelta(days=periodo) ]

dolarsCER = pd.merge(dolars, CER, on= 'd')

#---------datos relevantes----
print('Ultimos datos relevantes:')
print(f'  Ultimo precio dolar oficial fecha {dolarsCER.iloc[-1, 0]} : ${dolarsCER.iloc[-1, 1] }')
print(f'  Ultimo precio dolar oficial fecha {dolarsCER.iloc[-1, 0]} : ${dolarsCER.iloc[-1, 2] }')
inflacion_periodo= (dolarsCER.iloc[-1, 9]/dolarsCER.iloc[0, 9]-1)*100
print(f'  Inflación acumulada periodo {periodo} dias: {round(inflacion_periodo,2)} %')
print('')

#----------------graficas

fig, ax = plt.subplots(figsize=(20, 10))

ax.set_xlabel('fecha',   fontsize=16)
ax.set_ylabel('cotizacion pesos ARS ', fontsize=16)
ax.set_title('Dolar oficial - dolar blue - CER',  fontsize=14, fontweight='bold')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=15)) 
ax.plot(dates,  dolars.v_x,     label='dolar oficial $', linewidth=2 )
ax.plot(dates, dolars.v_y, label='dolar blue $', color='red')
ax.plot(dates, dolarsCER.v, label= 'CER', color='black' , linewidth=2 )
ax.plot(dates, dolars.SMA,  label='media movil blue', color='green'  )

ax.grid(True)

ax.tick_params( labelrotation=45)
ax.legend(loc='upper center', fontsize='x-large');
plt.savefig('Dolar oficial-blue.png')
plt.show()

#--- grafico  brecha volatilidad
fig, ax1 = plt.subplots(figsize=(20, 10))

ax1.set_xlabel('fecha',   fontsize=16)
ax1.set_ylabel('variacion porcentual ', fontsize=16)
ax1.set_title('Variacion brecha-volatilidad ',  fontsize=14, fontweight='bold')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=15)) 

ax1.plot(dates, dolars.VarBrecha,  label='Variacion brecha', color='black' )
ax1.plot(dates, dolars.Volatil,  label='volatilidad', color='brown' )

ax1.grid(True)

ax1.tick_params( labelrotation=45)
ax1.legend(loc='upper center', fontsize='x-large');
plt.savefig('Variacion brecha-volatilidad.png')
plt.show()

#---------eventos gobierno-----
dolars_1 = dolars_1.rename(columns={'e': 'Evento', 'v_x':'precio dolar oficial', 'v_y':'precio dolar blue' } )
dolars_1.plot(kind = 'bar', x = 'Evento', y=['precio dolar oficial', 'precio dolar blue'  ], logy=False, figsize=(18, 10))
plt.savefig('Eventos gobierno vs precio dolar')
plt.show()




def regressor_plots(money):
    if money == 'oficial':
        y= dolars.v_x.values      #dolar oficial
        #grado=2
        pltText1=115
        pltText2=120
        title='dolar oficial'
    elif money == 'blue':
        y= dolars.v_y.values   #dolar blue
        pltText1=280
        pltText2=290
        title='dolar blue'
    else : return None    
        
    X= dolars.newindex.values.reshape(-1,1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    
    #-------------Polynomial regression
    pr =  PolynomialFeatures(degree=grado)   
    X_train_pol = pr.fit_transform(X_train)
    lr2 = LinearRegression()
    lr2.fit(X_train_pol, y_train)
    
    y_train_pred = lr2.predict(X_train_pol)
    y_test_pred = lr2.predict (pr.fit_transform(X_test) )           
    y_pred = lr2.predict (pr.fit_transform(X) )  
    
    
    
    R2_train_error = r2_score(y_train, y_train_pred)
    R2_test_error = r2_score(y_test, y_test_pred)
    R2_full_error= r2_score(y, y_pred)
    
    #-----graficos------------
    figure(figsize=(16, 8), dpi=80)
    plt.title('regresion lineal' + title, fontsize=18)
    
    r2err_train = 'r2  train=' + str(round (R2_train_error, 4))
    r2err_test = 'r2_test = ' + str(round (R2_test_error, 4))
    plt.text(0, pltText1,  r2err_train, fontsize=16)
    plt.text(0, pltText2,  r2err_test, fontsize=16)
    plt.xlabel("ruedas mercado", fontsize=16)
    plt.ylabel("cotizacion en pesos", fontsize=16)
    plt.scatter(X_train, y_train, label='train')
    plt.scatter(X_train, y_train_pred, color='red')
    
    plt.savefig('regresion lineal ' + title)
    plt.show()
    
    
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    ax.set_xlabel('fecha',   fontsize=16)
    ax.set_ylabel('cotizacion ', fontsize=16)
    ax.set_title('serie tiempo '+ title,  fontsize=16, fontweight='bold')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=15)) 
    ax.scatter(dates,  y,     label='real', linewidth=2 )
    ax.plot(dates, y_pred, label='predicción', color='red')
    ax.grid(True)
    
    ax.tick_params( labelrotation=45)
    ax.legend(loc='upper center', fontsize='x-large');
    plt.savefig('cotizacion ' +title)
    plt.show()
    
    
    d3meses = dolars.iloc[-1, 8] * 1.25
    d6meses = dolars.iloc[-1, 8] * 1.5
    d12meses =dolars.iloc[-1, 8] *2
    
    predict_3meses= int(lr2.predict (pr.fit_transform([[d3meses]]))[0])
    predict_6meses= int(lr2.predict (pr.fit_transform([[d6meses]]))[0])
    predict_12meses= int(lr2.predict (pr.fit_transform([[d12meses]]))[0])
    
    print (f'Prediccion valor futuro del dolar {money} en pesos')
    print( f' prediccion 3 meses: {predict_3meses}')
    print( f' prediccion 6 meses: {predict_6meses}')                
    print( f' prediccion 12 meses: {predict_12meses}')
    print()
    
    inputfecha_2 = datetime.strptime(inputfecha, '%Y-%m-%d')
    dias = (inputfecha_2 - dolars.iloc[0, 7]).days
    dias_mercado= int(dias/7*5)

    valor_pred = lr2.predict (pr.fit_transform([[dias_mercado]]))[0]  
    
    print(f' valor calculado para {inputfecha} {money}: $ {int(valor_pred)} \n')
    
   
    
    return
                    

regressor_plots('oficial')
regressor_plots('blue')


sys.exit()



