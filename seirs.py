from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.style.use('seaborn')

#-------------- SEIR POBLACIONAL -----------------------

#------ Variables iniciales ----------
# En SEIR agregamos stock de latentes (E) y muertos
# N -> total poblacion
# I0 -> infectados iniciales
# S0 -> susceptibles iniciales
# R0 -> recuperados iniciales
# E0 -> latentes iniciales

N =  100_000
N_trabajadores =  N * 0.1   #para SEIR trabajadores
# camas_hospital = N / 100    #para hospital
# camas_icu = N /500          #para hospital

I0 = 0
S0 = N - I0
E0 = 1
R0 = 0
M0 = 0

Y0 = (S0, E0, I0, R0, M0)

CE = 1.5
fraccion_muertos = 0.116    #dato obtenido de la tasa de mortalidad del covid-19
tiempo_recuperacion = 3     #duracion de la infeccion
f = 14
#tiempo_inmunidad = 90
#likelihood_cuarentena = 0.0
#mortalidad = 0.0

def seirs_model(t, y):
    susceptibles, latentes, infectados, recuperados, muertos = y

    β = CE / N
    λ = β * infectados

    # Flujos
    ER = susceptibles * λ                   #flujo latentes
    IR =  latentes / f                      #flujo infectados
    MR = infectados * fraccion_muertos      #flujo muertos
    RR = infectados / tiempo_recuperacion   #flujo recuperados

    # Stocks
    ds = - ER
    de = ER - IR
    di = IR - RR - MR
    dm = MR
    dr = RR

    return (ds, de, di, dr, dm)

ts = 150
sol = solve_ivp(seirs_model, [0,ts], Y0, t_eval=np.arange(0,ts,0.125), max_step=0.5)

plt.plot(sol.t, sol.y.T, label=['S', 'E', 'I', 'R', 'M'])
plt.legend(['S', 'E', 'I','R', 'M'],loc='upper right')
plt.title('Población')
plt.show()


#-------------- SEIR DE TRABAJADORES -----------------------
#------ Variables iniciales ----------
# En SEIR agregamos stock de latentes (E) y muertos
# N_trabajadores -> total poblacion de trabajadores, inicializada arriba
# I0_trabajadores -> infectados iniciales
# S0_trabajadores -> susceptibles iniciales
# R0_trabajadores -> recuperados iniciales
# E0_trabajadores -> latentes iniciales



I0_trabajadores = 0
S0_trabajadores = N_trabajadores - I0
E0_trabajadores = 1
R0_trabajadores = 0
M0_trabajadores = 0
#trabajadores_aps_sanos = [S0_trabajadores + E0_trabajadores + R0_trabajadores]

Y0 = (S0_trabajadores, E0_trabajadores, I0_trabajadores, R0_trabajadores, M0_trabajadores)

multiplicador_contacto = 2



def seirs_model_trabajadores(t, y):
    susceptibles, latentes, infectados, recuperados, muertos = y

    β = CE / N_trabajadores
    λ = β * infectados * multiplicador_contacto

    # Flujos
    ER = susceptibles * λ                   #flujo latentes
    IR =  latentes / f                      #flujo infectados
    MR = infectados * fraccion_muertos      #flujo muertos
    RR = infectados / tiempo_recuperacion   #flujo recuperados

    # Stocks
    ds = - ER
    de = ER - IR
    di = IR - RR - MR
    dm = MR
    dr = RR

    return (ds, de, di, dr, dm)

ts = 130
sol = solve_ivp(seirs_model_trabajadores, [0,ts], Y0, t_eval=np.arange(0,ts,0.125), max_step=0.5)

plt.plot(sol.t, sol.y.T, label=['S', 'E', 'I', 'R', 'M'])
plt.legend(['S', 'E', 'I','R', 'M'],loc='upper right')
plt.title('Trabajadores')
plt.show()

# plt.plot(sol.t, trabajadores_aps_sanos, label=['Aparentemente Sanos'])
# plt.legend(['AparentementeSanos'],loc='upper right')
# plt.show()

# #-------------- HOSPITALES -----------------------
# #------ Variables iniciales ----------
# # En SEIR agregamos stock de latentes (E) y muertos
# # N -> total poblacion
# # I0 -> infectados iniciales
# # S0 -> susceptibles iniciales
# # R0 -> recuperados iniciales
# # E0 -> latentes iniciales

# #----------- Stocks -------------------
# #En espera
# #Hospitalizados
# #ICU

# pacientes_trabajador = 9    #9 pacientes por trabajador
# infectados_hospital = 0.25

# fracc_muertes_espera = 0.01
# fracc_recuperacion_espera = 0.05
# fraccion_icu = 0.1
# tiempo_estadia = 5
# fracc_muertes_icu = 0.2
# tiempo_estadia_icu = 3
# fracc_muertes_hosp = 0.15



# def hospital_model(t, y, dep):
#     espera, hospitalizados, icu = y
#     infectados, trabajadores_sanos = dep
#     global camas_hospital, camas_icu


#     capacidad_hosp_trab = trabajadores_sanos * pacientes_trabajador
#     camas_hosp_disp = camas_hospital - hospitalizados

#     capacidad_admision = min(capacidad_hosp_trab, camas_hosp_disp) - hospitalizados - icu
#     camas_disp_icu = camas_icu - icu

#     # ------------------- Flujos ---------------------------------
#     # Espera
#     llegando_espera = infectados * infectados_hospital
#     muertos_esp = espera * fracc_muertes_espera
#     recuperados_esp = espera * fracc_recuperacion_espera
#     admitidos_dia = min(capacidad_admision, espera)

#     # Hospitalizados
#     muertos_hosp = fracc_muertes_hosp * hospitalizados
#     altas_dia = hospitalizados / tiempo_estadia

#     # ICU
#     entran_icu = min(fraccion_icu * hospitalizados, camas_disp_icu)
#     muertos_icu = fracc_muertes_icu * icu
#     altas_icu = icu / tiempo_estadia_icu


#     # Stocks
#     desp = llegando_espera - admitidos_dia - muertos_esp - recuperados_esp
#     dhosp = admitidos_dia - muertos_hosp - altas_dia - entran_icu
#     dicu = entran_icu - muertos_icu - altas_icu

#     return (desp, dhosp, dicu)

# ts = 130
# sol = solve_ivp(hospital_model, [0,ts], Y0, t_eval=np.arange(0,ts,0.125), max_step=0.5)

# plt.plot(sol.t, sol.y.T, label=['S', 'E', 'I', 'R', 'M'])
# plt.legend(['S', 'E', 'I','R', 'M'],loc='upper right')
# plt.title('Trabajadores')
# plt.show()


# # ============================ JUNTAMOS LOS TRES MODELOS ===================================

# # ============================== VARIABLES INICIALES =======================================
# N =  100_000
# N_trabajadores =  N * 0.1   #para SEIR trabajadores
# camas_hospital = N / 100    #para hospital
# camas_icu = N /500          #para hospital

# I0 = 0
# S0 = N - I0
# E0 = 1
# R0 = 0
# M0 = 0

# Y0_p = (S0, E0, I0, R0, M0)

# CE = 1.5
# fraccion_muertos = 0.116    #dato obtenido de la tasa de mortalidad del covid-19
# tiempo_recuperacion = 3     #duracion de la infeccion
# f = 14

# I0_trabajadores = 0
# S0_trabajadores = N_trabajadores - I0
# E0_trabajadores = 1
# R0_trabajadores = 0
# M0_trabajadores = 0

# Y0_t = (S0_trabajadores, E0_trabajadores, I0_trabajadores, R0_trabajadores, M0_trabajadores)

# multiplicador_contacto = 2

# pacientes_trabajador = 9    #9 pacientes por trabajador
# infectados_hospital = 0.25

# fracc_muertes_espera = 0.01
# fracc_recuperacion_espera = 0.05
# fraccion_icu = 0.1
# tiempo_estadia = 5
# fracc_muertes_icu = 0.2
# tiempo_estadia_icu = 3
# fracc_muertes_hosp = 0.15

# espera = 0
# hospitalizados = 0
# icu = 0

# Y0_h = (espera, hospitalizados, icu)

# Y0 = (Y0_p, Y0_t, Y0_h)

# def complete_model(t, y):
#     # ====== SEIR POBLACIONAL ==============================, ================== SEIR TRABAJADORES =============================, ======= HOSPITAL ===========
#     susceptibles, latentes, infectados, recuperados, muertos, susceptibles_t, latentes_t, infectados_t, recuperados_t, muertos_t,  espera, hospitalizados, icu = y
#     global camas_hospital, camas_icu, N, N_trabajadores

#     # ========= SEIR POBLACIONAL ================
#     β = CE / N
#     λ = β * infectados

#     # Flujos
#     ER = susceptibles * λ                   #flujo latentes
#     IR =  latentes / f                      #flujo infectados
#     MR = infectados * fraccion_muertos      #flujo muertos
#     RR = infectados / tiempo_recuperacion   #flujo recuperados

#     # Stocks
#     ds = - ER
#     de = ER - IR
#     di = IR - RR - MR
#     dm = MR
#     dr = RR

#     N = N - MR

#     # ========= SEIR TRABAJADORES ================
#     β_t = CE / N_trabajadores
#     λ_t = β_t * infectados_t * multiplicador_contacto

#     # Flujos
#     ER_t = susceptibles_t * λ_t                   #flujo latentes
#     IR_t =  latentes_t / f                      #flujo infectados
#     MR_t = infectados_t * fraccion_muertos      #flujo muertos
#     RR_t = infectados_t / tiempo_recuperacion   #flujo recuperados

#     # Stocks
#     ds_t = - ER_t
#     de_t = ER_t - IR_t
#     di_t = IR_t - RR_t - MR_t
#     dm_t = MR_t
#     dr_t = RR_t

#     N_trabajadores = N_trabajadores - MR_t


#     trabajadores_sanos = susceptibles_t + latentes_t + recuperados_t
#     # ========= HOSPITAL ================

#     capacidad_hosp_trab = trabajadores_sanos * pacientes_trabajador
#     camas_hosp_disp = camas_hospital - hospitalizados

#     capacidad_admision = min(capacidad_hosp_trab, camas_hosp_disp) - hospitalizados - icu
#     camas_disp_icu = camas_icu - icu

#     # ------------------- Flujos ---------------------------------
#     # Espera
#     llegando_espera = infectados * infectados_hospital
#     muertos_esp = espera * fracc_muertes_espera
#     recuperados_esp = espera * fracc_recuperacion_espera
#     admitidos_dia = min(capacidad_admision, espera)

#     # Hospitalizados
#     muertos_hosp = fracc_muertes_hosp * hospitalizados
#     altas_dia = hospitalizados / tiempo_estadia

#     # ICU
#     entran_icu = min(fraccion_icu * hospitalizados, camas_disp_icu)
#     muertos_icu = fracc_muertes_icu * icu
#     altas_icu = icu / tiempo_estadia_icu


#     # Stocks
#     desp = llegando_espera - admitidos_dia - muertos_esp - recuperados_esp
#     dhosp = admitidos_dia - muertos_hosp - altas_dia - entran_icu
#     dicu = entran_icu - muertos_icu - altas_icu

#     return (ds, de, di, dr, dm, ds_t, de_t, di_t, dr_t, dm_t, desp, dhosp, dicu)

# ts = 130
# sol = solve_ivp(complete_model, [0,ts], Y0, t_eval=np.arange(0,ts,0.125), max_step=0.5)

# plt.plot(sol.t, sol.y.T, label=['S', 'E', 'I', 'R', 'M','S_T', 'E_T', 'I_T', 'R_T', 'M_T', 'Esp', 'Hosp', 'Icu'])
# plt.legend(['S', 'E', 'I', 'R', 'M','S_T', 'E_T', 'I_T', 'R_T', 'M_T', 'Esp', 'Hosp', 'Icu'],loc='upper right')
# plt.title('Completo')
# plt.show()
