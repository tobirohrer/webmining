# Praktikum 1: Janik Tinz, Patrick Tinz, Tobias Rohrer (Gruppe X-D)

## Allgemein
* Link zum GitHub Repo: https://github.com/tobirohrer/webmining 
## Vorbereitung 
### heise Webseite:
* Format von seiteninternen URL:
https://www.heise.de/newsticker/meldung/<titel_des_artikels>.html

* DOM-Baum relevante Informationen:

* Beispiel (HTML-Auszug):
URL: https://www.heise.de/newsticker/meldung/Wie-Geheimdienste-Cyberattacken-durchfuehren-4582214.html (Zugegriffen am 11.11.2019)


### t3n:
* Format von seiteninternen URL:
https://t3n.de/news/<titel_des_artikels>

* DOM-Baum relevante Informationen:
    * Datum und Uhrzeit des Artikels: class=“u-color-mute”  
    * Teaser-Text: class=“u-text-teaser”

* Beispiel (HTML-Auszug):
URL: https://t3n.de/news/starlink-spacex-60-satelliten-1219838/ (Zugegriffen am 11.11.2019)

## Teil 1
Diese Aufgabe wurde im Juypter Notebook “p1_regulaere_ausdrucke” bearbeitet. 

## Teil 2
1. Klinik.xml:
    * a.) ```//Personal/*/Pfleger[@Station=“Rehabilitation”]/child::Name```
    * b.) ```//Stationen/Station[contains(Standort,"Seestrasse") and count(Bett)>2]```
    * c.) ```//Pfleger[@ID=/Klinik/Stationen/Station/@Leitung]/Name/Nachname```
    * d.) ```//Personal/angestelltes_Personal/*/Adresse[Stadt='Berlin']/preceding-sibling::Name```
2. Hamlet.xml:
    * a.) ```//SCENE[count(SPEECH) < 10]/TITLE```
    * b.) ```//ACT/SCENE/SPEECH/LINE/text()[contains(.,"Part them; they are incensed.")]/../../preceding-sibling::STAGEDIR[position() = count(//ACT/SCENE/SPEECH/LINE/text()[contains(.,"Part them; they are incensed.")])]```
    * c.) ```//ACT//SPEECH[position() = 2]/SPEAKER/text()```   
        * Dieser Ausdruck wählt das zweite SPEECH Elemente des Elternknotens aus.
    ```//ACT//SPEECH[position() = 187]/SPEAKER/text()```
        * Dieser Ausdruck wählt das 187. SPEECH Element des Elternknotens aus (In der Hamlet.xml Datei liefert dieser Befehl keine Ausgabe.).
    ```//ACT/descendant::SPEECH[position() = 2]/SPEAKER/text()```  
        * Dieser Ausdruck wählt das zweite SPEECH Element vom ACT Element aus.
    ```//ACT/descendant::SPEECH[position() = 187]/SPEAKER/text()```
        * Dieser Ausdruck wählt das 187. SPEECH Element vom ACT Element aus.

3. XPath Ausdrücke für unser Text-Mining Projekt:   
    * Hier kommen unsere Ausdrücke hin.

## Teil 3

