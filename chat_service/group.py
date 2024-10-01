from fastapi import HTTPException
from database import db

# 创建
def create_group(group, manager):
    try:
        with db.cursor() as cursor:
            cursor.execute("select id from users where username = %s", (group.created_by,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail=f"User '{group.created_by}' not found.")
            created_by_id = result[0]

            sql = "insert into chat_groups (group_name, created_by) values (%s, %s)"
            cursor.execute(sql, (group.group_name, created_by_id))
            db.commit()

        return {"status": "success", "message": f"Group '{group.group_name}' created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 加入
def join_group(request, manager):
    try:
        with db.cursor() as cursor:
            cursor.execute("select id from users where username = %s", (request.username,))
            user_result = cursor.fetchone()
            if not user_result:
                raise HTTPException(status_code=404, detail=f"User '{request.username}' not found.")
            user_id = user_result[0]

            cursor.execute("select id from chat_groups where group_name = %s", (request.group_name,))
            group_result = cursor.fetchone()
            if not group_result:
                raise HTTPException(status_code=404, detail=f"Group '{request.group_name}' not found.")
            group_id = group_result[0]

            sql = "insert into group_members (group_id, user_id) values (%s, %s)"
            cursor.execute(sql, (group_id, user_id))
            db.commit()

            manager.add_user_to_group(request.username, request.group_name)

        return {"status": "success", "message": f"User '{request.username}' joined group '{request.group_name}' successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

