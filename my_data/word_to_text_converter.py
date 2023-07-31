import os
import docx

def extract_text_from_word_doc(word_file):
    extracted_text = []

    doc = docx.Document(word_file)
    for para in doc.paragraphs:
        extracted_text.append(para.text)

    return "\n".join(extracted_text)

def save_text_to_file(text_data, output_dir, output_file):
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text_data)
    return output_path  # Return the full path of the saved file

def process_all_word_docs_in_current_directory():
    current_directory = "."  # Representing the current directory
    word_files = [f for f in os.listdir(current_directory) if f.lower().endswith((".doc", ".docx"))]

    print("Found these Word documents:\n", word_files)
    print("This may take a while...")

    if not word_files:
        print("No Word documents found in the current directory.")
        return

    for word_file in word_files:
        print("Doing: ", word_file)
        word_path = os.path.join(current_directory, word_file)

        # Step 1: Extract text from the Word document
        extracted_text = extract_text_from_word_doc(word_path)

        # Step 2: Create the output text file name with the same name as the Word document but with ".txt" extension
        output_file = os.path.splitext(word_file)[0] + ".txt"

        # Step 3: Save the extracted text to the text file in the current directory
        output_path = save_text_to_file(extracted_text, current_directory, output_file)

        print("Done with: ", word_file)
        print(f"Text file saved to: {output_path}")

if __name__ == "__main__":
    process_all_word_docs_in_current_directory()
