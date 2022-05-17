# SBB Schedule Information

Swiss public transport stops as adjacency graph.

Get the graph:

```py
import fahrplan
sbb = fahrplan.latest
```

Display some data:
```bash
>>> len(sbb)
34010

>>> sbb['Romanshorn']
{'Amriswil': 5, 'Egnach': 1, 'Konstanz': 17, 'Kreuzlingen Hafen': 14, 'Neukirch-Egnach': 2, 'Romanshorn': 3, 'Romanshorn (See)': 5, 'Romanshorn Autoquai': 6, 'Romanshorn, Bahnhof': 3, 'St. Gallen': 18, 'Uttwil': 3, 'Weinfelden': 13, 'Wittenbach': 11}
```

The graph contains direct non-stop connections including transfers, with connection time in minutes.

The graph only records whether two stations are directly connected with each other by at least one connection. It omits any information on
  * lines
  * time of day
  * service schedules

So, some edges may be the consequence of special effects such as end-of-day connections, weekend night service, and the like.

Also, since each edge distance is recorded in minutes from departure to arrival, concatenating multiple legs will underestimate actual travelling time, as the stop time
is ignored.

### Source

The data ist parsed from [GTFS](https://opentransportdata.swiss/de/cookbook/gtfs) data available from https://opentransportdata.swiss/de/group/timetables-gtfs

```py
sbb = read_gtfs("fahrplan/gtfs_fp2022_2022-05-11_04-15")
write_schedule("fahrplan/sbb_2022.json", sbb)
```
