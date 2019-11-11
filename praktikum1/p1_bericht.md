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
    * a.) //Personal/*/Pfleger[@Station=“Rehabilitation”]/child::Name
    * b.) //Stationen/Station[contains(Standort,"Seestrasse") and count(Bett)>2]
    * c.) //Pfleger[@ID=/Klinik/Stationen/Station/@Leitung]/Name/Nachname
    * d.) //Personal/angestelltes_Personal/*/Adresse[Stadt='Berlin']/preceding-sibling::Name
2. Hamlet.xml:
    * a.) //SCENE[count(SPEECH) < 10]/TITLE
    * b.)
    * c.)
3. XPath Ausdrücke für unser Text-Mining Projekt:   
    * Hier kommen unsere Ausdrücke hin.

## Teil 3

