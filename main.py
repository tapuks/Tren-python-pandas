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
        self.numero_teorico_vueltas = 0
        self.distancia_origen_valiza1 = 0
        self.distancia_origen_valiza2 = 0
        self.distancia_paquete = 0
        self.longitud_seccion = 0
        self.lista_fecha_hora = []
        self.lista_solar_1 = []
        self.lista_solar_2 = []
        self.lista_solar_3 = []
        self.lista_record = []
        #self.lista_distancia_al_origen=[]
        self.lista_distancia_al_origen_round=[]
        self.lista_coordenadas_xr = []
        self.lista_coordenadas_yr = []
        self.df_resultados =[]
        self.error_RECR = 0
        self.baliza_real = 0


    def __str__(self):

        return f'Trabajamos con el paquete: {self.primeraValiza}.\n' \
               f'La primera valiza es: {self.primeraValiza} y tiene {self.vueltas_rueda_acum_valiza1} vueltas.' \
               f'\nLa segunda valiza es: {self.segundaValiza} y tiene {self.vueltas_rueda_acum_valiza2} vueltas.' \
               f'\nLa distancia del paquete es: {self.distancia_paquete}mm.' \
               f'\nEl numero de vueltas del paquete  es: {self.num_vueltas_paquete}.' \
               f'\nEl numero_teorico_vueltas entre dos valizas: {self.numero_teorico_vueltas}'\
               f'\nLa distancia al origen de valiza1 es: {self.distancia_origen_valiza1}' \
               f'\nLa distancia al origen de valiza2 es: {self.distancia_origen_valiza2}' \
               f'\nLa longitud de cada seccion es: {self.longitud_seccion} mm' \
               f'\nLas balizas reales que forman el paquete son baliza {self.primeraValiza} y {self.baliza_real}'

    def set_numero_vueltas_paquete(self):
        # Capturamos la fila de la Primera Valiza
        self.vueltas_rueda_acum_valiza1 = df_medicion.loc[df_medicion['Nº Valizas Acum'] == self.primeraValiza].iloc[0][
            'Acum. Vuelta rueda']
        # Capturamos la fila de la Segunda Valiza
        self.vueltas_rueda_acum_valiza2 = df_medicion.loc[df_medicion['Nº Valizas Acum'] == self.segundaValiza].iloc[0][
            'Acum. Vuelta rueda']
        self.num_vueltas_paquete = self.vueltas_rueda_acum_valiza2 - self.vueltas_rueda_acum_valiza1


    def set_distancia_paquete(self):
        self.distancia_origen_valiza1 = df_circuito.loc[df_circuito['Valizas Acum.'] == self.primeraValiza].iloc[0][
            'Distancia al origen']
        self.distancia_origen_valiza2 = df_circuito.loc[df_circuito['Valizas Acum.'] == self.segundaValiza].iloc[0][
            'Distancia al origen']
        self.distancia_paquete = self.distancia_origen_valiza2 - self.distancia_origen_valiza1


    def verificar_error_nvueltas(self):
        longitud_rueda = 37.699
        self.numero_teorico_vueltas = self.distancia_paquete / longitud_rueda

        # if ((ntv - self.num_vueltas_paquete)/ntv > 0.30)
        # error = (numero_teorico_vueltas - self.num_vueltas_paquete) / numero_teorico_vueltas
        error = ( abs(self.num_vueltas_paquete-self.numero_teorico_vueltas)/self.num_vueltas_paquete)*100

        if (error < 50):
            print("Todo es correcto, error del ", error, "%")
            self.baliza_real = self.segundaValiza

        else:
            print("MAL, error del ", error, "%")
            self.error_RECR += 1
            self.baliza_real = self.segundaValiza+1


    def set_longitud_seccion(self):
        self.longitud_seccion = self.distancia_paquete / self.num_vueltas_paquete

    def get_fecha_and_solars_and_record(self):
        for i in range(self.vueltas_rueda_acum_valiza1, self.vueltas_rueda_acum_valiza2 + 1):
            self.lista_fecha_hora.append(df_medicion.loc[df_medicion['Acum. Vuelta rueda'] == i].iloc[0][
                                        'Fecha'])
            self.lista_solar_1.append(df_medicion.loc[df_medicion['Acum. Vuelta rueda'] == i].iloc[0]['Solar1'])
            self.lista_solar_2.append(df_medicion.loc[df_medicion['Acum. Vuelta rueda'] == i].iloc[0]['Solar2'])
            self.lista_solar_3.append(df_medicion.loc[df_medicion['Acum. Vuelta rueda'] == i].iloc[0]['Solar3'])
            self.lista_record.append(df_medicion.loc[df_medicion['Acum. Vuelta rueda'] == i].iloc[0]['numero'])

    def get_distancia_al_origen(self):
        index = 0
        for i in range(self.vueltas_rueda_acum_valiza1, self.vueltas_rueda_acum_valiza2 + 1):
            if (index == 0):
                self.lista_distancia_al_origen.append(self.distancia_origen_valiza1)
            else:
                self.lista_distancia_al_origen.append(
                    round(self.lista_distancia_al_origen[index - 1] + self.longitud_seccion, 2))
            index = index + 1
        # REDONDEO DE LISTA_DISTANCIA_ORIGEN(SIN DECIMALES)
        for e in self.lista_distancia_al_origen:
            self.lista_distancia_al_origen_round.append(round(e))



    def new_dataframe_resultados(self):
        self.df_resultados = pd.DataFrame(
            {'Fecha y hora': self.lista_fecha_hora,'Record': self.lista_record, 'Red solar 1': self.lista_solar_1, 'Red solar 2': self.lista_solar_2, 'Red solar 3': self.lista_solar_3,
        'D.O': self.lista_distancia_al_origen_round})

    def get_coordenadas_xr_yr(self):
        cordenada_x_inicial=df_circuito.loc[df_circuito['Valizas Acum.'] == self.primeraValiza].iloc[0]['X']
        cordenada_y_inicial=df_circuito.loc[df_circuito['Valizas Acum.'] == self.primeraValiza].iloc[0]['Y']

        cordenada_x_final = df_circuito.loc[df_circuito['Valizas Acum.'] == self.segundaValiza].iloc[0]['X']
        cordenada_y_final = df_circuito.loc[df_circuito['Valizas Acum.'] == self.segundaValiza].iloc[0]['Y']

        print('cordenadaxinice', cordenada_x_inicial)
        print('cordenadayinici', cordenada_y_inicial)
        print('cordenadaXfinal', cordenada_x_final)
        print('cordenadayfinal', cordenada_y_final)

        for i in self.df_resultados.index:
            print(i)
            dc = self.df_resultados['D.O'][i]
            sen = 0
            cos = 1
            ce = dc * sen
            de = dc * cos
            print("dc", dc)
            print("ce", ce)
            print("de", de)
            xr = 0
            yr =0
            if (cordenada_x_inicial - cordenada_x_final) >0:
                xr = cordenada_x_inicial - de
            else:
                xr = cordenada_x_inicial + de
            if (cordenada_y_inicial - cordenada_y_final) >0:
                yr = cordenada_y_inicial - ce
            else:
                yr= cordenada_y_inicial + ce



            self.lista_coordenadas_xr.append(xr)
            self.lista_coordenadas_yr.append(yr)

        self.df_resultados['Xr'] = self.lista_coordenadas_xr
        self.df_resultados['Yr'] = self.lista_coordenadas_yr
        print(self.df_resultados)








    # def newdataFrame(self):
    #     # VARIABLES
    #     lista_vueltas_rueda = []
    #     lista_distancia_origen = []
    #     lista_distancia_origen_round = []
    #     index = 0
    #     i_anterior = 0
    #     lista_x_origen = []
    #     lista_y_origen = []
    #     lista_x_final = []
    #     lista_y_final = []
    #     lista_distancia_origen_inicio = []
    #     lista_distancia_origen_final = []
    #     lista_distancia_del_tramo = []
    #     lista_distancia_al_punto_origen_tramo = []
    #     # CALCULO VUELTAS ACUM-RUEDA Y DISTANCIA AL ORIGEN
    #     for i in range(self.vueltas_rueda_acum_valiza1, self.vueltas_rueda_acum_valiza2 + 1):
    #         lista_vueltas_rueda.append(i)
    #         if (index == 0):
    #             lista_distancia_origen.append(self.distancia_origen_valiza1)
    #         else:
    #
    #             lista_distancia_origen.append(
    #                 round(lista_distancia_origen[index - 1] + self.longitud_seccion, 2))
    #         index = index + 1
    #
    #     # REDONDEO DE LISTA_DISTANCIA_ORIGEN
    #     for e in lista_distancia_origen:
    #         lista_distancia_origen_round.append(round(e))
    #
    #     # CALCULO X-Y ORIGEN, X-Y FINAL, DISTANCIA-ORIGEN-INICIO E DISTANCIA-ORIGEN-FINAL
    #     for i in lista_distancia_origen_round:
    #         if i != i_anterior:
    #             # X-Y ORIGEN, DISTANCIA-ORIGEN-INICIO
    #             valores_menores = df_circuito[df_circuito['Distancia al origen'] <= i]
    #             valor_menor = valores_menores['Distancia al origen'].max()
    #             df_menor = df_circuito[df_circuito['Distancia al origen'] == valor_menor]
    #             x_origen = df_menor.iloc[0]['X']
    #             y_origen = df_menor.iloc[0]['Y']
    #             inicio_distancia_origen = df_menor.iloc[0]['Distancia al origen']
    #             lista_x_origen.append(round(x_origen))
    #             lista_y_origen.append(round(y_origen))
    #             lista_distancia_origen_inicio.append(round(inicio_distancia_origen))
    #
    #             # X-Y FINAL, DISTANCIA-ORIGEN-FINAL
    #             valores_mayores = df_circuito[df_circuito['Distancia al origen'] >= i]
    #             valor_mayor = valores_mayores['Distancia al origen'].min()
    #             df_mayor = df_circuito[df_circuito['Distancia al origen'] == valor_mayor]
    #             x_final = df_mayor.iloc[0]['X']
    #             y_final = df_mayor.iloc[0]['Y']
    #             final_distancia_origen = df_mayor.iloc[0]['Distancia al origen']
    #             lista_x_final.append(round(x_final))
    #             lista_y_final.append(round(y_final))
    #             lista_distancia_origen_final.append(round(final_distancia_origen))
    #
    #         i_anterior = i
    #
    #     # CREATE NEW DATAFRAME
    #     df = pd.DataFrame(
    #         {'Vueltas acum rueda': lista_vueltas_rueda, 'Distancia al origen': lista_distancia_origen_round,
    #          'X Origen': lista_x_origen, 'Y Origen': lista_y_origen, 'X Final': lista_x_final, 'Y Final': lista_y_final,
    #          'Distancia Origen Inicio': lista_distancia_origen_inicio,
    #          'Distancia Origen Final': lista_distancia_origen_final})
    #
    #     # DISTANCIA DEL TRAMO (PITAGORAS)
    #     for i in df.index:
    #         x = pow(df['X Origen'][i] - df['X Final'][i], 2)
    #         y = pow(df['Y Origen'][i] - df['Y Final'][i], 2)
    #         distancia_tramo = math.sqrt(x + y)
    #         lista_distancia_del_tramo.append(round(distancia_tramo))
    #     # ADD NEW COLUMN IN DATAFRAME
    #     df['Distancia del tramo']=lista_distancia_del_tramo
    #
    #
    #     # DISTANCIA AL PUNTO DE ORIGEN DEL TRAMO
    #     for i in df.index:
    #         lista_distancia_al_punto_origen_tramo.append(df['Distancia al origen'][i] - df['Distancia Origen Inicio'][i])
    #     # ADD NEW COLUMN IN DATAFRAME
    #     df['Distancia al punto de origen del tramo'] = lista_distancia_al_punto_origen_tramo
    #
    #     # COORDENADAS PUNTO X,Y
    #
    #     print(df_medicion)
    #
    #     print(df)







# ------------BLOQUE PRINCIPAL-----------------


# Lectura de ficheros
df_medicion = pd.read_table('data/CR800 LT directe_Table100930 0718.dat', sep=",", skiprows=4, header=None,
                            encoding='unicode_escape')
nombres_columna = ['Fecha', 'numero', 'Vol. Bat', 'Solar1', 'Solar2', 'Solar3', 'Vuelta rueda', 'Acum. Vuelta rueda','Nº Valizas','Nº Valizas Acum']
df_medicion.columns = nombres_columna

df_circuito = pd.read_csv('data/CCLT_100930_Mollerussa.csv', header=None)
nombres_columna = ['Registro', 'Via', 'X', 'Y', 'Valizas Acum.', 'Valiza', 'mm de via', 'Distancia al origen', '???']
df_circuito.columns = nombres_columna
valiza1 = int(input("Selección la valiza"))
# valiza2 = int(input("Selección de la segunda valiza"))
valiza2 = valiza1+1

tren1 = Tren(valiza1, valiza2)
tren1.set_numero_vueltas_paquete()
tren1.set_distancia_paquete()
tren1.verificar_error_nvueltas()
tren1.set_longitud_seccion()
print(tren1.__str__())
tren1.get_fecha_and_solars_and_record()
tren1.get_distancia_al_origen()

tren1.new_dataframe_resultados()

tren1.get_coordenadas_xr_yr()



# INSTANCIAMOS PAQUETES DEL 3 AL 5
# objs = list()
# for i in range(3):
#     objs.append(Tren(i+3, i+4))
#
# for obj in objs:
#     obj.set_numero_vueltas_paquete()
#     obj.set_distancia_paquete()
#     obj.verificar_error_nvueltas()
#     obj.set_longitud_seccion()
#     print(obj.__str__())
#     obj.get_fecha_and_solars_and_record()
#     obj.get_distancia_al_origen()
#     obj.new_dataframe_resultados()
#     obj.get_coordenadas_xr_yr()





