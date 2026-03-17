import ollama


def generate_answer(context, query):
    if not context or not query:
        return "Context or query is missing."

    prompt = f"""
You are an industrial AI assistant working in an automotive manufacturing plant.

STRICT RULES:
- Always use machine FULL names (CNC Milling, Lathe, etc.)
- NEVER use IDs like M_1, M_2
- Mention possible failure causes if relevant
- Keep answer VERY SHORT (max 2 sentences)

Context:
{context}

Question:
{query}
"""

    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": "You are a professional industrial AI assistant."},
                {"role": "user", "content": prompt}
            ],
            options={
                "num_predict": 100,
                "temperature": 0.3
            }
        )

        return response.get("message", {}).get("content", "No response from model.")

    except Exception as e:
        print(f"LLM ERROR: {e}")
        return "AI model error while generating response."