import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from config.db_config import get_database
from utils.session_auth import get_current_user_id_from_session
from crud import auth_crud, session_crud
from sqlalchemy import select
from model.user_model import User

router = APIRouter(
    prefix="/upload",
    tags=["文件上传"]
)

# 定义头像存储目录
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

async def get_user_id_fast(
    authorization: str = Header(...),
    db = Depends(get_database)
) -> int:
    """
    快速获取用户ID（优化版）
    直接从token查询，减少不必要的验证步骤
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证令牌")
    
    token = authorization[7:]  # 去掉 "Bearer " 前缀
    
    # 直接查询session，不检查过期时间（加快速度）
    from model.session_token_model import SessionToken
    result = await db.execute(
        select(SessionToken.user_id).where(
            SessionToken.token == token,
            SessionToken.is_active == True
        )
    )
    user_id = result.scalar_one_or_none()
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Token无效")
    
    return user_id

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
    current_user_id: int = Depends(get_user_id_fast)  # 使用快速认证
):
    """上传用户头像"""
    try:
        # 校验文件
        content = validate_image(file)
        
        # 生成唯一文件名
        ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # 保存图片（同步操作，快速）
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
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")
