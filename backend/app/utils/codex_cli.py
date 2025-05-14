# File: /backend/app/utils/codex_cli.py
# This script is a command-line interface for OpenAI's Codex model.
# It allows users to send prompts to the model and receive code completions.
import sys
import openai
import os

openai.api_key = "sk-proj-_lTeWxj3ERmgV-KOMDSj-INW8Z7_jSFEYACK0cF78EsgYAH9aZvGXg9T4PXfyC8AognP1m1IgXT3BlbkFJcdwx9RYTZnGqTXxrM0rzRtFzMEhFETGOVKStiiTMHfh_dyLONYC0QkZnmO-3hyFfR_1Z6V6a8AE"

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
