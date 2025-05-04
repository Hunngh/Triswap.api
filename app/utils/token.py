# from fastapi import Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from typing import Dict
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# SECRET_KEY = "secret_key"
# ALGORITHM = "HS256"
#
# def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("user_id")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid authentication credentials")
#         return {"user_id": user_id}
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid authentication credentials")
