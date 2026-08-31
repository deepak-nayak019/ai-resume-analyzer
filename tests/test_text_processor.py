from app.text_processor import clean_text


sample_text = """
Deepak Nayak
Python Developer!

Email: deepak@gmail.com
GitHub: https://github.com/deepak

Skills: Python, SQL, Pandas, NumPy.
"""


cleaned = clean_text(sample_text)

print("Original Text:")
print(sample_text)

print("\nCleaned Text:")
print(cleaned)