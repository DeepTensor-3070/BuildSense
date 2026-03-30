def generate_smart_insights(features, prediction):
    insights = []

    # 🔴 Weather risk
    if features["weather_index"] > 0.6:
        insights.append("⚠️ High risk due to adverse weather conditions")

    # 🔴 Project complexity
    if features["project_complexity"] >= 3:
        insights.append("⚠️ Complex project structure may cause delays")

    # 🔴 Soil issues
    if features["soil_type"] == 3:
        insights.append("⚠️ Poor soil quality may increase foundation cost")

    # 🔴 Low efficiency
    if features["efficiency"] < 3:
        insights.append("⚠️ Low contractor efficiency may impact timeline")

    # 🔴 High inflation
    if features["inflation_factor"] > 1.2:
        insights.append("⚠️ Rising inflation may increase material costs")

    # 🟡 Cost warning
    if prediction["estimated_cost"] > 1500000:
        insights.append("💰 High project cost detected")

    # 🟡 Time warning
    if prediction["estimated_time"] > 120:
        insights.append("⏱️ Extended timeline expected")

    # 🟢 Positive insight
    if prediction["dcs_score"] > 80:
        insights.append("✅ Project is well-optimized with low risk")

    return insights