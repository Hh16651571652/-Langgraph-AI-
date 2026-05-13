import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from config.db_config import get_database
from utils.session_auth import get_current_user_id_from_session
from crud import auth_crud

router = APIRouter(
    prefix="/upload",
    tags=["文件上传"]
)

# 定义头像存储目录
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

def validate_image(file: UploadFile):
    """校验图片格式和大小"""
    if file.content_type not in ["image/png", "image/jpeg", "image/webp"]:
        raise HTTPException(status_code=400, detail="不支持的图片格式")
    
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="图片大小不能超过2MB")
    
    # 重置文件指针
    file.file.seek(0)
    return content

@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db = Depends(get_database),
    current_user_id: int = Depends(get_current_user_id_from_session)
):
    """上传用户头像"""
    try:
        # 校验文件
        content = validate_image(file)
        
        # 生成唯一文件名
        ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # 保存图片
        with open(filepath, "wb") as f:
            f.write(content)
            
        # 更新数据库中的 avatar_url
        avatar_url = f"/{filepath}"
        await auth_crud.update_user_info(db, current_user_id, avatar_url=avatar_url)
        
        return {
            "code": 200,
            "message": "头像上传成功",
            "data": {"avatar_url": avatar_url}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
