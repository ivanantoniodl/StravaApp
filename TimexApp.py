from lxml import etree
from xml.dom.minidom import Document
from datetime import datetime, date, time, timedelta
import calendar


documento = etree.parse('BaseCarrera.tcx')

print "Bienvenido a la App Timex X20 Run IronMan"

#Vamos a ingresar la hora de inicio de la actividad
datoingresado = raw_input('Ingrese la fecha de inicio actividad Formato: dd/mm/yyyy HH:mm:ss  ')
fecha = datetime.strptime(datoingresado, '%d/%m/%Y %H:%M:%S')
#Se suman 6 horas, pora el cambio de horario
fecha = fecha + + timedelta(seconds=21600)

fechabase = documento.find("Activities/Activity/Id")
fechabase.text = fecha.strftime('%Y-%m-%dT%H:%M:%SZ')

fechaatributo = documento.find("Activities/Activity")
fechaatributo[2].set("StartTime",fecha.strftime('%Y-%m-%dT%H:%M:%SZ'))



#Vamos a buscar la distancia total y vamos a sustituirla
print "Ingrese la Distancia Total metros"
metrostotales = input()
metrostotalesbase=documento.find("Activities/Activity/Lap/DistanceMeters")
metrostotalesbase.text = str(metrostotales)

#Vamos a buscar el tiempo total en segundos y vamos a sustituir
print "Ingrese el tiempo total en segundos"
segundostotales = input()
segundostotalesbase=documento.find("Activities/Activity/Lap/TotalTimeSeconds")
segundostotalesbase.text=str(segundostotales)

#Vamos a buscar las colorias y vamos a sustituir
print "Ingrese las calorias totales"
caloriastotales = input()
caloriastotalesbase=documento.find("Activities/Activity/Lap/Calories")
caloriastotalesbase.text=str(caloriastotales)

#---------Ya teniendo la base del documento, ahora vamos a crear Tracks
#Primero Leemos el Mapa
mapa = etree.parse('Mapa.tcx')




trackpoint = mapa.findall("Courses/Course/Track/Trackpoint")
Laps = input("No de Laps  ")
ContadorLaps=1
ContadorTracks=0
Distancia=0
fraccion=0.0
mili=0.0
metrosact=0.0
metrosant=0.0
metrosdif=0.0
tiempometros=0.0
tiempoquefalto=0
segundosgenerales=0
distanciasumada=0;

ListaTracks = []

FechaTrackPoint = fecha

for TracksPoints in trackpoint:
    #Se limpia el contador de Tracks para saber cuantos hay en cada Lap
    ContadorTracks=0;

    if(Distancia==0):
        Distancia = input("Ingrese Distancia del del Lap " + str(ContadorLaps) + "  ")

    Track = documento.find("Activities/Activity/Lap/Track")
    DistanciaMapa = float(TracksPoints.find('DistanceMeters').text)

    


    # Se va a pedir la informacion del cada Lap


    if DistanciaMapa<=(Distancia+15):
        ListaTracks.append(TracksPoints)
        metrosact=Distancia
        #print (len(ListaTracks))
    else:
        #Ingresamos el Tiempo del Lap terminado

        minutosingresado = raw_input('Ingrese el tiempo del Lap' + str(ContadorLaps) +  ' en HH:mm:ss    ')
        minutos = datetime.strptime(minutosingresado, '%H:%M:%S')
        #Ya con este tiempo, se va a tener fraccion, por cada TracPoints
        #fraccion = (int(minutos.strftime('%M'))*60 + int(minutos.strftime('%S')))/float(len(ListaTracks))
        #print fraccion
        #print (fraccion)

        #Primero se calcula los metros totales, para saber el total en segundos por metro
        #tiempometros=(int(minutos.strftime('%M'))*60 + int(minutos.strftime('%S')))/float(metrosact)
        if(distanciasumada==0):
            tiempometros=(int(minutos.strftime('%M'))*60 + int(minutos.strftime('%S')))/float(Distancia)
        else:
            tiempometros=(int(minutos.strftime('%M'))*60 + int(minutos.strftime('%S')))/float(Distancia  - distanciasumada)


        contLista=0;

        if(ContadorLaps==1):
            metrosant=0;
        else:
            metrosant= Distancia  - (Distancia - distanciasumada)


        segundosgenerales=0

        for Lista in ListaTracks:

            metrosact=float(Lista.find('DistanceMeters').text)

            fechanueva = Lista.find("Time")
            metrosdif = metrosact - metrosant

         

            #Se incrementa Fecha para poder aumentar tiempo
            FechaTrackPoint = FechaTrackPoint + timedelta(seconds=((metrosdif*tiempometros)+tiempoquefalto))


            segundosgenerales=segundosgenerales + (metrosdif*tiempometros)


            fechanueva.text = FechaTrackPoint.strftime('%Y-%m-%dT%H:%M:%S.%fZ')


            Track.append(Lista)
            #Se haya la diferencia de metros, para saber los segundos a incrementa

            metrosant=metrosact
            contLista=contLista+1
            tiempoquefalto=0;

        distanciasumada = Distancia

        tiempoquefalto=(int(minutos.strftime('%M'))*60 + int(minutos.strftime('%S'))) - segundosgenerales


        ContadorLaps=ContadorLaps+1
        ListaTracks = []
        ListaTracks.append(TracksPoints)
        Distancia=0;

        if(ContadorLaps>Laps):
            break

        #ContadorTracks= ContadorTracks + 1
        #print ContadorTracks;
        #Track.append(TracksPoints)




#Ya teniendo los Tracks Vamos a insertarlo dentro del otro documento


documento.write('BaseCarreraFinal.tcx')
