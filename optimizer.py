
def solve_knapsack(items, capacity):

    capacity = max(0, int(capacity))

    normalized = []

    for item in items:
        cost = int(item["Cost"])
        value = int(item["Value"])

        if cost > 0 and value > 0:
            normalized.append({
                "Item": str(item["Item"]),
                "Cost": cost,
                "Value": value
            })

    n = len(normalized)

    # Create DP table
    dp = [
        [0] * (capacity + 1)
        for _ in range(n + 1)
    ]

    # Fill DP table
    for i in range(1, n + 1):

        cost = normalized[i - 1]["Cost"]
        value = normalized[i - 1]["Value"]

        for w in range(capacity + 1):

            if cost <= w:

                dp[i][w] = max(
                    dp[i - 1][w],
                    value + dp[i - 1][w - cost]
                )

            else:
                dp[i][w] = dp[i - 1][w]

    # Recover selected items
    selected = []

    w = capacity

    for i in range(n, 0, -1):

        if dp[i][w] != dp[i - 1][w]:

            selected.append(normalized[i - 1])

            w -= normalized[i - 1]["Cost"]

    selected.reverse()

    return {
        "max_value": dp[n][capacity],
        "selected": selected,
        "dp": dp
    }
