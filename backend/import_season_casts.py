from app.services.theatre_season_sync import (
    sync_all_season_cast_members,
)


def main() -> None:
    missing_by_season = sync_all_season_cast_members()

    print("All Theatre season casts synchronized.")

    if missing_by_season:
        print("\nMissing avatar IDs:")

        for season_number, avatar_ids in missing_by_season.items():
            print(
                f"Season {season_number}: "
                f"{avatar_ids}"
            )
    else:
        print("No missing characters.")


if __name__ == "__main__":
    main()