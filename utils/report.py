def generate_pdf_report(plan_text: str, output_path: str = "camping_plan.pdf"):
    """Stub: write plan text to a .txt file as a stand-in for PDF."""
    txt_path = output_path.replace(".pdf", ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(plan_text)
