from sim import items as I
from sim import rotation as R


def test_every_guild_visits_every_room_exactly_once():
    for guild in ("Lisbon", "Bursa", "Stockholm", "Ghent", "Gdansk", "Venice", "Prague", "Vienna"):
        rooms = [room for _, room in R.rooms_for_guild(guild)]
        assert sorted(rooms) == ["Room1", "Room2", "Room3", "Room4"]


def test_room_capacity_is_exactly_two_every_round():
    for rooms in R.FIXED_ROTATION:
        assert set(rooms.keys()) == {"Room1", "Room2", "Room3", "Room4"}
        for pair in rooms.values():
            assert len(pair) == 2
            assert pair[0] != pair[1]


def test_no_guild_faces_same_opponent_twice():
    opponents = {}
    for rooms in R.FIXED_ROTATION:
        for a, b in rooms.values():
            opponents.setdefault(a, []).append(b)
            opponents.setdefault(b, []).append(a)
    for guild, opps in opponents.items():
        assert len(opps) == len(set(opps)), f"{guild} has a repeated opponent: {opps}"


def test_no_guild_faces_its_own_specialty_twin():
    twin = {
        "Lisbon": "Bursa", "Bursa": "Lisbon", "Stockholm": "Ghent", "Ghent": "Stockholm",
        "Gdansk": "Venice", "Venice": "Gdansk", "Prague": "Vienna", "Vienna": "Prague",
    }
    for rooms in R.FIXED_ROTATION:
        for a, b in rooms.values():
            assert twin[a] != b, f"{a} faced its own twin {b}"


def test_coordinated_starting_hand_can_always_pay_round1_fee():
    """Analysis §2.1: the coordinated deal must guarantee every guild's
    starting hand can craft its Round-1 room's exact prerequisite."""
    for guild, missing in R.COORDINATED_MISSING_MATERIAL.items():
        room = R.ROUND1_ROOM_BY_GUILD[guild]
        needed = I.ROOM_PREREQUISITE[room]
        assert needed in I.tier1_options(missing), (
            f"{guild} missing={missing} can craft {I.tier1_options(missing)}, "
            f"but Round-1 room {room} needs {needed}"
        )


def test_opponent_in_room_is_symmetric():
    a, b = R.FIXED_ROTATION[0]["Room1"]
    assert R.opponent_in_room(0, "Room1", a) == b
    assert R.opponent_in_room(0, "Room1", b) == a
