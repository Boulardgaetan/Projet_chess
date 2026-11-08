import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
csv_path = os.path.join(PROJECT_ROOT, "calculate_model", "dataset.csv")

def logarithmic_model(x, a, b):
    """Logarithmic model mapping coefficiented loss to Elo rating."""
    return a * np.log(x) + b

# Search space for alpha optimization
alpha_table = [0.0001 * i for i in range(0, 2000)]
df = pd.read_csv(csv_path)

# Filter dataset to keep only players within the 1400-2600 Elo bracket
df = df[(df["Elo"] >= 1400) & (df["Elo"] < 2600)].copy()

bin_edges = [1400, 1600, 1800, 2000, 2200, 2400, 2600]
bin_labels = ['1400-1600', '1600-1800', '1800-2000', '2000-2200', '2200-2400', '2400-2600']

best_rmse = np.inf
best_alpha_value = 0
best_coeff = None

for alpha in alpha_table:
    # 1. Vectorized calculation of the coefficiented loss
    df["CoefficientedLoss"] = df["WinRateLoss"] * (1.0 / (1.0 - alpha * df["PlayableMovesCount"]))
    
    # 2. Assignment and grouping by Elo brackets
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
        # 3. Curve fitting (logarithmic regression)
        popt, _ = curve_fit(logarithmic_model, x_data, y_data)
        A, B = popt
        
        # Constraint: logarithmic coefficient A must be negative (higher loss = lower Elo)
        if A >= 0:
            continue

        # 4. Compute RMSE on the brackets
        y_pred = logarithmic_model(x_data, A, B)
        rmse = np.sqrt(np.mean((y_data - y_pred) ** 2))
        
        # Look for parameters minimizing the direct error between the model and real points
        if rmse < best_rmse:
            best_rmse = rmse
            best_alpha_value = alpha
            best_coeff = (A, B)
            if best_alpha_value == 0:
                print(f"Initial coefficients (A, B): {best_coeff}")
                print(f"Initial minimal RMSE on brackets: {best_rmse:.2f} Elo points")
        
    except RuntimeError:
        continue

print("\n--- Optimal Results (Based on Brackets RMSE) ---")
print(f"Best Alpha: {best_alpha_value:.4f}")
print(f"Best Coefficients (A, B): {best_coeff}")
print(f"Minimal RMSE on brackets: {best_rmse:.2f} Elo points")