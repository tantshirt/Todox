"""
User repository
Database operations for user entities
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Optional

from ..models.user import UserInDB


class UserRepository:
    """Repository for user database operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.users
    
    async def create_user(self, email: str, hashed_password: str) -> UserInDB:
        """
        Create a new user in the database
        
        Args:
            email: User's email address
            hashed_password: Bcrypt hashed password
            
        Returns:
            UserInDB: Created user with id and timestamps
        """
        user_data = {
            "email": email,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await self.collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        
        return UserInDB(
            id=str(user_data["_id"]),
            email=user_data["email"],
            hashed_password=user_data["hashed_password"],
            created_at=user_data["created_at"],
            updated_at=user_data["updated_at"]
        )
    
    async def find_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Find user by email address
        
        Args:
            email: User's email address
            
        Returns:
            UserInDB if found, None otherwise
        """
        user = await self.collection.find_one({"email": email})
        if not user:
            return None
        
        return UserInDB(
            id=str(user["_id"]),
            email=user["email"],
            hashed_password=user["hashed_password"],
            created_at=user["created_at"],
            updated_at=user["updated_at"]
        )
    
    async def find_by_id(self, user_id: ObjectId) -> Optional[UserInDB]:
        """
        Find user by ID
        
        Args:
            user_id: MongoDB ObjectId
            
        Returns:
            UserInDB if found, None otherwise
        """
        user = await self.collection.find_one({"_id": user_id})
        if not user:
            return None
        
        return UserInDB(
            id=str(user["_id"]),
            email=user["email"],
            hashed_password=user["hashed_password"],
            created_at=user["created_at"],
            updated_at=user["updated_at"]
        )
    
    async def update_password(self, user_id: str, new_hashed_password: str) -> None:
        """
        Update user's password
        
        Args:
            user_id: User's ID (string format)
            new_hashed_password: New bcrypt hashed password
        """
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "hashed_password": new_hashed_password,
                    "updated_at": datetime.utcnow()
                }
            }
        )
    
    async def ensure_indexes(self):
        """Create required indexes for users collection"""
        # Unique index on email to prevent duplicate registrations
        await self.collection.create_index("email", unique=True)
