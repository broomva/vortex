from typing import Dict, Optional

import chainlit as cl


@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: Dict[str, str],
    default_app_user: cl.AppUser,
) -> Optional[cl.AppUser]:
    # set AppUser tags as regular_user
    match default_app_user.username:
        case "Broomva":
            default_app_user.tags = ["admin_user"]
            default_app_user.role = "ADMIN"
        case _:
            default_app_user.tags = ["regular_user"]
            default_app_user.role = "USER"
    # print(default_app_user)
    return default_app_user


@cl.password_auth_callback
def auth_callback(
    username: str = "guest", password: str = "guest"
) -> Optional[cl.AppUser]:
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    import hashlib

    # Create a new sha256 hash object
    hash_object = hashlib.sha256()

    # Hash the password
    hash_object.update(password.encode())

    # Get the hexadecimal representation of the hash
    hashed_password = hash_object.hexdigest()

    if (username, hashed_password) == (
        "broomva",
        "b68cacbadaee450b8a8ce2dd44842f1de03ee9993ad97b5e99dea64ef93960ba",
    ):
        return cl.AppUser(
            username="Broomva",
            role="OWNER",
            provider="credentials",
            tags=["admin_user"],
        )
    elif (username, password) == ("guest", "guest"):
        return cl.AppUser(username="Guest", role="USER", provider="credentials")
    else:
        return None


@cl.set_chat_profiles
async def chat_profile(current_user: cl.AppUser):
    if "ADMIN" not in current_user.role:
        # Default to 3.5 when not admin
        return [
            cl.ChatProfile(
                name="Vortex Agent",
                markdown_description="The underlying LLM model is **GPT-3.5**.",
            ),
        ]

    return [
        cl.ChatProfile(
            name="Turbo Agent",
            markdown_description="The underlying LLM model is **GPT-3.5**.",
        ),
        cl.ChatProfile(
            name="GPT4 Agent",
            markdown_description="The underlying LLM model is **GPT-4 Turbo**.",
        ),
    ]
