from docxtpl import DocxTemplate

# Load the template
doc = DocxTemplate("resume_template.docx")

# Define the context
context = {
    'full_name': 'JOHN DOE',
    'location': 'Vancouver, BC',
    'email': 'abc@abc.com',
    'phone': '+1 (123) 456-7890',
    'linkedIn': 'https://www.linkedin.com/in/johndoe',
    'sections': [
        {
            'title': 'Experience',
            'entries': [
                'Software Engineer at XYZ Corp | Jan 2020 - Present',
                'Developed scalable web applications using React and Node.js.'
            ]
        },
        {
            'title': 'Education',
            'entries': [
                'B.Sc. in Computer Science, University of British Columbia'
            ]
        }
    ]
}

print(context)

# Render the template with the context
doc.render(context)

# Save the rendered document to a new file
output_path = "output.docx"
doc.save(output_path)

print(f"Document saved to {output_path}")