"""
Finds and verifies the fixed room/opponent rotation recommended in §1
of the analysis.

Constraints (all satisfied simultaneously, verified below rather than
eyeballed — an earlier draft of this rotation satisfied only the first
two and was caught by review):
  1. 8 guilds, 4 rooms, 4 rounds, capacity 2 guilds/room/round.
  2. Every guild visits every room exactly once across the 4 rounds.
  3. Every guild faces a different opponent every round (no repeats).
  4. No guild ever faces its own same-Tier-1-specialty "twin"
     (Lisbon/Bursa, Stockholm/Ghent, Gdansk/Venice, Prague/Vienna).

Run: python3 rotation_schedule.py
"""
import itertools

SPECIALTY = {
    "Lisbon": "wax", "Bursa": "wax",
    "Stockholm": "flax", "Ghent": "flax",
    "Gdansk": "saltpetre", "Venice": "saltpetre",
    "Prague": "charcoal", "Vienna": "charcoal",
}
TWIN = {
    "Lisbon": "Bursa", "Bursa": "Lisbon",
    "Stockholm": "Ghent", "Ghent": "Stockholm",
    "Gdansk": "Venice", "Venice": "Gdansk",
    "Prague": "Vienna", "Vienna": "Prague",
}
GUILDS = list(SPECIALTY.keys())
N_ROUNDS = 4
N_ROOMS = 4


def gen_pairings(guilds):
    if not guilds:
        yield []
        return
    a = guilds[0]
    for i in range(1, len(guilds)):
        b = guilds[i]
        rest = guilds[1:i] + guilds[i + 1:]
        for sub in gen_pairings(rest):
            yield [(a, b)] + sub


def search(rnd, room_visited, opponents, schedule):
    """Depth-first search that prunes any twin-pairing immediately (not just
    at the leaf) - a solution with zero twin-pairings is known to exist, so
    this finds one quickly instead of exploring the whole tree."""
    if rnd == N_ROUNDS:
        return True

    for pairing in gen_pairings(list(GUILDS)):
        if any(b in opponents[a] or TWIN[a] == b for a, b in pairing):
            continue
        for room_perm in itertools.permutations(range(N_ROOMS)):
            if any(room in room_visited[a] or room in room_visited[b]
                   for (a, b), room in zip(pairing, room_perm)):
                continue
            new_rv = {g: set(s) for g, s in room_visited.items()}
            new_op = {g: set(s) for g, s in opponents.items()}
            assignment = {}
            for (a, b), room in zip(pairing, room_perm):
                new_rv[a].add(room)
                new_rv[b].add(room)
                new_op[a].add(b)
                new_op[b].add(a)
                assignment[room] = (a, b)
            schedule.append(assignment)
            if search(rnd + 1, new_rv, new_op, schedule):
                return True
            schedule.pop()
    return False


def find_rotation():
    room_visited = {g: set() for g in GUILDS}
    opponents = {g: set() for g in GUILDS}
    schedule = []
    ok = search(0, room_visited, opponents, schedule)
    assert ok, "no zero-twin-pairing solution found"
    twin_pairs = 0  # by construction, since twin pairings were pruned
    return twin_pairs, schedule


def verify(schedule):
    room_visited = {g: [] for g in GUILDS}
    opponents = {g: [] for g in GUILDS}
    for rnd in schedule:
        seen = set()
        for room, (a, b) in rnd.items():
            assert a not in seen and b not in seen, "guild double-booked"
            seen.update([a, b])
            room_visited[a].append(room)
            room_visited[b].append(room)
            opponents[a].append(b)
            opponents[b].append(a)
        assert seen == set(GUILDS), "not all guilds scheduled"
    for g in GUILDS:
        assert sorted(room_visited[g]) == list(range(N_ROOMS)), f"{g} room coverage wrong"
        assert len(set(opponents[g])) == 4, f"{g} has a repeated opponent"
        assert TWIN[g] not in opponents[g], f"{g} faces its own twin"
    return room_visited, opponents


if __name__ == "__main__":
    twin_pairs, schedule = find_rotation()
    print(f"Best schedule found: {twin_pairs} twin-pairings, "
          f"{'ALL constraints satisfied' if twin_pairs == 0 else 'twin-pairing not fully avoidable'}\n")
    room_visited, opponents = verify(schedule)
    room_names = ["Room 1 (Cloth)", "Room 2 (Dye)", "Room 3 (Black Powder)", "Room 4 (Candle)"]
    for i, rnd in enumerate(schedule):
        print(f"Round {i + 1}:")
        for room in range(N_ROOMS):
            a, b = rnd[room]
            print(f"  {room_names[room]}: {a}, {b}")
    print("\nPer-guild check:")
    for g in GUILDS:
        print(f"  {g:10s} ({SPECIALTY[g]:9s}) opponents={opponents[g]}")
