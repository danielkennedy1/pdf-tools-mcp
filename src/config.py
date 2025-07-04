import re

allowed_prefixes = [
    "merged_",
    "snippet_",
    # Add more prefixes here as needed
]
# Join the prefixes with | for alternation and make the entire group optional
prefix_pattern = f"(?:{'|'.join(re.escape(prefix) for prefix in allowed_prefixes)})?"
uuid4_pdf_re = re.compile(r".*(\.pdf|\.PDF)$")
