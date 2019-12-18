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
### 1. 
Die zehn häufigsten Folgen von Adjektiv-Nomen Bigrammen im Corpus wurden mithilfe des folgenden SQL-Statements abgefragt.
```sql
select top 10 t1.TA_TOKEN, t2.TA_TOKEN, count(*) from "SYSTEM"."$TA_CDESCRIND" as t1, "SYSTEM"."$TA_CDESCRIND" as t2 where t1.cmplid=t2.cmplid and t1.TA_COUNTER=t2.TA_COUNTER-1 and t1.TA_SENTENCE=t2.TA_SENTENCE and t1.TA_TYPE=\'adjective\' and t2.TA_TYPE=\'noun\' group by t1.TA_TOKEN, t2.TA_TOKEN order by count(*) desc
```
Die Abfrage lieferte folgendes Ergebnis (absteigend sortiert):   
Hinweis: Im Bericht wurden nur die Top 5 dargestellt. 
|Adjektiv|Nomen|Anzahl|
|---|---|---|
|REAR|TIRE|4569|
|STEERING|WHEEL|3154|
|FRONT|TIRE|2901|
|APPROXIMATE|FAILURE|2412|
|SIDE|TIRE|2353|

### 2. 
Die zehn häufigsten Ko-Vorkommen von Adjektiven innerhalb von eines Satzes wurden mithilfe des folgenden SQL-Statements abgefragt.

```sql
select top 10 t1.TA_TOKEN as adjective, t2.TA_TOKEN as adjective2, count(*) from "SYSTEM"."$TA_CDESCRIND" as t1, "SYSTEM"."$TA_CDESCRIND" as t2 where t1.cmplid=t2.cmplid and t1.TA_COUNTER<t2.TA_COUNTER and t1.TA_SENTENCE=t2.TA_SENTENCE and t1.TA_TYPE=\'adjective\' and t2.TA_TYPE=\'adjective\' group by t1.TA_TOKEN, t2.TA_TOKEN order by count(*) desc
```
Die Abfrage lieferte folgendes Ergebnis (absteigend sortiert): 
Hinweis: Im Bericht wurden nur die Top 5 dargestellt. 
|Adjektiv|Adjektiv 2|Anzahl|
|---|---|---|
|RIGHT|REAR|1858|
|FRONT|SIDE|1752|
|REAR|SIDE|1641|
|LEFT|REAR|1627|
|RIGHT|FRONT|1496|

### 3. 
tf:
Zunächst wurde das am häufigsten vorkommende Nomen selektiert, dies konnte über folgende SQL-Abfrage realisiert werden. 

```sql
select top 1 t1.TA_TOKEN as noun, count(*) as maxfreq from "SYSTEM"."$TA_CDESCRIND" as t1 where t1.TA_TYPE=\'noun\' group by t1.TA_TOKEN order by count(*) desc
```

Im Weiteren wurde über folgende SQL-Abfrage die term frequency ausgeben.

```sql
select top 3 t1.TA_TOKEN, (count(*)/t2.maxfreq) from "SYSTEM"."$TA_CDESCRIND" as t1, "SYSTEM"."MAX_FREQ_NOUN" as t2 where t1.TA_TYPE=\'noun\' group by t1.TA_TOKEN, t2.maxfreq order by count(*) desc
```

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