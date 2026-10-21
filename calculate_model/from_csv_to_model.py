import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
csv_path = os.path.join(PROJECT_ROOT, "calculate_model", "dataset.csv")

def modele_log(x, a, b):
    return a * np.log(x) + b

alpha_table = [0.0001 * i for i in range(0, 2000)]
df = pd.read_csv(csv_path)

# Filtrer pour ne garder que les joueurs entre 1400 et 2600 Elo
df = df[(df["Elo"] >= 1400) & (df["Elo"] < 2600)].copy()

bin_edges = [1400, 1600, 1800, 2000, 2200, 2400, 2600]
bin_labels = ['1400-1600', '1600-1800', '1800-2000', '2000-2200', '2200-2400', '2400-2600']

best_rmse = np.inf
best_alpha_value = 0
best_coeff = None

for alpha in alpha_table:
    # 1. Calcul vectorisé de la perte coefficientée
    df["CoefficientedLoss"] = df["WinRateLoss"] * (1.0 / (1.0 - alpha * df["PlayableMovesCount"]))
    
    # 2. Attribution et regroupement par tranche
    df["Elo_Bin"] = pd.cut(df["Elo"], bins=bin_edges, labels=bin_labels, right=False)
    df_contracted = df.groupby("Elo_Bin", observed=True).agg({
        "CoefficientedLoss": "mean",
        "Elo": "mean"
    }).dropna().reset_index()
    
    if len(df_contracted) < 3:
        continue

    x_data = df_contracted["CoefficientedLoss"]
    y_data = df_contracted["Elo"]
    
    try:
        # 3. Ajustement de la courbe
        popt, _ = curve_fit(modele_log, x_data, y_data)
        A, B = popt
        
        if A >= 0:
            continue

        # 4. Calcul de l'erreur de prédiction (RMSE) sur les tranches
        y_pred = modele_log(x_data, A, B)
        rmse = np.sqrt(np.mean((y_data - y_pred) ** 2))
        
        # On cherche à minimiser l'écart direct entre le modèle et les points réels
        if rmse < best_rmse:
            best_rmse = rmse
            best_alpha_value = alpha
            best_coeff = (A, B)
            if best_alpha_value == 0:
                print(f"coefficients initiaux (A, B) : {best_coeff}")
                print(f"RMSE minimal sur la tranche initial : {best_rmse:.2f} points d'Elo")
        
    except RuntimeError:
        continue

print("\n--- Résultat Optimal (Basé sur le RMSE des tranches) ---")
print(f"Meilleur Alpha : {best_alpha_value:.4f}")
print(f"Meilleurs coefficients (A, B) : {best_coeff}")
print(f"RMSE minimal sur les tranches : {best_rmse:.2f} points d'Elo")