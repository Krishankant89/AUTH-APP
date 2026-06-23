from fastapi import Depends, HTTPException, status
from typing import List
from app.schemas.token import TokenData
from app.auth.jwt import get_current_user

class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: TokenData = Depends(get_current_user)):
        if not current_user.scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No roles assigned"
            )
        for role in self.allowed_roles:
            if role in current_user.scopes:
                return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )

def check_roles(allowed_roles: List[str]):
    return RoleChecker(allowed_roles)