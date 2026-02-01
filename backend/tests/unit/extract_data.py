import pandas as pd
import re

def get_snippet(text, term, context_words=5):
    """
    Finds the 'term' in 'text' and returns it with a 
    specified number of words before and after.
    """
    # Handle empty or non-string values
    if not isinstance(text, str) or not isinstance(term, str) or term.strip() == "":
        return "Not Found"
    
    clean_term = term.strip()
    
    # Escape special characters (like parentheses) so they don't break the Regex
    pattern_str = re.escape(clean_term)
    
    # Add word boundaries (\b) only if the term starts/ends with alphanumeric characters
    # This prevents "Director" from matching "Directors" or "Subdirector"
    if clean_term[0].isalnum():
        pattern_str = r'\b' + pattern_str
    if clean_term[-1].isalnum():
        pattern_str = pattern_str + r'\b'
        
    try:
        pattern = re.compile(pattern_str, re.IGNORECASE)
        match = pattern.search(text)
        
        if not match:
            return "Not Found"
        
        start, end = match.span()
        matched_text = text[start:end]
        
        # Split the text into words based on whitespace
        before_text = text[:start]
        before_words = before_text.split()
        snippet_before = " ".join(before_words[-context_words:])
        if len(before_words) > context_words:
            snippet_before = "... " + snippet_before
            
        after_text = text[end:]
        after_words = after_text.split()
        snippet_after = " ".join(after_words[:context_words])
        if len(after_words) > context_words:
            snippet_after = snippet_after + " ..."
            
        return f"{snippet_before} {matched_text} {snippet_after}".strip()
    
    except Exception:
        return "Error Processing"

def main():
    input_file = 'gold_jobs_updated.csv'
    output_file = 'gold_jobs_with_snippets.csv'
    
    print(f"Loading {input_file}...")
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: {input_file} not found in this folder.")
        return

    print("Processing snippets (this may take a moment)...")
    
    # Apply the function to create the new columns
    # Column names match your description: 'job_title', 'company_name', 'job_description'
    df['title_snippet'] = df.apply(
        lambda row: get_snippet(row['job_description'], row['job_title']), axis=1
    )
    
    df['company_snippet'] = df.apply(
        lambda row: get_snippet(row['job_description'], row['company_name']), axis=1
    )

    # Save to a new CSV
    df.to_csv(output_file, index=False)
    print(f"Success! Processed file saved as: {output_file}")

if __name__ == "__main__":
    main()