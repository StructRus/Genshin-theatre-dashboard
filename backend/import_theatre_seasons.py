from app.services.theatre_season_sync import (
    fetch_all_theatre_seasons,
    upsert_theatre_season,
    ensure_season_casts,
)


def main() -> None:
    seasons = fetch_all_theatre_seasons()

    print(f"Found {len(seasons)} Theatre seasons.")

    for season in seasons:
        upsert_theatre_season(season)

        print(
            f"Imported Theatre Season "
            f"{season['season_number']}."
        )

    ensure_season_casts()

    print("Season casts are ready.")


if __name__ == "__main__":
    main()