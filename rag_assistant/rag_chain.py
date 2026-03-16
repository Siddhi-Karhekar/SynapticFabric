import ollama


def generate_answer(context, query):
    if not context or not query:
        return "Context or query is missing."

    prompt = f"""You are an industrial AI assistant.
Answer the question using the context below.
Keep the answer SHORT (2–3 sentences max).

Context:
{context}

Question:
{query}
"""

    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": "You are a helpful industrial AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.get("message", {}).get("content", "No response from model.")

    except Exception as e:
        print(f"LLM ERROR: {e}")
        return "AI model error while generating response."