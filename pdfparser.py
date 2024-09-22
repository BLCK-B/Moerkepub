import pdfplumber
import pikepdf
import text_processor


def extract_and_modify_text(input_pdf_path, output_pdf_path):
    with pikepdf.open(input_pdf_path) as pdf:
        with pdfplumber.open(input_pdf_path) as pdfplumb:
            for page_number, page in enumerate(pdf.pages):
                extracted_text = pdfplumb.pages[page_number].extract_text()
                if extracted_text:
                    text = extracted_text.replace('\n', ' ').strip()
                    sentences = text_processor.split_sentences(text)
                    for i, sentence in enumerate(sentences):
                        sentences[i] = sentences[i].strip()
                        if not (sentence.endswith('.') or sentence.endswith('!') or sentence.endswith('?')):
                            sentences[i] += '.'

                    # modified_text = ''.join(text_processor.translate(sentences, batch_size=4, name="heythere"))
                    # modified_text = ''.join(sentences)

                    modified_text = extracted_text

        pdf.save(output_pdf_path)


input_pdf_path = r"sideTesting/testpdf.pdf"
output_pdf_path = r"sideTesting/output/exportPDF.pdf"

extract_and_modify_text(input_pdf_path, output_pdf_path)
