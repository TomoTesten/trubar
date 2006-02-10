---
kratica: NAVO803
naziv: "Navodilo o spremembah in dopolnitvah Navodila za izvajanje sklepa o obveznosti poročanja o poslovanju s tujino"
vrsta: "navodilo"
datum: 2006-02-24
sop: 2006-01-0765
organ: ""
zbirka: "Neuradna prečiščena besedila"
status: "Neznano"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=2006-01-0765"
---

# Navodilo o spremembah in dopolnitvah Navodila za izvajanje sklepa o obveznosti poročanja o poslovanju s tujino

Na podlagi 53. člena Zakona o deviznem poslovanju (Uradni list RS, št. 110/03 – uradno prečiščeno besedilo), 8. točke Sklepa o obveznosti poročanja o poslovanju s tujino (Uradni list RS, št. 92/03 in 56/04) in tretjega odstavka 29. člena Zakona o Banki Slovenije (Uradni list RS, št. 58/02 in 85/02) izdaja guverner Banke Slovenije


## N A V O D I L O
o spremembah in dopolnitvah Navodila za izvajanje sklepa o obveznosti poročanja o poslovanju s tujino


### 1

V Navodilu za izvajanje sklepa o obveznosti poročanja o poslovanju s tujino (Uradni list RS, št. 102/03, 135/03, 64/04 in 9/05) se v poglavju V. POROČILA O PLAČILNEM PROMETU S TUJINO 1. točka spremeni tako, da se glasi:

"Predmet poročanja so transakcije plačilnega prometa s tujino (glej prilogo PLAČILNI PROMET S TUJINO – TERJATVE IN OBVEZNOSTI DO TUJINE – SEZNAM KONTOV)."


### 2

V poglavju V. se spremeni prvi del prvega stavka 4. točke tako, da se glasi:

"Način poročanja: banke pošiljajo podatke v obliki zapisov VP60 – Plačilo nerezidenta rezidentu, VP70 – Plačilo rezidenta nerezidentu, VP66 in VP77 – Transakcije med rezidenti in nevtralne transakcije, VP06 in VP07 – Zbirno poročilo o transakcijah po elektronski pošti na naslov:"


### 3

V poglavju V. se črtata 5. in 6. točka.


### 4

V poglavju V. se 7. točka spremeni tako, da se glasi:

"Banka mora poročati o vsaki posamezni transakciji, ki je višja ali enaka protivrednosti 12.500,00 evrov. Kadar je več osnov plačila, se specifikacije osnov ne poroča, uporabi se osnova plačila najvišjega zneska.

+----------------+----+-+---------------------------------------------------+
|Vrsta posla (VP)|  2N| |60                                                 |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Banka           |  7N| |matična številka banke, ki pošilja podatke         |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Datum poročila  |  8N| |llllmmdd                                           |
|                |    | |pri računih, ki se poročajo dnevno, je lahko vsak  |
|                |    | |datum v okviru dekade;                             |
|                |    | |pri računih, ki se poročajo dekadno, je lahko samo |
|                |    | |zadnji dan dekade                                  |
+----------------+----+-+---------------------------------------------------+
|Račun           | 6AN| |račun iz priloge PLAČILNI PROMET S TUJINO –        |
|                |    | |TERJATVE IN OBVEZNOSTI DO TUJINE – SEZNAM KONTOV   |
|                |    | |(račun je lahko analitičen), ki ima v koloni       |
|                |    | |»TRANSAKCIJE PROMETA V BREME« kljukico             |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Oznaka vrste    |  1N| |1- v breme                                         |
|posla           |    | |                                                   |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Valuta          |  3N| |šifra valute iz šifranta valut                     |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Instrument      |  1N| |šifra instrumenta iz šifranta instrumentov plačil  |
|plačila         |    | |                                                   |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Banka           |  7N| |kadar banka, ki prva prejme kritje, ni ista kot je |
|                |    | |banka komitenta, je potrebno vpisati matično       |
|                |    | |številko druge slovenske banke; sicer matično      |
|                |    | |številko banke, ki pošilja podatke                 |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Uporabnik       |  7N| |matična številka rezidenta                         |
|plačila         |    | |                                                   |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Številka naloga |16AN| |evidenčna številka                                 |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Država banke    |  3N| |šifra države iz šifranta držav;                    |
|                |    | |pri računih nerezidentov šifra za Slovenijo        |
+----------------+----+-+---------------------------------------------------+
|SWIFT adresa    | 8AN| |šifra iz šifranta SWIFT adres (BIC)                |
|banke           |    | |                                                   |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Država partnerja| 3AN| |šifra države partnerja iz šifranta držav oziroma   |
|                |    | |šifra mednarodne organizacije                      |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Znesek v valuti | 16N| |različen od 0                                      |
|                |    | |1 predznak, 13 celih, 2 decimalki                  |
+----------------+----+-+---------------------------------------------------+
|Datum knjiženja |  8N| |llllmmdd                                           |
|                |    | |pri računih, ki se poročajo dnevno, mora biti      |
|                |    | |datum enak datumu iz polja datum poročila;         |
|                |    | |pri računih, ki se poročajo dekadno, mora biti     |
|                |    | |datum v okviru dekade                              |
+----------------+----+-+---------------------------------------------------+
|Protipostavka   | 6AN| |račun iz kontnega okvira za banke in hranilnice    |
|knjiženja       |    | |(lahko analitičen)                                 |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Zaporedna       |  2N| |Konstanta 01                                       |
|številka za     |    | |                                                   |
|osnovo          |    | |                                                   |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Osnova plačila  |  3N| |šifra osnove plačila iz šifranta plačil iz tujine  |
|                |    | |in plačil v tujino; dovoljena tudi šifra 000       |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Registrska      |  6N| |Konstanta 000000                                   |
|številka kredita|    | |                                                   |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Znesek v valuti | 16N| |1 predznak, 13 celih, 2 decimalki                  |
|za osnovo       |    | |                                                   |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Naziv partnerja |70AN| |obvezen vnos vsaj 10 znakov                        |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+
|Opis osnove     |70AN| |obvezen tekst samo pri zneskih v valuti za osnovo  |
|                |    | |nad protivrednostjo USD 100.000,00 (preračun po    |
|                |    | |srednjih tečajih BS na prvi dan dekade)"           |
|                |    | |                                                   |
+----------------+----+-+---------------------------------------------------+


### 5

V poglavju V. se spremeni 8. točka tako, da se glasi:

"Banka mora poročati o vsaki posamezni transakciji, ki je višja ali enaka protivrednosti 12.500,00 evrov." Kadar je več osnov plačila, se specifikacije osnov ne poroča, uporabi se osnova plačila najvišjega zneska.

+----------------+----+-+--------------------------------------------------+
|Vrsta posla (VP)|  2N| |70                                                |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Banka           |  7N| |matična številka banke, ki pošilja podatke        |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Datum poročila  |  8N| |llllmmdd                                          |
|                |    | |pri računih, ki se poročajo dnevno, je lahko vsak |
|                |    | |datum v okviru dekade;                            |
|                |    | |pri računih, ki se poročajo dekadno, je lahko     |
|                |    | |samo zadnji dan dekade                            |
+----------------+----+-+--------------------------------------------------+
|Račun           | 6AN| |račun iz priloge PLAČILNI PROMET S TUJINO –       |
|                |    | |TERJATVE IN OBVEZNOSTI DO TUJINE – SEZNAM KONTOV  |
|                |    | |(račun je lahko analitičen), ki ima v koloni      |
|                |    | |»TRANSAKCIJE PROMETA V DOBRO« kljukico            |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Oznaka vrste    |  1N| |2- v dobro                                        |
|posla           |    | |                                                  |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Valuta          |  3N| |šifra valute iz šifranta valut                    |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Instrument      |  1N| |šifra instrumenta iz šifranta instrumentov plačil |
|plačila         |    | |                                                  |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Banka           |  7N| |matična številka banke, ki je nalog sprejela od   |
|                |    | |komitenta                                         |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Nalogodajalec   |  7N| |matična številka rezidenta                        |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Številka naloga |16AN| |evidenčna številka                                |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Država partnerja| 3AN| |šifra države partnerja iz šifranta držav oziroma  |
|                |    | |šifra mednarodne organizacije                     |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Država banke    |  3N| |šifra države banke iz šifranta držav;             |
|                |    | |pri računih nerezidentov šifra za Slovenijo       |
+----------------+----+-+--------------------------------------------------+
|SWIFT adresa    | 8AN| |šifra iz šifranta SWIFT adres (BIC)               |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Znesek v valuti | 16N| |različen od 0                                     |
|                |    | |1 predznak, 13 celih, 2 decimalki                 |
+----------------+----+-+--------------------------------------------------+
|Datum knjiženja |  8N| |llllmmdd                                          |
|                |    | |pri računih, ki se poročajo dnevno, mora biti     |
|                |    | |datum enak datumu iz polja datum poročila;        |
|                |    | |pri računih, ki se poročajo dekadno, mora biti    |
|                |    | |datum v okviru dekade                             |
+----------------+----+-+--------------------------------------------------+
|Protipostavka   | 6AN| |račun iz kontnega okvira za banke in hranilnice   |
|knjiženja       |    | |(lahko analitičen)                                |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Zaporedna       |  2N| |konstanta 01                                      |
|številka za     |    | |                                                  |
|osnovo          |    | |                                                  |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Osnova plačila  |  3N| |šifra osnove plačila iz šifranta plačil iz tujine |
|                |    | |in plačil v tujino                                |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Registrska      |  6N| |Konstanta 000000                                  |
|številka kredita|    | |                                                  |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Znesek v valuti | 16N| |1 predznak, 13 celih, 2 decimalki                 |
|za osnovo       |    | |                                                  |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Naziv partnerja |70AN| |obvezen vnos vsaj 10 znakov                       |
|                |    | |                                                  |
+----------------+----+-+--------------------------------------------------+
|Opis osnove     |70AN| |obvezen tekst samo pri zneskih v valuti za osnovo |
|                |    | |nad protivrednostjo USD 100.000,00                |
|                |    | |(preračun po srednjih tečajih BS na prvi dan      |
|                |    | |dekade)"                                          |
+----------------+----+-+--------------------------------------------------+


### 6

V poglavju V. se spremeni 10. točka tako, da se glasi:

"Banke lahko posredujejo zbirne podatke za račune 701*, 708* in 818* za naslednje posle:

· polaganje tuje gotovine in čekov na račune in vloge nerezidentov v tuji valuti oziroma dvignjena tuja gotovina in izdani čeki z računov in vlog nerezidentov v tuji valuti (šifra osnove 898);
· povečanje oziroma zmanjšanje vlog nerezidentov – razen tujih bank in drugih tujih finančnih organizacij (šifri osnov 502 in 102);
· povečanje oziroma zmanjšanje vezanih vlog nerezidentov (šifri osnov 504 in 104);
· izplačilo v domači valuti v breme računov in vlog nerezidentov oziroma vplačilo v domači valuti v dobro teh računov brez konverzije (šifra osnove 890)
· izplačilo v domači valuti v breme računov in vlog nerezidentov oziroma vplačilo v domači valuti v dobro računov in vlog nerezidentov s konverzijo (šifra osnove 891)
· prenosi med istovrstnimi računi (šifri osnov 565 in 165).

+----------------------+-----+-+-------------------------------------------+
|Vrsta posla (VP)      |   2N| |06, 07                                     |
|                      |     | |06 – za knjižbe v breme računa             |
|                      |     | |07 – za knjižbe v dobro računa             |
+----------------------+-----+-+-------------------------------------------+
|Banka                 |   7N| |matična številka banke, ki pošilja poročilo|
|                      |     | |                                           |
+----------------------+-----+-+-------------------------------------------+
|Datum poročila        |   8N| |llllmmdd                                   |
|                      |     | |samo zadnji dan dekade                     |
+----------------------+-----+-+-------------------------------------------+
|Račun                 |  6AN| |701*, 708* in 818* (lahko analitičen)      |
|                      |     | |                                           |
+----------------------+-----+-+-------------------------------------------+
|Oznaka vrste posla    |   1N| |1-v breme, 2- v dobro                      |
|                      |     | |1 – samo pri vrsti posla 06                |
|                      |     | |2 – samo pri vrsti posla 07                |
+----------------------+-----+-+-------------------------------------------+
|Valuta                |   3N| |šifra iz šifranta valut                    |
|                      |     | |                                           |
+----------------------+-----+-+-------------------------------------------+
|Zaporedna številka za |   2N| |biti mora večja od 0                       |
|osnovo                |     | |                                           |
|                      |     | |                                           |
+----------------------+-----+-+-------------------------------------------+
|Osnova plačila        |   3N| |šifra osnove plačila iz šifranta plačil iz |
|                      |     | |tujine in plačil v tujino                  |
|                      |     | |                                           |
+----------------------+-----+-+-------------------------------------------+
|Znesek v valuti za    |  16N| |različen od 0                              |
|osnovo                |     | |1 predznak, 13 celih, 2 decimalki          |
|                      |     | |                                           |
+----------------------+-----+-+-------------------------------------------+
|Protipostavka         |  6AN| |račun iz kontnega okvira za banke in       |
|knjiženja             |     | |hranilnice (lahko analitičen)              |
|                      |     | |                                           |
+----------------------+-----+-+-------------------------------------------+
|»Prazno«              |215A"| |                                           |
|                      |     | |                                           |
+----------------------+-----+-+-------------------------------------------+


### 7

Priloga "PLAČILNI PROMET S TUJINO – TERJATVE IN OBVEZNOSTI DO TUJINE – SEZNAM KONTOV" se spremeni tako, da se glasi:


### 8

To navodilo začne veljati z dnem objave v Uradnem listu RS, uporabljati pa se začne z dnem 1. 1. 2007.
Ne glede na prejšnji odstavek so poročevalci od 1. 4. 2006 dalje dolžni poročati za konte 1086, 1110 in 1111 po veljavnem navodilu.

Ljubljana, dne 15. februarja 2006

Guverner
Banke Slovenije
Mitja Gaspari l.r.
