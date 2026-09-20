from sqlalchemy import select

from app.database import SessionLocal
from app.models.character import Character
from app.models.theatre_season import TheatreSeason
from app.models.season_cast import SeasonCast
from app.models.season_cast_member import SeasonCastMember

import json
from datetime import datetime
from urllib.request import Request, urlopen


LUNARIS_API_BASE_URL = "https://api.lunaris.moe/data"
LUNARIS_VERSION_URL = (f"{LUNARIS_API_BASE_URL}/version.json")


def build_lunaris_url(
    path: str,
    version: str,
) -> str:
    return (
        f"{LUNARIS_API_BASE_URL}/"
        f"{version}/{path}"
    )

# Lunaris contains two historical records before Imaginarium Theatre
# and one anomalous future record that we do not want.
EXCLUDED_LUNARIS_SEASONS = {"1", "2", "101"}

# Lunaris starts its actual Imaginarium Theatre numbering at 3.
# Therefore:
# Lunaris 3 -> Theatre Season 1
# Lunaris 4 -> Theatre Season 2
# ...
THEATRE_SEASON_NUMBER_OFFSET = 2


LUNARIS_ELEMENT_MAP = {
    2: "Pyro",
    3: "Hydro",
    4: "Dendro",
    5: "Electro",
    6: "Cryo",
    7: "Anemo",
    8: "Geo",
}


def fetch_json(url: str) -> dict:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
    )

    with urlopen(request) as response:
        return json.load(response)

def fetch_lunaris_data_version() -> str:
    version_data = fetch_json(LUNARIS_VERSION_URL)

    version = version_data.get("version")

    if not isinstance(version, str):
        raise ValueError(
            "Lunaris version response does not contain "
            "a valid version."
        )

    return version


def fetch_roleplay_playlist(version: str) -> dict:
    url = build_lunaris_url(
        "roleplaylist.json",
        version,
    )
    return fetch_json(url)


def fetch_roleplay_season(
    season_id: str,
    version: str,
) -> dict:
    url = build_lunaris_url(
        f"en/roleplay/{season_id}.json",
        version,
    )
    return fetch_json(url)


def parse_source_datetime(value: str):
    return datetime.strptime(
        value,
        "%Y-%m-%d %H:%M:%S",
    ).date()


def translate_elements(element_restrictions: list[int]) -> list[str]:
    element_ids = [
        element_id
        for element_id in element_restrictions
        if element_id != 0
    ]

    if len(element_ids) != 3:
        raise ValueError(
            f"Expected exactly 3 Theatre elements, "
            f"got {element_ids}"
        )

    unknown_element_ids = [
        element_id
        for element_id in element_ids
        if element_id not in LUNARIS_ELEMENT_MAP
    ]

    if unknown_element_ids:
        raise ValueError(
            f"Unknown Lunaris element IDs: "
            f"{unknown_element_ids}"
        )

    return [
        LUNARIS_ELEMENT_MAP[element_id]
        for element_id in element_ids
    ]


def translate_season(
    lunaris_season_id: str,
    playlist_data: dict,
    roleplay_data: dict,
) -> dict:
    season_data = playlist_data[lunaris_season_id]

    theatre_season_number = (
        int(lunaris_season_id)
        - THEATRE_SEASON_NUMBER_OFFSET
    )

    allowed_elements = translate_elements(
        season_data["elementRestrictions"]
    )

    avatar_config = roleplay_data["avatarConfig"]

    primary_avatar_ids = [
        avatar["avatarId"]
        for avatar in avatar_config["bonusAvatars"]
    ]
    special_guest_avatar_ids = avatar_config["featuredAvatars"]

    if len(primary_avatar_ids) != 6:
        raise ValueError(
            f"Theatre Season {theatre_season_number} "
            f"should have 6 primary cast members, "
            f"got {len(primary_avatar_ids)}"
        )

    if len(special_guest_avatar_ids) != 4:
        raise ValueError(
            f"Theatre Season {theatre_season_number} "
            f"should have 4 special guests, "
            f"got {len(special_guest_avatar_ids)}"
        )

    return {
        "season_number": theatre_season_number,
        "start_date": parse_source_datetime(
            season_data["beginTime"]
        ),
        "end_date": parse_source_datetime(
            season_data["endTime"]
        ),
        "allowed_elements": allowed_elements,
        "primary_avatar_ids": primary_avatar_ids,
        "special_guest_avatar_ids": special_guest_avatar_ids,
    }

def resolve_characters(
    avatar_ids: list[int],
) -> tuple[list[Character], list[int]]:
    with SessionLocal() as session:
        characters = session.scalars(
            select(Character).where(
                Character.avatar_id.in_(avatar_ids)
            )
        ).all()

        characters_by_avatar_id = {
            character.avatar_id: character
            for character in characters
        }

        resolved_characters = []
        missing_avatar_ids = []

        for avatar_id in avatar_ids:
            character = characters_by_avatar_id.get(avatar_id)

            if character is None:
                missing_avatar_ids.append(avatar_id)
            else:
                resolved_characters.append(character)

        return resolved_characters, missing_avatar_ids

def upsert_theatre_season(season_data: dict) -> None:
    with SessionLocal() as session:
        existing_season = session.scalar(
            select(TheatreSeason).where(
                TheatreSeason.season_number
                == season_data["season_number"]
            )
        )

        if existing_season is None:
            theatre_season = TheatreSeason(
                season_number=season_data["season_number"],
                start_date=season_data["start_date"],
                end_date=season_data["end_date"],
                allowed_elements=season_data["allowed_elements"],
            )

            session.add(theatre_season)

        else:
            existing_season.start_date = season_data["start_date"]
            existing_season.end_date = season_data["end_date"]
            existing_season.allowed_elements = (
                season_data["allowed_elements"]
            )

        session.commit()

def get_or_create_season_cast(
    season_id: int,
) -> SeasonCast:
    with SessionLocal() as session:
        existing_cast = session.scalar(
            select(SeasonCast).where(
                SeasonCast.season_id == season_id
            )
        )

        if existing_cast is not None:
            return existing_cast

        season_cast = SeasonCast(
            season_id=season_id,
        )

        session.add(season_cast)
        session.commit()
        session.refresh(season_cast)

        return season_cast

def get_theatre_season(
    season_number: int,
) -> TheatreSeason | None:
    with SessionLocal() as session:
        return session.scalar(
            select(TheatreSeason).where(
                TheatreSeason.season_number == season_number
            )
        )

def ensure_season_casts() -> None:
    with SessionLocal() as session:
        seasons = session.scalars(
            select(TheatreSeason).order_by(
                TheatreSeason.season_number
            )
        ).all()

        for season in seasons:
            existing_cast = session.scalar(
                select(SeasonCast).where(
                    SeasonCast.season_id == season.id
                )
            )

            if existing_cast is None:
                session.add(
                    SeasonCast(
                        season_id=season.id,
                    )
                )

        session.commit()

def resolve_season_cast_members(
    season_data: dict,
) -> tuple[list[tuple[Character, str]], list[int]]:
    primary_avatar_ids = season_data["primary_avatar_ids"]
    special_guest_avatar_ids = season_data[
        "special_guest_avatar_ids"
    ]

    all_avatar_ids = (
        primary_avatar_ids + special_guest_avatar_ids
    )

    characters, missing_avatar_ids = resolve_characters(
        all_avatar_ids
    )

    characters_by_avatar_id = {
        character.avatar_id: character
        for character in characters
    }

    resolved_members = []

    for avatar_id in primary_avatar_ids:
        character = characters_by_avatar_id.get(avatar_id)

        if character is not None:
            resolved_members.append(
                (character, "PRIMARY")
            )

    for avatar_id in special_guest_avatar_ids:
        character = characters_by_avatar_id.get(avatar_id)

        if character is not None:
            resolved_members.append(
                (character, "SPECIAL_GUEST")
            )

    return resolved_members, missing_avatar_ids

def sync_season_cast_members(
    season_data: dict,
) -> list[int]:
    season = get_theatre_season(
        season_data["season_number"]
    )

    if season is None:
        raise ValueError(
            f"Theatre Season "
            f"{season_data['season_number']} was not found."
        )

    season_cast = get_or_create_season_cast(season.id)

    resolved_members, missing_avatar_ids = (
        resolve_season_cast_members(season_data)
    )

    with SessionLocal() as session:
        existing_members = session.scalars(
            select(SeasonCastMember).where(
                SeasonCastMember.season_cast_id
                == season_cast.id
            )
        ).all()

        existing_character_ids = {
            member.character_id
            for member in existing_members
        }

        for character, cast_type in resolved_members:
            if character.id in existing_character_ids:
                continue

            session.add(
                SeasonCastMember(
                    season_cast_id=season_cast.id,
                    character_id=character.id,
                    cast_type=cast_type,
                )
            )

        session.commit()

    return missing_avatar_ids

def sync_all_season_cast_members() -> dict[int, list[int]]:
    seasons = fetch_all_theatre_seasons()

    missing_by_season = {}

    for season_data in seasons:
        missing_avatar_ids = sync_season_cast_members(
            season_data
        )

        if missing_avatar_ids:
            missing_by_season[
                season_data["season_number"]
            ] = missing_avatar_ids

    return missing_by_season

def fetch_all_theatre_seasons() -> list[dict]:
    version = fetch_lunaris_data_version()

    playlist_data = fetch_roleplay_playlist(version)

    translated_seasons = []

    for lunaris_season_id in sorted(
        playlist_data,
        key=int,
    ):
        if lunaris_season_id in EXCLUDED_LUNARIS_SEASONS:
            continue

        roleplay_data = fetch_roleplay_season(
            lunaris_season_id,
            version,
        )

        translated_season = translate_season(
            lunaris_season_id,
            playlist_data,
            roleplay_data,
        )

        translated_seasons.append(
            translated_season
        )

    return translated_seasons


def print_season(season: dict) -> None:
    print()
    print(
        f"Theatre Season {season['season_number']}"
    )
    print(
        f"Dates: "
        f"{season['start_date']} → "
        f"{season['end_date']}"
    )

    print(
        "Elements: "
        + ", ".join(season["allowed_elements"])
    )

    print("Primary Cast:")

    for avatar_id in season["primary_avatar_ids"]:
        print(f"  - {avatar_id}")

    print("Special Guests:")

    for avatar_id in season["special_guest_avatar_ids"]:
        print(f"  - {avatar_id}")


def main() -> None:
    seasons = fetch_all_theatre_seasons()

    print(
        f"Fetched {len(seasons)} valid Theatre seasons."
    )

    for season in seasons:
        print_season(season)


if __name__ == "__main__":
    main()