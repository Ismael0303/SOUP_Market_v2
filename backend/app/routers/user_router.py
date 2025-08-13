from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from app.database import get_db
from app.schemas import UsuarioResponse
from app.crud import user as crud_user
from app.dependencies import get_current_user
from app.models import Usuario

# Create an API router specifically for user-related endpoints
router = APIRouter()

@router.get("/me", response_model=UsuarioResponse)
def get_current_user_profile(current_user: Usuario = Depends(get_current_user)):
    """
    Retrieves the current user's profile information.
    Args:
        current_user: The current authenticated user (injected by dependency).
    Returns:
        The current user's data as a UsuarioResponse.
    """
    print(f"DEBUG: User ID: {current_user.id}, Email: {current_user.email}")
    print(f"DEBUG: User negocios: {current_user.negocios}")
    if current_user.negocios:
        print(f"DEBUG: First business ID: {current_user.negocios[0].id}")
    else:
        print("DEBUG: User has no associated businesses.")
    print(f"DEBUG: negocio_principal_id property: {current_user.negocio_principal_id}")
    return current_user

@router.put("/me", response_model=UsuarioResponse)
def update_current_user_profile(
    user_update: dict,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the current user's profile information.
    Args:
        user_update: A dictionary containing the fields to update.
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Returns:
        The updated user's data as a UsuarioResponse.
    Raises:
        HTTPException 404: If the user is not found.
    """
    # Update the user's profile in the database
    updated_user = crud_user.update_user_profile(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.put("/me/cv", response_model=UsuarioResponse)
def update_current_user_cv(
    cv_data: dict,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Updates the current freelancer's curriculum vitae.
    Args:
        cv_data: A dictionary containing CV details.
        current_user: The current authenticated user (injected by dependency).
        db: The SQLAlchemy database session dependency.
    Returns:
        The updated user's data with CV details as a UsuarioResponse.
    Raises:
        HTTPException 404: If the user is not found.
        HTTPException 403: If the user is not a freelancer.
    """
    # Update the user's CV in the database
    updated_user = crud_user.update_user_cv(db, current_user.id, cv_data)
    if not updated_user:
        # Check if user exists but is not a freelancer
        user = crud_user.get_user_by_id(db, current_user.id)
        if user and user.tipo_tier.value != "freelancer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only freelancers can update their CV"
            )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

class PluginUpdate(BaseModel):
    plugin_name: str
    action: str # "activate" or "deactivate"

@router.put("/me/plugins", response_model=UsuarioResponse)
def update_user_plugins(
    plugin_update: PluginUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Activates or deactivates a plugin for the current user.
    """
    if plugin_update.action == "activate":
        updated_user = crud_user.activate_plugin(db, current_user.id, plugin_update.plugin_name)
    elif plugin_update.action == "deactivate":
        updated_user = crud_user.deactivate_plugin(db, current_user.id, plugin_update.plugin_name)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid action. Use 'activate' or 'deactivate'."
        )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


