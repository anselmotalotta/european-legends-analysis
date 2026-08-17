"""
Toy scheduling model — NOT the full economic simulation.

Question: with no coordination mechanism, how often does unmanaged
self-scheduling let all 8 guilds visit all 4 activity rooms exactly
once each across 4 rounds (2 guild slots per room per round, no
capacity margin)?

Model: each round, guilds are processed in a random order; each guild
picks uniformly at random among rooms it hasn't visited yet that still
have a free slot this round. Note this gives each guild full, accurate
knowledge of remaining capacity at the moment it chooses (it is NOT a
"no visibility" model) — what's absent is negotiation between guilds
and any ability to anticipate choices later in the round. If no room
is available, the guild gets no room this round (in the real event
this is where a loan / missed quest would happen).

This is a policy-specific baseline for one simple, fully-specified
decentralized-choice rule, used only to check whether the scheduling
concern in the written analysis is measurable. It is NOT a lower or
upper bound on the real event: real players might do better via
negotiation and visible queues, or worse via concurrent decisions and
confusion under time pressure. It also only models the pure room/seat
allocation mechanic in isolation — the real game entangles room choice
with which Tier-2 item a guild holds, coin availability, loans, and
the previous room's reward card, none of which is represented here.

Run: python3 toy_scheduling_model.py
"""
import random

random.seed(42)

N_GUILDS = 8
N_ROOMS = 4
N_ROUNDS = 4
CAPACITY = 2
TRIALS = 200_000

def run_trial():
    visited = {g: set() for g in range(N_GUILDS)}
    for rnd in range(N_ROUNDS):
        order = list(range(N_GUILDS))
        random.shuffle(order)
        remaining_capacity = {r: CAPACITY for r in range(N_ROOMS)}
        for g in order:
            eligible = [r for r in range(N_ROOMS)
                        if r not in visited[g] and remaining_capacity[r] > 0]
            if not eligible:
                continue  # guild fails to get a room this round (would need a loan / miss out)
            choice = random.choice(eligible)
            visited[g].add(choice)
            remaining_capacity[choice] -= 1
    return visited

all_guilds_complete = 0
guild_complete_count = 0
total_guilds = 0
rooms_missed_hist = {0:0,1:0,2:0,3:0,4:0}

for _ in range(TRIALS):
    visited = run_trial()
    complete = all(len(v) == N_ROOMS for v in visited.values())
    if complete:
        all_guilds_complete += 1
    for v in visited.values():
        total_guilds += 1
        if len(v) == N_ROOMS:
            guild_complete_count += 1
        rooms_missed_hist[N_ROOMS - len(v)] += 1

print(f"Trials: {TRIALS}")
print(f"Games where ALL 8 guilds visited all 4 rooms: {all_guilds_complete/TRIALS*100:.1f}%")
print(f"Individual guilds that completed all 4 rooms: {guild_complete_count/total_guilds*100:.1f}%")
print("Distribution of rooms missed per guild:")
for k,v in rooms_missed_hist.items():
    print(f"  missed {k} room(s): {v/total_guilds*100:.1f}%")
