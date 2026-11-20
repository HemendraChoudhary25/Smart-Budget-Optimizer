import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from optimizer import solve_knapsack

st.set_page_config(page_title="Smart Budget Optimizer", page_icon="💰", layout="wide")
st.title("💰 Smart Budget Optimizer")
st.caption("Choose the best combination of items within your budget using the 0–1 Knapsack algorithm.")

if "items" not in st.session_state:
    st.session_state.items = [
        {"Item": "Laptop", "Cost": 45000, "Value": 90},
        {"Item": "Smartphone", "Cost": 18000, "Value": 70},
        {"Item": "Headphones", "Cost": 3500, "Value": 25},
        {"Item": "Study Table", "Cost": 6000, "Value": 35},
        {"Item": "Books", "Cost": 2500, "Value": 30},
    ]

with st.sidebar:
    st.header("Add an item")
    name = st.text_input("Item name")
    cost = st.number_input("Cost (₹)", min_value=1, value=1000, step=100)
    value = st.number_input("Benefit / value score", min_value=1, value=10, step=1)
    if st.button("Add item", use_container_width=True):
        if name.strip():
            st.session_state.items.append({"Item": name.strip(), "Cost": int(cost), "Value": int(value)})
            st.success(f"Added {name.strip()}")
            st.rerun()
        else:
            st.warning("Enter an item name.")

    st.divider()
    budget = st.number_input("Total budget (₹)", min_value=1, value=50000, step=1000)

st.subheader("Available items")
df = pd.DataFrame(st.session_state.items)
edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="item_editor")
if st.button("Use edited item list"):
    cleaned = edited.dropna(subset=["Item", "Cost", "Value"])
    st.session_state.items = [
        {"Item": str(row["Item"]), "Cost": int(row["Cost"]), "Value": int(row["Value"])}
        for _, row in cleaned.iterrows() if str(row["Item"]).strip() and int(row["Cost"]) > 0 and int(row["Value"]) > 0
    ]
    st.success("Item list updated.")
    st.rerun()

if st.session_state.items:
    result = solve_knapsack(st.session_state.items, int(budget))
    selected = result["selected"]
    total_cost = sum(item["Cost"] for item in selected)
    total_value = sum(item["Value"] for item in selected)
    unused = int(budget) - total_cost

    st.subheader("Optimal recommendation")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total benefit", total_value)
    c2.metric("Budget used", f"₹{total_cost:,}", f"{total_cost / budget:.1%}")
    c3.metric("Remaining budget", f"₹{unused:,}")

    st.success("Recommended combination")
    st.dataframe(pd.DataFrame(selected) if selected else pd.DataFrame(columns=["Item", "Cost", "Value"]),
                 use_container_width=True, hide_index=True)

    left, right = st.columns(2)
    with left:
        st.markdown("**Budget utilization**")
        fig, ax = plt.subplots()
        ax.pie([total_cost, unused] if total_cost or unused else [1], labels=["Used", "Remaining"] if total_cost or unused else ["No allocation"], autopct="%1.1f%%")
        ax.set_title("Budget allocation")
        st.pyplot(fig)
        plt.close(fig)
    with right:
        st.markdown("**Benefit by selected item**")
        if selected:
            chart_df = pd.DataFrame(selected).set_index("Item")[["Value"]]
            st.bar_chart(chart_df)
        else:
            st.info("No item fits within this budget.")

    with st.expander("View Dynamic Programming table"):
        st.caption("Rows represent items; columns represent budget capacities. For readability, capacities are shown in ₹ units.")
        st.dataframe(pd.DataFrame(result["dp"]), use_container_width=True)

    with st.expander("Algorithm explanation"):
        st.write("""
        **0–1 Knapsack recurrence**

        For item *i* and capacity *w*:
        - If the item cost exceeds *w*, carry forward the previous best value.
        - Otherwise, choose the maximum of excluding the item or including it once.

        `DP[i][w] = max(DP[i-1][w], value[i] + DP[i-1][w-cost[i]])`

        The app uses integer budget units (₹1). For very large budgets, reduce the budget scale
        (for example, use ₹100 units) to reduce memory use.
        """)
else:
    st.info("Add at least one item to begin.")
