---
kratica: NAVO332
naziv: "Navodilo za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki"
vrsta: "navodilo"
datum: 1995-02-17
sop: 1995-01-0549
organ: ""
zbirka: "Neuradna prečiščena besedila"
status: "Neznano"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=1995-01-0549"
---

# Navodilo za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki

Na podlagi drugega in tretjega odstavka 4. člena, 19. člena ter drugega odstavka 77. člena zakona o Agenciji Republike Slovenije za plačilni promet, nadziranje in informiranje (Uradni list RS, št. 48/94), šestega odstavka 28. točke navodila o obliki, vsebini in uporabi obrazcev za opravljanje plačilnega prometa prek Agencije Republike Slovenije za plačilni promet, nadziranje in informiranje (Uradni list RS, št. 9/95) in v skladu z izdanim soglasjem Banke Slovenije, št. 29.00-1/95, z dne 10. 1. 1995, generalni direktor Agencije Republike Slovenije za plačilni promet, nadziranje in informiranje izdaja


## N A V O D I L O
za predložitev in prevzem podatkov s plačilnih nalogov v računalniški obliki


### I. SPLOŠNE DOLOČBE


### 1

Pravne osebe lahko predložijo podatke s plačilnih nalogov Agenciji Republike Slovenije za plačilni promet, nadziranje in informiranje (v nadaljnjem besedilu: agencija) na magnetnih medijih (magnetni trak in PC disketa) in prevzamejo podatke s plačilnih nalogov od agencije na magnetnih medijih ali z neposredno računalniško komunikacijo.


### 2

To navodilo predpisuje postopek predložitve in prevzema podatkov s plačilnih nalogov na magnetnih medijih.
Postopek za prevzem podatkov s plačilnih nalogov od agencije z neposredno računalniško komunikacijo pa se določi s pisnim dogovorom med pravno osebo in agencijo.


### 3

Pravne osebe predložijo agenciji podatke s plačilnih nalogov na magnetnem mediju in na zbirnem nalogu za prenos (obr. št. 47)1, vključno s spremnim pismom k magnetnemu mediju, PRILOGA 3 tega navodila.
Podatki s plačilnih nalogov morajo izpolnjevati naslednje pogoje:
– podatki na magnetnem mediju in na priloženem zbirnem nalogu za prenos morajo biti enaki in zapisani v enakem vrstnem redu,
– podatki smejo veljati samo za en datum obdelave,
– plačilni nalogi morajo biti razvrščeni v skladu s prioriteto njihove izvršitve,
– za plačilne naloge ne sme biti zahtevana nujna izvršitev.


### II. OPIS MAGNETNEGA MEDIJA ZA PREDLOŽITEV IN PREVZEM PODATKOV S PLAČILNIH NALOGOV


### 4

Magnetni trak, s pomočjo katerega se posredujejo in prevzemajo podatki s plačilnih nalogov, mora imeti naslednje lastnosti:
– 9-sledni,
– gostota zapisa 1600 BPI,
– obvezna standardna sistemska labela, zapisana v kodi ASCII ali EBCDIC,
– faktor blokiranja 10,
– stavki zapisani v standardu ISO 8859-2 (8 bit) ali EBCDIC kodi,
– podatki nepakirani,
– uporabljene le velike črke.


### 5

Disketa, s pomočjo katere se posredujejo in prevzemajo podatki s plačilnih nalogov, mora imeti naslednje lastnosti:
– velikost 5,25" ali 3,5",
– formatirana v PC DOS formatu,
– ime datoteke s podatki:TKDIS.TXT,
– stavki zapisani v standardu JUS.I.B1.002 (1982),
– stavki ločeni med seboj z znakoma CR (CtrlM, 13dec) in LF (CtrlJ, 10dec),
– datoteka zaključena z znakom SUB (CtrlZ, 26dec),
– uporabljene le velike črke.
Podatki na magnetnem mediju so lahko zapisani tudi v ASCII kodi (7 bit), vendar morajo biti sledeče črke (šumniki) zapisani s kodo:

Č – 5E,      Š – 5B,      Ž – 40,      Ć – 5D,       Đ – 5C (hex)
Č – 94,      Š – 91,      Ž – 64,      Ć – 93,       Đ – 92 (dec).


### III. STRUKTURA STAVKOV NA MAGNETNEM MEDIJU


### A) PREDLOŽITEV MAGNETNEGA MEDIJA AGENCIJI


### 6

Zapis na magnetnem mediju, ki ga pravne osebe predložijo agenciji, vsebuje tri vrste stavkov: naslovnega, zbirnega in individualnega. Stavki se zapišejo po naslednjem vrstnem redu:
naslovni {zbirni {individualni}}.
Naslovnemu stavku sledijo skupine, sestavljene iz enega zbirnega in več individualnih stavkov. Zbirni stavek in pripadajoči individualni stavki sestavljajo logično celoto podatkov:
– na magnetnem mediju sme biti toliko zbirnih stavkov, kolikor je priloženih zbirnih nalogov za prenos, vendar ne več kot 999; v okviru enega zbirnega naloga za prenos sme biti največ 99.999 individualnih nalogov,
– skupni znesek v okviru ene logične celote ne sme presegati 11 desetiških mest, ne glede na to, da je za znesek predvidenih 15 mest,
– številčni podatki morajo biti na magnetnem mediju zapisani z vodilnimi ničlami,
– prazna polja se izpolnijo s presledki (32dec).


### 7

Struktura naslovnega stavka:

– številka računa predlagatelja                  18 znakov
številka organizacijske enote agencije            5 znakov
številka osnovnega računa                         3 znaki
številka namena sredstev ali občine               3 znaki
številka individualne partije računa              7 znakov
– ime predlagatelja                              35 znakov
– kraj predlagatelja                             10 znakov
– datum obdelave (ddmmll)                         6 znakov
– številka magnetnega medija                      3 znaki
– vrsta posla                                     3 znaki
– prazno                                        104 znakov
– tip stavka                                      1 znak
----------------------------------------------------------
SKUPAJ                                          180 znakov
----------------------------------------------------------

Številka računa predlagatelja
(številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine, številka individualne partije računa) je identifikator predlagatelja magnetnega medija.
Datum obdelave
je datum, pod katerim mora agencija obdelati predložene podatke.
Številka magnetnega medija
je oznaka, ki jo predlagatelju magnetnega medija določi organizacijska enota agencije.
Vrsta posla
je oznaka 16.
Tip stavka
je oznaka 0.


### 8

Struktura zbirnega stavka:

– številka računa nalogodajalca                 18 znakov
številka organizacijske enote agencije           5 znakov
številka osnovnega računa                        3 znaki
številka namena sredstev ali občine              3 znaki
številka individualne partije računa             7 znakov
– ime nalogodajalca                             35 znakov
– kraj nalogodajalca                            10 znakov
– skupni znesek (s stotini)                     15 znakov
– število plačilnih nalogov                      5 znakov
– vrsta logične celote                           1 znak
– karakter logične celote                        1 znak
– prazno                                        94 znakov
– tip stavka                                     1 znak
SKUPAJ                                         180 znakov

Številka računa nalogodajalca
(številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine, številka individualne partije računa) je identifikator nalogodajalca. Lahko je enaka številki računa v naslovnem stavku, lahko je drugačna. Predlagatelj magnetnega medija sme na enem magnetnem mediju predložiti zbirne (in pripadajoče individualne) stavke za različne račune iste pravne osebe.
Skupni znesek
je seštevek zneskov individualnih plačilnih nalogov v okviru logične celote podatkov (zbirnega stavka).
Število plačilnih nalogov
je število individualnih plačilnih nalogov v okviru logične celote podatkov (zbirnega stavka).
Vrsta logične celote
– oznaka 1, če vsi individualni plačilni nalogi v okviru zbirnega naloga za prenos vsebujejo vse zahtevane podatke,
– sicer oznaka 0.
Karakter logične celote
– za naloge obremenitve: oznaka 1,
– za naloge odobritve: oznaka 2.
Tip stavka
je oznaka 9.


### 9

Struktura individualnega stavka:

– številka računa prejemnika
plačila/plačnika                                       18 znakov
številka organizacijske enote agencije                  5 znakov
številka osnovnega računa                               3 znaki
številka namena sredstev ali občine                     3 znaki
številka individualne partije računa                    7 znakov
– ime prejemnika plačila/plačnika                      35 znakov
– kraj prejemnika plačila/plačnika                     10 znakov
– prazno                                                1 znak
– sklicevanje na številko (obremenitev)                24 znakov
– namen nakazila                                       36 znakov
– prazno                                                5 znakov
– šifra razčlenjenega prometa                           6 znakov
– znesek (s stotini)                                   13 znakov
– sklicevanje na številko (odobritev)                  24 znakov
– prazno                                                7 znakov
– tip stavka                                            1 znak
----------------------------------------------------------------
SKUPAJ                                                180 znakov
----------------------------------------------------------------

Številka računa prejemnika plačila/plačnika
(številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine, številka individualne partije računa) je identifikator prejemnika plačila oziroma plačnika.
Sklicevanje na številko (obremenitev)
je podatek, ki natančneje identificira poslovno spremembo pri plačniku.
Namen nakazila
je opis namena nakazila.
Šifra
je sestavljena iz oznake za zvezo in iz šifre razčlenjenega prometa.
Znesek
je znesek posameznega plačilnega naloga iz zbirnega naloga za prenos.
Sklicevanje na številko (odobritev)
je podatek, ki natančneje identificira poslovno spremembo pri prejemniku plačila.
Tip stavka
je oznaka 1.


### B) PREVZEM MAGNETNEGA MEDIJA OD AGENCIJE


### 10

Pravne osebe od agencije skupaj z magnetnim medijem dobijo tudi pisno dokumentacijo o prometu in stanju denarnih sredstev na računih ter spremno pismo k magnetnemu mediju.
Pisna dokumentacija vsebuje podatke o skupnem prometu v breme in v dobro ter o stanju denarnih sredstev na posameznem računu pravne osebe ter tudi podatke za posamične prejete naloge odobritev in obremenitev.
Spremno pismo k magnetnemu mediju je PRILOGA 4 tega navodila.


### 11

Na magnetnem mediju, ki ga agencija pripravi za pravne osebe, so podatki oblikovani takole:

------------------------------------------------------------------------------
Zap.
št.    Pozicija    Dolžina   Tip    Opis polja
------------------------------------------------------------------------------
1.     1 - 5       5         N      Številka organizacijske enote agencije
                                    nalogodajalca
2.     6 - 8       3         N      Osnovni račun nalogodajalca
3.     9 - 11      3         N      Namen/občina
4.     12 - 18     7         N      Individualna partija računa nalogodajalca
5.     19 - 20     2         N      Vir informacije
                                    (1 x = obremenitev)
                                    (2 x = odobritev)
6.     21 - 28     8         Date   Datum obdelave v agenciji (DD.MM.LL)
7.     29 - 30     2         Char   Prazno
8.     31 - 65     35        Char   Ime prejemnika magnetnega medija
9.     66          1         N      Način izvršitve plačilnega naloga
10.    67 - 72     6         Date   Datum plačila v banki/pošti (DDMMLL)
11.    73 - 77     5         N      Številka organizacijske enote agencije
                                    prejemnika magnetnega medija
12.    78 - 80     3         N      Osnovni račun prejemnika magnetnega medija
13.    81 - 83     3         N      Namen/občina
14.    84 - 90     7         N      Individualna partija računa prejemnika
                                    magnetnega medija
15.    91 - 105    15        N      Znesek
16.    106 - 107   2         N      Oznaka za zvezo
17.    108 - 109   2         N      Šifra razčlenjenega prometa obremenitve
18.    110 - 111   2         N      Šifra razčlenjenega prometa odobritve
19.    112 - 135   24        Char   Sklicevanje na številko obremenitve
20.    136 - 159   24        Char   Sklicevanje na številko odobritve
21.    160 - 195   36        Char   Namen nakazila
22.    196 - 205   10        Char   Kraj nalogodajalca
23.    206 - 240   35        Char   Ime nalogodajalca
24.    241 - 252   12        N      Številka za reklamacijo
------------------------------------------------------------------------------

Številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine in številka individualne partije računa nalogodajalca
so identifikatorji nalogodajalca, razen v primerih, ko nalogodajalec obremeni račun prejemnika magnetnega medija. Vir informacije je oznaka posameznega plačilnega naloga v breme (1x) oziroma v dobro (2x) računa prejemnika magnetnega medija.
Datum obdelave v agenciji
je datum, pod katerim je agencija obdelala podatke, ki so na magnetnem mediju.
Način izvršitve plačilnega naloga
je številčni podatek, ki pomeni:
1 – plačilo, izvršeno brez dostave originalnega plačilnega naloga,
4 – plačilo, izvršeno z dostavo originalnega plačilnega naloga,
5 – plačilo, izvršeno z zbirnimi avizami po pošti,
9 – plačilo, izvršeno brez dostave originalnega plačilnega naloga, med plačnikom in prejemnikom plačila, ki imata račune pri isti podružnici agencije.
Datum plačila v banki/pošti
je datum, ko je bilo plačilo opravljeno v banki ali na pošti.
Številka organizacijske enote agencije, številka osnovnega računa, številka namena sredstev ali občine in številka individualne partije računa prejemnika magnetnega medija
so identifikatorji prejemnika plačila, razen v primerih, ko nalogodajalec obremeni njegov račun.
Znesek in vsebina podatkov: oznake za zvezo, šifre razčlenjenega prometa (obremenitve in odobritve), sklicevanje na številko (obremenitve in odobritve)
so pojasnjeni pri individualnem stavku v točki A – PREDLOŽITEV MAGNETNEGA MEDIJA AGENCIJI.


### IV. ZAPIS IN KONTROLA PODATKOV NA MAGNETNEM MEDIJU


### 12

Plačilni nalogi, ki jih pravne osebe posredujejo agenciji na magnetnem mediju, morajo vsebovati vse predpisane podatke. Pred predložitvijo magnetnega medija agenciji morajo pravne osebe vse vsebovane podatke preveriti na način in po postopku, opisanem v tem navodilu.


### 13

1. Kontrola številke računa plačnika in številke računa prejemnika plačila:
– kontrola številke organizacijske enote agencije, pri kateri se vodi račun plačnika oziroma prejemnika plačila, se opravi glede na obstoj številke v Pregledu oznak za organizacijske enote agencije 2,
– kontrola številke osnovnega računa plačnika oziroma prejemnika plačila se opravi glede na obstoj osnovnega računa v Planu računov za opravljanje plačilnega prometa prek agencije2,
– kontrola številke namena sredstev pri osnovnih računih razreda 7 plana računov se opravi glede na obstoj številke za namen sredstev v Pregledu oznak za namen sredstev2,
– kontrola številke za občine pri osnovnih računih 840, 842, 843 in 844 se opravi glede na obstoj številke za občino v Pregledu oznak za občine 2 (pri osnovnih računih razredov 6, 7, 8 plana računov, za katere ni predvidena oznaka za namen sredstev oziroma oznaka za občino, se vsa tri mesta v tem polju izpolnijo z ničlami),
– kontrola kontrolne številke individualne partije plačnika oziroma prejemnika plačila se opravi po modulu 11 takole:
– posamezne številke individualne partije z leve proti desni se pomnožijo z ponderji 0, 1, 2, 3, 4 in 5,
– seštevek zmnožkov se deli z 11,
– ostanek pri deljenju se odšteje od 11,
– dobljeni rezultat je kontrolna številka individualne partije, če je 1 < / = k < / = 9, kontrolna številka je 0, če je k=11, ni kontrolna številka individualne partije, če je k=10.
2. Podatek Šifra se kontrolira glede na obstoj oznake za zvezo in šifre razčlenjenega prometa v Pregledu tipskih besedil, ki se izpišejo na podlagi podatka Šifra, in v Pregledu osnovnih računov in šifer razčlenjenega prometa.
Pregled tipskih besedil, ki se izpišejo na podlagi podatka Šifra je PRILOGA 1 tega navodila. Pregled osnovnih računov in šifer razčlenjenega prometa je PRILOGA 2 tega navodila.
Če se plačilni nalog ne more označiti z eno izmed predpisanih oznak za zvezo, se na 1. in 2. mesto v podatku Šifra vpiše oznaka za zvezo 88. Če se osnovni račun ne šifrira po šifrah razčlenjenega prometa, se 3., 4., 5. in 6. mesto v podatku Šifra izpolnijo z ničlami.
3. Kontrola podatkov v sklicevanju na številko obremenitve oziroma odobritve se opravi na način, predpisan za izbrano številko modela v Pregledu in vsebini osnovnih modelov za sklicevanje na številko obremenitve in odobritve ter v pojasnilih za njihovo uporabo 3.
Podatki v sklicevanju na številko obremenitve in odobritve se ne kontrolirajo samo v primeru, če je izbrana številka modela 00.
4. Seštevek zneskov z vseh posameznih plačilnih nalogov na magnetnem mediju mora ustrezati znesku pod “skupaj tolarjev po zbirnem nalogu” v zbirnem nalogu za prenos.
Pravne osebe lahko opravijo kontrolo podatkov na magnetnem mediju s svojim računalniškim programom ali pa z računalniškim programom, ki ga dobijo v organizacijskih enotah agencije.


### V. PREHODNE IN KONČNE DOLOČBE


### 14

Pravne osebe, ki imajo odprte žiro račune v podružnicah agencije z UNISYS računalniškimi sistemi, do prehoda vseh podružnic agencije na obdelavo podatkov plačilnega prometa na enakih računalniških sistemih, lahko agenciji predlagajo podatke s plačilnih nalogov v skladu s tem navodilom, le na PC disketah.
Agencija bo sprejemala oziroma posredovala podatke pravnim osebam v podružnicah agencije z UNISYS računalniškimi sistemi tudi v obliki in vsebini, ki je veljala do začetka veljavnosti tega navodila, vendar najdalj do 31. 12. 1995.


### 15

Z dnem, ko začne veljati to navodilo, prenehajo veljati določbe PRILOGE 3 navodila za sprejem, kontrolo pravilnosti in izvrševanje plačilnih nalogov v plačilnem prometu v Službi družbenega knjigovodstva (Glasnik SDK, št. 16/86, s spremembami in dopolnitvami).


### 16

To navodilo začne veljati petnajsti dan po objavi v Uradnem listu Republike Slovenije.

Št. 020-15/95

Ljubljana, dne 13. februarja 1995.

Romana Logar l. r.
Generalna direktorica

AGENCIJA REPUBLIKE SLOVENIJE
ZA PLAČILNI PROMET, NADZIRANJE                          PRILOGA 1
IN INFORMIRANJE

   PREGLED TIPSKIH BESEDIL, KI SE IZPIŠEJO NA PODLAGI PODATKA
                             "ŠIFRA"
        (oznaka za zvezo in šifra razčlenjenega prometa)

-----------------------------------------------------------------
"Šifra"       Besedilo na zbirnem sporočilu o obremenitvi oziroma
              na zbirnem sporočilu o odobritvi
-----------------------------------------------------------------
   1                                  2
-----------------------------------------------------------------

01 Plačilo po fakturi

01  -  -      Plačilo po fakturi

01 30 11      Plač. fakt. za material, blago, storitve

01 31  -      Izpl. prebival. za proizvode in stor.

01 70 11      Plačana faktura - situacija za inv.


02 Prenos predujma

02  -  -      Prenos predujma

02 30 11      Plač. pred. za material, blago, storit.

02 70 11      Plačan predujem za investicije


03 Vnovčenje čeka

03  -  -      Vnovčenje čeka

03 30  -      Vnovč. čeka za mat., blago., storitve

03 30 11      Vnovč. čeka za mat., blago., storitve

03 40  -      Vnovčenje čeka za plače

03 70 11      Vnovčenje čeka za investicije

03 71  -      Vnovč. čeka za plače iz investicij


04 Plačilo obveznosti, krite z garancijo

04  -  -      Plačilo obveznosti, krite z garancijo

04 30 11      Pl. fak. za mat., blag. stor., krite z gar.

04 70 11      Pl. fak. -sit. za invest., krite z gar.


05 Promet z vrednostnimi papirji

05  -  -      Promet z vrednostnimi papirji

05 30 11      Izpl. menice za mat. blago, storitve

05 30  -      Izpl. menice za mat. blago, storitve

05 30 18      Izpl. menice za mat. blago, storitve

05 70 11      Izplačilo menice za investicije

05 70  -      Izplačilo menice za investicije

05 70 18      Izplačilo menice za investicije

05  - 11      Izpl. po pogodbi o eskontu menice

05  - 18      Izpl. po pogodbi o reeskontu menice

05 98 11      Izpl. po pogodbi o eskontu menice

05 98 18      Izpl. po pogodbi o reeskontu menice

05 99 18      Izpl. menice po blagovnem kreditu


06 Vplačilo dnevnega iztržka

06  -  -      Vplačilo dnev. iztržka-čeki občanov

06  - 10      Vplačilo dnev. iztržka-čeki občanov

06  - 11      Vplačilo dnev. iztržka-čeki občanov

06  - 19      Vplačilo dnev. iztržka-čeki občanov


07 Naložbe v druge pravne osebe

07  -  -      Naložbe v druge pravne osebe

07 98 11      Prenos prihodka-dohodka

07  - 11      Prenos prihodka-dohodka

07 99 19      Nal. v druge pr. os. brez vrač. obvezn.

07 98 19      Naložbe v druge pravne osebe

07 98 18      Naložbe v druge pravne osebe

07 98  -      Naložbe v druge pravne osebe

07  - 18      Naložbe v druge pravne osebe

07 99 18      Naložbe v druge pravne osebe


08 Pačilo davkov, prispevkov in drugih davščin

08  -  -      plačilo davkov, prispevkov in dr. dav.

08 30  -      Plačilo carine in dr. dav. v br. stroš.

08 38  -      Plačilo davkov, prispevkov idr.

08 51  -      Plačilo prometnega davka idr.

08 70  -      Plačilo carine in dr. dav. za inv.


09 Plačilo iz naslova zavarovanja

09  -  -      Plačilo iz naslova zavarovanja

09 35 11      Plačana zavarovalna premija

09  - 11      Plačilo zav. premij iz razporeda

09 35  -      Plačana zavarovalna premija

09 30 11      Plač. odškod. za obratna sredstva

09 30 19      Plač. odškod. za obratna sredstva


10 Prenosi sredstev družbenopolitičnih skupnost

10  -  -      Prenosi sredstev družbenop. skup.

10 84 11      Prenos sredstev izvajalcem storitev

10 84 12      Prenos sredstev za določene namene


11 Plačilo pred prejemom fakture

11  -  -      Plačilo pred prejemom fakture

11 30 11      Plač. za mat. blag. stor. pred prej. fak.

11 70 11      Plačilo za invest. brez fakture


12 Plačilo odtegljajev pri izplačilu plač

12  -  -      Plačilo odteglj. pri izplačilu plač

12 40  -      Odplačilo posojil

12 40 15      Plačila samoprisp. in članarin

12 40 17      Plačilo drugih odtegljajev

12 40 18      Odplačilo posojil


14 Plačilo zapadle obveznosti iz sredstev garanta

14  -  -      Plačilo zapadl. obv. iz sredst. garanta

14  - 11      Plačilo faktur iz sredstev garanta

14 98 11      Plačilo faktur iz sredstev garanta

14 30 13      Plač. za mat. blag. stor. iz sredst. gar.

14 70 13      Plač. za invest. iz sredstev garanta

14 93  -      Plačana obveznost garantu

14 93 18      Plačana obveznost garantu


15 Vnovčenje zapadle menice iz sredstev avalista

15  -  -      Vnovčenje zapadle men. iz sred. aval.

15  - 13      Prenos sredstev danega avala

15 98  -      Prenos sredstev za uporabljeni aval


16 Vplačilo občanov in plačilo za račun občanov

16  -  -      Vplačila in plačilo za račun občanov

16  - 10      Plačilo obveznosti za rač. občanov

16 40  -      Izplačilo plač prek bank-hranilnic

16 43  -      Izplačilo pokojnin prek bank-hranil.

16 32  -      Prenos sred. za nadomestila občanov

16  - 11      Plačilo obveznosti za račun občanov

16  - 19      Plačilo obveznosti za račun občanov

16 32 11      Prenos sred. za nadomestila občanov

16 32 19      Prenos sred. za nadomestila občanov

16 40 11      Izplačila plač prek bank-hranilnic

16 40 19      Izplačila plač prek bank-hranilnic

16 43 11      Izplačilo pokojnin prek bank-hranil.

16 43 19      Izplačilo pokojnin prek bank-hranil.


20 Obresti

20  -  -      Obresti

20 35  -      Obresti, plačane banki

20 35 11      Obresti

20 99 11      Obresti

20 99 19      Obresti


25 Plačilo z indosamentom

25  -  -      Plačilo z indosamentom

25 30 14      Pl. mat. blag., stor. z indosir. menice

25 70 14      Plačane invest. z indosir. menice


40 Nakazilo tolarske protivrednosti *

40  -  -

40  - 11

40  - 19

40 30 11

40 30 19

40 32 19

40 99 19

------------------
* Pravna oseba v zbirnem sporočilu obremenitve oziroma odobritve
dobi izpisano enako besedilo, kot je bilo vpisano v namenu
nakazila na originalnem plačilnem nalogu.


50 Plačilo iz naslova posojila

50  -  -      Plačilo iz naslova posojila

50  - 13      Prenos sredstev posoj. od banke

50 98 13      Prenos sredstev posojila od pr. os.

50 93  -      Odplačilo posojila banki

50 93 18      Odplačilo posojila pravnih oseb

50 99  -      Vrnjena neupor. sred. iz prim. emisije

50 99 18      Odplačilo posojil. za osn. sred. pr. os.

50  - 19      Prenos sredstev iz primarne emisije

50 99 19      Posojila iz sredstev primarne emisije


60 Prijava vplačil

60  -  -      Obračun vplačil hr. vlog, nakaznic idr.


65 Prijava izplačil

65  -  -      Obrač. izpl. hr. vl. nakaz. ček. tek. rač.


70 Plačilo iz naslova izvršljivih sklepov in odločb

70  -  -      Plačilo po izvršljivih odločbah

70 30 11      Plačilo fakture po izvršljivih odloč.

70 70 11      Plač. za invest. po izvršljivih odloč.

70 30  -      Plačilo fakture po izvršljivih odloč.

70 99 19      Plačilo po izvršljivih odločbah

70  - 19      Plačilo po izvršljivih odločbah


72 Plačilo v solidarne in humanitarne namene

72  -  -      Plačilo v solidar. in human. namene

72 99  19     Plačilo v solidar. in human. namene

72  -  19     Plačilo v solidar. in human. namene


76 Razporeditev sredstev s prehodnih računov

76  -  -      Razpored. sredst. s prehodnih računov

76  - 11      Razpored. sredst. s prehodnih računov


77 Prenos sredstev v depozit

77  -  -      Prenos sredstev v depozit

77 98 18      Prenos sredstev v depozit

77 98  -      Prenos sredstev v depozit


78 Plačilo iz depozita

78  -  -      Plačilo iz depozita

78 30 11      Plačilo po fakt. za mat. blag. storitve

78 35 19      Plačilo obresti, provizije idr.

78 93  -      Plačilo posojila iz depozita

78  - 11      Plačilo po fakt. za mat. blag. storitve

78  - 19      Plačilo obresti, provizije idt.


81 Prenos sredstev za plačilo po pooblastilu pravne osebe

81  -  -      Prenos sredstev za plač. po poob. pr. o.

81 99 19      Prenos sredstev po pogodbi

81  - 19      Prenos sredstev po pogodbi

81 99  -      Prenos sredstev po pogodbi


82 Plačilo po pooblastilu pravne osebe

82  -  -      Plačilo po pooblastilu pravne osebe

82  - 11      Plač. fakt. za material., blago, stor.

82 70 11      Plačilo faktur-situacij za invest.

82 30 11      Plač. fakt. za material., blago, stor.


83 Plačilo provizije

83  -  -      Plačilo provizije

83  - 11      Plačilo provizije

83 30 11      Plačilo provizije

83 30  -      Plačilo provizije

83 35 11      Plačilo provizije

83 35  -      Plačilo provizije


85 Prenos sredstev med bankami in njihovimi deli

85  -  -      Pren. sred. med bankami in njih. deli

85 99 19      Prenos sredstev banke

85 30 11      Prenos sredstev banke

85 35 11      Prenos sredstev banke


87 Prenos sredstev med računi, odprtimi pri Agenciji in pri
   bankah *

-------------------
* Pravna oseba v zbirnem sporočilu obremenitve oziroma odobritve
dobi izpisano enako besedilo, kot je bilo vpisano v namenu
nakazila na originalnem plačilnem nalogu.


90 Prenos sredstev na račun pravne osebe

90  -  -      Prenos sred. na rač. pr. os.

-----------------------------------------------------------------

AGENCIJA REPUBLIKE SLOVENIJE                            PRILOGA 2
ZA PLAČILNI PROMET, NADZIRANJE
IN INFORMIRANJE

            PREGLED OSNOVNIH RAČUNOV IN ŠIFER RAZČLENJENEGA PROMETA

---------------------------------------------------------------------------------------------
                              ŠIFRE
---------------------------------------------------------------------------------------------
OSNOVNI         Prejemki              .                       Izdatki
RAČUN                                 .
        10 11 12 13 14 15 16 17 18 19 . 30 31 32 35 38 40 43 51 70 71 72 82 84 93 96 97 98 99
---------------------------------------------------------------------------------------------
601      X  X  X  X  X  X  X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

603      X  X  X  X  X  X     X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X     X  X  X

604      X  X  X  X  X  X  X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

608      X  X  X  X  X  X  X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

609      X  X  X  X  X  X     X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X     X  X  X

611      X  X  X  X  X           X  X    X     X  X  X  X  X  X  X  X  X  X     X     X  X  X

620      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

621      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

625      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

626      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

627      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

628      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

630         X  X  X  X        X  X  X    X  X  X  X  X  X  X     X  X  X  X  X  X     X  X  X

637      X  X  X  X  X  X     X  X  X    X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X

638      X  X  X  X  X  X     X  X  X    X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X

639      X  X  X  X  X  X     X  X  X    X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X  X

645      X  X  X  X  X  X     X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X     X  X  X

649         X  X  X  X  X     X  X  X    X  X  X  X  X  X  X     X  X  X  X  X  X     X  X  X

650      X  X  X  X  X        X  X  X    X  X  X  X  X  X  X  X  X     X  X  X  X     X  X  X

651      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X           X  X  X  X  X  X

652         X  X  X  X  X     X  X  X    X  X  X  X  X  X  X     X  X  X  X  X  X     X  X  X

654         X  X  X  X        X  X  X    X  X  X  X  X  X  X     X  X  X  X  X  X     X  X  X

655         X  X  X  X        X  X  X    X  X  X  X  X  X  X     X  X  X  X  X  X     X  X  X

656      X     X  X  X  X  X     X  X    X  X  X  X  X  X  X  X              X  X  X  X  X  X

664         X     X  X     X  X  X  X    X  X  X  X  X  X  X     X  X  X  X     X  X  X  X  X

665         X     X  X     X  X  X  X    X  X  X  X  X  X  X     X  X  X  X     X  X  X  X  X

675                                 X                   X  X     X  X  X                    X

678      X  X  X  X  X  X  X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

679      X  X  X  X  X  X  X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

690                                 X                   X  X     X  X  X                    X

696                                 X                            X  X  X                    X

697                                 X                            X  X  X                    X

740         X           X     X  X  X    X  X  X  X  X     X                          X  X  X

742         X  X  X  X     X  X  X  X    X  X  X  X  X                          X  X  X  X  X

743         X           X     X  X  X    X  X  X  X  X     X                          X  X  X

748                                 X                                                       X

762                              X  X                            X  X  X                 X  X

763                              X  X                            X  X  X                 X  X

764      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

765      X  X  X  X  X     X  X  X  X    X  X  X  X  X  X  X  X  X  X  X  X     X  X  X  X  X

789                           X  X  X    X  X  X  X  X     X                             X  X
---------------------------------------------------------------------------------------------

PRILOGA 3

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

PRILOGA 4
AGENCIJA REPUBLIKE SLOVENIJE
ZA PLAČILNI PROMET, NADZIRANJE
IN INFORMIRANJE

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

1 Oblika, vsebina in uporaba zbirnega naloga za prenos so določene v Navodilu o obliki, vsebini in uporabi obrazcev za opravljanje plačilnega prometa prek agencije Republike Slovenije za plačilni promet, nadziranje in informiranje (Uradni list RS, št. 9/95).
2 Pregled oznak za organizacijske enote agencije, Plan računov za opravljanje plačilnega prometa prek agencije, Pregled oznak za namen sredstev in Pregled oznak za občine, pravne osebe dobijo pri organizacijski enoti agencije, ki vodi njihov račun.
3 Pregled in vsebina osnovnih modelov za sklicevanje na številko obremenitve in odobritve ter pojasnila za njihovo uporabo je PRILOGA 4 Navodila o obliki, vsebini in uporabi obrazcev za opravljanje plačilnega prometa prek agencije Republike Slovenije za plačilni promet, nadziranje in informiranje (Uradni list RS, št. 9/95).
