from transformers import pipeline
import os
import sys
generator = pipeline("text-generation", model="gpt2")

def simple_chat(user_input):
    prompt = f"""
You are BuildSense AI, a construction assistant.

User: {user_input}

Answer professionally and concisely.
"""

    result = generator(
        prompt,
        max_length=150,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.9
    )

    full_output = result[0]["generated_text"]
    response = full_output.replace(prompt, "").strip()

    if not response or len(response) < 10:
        return "Try optimizing materials, reducing labor cost, and simplifying the project."

    return response

def detect_intent(user_input):
    text = user_input.lower()

    if "reduce" in text or "improve" in text or "optimize" in text:
        return "advice"
    elif "cost" in text or "estimate" in text:
        return "predict"
    elif "what if" in text or "change" in text:
        return "what_if"
    else:
        return "general"
sys.path.append(os.path.abspath("../models"))
from predict import predict_with_dcs

def handle_query(user_input, features):
    intent = detect_intent(user_input)

    if intent == "predict":
        result = predict_with_dcs(features)

        return f"""
Estimated Cost: ₹{result['estimated_cost']:.2f}
Estimated Time: {result['estimated_time']:.0f} days
Risk: {result['risk_level']}
DCS Score: {result['dcs_score']}
"""

    elif intent == "advice":
        return "To reduce cost, you can use medium-quality materials, optimize labor usage, reduce project complexity, and improve efficiency."

    elif intent == "general":
        return simple_chat(user_input)

    return "I couldn't understand your request."



