import json
from urllib.parse import quote
from urllib.request import urlopen

from sqlalchemy import select

from app.database import SessionLocal
from app.models.character import Character


GENSHIN_DB_API_URL = (
    "https://genshin-db-api.vercel.app/api/v5/characters"
)


def build_character_api_url(character_name: str) -> str:
    encoded_name = quote(character_name)
    return f"{GENSHIN_DB_API_URL}?query={encoded_name}"


def fetch_character_names() -> list[str]:
    url = f"{GENSHIN_DB_API_URL}?query=names&matchCategories=true"

    with urlopen(url) as response:
        return json.load(response)


def fetch_character_from_api(character_name: str) -> dict:
    url = build_character_api_url(character_name)

    with urlopen(url) as response:
        return json.load(response)


def build_side_icon_url(side_icon_name: str) -> str:
    return f"https://enka.network/ui/{side_icon_name}.png"

def sync_character(character_data: dict) -> None:

    avatar_id = character_data["id"]

    side_icon_name = character_data["images"].get("filename_sideIcon")

    if side_icon_name is None:
        raise ValueError(
            f"No side icon filename found for "
            f"{character_data['name']} ({avatar_id})."
        )

    side_icon_url = build_side_icon_url(side_icon_name)

    with SessionLocal() as session:

        existing_character = session.scalar(
            select(Character).where(
                Character.avatar_id == avatar_id
            )
        )

        if existing_character is None:
            character = Character(
                avatar_id=avatar_id,
                name=character_data["name"],
                element=character_data["elementText"],
                weapon_type=character_data["weaponText"],
                rarity=character_data["rarity"],
                side_icon_url=side_icon_url,
            )

            session.add(character)
            print(
                f"Added {character.name} "
                f"({avatar_id}) to the database."
            )

        else:
            existing_character.name = character_data["name"]
            existing_character.element = character_data["elementText"]
            existing_character.weapon_type = character_data["weaponText"]
            existing_character.rarity = character_data["rarity"]
            existing_character.side_icon_url = side_icon_url

            print(
                f"Updated {existing_character.name} "
                f"({avatar_id}) in the database."
            )

        session.commit()


def sync_all_characters() -> None:
    character_names = fetch_character_names()

    print(f"Synchronizing {len(character_names)} characters...")

    for character_name in character_names:
        character_data = fetch_character_from_api(character_name)
        sync_character(character_data)

    print("Character synchronization completed.")


def main() -> None:
    sync_all_characters()

#needed so that main doesn't get called automatically everytime when character_sync.py's functions are imported elsewhere rather than character_sync module being directly executed through terminal
if __name__ == "__main__":
    main()