from google import genai
from dotenv import load_dotenv
import yaml
from rich.console import Console
from rich.markdown import Markdown


load_dotenv()

gemini_model = [
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
    "gemini-3-pro-preview",
    "gemini-2.5-pro",
]

assignment_keys = {
    "fuel": "assignments/fuel.yaml"
}

def main():
    while True:
        try:
            assignment_name = input("Assignment Name: ").lower()
            assignment = load_yaml(assignment_keys[assignment_name])
            break
        except (ValueError, KeyError):
            pass
    
    ai_core = load_yaml("ai_core.yaml")

    current_code = input("Current_code?: ")
    output_error = input("Error?: ")
    question = input("Question?: ")

    ai_answer = generate_answer(assignment, ai_core, current_code, output_error, question)

    console = Console()
    md = Markdown(ai_answer)
    console.print(md)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def call_ai(prompt: str) -> str:
    client = genai.Client()

    response = client.models.generate_content(model=gemini_model[0], contents=prompt)
    return response.text


def build_prompt(assignment, ai_core, current_code, output_error, question):
    return f"""
    You are an programming tutor that help student learn how to code Focus on guiding, give an example and hint.

    Assignment Detail below:

    Assignment name: {assignment["assignment_name"]}

    Assignment description:
    {assignment["assignment_desc"]}

    Learning focus on:
    {assignment["assignment_tags"]}

    Difficulty Level:
    {assignment["assignment_level"]}

    Reference solution (correct behavior (optional)):
    {assignment["solution_code"]}

    Assignment Constraint[A MUST]:
    {assignment["assignment_constraint"]}

    Requirements[A MUST]:
    {ai_core["requirements"]}
    _______________________________

    Student prompt below:

    Current code (Can be empty):
    {current_code}
    
    > Give completation signal
    if student complete assignment or acceptable answer, No need to perfection just for learning purposes.
    > Also give lesson reviews after finished that make sure they understan the topic

    Output Error (Can be empty):
    {output_error}

    Student Question (If empty just help them to get started):
    {question}
    """


def generate_answer(
    assignment,
    ai_core,
    current_code,
    output_error,
    question
):
    prompt = build_prompt(assignment, ai_core, current_code, output_error, question)

    answer = call_ai(prompt)

    return answer


if __name__ == "__main__":
    main()
