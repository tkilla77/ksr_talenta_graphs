from . import gtfs_reader
import os

fahrplan_2022 = gtfs_reader.read_json_schedule(os.path.join(__path__[0], "./fahrplan_2022.json"))
fahrplan_2024 = gtfs_reader.read_json_schedule(os.path.join(__path__[0], "./fahrplan_2024.json"))
latest = fahrplan_2024