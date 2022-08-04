El programa consta de un unico script que descarga distintos  datasets del BCRA, los guarda en formato csv y obtiene diversos analisis finacieros y gráficos, se actualiza al ejecutar con la opcion "descargar dataset"

 API BCRA
Enlace de la página: https://estadisticasbcra.com/  
Documentación: https://estadisticasbcra.com/api/documentacion

El usuario debe ingresar los siguientes datos:
1- Período de tiempo en dias (default: 365)
2- Grado de la regresion lineal=1, polinomica=2
3- Fecha de prediccion futura (default: hoy)
4 -Descargar datasets (obligatorio la primera vez) 


------ 
fecha de máxima brecha: 2022-07-22 00:00:00, Variac. brecha %: 160.48
cotizacion oficial: 129.76, cotizac. blue: 338.0
------ 

 Dia de la semana donde ocurren mayores variaciones de brecha: Wednesday


 Cinco dias maxima volatilidad:
       Fecha   Dolar oficial  Dolar blue  Variacion brecha %  Volatilidad %
0 2022-07-21          129.61       337.0          160.010802      17.694994
1 2022-07-22          129.76       338.0          160.480888      15.260017
2 2022-07-20          129.39       317.0          144.995749      13.518353
3 2022-07-04          125.99       260.0          106.365585      12.472963
4 2022-07-08          126.78       273.0          115.333649      11.656442 

Prediccion valor futuro del dolar oficial en pesos
 prediccion 3 meses: 152
 prediccion 6 meses: 177
 prediccion 12 meses: 242

Prediccion valor futuro del dolar blue en pesos
 prediccion 3 meses: 336
 prediccion 6 meses: 418
 prediccion 12 meses: 637

                            
![image](https://github.com/horaciogit/Proyecto-Individual-Henry/blob/main/images/Dolar%20oficial-blue.png)
![image](https://github.com/horaciogit/Proyecto-Individual/blob/main/images/Variacion%20brecha-volatilidad.png)
![image](https://github.com/horaciogit/Proyecto-Individual/blob/main/images/cotizacion%20dolar%20blue.png)
![image](https://github.com/horaciogit/Proyecto-Individual/blob/main/images/cotizacion%20dolar%20oficial.png)
![image](https://github.com/horaciogit/Proyecto-Individual-Henry/blob/main/images/regresion%20lineal%20dolar%20blue.png)
![image](https://github.com/horaciogit/Proyecto-Individual-Henry/blob/main/images/regresion%20lineal%20dolar%20oficial.png)
![image](https://github.com/horaciogit/Proyecto-Individual-Henry/blob/main/images/Eventos%20gobierno%20vs%20precio%20dolar.png)
![image](https://github.com/horaciogit/Proyecto-Individual-Henry/blob/main/images/salida-consola.png)

