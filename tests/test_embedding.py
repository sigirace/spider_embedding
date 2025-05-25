import fitz  # pymupdf
import os


def chunk_pdf_without_ocr(file_path, figures_directory="./test_files/figures"):
    if not os.path.exists(figures_directory):
        os.makedirs(figures_directory)

    doc = fitz.open(file_path)
    text_chunks = []
    image_chunks = []

    for page_index, page in enumerate(doc):
        # 텍스트 추출
        page_text = page.get_text("text")
        if page_text.strip():
            text_chunks.append(
                {"page": page_index + 1, "type": "text", "content": page_text.strip()}
            )

        # 이미지 추출
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page{page_index + 1}_img{img_index + 1}.{image_ext}"
            image_path = os.path.join(figures_directory, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_chunks.append(
                {
                    "page": page_index + 1,
                    "type": "image",
                    "file": image_path,
                }
            )

    return text_chunks, image_chunks


if __name__ == "__main__":
    # 테스트할 PDF 파일 경로
    pdf_path = "./test_files/pdfs/tech.pdf"
    figures_dir = "./test_files/figures/tech"

    text_chunks, image_chunks = chunk_pdf_without_ocr(pdf_path, figures_dir)

    print("=== 텍스트 청크 ===")
    for chunk in text_chunks:
        print(f"[Page {chunk['page']}]")
        print(chunk["content"])
        print("-" * 40)

    print("\n=== 이미지 청크 ===")
    for chunk in image_chunks:
        print(f"[Page {chunk['page']}] - {chunk['file']}")
        print("-" * 40)
