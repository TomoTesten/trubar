---
kratica: NAVO127
naziv: "Navodilo za izvajanje sklepa o obveznosti rezidentov in nerezidentov, da kupujejo oziroma prodajajo tuj denar samo od oseb, ki so si za opravljanje teh poslov predhodno pridobile dovoljenje Banke Slovenije in o obveznosti poročanja o tako sklenjenih poslih"
vrsta: "navodilo"
datum: 1999-06-28
sop: 1999-01-2407
organ: ""
zbirka: "Neuradna prečiščena besedila"
status: "Neznano"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=1999-01-2407"
---

# Navodilo za izvajanje sklepa o obveznosti rezidentov in nerezidentov, da kupujejo oziroma prodajajo tuj denar samo od oseb, ki so si za opravljanje teh poslov predhodno pridobile dovoljenje Banke Slovenije in o obveznosti poročanja o tako sklenjenih poslih

Na podlagi četrtega odstavka 45. člena in četrtega odstavka 53. člena zakona o deviznem poslovanju (Uradni list RS, št. 23/99), drugega odstavka 2. točke sklepa o obveznosti rezidentov in nerezidentov, da kupujejo oziroma prodajajo tuj denar samo od oseb, ki so si za opravljanje teh poslov predhodno pridobile dovoljenje Banke Slovenije (Uradni list RS, št. 50/99) in 23. člena zakona o Banki Slovenije (Uradni list RS, št. 1/91-I) izdaja guverner Banke Slovenije


## N A V O D I L O
za izvajanje sklepa o obveznosti rezidentov in nerezidentov, da kupujejo oziroma prodajajo tuj denar samo od oseb, ki so si za opravljanje teh poslov predhodno pridobile dovoljenje Banke Slovenije in o obveznosti poročanja o tako sklenjenih poslih

1. Banke, pooblaščene za opravljanje poslov s tujimi plačilnimi sredstvi, morajo Banki Slovenije dnevno do 12. ure dostavljati podatke o vsakem posamičnem poslu nakupa ali prodaje tujih plačilnih sredstev sklenjenem preteklega delovnega dne, če so znani vsi potrebni podatki za njegovo izvršitev.
O poslih nakupa med bankami poročata tako banka prodajalec kot banka kupec.
2. Banka posreduje podatke (zaključnica z vsemi potrebnimi podatki v prilogi) o vsakem posameznem poslu nakupa oziroma prodaje deviz:
– matično številko banke poročevalke
– oznako vrste posla
– datum sklenitve posla
– datum izvršitve posla
– matična številka prodajalca
– matična številka kupca
– oznaka valute
– znesek v valuti
– znesek v tolarjih
– tečaj.
3. Banka za vsak nakup oziroma prodajo deviz določi oznako posla. Oznako posla banka določi iz šifranta poslov glede na osebe, ki kupujejo oziroma prodajajo tuja plačilna sredstva.

02 odkup bank od podjetij    kupec je banka, prodajalec je
                             podjetje
03 nakupi od drugih bank     kupec in prodajalec je banka
04 prodaja bank podjetjem    kupec je podjetje, prodajalec je
                             banka
05 prodaje drugim bankam     kupec in prodajalec je banka
06 odkup od nerezidenta      kupec je banka, prodajalec je
                             nerezident
07 prodaja nerezidentu       kupec je nerezident, prodajalec je
                             banka
08 odkup od fizičnih oseb    kupec je banka, prodajalec je
                             fizična oseba
09 prodaja fizičnim osebam   kupec je fizična oseba, prodajalec
                             je banka.

Pri poslih nakupa oziroma prodaje tujih plačilnih sredstev, kjer je datum izvršitve za več kot 3 delovne dni daljši od dneva sklenitve posla, banka posreduje tudi podatek o datumu izvršitve posla, ter posameznemu poslu določi oznako vrste posla iz šifranta terminskih poslov:

22 odkup bank od podjetij    kupec je banka, prodajalec je
                             podjetje
23 nakupi od drugih bank     kupec in prodajalec je banka
24 prodaja bank podjetjem    kupec podjetje, prodajalec je banka
25 prodaje drugim bankam     kupec in prodajalec je banka
26 odkup od nerezidenta      kupec je banka, prodajalec je
                             nerezident
27 prodaja nerezidentu       kupec je nerezident, prodajalec je
                             banka
28 odkup od fizičnih oseb    kupec je banka, prodajalec je
                             fizična oseba
29 prodaja fizičnim osebam   kupec je fizična oseba, prodajalec
                             je banka

Poslov nakupa ali prodaje tujih plačilnih sredstev z Banko Slovenije banke ne poročajo.
4. Matična številka prodajalca ali kupca je:
– matična številka gospodarske družbe (banka, podjetje, obrtniki) je številka iz enotnega registra slovenskih organizacij in obrtnikov SURS
– matična številka domače fizične osebe je “5980003“, osebe zaposlene v svobodnih poklicih “6000053“ in za kmete “5000009“
– matična številka nerezidenta je sestavljena iz nizov “0001“ (tuja pravna oseba), “0002“ (tuja banka) ali “0003“ (tuja fizična oseba), ki jim je dodana trimestna numerična številka države nerezidenta. (Primer: tuja pravna oseba iz Avstrije ima matično številko “0001040“.)
5. Banka posreduje Banki Slovenije podatke po elektronski pošti (BS Net) v skladu s strukturo datoteke elektronskih zapisov o zaključnicah, ki je priložena temu navodilu.
6. Naslov za posredovanje poročil je:

Country (C)                   = SI
Administrative_domain (A)     = MAIL
Private_domain (P)            = BSLO
Organization (O)              = BS
Organization_unit (OUI)       = APPSRVR
Surname (S)                   = TRG

7. Vsako sporočilo naj vsebuje samo podatke in nobenih dodatnih tekstovnih obrazložitev. Subjekt je sestavljen iz niza:

-----------------------------------------------------------------
Podatek          Pozicija   Pozicija   Tip                Dolžina
                    od         do
-----------------------------------------------------------------
"TRG"                1          3      konstanta "TRG"          3
matična številka
poročevalke          4         10      numerični                7
datum pošiljanja    11         28      datumski tip formata
                                       LLLLMMDD                 8
"ZAKLJ"             29         33      konstanta "ZAKLJ"        5
-----------------------------------------------------------------

Če datum pošiljanja ni enak dnevu prispetja pošte, je pošta zavrnjena.
V Banki Slovenije se izvede smiselna in logična kontrola. Po elektronski pošti Banka Slovenije obvesti banko o ugotovljenih napakah, in sicer so v pripeti datoteki navedene ugotovljene napake. Če je procent napačnih zaključnic večji od določenega procenta tolerance, se zaključnice zavrnejo v celoti, tudi pravilne. Če je procent napačnih zaključnic manjši ali enak določenemu procentu tolerance, se vrnejo le napačne zaključnice. Posameznemu zapisu so dodane ugotovljene napake, šifrant napak je napisan na začetku datoteke. Ime datoteke z napačnimi zaključnicami ima obliko LLLLMMDD.nno. LLLLMMDD predstavlja datum pošiljanja podatkov, nn zaporedno številko poslane datoteke na dan pošiljanja, o pa ima dve vrednosti: Z – če je datoteka zavrnjena v celoti in N – če so napačni le posamezni zapisi.
Banka, ki prejme zavrnjeno datoteko v celoti (oznaka Z), pošlje ponovno celo poročilo brez potrebnega predhodnega brisanja napačnih podatkov. Če so zavrnjene le posamezne zaključnice (datoteka z oznako N), banka najprej pošlje zapis napačnih zaključnic z navedbo vrste transakcije 99 – brisani zapis, ter pod redno oznako transakcije 01 pravilne podatke.
Popravljene podatke je dolžna banka poslati Banki Slovenije naslednji delovni dan po dnevu zavrnjenega zapisa do 12. ure.
8. Struktura datoteke elektronskih zapisov o zaključnicah
Datoteka s podatki o zaključnicah (poslanih od banke poročevalke) je sestavljen iz dveh tipov zapisov:
Tip A (prvi in zadnji zapis v datoteki)

----------------------------------------------------------------------------------------------------------------------------
Podatek                                 Pozicija od     Pozicija do            Tip                                 Dolžina
----------------------------------------------------------------------------------------------------------------------------
"ZAKLJ"                                     1                5                 Konstanta "ZAKLJ"                          5
Matična številka poročevalke                6               12                 Numerični                                  7
Datum pošiljanja                           13               20                 Datumski tip formata LLLLMMDD              8
Število zapisov o zaključnicah             21               30                 Numerični                                 10
Vsota zneskov v tolarjih zapisov           31               48                 Numerični                   16 celih mest in
o zaključnicah                                                                                            2 decimalni mesti
----------------------------------------------------------------------------------------------------------------------------

Tip B (zapis o zaključnicah)

----------------------------------------------------------------------------------------------------------------------------
Podatek                                 Pozicija od      Pozicija do           Tip                                 Dolžina
----------------------------------------------------------------------------------------------------------------------------
Vrsta transakcije                           1                  2               Konstanta "01" za redni zapis
                                                                               Konstanta "99" za brisani zapis            2
Matična številka poročevalke                3                  9               Numerični                                  7
Oznaka vrste posla                         10                 11               Priloženi šifrant                          2
Datum sklenitve posla                      12                 19               Datumski tip formata LLLLMMDD              8
Datum izvršitve posla                      20                 27               Datumski tip formata LLLLMMDD              8
Matična številka prodajalca                28                 34               Numerični                                  7
Matična številka kupca                     35                 41               Numerični                                  7
Valuta                                     42                 44               Numerična šifra valute                     3
Znesek v valuti                            45                 59               Numerični                   13 celih mest in
                                                                                                          2 decimalni mesti
Znesek v tolarjih                          60                 74               Numerični                   13 celih mest in
                                                                                                          2 decimalni mesti
Tečaj                                      75                 87               Numerični                    7 celih mest in
                                                                                                          6 decimalnih mest
----------------------------------------------------------------------------------------------------------------------------

Vrsta transakcije:
Vsem novim zapisom dodelimo kot vrednost “01”. Zapisu, ki ga želimo brisati, priredimo vrednost “99”, vsi ostali podatki pa imajo enake vrednosti kot zapis, ki ga želimo brisati.
Vsi podatki so obvezni, le podatek “Datum izvršitve posla“ je obvezen pri terminskih vrstah poslov (oznaka posla od 21 do 29). Če podatka “Datum izvršitve posla“ ni, je dodeljena vrednost “00000000”.
Vsi podatki numeričnega tipa imajo vodilne ničle. Zneski niso predznačeni.
Prvi zapis datoteke je tipa A, sledijo mu zapisi tipa B. Na koncu datoteke pa je zopet zapis tipa A, ki ima enake vrednosti kot prvi zapis.
9. Z dnem uveljavitve tega navodila preneha veljati navodilo o načinu dostavljanja podatkov o izvršenih poslih nakupa in prodaje tujih plačilnih sredstev ter o najavah povpraševanja in ponudbe tujih plačilnih sredstev št. 23/00/371/92 z dne 10. 9. 1992.
10. To navodilo začne veljati 1. septembra 1999.

Ljubljana, dne 22. junija 1999

Guverner
Banke Slovenije
dr. France Arhar l. r.
