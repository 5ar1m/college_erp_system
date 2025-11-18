"""
Service for handling user authentication.
Corresponds to the "Authenticate User" process in the DFD.
"""
from typing import Optional
from source.college_erp.database import Database
from source.college_erp.models.user import User

def login(db: Database, user_id: str, password: str) -> Optional[User]:
    """
    Attempts to log a user in.
    
    Args:
        db: The database instance.
        user_id: The ID of the user trying to log in.
        password: The password provided by the user.

    Returns:
        The User object if authentication is successful, None otherwise.
    """
    user = db.get_user_by_id(user_id)
    
    if user and user.check_password(password):
        return user
    
    return None