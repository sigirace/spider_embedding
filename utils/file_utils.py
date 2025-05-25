import os
import hashlib
import shutil
from fastapi import UploadFile

BASE_DIR = os.path.abspath(
    os.path.dirname(os.path.dirname(__file__))
)  # 현재 파일 기준 절대 경로
DATA_DIR = os.path.join(BASE_DIR, "static/data")  # 최상위 ./static/data 디렉토리


async def compute_file_hash(file: UploadFile) -> str:
    """SHA-256 해시를 비동기적으로 계산"""
    hasher = hashlib.sha256()
    while chunk := await file.read(8192):
        hasher.update(chunk)
    await file.seek(0)
    return hasher.hexdigest()


async def save_file(
    file: UploadFile,
    file_path: str,  # app_id/source
) -> str:
    # 저장 경로 구성
    save_dir = os.path.join(DATA_DIR, file_path)
    os.makedirs(save_dir, exist_ok=True)

    dest_path = os.path.join(save_dir, file.filename)

    # 파일 저장
    with open(dest_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return dest_path


def rename_file(
    file_path: str,  # app_id/source
    old_filename: str,  # 기존 파일 이름 (ex: old.pdf)
    new_filename: str,  # 새 파일 이름 (ex: new.pdf)
) -> str:
    """
    static/data/{file_path}/{old_filename} → {new_filename} 으로 이름 변경

    Returns:
        변경된 파일의 전체 경로
    """
    dir_path = os.path.join(DATA_DIR, file_path)  # ./static/data/app_id/source
    old_path = os.path.join(
        dir_path, old_filename
    )  # ./static/data/app_id/source/old.pdf
    new_path = os.path.join(
        dir_path, new_filename
    )  # ./static/data/app_id/source/new.pdf

    if not os.path.isfile(old_path):
        raise FileNotFoundError(f"파일이 존재하지 않습니다: {old_path}")

    os.rename(old_path, new_path)

    return new_path


def delete_file(file_path: str) -> bool:
    try:
        # 절대 경로 확인 및 보안 검사
        full_path = os.path.abspath(file_path)

        if not full_path.startswith(DATA_DIR):
            raise ValueError("경로 보안 위반: 허용되지 않은 경로입니다.")

        if os.path.exists(full_path):
            os.remove(full_path)

        return True

    except Exception as e:
        raise e


def create_folder(app_id: str) -> bool:
    try:
        full_path = os.path.abspath(os.path.join(DATA_DIR, app_id))
        os.makedirs(full_path, exist_ok=True)
        return True
    except Exception as e:
        raise e


def delete_folder(app_id: str) -> bool:
    try:
        # 절대 경로로 변환
        full_path = os.path.abspath(os.path.join(DATA_DIR, app_id))

        # 보안 확인: ./data 내부인지 확인
        if not full_path.startswith(DATA_DIR):
            raise ValueError("경로 보안 위반: data 디렉토리 내부만 삭제 가능")

        if os.path.exists(full_path) and os.path.isdir(full_path):
            shutil.rmtree(full_path)
            return True

    except Exception as e:
        raise e


def save_extracted_image(
    image_bytes: bytes,
    file_path: str,  # app_id/meta_id ex) ABCD/1234~Z
    filename: str,  # 1_1.png
) -> str:

    # 저장 경로 구성
    save_dir = os.path.join(DATA_DIR, file_path)
    os.makedirs(save_dir, exist_ok=True)

    dest_path = os.path.join(save_dir, filename)

    # 파일 저장
    with open(dest_path, "wb") as buffer:
        buffer.write(image_bytes)

    return dest_path


def get_image_path(file_path: str) -> str:
    save_dir = os.path.join(DATA_DIR, file_path)

    # 디렉토리 재생성
    os.makedirs(save_dir, exist_ok=True)

    return save_dir


def delete_image_folder(file_path: str) -> None:
    save_dir = os.path.join(DATA_DIR, file_path)

    if os.path.exists(save_dir):
        # 하위 파일 및 디렉토리 전체 삭제
        shutil.rmtree(save_dir)
