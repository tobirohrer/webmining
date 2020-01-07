# Praktikum 4: Janik Tinz, Patrick Tinz, Tobias Rohrer (Gruppe X-D)

## Allgemein
* Link zum GitHub Repo: [https://github.com/tobirohrer/webmining](https://github.com/tobirohrer/webmining)

## Vorbereitung
### Common Crawl Datensatz
Der Common Crawl Korpus enthält Petabytes von Daten, welche in den letzten 7 Jahren gesammelt wurden. Es enthält rohe Webseitendaten, extrahierte Metadaten und Textextraktionen. Der Common Crawl Datensatz ist in Amazon S3 gespeichert und ist Teil des Amazon Public Datasets Programs. Die öffentlichen Datensätze können kostenlos heruntergeladen werden.    

Spaltennamen des untersuchten Datensatzes:    
'index', 'Target-URI', 'Date', 'IP-Address', 'Identified-Payload-Type', 'Payload', 'MetaData', 'Plaintext', 'Guessed-Language'

[Common Crawl Datensatz](https://github.com/tobirohrer/webmining)

### Python-Bibliothek Gensim
Gemsim ist eine Open-Source Library für unsupervised topic modeling und natural language processing, wobei aktuelle statistische ML-Algorithmen verwendet werden. 

[gensim](https://radimrehurek.com/gensim/auto_examples/index.html)

## Teil 1: Topic Modell Parameter und Interpretation (CommonCrawl)

### 1.1    
Schauen Sie sich die Topic-Wortverteilungen des erstellten Modells an (in Textform, der interaktiven Ausgabe, oder als Wordcloud). Für welche Topics können Sie intuitiv Überbegriffe bilden? Notieren Sie sich diese bzw. legen Sie eine entsprechende „lookup-tabelle“ als Datenstruktur an. Welche Topics erscheinen sinnvoll, welche nicht?

Das folgende Listing zeigt unsere Lookup-Tabelle:
```python
topics = {
    0: 'Research', 
    1: 'Misc',
    2: 'Month',
    3: 'Life',
    4: 'Education', 
    5: 'Medicine',
    6: 'Architect', 
    7: 'Adult', 
    8: 'Country', 
    9: 'Education', 
    10: 'Month', 
    11: 'Technology',
    12: 'Misc',
    13: 'Government',
    14: 'Temperature'
}
```
Die Topics 1 und 12 konnten wir nicht eindeutig zuordnen. Aus diesem Grund wurden die Topics als Misc bezeichnet. 

### 1.2 
Notieren Sie sich, welches Topic in Codeblock 11 als „adult content“ identifiziert wurde. Filtern Sie für die weiteren Aufgaben die entsprechenden Records aus dem „result“ DataFrame aus, also z.B. alle Dokumente mit einer entsprechenden Topicwahrscheinlichkeit > 50%. Öffnen Sie nicht die Links zu den entsprechenden Dokumenten im Browser. Aktivieren Sie sicherheitshalber den installierten Browser-Filter.



### 1.3 
Schauen Sie sich nun für einige andere Topics stichprobenartig Dokumente an. Passen diese zu den vorher von Ihnen vergebenen Topic-Überbegriffen? Warum bzw. warum nicht?



### 1.4
Formulieren Sie Anfragen zu bestimmten Topic-Mischungen (z.B. Topic A > 40% und Topic B > 40%). Passen die gematchten Dokumente zu Ihren Erwartungen? Warum bzw. warum nicht?



### 1.5 
Berechnen Sie zwei neue Modelle (auf dem Original-Corpus mit Adult-Content) mit verändertem Glättungsparameter für die Dokument-Topic Zuordnungen. Die restlichen Parameter sollen beibehalten werden. Berechnen Sie ein Modell mit Glättungsparameter=1 und ein Modell mit Glättungsparameter=10^-18. Wie sollte sich das Modell Ihrer Erwartung nach verändern? Schauen Sie sich wieder jeweils die ersten 20 Zeilen der Dokument-Topic Wahrscheinlichkeitsmatrizen an. Plotten Sie weiterhin die Häufigkeitsverteilungen der „Nicht-NaN-Topics“ pro Dokument. Was fällt Ihnen auf? Entspricht dies Ihren Erwartungen?



## Teil 2: Topic Modell Vergleich mit Referenz-Clustering (NHTSA)

### 2.1    
Machen Sie sich, ähnlich wie in Teil I, mit dem erstellten Topicmodell für den NHTSA-Teildatensatz vertraut, indem Sie einzelne Topics bzw. Dokumente genauer unter die Lupe nehmen. Dokumentieren Sie Ihre Erkenntnisse, d.h. in welchen Fällen Sie das Modell für sinnvoll halten und in welchen nicht.



### 2.2 
Überführen Sie das Soft-Clustering in ein Hard-Clustering, indem Sie einen Vektor erstellen, der pro Dokument das Topic mit der höchsten Wahrscheinlichkeit enthält. Die NHTSA-Kategorien (COMPDESCR) finden Sie bereits im Vektor docCats. Berechnen Sie auf dieser Basis die RANDMetrik zum Vergleich von Clusterings und interpretieren Sie diese soweit möglich.



### 2.3 
Erstellen Sie eine Kreuztabellle, bei der eine Dimension die Topics und eine Dimension die Kategorien (COMPDESC) darstellen. In den Zellen soll gezählt werden, wie häufig im Corpus das Top-Topic eines Dokuments mit der tatsächlichen Kategorie korrespondiert. Nutzen Sie zur Visualisierung z.B. „clustermap“ aus der Python Bibliothek seaborn. Wie interpretieren Sie die Ergebnisse? Schauen Sie sich einzelne Dokumente als Repräsentanten/Beispiele interessanter Konstellationen in der Kreuztabelle an.



## Teil 3: Topic Modell auf eigenen gecrawlten Texten
 
