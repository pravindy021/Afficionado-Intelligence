from typing import Any

import pandas as pd

from app.services.analytics import core_metrics, category_analytics, pareto_analysis, product_ranking


def copilot_answer(question: str, frame: pd.DataFrame) -> dict[str, Any]:
    text = question.lower()
    metrics = core_metrics(frame)
    products = product_ranking(frame)
    categories = category_analytics(frame)
    pareto = pareto_analysis(frame)

    if "most revenue" in text or "top product" in text:
        top = products[0]
        answer = f"{top['product_detail']} has the highest source revenue at ${top['revenue']:,.2f}."
        evidence = [{"metric": "product_revenue", "value": top["revenue"], "product": top["product_detail"]}]
        followups = ["Compare this product with the second-ranked product.", "What segment does this product belong to?"]
    elif "category" in text:
        top = categories[0]
        answer = f"{top['product_category']} is the largest category by source revenue at ${top['revenue']:,.2f}."
        evidence = [{"metric": "category_revenue", "value": top["revenue"], "category": top["product_category"]}]
        followups = ["Which stores perform best for this category?", "Which products drive this category?"]
    elif "pareto" in text or "concentration" in text:
        top_share = sum(float(row["revenue_share"]) for row in pareto[:10])
        answer = f"The top 10 products contribute {top_share:.1%} of observed revenue."
        evidence = [{"metric": "top_10_revenue_share", "value": round(top_share, 6)}]
        followups = ["Which products are in the A class?", "Which products need investigation?"]
    elif "weak" in text or "least" in text or "bottom" in text:
        bottom = sorted(products, key=lambda row: row["revenue"])[:5]
        answer = "The five lowest-revenue products are " + ", ".join(row["product_detail"] for row in bottom) + "."
        evidence = [{"metric": "product_revenue", "value": row["revenue"], "product": row["product_detail"]} for row in bottom]
        followups = ["Should low sales lead to removal?", "How do units and revenue compare?"]
    else:
        answer = (
            f"The source dataset has ${metrics['total_revenue']:,.2f} of calculated revenue, "
            f"{metrics['total_quantity']} units, and {metrics['transaction_count']} source transactions."
        )
        evidence = [{"metric": key, "value": value} for key, value in metrics.items()]
        followups = ["Which product generates the most revenue?", "Which category dominates revenue?", "Explain the Pareto distribution."]
    return {
        "answer": answer,
        "evidence": evidence,
        "follow_up_questions": followups,
        "analysis_period": "2025 source year",
        "limitations": ["Revenue is sales value, not profit.", "No complete basket or calendar-date forecasting is supported."],
    }
