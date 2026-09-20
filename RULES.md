# Mah Jong Rules

**English version below. Deutsche Version weiter unten.**

## 1. Scope

This document defines the gameplay and hand-scoring rules used by the Mah Jong project. These project rules are the source of truth and must not be silently replaced by rules from another Mah Jong variant. `SPEC.md` separately defines the application's settlement and implementation requirements.

## 2. Tiles

The game uses 144 tiles.

### Numbered suits
There are three suits, each numbered 1 through 9:
- Characters
- Bamboo
- Circles/Dots

There are four copies of each numbered tile: 108 suited tiles total.

### Winds
East, South, West and North, with four copies of each: 16 tiles.

### Dragons
Red, Green and White, with four copies of each: 12 tiles.

### Flowers and Seasons
There are eight bonus tiles: Flowers 1-4 and Seasons 1-4, one copy each.

Their numbers correspond to seat Winds:
1 = East, 2 = South, 3 = West, 4 = North.

Flowers and Seasons are exposed and replaced from the dead end of the wall. They do not remain as normal hand tiles.

## 3. Determining the Initial Winds

At the beginning of the complete game, order the four players from oldest to youngest. Starting with the oldest, each player rolls two dice and adds them.

Rank players by dice total:
1. highest = East
2. second = South
3. third = West
4. lowest = North

For a tie, the older player ranks higher.

This establishes the physical seating order for the entire game. The order is East -> South -> West -> North counterclockwise. Physical seats never change; seat Winds change as East rotates.

## 4. Round Winds and the Complete Game

A complete game ideally consists of four whole rounds:
1. East Round
2. South Round
3. West Round
4. North Round

The Round Wind applies to everyone during that whole round and affects scoring.

A whole round ends immediately when East has completed a full circuit and the player who was East at the beginning of that whole round becomes East again. The next Round Wind then begins with that player still East.

After the North Round completes its circuit, the complete game ends.

## 5. Building the Wall

Shuffle all 144 tiles face-down. Each player builds one wall of 18 two-tile stacks, giving 36 tiles per wall. The four walls form a square.

## 6. Opening the Wall

### Select the wall
East rolls two dice and adds them. Starting with East as 1, count clockwise around the table:

1 East, 2 North, 3 West, 4 South, then repeat.

This clockwise count is only for selecting the wall; normal play is counterclockwise.

### Select the break
The player whose wall was selected rolls two dice. Add this second total to East's first total. Starting from the left side of the selected wall, count that many two-tile stacks. Break the wall at that stack.

Example: first roll 5 and second roll 7 gives 12, so break at the 12th stack.

At the break, two tiles are removed and placed on top of the dead-wall side, on the first and third stacks to the left of the break. The initial deal starts from the right-hand side of the break.

## 7. Initial Deal

Starting with East and proceeding counterclockwise, each player receives two stacks (four tiles) at a time. Repeat this three times, leaving everyone with 12 tiles.

Then:
- East receives 2 more tiles, reaching 14.
- South, West and North each receive 1 more tile, reaching 13.

East starts actual play by discarding and therefore does not draw first.

## 8. Initial Flowers and Seasons

Complete the entire initial deal before replacing bonus tiles.

Everyone inspects their hand. Starting with East and continuing counterclockwise, each player exposes all Flowers and Seasons and takes the same number of replacement tiles from the dead end.

After all four players have done this, everyone checks again. If a replacement is another Flower or Season, repeat the replacement process in player order until none remain unresolved.

Only then does normal play begin.

## 9. Live and Dead Ends

Normal turn draws come from the live end. Flower/Season and Kong replacement draws come from the dead end.

At either end, simply take the next available tile, top tile first; then the lower tile; then continue to the next stack.

## 10. Normal Turn

After East's opening discard, a normal turn is:
1. draw one tile from the live wall
2. discard one tile
3. continue counterclockwise

A normal resting hand has 13 effective tiles. Flowers and Seasons do not count toward this size. A declared Kong counts as one meld because its replacement draw compensates for the fourth physical tile.

## 11. Winning Structure

Mah Jong always requires four melds plus one pair. There are no alternative winning structures such as seven pairs or thirteen orphans.

A Chow is three consecutive numbered tiles of the same suit.
A Pung is three identical tiles.
A Kong is four identical tiles and occupies one meld position.
A pair is two identical tiles.

Conceptually, the normal structure is 3 + 3 + 3 + 3 + 2, with a Kong replacing one three-tile meld where applicable.

## 12. Claiming Discards

### Chow
Only the player whose turn would normally come next may claim a discard for a Chow. The Chow is exposed.

### Pung
Any player may claim a discard that completes a Pung. The Pung is exposed. Play continues from the claimant, so players may be skipped.

### Kong
Any player holding the other three identical tiles may claim the fourth discard for a Kong. The Kong is exposed and the player takes a replacement from the dead wall.

### Mah Jong
A player may claim a discard that completes Mah Jong. The round ends immediately.

Priority is:

**Mah Jong > Pung/Kong > Chow**

A competing Pung and Kong claim for the same tile is physically impossible because only four copies exist.

If two players can both Mah Jong from the same discard, whoever calls/shouts "Mah Jong" first wins the tile and the round.

## 13. Concealed Melds

Chows and Pungs formed from self-drawn tiles do not have to be exposed. They may remain concealed, preserving flexibility and giving opponents less information.

A meld made by claiming a discard is exposed.

## 14. Kongs

A Kong must be declared because a replacement tile is required from the dead wall.

### Concealed Kong
All four matching tiles were obtained without claiming the fourth from another player's discard. The Kong is declared/revealed but receives the concealed Kong base value.

### Claimed Kong
The player holds three matching tiles and claims another player's discard as the fourth. This receives the exposed Kong base value.

### Extended Kong
A previously exposed Pung is extended after the player later draws the fourth matching tile themselves. In this ruleset, the resulting Kong receives the same higher base value as a concealed Kong.

Every declared Kong receives a dead-wall replacement.

# Scoring

## 15. Scoring Model

Scoring has two separate stages:

1. Add all base points.
2. Count all applicable doubles and multiply the complete base score.

If there are `n` doubles:

**Final hand value = total base points x 2^n**

A higher base value for a concealed meld is not itself a final-score double.

## 16. Chow Base Points

A Chow always contributes 0 points, exposed or concealed.

## 17. Pung Base Points

| Pung | Exposed | Concealed |
| --- | ---: | ---: |
| suited 2-8 | 2 | 4 |
| suited 1 or 9 | 4 | 8 |
| Wind | 4 | 8 |
| Dragon | 4 | 8 |

Wind and Dragon doubles are separate from these base values.

## 18. Kong Base Points

| Kong | Exposed | Concealed / Extended |
| --- | ---: | ---: |
| suited 2-8 | 8 | 16 |
| suited 1 or 9 | 16 | 32 |
| Wind | 16 | 32 |
| Dragon | 16 | 32 |

Every Kong also gives one final-score double.

## 19. Pair Base Points

Only one pair is treated as the hand's scoring pair.

- any Dragon pair = 2 points
- pair of the player's current seat Wind = 2 points
- any other pair = 0 points

The pair itself does not receive the Wind or Dragon doubles that apply to Pungs and Kongs. A qualifying pair can also score in a losing hand.

## 20. Flowers and Seasons

Every Flower and Season is worth 4 base points.

In addition, a Flower or Season whose number matches the player's current seat Wind gives one final-score double:

1 East, 2 South, 3 West, 4 North.

Each matching bonus tile is evaluated separately. Thus the matching Flower and matching Season together give two doubles.

## 21. Mah Jong Points

A winner receives +20 base points for Mah Jong.

### Zero-additional-points bonus
If the winning hand has literally 0 other base points before the +20 Mah Jong award, add +2 base points.

Thus four zero-point Chows plus a zero-point pair produce:
- ordinary base points = 0
- bonus = 2
- Mah Jong = 20
- base score = 22

Any other base points, including a 2-point pair or a 4-point Flower/Season, prevent this +2 bonus.

This is why 22 is the minimum valid winning value.

## 22. Final-Score Doubles

Doubles multiply the complete accumulated base score and stack exponentially.

- 1 double = x2
- 2 doubles = x4
- 3 doubles = x8
- 4 doubles = x16

The doubles are:

### Kong
Every Kong: +1 double.

### Wind
Every Wind Pung or Kong: +1 double.

### Own seat Wind
A Wind Pung or Kong matching the player's current seat Wind: +1 additional double.

### Round Wind
A Wind Pung or Kong matching the current Round Wind: +1 additional double.

Seat Wind and Round Wind are separate and can both match the same meld.

### Dragon
Every Dragon Pung or Kong: +1 double.

### Matching Flower/Season
Each Flower or Season matching the player's current seat-Wind number: +1 double.

## 23. Double-Stacking Example

During the South Round, suppose a player whose seat Wind is South has a Kong of South Winds.

It gives:
- Kong: +1 double
- Wind: +1 double
- own seat Wind: +1 double
- Round Wind: +1 double

That is four doubles, so the hand's complete base score is multiplied by 16. The Kong's base-point contribution is calculated separately according to whether it is exposed or concealed/extended.

## 24. No Other Bonuses

There are no extra points or doubles merely for:
- self-drawing Mah Jong
- winning from a discard
- a fully concealed winning hand
- winning on the last available tile
- winning with a replacement tile
- all Pungs
- one suit / pure or mixed suit
- all terminals/honours
- other whole-hand patterns from other Mah Jong variants

Only explicitly defined bonuses apply.

## 25. Losing Hands

Losing hands use the same component base values and doubles, but receive neither:
- the +20 Mah Jong award
- the winner's +2 zero-additional-points bonus

Completed scoring Pungs, Kongs, Flowers, Seasons and a qualifying scoring pair count normally. Loose or incomplete combinations do not score.

# Round Progression and Settlement

## 26. Successful Round

A successful round ends immediately when a player declares Mah Jong, either from a self-drawn tile or a claimed discard. There is no scoring difference between these two methods.

All four hands are valued, then the resulting hand values are settled.

## 27. Settlement

Each of the six unique player pairs settles once.

### Winner vs loser
Each loser pays the winner the winner's full hand value. The loser's own value does not reduce this payment.

### Loser vs loser
The lower-valued loser pays the higher-valued loser the difference. Equal values produce no payment.

### East settlement multiplier
Every payment involving the player who was East during that round is multiplied by 2, whether East pays, receives, wins or loses.

This settlement x2 is completely separate from hand-scoring doubles.

### Zero-sum invariant
Every round's net settlement changes must sum to zero, and cumulative totals must also sum to zero.

## 28. East Rotation

Physical seating remains fixed.

If East wins, East stays East and the consecutive East-win counter increases by one.

If another player wins, East moves one position forward in the fixed counterclockwise seating order and the consecutive-win counter resets. East moves to the next seat, not directly to the winner.

If East wins four consecutive successful rounds while holding East, East rotates after the fourth win anyway and the counter resets.

## 29. Unsuccessful Round

When fewer than 8 tiles remain in total as the live and dead ends converge, the round is unsuccessful and is restarted.

There is:
- no winner
- no settlement
- no cumulative-score change
- no East rotation
- no change to East's consecutive-win counter

Shuffle, rebuild and restart with the same East.

## 30. Whole-Round Boundary

A whole Round Wind ends immediately when East has completed a full circuit and the player who began that whole round as East becomes East again.

The Round Wind then advances:

**East -> South -> West -> North**

The next whole round begins with that same player as East.

After the North Round completes its circuit, the complete game ends.

## 31. Three Different Kinds of Doubling

These must remain distinct.

### Meld base-value increases
Concealed Pungs/Kongs and terminal/honour melds have higher base-point values. These affect only the meld's base contribution.

### Hand-scoring doubles
Kong, Wind, own seat Wind, Round Wind, Dragon and matching Flower/Season doubles multiply the complete accumulated hand base score.

### East settlement multiplier
East's x2 applies only to payments between players after hand values have been calculated. It does not alter the intrinsic hand value.

## 32. Source of Truth

These rules were established specifically for the Mah Jong project.

Do not substitute rules from Japanese Riichi, Hong Kong Mah Jong, Mah Jong Competition Rules or another variant. Do not invent special hands or bonuses. If an implementation-relevant ambiguity remains, ask rather than infer an external rule.

`RULES.md` defines gameplay and hand scoring.

`SPEC.md` defines application settlement behavior and implementation requirements.

---

# Deutsche Version

## 1. Geltungsbereich

Dieses Dokument definiert die Spiel- und Wertungsregeln des Mah Jong-Projekts. Diese projektspezifischen Regeln sind maßgeblich und dürfen nicht stillschweigend durch Regeln einer anderen Mah Jong-Variante ersetzt werden. `SPEC.md` definiert separat die Anforderungen an die Abrechnung und Implementierung der Anwendung.

## 2. Spielsteine

Das Spiel verwendet 144 Steine.

### Zahlenfarben
Es gibt drei Farben mit den Zahlen 1 bis 9:
- Zeichen
- Bambus
- Kreise/Punkte

Von jedem Zahlenstein gibt es vier Exemplare. Insgesamt sind dies 108 Zahlensteine.

### Winde
Ost, Süd, West und Nord, jeweils viermal: insgesamt 16 Steine.

### Drachen
Roter, Grüner und Weißer Drache, jeweils viermal: insgesamt 12 Steine.

### Blumen und Jahreszeiten
Es gibt acht Bonussteine: Blumen 1 bis 4 und Jahreszeiten 1 bis 4, jeweils einmal.

Die Nummern entsprechen den Sitzwinden:
1 = Ost, 2 = Süd, 3 = West, 4 = Nord.

Blumen und Jahreszeiten werden aufgedeckt und vom toten Ende der Mauer ersetzt. Sie bleiben nicht als normale Steine in der Hand.

## 3. Bestimmung der anfänglichen Winde

Zu Beginn des gesamten Spiels werden die vier Spieler nach Alter vom ältesten zum jüngsten geordnet. Beginnend mit dem ältesten Spieler würfelt jeder mit zwei Würfeln und addiert die Augenzahlen.

Die Spieler werden nach Würfelsumme eingeordnet:
1. höchste Summe = Ost
2. zweithöchste Summe = Süd
3. dritthöchste Summe = West
4. niedrigste Summe = Nord

Bei Gleichstand wird der ältere Spieler höher eingeordnet.

Damit wird die physische Sitzordnung für das gesamte Spiel festgelegt. Die Reihenfolge Ost -> Süd -> West -> Nord verläuft gegen den Uhrzeigersinn. Die physischen Sitzplätze ändern sich nicht; die Sitzwinde ändern sich, wenn die Ost-Position weitergegeben wird.

## 4. Rundenwinde und vollständiges Spiel

Ein vollständiges Spiel besteht idealerweise aus vier vollständigen Runden:

1. Ostrunde
2. Südrunde
3. Westrunde
4. Nordrunde

Der Rundenwind gilt während der gesamten jeweiligen Runde für alle Spieler und beeinflusst die Wertung.

Eine vollständige Runde endet sofort, wenn die Ost-Position einmal vollständig um den Tisch gewandert ist und der Spieler, der zu Beginn dieser Runde Ost war, wieder Ost wird. Anschließend beginnt der nächste Rundenwind, wobei dieser Spieler zunächst Ost bleibt.

Nach Abschluss der Nordrunde endet das vollständige Spiel.

## 5. Aufbau der Mauer

Alle 144 Steine werden verdeckt gemischt. Jeder Spieler baut vor sich eine Mauer aus 18 Stapeln mit jeweils zwei Steinen. Damit besteht jede Seite aus 36 Steinen.

Die vier Mauern bilden ein Quadrat.

## 6. Öffnen der Mauer

### Auswahl der Mauer
Ost würfelt mit zwei Würfeln und addiert die Augenzahlen. Beginnend mit Ost als 1 wird im Uhrzeigersinn um den Tisch gezählt:

1 Ost, 2 Nord, 3 West, 4 Süd, anschließend wieder von vorn.

Diese Zählrichtung im Uhrzeigersinn gilt nur für die Auswahl der Mauer. Das eigentliche Spiel verläuft gegen den Uhrzeigersinn.

### Bestimmung der Bruchstelle
Der Spieler, dessen Mauer ausgewählt wurde, würfelt mit zwei Würfeln. Diese zweite Würfelsumme wird zur ersten Würfelsumme von Ost addiert.

Von der linken Seite der ausgewählten Mauer aus wird diese Anzahl an Zwei-Stein-Stapeln abgezählt. An diesem Stapel wird die Mauer geöffnet.

Beispiel: Erste Würfelsumme 5 und zweite Würfelsumme 7 ergeben 12. Die Mauer wird am 12. Stapel geöffnet.

An der Bruchstelle werden zwei Steine entnommen und auf der Seite des toten Mauerendes auf den ersten beziehungsweise dritten Stapel links von der Bruchstelle gelegt. Die anfängliche Ausgabe beginnt rechts von der Bruchstelle.

## 7. Anfängliche Ausgabe

Beginnend mit Ost und anschließend gegen den Uhrzeigersinn erhält jeder Spieler jeweils zwei Stapel, also vier Steine.

Dies wird dreimal wiederholt, sodass jeder Spieler zunächst 12 Steine besitzt.

Danach:
- Ost erhält 2 weitere Steine und hat damit 14.
- Süd, West und Nord erhalten jeweils 1 weiteren Stein und haben damit jeweils 13.

Ost beginnt das eigentliche Spiel mit einem Abwurf und zieht daher vor dem ersten Abwurf keinen Stein.

## 8. Blumen und Jahreszeiten bei der anfänglichen Ausgabe

Zunächst wird die gesamte anfängliche Ausgabe abgeschlossen. Erst danach werden Bonussteine ersetzt.

Alle Spieler überprüfen ihre Hand. Beginnend mit Ost und anschließend gegen den Uhrzeigersinn deckt jeder Spieler alle Blumen und Jahreszeiten auf und nimmt dieselbe Anzahl an Ersatzsteinen vom toten Ende der Mauer.

Nachdem alle vier Spieler dies durchgeführt haben, wird erneut überprüft. Befindet sich unter den Ersatzsteinen eine weitere Blume oder Jahreszeit, wird der Ersatzvorgang erneut in derselben Spielerreihenfolge durchgeführt.

Dies wird wiederholt, bis keine unersetzte Blume oder Jahreszeit mehr vorhanden ist.

Erst danach beginnt das normale Spiel.

## 9. Lebendes und totes Ende der Mauer

Normale Züge erfolgen vom lebenden Ende der Mauer. Ersatzsteine für Blumen, Jahreszeiten und Kongs werden vom toten Ende genommen.

An beiden Enden wird jeweils der nächste verfügbare Stein genommen: zuerst der obere Stein eines Stapels, danach der untere, anschließend der nächste Stapel.

## 10. Normaler Spielzug

Nach dem ersten Abwurf von Ost besteht ein normaler Zug aus:

1. einen Stein vom lebenden Ende ziehen
2. einen Stein abwerfen
3. gegen den Uhrzeigersinn weiterspielen

Eine normale ruhende Hand besteht aus 13 effektiven Handsteinen. Blumen und Jahreszeiten zählen nicht zu dieser Handgröße.

Ein deklarierter Kong zählt als ein Meld, da der vierte physische Stein durch einen Ersatzstein ausgeglichen wird.

## 11. Struktur einer Gewinnhand

Mah Jong besteht immer aus vier Melds und einem Paar.

Alternative Gewinnstrukturen wie sieben Paare oder dreizehn Waisen gibt es in diesen Regeln nicht.

Ein Chow besteht aus drei aufeinanderfolgenden Zahlensteinen derselben Farbe.

Ein Pung besteht aus drei identischen Steinen.

Ein Kong besteht aus vier identischen Steinen und belegt eine Meld-Position.

Ein Paar besteht aus zwei identischen Steinen.

Die normale Struktur ist somit konzeptionell:

**3 + 3 + 3 + 3 + 2**

Ein Kong ersetzt dabei gegebenenfalls eines der Drei-Stein-Melds.

## 12. Beanspruchen abgeworfener Steine

### Chow
Nur der Spieler, der als Nächstes regulär an der Reihe wäre, darf einen abgeworfenen Stein für einen Chow beanspruchen. Der Chow wird offen ausgelegt.

### Pung
Jeder Spieler darf einen Abwurf beanspruchen, wenn dieser einen Pung vervollständigt. Der Pung wird offen ausgelegt. Das Spiel wird beim beanspruchenden Spieler fortgesetzt, sodass andere Spieler übersprungen werden können.

### Kong
Jeder Spieler, der die anderen drei identischen Steine besitzt, darf den vierten abgeworfenen Stein für einen Kong beanspruchen. Der Kong wird offen ausgelegt und der Spieler zieht einen Ersatzstein vom toten Ende.

### Mah Jong
Ein Spieler darf einen Abwurf beanspruchen, wenn dieser seine Mah Jong-Hand vervollständigt. Die Hand endet sofort.

Die Priorität lautet:

**Mah Jong > Pung/Kong > Chow**

Eine konkurrierende Pung- und Kong-Beanspruchung desselben Steins ist physisch nicht möglich, da von jedem normalen Stein nur vier Exemplare existieren.

Könnten zwei Spieler mit demselben Abwurf Mah Jong erreichen, gewinnt derjenige den Stein und die Hand, der zuerst "Mah Jong" ruft.

## 13. Verdeckte Melds

Chows und Pungs, die ausschließlich aus selbst gezogenen Steinen gebildet wurden, müssen während des Spiels nicht aufgedeckt werden. Sie können verdeckt in der Hand bleiben.

Ein durch Beanspruchen eines Abwurfs gebildetes Meld wird offen ausgelegt.

## 14. Kongs

Ein Kong muss deklariert werden, da ein Ersatzstein vom toten Ende benötigt wird.

### Verdeckter Kong
Alle vier identischen Steine wurden erhalten, ohne den vierten Stein aus dem Abwurf eines anderen Spielers zu beanspruchen. Der Kong wird deklariert und aufgedeckt, erhält aber den Grundwert eines verdeckten Kongs.

### Beanspruchter Kong
Der Spieler besitzt drei identische Steine und beansprucht den Abwurf eines anderen Spielers als vierten Stein. Dieser Kong erhält den Grundwert eines offenen Kongs.

### Erweiterter Kong
Ein zuvor offener Pung wird erweitert, nachdem der Spieler den vierten identischen Stein später selbst zieht. In diesem Regelwerk erhält dieser Kong denselben höheren Grundwert wie ein verdeckter Kong.

Für jeden deklarierten Kong wird ein Ersatzstein vom toten Ende gezogen.

# Wertung

## 15. Wertungsmodell

Die Wertung erfolgt in zwei getrennten Schritten:

1. Alle Grundpunkte werden addiert.
2. Alle anwendbaren Verdopplungen werden gezählt und auf die gesamte Grundpunktzahl angewendet.

Bei `n` Verdopplungen gilt:

**Endwert der Hand = gesamte Grundpunkte x 2^n**

Ein höherer Grundwert für ein verdecktes Meld ist selbst keine zusätzliche Verdopplung des Endwerts.

## 16. Grundpunkte für Chows

Ein Chow bringt immer 0 Punkte, unabhängig davon, ob er offen oder verdeckt ist.

## 17. Grundpunkte für Pungs

| Pung | Offen | Verdeckt |
| --- | ---: | ---: |
| Zahlenstein 2-8 | 2 | 4 |
| Zahlenstein 1 oder 9 | 4 | 8 |
| Wind | 4 | 8 |
| Drache | 4 | 8 |

Verdopplungen durch Winde und Drachen werden separat berechnet.

## 18. Grundpunkte für Kongs

| Kong | Offen | Verdeckt / Erweitert |
| --- | ---: | ---: |
| Zahlenstein 2-8 | 8 | 16 |
| Zahlenstein 1 oder 9 | 16 | 32 |
| Wind | 16 | 32 |
| Drache | 16 | 32 |

Jeder Kong gibt zusätzlich eine Verdopplung des Endwerts.

## 19. Grundpunkte für das Paar

Nur ein Paar wird als Wertungspaar der Hand behandelt.

- Paar eines beliebigen Drachen = 2 Punkte
- Paar des aktuellen Sitzwinds des Spielers = 2 Punkte
- jedes andere Paar = 0 Punkte

Das Paar selbst erhält nicht die Wind- oder Drachen-Verdopplungen, die für Pungs und Kongs gelten.

Ein qualifizierendes Paar kann auch in der Hand eines Verlierers gewertet werden.

## 20. Blumen und Jahreszeiten

Jede Blume und jede Jahreszeit ist 4 Grundpunkte wert.

Zusätzlich gibt eine Blume oder Jahreszeit, deren Nummer dem aktuellen Sitzwind des Spielers entspricht, eine Verdopplung:

1 Ost, 2 Süd, 3 West, 4 Nord.

Jeder passende Bonusstein wird einzeln gewertet. Eine passende Blume und eine passende Jahreszeit ergeben daher zusammen zwei Verdopplungen.

## 21. Mah Jong-Punkte

Der Gewinner erhält für Mah Jong:

**+20 Grundpunkte**

### Bonus für null zusätzliche Grundpunkte
Hat die Gewinnhand vor den +20 Mah Jong-Punkten tatsächlich 0 andere Grundpunkte, erhält der Gewinner zusätzlich:

**+2 Grundpunkte**

Vier Chows mit jeweils 0 Punkten und ein Paar mit 0 Punkten ergeben daher:

- normale Grundpunkte = 0
- Bonus = 2
- Mah Jong = 20
- Grundwert = 22

Sobald andere Grundpunkte vorhanden sind, etwa durch ein 2-Punkte-Paar oder eine Blume/Jahreszeit mit 4 Punkten, entfällt der +2-Bonus.

Daher beträgt der kleinste gültige Gewinnwert 22 Punkte.

## 22. Verdopplungen des Endwerts

Verdopplungen werden auf die gesamte angesammelte Grundpunktzahl angewendet und stapeln sich exponentiell:

- 1 Verdopplung = x2
- 2 Verdopplungen = x4
- 3 Verdopplungen = x8
- 4 Verdopplungen = x16

Es gelten folgende Verdopplungen:

### Kong
Jeder Kong: +1 Verdopplung.

### Wind
Jeder Wind-Pung oder Wind-Kong: +1 Verdopplung.

### Eigener Sitzwind
Ein Wind-Pung oder Wind-Kong, der dem aktuellen Sitzwind des Spielers entspricht: +1 zusätzliche Verdopplung.

### Rundenwind
Ein Wind-Pung oder Wind-Kong, der dem aktuellen Rundenwind entspricht: +1 zusätzliche Verdopplung.

Sitzwind und Rundenwind werden getrennt gewertet und können beide auf dasselbe Meld zutreffen.

### Drache
Jeder Drachen-Pung oder Drachen-Kong: +1 Verdopplung.

### Passende Blume/Jahreszeit
Jede Blume oder Jahreszeit, deren Nummer dem aktuellen Sitzwind des Spielers entspricht: +1 Verdopplung.

## 23. Beispiel für mehrere Verdopplungen

Während der Südrunde besitzt ein Spieler mit Sitzwind Süd einen Kong aus Südwinden.

Dieser gibt:

- Kong: +1 Verdopplung
- Wind: +1 Verdopplung
- eigener Sitzwind: +1 Verdopplung
- Rundenwind: +1 Verdopplung

Das sind vier Verdopplungen. Der gesamte Grundwert der Hand wird daher mit 16 multipliziert.

Der Grundpunktwert des Kongs selbst wird separat danach berechnet, ob der Kong offen oder verdeckt/erweitert ist.

## 24. Keine weiteren Boni

Es gibt keine zusätzlichen Punkte oder Verdopplungen allein für:

- selbst gezogenes Mah Jong
- Mah Jong durch einen Abwurf
- eine vollständig verdeckte Gewinnhand
- Gewinn mit dem letzten verfügbaren Stein
- Gewinn mit einem Ersatzstein
- eine Hand nur aus Pungs
- reine oder gemischte Einfarbenhände
- Hände nur aus Randsteinen/Ehrensteinen
- andere vollständige Handmuster aus anderen Mah Jong-Varianten

Es gelten ausschließlich die ausdrücklich in diesem Dokument definierten Boni.

## 25. Wertung der Verlierer

Die Hände der Verlierer verwenden dieselben Grundwerte und Verdopplungen für ihre wertbaren Bestandteile, erhalten jedoch weder:

- die +20 Punkte für Mah Jong
- noch den +2-Bonus für eine Gewinnhand ohne weitere Grundpunkte

Vollständige wertbare Pungs, Kongs, Blumen, Jahreszeiten und ein qualifizierendes Wertungspaar zählen normal.

Lose Steine oder unvollständige Kombinationen zählen nicht.

# Rundenverlauf und Abrechnung

## 26. Erfolgreiche Hand

Eine erfolgreiche Hand endet sofort, sobald ein Spieler Mah Jong erklärt, entweder mit einem selbst gezogenen Stein oder mit einem beanspruchten Abwurf.

Zwischen diesen beiden Gewinnarten gibt es keinen Wertungsunterschied.

Anschließend werden die Werte aller vier Hände berechnet und miteinander abgerechnet.

## 27. Abrechnung

Jedes der sechs eindeutigen Spielerpaare rechnet genau einmal miteinander ab.

### Gewinner gegen Verlierer
Jeder Verlierer zahlt dem Gewinner den vollständigen Handwert des Gewinners. Der eigene Handwert des Verlierers reduziert diese Zahlung nicht.

### Verlierer gegen Verlierer
Zwischen zwei Verlierern zahlt der Spieler mit dem niedrigeren Handwert dem Spieler mit dem höheren Handwert die Differenz ihrer Werte.

Bei identischen Handwerten erfolgt keine Zahlung.

### Ost-Multiplikator bei der Abrechnung
Jede Zahlung, an der der Spieler beteiligt ist, der während dieser Hand Ost war, wird mit 2 multipliziert.

Dies gilt unabhängig davon, ob Ost:
- zahlt
- erhält
- gewinnt
- verliert

Dieser Abrechnungsfaktor ist vollständig von den Verdopplungen der Handwertung getrennt.

### Nullsummenbedingung
Jede Zahlung verlässt einen Spieler und erreicht einen anderen. Daher müssen sowohl die Nettoänderungen jeder Hand als auch die kumulierten Gesamtstände in Summe 0 ergeben.

## 28. Weitergabe von Ost

Die physischen Sitzplätze bleiben unverändert.

Gewinnt Ost, bleibt derselbe Spieler Ost und der Zähler für aufeinanderfolgende Siege als Ost wird um eins erhöht.

Gewinnt ein anderer Spieler, wandert Ost um genau eine Position in der festen Sitzreihenfolge gegen den Uhrzeigersinn weiter. Der Zähler wird zurückgesetzt. Ost geht also an den nächsten Sitz und nicht automatisch an den Gewinner.

Gewinnt Ost vier erfolgreiche Hände in Folge als Ost, wird Ost nach dem vierten Sieg trotzdem an den nächsten Sitz weitergegeben. Der Zähler wird anschließend zurückgesetzt.

## 29. Erfolglose Hand

Wenn beim Zusammenlaufen des lebenden und toten Endes insgesamt weniger als 8 Steine verbleiben, ist die Hand erfolglos und wird neu gestartet.

Dabei gibt es:
- keinen Gewinner
- keine Abrechnung
- keine Änderung des Gesamtstands
- keine Weitergabe von Ost
- keine Änderung des Zählers für aufeinanderfolgende Ost-Siege

Die Steine werden neu gemischt, die Mauer wird neu aufgebaut und mit demselben Ost erneut begonnen.

## 30. Ende einer vollständigen Runde

Eine vollständige Rundenwind-Runde endet sofort, wenn Ost einmal vollständig um den Tisch gewandert ist und der Spieler, der zu Beginn dieser Runde Ost war, wieder Ost wird.

Danach wechselt der Rundenwind:

**Ost -> Süd -> West -> Nord**

Die nächste vollständige Runde beginnt mit demselben Spieler als Ost.

Nach Abschluss der Nordrunde endet das gesamte Spiel.

## 31. Drei verschiedene Arten der Verdopplung

Diese Konzepte müssen getrennt bleiben.

### Erhöhung des Meld-Grundwerts
Verdeckte Pungs/Kongs sowie Melds aus Randsteinen, Winden oder Drachen besitzen höhere Grundwerte. Dies verändert nur den Grundpunktbeitrag des jeweiligen Melds.

### Verdopplungen der Handwertung
Kong, Wind, eigener Sitzwind, Rundenwind, Drache und passende Blume/Jahreszeit können den gesamten angesammelten Grundwert der Hand verdoppeln.

### Ost-Multiplikator bei der Abrechnung
Der Faktor x2 für Ost wird erst auf Zahlungen zwischen Spielern angewendet, nachdem die Handwerte vollständig berechnet wurden. Er verändert nicht den eigentlichen Wert der Hand.

## 32. Maßgebliche Regeln

Diese Regeln wurden speziell für das Mah Jong-Projekt festgelegt.

Regeln aus japanischem Riichi-Mah Jong, Hongkong-Mah Jong, Mah Jong Competition Rules oder anderen Varianten dürfen nicht ersatzweise übernommen werden. Es dürfen keine zusätzlichen Spezialhände oder Boni erfunden werden.

Bleibt eine für die Implementierung relevante Regel unklar, muss nachgefragt werden, statt eine externe Regel anzunehmen.

`RULES.md` definiert Spielablauf und Handwertung.

`SPEC.md` definiert die Anforderungen an Abrechnung und Implementierung der Anwendung.
