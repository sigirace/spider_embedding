import re
from pymupdf4llm import to_markdown
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


# ✅ 이미지 추출 & 제거
def extract_images_and_clean_text(md_text: str) -> tuple[str, list[str]]:
    pattern = r"!\[\]\((.*?)\)"
    image_paths = re.findall(pattern, md_text)
    cleaned_text = re.sub(pattern, "", md_text)
    return cleaned_text.strip(), image_paths


# ✅ 헤딩 추출: # ~ #### 까지 포함
def extract_tags(md_text: str) -> list[str]:
    lines = md_text.splitlines()
    tags = []
    for line in lines:
        match = re.match(r"^#{1,4} (.+)", line)
        if match:
            tags.append(match.group(1).strip().replace("*", ""))
    return tags


# ✅ 텍스트 분할기
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""],
)

# ✅ PDF → 페이지 단위 마크다운
page_chunks = to_markdown(
    doc="./test_files/pdfs/mydata.pdf",
    page_chunks=True,
    force_text=True,
    use_glyphs=True,
    write_images=True,
    image_path="./test_files/outputs/images",
    show_progress=True,
)

documents = []

for i, chunk in enumerate(page_chunks):
    raw_md = chunk.get("text", "")

    # 이미지 + 태그 추출
    cleaned_text, image_paths = extract_images_and_clean_text(raw_md)
    tags = extract_tags(raw_md)

    base_metadata = {
        "source": "mydata.pdf",
        "page": i + 1,
        "tags": tags,
        **chunk.get("metadata", {}),
    }

    # 페이지 문서 → 청크 분할
    base_doc = Document(page_content=cleaned_text, metadata=base_metadata)
    split_docs = text_splitter.split_documents([base_doc])

    for j, sub_doc in enumerate(split_docs):
        if j == 0 and image_paths:
            sub_doc.metadata["images"] = image_paths
        documents.append(sub_doc)

for i, doc in enumerate(documents):
    print("page: ", doc.metadata.get("page", ""))
    print("tags: ", doc.metadata.get("tags", []))
    print("images: ", doc.metadata.get("images", []))
    print("text: ", doc.page_content.replace("#", "").replace("*", ""))
    print("-" * 40)
