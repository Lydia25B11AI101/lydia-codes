"""
Program Title: Monte Carlo Portfolio Risk Simulation
Author: Lydia S. Makiwa
Date: June 2, 2026

Description:
This program models the future performance of a stock portfolio using Monte Carlo Simulation.
It calculates expected returns, standard deviations, and estimates Value at Risk (VaR) 
and Conditional Value at Risk (CVaR). Highly relevant for quantitative finance and risk analytics.
"""

import numpy as np

def run_portfolio_simulation(initial_val, weights, means, cov_matrix, days=252, runs=1000):
    """
    Simulates portfolio paths using Geometric Brownian Motion multivariate projection.
    """
    num_assets = len(weights)
    weights = np.array(weights)
    
    # Daily returns simulation setup
    # Calculate portfolio mean and standard deviation mathematically
    port_mean = np.dot(weights, means)
    port_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    port_std = np.sqrt(port_variance)
    
    # Simulate daily log returns
    # Normal distribution of returns
    simulated_returns = np.random.normal(port_mean, port_std, size=(days, runs))
    
    # Convert returns to cumulative portfolio values
    # price_t = price_0 * e^(sum of daily log returns)
    portfolio_paths = initial_val * np.exp(np.cumsum(simulated_returns, axis=0))
    
    return portfolio_paths

# --- Working Demo ---
if __name__ == "__main__":
    print("--- Stock Portfolio Monte Carlo Simulation ---")
    
    # Portfolio Configuration
    initial_investment = 100000  # $100,000 USD
    asset_weights = [0.4, 0.3, 0.3]  # Tech, Energy, Bonds
    
    # Annual expected returns (Tech: 12%, Energy: 8%, Bonds: 4%)
    # Converted to daily returns (approx 252 trading days per year)
    expected_annual_returns = np.array([0.12, 0.08, 0.04])
    daily_returns_mean = expected_annual_returns / 252
    
    # Covariance Matrix (reflecting volatilities and relationships between assets)
    # Volatilities: Tech ~25%, Energy ~20%, Bonds ~5%
    cov_matrix = np.array([
        [0.00025, 0.00010, -0.00001],  # Tech relations
        [0.00010, 0.00018,  0.00000],  # Energy relations
        [-0.00001, 0.00000, 0.00002]   # Bonds relations
    ])
    
    # Run 5000 simulations over 1 year (252 trading days)
    sim_days = 252
    num_runs = 5000
    
    np.random.seed(42)  # For reproducibility
    paths = run_portfolio_simulation(initial_investment, asset_weights, daily_returns_mean, cov_matrix, days=sim_days, runs=num_runs)
    
    # Ending values after 252 days
    ending_values = paths[-1, :]
    
    # Calculate statistics
    mean_ending = np.mean(ending_values)
    median_ending = np.median(ending_values)
    min_ending = np.min(ending_values)
    max_ending = np.max(ending_values)
    
    # Value at Risk (VaR) - 95% confidence (5th percentile of ending values)
    var_95 = initial_investment - np.percentile(ending_values, 5)
    # Conditional Value at Risk (CVaR) - average loss in the worst 5% of cases
    worst_5_percent = ending_values[ending_values <= np.percentile(ending_values, 5)]
    cvar_95 = initial_investment - np.mean(worst_5_percent)
    
    print(f"\nSimulation Results for a ${initial_investment:,.2f} Portfolio:")
    print(f"  Asset Allocation: Tech: 40% | Energy: 30% | Bonds: 30%")
    print(f"  Mean Portfolio End Value: ${mean_ending:,.2f} ({(mean_ending-initial_investment)/initial_investment*100:.2f}% return)")
    print(f"  Median Portfolio End Value: ${median_ending:,.2f}")
    print(f"  Worst Case Scenario (Minimum): ${min_ending:,.2f}")
    print(f"  Best Case Scenario (Maximum): ${max_ending:,.2f}")
    print(f"\nRisk Assessment Metrics:")
    print(f"  Value at Risk (95% Confidence): ${var_95:,.2f}")
    print(f"    (There is a 5% chance of losing ${var_95:,.2f} or more over 1 year)")
    print(f"  Conditional Value at Risk (95% CVaR): ${cvar_95:,.2f}")
    print(f"    (If we hit the worst 5% scenario, the average expected loss is ${cvar_95:,.2f})")