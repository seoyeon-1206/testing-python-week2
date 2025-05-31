def test_register_user_api(client):
    image_path = "images/Aaron_Peirsol/Aaron_Peirsol_0001.jpg"
    user_id = "aaron_peirsol"

    with open(image_path, "rb") as img_file:
        response = client.post(
            "/users/register",
            data={"user_id": user_id},
            files={"image": ("user1.jpg", img_file, "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["registered_at"] is not None


def test_authenticate_user_api(client, setup_user_db):
    image_path = "images/Aaron_Peirsol/Aaron_Peirsol_0001.jpg"

    with open(image_path, "rb") as img_file:
        response = client.post(
            "/users/authenticate",
            files={"image": ("user1.jpg", img_file, "image/jpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "aaron_peirsol"


def test_get_registered_user_api(client, setup_user_db):
    user_id = "aaron_peirsol"

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert "registered_at" in data


def test_delete_registered_user_api(client, setup_user_db):
    user_id = "aaron_peirsol"

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
