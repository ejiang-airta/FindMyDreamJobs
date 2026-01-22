# File: /backend/app/utils/codex_cli.py
# This script is a command-line interface for OpenAI's Codex model.
# It allows users to send prompts to the model and receive code completions.
import sys
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("Error: OPENAI_API_KEY environment variable not set")
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python codex_cli.py 'Your prompt here'")
        sys.exit(1)

    prompt = sys.argv[1]

    # Detect if argument is a filename
    if os.path.isfile(prompt):
        with open(prompt, 'r') as f:
            prompt = f.read()
   

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=1500,
    )

    print("\n=== Codex Response ===\n")
    print(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    main()

