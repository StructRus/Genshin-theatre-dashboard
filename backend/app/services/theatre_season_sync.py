import json
from datetime import datetime
from urllib.request import Request, urlopen


LUNARIS_BASE_URL = "https://api.lunaris.moe/data/7.0.54.2"

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


def fetch_roleplay_playlist() -> dict:
    url = f"{LUNARIS_BASE_URL}/roleplaylist.json"
    return fetch_json(url)


def fetch_roleplay_season(season_id: str) -> dict:
    url = f"{LUNARIS_BASE_URL}/en/roleplay/{season_id}.json"
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


def fetch_all_theatre_seasons() -> list[dict]:
    playlist_data = fetch_roleplay_playlist()

    translated_seasons = []

    for lunaris_season_id in sorted(
        playlist_data,
        key=int,
    ):
        if lunaris_season_id in EXCLUDED_LUNARIS_SEASONS:
            continue

        roleplay_data = fetch_roleplay_season(
            lunaris_season_id
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