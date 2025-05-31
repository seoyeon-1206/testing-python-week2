from datetime import datetime

import cv2
import numpy as np

from app.face.face_db import load_db, save_db, save_user
from app.face.face_embedding import extract_embedding, verify_embedding


def register_user(user_id: str, image_bytes: bytes) -> dict:
    """이미지와 ID로 회원 등록"""
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    embedding = extract_embedding(image)
    save_user(user_id, embedding)
    return {"user_id": user_id, "registered_at": str(datetime.now())}


def authenticate_user(image_bytes: bytes):
    """이미지로 회원 인증"""
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    db = load_db()

    embedding_to_check = extract_embedding(image)

    for user_id, data in db.items():
        if verify_embedding(data["embedding"], embedding_to_check):
            return user_id

    return None  # 인증 실패


def get_user(user_id):
    """user_id로 회원 정보 조회"""
    db = load_db()
    user_data = db.get(user_id)

    if user_data:
        return {"user_id": user_id, "registered_at": user_data["registered_at"]}
    else:
        return None  # 사용자 없음


def delete_user(user_id):
    """user_id로 회원 삭제"""
    db = load_db()
    if user_id in db:
        del db[user_id]
        save_db(db)
        return True
    return False
