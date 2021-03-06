from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.style.use('seaborn')

# ============================ JUNTAMOS LOS TRES MODELOS ===================================

# ============================== VARIABLES INICIALES =======================================
N =  8_000_000                # Población total
N_trabajadores =  N * 0.013  #para SEIR trabajadores
camas_hospital = N / 4000          #para hospital
camas_icu = N /12000          #para hospital

# Inicialización de valores iniciales poblacionales

I0 = 1
E0 = 0
S0 = N - I0
R0 = 0
M0 = 0

Y0_p = (S0, E0, I0, R0, M0)

CE = 1.5                    #valor usado por profesor
fraccion_muertos = 0.116    #dato obtenido de la tasa de mortalidad del covid-19
tiempo_recuperacion = 9     #duracion de la infeccion
f = 14                      #tiempo en que un individuo pasa de latente a infeccioso

#Valores iniciales para modelo trabajadores
I0_trabajadores = 1
E0_trabajadores = 0
S0_trabajadores = N_trabajadores - I0_trabajadores
R0_trabajadores = 0
M0_trabajadores = 0

Y0_t = (S0_trabajadores, E0_trabajadores, I0_trabajadores, R0_trabajadores, M0_trabajadores)

multiplicador_contacto = 3  

pacientes_trabajador = 9            #9 pacientes por trabajador
infectados_hospital = 0.15           #Fracción de infectados que deben ser hospitalizados

fracc_muertes_espera = 0.15         #Fracción de personas que mueren en espera
fracc_recuperacion_espera = 0.05    #Fracción de personas que se recuperan en espera
fraccion_icu = 0.33                  #Fracción de hospitalizados que deben ser trasladados a icu
tiempo_estadia = 12                  #Tiempo de hospitalización
fracc_muertes_icu = 0.3             #Fracción de muertes de personas en icu
tiempo_estadia_icu = 3              #Tiempo de estadia en icu
fracc_muertes_hosp = 0.12           #Fracción de muertes de individuos hospitalizados

#Valores iniciales para el sistema hospitalario
espera = 0
hospitalizados = 0
icu = 0

Y0_h = (espera, hospitalizados, icu)

Y0 = (S0, E0, I0, R0, M0, S0_trabajadores, E0_trabajadores, I0_trabajadores, R0_trabajadores, M0_trabajadores, espera, hospitalizados, icu)

def complete_model(t, y):
    # ====== SEIR POBLACIONAL ==============================, ================== SEIR TRABAJADORES =============================, ======= HOSPITAL ===========
    susceptibles, latentes, infectados, recuperados, muertos, susceptibles_t, latentes_t, infectados_t, recuperados_t, muertos_t,  espera, hospitalizados, icu = y
    global camas_hospital, camas_icu

    # ========= SEIR POBLACIONAL ================
    β = CE / N
    λ = β * infectados

    # Flujos
    ER = susceptibles * λ                   #flujo latentes
    IR =  latentes / f                      #flujo infectados
    MR = infectados * fraccion_muertos      #flujo muertos
    RR = infectados / tiempo_recuperacion   #flujo recuperados


    # ========= SEIR TRABAJADORES ================
    β_t = CE / N_trabajadores
    λ_t = β_t * infectados_t * multiplicador_contacto

    # Flujos
    ER_t = susceptibles_t * λ_t                   #flujo latentes
    IR_t =  latentes_t / f                      #flujo infectados
    MR_t = infectados_t * fraccion_muertos      #flujo muertos
    RR_t = infectados_t / tiempo_recuperacion   #flujo recuperados

    trabajadores_sanos = susceptibles_t + latentes_t + recuperados_t
    # ========= HOSPITAL ================

    #Número total de personas que el hospital puede tratar
    capacidad_hosp_trab = trabajadores_sanos * pacientes_trabajador
    camas_hosp_disp = camas_hospital - hospitalizados

    #Máximo número de personas que pueden ser admitidas en un día
    capacidad_admision = min(capacidad_hosp_trab - hospitalizados - icu, camas_hosp_disp)
    camas_disp_icu = camas_icu - icu

    # ------------------- Flujos ---------------------------------
    # Espera
    llegando_espera = infectados * infectados_hospital
    muertos_esp = espera * fracc_muertes_espera
    recuperados_esp = espera * fracc_recuperacion_espera
    #Se admite a todos los que están esperando o a los que se pueden acomodar
    admitidos_dia = min(capacidad_admision, espera)

    # Hospitalizados
    muertos_hosp = fracc_muertes_hosp * hospitalizados
    altas_dia = hospitalizados / tiempo_estadia

    # ICU
    entran_icu = min(fraccion_icu * hospitalizados, camas_disp_icu)
    muertos_icu = fracc_muertes_icu * icu
    altas_icu = icu / tiempo_estadia_icu


    # Stocks
    ds = - ER
    de = ER - IR
    di = IR - RR - MR - llegando_espera
    dm = MR + muertos_esp + muertos_hosp + muertos_icu
    dr = RR + recuperados_esp + altas_dia

    ds_t = - ER_t
    de_t = ER_t - IR_t
    di_t = IR_t - RR_t - MR_t
    dm_t = MR_t
    dr_t = RR_t

    desp = llegando_espera - admitidos_dia - muertos_esp - recuperados_esp
    dhosp = admitidos_dia - muertos_hosp - altas_dia - entran_icu + altas_icu
    dicu = entran_icu - muertos_icu - altas_icu

    return (ds, de, di, dr, dm, ds_t, de_t, di_t, dr_t, dm_t, desp, dhosp, dicu)

ts = 200
sol = solve_ivp(complete_model, [0,ts], Y0, t_eval=np.arange(0,ts,0.125), max_step=0.5)

plt.plot(sol.t, sol.y.T, label=['S', 'E', 'I', 'R', 'M','S_T', 'E_T', 'I_T', 'R_T', 'M_T', 'Esp', 'Hosp', 'Icu'])
plt.legend(['S', 'E', 'I', 'R', 'M','S_T', 'E_T', 'I_T', 'R_T', 'M_T', 'Esp', 'Hosp', 'Icu'],loc='upper right')
plt.title('Modelo Poblacional-Trabajadores-Hospital')
plt.show()
