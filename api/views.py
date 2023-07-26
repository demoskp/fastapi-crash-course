from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Query, Depends

from schemas.user import UserIn, UserOut, UpdateUser

api = APIRouter(prefix="/api")


users: List[UserOut] = [
    UserOut(id=1, first_name="John", last_name="Smith", email="jsmith@gmail.com"),
    UserOut(id=2, first_name="Jane", last_name="Doe", email="jdoe@gmail.com"),
    UserOut(id=3, first_name="Jack", last_name="Jones", email="jjones@gmail.com"),
    UserOut(id=4, first_name="Sarah", last_name="Smith", email="ssmith@gmail.com"),
]


def save_user(user: UserIn) -> UserOut:
    user_data = user.model_dump()
    user_data.pop("password")
    user_id = users[-1].id + 1
    user_out = UserOut(id=user_id, **user_data)
    users.append(user_out)
    return user_out


def update_user_or_404(user_id: int, update: UpdateUser) -> UserOut:
    updated_user = None
    for i, user in enumerate(users):
        if user.id == user_id:
            updated_user = users[i].model_copy(update=update.model_dump())
            users[i] = updated_user
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


def get_user_or_404(user_id: int) -> UserOut:
    user = next(filter(lambda u: u.id == user_id, users), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def delete_user_or_404(user_id: int) -> None:
    found = False
    for user in users:
        if user.id == user_id:
            found = True
            users.remove(user)

    if not found:
        raise HTTPException(status_code=404, detail="User not found")


def filter_users(
        first_name: Annotated[str, Query()] = None,
        last_name: Annotated[str, Query()] = None,
        email: Annotated[str, Query()] = None
):
    filtered = users
    if first_name:
        filtered = list(filter(lambda u: first_name in u.first_name, users))
    if last_name:
        filtered = list(filter(lambda u: last_name in u.last_name, users))
    if email:
        filtered = list(filter(lambda u: email in u.email, filtered))
    return filtered


@api.get("/users")
def get_users(filtered_users: Annotated[List[UserOut], Depends(filter_users)]) -> List[UserOut]:
    return filtered_users


@api.post("/users", status_code=201)
def create_user(user: Annotated[UserOut, Depends(save_user)]) -> UserOut:
    # user = save_user(user)
    return user


@api.put("/users/{user_id}", status_code=201)
def update_user(user: Annotated[UserOut, Depends(update_user_or_404)]) -> UserOut:
    return user


@api.delete("/users/{user_id}")
def create_user(user_id: int):
    delete_user_or_404(user_id)
    return {"msg": "user deleted"}


@api.get("/users/{user_id}")
# def get_user(user_id: int) -> dict[str, UserOut]:
#     user = next(filter(lambda u: u.id == user_id, users), None)
#     if user is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"user": user}
def get_user(user: Annotated[UserOut, Depends(get_user_or_404)]) -> dict[str, UserOut]:
    return {"user": user}
