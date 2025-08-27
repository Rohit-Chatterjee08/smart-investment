# app_optimizer.py

import gradio as gr
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco

# --- 1. MODERN CSS FOR AN IMPRESSIVE UI (UNCHANGED) ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
body, #optimizer-app {
    background: linear-gradient(135deg, #1f2023 0%, #2c3e50 100%);
    font-family: 'Poppins', sans-serif;
}
#optimizer-app {
    background: rgba(30, 30, 45, 0.6);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}
#header h1 {
    font-size: 3em;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0 0 10px rgba(0, 198, 255, 0.5);
}
#header p {
    color: #bdc3c7;
    font-size: 1.1em;
}
.gradio-container .form-control, .gradio-dataframe {
    background-color: rgba(0, 0, 0, 0.2);
    color: #ecf0f1;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
}
.gradio-dataframe table th {
    background-color: rgba(0, 198, 255, 0.2) !important;
}
#optimize-button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 8px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px 0 rgba(0, 198, 255, 0.4);
}
#optimize-button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 8px 25px 0 rgba(0, 198, 255, 0.6);
}
.output-header {
    font-size: 1.5em;
    font-weight: 600;
    color: #ecf0f1;
    text-align: center;
    border-bottom: 2px solid #00c6ff;
    padding-bottom: 5px;
    margin-bottom: 15px;
}
"""

# --- 2. THE CORE OPTIMIZATION LOGIC (UNCHANGED) ---
def optimize_portfolio(tickers_str, start_date='2020-01-01'):
    try:
        tickers = [ticker.strip().upper() for ticker in tickers_str.split(',')]
        if not tickers or tickers_str == '':
            raise ValueError("Ticker list cannot be empty.")
            
        data = yf.download(tickers, start=start_date, auto_adjust=True)['Close']
        if data.empty or data.isnull().all().all() or (isinstance(data, pd.DataFrame) and data.shape[1] != len(tickers)):
            raise ValueError("Could not download valid data for all tickers. Please check the company symbols.")
        
        returns = data.pct_change().dropna()
        mean_returns = returns.mean() * 252
        cov_matrix = returns.cov() * 252
        num_assets = len(tickers)

        def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0):
            p_return = np.dot(weights, mean_returns)
            p_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            # Add a small epsilon to avoid division by zero
            return -(p_return - risk_free_rate) / (p_volatility + 1e-9)

        constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
        bounds = tuple((0, 1) for _ in range(num_assets))
        initial_guess = num_assets * [1. / num_assets]

        solution = sco.minimize(negative_sharpe_ratio, initial_guess, args=(mean_returns, cov_matrix),
                                method='SLSQP', bounds=bounds, constraints=constraints)
        
        optimal_weights = solution.x
        
        num_portfolios = 10000
        p_returns, p_volatility = [], []
        for _ in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights /= np.sum(weights)
            p_returns.append(np.dot(weights, mean_returns))
            p_volatility.append(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))

        weights_df = pd.DataFrame({'Stock': tickers, 'Recommended Mix': [f"{w:.2%}" for w in optimal_weights]})
        opt_return = np.dot(optimal_weights, mean_returns)
        opt_volatility = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))
        opt_sharpe = opt_return / (opt_volatility + 1e-9)
        summary_str = (
            f"Expected Yearly Return: {opt_return:.2%}\n"
            f"Expected Yearly Risk: {opt_volatility:.2%}\n"
            f"Return/Risk Ratio (Sharpe): {opt_sharpe:.2f}"
        )
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 7), facecolor='#1a1a1a')
        ax.scatter(p_volatility, p_returns, c=(np.array(p_returns)/(np.array(p_volatility)  + 1e-9)), cmap='plasma', marker='o')
        ax.scatter(opt_volatility, opt_return, c='cyan', marker='*', s=500, edgecolors='white', label='Smartest Mix')
        ax.set_title('Possible Investment Outcomes', color='white', fontsize=16)
        ax.set_xlabel('Risk (Volatility)', color='white', fontsize=12)
        ax.set_ylabel('Profit (Return)', color='white', fontsize=12)
        ax.tick_params(colors='white')
        ax.legend()
        plt.tight_layout()

        return fig, weights_df, summary_str

    except Exception as e:
        error_message = f"An error occurred: {e}"
        empty_fig, _ = plt.subplots(facecolor='#1a1a1a')
        return empty_fig, pd.DataFrame(), error_message

# --- 3. BUILD THE GRADIO APP WITH SIMPLIFIED TEXT ---
with gr.Blocks(css=custom_css, elem_id="optimizer-app") as app:
    with gr.Column(elem_id="header"):
        gr.Markdown("<h1>📈 Smart Investment Mixer</h1>")
        # <<< CHANGED: Simplified description
        gr.Markdown("<p>Want to invest in a few companies but don't know how to split your money? This tool finds the smartest investment mix for you, balancing potential profit with risk.</p>")

    with gr.Row():
        # <<< CHANGED: Simplified label and placeholder
        ticker_input = gr.Textbox(
            label="Enter Company Stock Symbols (separated by commas)", 
            placeholder="e.g., AAPL for Apple, MSFT for Microsoft, TSLA for Tesla"
        )
        optimize_button = gr.Button("Find Smartest Mix", elem_id="optimize-button")
    
    with gr.Row():
        with gr.Column(scale=1):
            # <<< CHANGED: Simplified headers
            gr.Markdown("<h3 class='output-header'>Recommended Investment Mix</h3>")
            weights_output = gr.DataFrame(headers=["Stock", "Recommended Mix"])
            gr.Markdown("<h3 class='output-header'>Expected Performance</h3>")
            summary_output = gr.Textbox(label="Metrics", interactive=False)
        with gr.Column(scale=2):
            gr.Markdown("<h3 class='output-header'>Map of Possible Outcomes</h3>")
            plot_output = gr.Plot()

    optimize_button.click(
        fn=optimize_portfolio,
        inputs=ticker_input,
        outputs=[plot_output, weights_output, summary_output]
    )

app.launch()