# Praktikum 1: Janik Tinz, Patrick Tinz, Tobias Rohrer (Gruppe X-D)

## Allgemein
* Link zum GitHub Repo: [https://github.com/tobirohrer/webmining](https://github.com/tobirohrer/webmining)

## Vorbereitung 

In der ersten Phase hat sich herausgestellt, dass die Website von [t3n.de](t3n.de) ausreichend Inhalte sowie Links zum Crawlen beinhaltet. Deshalb haben wir uns im ersten Praktikum ausschließlich auf [t3n.de](t3n.de) fokussiert.


* Format von seiteninternen URLs:
https://t3n.de/news/<titel_des_artikels>

* Relevante Informationen des DOM-Baums:
    * Kategorie: ```class="o-list c-breadcrumb"```, ```class="u-text-extrasmall u-color-mute u-link-simple"```
    * Überschrift: ```class="u-gap-medium u-text-extralarge"```
    * Teaser-Text: ```class=“u-text-teaser”```
    * Text-Inhalt: ```class="c-entry"```

* Beispiel (HTML-Auszug):
URL: https://t3n.de/news/starlink-spacex-60-satelliten-1219838/ (Zugegriffen am 11.11.2019)

## Teil 1
Diese Aufgabe wurde im Juypter Notebook [p1\_regulaere\_ausdrucke](https://github.com/tobirohrer/webmining/blob/master/praktikum1/p1_regulaere_ausdrucke.ipynb) bearbeitet. 

Anmerkung zu Übung 3: Hier haben wir `-.2` zusätzlich in unserer Ergebnismenge aufgenommen.
Anmerkung zu Übung 5: Hier haben wir zwei Reguläre Ausdrücke gefunden. Der erste RegEx extrahiert nur neunstellige Postleitzahlen. Der zweite RegEx extrahiert  fünf- oder neunstellige Postleitzahlen.

## Teil 2
1. Klinik.xml:
    * a.) ```//Personal/*/Pfleger[@Station=“Rehabilitation”]/child::Name```
    * b.) ```//Stationen/Station[contains(Standort,"Seestrasse") and count(Bett)>2]```
    * c.) ```//Pfleger[@ID=/Klinik/Stationen/Station/@Leitung]/Name/Nachname```
    * d.) ```//Personal/angestelltes_Personal/*/Adresse[Stadt='Berlin']/preceding-sibling::Name```
2. Hamlet.xml:
    * a.) ```//SCENE[count(SPEECH) < 10]/TITLE```
    * b.) ```//ACT/SCENE/SPEECH/LINE/text()[contains(.,"Part them; they are incensed.")]/../../preceding-sibling::STAGEDIR[position() = count(//ACT/SCENE/SPEECH/LINE/text()[contains(.,"Part them; they are incensed.")])]```
    * c.) 
        * ```//ACT//SPEECH[position() = 2]/SPEAKER/text()```   
        Dieser Ausdruck wählt das zweite SPEECH Elemente des Elternknotens aus.
        * ```//ACT//SPEECH[position() = 187]/SPEAKER/text()```
        Dieser Ausdruck wählt das 187. SPEECH Element des Elternknotens aus (In der Hamlet.xml Datei liefert dieser Befehl keine Ausgabe.).   
        * ```//ACT/descendant::SPEECH[position() = 2]/SPEAKER/text()```  
        Dieser Ausdruck wählt das zweite SPEECH Element vom ACT Element aus.
        * ```//ACT/descendant::SPEECH[position() = 187]/SPEAKER/text()```
        Dieser Ausdruck wählt das 187. SPEECH Element vom ACT Element aus.

3. XPath-Ausdrücke für unser Text-Mining Projekt: 
    * ```//h2[@class='u-gap-medium u-text-extralarge']/text()```
    * ```//p[@class='u-text-teaser']/text()```
    * ```//p[@class='u-text-teaser']/following-sibling::p/text()```
    * ```//ul[@class='o-list c-breadcrumb']/li[position() = 2]/a[@class='u-text-extrasmall u-color-mute u-link-simple']/text()```

## Teil 3

### 3.1 Implementierung Scrapy Crawler

Wir haben uns bei der Implementierung unserer Crawler für Link- und Content-Extraction zunächst auf die URL [https://t3n.de/news]() konzentriert. Dafür wurden die zwei Klassen `T3nUrlSpider` und `T3nDataSpider` implementiert.

#### T3nUrlSpider
Der T3nUrlSpider wurde so konfiguriert, dass er sich ausschließlich auf [t3n.de](t3n.de) bewegt, jedoch ausgehende URLs zu jeder beliebigen Seite extrahiert.

```
class T3nUrlSpider(scrapy.Spider):
    name = 't3n_url_spider'
    allowed_domains = ['t3n.de']
    start_urls = ['https://t3n.de/news']

    def parse(self, response):
        extractor = LinkExtractor()
        links = extractor.extract_links(response)

        for link in links:
            absolute_next_page_url = response.urljoin(link.url)
            yield {'from': response.url, 
                   'url': link.url, 
                   'text': link.text.strip()}
            yield scrapy.Request(absolute_next_page_url)
```

#### T3nDataSpider
Der T3nDataSpider extrahiert ausschließlich URLs, die auf die `/news` Subdomain zielen. Somit wird gesteuert, wie sich der T3nDataSpider "fortbewegt". Die XPath-Ausdrücke für die zu extrahierenden Informationen sind in Teil 2.3 definiert.

```
class T3nDataSpider(scrapy.Spider):
    name = 't3n_data_spider'
    allowed_domains = ['t3n.de']
    start_urls = ['https://t3n.de/news']

    def parse(self, response):

        ... # xpath expressions see Teil 2.3
        
                yield {'category': category, 
               'heading': heading, 
               'teaser': teaser, 
               'text': text, 
               'url': response.url}

        extractor = LinkExtractor(allow='news', allow_domains=self.allowed_domains)
        links = extractor.extract_links(response)

        for link in links:
            absolute_next_page_url = response.urljoin(link.url)
            yield scrapy.Request(absolute_next_page_url)
```

Die Abbruchbedingung unserer Spider wurde zunächst auf einen Pagecount von jeweils 500 Seiten definiert. Hierfür musste im CrawlerProess die folgende Eigenschaft gesetzt werden:

```
    c = CrawlerProcess({
        'CLOSESPIDER_PAGECOUNT': 500,
        ...
    })
```

### 3.2 Link Analyse DarmstadtSpider
Die Link Analyse wurde in dem Jupyter Notebook [link\_analysis\_DarmstadtSpider](https://github.com/tobirohrer/webmining/blob/master/praktikum1/link_analyses_DarmstadtSpider.ipynb) realisiert.

#### Data Preprocessing

Um mit den Auswertungen starten zu können, mussten zunächst die Daten bereinigt werden. Viele URLs wurden mehrfach mit unterschiedlichen URL-Parametern für die Darstellung verlinkt. Für unsere Auswertung mussten diese aus dem Datensatz entfernt werden. Mit einer Einfachen Abfrage konnte dies realisiert werden.

```
df = df.loc[~df['from'].str.contains('(\?|\&)(tx_contrast|type=97)')]
```

#### Top-Level Domain Statisitk
Zunächst wurde den Daten eine Spalte `tld` mit der Zugehörigen Top-Level Domain eingefügt.

```
df['tld'] = df.url.map(lambda url:  get_tld(url, fail_silently=True))
```

Nachdem die Informationen in der Spalte `tld` vorhanden waren, konnte ein `Countplot` über die Verteilung erstellt werden.

![alt text](./plots/tld_darmstadt_spider.png)

#### Outgoing / Incoming URL Statistik

Die Statistik über die Anzahl an ausgehenden Links pro Seite sieht für den DarmstadtSpider wie folgt aus.
Es ist zu erkennen, dass die meisten Seiten in Etwa 15 ausgehende Links beinhalten. Die wenigsten Seiten beinhalten mehr als 20 ausgehende Links.

![alt text](./plots/outgoing_links_darmstadt_spider.png)

Auf dem Plot für die eingehenden Links pro Seite ist zu erkennen, dass es wenige Seiten mit 21 eingehenden Links, jedoch sehr viele Seiten mit nur einem eingehenden Link gibt. Seiten mit 21 eingehenden Links sind auf jeder Unterseite verlinkt. Zum Beispiel in dem "Oft gesucht" Menü der Navigationsleiste.

![alt text](./plots/incoming_links_darmstadt_spider.png)



### 3.3 Link Analyse t3n
Die Link Analyse wurde in dem Jupyter Notebook  und [link\_analysis\_t3n](https://github.com/tobirohrer/webmining/blob/master/praktikum1/link_analysis_t3n.ipynb) realisiert.

#### Statistiken aus 3.2 für t3n
Auf den nachfolgenden Plots ist zu erkennen, dass die Seiten auf [t3n/news](t3n.de/news) generell mehr eingehende sowie ausgehende Links, als   die Seiten auf [https://www.darmstadt.de/leben-in-darmstadt](https://www.darmstadt.de/leben-in-darmstadt) enthalten.

![alt text](./plots/tld_t3n.png)
![alt text](./plots/outgoing_links_t3n.png)
![alt text](./plots/incoming_links_t3n.png)

#### Zusätzliche Statistiken
Zunächst sollte geklärt werden, wie viele URLs von T3n auf externe Seiten zeigen. Der nachfolgende Plot zeigt das Verhältnis von t3n zu externen URLs. Diese Statistik war die Grundlage für die Erkenntnis, dass t3n neben Content auch ausreichend Links zum Crawlen enthält.

![alt text](./plots/distribution_internal_external_links_t3n.png)

Außerdem wurde der Datensatz in einer Graph-Datenstruktur abgespeichert. Das ermöglicht uns in Zukunft auf einfache Weise Graph-Algorithmen sowie Netwerk-Plots zu realisieren. Hierfür wurden zunächst alle URLs auf ihre Domain getrimmt. 

```
graph = pd.DataFrame()
graph['to'] = t3n.url.map(lambda url:  tldextract.extract(url).domain)
graph['from'] = t3n['from'].map(lambda url:  tldextract.extract(url).domain)
```

Die Summe aller gleichen Verlinkungen nach dem trimmen, wurde als Gewichtung einer Kante im Graph abgespeichert.

``` 
graph = graph.groupby(['to', 'from']).size().reset_index(name='weight')
```

Zu guter Letzt wird der DataFrame dann noch in eine Graph-Datenstruktur überführt. In unserem Beispiel unten überführen wir nur alle Verlinkungen, die mehr als 10 mal auftreten. Zur Unterstützung haben wir die Python Bibliothek `networkx` verwendet.

```
import networkx as nx
...
G = nx.DiGraph()
for index, row in graph.iterrows():
    if(row['weight'] > 10): #Optional
        G.add_edge(row['from'], row['to'], weight=row['weight'])
```


Nachstehend ist ein beispielhafter Plot des Graphen zu sehen. Es werden Seiten, die öfter als 10 mal von T3n verlinkt werden gezeit.

![alt text](./plots/graph_t3n.png)






