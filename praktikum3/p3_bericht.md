# Praktikum 3: Janik Tinz, Patrick Tinz, Tobias Rohrer (Gruppe X-D)

## Allgemein
* Link zum GitHub Repo: [https://github.com/tobirohrer/webmining](https://github.com/tobirohrer/webmining)

## Teil 1: Fortgeschrittenes Reporting und Dokumentähnlichkeit auf zerlegten Texten (SQL)
Die Aufgaben wurden im Jupyter-Notebook [praktikum3](https://github.com/tobirohrer/webmining/blob/master/praktikum3/praktikum3.ipynb) umgesetzt.
### 1.1    
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

### 1.2 
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

### 1.3 
#### term frequency (tf):
Zunächst wurde das am häufigsten vorkommende Nomen selektiert, dies konnte über folgende SQL-Abfrage realisiert werden. 

```sql
select top 1 t1.TA_TOKEN as noun, count(*) as maxfreq from "SYSTEM"."$TA_CDESCRIND" as t1 where t1.TA_TYPE=\'noun\' group by t1.TA_TOKEN order by count(*) desc
```

Im Weiteren wurde über folgende SQL-Abfrage die term frequency ausgegeben.

```sql
select top 3 t1.TA_TOKEN, (count(*)/t2.maxfreq) from "SYSTEM"."$TA_CDESCRIND" as t1, "SYSTEM"."MAX_FREQ_NOUN" as t2 where t1.TA_TYPE=\'noun\' group by t1.TA_TOKEN, t2.maxfreq order by count(*) desc
```
Ergebnisse:
| Nomen | tf |
| :---: | :---: |
| VEHICLE | 1 |
| CAR | 0.826885 |
| TIRE | 0.798524 |

#### inverse document frequency (idf):
Die inverse document frequency konnte über folgendes SQL-Statement realisiert werden.

```sql
select TA_TOKEN, count_docs_term, n_total, LOG(10,(n_total/count_docs_term)) as idf from VALUES_IDF
```
Ergebnisse:
| Nomen | idf |
| :---: | :---: |
| TIRE | 0.562717 |
| VEHICLE | 0.405825 |
| CAR | 0.576766 |

### 1.4
Im Folgenden ist die SQL-Abfrage zu sehen, welche für den Chi2 Test benötigt wird.
```sql
select adjective, noun, o11, o12, o21, o22 from 
(
select t1.adjective, t1.noun, w1_and_w2 as o11, (sum_w1_and_w2-SUM(w1_and_w2)) as o12, t3.sum_w1_and_not_w2 as o21, (sum_NOT_w2 - t3.sum_w1_and_not_w2) as o22 from 
"SYSTEM"."ADJECTIVE_NOUN_BIGRAM" as t1, 
(select SUM(w1_and_w2) as sum_w1_and_w2 from "SYSTEM"."ADJECTIVE_NOUN_BIGRAM") as t2,
(select adjective, SUM(w1_and_not_w2) as sum_w1_and_not_w2 from "SYSTEM"."ADJECTIVE_NOUN_BIGRAM_NOT_TIRE" group by adjective) as t3,
(select SUM(w1_and_not_w2) as sum_NOT_w2 from "SYSTEM"."ADJECTIVE_NOUN_BIGRAM_NOT_TIRE" order by sum_NOT_w2 desc) as t4 where t3.adjective=t1.adjective group by t1.adjective, t1.noun, w1_and_w2, t2.sum_w1_and_w2, t3.sum_w1_and_not_w2, t4.sum_NOT_w2
)
```
Der Chi2 Test liefert folgendes Ergebnis:   
Die drei statistisch signifikantesten zusammenhängenden Bigramme mit w1=* (beliebig) und w2=Tire:    
| Adjektiv | Nomen | Chi2         
| :------: | :------: | :------: |
| SPARE | TIRE | 6579.940291 |
| SIDE | TIRE | 3694.976263 |
| FLAT | TIRE | 855.441141 |


Die drei am wenigsten statistisch signifikant zusammenhängenden Bigramme mit w1=* (beliebig) und w2=Tire:  

| Adjektiv | Nomen | Chi2         
| :------: | :------: | :------: |
| AUXILIARY | TIRE | 0.003935 |
| BACK | TIRE | 0.002535 |
| VIOLENT | TIRE | 0.000019 |

### 1.5 a
Für die Berechnung des Skalarprodukt wurde eine neue View zur Hilfe erzeugt. Diese View wurde mit folgendem SQL-Befehl erstellt: 
```sql
create view TERMS_NHTSA as SELECT CMPLID, TA_TOKEN AS WORD, count(*) AS TERM, POWER(count(*),2) AS TERMSQR FROM "SYSTEM"."$TA_CDESCRIND" WHERE TA_TYPE='noun' GROUP BY CMPLID, TA_TOKEN
```

Das Skalarprodukt wird berechnet, indem die Terme (Nomen) herausgefiltert werden, die in beiden Dokumenten vorkommen. Anschließend werden die Häufigkeiten der Nomen multipliziert und aufsummiert. Die folgende Python-Funktion wurde implementiert, um das Ähnlichkeitsmaß (Skalarprodukt) für einen gegebenen Anfragevektor auszugeben. 
```python
def scalar_product(id):
    sql = 'SELECT CMPLID, sum(PROD) AS SCALARPRODUCT FROM (SELECT a.CMPLID, a.WORD, a.TERM * b.CountReq AS PROD FROM TERMS_NHTSA AS a, (SELECT TA_TOKEN, count(*) AS CountReq FROM "SYSTEM"."$TA_CDESCRIND" WHERE CMPLID = '+id+' GROUP BY TA_TOKEN) AS b WHERE a.WORD = b.TA_TOKEN) GROUP BY CMPLID ORDER BY SCALARPRODUCT desc LIMIT 10;'
    cursor.execute(sql)
    idf = cursor.fetchall()
    idf_df = pd.DataFrame(idf)
    print(idf_df)
```

### 1.5 b
Für die Durchführung der Kosinus Ähnlichkeit wurde eine neue View zur Hilfe erzeugt. Diese View wurde mit folgendem SQL-Befehl erstellt:   
```sql
create view COS_NHTSA as SELECT x.CMPLID AS CMPLID, x.SCALARPRODUCT AS SCALARPRODUCT, y.Cos AS Cos From (SELECT CMPLID, sum(PROD) AS SCALARPRODUCT FROM (SELECT a.CMPLID, a.WORD, a.TERM * b.CountReq AS PROD FROM TERMS_NHTSA AS a, (SELECT TA_TOKEN, count(*) AS CountReq FROM "SYSTEM"."$TA_CDESCRIND" WHERE CMPLID = 119408 GROUP BY TA_TOKEN) AS b WHERE a.WORD = b.TA_TOKEN) GROUP BY CMPLID) AS x, (SELECT CMPLID, SQRT(SUM(TERMSQR)) AS Cos FROM TERMS_NHTSA GROUP BY CMPLID) AS y WHERE x.CMPLID = y.CMPLID
```
Die Cosinus Ähnlichkeit wurde mithilfe des Skalarprodukts berechnet. Schließlich wurde eine Python-Funktion implementiert, welche die Cosinus Ähnlichkeit bzgl. eines Anfragevektors ausgibt. 
```python
def cosinus(id):
    sql = 'SELECT CMPLID, SCALARPRODUCT / (Cos * (SELECT SQRT(sum(coutsqr)) FROM (SELECT TA_TOKEN, POWER(count(*),2) AS coutsqr FROM "SYSTEM"."$TA_CDESCRIND" WHERE CMPLID = '+id+' AND TA_TYPE = \'noun\' GROUP BY TA_TOKEN))) AS COSINUS FROM COS_NHTSA ORDER BY COSINUS DESC LIMIT 10'
    cursor.execute(sql)
    idf = cursor.fetchall()
    idf_df = pd.DataFrame(idf)
    print(idf_df)
```

### 1.6
Die jeweils ähnlichsten Dokumente für Complaint 119408 wurden mithilfe der beiden Funktionen aus 1.5 ermittelt. Ein Vergleich der beiden Ähnlichkeitsmaße Skalarprodukt und Cosinus Ähnlichkeit zeigt, dass man mithilfe der Cosinus Ähnlichkeit Duplikate erkennen kann. Für das Complaint 119408 liegt ein Duplikat vor. 
#### Ähnliche Dokumente für Complaint 119408
#### Top 3 Skalarprodukt
| Complaint ID  | Value         
| :-----------: |:-------------:|
| 1279795       |      37       |
|  765755       |      31       |
|  431818       |      28       |

#### Top 3 Cosinus Ähnlichkeit
| Complaint ID  | Value         
| :-----------: |:-------------:|
|    119408    |      1       |
|    119409    |      1       |
|    1456180   |    0.8819    |

### 1.7
Die Aufgaben 1.1 - 1.7 wurden auch für t3n durchgeführt. Die Umsetzung wurde im Jupyter-Notebook [praktikum3](https://github.com/tobirohrer/webmining/blob/master/praktikum3/praktikum3.ipynb) festgehalten.

## Teil 2: Evaluation
Die Aufgaben wurden im Jupyter-Notebook [praktikum3](https://github.com/tobirohrer/webmining/blob/master/praktikum3/praktikum3.ipynb) umgesetzt.

## Teil 3: Duplikaterkennung mit Shingling und MinHashing

### Freiheitsgrade zur Verbesserung
Eine Verbesserung des Precision-Recall Wertes kann durch die Erhöhung der Variable numHashes erreicht werden. Diese Variable bestimmt die Anzahl der Hashfunktionen für eine Dokumentensignatur. Der Grund für diese Verbesserung ist, dass die Wahrscheinlichkeit für eine gleiche Signatur bei zwei unterschiedlichen Dokumenten sinkt. Es folgt daraus, dass sich die False-Positive-Rate verringert und der Precision-Recall Wert erhöht. Im Weiteren kann die Anzahl der Wörter pro Shingling angepasst werden. Im nächsten Abschnitt zeigt die Tabelle, die Ergebnisse für verschiedene Parameter beim wortbasierten Shingling.


### Zeichenbasiertes Shingling
Das zeichenbasierte Shingling wurde im Skript [runMinHashExample.py](https://github.com/tobirohrer/webmining/blob/master/praktikum3/runMinHashExample.py) implementiert. Während des Ausführens des Skripts können die folgenden Parameter freigewählt werden:

* randomSeed
* numHashes
* numberShingles
* word (w) oder character (c) (Für wortbasierendes oder zeichenbasierendes Shingling)

Das wortbasierte und das zeichenbasierte Shingling wurden mit unterschiedlichen Freiheitsgraden getestet. Die Tests wurden mit einem Random-Seed Wert von 42 durchgeführt und sind in folgender Tabelle aufgelistet. 

|Shingles|Wortbasiert/ Zeichenbasiert|numHashes|Precision-Recall|
|:---:|:---:|:---:|:---:|:---:|
|3|Wortbasiert|2|0.67|
|3|Wortbasiert|4|1.00|
|6|Wortbasiert|2|0.83|
|6|Wortbasiert|4|0.95|
|6|Zeichenbasiert|2|0.05|
|6|Zeichenbasiert|4|1.00|
|12|Zeichenbasiert|2|0.83|
|12|Zeichenbasiert|4|0.99|

Zunächst fällt auf, dass beim zeichenbasierten Shingling die Anzahl der Zeichen pro Shingling eine größere Rolle spielen als beim wortbasierten Shingling. Es wurden daher sechs und zwölf Zeichen pro Shingling gewählt. Die Anzahl der Zeichen pro Shingling beim wortbasierten Shingling wurde auf drei und sechs gesetzt, da bei dieser Anzahl bereits gute Werte für den Precision-Recall erreicht werden konnten. Außerdem ist bei beiden Verfahren anzumerken, dass bei einer Verwendung von vier Hashfunktionen der Precision-Recall deutlich besser war, als bei zwei Hashfunktionen. Im Weiteren erkennt man, dass der Precision-Recall bei zwei Hashfunktionen durch die Erhöhung der Zeichenanzahl pro Shingling deutlich ansteigt, dies ist sowohl beim wortbasierten, als auch bei zeichenbasierten Shingling zu erkennen. 