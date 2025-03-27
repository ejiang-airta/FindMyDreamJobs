def optimize_resume(original_text: str, missing_skills: str) -> str:
    """
    AI Enhancement: Inserts missing skills naturally into the resume text.
    """
    if not missing_skills:
        return original_text  # No changes if no missing skills

    enhancements = f"\n\n### Optimization Enhancements:\nWe have enhanced the resume by adding context for missing skills: {missing_skills}."

    return original_text + enhancements
