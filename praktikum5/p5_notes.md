# Praktikum 5: Janik Tinz, Patrick Tinz, Tobias Rohrer (Gruppe X-D)

## Allgemein
* Link zum GitHub Repo: [https://github.com/tobirohrer/webmining](https://github.com/tobirohrer/webmining)

## Vorbereitung
Bei Reviews achtet man vor allem auf positive und negative Adjektive bzw. Adverben.

## Textklassifikation und Deep Learning
Die Aufgaben wurden im Jupyter-Notebook [Praktikum5](https://github.com/tobirohrer/webmining/blob/master/praktikum5/Praktikum5.ipynb) bearbeitet. Außerdem wurden die Aufgaben auf [Google Colab](https://colab.research.google.com/notebooks/welcome.ipynb) ausgeführt. 

### 1. Aufgabe
Machen Sie Sie sich mit dem konkreten Keras-IMDB Datensatz vertraut. Schauen Sie sich z.b. einige Review-Texte und deren Labels an. Stimmen Sie als Leser mit den Labels überein? Warum bzw. warum nicht?

#### Antwort:
Die Betrachtung der ersten zehn Review-Texte hat gezeigt, dass die Labels sehr gut für die einzelnen Reviews gewählt wurden.

### 2. Aufgabe
Identifizieren Sie die relevantesten Features (Wörter) anhand des Chi^2-Wertes auf den Trainingsdaten. Nutzen Sie dazu aus sklearn: CountVectorizer und chi2, sowie aus numpy argsort.

#### Antwort:
Die relevantesten Features (Wörter) anhand des Chi^2-Wertes sind:   
* bad
* worst
* great
* awful 
* waste 
* terrible
* movie
* excellent 
* stupid
* worse

### 3. Aufgabe
Prüfen und begründen Sie, ob „accuracy“ ein sinnvolles Gütemaß für einen Klassifikator auf diesem Datensatz ist.

#### Antwort:
Plot:   
<img src="./plots/accuracy.png" alt="Tab Cross Table nhtsa" width="400"/> 

Formel:   
<a target="_blank"><img src="https://latex.codecogs.com/png.latex?\dpi{107}&space;Accuracy&space;=&space;\frac{TP&space;&plus;&space;TN}{TP&plus;FP&plus;FN&plus;TN}" title="Accuracy = \frac{TP + TN}{TP+FP+FN+TN}" /></a>   

Der Plot zeigt, dass die beiden Klassen (0 und 1) die gleiche Anzahl von Review-Texten enthalten. Die Fehlermetrik Accuracy kann vor allem auf balancierten Datensätzen aussagekräftig eingesetzt werden, dies trifft bei diesem Datensatz zu.

### 4. Aufgabe
Wie interpretieren Sie die Performance-Kurven und Ergebnisse auf den Testdaten zum RNN bzw. was fällt Ihnen auf?

#### Antwort:
Es ist zu erkennen, dass das RNN auf den Trainingsdaten eine deutlich bessere Performance hat als auf den Validierungsdaten. Dieses Ergebnis zeigt, dass bei diesem RNN ein Overfitting vorliegt. Das Overfitting steigt mit steigender Epochengröße an. Die Verteilung der Trainings- und der Validierungsdaten scheint sich zu unterscheiden.

### 5. Aufgabe
Schauen Sie sich einige der "drastischsten" FPs und FNs an (hoher Score und Label=1 oder niedriger Score und Label=0). Können Sie erahnen, was das Modell ggf. verwirrt hat?

#### Antwort:

### 6. Aufgabe
Optional (nur wenn Sie gut in der Zeit liegen und fit in der Materie sind!): Wie interpretieren Sie die Performance-Kurven und Ergebnisse auf den Testdaten zum RNN mit vorgelernten Glove-Embedding bzw. was fällt Ihnen auf?

#### Antwort:

### 7. Aufgabe
Wie interpretieren Sie die Performance-Kurven und Ergebnisse auf den Testdaten zum LSTM bzw. was fällt Ihnen auf?

#### Antwort:

### 8. Aufgabe
Wie interpretieren Sie die Ergebnisse der „einfacheren“ Klassifikationsmodelle auf den Testdaten bzw. was fällt Ihnen auf? Inwiefern deckt sich die Wichtigkeit der Features mit der, die Sie in Aufgabe (2) ermittelt haben?

#### Antwort:

