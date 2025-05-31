import pytest
from fastapi.testclient import TestClient

from app.face.face_db import save_user
from app.face.face_embedding import extract_embedding
from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def setup_user_db():
    image_paths = ["images/Aaron_Peirsol/Aaron_Peirsol_0001.jpg"]
    user_ids = ["aaron_peirsol"]
    for image_path, user_id in zip(image_paths, user_ids):
        embedding = extract_embedding(image_path)
        save_user(user_id, embedding)
    yield
