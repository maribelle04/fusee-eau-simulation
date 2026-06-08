"""
Simulation de vol d'une fusée à eau avec traînée aérodynamique.

Ce programme résout numériquement les équations différentielles couplées régissant
le vol d'une fusée à eau (propulsion par éjection d'eau sous pression). Il prend
en compte :
- La détente adiabatique de l'air (loi de Laplace)
- La vitesse d'éjection de l'eau (équation de Bernoulli)
- La poussée en fonction de la pression
- La variation de masse pendant l'éjection
- La traînée aérodynamique (coefficient Cx fixe)
- La phase balistique après éjection de l'eau

Paramètres d'entrée :
    Masse à vide (kg) : masse de la fusée sans eau (structure + avionique)
    Volume d'eau (L) : volume d'eau initial dans les bouteilles
    Pression relative (bar) : pression de gonflage (différence avec P_atm)

Sorties :
    - Affichage console des valeurs (temps, poussée, vitesse, débits, hauteur)
    - Hauteur maximale atteinte (avec traînée)
    - Courbes : poussée(t), vitesse(t), hauteur(t), volume d'air(t)

Méthode numérique :
    - Méthode d'Euler explicite
    - Pas de temps : 0,0001 s

Auteur : Maribellé BADAKOU 
Date : 5 juin 2026
"""

import math
import matplotlib.pyplot as plt

# ============================================================================
# SAISIE DES PARAMÈTRES PAR L'UTILISATEUR
# ============================================================================

print("=== SIMULATION FUSÉE À EAU AVEC TRAÎNÉE ===")
m_struct = float(input("Masse à vide (kg) : "))               # Masse structure (kg)
V_eau0_L = float(input("Volume d'eau (L) : "))               # Volume eau (Litres)
V_eau0 = V_eau0_L / 1000                                      # Conversion en m³
P_rel0_bar = float(input("Pression relative (bar) : "))       # Pression gonflage (bar)
P_rel0 = P_rel0_bar * 1e5                                     # Conversion en Pa

# ============================================================================
# PARAMÈTRES FIXES (NE PAS MODIFIER SANS RAISON)
# ============================================================================

P_atm = 1.013e5          # Pression atmosphérique (Pa)
rho = 1000.0             # Masse volumique de l'eau (kg/m³)
rho_air = 1.225          # Masse volumique de l'air (kg/m³) à 15°C
gamma = 1.4              # Coefficient adiabatique de l'air (diatomique)
d_goulot = 0.022         # Diamètre du goulot (m) = 22 mm
S_t = math.pi * (d_goulot/2)**2   # Section du goulot (m²)
V_total = 0.004          # Volume total des bouteilles (m³) = 4 L
g = 9.81                 # Accélération de la pesanteur (m/s²)

# Paramètres de traînée aérodynamique
Cx = 0.5                 # Coefficient de traînée (sans unité)
d_fusee = 0.11           # Diamètre extérieur de la fusée (m) = 11 cm
S_ref = math.pi * (d_fusee/2)**2   # Section de référence pour la traînée (m²)

# Paramètres numériques
dt = 0.0001              # Pas de temps pour la méthode d'Euler (s)
t_max = 0.5              # Temps maximal de simulation (s) (sécurité)

# ============================================================================
# INITIALISATION DES VARIABLES
# ============================================================================

V_air0 = V_total - V_eau0                # Volume d'air initial (m³)
P_abs0 = P_rel0 + P_atm                  # Pression absolue initiale (Pa)

# Listes pour stocker les résultats (phase propulsion)
t_prop, F_prop, v_prop, z_prop, V_air_prop = [], [], [], [], []
debit_massique_prop = []   # Débit massique (kg/s)
debit_volumique_prop = []  # Débit volumique (L/s)

# Variables évolutives au cours du temps
t = 0.0                    # Temps (s)
V_air = V_air0             # Volume d'air actuel (m³)
v_fusee = 0.0              # Vitesse de la fusée (m/s)
z = 0.0                    # Hauteur de la fusée (m)

# ============================================================================
# PHASE PROPULSION (ÉJECTION DE L'EAU)
# ============================================================================

print("\nCalcul propulsion (avec traînée)...")
print("t(s)   F(N)   v_fusée(m/s)   débit_massique(kg/s)   débit_volumique(L/s)   z(m)")

# Boucle principale : tant qu'il reste de l'eau et que le temps max n'est pas dépassé
while V_air < V_total and t < t_max:
    
    # 1. Pression absolue actuelle (loi de Laplace : PV^gamma = constante)
    P_abs = P_abs0 * (V_air0 / V_air) ** gamma
    
    # 2. Pression relative (ne peut pas être négative)
    P_rel = max(P_abs - P_atm, 0.0)
    
    # 3. Vitesse d'éjection de l'eau (Bernoulli)
    v_e = math.sqrt(2.0 * P_rel / rho)
    
    # 4. Poussée instantanée
    F = rho * S_t * v_e * v_e
    
    # 5. Débits volumique et massique
    debit_vol = S_t * v_e                # m³/s
    debit_mass = rho * debit_vol         # kg/s
    
    # 6. Masse actuelle de la fusée (structure + eau restante)
    m = m_struct + rho * (V_total - V_air)
    
    # 7. Traînée aérodynamique (opposée à la vitesse)
    if v_fusee > 0:
        F_trainee = 0.5 * rho_air * Cx * S_ref * v_fusee**2
    else:
        F_trainee = 0
    
    # 8. Accélération (Principe Fondamental de la Dynamique)
    a = (F - F_trainee) / m - g
    
    # 9. Mise à jour des variables (méthode d'Euler)
    V_air += S_t * v_e * dt       # Nouveau volume d'air
    v_fusee += a * dt             # Nouvelle vitesse
    z += v_fusee * dt             # Nouvelle hauteur
    t += dt                       # Nouveau temps
    
    # 10. Stockage dans les listes
    t_prop.append(t)
    F_prop.append(F)
    v_prop.append(v_fusee)
    z_prop.append(z)
    V_air_prop.append(V_air)
    debit_massique_prop.append(debit_mass)
    debit_volumique_prop.append(debit_vol * 1000)   # Conversion en L/s
    
    # 11. Affichage périodique (toutes les 100 itérations)
    if len(t_prop) % 100 == 0:
        print(f"{t:.3f}   {F:.0f}   {v_fusee:.2f}          {debit_mass:.2f}                  {debit_vol*1000:.1f}            {z:.2f}")

# Affichage des valeurs en fin de propulsion
print(f"\nFin propulsion : t={t:.3f}s, v={v_fusee:.1f}m/s, z={z:.1f}m")

# ============================================================================
# PHASE BALISTIQUE (APRÈS ÉJECTION DE L'EAU)
# ============================================================================

t_bal, z_bal = [], []      # Listes pour le temps et la hauteur (phase balistique)
t_b = t                    # Temps initial pour la balistique
z_b = z                    # Hauteur initiale
v_b = v_fusee              # Vitesse initiale

# Boucle : tant que la fusée monte (v > 0) et que le temps max n'est pas dépassé
while v_b > 0 and t_b < t_max + 2:
    
    # Traînée pendant la balistique (masse constante = m_struct)
    if v_b > 0:
        F_trainee = 0.5 * rho_air * Cx * S_ref * v_b**2
    else:
        F_trainee = 0
    
    # Accélération : uniquement poids et traînée (plus de poussée)
    a = -g - F_trainee / m_struct
    
    # Mise à jour (Euler)
    v_b += a * dt
    z_b += v_b * dt
    t_b += dt
    
    # On ne garde que les hauteurs positives (évite les valeurs négatives)
    if z_b >= 0:
        t_bal.append(t_b)
        z_bal.append(z_b)

# Hauteur maximale (apogée)
if z_bal:
    z_max = max(z_bal)
else:
    z_max = z

print(f"\nHauteur maximale (avec traînée) : {z_max:.1f} m")

# ============================================================================
# TRACÉ DES COURBES
# ============================================================================

plt.figure(figsize=(12, 10))

# Courbe 1 : Poussée en fonction du temps
plt.subplot(2, 2, 1)
plt.plot(t_prop, F_prop, 'b-')
plt.xlabel('Temps (s)')
plt.ylabel('Poussée (N)')
plt.title('Poussée')
plt.grid(True)

# Courbe 2 : Vitesse de la fusée en fonction du temps
plt.subplot(2, 2, 2)
plt.plot(t_prop, v_prop, 'r-')
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.title('Vitesse de la fusée')
plt.grid(True)

# Courbe 3 : Hauteur (propulsion en trait plein, balistique en pointillés)
plt.subplot(2, 2, 3)
plt.plot(t_prop, z_prop, 'g-', label='Propulsion')
if t_bal:
    plt.plot(t_bal, z_bal, 'g--', label='Balistique')
plt.xlabel('Temps (s)')
plt.ylabel('Hauteur (m)')
plt.title('Altitude')
plt.legend()
plt.grid(True)

# Courbe 4 : Volume d'air dans les bouteilles (en Litres)
plt.subplot(2, 2, 4)
plt.plot(t_prop, [v*1000 for v in V_air_prop], 'm-')
plt.xlabel('Temps (s)')
plt.ylabel("Volume d'air (L)")
plt.title("Volume d'air")
plt.grid(True)

plt.tight_layout()   # Ajuste automatiquement l'espacement entre les sous-graphiques
plt.show()
