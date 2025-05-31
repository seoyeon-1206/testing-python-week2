from typing import Union

import numpy as np
from deepface import DeepFace


def extract_embedding(img_path: Union[str, np.ndarray]) -> list:
    """이미지에서 임베딩 추출"""
    embedding = DeepFace.represent(img_path)[0]["embedding"]
    return embedding


def verify_embedding(embedding1: list, embedding2: list) -> bool:
    """두 임베딩이 같은 사람인지 검증"""
    is_same_person = DeepFace.verify(embedding1, embedding2)["verified"]
    return is_same_person
