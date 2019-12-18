# Praktikum 3: Janik Tinz, Patrick Tinz, Tobias Rohrer (Gruppe X-D)

## Allgemein
* Link zum GitHub Repo: [https://github.com/tobirohrer/webmining](https://github.com/tobirohrer/webmining)

## Vorbereitung 
### Ähnliche Dokumente 

### Themenbereich - Identifizierung von relevanten Dokumenten
* Kategorie: Gadgets und Lifestyle 

### Gewichtete Anfragen im Vektorraum T3N


### Anfragevektoren NHTSA Complaints


## Teil 1: Fortgeschrittenes Reporting und Dokumentähnlichkeit auf zerlegten Texten (SQL)


## Teil 2: Evaluation


## Teil 3: Duplikaterkennung mit Shingling und MinHashing
### 1. Nachvollziehen der einzelnen Schritte

### 2. Freiheitsgrade zur Verbesserung
Eine Verbesserung des Precision-Recall Wertes kann durch die Erhöhung der Variable numHashes ereicht werden. Diese Variable bestimmt die Anzahl der Hashfunktionen für eine Dokumentensignatur. Der Grund für diese Verbesserung ist, dass die Wahrscheinlichkeit für eine gleiche Signatur bei zwei unterschiedlichen Dokumenten sinkt. Es folgt daraus, dass sich die False-Positive-Rate verringert und der Precision-Recall Wert erhöht. Im Weiteren kann die Anzahl der Wörter pro Shingling angepasst werden. Im nächsten Abschnitt zeigt die Tabelle, die Ergebnisse für verschiedene Parameter beim wortbasierten Shingling.


### 3. Zeichenbasiertes Shingling
Das wortbasierte und das zeichenbasierte Shingling wurden mit unterschiedlichen Freiheitsgraden getetest. Die Tests wurden mit einem Random-Seed Wert von 42 durchgeführt und sind in folgender Tabelle aufgelistet. 

|Shingles|Wortbasiert/ Zeichenbasiert|numHashes|Precision-Recall|
|---|---|---|---|---|
|3|Wortbasiert|2|0.67|
|3|Wortbasiert|4|1.00|
|6|Wortbasiert|2|0.83|
|6|Wortbasiert|4|0.95|
|6|Zeichenbasiert|2|0.05|
|6|Zeichenbasiert|4|1.00|
|12|Zeichenbasiert|2|0.83|
|12|Zeichenbasiert|4|0.99|

Zunächst fällt auf, dass beim zeichenbasierten Shingling die Anzahl der Zeichen pro Shingling eine größere Rolle spielt als beim wortbasierten Shingling. Es wurde daher sechs und zwölf Zeichen pro Shingling gewählt. Die Anzahl der Zeichen pro Shingling beim wortbasierten Shingling wurde auf drei und sechs gesetzt, da bei dieser Anzahl bereits gute Werte für den Precision-Recall erreicht werden konnten. Außerdem ist bei beiden Verfahren anzumerken, dass bei einer Verwendung von vier Hashfunktionen der Precision-Recall deutlich besser war, als bei zwei Hashfunktionen. Im Weiteren erkennt man, dass der Precision-Recall bei zwei Hashfunktionen durch die Erhöhung der Zeichenanzahl pro Shingling deutlich ansteigt, dies ist sowohl beim wortbasierten, als auch bei zeichenbasierten Shingling zu erkennen. 