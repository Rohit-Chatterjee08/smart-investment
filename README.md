# 📈 Smart Investment Mixer

An interactive tool that helps you find the smartest way to split your investment money across different stocks, balancing potential profit with risk.

## Live Demo

You can try the live application here: **https://huggingface.co/spaces/chatterjeerohit08/investment-portfolio-optimizer**

---

## Overview

Ever wondered how to best allocate your investments? This tool takes the guesswork out of building a stock portfolio. Based on the Nobel Prize-winning Modern Portfolio Theory, it analyzes historical data to find the optimal investment mix.

**Key Features:**
-   **Simple Input:** Accepts a list of company stock symbols.
-   **Smart Calculation:** Finds the best investment mix to maximize return for the amount of risk taken (the Sharpe Ratio).
-   **Clear Visualization:** Displays a chart of thousands of possible investment outcomes, highlighting the "smartest mix."
-   **Modern UI:** A beautiful, user-friendly interface designed to be clear and intuitive.

---

## How to Use

1.  **Find Company Stock Symbols:** A "stock symbol" is the unique code for a company on the stock market (like `AAPL` for Apple or `TSLA` for Tesla). You can find the correct symbol for any company by searching its name on **Yahoo Finance**. 
2.  **Enter the Symbols:** Type the stock symbols into the input box, separated by commas.
3.  **Click "Find Smartest Mix":** The tool will analyze the stocks and provide its recommendation.

**Example Input:**
`AAPL, GOOGL, TSLA, NVDA`

**The Output Will Show You:**
-   **Recommended Investment Mix:** The exact percentage of your money to put into each stock.
-   **Expected Performance:** A summary of the portfolio's potential yearly profit and risk.
-   **Map of Possible Outcomes:** A chart showing how your recommended mix compares to thousands of other possibilities.

---

## Technology Stack

-   **Backend:** Python
-   **Data & Optimization:** Pandas, NumPy, yfinance, SciPy
-   **Web Framework/UI:** Gradio
-   **Plotting:** Matplotlib

---

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone [Your GitHub Repository URL]
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd [repository-name]
    ```
3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python app.py
    ```
