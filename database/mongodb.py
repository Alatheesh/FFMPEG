from __future__ import annotations

from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB:

    def __init__(self,uri:str,database:str):

        self.client=AsyncIOMotorClient(uri)
        self.db=self.client[database]

        self.users=self.db.users
        self.workspaces=self.db.workspaces
        self.jobs=self.db.jobs
        self.history=self.db.history
        self.settings=self.db.settings

    # ==================================================
    # Initialization
    # ==================================================

    async def initialize(self):

        await self.users.create_index(
            "user_id",
            unique=True
        )

        await self.workspaces.create_index(
            "user_id",
            unique=True
        )

        await self.jobs.create_index(
            "job_id",
            unique=True
        )

        await self.history.create_index(
            "user_id"
        )

        await self.settings.create_index(
            "user_id",
            unique=True
        )

    # ==================================================
    # Users
    # ==================================================

    async def get_user(
        self,
        user_id:int
    ):

        return await self.users.find_one(
            {
                "user_id":user_id
            }
        )

    async def create_user(
        self,
        user_id:int,
        first_name:str="",
        username:str=""
    ):

        data={
            "user_id":user_id,
            "first_name":first_name,
            "username":username,
            "created_at":datetime.utcnow(),
            "last_seen":datetime.utcnow()
        }

        await self.users.update_one(
            {
                "user_id":user_id
            },
            {
                "$set":data
            },
            upsert=True
        )

        return data

    async def update_last_seen(
        self,
        user_id:int
    ):

        await self.users.update_one(
            {
                "user_id":user_id
            },
            {
                "$set":{
                    "last_seen":datetime.utcnow()
                }
            }
        )

    async def delete_user(
        self,
        user_id:int
    ):

        await self.users.delete_one(
            {
                "user_id":user_id
            }
        )

    async def total_users(self):

        return await self.users.count_documents(
            {}
        )

    # ==================================================
    # Settings
    # ==================================================

    async def get_settings(
        self,
        user_id:int
    ):

        data=await self.settings.find_one(
            {
                "user_id":user_id
            }
        )

        if data:
            return data

        defaults={
            "user_id":user_id,
            "output":"mkv",
            "video_codec":"copy",
            "audio_codec":"copy",
            "language":"en",
            "progress":True
        }

        await self.settings.insert_one(
            defaults
        )

        return defaults

    async def update_settings(
        self,
        user_id:int,
        values:dict
    ):

        await self.settings.update_one(
            {
                "user_id":user_id
            },
            {
                "$set":values
            },
            upsert=True
        )
    # ==================================================
    # Workspace
    # ==================================================

    async def get_workspace(
        self,
        user_id:int
    ):

        return await self.workspaces.find_one(
            {
                "user_id":user_id
            }
        )

    async def save_workspace(
        self,
        user_id:int,
        workspace:dict
    ):

        workspace["updated_at"]=datetime.utcnow()

        await self.workspaces.update_one(
            {
                "user_id":user_id
            },
            {
                "$set":workspace
            },
            upsert=True
        )

    async def delete_workspace(
        self,
        user_id:int
    ):

        await self.workspaces.delete_one(
            {
                "user_id":user_id
            }
        )

    async def workspace_exists(
        self,
        user_id:int
    ):

        return (
            await self.workspaces.count_documents(
                {
                    "user_id":user_id
                },
                limit=1
            )
        )>0

    # ==================================================
    # Jobs
    # ==================================================

    async def create_job(
        self,
        job:dict
    ):

        job.setdefault(
            "created_at",
            datetime.utcnow()
        )

        job.setdefault(
            "updated_at",
            datetime.utcnow()
        )

        job.setdefault(
            "status",
            "pending"
        )

        await self.jobs.insert_one(job)

    async def get_job(
        self,
        job_id:str
    ):

        return await self.jobs.find_one(
            {
                "job_id":job_id
            }
        )

    async def update_job(
        self,
        job_id:str,
        values:dict
    ):

        values["updated_at"]=datetime.utcnow()

        await self.jobs.update_one(
            {
                "job_id":job_id
            },
            {
                "$set":values
            }
        )

    async def delete_job(
        self,
        job_id:str
    ):

        await self.jobs.delete_one(
            {
                "job_id":job_id
            }
        )

    async def jobs_by_user(
        self,
        user_id:int,
        limit:int=20
    ):

        cursor=self.jobs.find(
            {
                "user_id":user_id
            }
        ).sort(
            "created_at",
            -1
        ).limit(limit)

        return await cursor.to_list(length=limit)

    async def pending_jobs(self):

        cursor=self.jobs.find(
            {
                "status":{
                    "$in":[
                        "pending",
                        "processing"
                    ]
                }
            }
        )

        return await cursor.to_list(length=None)

    # ==================================================
    # History
    # ==================================================

    async def add_history(
        self,
        user_id:int,
        action:str,
        data:dict=None
    ):

        await self.history.insert_one(
            {
                "user_id":user_id,
                "action":action,
                "data":data or {},
                "created_at":datetime.utcnow()
            }
        )

    async def get_history(
        self,
        user_id:int,
        limit:int=50
    ):

        cursor=self.history.find(
            {
                "user_id":user_id
            }
        ).sort(
            "created_at",
            -1
        ).limit(limit)

        return await cursor.to_list(length=limit)

    async def clear_history(
        self,
        user_id:int
    ):

        await self.history.delete_many(
            {
                "user_id":user_id
            }
        )

    # ==================================================
    # Recovery
    # ==================================================

    async def recover_jobs(self):

        return await self.pending_jobs()
    # ==================================================
    # Progress
    # ==================================================

    async def update_progress(
        self,
        job_id:str,
        progress:int,
        message:str=""
    ):

        progress=max(0,min(100,int(progress)))

        await self.jobs.update_one(
            {
                "job_id":job_id
            },
            {
                "$set":{
                    "progress":progress,
                    "message":message,
                    "updated_at":datetime.utcnow()
                }
            }
        )

    async def finish_job(
        self,
        job_id:str,
        output_file:str=""
    ):

        await self.jobs.update_one(
            {
                "job_id":job_id
            },
            {
                "$set":{
                    "status":"completed",
                    "progress":100,
                    "output_file":output_file,
                    "updated_at":datetime.utcnow()
                }
            }
        )

    async def fail_job(
        self,
        job_id:str,
        error:str
    ):

        await self.jobs.update_one(
            {
                "job_id":job_id
            },
            {
                "$set":{
                    "status":"failed",
                    "error":error,
                    "updated_at":datetime.utcnow()
                }
            }
        )

    async def cancel_job(
        self,
        job_id:str
    ):

        await self.jobs.update_one(
            {
                "job_id":job_id
            },
            {
                "$set":{
                    "status":"cancelled",
                    "updated_at":datetime.utcnow()
                }
            }
        )

    # ==================================================
    # Cleanup
    # ==================================================

    async def cleanup_old_jobs(
        self,
        before:datetime
    ):

        result=await self.jobs.delete_many(
            {
                "updated_at":{
                    "$lt":before
                }
            }
        )

        return result.deleted_count

    async def cleanup_old_history(
        self,
        before:datetime
    ):

        result=await self.history.delete_many(
            {
                "created_at":{
                    "$lt":before
                }
            }
        )

        return result.deleted_count

    async def cleanup_old_workspaces(
        self,
        before:datetime
    ):

        result=await self.workspaces.delete_many(
            {
                "updated_at":{
                    "$lt":before
                }
            }
        )

        return result.deleted_count

    # ==================================================
    # Statistics
    # ==================================================

    async def statistics(self):

        return {
            "users":await self.total_users(),
            "workspaces":await self.workspaces.count_documents({}),
            "jobs":await self.jobs.count_documents({}),
            "history":await self.history.count_documents({})
        }

    async def health(self):

        try:
            await self.db.command("ping")
            return True
        except Exception:
            return False

    # ==================================================
    # Connection
    # ==================================================

    async def close(self):

        self.client.close()

    # ==================================================
    # Magic
    # ==================================================

    async def __aenter__(self):

        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        tb
    ):

        await self.close()

    def __repr__(self):

        return (
            f"<MongoDB "
            f"database={self.db.name}>"
        )
