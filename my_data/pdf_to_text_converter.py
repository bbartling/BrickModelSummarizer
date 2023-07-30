import os
import pdfplumber

def extract_text_from_pdf(pdf_file):
    extracted_text = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text.append(page.extract_text())

    return extracted_text

def save_text_to_file(text_data, output_dir, output_file):
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, "w", encoding="utf-8") as file:
        for text in text_data:
            file.write(text + "\n")
    return output_path  # Return the full path of the saved file

def process_all_pdfs_in_current_directory():
    current_directory = "."  # Representing the current directory
    pdf_files = [f for f in os.listdir(current_directory) if f.lower().endswith(".pdf")]
    
    print("Found these PDFs:\n", pdf_files)
    print("This may take a while...")

    if not pdf_files:
        print("No PDF files found in the current directory.")
        return

    for pdf_file in pdf_files:
        print("Doing: ", pdf_file)
        pdf_path = os.path.join(current_directory, pdf_file)

        # Step 1: Extract text from the PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        # Step 2: Create the output text file name with the same name as the PDF but with ".txt" extension
        output_file = os.path.splitext(pdf_file)[0] + ".txt"

        # Step 3: Save the extracted text to the text file in the current directory
        output_path = save_text_to_file(extracted_text, current_directory, output_file)

        print("Done with: ", pdf_file)
        print(f"Text file saved to: {output_path}")

if __name__ == "__main__":
    process_all_pdfs_in_current_directory()
