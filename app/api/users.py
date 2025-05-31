from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.user import UserResponse
from app.services.user_service import (
    authenticate_user,
    delete_user,
    get_user,
    register_user,
)

router = APIRouter()


@router.post("/users/register", response_model=UserResponse)
async def register(user_id: str = Form(...), image: UploadFile = File(...)):
    """회원 등록 엔드포인트"""
    image_data = await image.read()
    registered_user = register_user(user_id, image_data)

    return UserResponse(
        user_id=registered_user["user_id"],
        registered_at=registered_user["registered_at"],
    )


@router.post("/users/authenticate")
async def authenticate(image: UploadFile = File(...)):
    """회원 인증 엔드포인트"""
    image_data = await image.read()
    user_id = authenticate_user(image_data)

    if user_id is None:
        raise HTTPException(status_code=401, detail="인증 실패: 사용자 없음")

    return {"user_id": user_id}


@router.get("/users/{user_id}")
def get_user_info(user_id: str):
    """회원 정보 조회 엔드포인트"""
    user_info = get_user(user_id)

    if user_info is None:
        raise HTTPException(status_code=404, detail="사용자가 존재하지 않습니다.")

    return user_info


@router.delete("/users/{user_id}")
def delete_user_info(user_id: str):
    """회원 삭제 엔드포인트"""
    result = delete_user(user_id)

    if not result:
        raise HTTPException(status_code=404, detail="사용자가 존재하지 않습니다.")

    return {"message": "사용자가 성공적으로 삭제 되었습니다."}
