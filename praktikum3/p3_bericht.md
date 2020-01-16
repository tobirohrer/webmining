# Praktikum 3: Janik Tinz, Patrick Tinz, Tobias Rohrer (Gruppe X-D)

## Allgemein
* Link zum GitHub Repo: [https://github.com/tobirohrer/webmining](https://github.com/tobirohrer/webmining)

## Teil 1: Fortgeschrittenes Reporting und Dokumentähnlichkeit auf zerlegten Texten (SQL)
Die Aufgaben wurden im Jupyter-Notebook [praktikum3](https://github.com/tobirohrer/webmining/blob/master/praktikum3/praktikum3.ipynb) umgesetzt.
### 1.1    
Die zehn häufigsten Folgen von Adjektiv-Nomen Bigrammen im Corpus wurden mithilfe des folgenden SQL-Statements abgefragt.
```sql
select top 10 t1.TA_TOKEN, t2.TA_TOKEN, count(*) from "SYSTEM"."$TA_CDESCRIND" as t1, "SYSTEM"."$TA_CDESCRIND" as t2 where t1.cmplid=t2.cmplid and t1.TA_COUNTER=t2.TA_COUNTER-1 and t1.TA_SENTENCE=t2.TA_SENTENCE and t1.TA_TYPE=\'adjective\' and t2.TA_TYPE=\'noun\' group by t1.TA_TOKEN, t2.TA_TOKEN order by count(*) desc
```
Die Abfrage lieferte folgendes Ergebnis (absteigend sortiert):   
Hinweis: Im Bericht wurden nur die Top 5 dargestellt.     

| Adjektiv  | Nomen | Anzahl    
| :-----------: | :-----------: | :-----------: |
| REAR          | TIRE          | 4569          |
| STEERING      | WHEEL         | 3154          |
| FRONT         | TIRE          | 2901          |
| APPROXIMATE   | FAILURE       | 2412          |
| SIDE          | TIRE          | 2353          |

### 1.2 
Die zehn häufigsten Ko-Vorkommen von Adjektiven innerhalb von eines Satzes wurden mithilfe des folgenden SQL-Statements abgefragt.

```sql
select top 10 t1.TA_TOKEN as adjective, t2.TA_TOKEN as adjective2, count(*) from "SYSTEM"."$TA_CDESCRIND" as t1, "SYSTEM"."$TA_CDESCRIND" as t2 where t1.cmplid=t2.cmplid and t1.TA_COUNTER<t2.TA_COUNTER and t1.TA_SENTENCE=t2.TA_SENTENCE and t1.TA_TYPE=\'adjective\' and t2.TA_TYPE=\'adjective\' group by t1.TA_TOKEN, t2.TA_TOKEN order by count(*) desc
```
Die Abfrage lieferte folgendes Ergebnis (absteigend sortiert):   
Hinweis: Im Bericht wurden nur die Top 5 dargestellt.

| Adjektiv  | Adjektiv 2 | Anzahl   
|:---:|:---:|:---:|
|RIGHT|REAR|1858|
|FRONT|SIDE|1752|
|REAR|SIDE|1641|
|LEFT|REAR|1627|
|RIGHT|FRONT|1496|

### 1.3 
#### term frequency (tf):
Zunächst wurde eine SQL-View angelegt, welche die Vorkommenshäufigkeit (term frequency) von einen Term in jeweiligen Dokument beinhaltet. 

```sql
create view MAX_FREQ_NOUN as select CMPLID as CMPLID, TA_TOKEN as noun, count(*) as tf from "$TA_CDESCRIND" where TA_TYPE=\'noun\' group by CMPLID, TA_TOKEN order by count(*) desc
```

Im Weiteren wurde über folgende SQL-Abfrage die term frequency ausgegeben.

```sql
select top 3 CMPLID, noun, tf from MAX_FREQ_NOUN
```
Ergebnisse: 

| CMPLID | noun  | tf         
| :-----------: |:-------------:|:-------------:|
| 646431      |      TIRE       |     23     |
| 646433      |      TIRE       |     23    |
| 1405206       |      CAR      |     22   |

#### inverse document frequency (idf):
Die inverse document frequency wurde mithilfe von drei Views realisiert. Im Folgenden sind die SQL-Befehle zusehen. 

```sql
create view COUNT_DOCS as select count(DISTINCT cmplid) as n_total from "SYSTEM"."$TA_CDESCRIND"
```
```sql
create view VALUES_DF as select TA_TOKEN as noun, count(DISTINCT CMPLID) as DF from "$TA_CDESCRIND" where TA_TYPE=\'noun\' group by TA_TOKEN
```
```sql
create view VALUES_IDF as select t1.noun, ln((t2.n_total/t1.DF)) as idf from VALUES_DF as t1, COUNT_DOCS as t2 order by idf desc
```

Das folgende SQL-Statement liefert schließlich die Ausgabe zu der inverse document frequency.

```sql
select top 3 * from VALUES_IDF
```
Ergebnisse:

| Nomen  | idf        
| :-----------: |:-------------:|
| MILLIAMPS | 11.541007 |
| MILLAGE | 11.541007 |
| MILLER | 11.541007 |

Die top-3 tf-idf (ntn nach der SMART Notation) Werte von Nomen im Corpus sind in folgender Tabelle zu sehen:

| CMPLID | noun  | tf   |   idf   |   tfidf |
| :-----------: |:-------------:|:-------------:|:-------------:|:-------------:|
|    769417       |      DEFLECTORS       |       14      |   9.749248    |      136.489472     |
|      1001131     |       PLATFORM      |      15       |   8.139810    |    122.097151       |
|      1001132     |        PLATFORM     |      15       |    8.139810   |     122.097151       |


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
Die drei statistisch signifikantesten zusammenhängenden Bigramme mit w1=* (beliebig) und w2=Tire:    

| Adjektiv | Nomen | Chi2         
| :------: | :------: | :------: |
| REAR | TIRE | 6660.536074 |
| SPARE | TIRE | 3872.408630 |
| SIDE | TIRE | 2849.785685 |

Die drei am wenigsten statistisch signifikant zusammenhängenden Bigramme mit w1=* (beliebig) und w2=Tire:  

| Adjektiv | Nomen | Chi2         
| :------: | :------: | :------: |
| TWIN | TIRE | 0.000614 |
| BROUGHT | TIRE | 0.000415 |
| TANDEM | TIRE | 0.000024 |

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
Die jeweils ähnlichsten Dokumente für Complaint 119408 wurden mithilfe der beiden Funktionen aus 1.5 ermittelt. Ein Vergleich der beiden Ähnlichkeitsmaße Skalarprodukt und Cosinus Ähnlichkeit zeigt, dass man mithilfe der Cosinus Ähnlichkeit Duplikate besser erkennen kann. Für das Complaint 119408 liegt ein Duplikat vor. 
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
Die Aufgaben 1.1 - 1.7 wurden auch für t3n durchgeführt. Die Umsetzung wurde ebenfalls im Jupyter-Notebook [praktikum3](https://github.com/tobirohrer/webmining/blob/master/praktikum3/praktikum3.ipynb) durchgeführt.

### 1.7.1    
Die zehn häufigsten Folgen von Adjektiv-Nomen Bigrammen im Corpus wurden mithilfe des folgenden SQL-Statements abgefragt.
```sql
select top 10 t1.TA_TOKEN, t2.TA_TOKEN, count(*) from "SYSTEM"."$TA_T3NTEXTIND" as t1, "SYSTEM"."$TA_T3NTEXTIND" as t2 where t1.ID=t2.ID and t1.TA_COUNTER=t2.TA_COUNTER-1 and t1.TA_SENTENCE=t2.TA_SENTENCE and t1.TA_TYPE=\'adjective\' and t2.TA_TYPE=\'noun\' group by t1.TA_TOKEN, t2.TA_TOKEN order by count(*) desc
```
Die Abfrage lieferte folgendes Ergebnis (absteigend sortiert):   
Hinweis: Im Bericht wurden nur die Top 5 dargestellt.     

| Adjektiv  | Nomen | Anzahl    
| :-----------: | :-----------: | :-----------: |
| vergangenen   | Jahr          | 49            |
| erster        | Linie         | 48            |
| ersten        | Blick         | 39            |
| Sublime       | Text          | 34            |
| letzten       | Jahr          | 33            |

### 1.7.2 
Die zehn häufigsten Ko-Vorkommen von Adjektiven innerhalb von eines Satzes wurden mithilfe des folgenden SQL-Statements abgefragt.

```sql
select top 10 t1.TA_TOKEN as adjective, t2.TA_TOKEN as adjective2, count(*) from "SYSTEM"."$TA_T3NTEXTIND" as t1, "SYSTEM"."$TA_T3NTEXTIND" as t2 where t1.ID=t2.ID and t1.TA_COUNTER<t2.TA_COUNTER and t1.TA_SENTENCE=t2.TA_SENTENCE and t1.TA_TYPE=\'adjective\' and t2.TA_TYPE=\'adjective\' group by t1.TA_TOKEN, t2.TA_TOKEN order by count(*) desc
```
Die Abfrage lieferte folgendes Ergebnis (absteigend sortiert):   
Hinweis: Im Bericht wurden nur die Top 5 dargestellt.

| Adjektiv  | Adjektiv 2 | Anzahl   
|:---:|:---:|:---:|
|neue|neuen|39|
|neuen|neuen|38|
|neuen|neue|23|
|neue|neue|23|
|neue|ersten|16|

### 1.7.3 
#### term frequency (tf):
Zunächst wurde eine SQL-View angelegt, welche die Vorkommenshäufigkeit (term frequency) von einen Term in jeweiligen Dokument beinhaltet. 

```sql
create view MAX_FREQ_NOUN_T3N as select ID as ID, TA_TOKEN as noun, count(*) as tf from "$TA_T3NTEXTIND" where TA_TYPE=\'noun\' group by ID, TA_TOKEN order by count(*) desc
```

Im Weiteren wurde über folgende SQL-Abfrage die term frequency ausgegeben.

```sql
select top 3 ID, noun, tf from MAX_FREQ_NOUN_T3N
```
Ergebnisse: 

| ID | noun  | tf         
| :-----------: |:-------------:|:-------------:|
| 672883b7-cc05-47a1-99d4-1fbcb5fb2431      |      VR             |     59     |
| 3b1f130f-bed6-4e10-8a13-a2ae2a1381bd      |      Kurs           |     46     |
| 4cd65e7e-f99f-4d65-aa9d-681c649a2983      |      Instagram      |     44     |

#### inverse document frequency (idf):
Die inverse document frequency wurde mithilfe von drei Views realisiert. Im Folgenden sind die SQL-Befehle zusehen. 

```sql
create view COUNT_DOCS_T3N as select count(DISTINCT id) as n_total from "$TA_T3NTEXTIND"
```
```sql
create view VALUES_DF_T3N as select TA_TOKEN as noun, count(DISTINCT ID) as DF from "$TA_T3NTEXTIND" where TA_TYPE=\'noun\' group by TA_TOKEN
```
```sql
create view VALUES_IDF_T3N as select t1.noun, ln((t2.n_total/t1.DF)) as idf from VALUES_DF_T3N as t1, COUNT_DOCS_T3N as t2 order by idf desc
```

Das folgende SQL-Statement liefert schließlich die Ausgabe zu der inverse document frequency.

```sql
select top 3 * from VALUES_IDF_T3N
```
Ergebnisse:

| Nomen  | idf        
| :-----------: |:-------------:|
| 080p  | 6.901737 |
| 08    | 6.901737 |
| 000er | 6.901737 |

Die top-3 tf-idf (ntn nach der SMART Notation) Werte von Nomen im Corpus sind in folgender Tabelle zu sehen:

| ID | noun  | tf   |   idf   |   tfidf |
| :-----------: |:-------------:|:-------------:|:-------------:|:-------------:|
|    b142c820-1887-42ae-b3f6-3dba1fbbcbfb       |      Ello       |       32      |   6.208590    |      198.674881     |
|      f817b5e8-8ca0-4a53-b0fd-21fac768c3e0     |       Chronik      |      38       |   5.109978    |    194.179154       |
|      672883b7-cc05-47a1-99d4-1fbcb5fb2431     |        VR     |      59       |    3.164068   |     186.679986       |


### 1.7.4
Im Folgenden ist die SQL-Abfrage zu sehen, welche für den Chi2 Test benötigt wird.
```sql
select adjective, noun, o11, o12, o21, o22 from 
(
select t1.adjective, t1.noun, w1_and_w2 as o11, (sum_w1_and_w2-SUM(w1_and_w2)) as o12, t3.sum_w1_and_not_w2 as o21, (sum_NOT_w2 - t3.sum_w1_and_not_w2) as o22 from 
"SYSTEM"."ADJECTIVE_NOUN_BIGRAM_T3N" as t1, 
(select SUM(w1_and_w2) as sum_w1_and_w2 from "SYSTEM"."ADJECTIVE_NOUN_BIGRAM_T3N") as t2,
(select adjective, SUM(w1_and_not_w2) as sum_w1_and_not_w2 from "SYSTEM"."ADJECTIVE_NOUN_BIGRAM_NOT_TEXT" group by adjective) as t3,
(select SUM(w1_and_not_w2) as sum_NOT_w2 from "SYSTEM"."ADJECTIVE_NOUN_BIGRAM_NOT_TEXT" order by sum_NOT_w2 desc) as t4 where t3.adjective=t1.adjective group by t1.adjective, t1.noun, w1_and_w2, t2.sum_w1_and_w2, t3.sum_w1_and_not_w2, t4.sum_NOT_w2
)
```
Der Chi2 Test liefert folgendes Ergebnis:   
Die drei statistisch signifikantesten zusammenhängenden Bigramme mit w1=* (beliebig) und w2=Text:    

| Adjektiv | Nomen | Chi2         
| :------: | :------: | :------: |
| prägnanten | Text | 1087.674939 |
| eingegebenen | Text | 1087.674939 |
| markierten | Text | 722.244913 |

Die drei am wenigsten statistisch signifikant zusammenhängenden Bigramme mit w1=* (beliebig) und w2=Text:  

| Adjektiv | Nomen | Chi2         
| :------: | :------: | :------: |
| richtigen | Text | 46.493854 |
| Smart | Text | 43.900362 |
| folgenden | Text | 38.388556 |

### 1.7.5 a
Für die Berechnung des Skalarprodukt wurde eine neue View zur Hilfe erzeugt. Diese View wurde mit folgendem SQL-Befehl erstellt: 
```sql
create view TERMS_T3N as SELECT ID, TA_TOKEN AS WORD, count(*) AS TERM, POWER(count(*),2) AS TERMSQR FROM "SYSTEM"."$TA_T3NTEXTIND" WHERE TA_TYPE=\'noun\' GROUP BY ID, TA_TOKEN
```

Das Skalarprodukt wird berechnet, indem die Terme (Nomen) herausgefiltert werden, die in beiden Dokumenten vorkommen. Anschließend werden die Häufigkeiten der Nomen multipliziert und aufsummiert. Die folgende Python-Funktion wurde implementiert, um das Ähnlichkeitsmaß (Skalarprodukt) für einen gegebenen Anfragevektor auszugeben. 
```python
def scalar_product(id):
    sql = 'SELECT ID, sum(PROD) AS SCALARPRODUCT FROM (SELECT a.ID, a.WORD, a.TERM * b.CountReq AS PROD FROM TERMS_T3N AS a, (SELECT TA_TOKEN, count(*) AS CountReq FROM "SYSTEM"."$TA_T3NTEXTIND" WHERE ID = \''+id+'\' GROUP BY TA_TOKEN) AS b WHERE a.WORD = b.TA_TOKEN) GROUP BY ID ORDER BY SCALARPRODUCT desc LIMIT 10;'
    cursor.execute(sql)
    idf = cursor.fetchall()
    idf_df = pd.DataFrame(idf)
    print(idf_df)
```

### 1.7.5 b
Für die Durchführung der Kosinus Ähnlichkeit wurde eine neue View zur Hilfe erzeugt. Außerdem wurde die Cosinus Ähnlichkeit mithilfe des Skalarprodukts berechnet. Schließlich wurde eine Python-Funktion implementiert, welche die Cosinus Ähnlichkeit bzgl. eines Anfragevektors ausgibt. 
```python
def cosinus(id):
    # create view COS_T3N
    sql = 'create view COS_T3N as SELECT x.ID AS ID, x.SCALARPRODUCT AS SCALARPRODUCT, y.Cos AS Cos From (SELECT ID, sum(PROD) AS SCALARPRODUCT FROM (SELECT a.ID, a.WORD, a.TERM * b.CountReq AS PROD FROM TERMS_T3N AS a, (SELECT TA_TOKEN, count(*) AS CountReq FROM "SYSTEM"."$TA_T3NTEXTIND" WHERE ID = \''+id+'\' GROUP BY TA_TOKEN) AS b WHERE a.WORD = b.TA_TOKEN) GROUP BY ID) AS x, (SELECT ID, SQRT(SUM(TERMSQR)) AS Cos FROM TERMS_T3N GROUP BY ID) AS y WHERE x.ID = y.ID'
    cursor.execute(sql)
    
    sql = 'SELECT ID, SCALARPRODUCT / (Cos * (SELECT SQRT(sum(coutsqr)) FROM (SELECT TA_TOKEN, POWER(count(*),2) AS coutsqr FROM "SYSTEM"."$TA_T3NTEXTIND" WHERE ID = \''+id+'\' AND TA_TYPE = \'noun\' GROUP BY TA_TOKEN))) AS COSINUS FROM COS_T3N ORDER BY COSINUS DESC LIMIT 10'
    cursor.execute(sql)
    idf = cursor.fetchall()
    idf_df = pd.DataFrame(idf)
    
    # drop SQL-View
    sql_drop_view = 'drop view COS_T3N'
    cursor.execute(sql_drop_view)
    
    print(idf_df)
```

### 1.7.6
Die jeweils ähnlichsten Dokumente zu dem Dokument mit der ID 54ff8c69-007f-49a8-94cf-093fb5b0951b wurden mithilfe der beiden Funktionen aus 1.5 ermittelt. Ein Vergleich der beiden Ähnlichkeitsmaße Skalarprodukt und Cosinus Ähnlichkeit zeigt, dass man mithilfe der Cosinus Ähnlichkeit Duplikate besser erkennen kann. Für die ID 54ff8c69-007f-49a8-94cf-093fb5b0951b liegt kein eindeutiges Duplikat vor. Es wird nur das Dokument (54ff8c69-007f-49a8-94cf-093fb5b0951b) selbst als Duplikat erkannt.   

#### Ähnliche Dokumente für die ID 54ff8c69-007f-49a8-94cf-093fb5b0951b
#### Top 3 Skalarprodukt
| ID  | Value         
| :-----------: |:-------------:|
| 54ff8c69-007f-49a8-94cf-093fb5b0951b       |      91       |
|  53046188-b726-4c86-828a-617cc0a14894       |      73       |
|  29983671-fcf8-4c0d-a447-dc5a57384f02       |      70       |

#### Top 3 Cosinus Ähnlichkeit
| ID  | Value         
| :-----------: |:-------------:|
|    54ff8c69-007f-49a8-94cf-093fb5b0951b    |      1       |
|    53046188-b726-4c86-828a-617cc0a14894    |      0.3009       |
|    29983671-fcf8-4c0d-a447-dc5a57384f02   |    0.2687    |


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

Das wortbasierte und das zeichenbasierte Shingling wurden mit unterschiedlichen Freiheitsgraden getestet. Die Tests wurden mit den Random-Seed Werten 42, 127 und 1700 durchgeführt und sind in folgender Tabelle aufgelistet. 

Precision-Recall Werte für die jeweiligen Random-Seeds:

| Shingles  | Wortbasiert/ Zeichenbasiert  | numHashes  | 42  | 127  | 1700  |
|---|---|---|---|---|---|
|3|Wortbasiert|2|0.67|0.71|1.00|
|3|Wortbasiert|4|1.00|1.00|0.98|
|6|Wortbasiert|2|0.83|0.52|0.91|
|6|Wortbasiert|4|0.95|1.00|0.96|
|6|Zeichenbasiert|2|0.05|0.00|0.14|
|6|Zeichenbasiert|4|1.00|1.00|0.43|
|12|Zeichenbasiert|2|0.83|0.71|0.83|
|12|Zeichenbasiert|4|0.99|1.00|1.00|

Zunächst fällt auf, dass beim zeichenbasierten Shingling die Anzahl der Zeichen pro Shingling eine größere Rolle spielen als beim wortbasierten Shingling. Es wurden daher sechs und zwölf Zeichen pro Shingling gewählt. Die Anzahl der Zeichen pro Shingling beim wortbasierten Shingling wurde auf drei und sechs gesetzt, da bei dieser Anzahl bereits gute Werte für den Precision-Recall erreicht werden konnten. Außerdem ist bei beiden Verfahren anzumerken, dass bei einer Verwendung von vier Hashfunktionen der Precision-Recall deutlich besser war, als bei zwei Hashfunktionen. Im Weiteren erkennt man, dass der Precision-Recall bei zwei Hashfunktionen durch die Erhöhung der Zeichenanzahl pro Shingling deutlich ansteigt, dies ist sowohl beim wortbasierten, als auch bei zeichenbasierten Shingling zu erkennen. 
