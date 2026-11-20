
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from optimizer import solve_knapsack

# Page configuration
st.set_page_config(
    page_title="Smart Budget Optimizer",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Smart Budget Optimizer")
st.caption(
    "Choose the best combination of items within your budget "
    "using the 0–1 Knapsack Dynamic Programming Algorithm."
)

# Initialize session state
if "items" not in st.session_state:
    st.session_state["items"] = [
        {"Item": "Laptop", "Cost": 45000, "Value": 90},
        {"Item": "Smartphone", "Cost": 18000, "Value": 70},
        {"Item": "Headphones", "Cost": 3500, "Value": 25},
        {"Item": "Study Table", "Cost": 6000, "Value": 35},
        {"Item": "Books", "Cost": 2500, "Value": 30},
    ]

# Sidebar
with st.sidebar:
    st.header("➕ Add New Item")

    name = st.text_input("Item Name")

    cost = st.number_input(
        "Item Cost (₹)",
        min_value=1,
        value=1000,
        step=100
    )

    value = st.number_input(
        "Benefit Score",
        min_value=1,
        value=10,
        step=1
    )

    if st.button("Add Item", use_container_width=True):
        if name.strip():
            st.session_state["items"].append({
                "Item": name.strip(),
                "Cost": int(cost),
                "Value": int(value)
            })
            st.success("Item added successfully!")
            st.rerun()
        else:
            st.warning("Please enter an item name.")

    st.divider()

    budget = st.number_input(
        "Total Budget (₹)",
        min_value=1,
        value=50000,
        step=1000
    )

# Available Items
st.subheader("📦 Available Items")

df = pd.DataFrame(
    st.session_state["items"],
    columns=["Item", "Cost", "Value"]
)

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="item_editor"
)

if st.button("Update Item List"):
    try:
        cleaned = edited_df.dropna(
            subset=["Item", "Cost", "Value"]
        )

        updated_items = []

        for _, row in cleaned.iterrows():
            item_name = str(row["Item"]).strip()
            item_cost = int(row["Cost"])
            item_value = int(row["Value"])

            if item_name and item_cost > 0 and item_value > 0:
                updated_items.append({
                    "Item": item_name,
                    "Cost": item_cost,
                    "Value": item_value
                })

        st.session_state["items"] = updated_items
        st.success("Item list updated successfully!")
        st.rerun()

    except (ValueError, TypeError):
        st.error("Please enter valid positive numbers for cost and value.")

# Optimization
if st.session_state["items"]:

    try:
        result = solve_knapsack(
            st.session_state["items"],
            int(budget)
        )

        selected = result["selected"]

        total_cost = sum(item["Cost"] for item in selected)
        total_value = sum(item["Value"] for item in selected)
        remaining = int(budget) - total_cost

        # Results
        st.divider()
        st.subheader("🎯 Optimal Recommendation")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Benefit",
            total_value
        )

        col2.metric(
            "Budget Used",
            f"₹{total_cost:,}"
        )

        col3.metric(
            "Remaining Budget",
            f"₹{remaining:,}"
        )

        # Selected Items
        st.subheader("✅ Recommended Items")

        if selected:
            st.dataframe(
                pd.DataFrame(selected),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No items fit within the given budget.")

        # Charts
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.subheader("📊 Budget Utilization")

            fig, ax = plt.subplots()

            if total_cost > 0:
                ax.pie(
                    [total_cost, remaining],
                    labels=["Used Budget", "Remaining Budget"],
                    autopct="%1.1f%%",
                    startangle=90
                )
            else:
                ax.pie([1], labels=["No Budget Used"])

            ax.set_title("Budget Allocation")
            st.pyplot(fig)
            plt.close(fig)

        with chart_col2:
            st.subheader("📈 Selected Item Benefits")

            if selected:
                chart_df = pd.DataFrame(selected)
                chart_df = chart_df.set_index("Item")

                st.bar_chart(chart_df["Value"])
            else:
                st.info("No selected items to display.")

        # DP Table
        with st.expander("🔍 View Dynamic Programming Table"):

            st.write(
                "Rows represent items and columns represent "
                "different budget capacities."
            )

            dp_df = pd.DataFrame(result["dp"])

            st.dataframe(
                dp_df,
                use_container_width=True
            )

        # Algorithm explanation
        with st.expander("📚 Algorithm Explanation"):

            st.markdown("""
            ### 0–1 Knapsack Algorithm

            The algorithm uses Dynamic Programming to find
            the maximum benefit within a fixed budget.

            **Recurrence Relation:**

            `DP[i][w] = max(DP[i-1][w], Value[i] + DP[i-1][w-Cost[i]])`

            **Complexity:**

            - Time Complexity: O(n × W)
            - Space Complexity: O(n × W)

            Each item can be selected only once.
            """)

    except Exception as error:
        st.error(f"Optimization Error: {error}")

else:
    st.warning("Please add at least one item.")
