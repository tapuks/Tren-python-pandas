import math

import pandas as pd
import numpy as np


class Tren:
    def __init__(self, primeraValiza, segundaValiza):
        self.primeraValiza = primeraValiza
        self.segundaValiza = segundaValiza
        self.vueltas_rueda_acum_valiza1 = 0
        self.vueltas_rueda_acum_valiza2 = 0
        self.num_vueltas_paquete = 0
        self.distancia_origen_valiza1 = 0
        self.distancia_origen_valiza2 = 0
        self.distancia_paquete = 0
        self.distancia_media_recorrida_vuelta_rueda = 0

    def __str__(self):
        return f'La primera valiza es: {self.primeraValiza} y tiene {self.vueltas_rueda_acum_valiza1} vueltas.' \
               f'\nLa segunda valiza es: {self.segundaValiza} y tiene {self.vueltas_rueda_acum_valiza2} vueltas.' \
               f'\nEl numero de vueltas del paquete es: {self.num_vueltas_paquete}.' \
               f'\nLa distancia al origen de valiza1 es: {self.distancia_origen_valiza1}' \
               f'\nLa distancia al origen de valiza2 es: {self.distancia_origen_valiza2}' \
               f'\nLa distancia del paquete es: {self.distancia_paquete}mm.' \
               f'\nLa distancia media recorrida por cada vuelta de rueda es: {self.distancia_media_recorrida_vuelta_rueda} mm'

    def set_numero_vueltas_paquete(self):
        # Capturamos la fila de la Primera Valiza
        self.vueltas_rueda_acum_valiza1 = df_medicion.loc[df_medicion['Nº Valizas Acum'] == self.primeraValiza].iloc[0][
            'Acum. Vuelta rueda']
        # Capturamos la fila de la Segunda Valiza
        self.vueltas_rueda_acum_valiza2 = df_medicion.loc[df_medicion['Nº Valizas Acum'] == self.segundaValiza].iloc[0][
            'Acum. Vuelta rueda']
        self.num_vueltas_paquete = self.vueltas_rueda_acum_valiza2 - self.vueltas_rueda_acum_valiza1
        print('NVP: ', self.num_vueltas_paquete)

    def set_distancia_paquete(self):
        self.distancia_origen_valiza1 = df_circuito.loc[df_circuito['Valizas Acum.'] == self.primeraValiza].iloc[0][
            'Distancia al origen']
        self.distancia_origen_valiza2 = df_circuito.loc[df_circuito['Valizas Acum.'] == self.segundaValiza].iloc[0][
            'Distancia al origen']
        self.distancia_paquete = self.distancia_origen_valiza2 - self.distancia_origen_valiza1

    def verificar_error_nvueltas(self):
        longitud_rueda = 37.699
        numero_teorico_vueltas = self.distancia_paquete / longitud_rueda
        print('numero_teorico_vueltas', numero_teorico_vueltas)
        # if ((ntv - self.num_vueltas_paquete)/ntv > 0.30)
        error = (numero_teorico_vueltas - self.num_vueltas_paquete) / numero_teorico_vueltas
        if (error < 0.30):
            print("Todo es correcto, error del ", error)
        else:
            print("MAL, error del ", error)

    def set_distancia_media_recorrida_vuelta_rueda(self):
        self.distancia_media_recorrida_vuelta_rueda = self.distancia_paquete / self.num_vueltas_paquete

    def newdataFrame(self):
        # VARIABLES
        lista_vueltas_rueda = []
        lista_distancia_origen = []
        lista_distancia_origen_round = []
        index = 0
        i_anterior = 0
        lista_x_origen = []
        lista_y_origen = []
        lista_x_final = []
        lista_y_final = []
        lista_distancia_origen_inicio = []
        lista_distancia_origen_final = []
        lista_distancia_del_tramo = []
        lista_distancia_al_punto_origen_tramo = []
        # CALCULO VUELTAS ACUM-RUEDA Y DISTANCIA AL ORIGEN
        for i in range(self.vueltas_rueda_acum_valiza1, self.vueltas_rueda_acum_valiza2 + 1):
            lista_vueltas_rueda.append(i)
            if (index == 0):
                lista_distancia_origen.append(self.distancia_origen_valiza1)
            else:

                lista_distancia_origen.append(
                    round(lista_distancia_origen[index - 1] + self.distancia_media_recorrida_vuelta_rueda, 2))
            index = index + 1

        # REDONDEO DE LISTA_DISTANCIA_ORIGEN
        for e in lista_distancia_origen:
            lista_distancia_origen_round.append(round(e))

        # CALCULO X-Y ORIGEN, X-Y FINAL, DISTANCIA-ORIGEN-INICIO E DISTANCIA-ORIGEN-FINAL
        for i in lista_distancia_origen_round:
            if i != i_anterior:
                # X-Y ORIGEN, DISTANCIA-ORIGEN-INICIO
                valores_menores = df_circuito[df_circuito['Distancia al origen'] <= i]
                valor_menor = valores_menores['Distancia al origen'].max()
                df_menor = df_circuito[df_circuito['Distancia al origen'] == valor_menor]
                x_origen = df_menor.iloc[0]['X']
                y_origen = df_menor.iloc[0]['Y']
                inicio_distancia_origen = df_menor.iloc[0]['Distancia al origen']
                lista_x_origen.append(round(x_origen))
                lista_y_origen.append(round(y_origen))
                lista_distancia_origen_inicio.append(round(inicio_distancia_origen))

                # X-Y FINAL, DISTANCIA-ORIGEN-FINAL
                valores_mayores = df_circuito[df_circuito['Distancia al origen'] >= i]
                valor_mayor = valores_mayores['Distancia al origen'].min()
                df_mayor = df_circuito[df_circuito['Distancia al origen'] == valor_mayor]
                x_final = df_mayor.iloc[0]['X']
                y_final = df_mayor.iloc[0]['Y']
                final_distancia_origen = df_mayor.iloc[0]['Distancia al origen']
                lista_x_final.append(round(x_final))
                lista_y_final.append(round(y_final))
                lista_distancia_origen_final.append(round(final_distancia_origen))

            i_anterior = i

        # CREATE NEW DATAFRAME
        df = pd.DataFrame(
            {'Vueltas acum rueda': lista_vueltas_rueda, 'Distancia al origen': lista_distancia_origen_round,
             'X Origen': lista_x_origen, 'Y Origen': lista_y_origen, 'X Final': lista_x_final, 'Y Final': lista_y_final,
             'Distancia Origen Inicio': lista_distancia_origen_inicio,
             'Distancia Origen Final': lista_distancia_origen_final})

        # DISTANCIA DEL TRAMO (PITAGORAS)
        for i in df.index:
            x = pow(df['X Origen'][i] - df['X Final'][i], 2)
            y = pow(df['Y Origen'][i] - df['Y Final'][i], 2)
            distancia_tramo = math.sqrt(x + y)
            lista_distancia_del_tramo.append(round(distancia_tramo))
        # ADD NEW COLUMN IN DATAFRAME
        df['Distancia del tramo']=lista_distancia_del_tramo


        # DISTANCIA AL PUNTO DE ORIGEN DEL TRAMO
        for i in df.index:
            lista_distancia_al_punto_origen_tramo.append(df['Distancia al origen'][i] - df['Distancia Origen Inicio'][i])
        # ADD NEW COLUMN IN DATAFRAME
        df['Distancia al punto de origen del tramo'] = lista_distancia_al_punto_origen_tramo

        # COORDENADAS PUNTO X,Y


        print(df)







# ------------BLOQUE PRINCIPAL-----------------


# Lectura de ficheros
df_medicion = pd.read_table('data/CR800 LT directe_Table100930 0718.dat', sep=",", skiprows=4, header=None,
                            encoding='unicode_escape')
nombres_columna = ['Fecha', 'numero', 'Vol. Bat', 'Solar1', 'Solar2', 'Solar3', 'Vuelta rueda', 'Acum. Vuelta rueda','Nº Valizas','Nº Valizas Acum']
df_medicion.columns = nombres_columna

df_circuito = pd.read_csv('data/CCLT_100930_Mollerussa.csv', header=None)
nombres_columna = ['Registro', 'Via', 'X', 'Y', 'Valizas Acum.', 'Valiza', 'mm de via', 'Distancia al origen', '???']
df_circuito.columns = nombres_columna

valiza1 = int(input("Selección de la primera valiza"))
valiza2 = int(input("Selección de la segunda valiza"))

tren1 = Tren(valiza1, valiza2)
tren1.set_numero_vueltas_paquete()
tren1.set_distancia_paquete()
tren1.verificar_error_nvueltas()
tren1.set_distancia_media_recorrida_vuelta_rueda()
print(tren1.__str__())
tren1.newdataFrame()

