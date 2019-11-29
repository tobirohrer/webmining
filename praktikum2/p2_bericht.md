# Praktikum 2: Janik Tinz, Patrick Tinz, Tobias Rohrer (Gruppe X-D)

## Allgemein
* Link zum GitHub Repo: [https://github.com/tobirohrer/webmining](https://github.com/tobirohrer/webmining)

## Vorbereitung 
Bei der Umsetzung der Aufgabenstellung wurde das Datenbank Tool [DBeaver](https://dbeaver.io/) verwendet, da das HANA Eclipse Plugin Verbindungsprobleme verursachte. 

### Verbinden mit HANA VM
#### SQL Statement   
```select top 10 * from SYSTEM.CMPL100K``` (Ausgabe der ersten zehn Zeilen der Tabelle CMPL100K)
#### Verbindung mit Python
Die Durchführung des Beispielskripts befindet sich im Juypter Notebook p2_preparation. 

### Python Extraktionsskript
Das Extraktionsskript befindet sich im Jupyter Notebook [praktikum2](https://github.com/tobirohrer/webmining/blob/master/praktikum2/praktikum2.ipynb). 

### Hintergrund der „NHTSA Complaints Datenbank“ 
Die National Highway Traffic Safety Administration (NHTSA) ist eine zivile Bundesbehörde in den USA für Straßen- und Fahrzeugsicherheit. 

##### Aufbau der Datenstruktur (Interessante Spalten)
* CMPLID: NHTSA'S INTERNAL UNIQUE SEQUENCE NUMBER
* CDESCR: Beschreibung der Beschwerde
* MFR_NAME: Autohersteller

### Statistiken für unsere Webdaten
* Die Verteilung der Top 20 Wörter vor bzw. nach den Löschen der Stop Words 
* Die Verteilung der Top 20 Part of Speech Tags

## Teil 1: Informationsextraktion und Textzerlegung
### 1.1 - 1.4
Diese Aufgaben wurden im Jupyter Notebook [praktikum2](https://github.com/tobirohrer/webmining/blob/master/praktikum2/praktikum2.ipynb) bearbeitet.  

### 1.5/ 1.6 Linguistische Analyse
#### Erstellung von einem Text-Index 
* CONFIGURATION 'LINGANALYSIS_BASIC'   
```CREATE FULLTEXT INDEX "T3NTEXTIND" ON "SYSTEM"."T3N" ("TEXT") CONFIGURATION 'LINGANALYSIS_BASIC' ASYNC LANGUAGE DETECTION ('de', 'en') TEXT ANALYSIS ON```

* CONFIGURATION 'LINGANALYSIS_STEMS'   
```CREATE FULLTEXT INDEX "T3NTEXTIND" ON "SYSTEM"."T3N" ("TEXT") CONFIGURATION 'LINGANALYSIS_STEMS' ASYNC LANGUAGE DETECTION ('de', 'en') TEXT ANALYSIS ON```

* CONFIGURATION 'LINGANALYSIS_FULL'   
```CREATE FULLTEXT INDEX "T3NTEXTIND" ON "SYSTEM"."T3N" ("TEXT") CONFIGURATION 'LINGANALYSIS_FULL' ASYNC LANGUAGE DETECTION ('de', 'en') TEXT ANALYSIS ON```

#### Löschen von einem Text-Index   
```DROP FULLTEXT INDEX "T3NTEXTIND";```

Welche Informationen werden dort zur Verfügung gestellt und welchen in der Vorlesung besprochenen Konzepten entsprechen diese? 
* CONFIGURATION 'LINGANALYSIS_BASIC'
    * Tokenisierung
* CONFIGURATION 'LINGANALYSIS_STEMS'
    * Tokenisierung
    * Stemming
* CONFIGURATION 'LINGANALYSIS_FULL'
    * Tokenisierung
    * Normalisierung
    * Stemming
    * Part of Speech (POS)

* Tokenisierung: Hierbei werden die textuellen Zeichenketten in linguistische Einheiten zerlegt. Ein Token ist die kleinste segmentierte Einheit eines Textes.
    * TA_TOKEN: Die einzelnen Tokens werden aufgelistet.
* Normalisierung: Dieses Verfahren wird in mehreren Schritten durchgeführt. Im ersten Schritt werden diakritische Zeichen umgewandelt. Dann werden die Großbuchstaben in reine Kleinbuchstaben überführt. Abschließend werden die Punkte, Apostrophe etc. entfernt. 
    * TA_NORMALIZED -> TA_TOKEN: Jubiläen -> jubilaeen (Beispiel aus unseren Webdaten)
* Stemming: Hierbei werden die Wörter nach relativ groben Regelen verändert. Das Problem ist, dass es häufig zu fehlerhaften Veränderungen kommt, da Sprachen sehr komplexe Konstrukte haben.
    * TA_TOKEN -> TA_STEM: Änderungen -> Änderung, fürs -> für=das (Beispiele aus unseren Webdaten)
* Part of Speech (POS): Bei diesem Verfahren wird jedem Token in einem Satz die korrekte Wortart zugeordnet. 
    * TA_TOKEN -> TA_TYPE: möglicherweise -> adverb (Beispiel aus unseren Webdaten)

Wo gibt es ggf. Probleme mit der Datenqualität und wie könnten Sie diese beheben? 
* Probleme mit der Datenqualität: ...
* Lösungsanstätze: ...

## Teil 2: Reporting auf zerlegten Texten