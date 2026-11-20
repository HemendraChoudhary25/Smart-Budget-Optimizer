# Smart Budget Optimizer

A live Streamlit project that recommends the most valuable set of items within a fixed budget using the **0–1 Knapsack Dynamic Programming algorithm**.

## Features
- Add and edit items (name, cost, benefit score)
- Set a budget
- Optimal item selection with 0–1 Knapsack
- Budget-used and remaining metrics
- Budget allocation pie chart and benefit bar chart
- Expandable DP table and algorithm explanation

## Run locally (Windows / VS Code)
1. Install Python 3.10 or later.
2. Extract this ZIP.
3. Open the extracted folder in VS Code.
4. Open the terminal and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

The app opens in your browser, usually at `http://localhost:8501`.

## Algorithm
For each item `i` and budget capacity `w`:

`DP[i][w] = max(DP[i-1][w], value[i] + DP[i-1][w-cost[i]])`

when `cost[i] <= w`; otherwise `DP[i][w] = DP[i-1][w]`.

- Time complexity: `O(n × W)`
- Space complexity: `O(n × W)`
- `n`: number of items, `W`: budget capacity in integer rupee units

**Note:** The DP table grows with the budget. For large budgets, use a scaled unit such as ₹100 instead of ₹1.
