from gtfspy import import_gtfs


def load_or_import_example_gtfs(verbose=False):
    imported_database_path = "transport.db"
    import_gtfs.import_gtfs(
        ["../data/PID_GTFS.zip"],
        imported_database_path,
        print_progress=verbose,
        location_name="Prague",
    )


if __name__ == "__main__":
    load_or_import_example_gtfs(verbose=True)
