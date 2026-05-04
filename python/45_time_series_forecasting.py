# ============================================================
# Program Title : Time Series Forecasting (Moving Average)
# Author        : Lydia S. Makiwa
# Date          : 2026-05-04
# Description   : Implement a simple time-series forecaster
#                 using exponential smoothing and moving average.
#                 Great foundation before learning ARIMA/LSTM.
# ============================================================

import numpy as np

# --- Simulated monthly sales data (24 months) ---
np.random.seed(0)
trend  = np.linspace(100, 200, 24)
seasonal = 15 * np.sin(np.linspace(0, 4*np.pi, 24))
noise  = np.random.normal(0, 5, 24)
data   = trend + seasonal + noise

def moving_average(series, window):
    result = []
    for i in range(len(series)):
        if i < window:
            result.append(np.mean(series[:i+1]))
        else:
            result.append(np.mean(series[i-window:i]))
    return np.array(result)

def exp_smoothing(series, alpha=0.3):
    result = [series[0]]
    for i in range(1, len(series)):
        result.append(alpha * series[i] + (1-alpha) * result[-1])
    return np.array(result)

def forecast_next(series, n_ahead=3, alpha=0.3):
    smoothed = exp_smoothing(series, alpha)
    last = smoothed[-1]
    slope = (smoothed[-1] - smoothed[-6]) / 6
    return [last + slope*(i+1) for i in range(n_ahead)]

ma3  = moving_average(data, 3)
es   = exp_smoothing(data, 0.3)
future = forecast_next(data)

print('Month | Actual | MA(3) | Exp.Smooth')
print('-' * 40)
for i in range(len(data)):
    print(f'  {i+1:2d}  | {data[i]:6.1f} | {ma3[i]:6.1f} | {es[i]:6.1f}')
print('\nNext 3-month forecast (Exp. Smoothing):')
for i, v in enumerate(future, 1):
    print(f'  Month {len(data)+i}: {v:.1f}')
mse = np.mean((data - es)**2)
print(f'\nExp. Smoothing MSE: {mse:.2f}')
print('Time series forecasting demo complete!')
