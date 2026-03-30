from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="google/flan-t5-small"
)

def generate_whatif_insight(base, modified, impact):

    prompt = f"""
You are a construction AI expert.

Base:
Cost: {base['estimated_cost']}
Time: {base['estimated_time']}
Risk: {base['risk']['label']}

Modified:
Cost: {modified['estimated_cost']}
Time: {modified['estimated_time']}
Risk: {modified['risk']['label']}

Impact:
Cost change: {impact['cost_change']}
Time change: {impact['time_change']}
DCS change: {impact['dcs_change']}

Explain briefly:
- Why changes happened
- What actions to take
"""

    result = generator(prompt, max_length=150, temperature=0.7)

    return result[0]["generated_text"].strip()


