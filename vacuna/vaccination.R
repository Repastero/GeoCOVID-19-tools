# Autor: Pierino Martn Goette
# Datos obtenidos a través de:
# http://datos.salud.gob.ar/dataset/vacunas-contra-covid19-dosis-aplicadas-en-la-republica-argentina
# Instalamos los paquetes: Descomentar (Ctrl+c)
# install.packages("readr")
 
#install.packages("tibble")
#install.packages("tidyverse")
#install.packages("lubridate")
#install.packages("stringi")
#install.packages("forcats")

rm(list=ls())

require(readr)
require(tibble)
require(tidyverse)
require(lubridate)
require(forcats)
require(stringi)


##### LECTURA Y LIMPIEZA DE DATOS #####
# Para setear el directorio ir a:
# session -> Set Working Directory -> To sourse file location
# Recordar que el script y los datos deben estar en el mismo directorio
set.seed(1) 

vaccinationArg<-tibble(read.csv("datos_nomivac_covid19.csv", encoding="UTF-8"))

# Se descomenta de acuerdo a los datos de la provincia que se desea obtener

provincia<-("Entre R�os")
# provincia<-("La Rioja")
# provincia<-("Santa Fe")

vaccination<-vaccinationArg %>% filter(jurisdiccion_residencia==provincia)

# rm(vaccinationArg)
dateInitial='20200101'
vaccination <-vaccination[order(vaccination$fecha_aplicacion), ]
fechas=interval(ymd(dateInitial),ymd(vaccination$fecha_aplicacion))
vaccination$phase<-0;
vaccination$phase <- fechas %/% days(1)

#### Se agrupan de acuerdo a un porcentaje estimado a los grupos etarios que tenemos en cuenta en el modelo

transformRangeEtary<-function(x){
  # Estimamos que el 60% de 60-69 pertecenece al rango 41-65 y el 40% restante a 65+
  if(x["grupo_etario"]=="60-69"){
    if(runif(1)>0.6){
      x["grupo_etario"]<-"70-79"
    }
    else{
      x["grupo_etario"]<- "60-69"
    }
  }
  else{
    # Estimamos que el 50% de 18-29 pertecenece al rango 15-24 y el 50% restante 25-40
    if(x["grupo_etario"]=="18-29"){
      if(runif(1)>0.5){
        x["grupo_etario"]<-"30-39"
      }
    }
  }
  x["grupo_etario"]<-  x["grupo_etario"]
}

vaccination$grupo_etario <-apply(vaccination,1,transformRangeEtary)
vaccination$grupo_etario<-factor(vaccination$grupo_etario)
vaccination<-vaccination %>% mutate(grupo_etario = fct_recode(grupo_etario,
                                                              "5-15"  = "S.I.",
                                                              "16-24" = "18-29",
                                                              "25-40" = "30-39",
                                                              "41-64" = "40-49",
                                                              "41-64" = "50-59",
                                                              "41-64" = "60-69",
                                                              "65+" = "70-79",
                                                              "65+" = "80-89",
                                                              "65+" = "90-99",
                                                              "65+" = ">=100" ))

# Con los siguientes comandos se reordenan los niveles de los grupos etarios
vaccination$grupo_etario<-fct_relevel(vaccination$grupo_etario, "5-15", "16-24",  "25-40", "41-64", "65+")

# S.I. son sujetos sin identificación, como la proporción de personas es baja se utilizao como referencia para el el rango 5-15 años

##Separamos en las 2 dosis los datos

vaccinationDoseOne <- vaccination %>% 
                      filter(orden_dosis==1) %>%
                      select(phase,depto_residencia,grupo_etario, vacuna)

vaccinationDoseTwo <- vaccination %>% 
                      filter(orden_dosis==2) %>%
                      select(phase,depto_residencia,grupo_etario, vacuna)


# Crear un csv para modelar

datosAux<-as.data.frame(table(vaccinationDoseOne$phase,vaccinationDoseOne$depto_residencia ,vaccinationDoseOne$grupo_etario))
names(datosAux)<- c("phase","Departamento", "GrupoEtario", "Freq")
datosModeloDoseOne <- datosAux %>% pivot_wider(names_from = GrupoEtario, values_from = Freq) %>% tibble()

# Cantidad  de dosis por departamento estas linea debe completarse de acuerdo a la cantidad de agentes que se está representando según el departamento
# Entre Rios fuente: https://github.com/Repastero/GeoCOVID-19-tools/blob/master/datos/muertos%20er/reporte_epidem_16022021.ods
if(provincia=="Entre R�os"){
  poblacionPorDepartamento<- tibble(Departamento=unique(vaccination$depto_residencia), 
                                    porcentajePoblacionRepresentada=c(76.92,50.7,42.99,30.00,89.56,70.74,76.21,82.9,
                                                                      53.47,73.2,82.90,39.95,89.03,69.66,60.73,35.57,80.14,35.57))
}else
  { if(provincia=="Santa Fe"){
  # Santa fe
    ProporcionHabitantesCapital<-401544/525093*100
    poblacionSantaFe<- tibble(Departamento=unique(vacunacionStaFe$depto_residencia),
                            porcentajePoblacionRepresentada=c(ProporcionHabitantesCapital,100,100,100,100,100,100,100,
                                                              100,100,100,100,100,100,100,100,100,100,100,100,100,100))
    }else{
      # TODO en este caso no sé si la proporción de personas es la correcta La rioja
      if(provincia=="La Rioja"){
        ProporcionHabitantesCapital<-100
        poblacionSantaFe<- tibble(Departamento=unique(vacunacionStaFe$depto_residencia),
                                  porcentajePoblacionRepresentada=c(ProporcionHabitantesCapital,100,100,100,100,100,100,100,
                                                                    100,100,100,100,100,100,100,100,100,100,100,100,100,100))
      }
    }
}


# 
for(i in 1:nrow(poblacionPorDepartamento)){
  for(j in 1:nrow(datosModeloDoseOne)){
    if(poblacionPorDepartamento$Departamento[i]==datosModeloDoseOne$Departamento[j]){
      datosModeloDoseOne[j,(c(ncol(datosModeloDoseOne)-(length(levels(vaccinationDoseOne$grupo_etario))-1)):ncol(datosModeloDoseOne))]<-
        round(datosModeloDoseOne[j,(c(ncol(datosModeloDoseOne)-(length(levels(vaccinationDoseOne$grupo_etario))-1)):ncol(datosModeloDoseOne))]*poblacionPorDepartamento$porcentajePoblacionRepresentada[i]/100)
    }
  }
  
}


##Crear archivos de acuerdo a la ciudad
aux=1
for (i in 2:nrow(datosModeloDoseOne)) {
  if(datosModeloDoseOne$Departamento[i]!=datosModeloDoseOne$Departamento[i-1] || i==nrow(datosModeloDoseOne) ){
    datosCiudadDoseOne<- datosModeloDoseOne[aux:i-1,-2]
    nombre <- paste("vacunaDose1/",datosModeloDoseOne$Departamento[i-1],".csv")
    nombre<-gsub(" ","", tolower(stri_trans_general(nombre,"Latin-ASCII")))
    write_csv(datosCiudadDoseOne,file=nombre)
    aux=i+1
    }
}

# Segundas dosis 

datosAux<-as.data.frame(table(vaccinationDoseTwo$phase,vaccinationDoseTwo$depto_residencia ,vaccinationDoseTwo$grupo_etario))
names(datosAux)<- c("phase","Departamento", "GrupoEtario", "Freq")
datosModeloDoseTwo <- datosAux %>% pivot_wider(names_from = GrupoEtario, values_from = Freq) %>% tibble()

for(i in 1:nrow(poblacionPorDepartamento)){
  for(j in 1:nrow(datosModeloDoseTwo)){
    if(poblacionPorDepartamento$Departamento[i]==datosModeloDoseTwo$Departamento[j]){
      datosModeloDoseTwo[j,(c(ncol(datosModeloDoseTwo)-(length(levels(vaccinationDoseOne$grupo_etario))-1)):ncol(datosModeloDoseTwo))]<-round(datosModeloDoseTwo[j,(c(ncol(datosModeloDoseTwo)-(length(levels(vaccinationDoseOne$grupo_etario))-1)):ncol(datosModeloDoseTwo))]*poblacionPorDepartamento$porcentajePoblacionRepresentada[i]/100)
    }
  }
}

aux=1
for (i in 2:nrow(datosModeloDoseTwo)) {
  if(datosModeloDoseTwo$Departamento[i]!=datosModeloDoseTwo$Departamento[i-1] || i==nrow(datosModeloDoseTwo)-1 ){
    datosCiudadDoseTwo<- datosModeloDoseTwo[aux:i-1,-2]
    nombre <- paste("vacunaDose2/",datosModeloDoseTwo$Departamento[i-1],".csv")
    nombre<-gsub(" ","", tolower(stri_trans_general(nombre,"Latin-ASCII")))
    write_csv(datosCiudadDoseTwo,file=nombre)
    aux=i+1
  }
}

#### Datos cantidad de vacunas por rango etario####
# Para cambiar las variables 
# PROPORTION_OF_VACCINES_ONE_DOSE
# PROPORTION_OF_VACCINES_TWO_DOSE
table(vaccinationDoseOne$vacuna)/sum(table(vaccinationDoseOne$vacuna))*100 
table(vaccinationDoseTwo$vacuna)/sum(table(vaccinationDoseTwo$vacuna))*100 






