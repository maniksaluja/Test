from datetime import datetime
from . import db

db = db.count

# Increment the count and store the last 2 values
async def incr_count() -> int:
    x = await db.find_one({"count": 69})
    if x:
        y = x["actual_count"]  # Current count
        y += 1  # Increment the count
        # Update actual count and store the last 2 values in history
        await db.update_one(
            {"count": 69},
            {
                "$set": {"actual_count": y},
                "$push": {
                    "history": {
                        "$each": [{"old_value": x["actual_count"], "updated_at": datetime.now()}],
                        "$slice": -2  # Keep only the last 2 values
                    }
                },
            }
        )
    else:
        y = 1  # Initialize the count if not present
        # Create the document and initialize history with old_value = 0
        await db.update_one(
            {"count": 69},
            {
                "$set": {"actual_count": y},
                "$push": {
                    "history": {
                        "$each": [{"old_value": 0, "updated_at": datetime.now()}],
                        "$slice": -2
                    }
                },
            },
            upsert=True
        )
    return y

# Get the current count
async def get_count() -> int:
    x = await db.find_one({"count": 69})
    if x:
        return x["actual_count"]
    return 0

# Increment the count by a specific number and store the last 2 values
async def incr_count_by(c: int) -> int:
    x = await db.find_one({"count": 69})
    if x:
        y = x["actual_count"]
        y += c
        # Update actual count and store the last 2 values in history
        await db.update_one(
            {"count": 69},
            {
                "$set": {"actual_count": y},
                "$push": {
                    "history": {
                        "$each": [{"old_value": x["actual_count"], "updated_at": datetime.now()}],
                        "$slice": -2
                    }
                },
            }
        )
    else:
        y = c  # Initialize the count with the given increment value
        # Create the document and initialize history
        await db.update_one(
            {"count": 69},
            {
                "$set": {"actual_count": y},
                "$push": {
                    "history": {
                        "$each": [{"old_value": 0, "updated_at": datetime.now()}],
                        "$slice": -2
                    }
                },
            },
            upsert=True
        )
    return y

# Reset the count and delete the history
async def reset_count():
    await db.delete_one({"count": 69})
