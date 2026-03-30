def evaluate_scenario(result, goal="balanced"):
    cost = result["estimated_cost"]
    time = result["estimated_time"]
    dcs = result["dcs_score"]

    if goal == "min_cost":
        return -cost

    elif goal == "fastest":
        return -time

    elif goal == "max_quality":
        return dcs

    elif goal == "balanced":
        return (dcs * 1000) - (cost * 0.001) - (time * 10)

    return dcs

def find_best_scenario(base_result, scenarios):
    best = None
    best_score = float("-inf")

    for s in scenarios:
        if "result" not in s:
            continue

        score = evaluate_scenario(s["result"])
        s["score"] = score

        if score > best_score:
            best_score = score
            best = s

    return best

def generate_copilot_advice(best, base):
    if not best:
        return "No valid scenario found."

    cost_diff = best["impact"]["cost_change"]
    time_diff = best["impact"]["time_change"]
    dcs_diff = best["impact"]["dcs_change"]

    advice = f"""
🏆 Best Scenario: {best['scenario']}

📉 Cost Change: ₹{cost_diff}
⏱ Time Change: {time_diff} days
📊 DCS Improvement: {dcs_diff}

💡 Recommendation:
This scenario offers the best balance between cost, time, and efficiency.
"""

    if cost_diff < 0:
        advice += "\n✔ Reduces overall cost"
    if time_diff < 0:
        advice += "\n✔ Faster project completion"
    if dcs_diff > 0:
        advice += "\n✔ Improves decision confidence score"

    return advice

def rank_scenarios(base_result, scenarios, goal):
    ranked = []

    for s in scenarios:
        if "result" not in s:
            continue

        score = evaluate_scenario(s["result"], goal)
        s["score"] = score
        ranked.append(s)

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked

def generate_smart_suggestions(best, base):
    suggestions = []

    if best["impact"]["cost_change"] > 0:
        suggestions.append("Reduce material quality to lower cost")

    if best["impact"]["time_change"] > 0:
        suggestions.append("Improve labor efficiency to reduce time")

    if best["impact"]["dcs_change"] < 0:
        suggestions.append("Increase contractor experience or equipment availability")

    if not suggestions:
        suggestions.append("This scenario is already well optimized")

    return suggestions

from genai import generate_whatif_insight
def generate_llm_explanation(base, best):
    try:
        return generate_whatif_insight(
            base,
            best["result"],
            best["impact"]
        )
    except:
        return "AI explanation unavailable"
    

def copilot_engine(base_result, scenarios, goal):
    ranked = rank_scenarios(base_result, scenarios, goal)

    best = ranked[0] if ranked else None

    suggestions = generate_smart_suggestions(best, base_result)
    llm_explanation = generate_llm_explanation(base_result, best)

    return {
        "best": best,
        "ranked": ranked,
        "suggestions": suggestions,
        "llm_explanation": llm_explanation
    }