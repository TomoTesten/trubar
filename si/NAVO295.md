---
kratica: NAVO295
naziv: "Navodilo za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki"
vrsta: "navodilo"
datum: 1998-10-23
sop: 1998-01-3581
organ: ""
zbirka: "Neuradna prečiščena besedila"
status: "Neznano"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=1998-01-3581"
---

# Navodilo za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki

Generalni direktor Agencije Republike Slovenije za plačilni promet določa prečiščeno besedilo navodila za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki.

Prečiščeno besedilo navodila za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki obsega: navodilo za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki (Uradni list RS, št. 9/95), ki je začelo veljati 4. 3. 1995, navodilo o spremembah in dopolnitvah navodila za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki (Uradni list RS, št. 70/95), ki je začelo veljati 1. 1. 1996, navodilo o spremembah in dopolnitvah navodila za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki (Uradni list RS, št. 5/97), ki je začelo veljati 15. 2. 1997, navodilo o spremembah in dopolnitvah navodila za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki (Uradni list RS, št. 17/97), ki je začelo veljati 29. 3. 1997, navodilo o spremembah in dopolnitvah navodila za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki (Uradni list RS, št. 81/97), ki je začelo veljati 30. 12. 1997

Št. 660-34/98

Ljubljana, dne 15. oktobra 1998.

Darinka Pozvek l. r.
Generalna direktorica


## N A V O D I L O
za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki
(prečiščeno besedilo)


### I. SPLOŠNE DOLOČBE


### 1

Pravne osebe lahko predložijo podatke s plačilnih nalogov Agenciji Republike Slovenije za plačilni promet (v nadaljnjem besedilu: agencija) na magnetnih medijih (magnetni trak in PC disketa) in prevzamejo podatke s plačilnih nalogov od agencije na magnetnih medijih ali z neposredno računalniško komunikacijo.


### 2

To navodilo predpisuje postopek predložitve in prevzema podatkov s plačilnih nalogov na magnetnih medijih.
Postopek za prevzem podatkov s plačilnih nalogov od agencije z neposredno računalniško komunikacijo pa se določi s pisnim dogovorom med pravno osebo in agencijo.


### 3

Pravne osebe lahko predložijo agenciji podatke s plačilnih nalogov na magnetnem mediju in na zbirnem nalogu za prenos (Obr. št. 47)(1) vključno s spremnim pismom k magnetnemu mediju, PRILOGA 1 tega navodila.
Podatki s plačilnih nalogov morajo izpolnjevati naslednje pogoje:
– podatki na magnetnem mediju in na priloženem zbirnem nalogu za prenos morajo biti enaki in zapisani v enakem vrstnem redu,
– podatki smejo veljati samo za en datum obdelave,
– plačilni nalogi morajo biti razvrščeni v skladu s prioriteto njihove izvršitve.
Pravne osebe lahko agenciji predlagajo na magnetnem mediju tudi nujne plačilne naloge. V tem primeru morajo biti ti plačilni nalogi predloženi ločeno od rednih plačilnih nalogov – na posebnem magnetnem mediju.


### II. OPIS MAGNETNEGA MEDIJA ZA PREDLOŽITEV  IN PREVZEM PODATKOV S PLAČILNIH NALOGOV


### 4

Magnetni trak, s pomočjo katerega se posredujejo in prevzemajo podatki s plačilnih nalogov, mora imeti naslednje lastnosti:
– 9-sledni,
– gostota zapisa 1600 BPI,
– obvezna standardna sistemska labela, zapisana v kodi ASCII,
– faktor blokiranja 10,
– stavki zapisani v standardu ISO 8859-2 (8 bit),
– podatki nepakirani,
– uporabljene le velike črke.


### 5

Disketa, s pomočjo katere se posredujejo in prevzemajo podatki s plačilnih nalogov, mora imeti naslednje lastnosti:
– velikost 5,25" ali 3,5",
– formatirana v PC DOS formatu,
– ime datoteke s podatki: TKDIS.TXT,
– stavki zapisani v standardu JUS. I. B1. 002 (1982),
– stavki ločeni med seboj z znakoma CR (CtrlM, 13dec) in LF (CtrlJ, 10dec),
– datoteka zaključena z znakom SUB (CtrlZ, 26dec),
– uporabljene le velike črke.
Podatki na magnetnem mediju so lahko zapisani tudi v ASCII kodi (7 bit), vendar morajo biti sledeče črke (šumniki) zapisani s kodo:
Č-5E, Š-5B, Ž-40, Ć-5D, Đ-5C (hex)
Č-94, Š-91, Ž-64, Ć-93, Đ-92 (dec).


### III. STRUKTURA STAVKOV NA MAGNETNEM MEDIJU


### a) Predložitev magnetnega medija agenciji


### 6

Zapis na magnetnem mediju, ki ga pravne osebe predložijo agenciji, vsebuje tri vrste stavkov: naslovnega, zbirnega in individualnega.
Stavki se zapišejo po naslednjem vrstnem redu:
naslovni {zbirni (individualni)}.
Naslovnemu stavku sledijo skupine, sestavljene iz enega zbirnega in več individualnih stavkov. Zbirni stavek in pripadajoči individualni stavki sestavljajo logično celoto podatkov:
– na magnetnem mediju sme biti toliko zbirnih stavkov, kolikor je priloženih zbirnih nalogov za prenos, vendar ne več kot 999; v okviru enega zbirnega naloga za prenos sme biti največ 9.999 individualnih nalogov,
– skupni znesek v okviru ene logične celote na sme presegati 11 desetiških mest, ne glede na to, da je za znesek predvidenih 15 mest,
– številčni podatki morajo biti na magnetnem mediju zapisani z vodilnimi ničlami,
– prazna polja se izpolnijo s presledki (32dec).


### 7

Struktura naslovnega stavka:

– številka računa predlagatelja                        18 znakov
 številka organizacijske enote agencije                 5 znakov
 številka osnovnega računa                               3 znaki
 številka namena sredstev ali občine                     3 znaki
 številka individualne partije računa                   7 znakov
– ime predlagatelja                                    35 znakov
– kraj predlagatelja                                   10 znakov
– datum obdelave (ddmmll)                               6 znakov
– številka magnetnega medija                             3 znaki
– vrsta posla                                            3 znaki
– prazno                                              104 znakov
– tip stavka                                              1 znak
----------------------------------------------------------------
Skupaj                                                180 znakov

Številka računa predlagatelja
(številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine, številka individualne partije računa) je identifikator predlagatelja magnetnega medija.
Datum obdelave
je datum, pod katerim mora agencija obdelati predložene podatke.
Številka magnetnega medija
je oznaka, ki jo predlagatelju magnetnega medija določi organizacijska enota agencije.
Vrsta posla je oznaka 16.
Tip stavka je oznaka 0.


### 8

Struktura zbirnega stavka:

– številka računa nalogodajalca                        18 znakov
 številka organizacijske enote agencije                 5 znakov
 številka osnovnega računa                               3 znaki
 številka namena sredstev ali občine                     3 znaki
 številka individualne partije računa                   7 znakov
– ime nalogodajalca                                    35 znakov
– kraj nalogodajalca                                   10 znakov
– skupni znesek (s stotini)                            15 znakov
– število plačilnih nalogov                             5 znakov
– vrsta logične celote                                    1 znak
– karakter logične celote                                 1 znak
– prazno                                               89 znakov
– številka specifikacije                                 3 znaki
– vir informacije                                        2 znaka
– tip stavka                                              1 znak
----------------------------------------------------------------
Skupaj                                                180 znakov

Številka računa nalogodajalca
(številka organizacijske enote agencije, številka osnovnega računa, številka namena ali občine, številka individualne partije računa) je identifikator nalogodajalca. Lahko je enaka številki računa v naslovnem stavku, lahko je drugačna. Predlagatelj magnetnega medija sme na enem magnetnem mediju predložiti zbirne (in pripadajoče individualne) stavke za različne račune iste pravne osebe.
Skupni znesek
je seštevek zneskov individualnih plačilnih nalogov v okviru logične celote podatkov (zbirnega stavka).
Število plačilnih nalogov
je število individualnih plačilnih nalogov v okviru logične celote podatkov (zbirnega stavka).
Vrsta logične celote:
– oznaka 1, če vsi individualni plačilni nalogi v okviru zbirnega naloga za prenos vsebujejo vse zahtevane podatke,
– sicer oznaka 0.
Karakter logične celote:
– za naloge obremenitve: oznaka 1,
– za naloge odobritve: oznaka 2.
Številka specifikacije
je zaporedna številka dneva v letu. Podatek se v polje vpiše, le v primerih, ko je vpisan tudi podatek o viru informacije 14 ali 21, sicer pa polje ostane prazno in se ga izpolni v skladu s četrto alineo drugega odstavka 6. točke tega navodila.
Vir informacije:
(14 = gotovinska vplačila, opravljena v bankah)
(21 = gotovinska vplačila, opravljena na poštah)
(33 = disketa z nujnimi plačilnimi nalogi)
(34 = magnetni trak z nujnimi plačilnimi nalogi)
(35 = nujni plačilni nalogi, predloženi po elektronski pošti).
Kolikor se ne uporabi nobenega od navedenih virov informacije, ta prostor ostane prazen in se ga izpolni v skladu s četrto alineo drugega odstavka 6. točke tega navodila.
Tip stavka je oznaka 9.


### 9

Struktura individualnega stavka:

– številka računa prejemnika
plačila/plačnika                                       18 znakov
 številka organizacijske enote agencije                 5 znakov
 številka osnovnega računa                               3 znaki
 številka namena sredstev ali občine                     3 znaki
 številka individualne partije računa                   7 znakov
– ime prejemnika plačila/plačnika                      35 znakov
– kraj prejemnika plačila/plačnika                     10 znakov
– zakonska prioriteta                                     1 znak
– sklicevanje na številko (obremenitev)                24 znakov
– namen nakazila                                       36 znakov
– prazno                                                5 znakov
– šifra izdatkov in šifra prejemkov                     6 znakov
– znesek (s stotini)                                   13 znakov
– sklicevanje na številko (odobritev)                  24 znakov
– prazno                                                7 znakov
– tip stavka                                              1 znak
----------------------------------------------------------------
Skupaj                                                180 znakov

Številka računa prejemnika plačila/plačnika
(številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine, številka individualne partije računa) je identifikator prejemnika plačila oziroma plačnika.
Zakonska prioriteta
je številka vrstnega reda plačila obveznosti iz 36. člena zakona o Agenciji Republike Slovenije za revidiranje lastninskega preoblikovanja podjetij in o Agenciji Republike Slovenije za plačilni promet, nadziranje in informiranje.
Sklicevanje na številko (obremenitev)
je podatek, ki natančneje identificira poslovno spremembo pri plačniku.
Namen nakazila
je opis namena nakazila.
Šifra
je sestavljena iz oznake za zvezo in šifre izdatkov in šifre prejemkov.
Znesek
je znesek posameznega plačilnega naloga iz zbirnega naloga za prenos.
Sklicevanje na številko (odobritev)
je podatek, ki natančneje identificira poslovno spremembo pri prejemniku plačila.
Tip stavka je oznaka 1.


### b) Prevzem magnetnega medija od agencije


### 10

Pravne osebe od agencije skupaj z magnetnim medijem dobijo tudi pisno dokumentacijo o prometu in stanju denarnih sredstev na računih ter spremno pismo k magnetnemu mediju.
Pisna dokumentacija vsebuje podatke o skupnem prometu v breme in v dobro ter o stanju denarnih sredstev na posameznem računu pravne osebe ter tudi podatke za posamične prejete naloge odobritev in obremenitev.
Spremno pismo k magnetnemu mediju je PRILOGA 2 tega navodila.


### 11

Na magnetnem mediju, ki ga agencija pripravi za pravne osebe, so podatki oblikovani takole:

------------------------------------------------------------------------------------------------------------
Zap.
št.          Pozicija     Dolžina      Tip          Opis polja
------------------------------------------------------------------------------------------------------------
1.             1–5         5           N            Številka organizacijske enote agencije  nalogodajalca
2.             6–8         3           N            Osnovni račun nalogodajalca
3.            9–11         3           N            Namen/občina
4.           12–18         7           N            Individualna partija računa nalogodajalca
5.           19–20         2           N            Vir informacije:
                                                    (1x = obremenitev)
                                                    (2x = odobritev)
6.           21–28         8           Date         Datum obdelave v agenciji (DD.MM.LL)
7.              29         1           Char         Vir informacije:
                                                    (S = storno nalog)
                                                    (T = telefonski nalog)
8.              30         1           Char         Prazno
9.           31–65        35           Char         Ime prejemnika magnetnega medija
10.             66         1           N            Način izvršitve plačilnega naloga
11.          67–72         6           Date         Datum plačila v banki/pošti (DDMMLL)
12.          73–77         5           N            Številka organizacijske enote agencije prejemnika
                                                    magnetnega medija
13.          78–80         3           N            Osnovni račun prejemnika magnetnega medija
14.          81–83         3           N            Namen /občina
15.          84–90         7           N            Individualna paritja računa prejemnika magnetnega medija
16.          91–105       15           N            Znesek
17.          106–107       2           N            Oznaka za zvezo
18.          108–109       2           N            Šifra izdatkov
19.          110–111       2           N            Šifra prejemkov
20.          112–135      24           Char         Sklicevanje na številko obremenitve
21.          136–159      24           Char         Sklicevanje na številko odobritve
22.          160–195      36           Char         Namen nakazila
23.          196–205      10           Char         Kraj nalogodajalca
24.          206–240      35           Char         Ime nalogodajalca
25.          241–262      22           N            Številka za reklamacijo
26.          263–280      18           N            Številka računa
------------------------------------------------------------------------------------------------------------

Številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine in številka individualne partije računa nalogodajalca so identifikatorji nalogodajalca, razen v primerih, ko nalogodajalec obremeni račun prejemnika magnetnega medija.
Vir informacije
je oznaka posameznega plačilnega naloga v breme (1x) oziroma v dobro (2x) računa prejemnika magnetnega medija.
Datum obdelave v agenciji
je datum, pod katerim je agencija obdelala podatke, ki so na magnetnem mediju.
Način izvršitve plačilnega naloga
je številčni podatek, ki pomeni:
1 – plačilo, izvršeno brez dostave originalnega plačilnega naloga,
5 – plačilo, izvršeno z zbirnimi avizami po pošti.
Datum plačila v banki/pošti
je datum, ko je bilo plačilo opravljeno v banki ali na pošti.
Številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine in številka individualne partije računa prejemnika magnetnega medija so identifikatorji prejemnika plačila, razen v primerih, ko nalogodajalec obremeni njegov račun.
Znesek in vsebina podatkov: oznake za zvezo, šifre izdatkov in šifre prejemkov, sklicevanje na številko (obremenitve in odobritve) so pojasnjeni pri individualnem stavku v točki a) Predložitev magnetnega medija agenciji.
Številka računa
je podatek o številki računa, v dobro katerega je bil izdan plačilni nalog, ki je bil izvršen v dobro računa naslednika.


### IV. ZAPIS IN KONTROLA PODATKOV NA MAGNETNEM MEDIJU


### 12

Plačilni nalogi, ki jih pravne osebe posredujejo agenciji na magnetnem mediju, morajo vsebovati vse predpisane podatke. Pred predložitvijo magnetnega medija agenciji morajo pravne osebe vse vsebovane podatke preveriti na način in po postopku, opisanem v tem navodilu.


### 13

1. Kontrola številke računa plačnika in številke računa prejemnika plačila:
– kontrola številke organizacijske enote agencije, pri kateri se vodi račun plačnika oziroma prejemnika plačila, se opravi glede na obstoj številke v Pregledu oznak za organizacijske enote agencije(2),
– kontrola številke osnovnega računa plačnika oziroma prejemnika plačila se opravi glede na obstoj osnovnega računa v Planu računov za opravljanje plačilnega prometa prek agencije(2),
– kontrola številke namena sredstev pri osnovnih računih razreda 7 plana računov se opravi glede na obstoj številke za namen sredstev v pregledu oznak za namen sredstev(2),
– kontrola številke za občine pri osnovnih računih 840, 842, 843 in 844 se opravi glede na obstoj številke za občino v Pregledu oznak za občine(2) (pri osnovnih računih razredov 6, 7, 8 plana računov, za katere ni predvidena oznaka za namen sredstev oziroma oznaka za občino, se vsa tri mesta v tem polju izpolnijo z ničlami),
– kontrola kontrolne številke individualne partije plačnika oziroma prejemnika plačila se opravi po modulu 11 takole:
– posamezne številke individualne partije z leve proti desni se pomnožijo s ponderji 0, 1, 2, 3, 4 in 5,
– seštevek zmnožkov se deli z 11,
– ostanek pri deljenju se odšteje od 11,
– dobljeni rezultat je kontrolna številka individualne partije, če je 1< k < 9, kontrolna številka je 0, če je k=11, ni kontrolna številka individualne partije, če je k=10.
2. Za plačilne naloge, predložene na magnetnem mediju, se na 1. in 2. mestu v podatku šifra vpiše oznaka za zvezo 88. Šifre izdatkov in šifre prejemkov na 3., 4., 5. in 6. mestu se vpišejo in kontrolirajo na podlagi pregleda šifer prejemkov in izdatkov po osnovnih računih pravnih oseb. Pregled šifer prejemkov in izdatkov po osnovnih računih pravnih oseb je v prilogi navodila o izvajanju mesečnega statističnega raziskovanja o prejemkih na račune in izdatkih z računov, ki jih vodi agencija Republike Slovenije za plačilni promet, nadziranje in informiranje (PI), Uradni list RS, št. 70/95, 1/96, 25/97 in 7/98.
3. Kontrola podatkov v sklicevanju na številko obremenitve oziroma odobritve se opravi na način, predpisan za izbrano številko modela v pregledu in vsebini osnovnih modelov za sklicevanje na številko obremenitve in odobritve ter v pojasnilih za njihovo uporabo(3).
Podatki v sklicevanju na številko obremenitve in odobritve se ne kontrolirajo samo v primeru, če je izbrana številka modela 00.
4. Seštevek zneskov z vseh posameznih plačilnih nalogov na magnetnem mediju mora ustrezati znesku pod “skupaj tolarjev po zbirnem nalogu” v zbirnem nalogu za prenos.
Pravne osebe lahko opravijo kontrolo podatkov na magnetnem mediju s svojim računalniškim programom ali pa z računalniškim programom, ki ga dobijo v organizacijskih enotah agencije.
5. Kontrola podatka o zakonski prioriteti se opravi na podlagi številk vrstnega reda plačila obveznosti, določenega v zakonu iz 9. točke tega navodila.


### V. PREHODNE IN KONČNE DOLOČBE

1. Navodilo za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki (Uradni list RS, št. 9/95) vsebuje naslednje prehodne in končne določbe:


### 14

Pravne osebe, ki imajo odprte žiro račune v podružnicah agencije z UNISYS računalniškimi sistemi, do prehoda vseh podružnic agencije na obdelavo podatkov plačilnega prometa na enakih računalniških sistemih, lahko agenciji predlagajo podatke s plačilnih nalogov v skladu s tem navodilom, le na PC disketah.
agencija bo sprejemala oziroma posredovala podatke pravnim osebam v podružnicah agencije z UNISYS računalniškimi sistemi tudi v obliki in vsebini, ki je veljala do začetka veljavnosti tega navodila, vendar najdalj do 31. 12. 1995.


### 15

Z dnem, ko začne veljati to navodilo, prenehajo veljati določbe PRILOGE 3 navodila za sprejem, kontrolo pravilnosti in izvrševanje plačilnih nalogov v plačilnem prometu v Službi družbenega knjigovodstva (Glasnik SDK, št. 16/86, s spremembami in dopolnitvami).
2. navodilo o spremembah in dopolnitvah navodila za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki (Uradni list RS, št. 17/97) vsebuje naslednje prehodne in končne določbe.


### 16

O začetku vpisovanja podatka o zakonski prioriteti iz  9. točke, bo agencija na primeren način obvestila imetnike računov pri agenciji.

1 Oblika, vsebina in uporaba zbirnega naloga za prenos so določene v navodilu o obliki, vsebini in uporabi obrazcev za opravljanje plačilnega prometa prek Agencije Republike Slovenije za plačilni promet (prečiščeno besedilo) - Uradni list RS, št. 72/98
2 Pregled oznak za organizacijske enote agencije, plan računov za opravljanje plačilnega prometa prek agencije, pregled oznak za namen sredstev in pregled oznak za občine, dobijo pravne osebe pri organizacijski enoti agencije, ki vodi njihov račun.
3 Pregled in vsebina osnovnih modelov za sklicevanje na številko obremenitve in odobritve ter pojasnila za njihovo uporabo je PRILOGA 2 navodila o obliki, vsebini in uporabi obrazcev za opravljanje plačilnega prometa prek Agencije Republike Slovenije za plačilni promet (prečiščeno besedilo) - Uradni list RS, št. 72/98.

PRILOGA 1

-----------------------------------------------
(predlagatelj magnetnega medija - pravna oseba)

                SPREMNO PISMO K MAGNETNEMU MEDIJU

-----------------------------------------------------------------
  (prejemnik magnetnega medija - organizacijska enota Agencije)

-----------------------------------------------------------------
                    (vrsta magnetnega medija)

-----------------------------------------------------------------
                         (ime datoteke)

-----------------------------------------------------------------
                        (gostota zapisa)

-----------------------------------------------------------------
                   (velikost logičnega stavka)

-----------------------------------------------------------------
               (velikost fizičnega stavka - bloka)

-----------------------------------------------------------------
                       (vrsta računalnika)

-----------------------------------------------------------------
                 (število individualnih stavkov)

-----------------------------------------------------------------
                            (opomba)

---------------------
      (datum)

                                            Podpis predlagatelja:

PRILOGA 2
AGENCIJA REPUBLIKE SLOVENIJE
ZA PLAČILNI PROMET

-----------------------------------
(organizacijska enota Agencije)

                SPREMNO PISMO K MAGNETNEMU MEDIJU

-----------------------------------------------------------------
          (prejemnik magnetnega medija - pravna oseba)

-----------------------------------------------------------------
            (žiro račun prejemnika magnetnega medija)

-----------------------------------------------------------------
                        (datum obdelave)

-----------------------------------------------------------------
                  (ime datoteke na PC disketi)

-----------------------------------------------------------------
                         (magnetni trak)

-----------------------------------------------------------------
                        (gostota zapisa)

-----------------------------------------------------------------
                 (število individualnih stavkov)

-----------------------------------------------------------------
                 (skupni znesek prometa v breme)

-----------------------------------------------------------------
                 (skupni znesek prometa v dobro)

---------------------
      (datum)

                                         Podpis delavca agencije:
