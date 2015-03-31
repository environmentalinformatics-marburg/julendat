# Vorbemerkung #
Für die Vorprozessierung (ki\_process\_resort\_level0000.py) und die Visualisierung (ki\_process\_vis.py) muss der X-Server über SSH verbunden werden (ssh **-X** ...).

# Vorprozessierung der neuen Daten (incomplete) #

  * Kili: Incoming-Daten von xxx.83 auf xxx.182 kopieren (dazu in `/incoming/` -Ordner navigieren)
```
scp *.7z eikistations@xxx.182:/xxx/incoming/
```

  * Exploratorien: Incoming-Daten von xxx.83 auf xxx.182 kopieren (dazu in `/incoming/` -Ordner navigieren), jedoch für jedes Gebiet (AEG, AEW, HEG, ...) einzeln. Beispiel für AEG:
```
scp * eibestations@xxx.182:/media/memory01/ei_data_exploratories/incoming/AEG
```

  * Kili: Kopierte Datei auf xxx.83 in `/moved/` -Ordner verschieben
```
mv *.7z moved/
```

  * Exploratorien: Kopierte Dateien auf xxx.83 in `/moved/` -Ordner verschieben, ebenfalls für jedes Gebiet einzeln. Beispiel für AEG:
```
mv * ../../moved_to_processing/ALB/AEG
```

  * Die folgenden Prozesse werden auf dem xxx.182 ausgeführt!

  * Kili: Kopierte ZIP Dateien in `/backup/incoming_backup/` sichern
```
scp incoming/*.7z backup/incoming_backup/
```

  * Exploratorien: Kopie der kopierten Dateien im entsprechenden Unterordner in `/backup/incoming_ftp/csv/` sichern (dazu in `/incoming/AEG` -Ordner auf xxx.182 navigieren). Auch das für jedes Gebiet einzeln. Beispiel für AEG:
```
scp *.csv ../../backup/incoming_ftp/csv/AEG/
```

  * Kili: Alte Dateien in `/incoming/` löschen (`alte x.7z`, `metadata`, `data`, etc.)


  * Kili: Kopierte ZIP Datei in `/incoming/` entpacken **(Immer nur eine ZIP Datei prozessieren!)**
```
7z X <filename>
```

  * Kili: Vorprozessierung starten (Verzeichnis wechseln in `xxx/scripts/julendat/src/julendat/scripts/stations_ki/`)

  * Kili: Überprüfen ob tfi-Dateien in der zu prozessierenden x.7z enthalten sind. Handelt es sich ausschließlich tfi-Dateien wird nur das erste Script benötigt, sind zusätzlich reguläre Dateien enthalten muss auch das zweite Script ausgeführt werden. Sind ausschließlich reguläre Dateien enthalten wird nur das zweite Script benötigt.
```
python2.7 ki_process_uitfstation_level0000_resort.py
```
```
python2.7 ki_process_resort_level0000.py
```

  * Exploratorien: In `/scripts/julendat_AEG/src/julendat/scripts/stations_be` -Ordner auf xxx.182 navigieren und folgende Datei für jedes Gebiet einzeln im entsprechenden `/julendat_*/` -Ordner starten (Achtung: im Incoming-Ordner darf immer nur ein Ordner sein, das heißt wenn Level 0000 für AEG prozessiert werden soll, dann müssen alle Ordner außer AEG kurzzeitig z. B. eine Ordnerebene höher geschoben werden):
```
python2.7 be_process_mntstation_level0000.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0000.txt 2>&1 & 
```

# Prozessierung der neuen Daten #
### Teil 1 ###
**Quality control level 0000 to level 0050**

  * Kili

```
python ki_process_level0050.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0050.txt 2>&1 & 
```

  * Exploratorien (bei diesem Prozessierungslevel auftretende Fehlermeldung rühren wahrscheinlich daher, dass Level-0000-Dateien entweder nur eine Zeile enthalten oder aber der Header fehlt oder aber in der Datei derselbe Inhalt zweimal steht. Die fehlerhaften 0000-Dateien einfach korrigieren und Level 0050 erneut starten)

```
python be_process_mntstation_level0050.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0050.txt 2>&1 & 
```


**Qualitiy control. Process data from level 0050 to qualitiy controled level 0100**

  * Kili

```
python ki_process_level0100.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0100.txt 2>&1 & 
```

  * Exploratorien

```
python be_process_level0100.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0100.txt 2>&1 & 
```
mit Angabe des Jahres
```
python be_process_level0100.py -y 2013 > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0100.txt 2>&1 & 
```

**Process data from level 0100 to level 0110 zip files**

  * Kili

```
python ki_process_level0110.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0110.txt 2>&1 & 
```


**Aggregation 1h. Process data from level 0100 to aggregated level 0200.**

  * Kili

```
python ki_process_level0200.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0200.txt 2>&1 & 
```

  * Exploratorien

```
python be_process_level0200.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0200.txt 2>&1 & 
```
mit Angabe des Jahres
```
python be_process_level0200.py -y 2013 > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0200.txt 2>&1 & 
```

**Qualitiy control. Process data from level 0200 to qualitiy controled level 0250.**

  * Kili

```
python ki_process_level0250.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0250.txt 2>&1 & 
```

  * Exploratorien

```
python be_process_level0250.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0250.txt 2>&1 & 
```
mit Angabe des Jahres
```
python be_process_level0250.py -y 2013 > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0250.txt 2>&1 & 
```

**Kallibrierung 260 - nicht im BE** ;)

```
python ki_process_level0260.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0260.txt 2>&1 & 
```

**Concatens files of level 0290**

  * Kili

```
python ki_process_level0290.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0290.txt 2>&1 & 
```

**Exploratorien**

```
python be_process_level0290.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0290.txt 2>&1 & 
```
mit Angabe des Jahres
```
python be_process_level0290.py -y 2013 > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0290.txt 2>&1 & 
```

**Interpolation. Process data from level 0290 to gap-filled level 0300**

  * Kili

```
python ki_process_level0300.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0300.txt 2>&1 & 
```

  * Exploratorien

```
python be_process_level0300.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0300.txt 2>&1 & 
```
mit Angabe des Jahres
```
python be_process_level0300.py -y 2013 > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0300.txt 2>&1 & 
```

**Interpolation. Process data from level 0300 to second-times gap-filled level 0310**

  * Kili

```
python ki_process_level0310.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0310.txt 2>&1 & 
```

  * Exploratorien

```
python be_process_level0310.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0310.txt 2>&1 & 
```

**Further aggregation. Process data from level 0310 to aggregated level 0400**

  * Kili

```
python ki_process_level0400.py > ../../../../..
```

  * Exploratorien

```
python be_process_level0400.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0400.txt 2>&1 & 
```

**Aggregation. Process data from level 0310 to aggregated level 0405 and 420 (only for Exploratories)**

  * Kili

```
python ki_process_level0405.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0405.txt 2>&1 & 
```

  * Exploratorien

```
python be_process_level0405.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0405.txt 2>&1 & 
```

```
python be_process_level0420.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0420.txt 2>&1 & 
```

**Process data from level 0400 to ready-for-bexis-upload-zips**

```
python ki_process_level0410.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0410.txt 2>&1 & 
```

**Process data from level 0400 to ready-for-bexis-upload-zips
```
python ki_process_level0415.py > ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_0415.txt 2>&1 & 
```**

  * **immer neue log-Datei erstellen**
  * Prozessnummer: ps 00000
  * log-Datei öffnen während des Prozesses:
```
less ../../../../../log_<Prozessierungsdatum>_<Uhrzeit>_<level>.txt
```

  * Fehlersuche (mehrere Stichworte; error, Error etc.):
```
less ../../../../../log_....| grep error
```

  * Dateien in `processing/plots` packen und nach `backup/backup_processing` verschieben

```
7z a -mmt=on backup/processing_backup/ki_processing_plots_<Prozessierungsdatum>.7z processing/plots/ > scripts/log_<Prozessierungsdatum>_<Uhrzeit>_zipProcessingPlots.txt 2>&1 &
```


**Prozessierung von mehreren ZIP-Dateien möglich**


# Visualisierung erstellen #

  * Kili: Visualisiere Level 0310 für 2012 (wird in plots/ki erstellt)

```
python ki_process_vis.py -p 310 -y 2012 > ../../../../../log_vis_<Prozessierungsdatum>_<Uhrzeit>_0310.txt 2>&1 &
```

  * Exploratorien: Level 290 und 300/310 müssen visualisiert werden

```
python be_process_vis.py -p 310 -y 2013 > ../../../../../log_vis_<Prozessierungsdatum>_<Uhrzeit>_0310.txt 2>&1 &
```



# Mercurial. How can I use editor "nano" to write commit message? #
```
Find your .hgrc file in your home directory and add the following line:

editor=vim

That should do it.

So let's say you use nano for cases like this. Your .hgrc file would read something like:

[ui]
username = Bob Jones <Bob.Jones@gmail.com>
editor=nano

```

# Überprüfung der prozessierten Daten (Level 310) #
  * Skript "revision\_level\_310\_auto.R" starten für Prozessierungslevel 310 (muss für jede Region (AEG, AEW, HEG, HEW, SEG, SEW) einzeln gestartet werden). Skript muss insgesamt zweimal pro Region gestartet werden, nämlich beim ersten Durchlauf mit "compute.thv <- TRUE" (Zeile 4) und beim zweiten Durchlauf mit "compute.thv <- FALSE".
  * Dann Skript "revision\_level\_310\_manual.R" starten (muss ebenfalls für jede Region einzeln gestartet werden).
  * Dann die korrigierten 310er-Dateien visualisieren und prüfen.
  * Nun mit den korrigierten 310er-Dateien die Prozessierungslevels 400, 405 und 420 starten.