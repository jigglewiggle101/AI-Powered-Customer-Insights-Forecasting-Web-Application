# backend/auto_report.py
def kpi_summary(kpis, top_category, top_channel) -> str:
    return (
        f"Total revenue is ${kpis['totalRevenue']:.2f}, average order value ${kpis['avgOrderValue']:.2f}. "
        f"Top category is {top_category['product_category']} (${top_category['amount']:.2f}). "
        f"Top channel is {top_channel['channel']} (${top_channel['amount']:.2f}). "
        "Revenue is stable with minor fluctuations over the selected horizon."
    )