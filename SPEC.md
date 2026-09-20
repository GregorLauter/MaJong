# Mah Jong Calculator - Project Specification

## 1. Project Goal

This project implements a score settlement calculator for four-player
traditional Chinese Classical Mah Jong.

The program does **not**: - play Mah Jong; - recognize or evaluate
tiles; - determine the hand value from a Mah Jong hand; - decide whether
a hand is legal.

The players calculate each player's hand value themselves. The program
receives those values and performs the settlement between the four
players.

Development is divided into three phases:

1.  Understand and specify the rules.
2.  Implement and thoroughly test the calculation engine.
3.  Build a locally installable desktop interface around the tested calculation engine.

Phase 2 is implemented and tested. As requested on 2026-09-20, the next
phase is a standalone desktop application for macOS, Windows, and Linux.
A website is not part of the current plan. This changes the delivery
format only; all Mah Jong rules below remain unchanged.

## 2. Players and Seating

There are exactly four players.

At the beginning of a game, the user enters the four player names in
seating/wind order:

1.  East
2.  South
3.  West
4.  North

This order is fixed for the game.

Rotation proceeds counterclockwise according to this stored order:

East -\> South -\> West -\> North -\> back to the first player

The application must remember which player is currently East.

## 3. Input for Each Round

For each round, the user provides:

-   the hand value for each of the four players;
-   which player won the round.

The current East player should **not** need to be entered again. The
program tracks East automatically.

## 4. Hand-Value Validation

All entered hand values must be non-negative integers.

All hand values must be **even numbers**.

Examples of valid values:

-   0
-   2
-   4
-   6
-   20
-   22
-   24
-   48

Examples of invalid values:

-   -2
-   1
-   3
-   21
-   25

If an odd value is entered, the round must not be calculated and the
user must receive a clear validation error.

The winner must have a hand value of **at least 22 points**.

Therefore, for example:

-   winner = 22: valid
-   winner = 24: valid
-   winner = 20: invalid
-   winner = 4: invalid

Non-winning players may have values below 22, including 0.

## 5. Settlement Rules

The settlement is zero-sum. Points are transferred between players;
points are never created or destroyed.

There are six unique player pairs in a four-player game. Each pair is
settled exactly once.

### 5.1 Winner vs. Loser

The winner receives their **absolute hand value** from every losing
player.

If player B wins with a hand value of 24:

-   A pays B 24
-   C pays B 24
-   D pays B 24

This calculation does not depend on the losing players' own hand values.

### 5.2 Loser vs. Loser

Two losing players settle only the **difference between their hand
values**.

The player with the higher hand value receives the difference from the
player with the lower hand value.

Example:

-   B = 6
-   C = 2

C pays B:

6 - 2 = 4 points

Another example:

-   B = 8
-   C = 8

No payment occurs between them.

## 6. East Multiplier

East has a factor of 2 for **every payment involving East**.

This applies regardless of whether East:

-   wins;
-   loses;
-   pays;
-   receives.

The normal pairwise payment is calculated first. If one of the two
players in that payment is the current East player, the payment is
multiplied by 2.

Examples:

Winner B has a hand value of 24 and A is East:

A -\> B = 48

because the normal winner payment is 24 and the payment involves East.

If A is East with value 12 and C is a losing player with value 8:

C -\> A = 8

because:

12 - 8 = 4

and:

4 \* 2 = 8

Payments between two non-East players are not doubled.

## 7. Verified Reference Example

The following example has been manually verified and must be included as
a regression test.

Initial state:

  Player   Wind      Hand value Result
  -------- ------- ------------ --------
  A        East              12 Loser
  B        South             24 Winner
  C        West               8 Loser
  D        North              4 Loser

Pairwise payments:

Winner payments:

-   A -\> B = 48, because A is East
-   C -\> B = 24
-   D -\> B = 24

Loser settlements:

-   C -\> A = 8
-   D -\> A = 16
-   D -\> C = 4

Net round changes:

  Player     Change
  -------- --------
  A             -24
  B             +96
  C             -28
  D             -44

Required control sum:

-24 + 96 - 28 - 44 = 0

After this round, B becomes East because B won and the previous East
player A did not win.

## 8. East Rotation

The application automatically tracks East after every round.

### If East does not win

East immediately rotates to the next player in the fixed seating order.

The East win-streak counter resets to zero.

### If East wins

East remains East for the next round.

The consecutive-East-win counter increases by one.

### Four consecutive wins as East

A player may remain East through repeated wins, but only through four
consecutive wins as East.

After the **fourth consecutive win as East**, East rotates to the next
player anyway.

The East win-streak counter then resets to zero.

This rule concerns **four consecutive wins**, not four total wins
accumulated at different times.

## 9. Game State

The calculation engine should maintain at least:

-   four player names;
-   fixed player/seating order;
-   current East player;
-   current consecutive East-win count;
-   cumulative score for each player;
-   round number;
-   round history.

A round-history entry should contain enough information to reconstruct
what happened, including at least:

-   round number;
-   East before the round;
-   winner;
-   four entered hand values;
-   calculated net changes;
-   cumulative totals after the round;
-   East for the following round.

## 10. Zero-Sum Invariant

This is a core correctness check.

For every round:

sum(round changes) == 0

For the cumulative game:

sum(total scores) == 0

The implementation should explicitly verify this.

If either invariant fails because of an internal calculation error, the
program should fail loudly rather than silently accepting the result.

## 11. Calculation Strategy

A simple and auditable implementation is preferred.

For each round:

1.  Validate all inputs.
2.  Generate the six unique player pairs.
3.  For each pair:
    -   if one player is the winner, the loser pays the winner the
        winner's full hand value;
    -   otherwise, settle the difference between the two losing hand
        values;
    -   if the payment involves East, multiply it by 2;
    -   subtract the amount from the payer;
    -   add the same amount to the receiver.
4.  Verify that round changes sum to zero.
5.  Add round changes to cumulative totals.
6.  Verify that cumulative totals sum to zero.
7.  Update the East win streak and East rotation.
8.  Save the round to history.

## 12. Initial Software Scope

The first implementation should be a clean Python project.

Priorities:

1.  correctness;
2.  readable calculation logic;
3.  automated tests;
4.  separation of calculation logic from user interface;
5.  easy reuse of the calculation engine by a desktop interface or other future application.

Do not over-engineer the initial implementation.

The core scoring engine should not depend on a particular CLI or future
web framework.

## 13. Required Tests

At minimum, automated tests should cover:

-   the verified A/B/C/D reference example;
-   East wins;
-   non-East wins;
-   East pays double;
-   East receives double;
-   equal losing hand values produce no payment between those players;
-   a losing player may have 0 points;
-   all round changes sum to zero;
-   cumulative totals sum to zero;
-   East remains East after East wins;
-   East rotates when another player wins;
-   East rotates after the fourth consecutive East win;
-   East win streak resets after rotation;
-   rotation wraps correctly from the fourth player to the first;
-   fewer or more than four players are rejected;
-   duplicate player names are rejected;
-   missing player scores are rejected;
-   unknown winner is rejected;
-   negative hand values are rejected;
-   odd hand values are rejected;
-   winning hand value below 22 is rejected;
-   winning hand value of exactly 22 is accepted.

## 14. Desktop Application

Phase 3 adds an offline desktop application around the tested Python
calculation engine. The GUI and CLI must use the same engine.

The desktop user flow is:

1.  Enter four player names in East/South/West/North order.
2.  Start game.
3.  For each round, see the automatically determined current East.
4.  Enter four hand values.
5.  Select the winner.
6.  Calculate round.
7.  Display each player's net change and cumulative score.
8.  Display the next East player.
9.  Continue to the next round.

Games can be saved to and opened from user-selected local files. Saved
games reconstruct state through the engine, validating every round.
Application packages are built separately for each supported operating
system. No server or online account is required to play.

This is a separate project with its own Git repository, dependencies,
build artifacts, and GitHub destination: GregorLauter/MaJong. It must not
modify or depend on any other user project.

## 15. Source of Truth

This file is the current project specification.

If implementation behavior conflicts with this document, do not silently
guess. Flag the conflict and clarify the Mah Jong rule before changing
the calculation semantics.
