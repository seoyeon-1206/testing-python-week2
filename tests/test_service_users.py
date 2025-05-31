from app.services.user_service import (
    authenticate_user,
    delete_user,
    get_user,
    register_user,
)


def test_register_user():
    # Given: 사용자의 ID와 얼굴 이미지가 주어짐
    image_path = "images/Aaron_Peirsol/Aaron_Peirsol_0001.jpg"
    user_id = "aaron_peirsol"

    # When: 사용자 등록 기능을 실행
    with open(image_path, "rb") as f:
        image_data = f.read()
        result = register_user(user_id, image_data)

    # Then: 사용자 등록 기능이 성공
    assert result["user_id"] == "aaron_peirsol"
    assert result["registered_at"] is not None


def test_authenticate_registered_user(setup_user_db):
    # Given: 이미 등록된 사용자의 얼굴이미지가 주어짐
    image_path = "images/Aaron_Peirsol/Aaron_Peirsol_0001.jpg"

    # When: 등록된 사용자와 동일한 인물의 얼굴 이미지를 제출
    with open(image_path, "rb") as f:
        image_data = f.read()
        user_id = authenticate_user(image_data)

    # Then: 인증 기능이 성공하여 사용자 ID를 반환
    assert user_id == "aaron_peirsol"


def test_authenticate_unregistered_user(setup_user_db):
    # Given: 등록되지 않은 사용자의 얼굴 이미지
    image_path = "images/Natasha_McElhone/Natasha_McElhone_0001.jpg"
    with open(image_path, "rb") as f:
        image_data = f.read()

    # When: 인증 서비스를 호출
    user_id = authenticate_user(image_data)

    # Then: 인증 실패(None 반환) 해야 함
    assert user_id is None


def test_get_registered_user(setup_user_db):
    # Given: 이미 등록된 사용자 ID
    user_id = "aaron_peirsol"

    # When: 사용자 정보 조회 서비스를 호출
    user_info = get_user(user_id)

    # Then: 등록 시각 등 사용자 정보를 정확히 반환해야 함
    assert user_info["user_id"] == user_id
    assert "registered_at" in user_info


def test_delete_registered_user(setup_user_db):
    # Given: 이미 등록된 사용자 ID
    user_id = "aaron_peirsol"

    # When: 사용자 삭제 서비스를 호출하면
    result = delete_user(user_id)

    # Then: 삭제가 성공적으로 이루어졌음을 반환
    assert result is True

    # 추가 확인: 사용자가 실제로 삭제되었는지 조회하여 확인
    user_info = get_user(user_id)
    assert user_info is None


def test_get_unregistered_user(setup_user_db):
    # Given: 등록되지 않은 사용자 ID
    user_id = "unknown_user"

    # When: 사용자 정보 조회 서비스를 호출
    user_info = get_user(user_id)

    # Then: 사용자 정보 조회 서비스가 None을 반환해야 함
    assert user_info is None
