import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessage
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_practice_questions(course_name, unit_number):
    course_prompts = {
        "AP Psychology": "You're an AP Psychology teacher.",
        "AP Calculus AB": "You're an AP Calculus AB teacher. Focus on rigorous multiple-choice questions involving concepts like limits, derivatives, and integrals.",
        "AP US History": "You're an AP US History teacher. Ask historical analysis questions with references to specific time periods and document-based reasoning."
    }

    if course_name not in course_prompts:
        return {"error": "Practice questions for this course are not yet supported."}

    prompt = (
        f"{course_prompts[course_name]} Generate 5 CollegeBoard-style multiple-choice practice questions "
        f"from Unit {unit_number}. Each question must include:\n"
        f"- 1 correct answer\n"
        f"- 3 plausible distractors\n\n"
        f"Return the result as a JSON array of objects with keys: 'question', 'choices' (list), and 'answer'."
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content

