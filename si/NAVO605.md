---
kratica: NAVO605
naziv: "Navodilo za predložitev in prevzem podatkov s plačilnih navodil in izpiska o prometu in stanju v računalniški obliki"
vrsta: "navodilo"
datum: 2002-06-28
sop: 2002-01-2771
organ: ""
zbirka: "Neuradna prečiščena besedila"
status: "Neznano"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=2002-01-2771"
---

# Navodilo za predložitev in prevzem podatkov s plačilnih navodil in izpiska o prometu in stanju v računalniški obliki

Na podlagi 2., 3. in 5. točke prvega odstavka 74. člena zakona o plačilnem prometu (Uradni list RS, št. 30/02) izdaja minister za finance


## N A V O D I L O
za predložitev in prevzem podatkov s plačilnih navodil  in izpiska o prometu in stanju v računalniški obliki


### I. SPLOŠNE DOLOČBE


### 1. člen

To navodilo določa način predložitve in prevzema podatkov s plačilnih navodil in izpiska o prometu in stanju v računalniški obliki.


### 2. člen

Uporabljeni pojmi v tem navodilu imajo naslednji pomen:

–  Proračunski uporabnik je neposredni in posredni uporabnik državnega in občinskega proračuna, določen z odredbo o določitvi neposrednih in posrednih uporabnikov državnega in občinskih proračunov (Uradni list RS, št. 97/01);

–  Plačilno navodilo (PNO) je tolarski nalog za prenos, obrazec št. 40;

–  Zbirno plačilno navodilo, je več PNO, predloženih v računalniški obliki (na disketi ali po elektronski pošti);

–  Devizno plačilno navodilo za odliv (DPNO 70) je naročilo proračunskega uporabnika Upravi Republike Slovenije za javna plačila (v nadaljevanju: UJP) za negotovinsko poravnavo obveznosti v tujino ali do nerezidentov, v domači ali tuji valuti, oziroma naročilo proračunskega uporabnika UJP za nakazilo sredstev za dvig gotovine;

–  Devizno plačilno navodilo za priliv (DPNP 60), je obvestilo UJP proračunskemu uporabniku o prilivu iz tujine ali potrdilo o izvedbi pologa tuje gotovine s strani proračunskega uporabnika;

–  Elektronska pošta (v nadaljevanju: e_pošta) je način predložitve podatkov s plačilnih navodil in način sprejemanja podatkov o izvršenih plačilnih transakcijah prek neposredne računalniške povezave med proračunskim uporabnikom in UJP.

–  Račun pomeni enotni zakladniški račun (v nadaljevanju: EZR) ali namenski devizni račun, ki je številčen v strukturi transakcijskega računa in odprt pri Banki Slovenije ter prek katerega potekajo vsa plačila in izplačila javnofinančnih sredstev.

–  Podračun pomeni podračune proračunskih uporabnikov, ki so številčeni v strukturi transakcijskega računa in odprti pri UJP.

–  Izpisek je izpisek plačilnih transakcij računa ali podračuna proračunskega uporabnika in izpisek stanja na računu ali podračunu.

–  Odredbodajalec je proračunski uporabnik – nalogodajalec.


### 3. člen

Proračunski uporabnik predloži UJP podatke s plačilnih navodil in podatke z deviznih plačilnih navodil za odlive v računalniški obliki in od UJP prevzame podatke izpiska v računalniški obliki.


### 4. člen

To navodilo določa strukturi računalniških zapisov podatkov s plačilnega navodila in z deviznega plačilnega navodila za odliv, ki ju proračunski uporabnik predloži UJP v izvršitev, ter strukturo računalniškega zapisa podatkov o opravljenih plačilnih transakcijah prek podračuna proračunskega uporabnika ali računa v obliki tolarskega in deviznega izpiska, ki ju UJP pošlje proračunskemu uporabniku.
Način predložitve podatkov s plačilnih navodil in z deviznih plačilnih navodil za odliv ter način pošiljanja izpiskov dogovorita proračunski uporabnik in UJP.


### 5. člen

Proračunski uporabnik lahko predloži UJP podatke s plačilnih navodil in z deviznih plačilnih navodil za odliv na disketi ali po e_pošti. Če so podatki predloženi na disketi, mora proračunski uporabnik skupaj z disketo UJP predložiti tudi izpisane podatke na papirju v obliki zbirnega plačilnega navodila. Vsebina izpisa zbirnega plačilnega navodila na papirju mora biti enaka vsebini podatkov na predloženi disketi, kar s podpisom potrdi pooblaščena oseba proračunskega uporabnika.
Za predložitev podatkov UJP po e_pošti veljajo splošni predpisi, ki urejajo elektronsko poslovanje. Podrobnosti in morebitne posebnosti pisno uredita proračunski uporabnik in UJP.
Proračunski uporabnik lahko UJP na predpisan način predloži tudi nujna plačilna navodila in nujna devizna plačilna navodila za odliv. V tem primeru morajo biti ta plačilna navodila predložena ločeno od rednih plačilnih navodil - na ločeni disketi oziroma v ločenem paketu e_pošte.


### II. LASTNOSTI DISKETE IN PRAVILA OBLIKOVANJA PODATKOV NA DISKETI


### 6. člen

Disketa, na kateri se predložijo podatki plačilnih navodil, podatki deviznih plačilnih navodil za odliv oziroma podatki izpiska, mora imeti naslednje lastnosti:
- velikost 3,5",
- formatirana v PC DOS formatu.
Podatki na disketi morajo biti oblikovani po pravilih:
1. ime datoteke s podatki:
- TKDIS.TXT za predložitev podatkov tolarskih plačilnih navodil,
- DPNO.TXT za predložitev podatkov deviznih plačilnih navodil za odlive,
- TKIZP.TXT za prevzem podatkov izpiska o stanju na računu ali podračunu,
- TKDIS.TXT za prevzem podatkov izpiska o transakcijah na računu ali podračunu,
2. stavki na datoteki morajo biti:
- zapisani v standardu JUS. I. B1. 002 (1982),
- med seboj ločeni z znakoma CR (CtrlM, 13dec) in LF (CtrlJ, 10dec),
- zapisani le z velikimi črkami,
3. datoteka mora biti zaključena z znakom SUB (CtrlZ, 26dec).
Podatki na disketi so lahko zapisani tudi v ASCII kodi (7 bit), vendar morajo biti sledeče črke (šumniki) zapisani s kodo:
Č-5E, Š-5B, Ž-40, Ć-5D, Đ-5C (hex)
Č-94, Š-91, Ž-64, Ć-93, Đ-92 (dec).
Za oblikovanje posameznih podatkov stavkov veljajo splošna pravila:
- številčni podatki so zapisani z vodilnimi ničlami in desno poravnani,
- številčni podatki so zapisani brez decimalne vejice, zadnja dva znaka predstavljata decimalni mesti,
- negativen predznak je prisoten na prvem mestu numeričnega polja in dovoljen le v poljih izpiska 'prejšnje stanje' in 'novo stanje',
- prazni podatki se napolnijo s presledki,
- alfanumerični podatki so levo poravnani in do dolžine polja zapolnjeni s presledki in
- transakcijski račun zapolnjuje prvih 15 mest (15 številk) in je do dolžine polja zapolnjen s presledki ali oznako tuje valute.


### III. STRUKTURE STAVKOV RAČUNALNIŠKEGA ZAPISA PODATKOV


### a) Struktura stavkov za predložitev podatkov tolarskih plačilnih navodil


### 7. člen

Računalniški zapis, za predložitev podatkov tolarskih plačilnih navodil vsebuje tri vrste stavkov: naslovnega, zbirnega in individualnega.
Stavki se zapišejo na datoteko po naslednjem vrstnem redu:

naslovni  (zbirni (individualni)(.

Naslovnemu stavku sledijo skupine, sestavljene iz enega zbirnega in več individualnih stavkov. Zbirni stavek in pripadajoči individualni stavki sestavljajo logično celoto podatkov, za katero veljajo pravila:
- v elektronskem zapisu sme biti toliko zbirnih stavkov, kolikor je priloženih zbirnih plačilnih navodil, vendar ne več kot 999,
- v okviru enega zbirnega plačilnega navodila sme biti največ 9.999 individualnih plačilnih navodil,
- tevilo znakov skupnega zneska v okviru ene logične celote na sme presegati 15 mest.


### 8. člen

Struktura naslovnega stavka:


### 9. člen

Struktura zbirnega stavka:


### 10. člen

Struktura individualnega stavka:


### b) Struktura stavkov za predložitev podatkov deviznih plačilnih navodil za odliv


### 11. člen

Datoteka za predložitev podatkov deviznih plačilnih navodil za odliv, ki jo proračunski uporabnik predloži UJP, vsebuje štiri vrste stavkov: odredbodajalec, plačilo, statistika in kritje.
Stavki se zapišejo na datoteko s podatki (DPNO.TXT) po naslednjem vrstnem redu:

odredbodajalec {plačilo (statistika,[kritje])}

Stavku ‘odredbodajalec’ sledijo skupine, sestavljene iz enega stavka ‘plačilo’ in več stavkov ‘statistika’ ter  nič ali več stavkov ‘kritje’. Stavek ‘plačilo’ in pripadajoči stavki ‘statistika’ in ‘kritje’ sestavljajo logično celoto podatkov, za katero veljajo pravila:
- v okviru enega stavka ‘plačilo’ sme biti največ 99 stavkov ‘statistika’ in največ 99 stavkov ‘kritje’,
- številčni podatki morajo biti zapisani z vodilnimi ničlami,
- prazna polja se izpolnijo s presledki (32dec).


### 12. člen

Struktura stavka odredbodajalec


### 13. člen

Struktura stavka plačilo


### 14. člen

Struktura stavka statistika:


### 15. člen

Struktura stavka kritje


### c)  Struktura stavkov za prevzem tolarskega in deviznega izpiska od UJP


### 16. člen

Proračunski uporabnik od UJP prejme tolarski izpisek stanja podračuna in devizni izpisek stanja podračuna in računa (podatke o prejšnjem stanju, skupnem dnevnem prometu v breme in skupnem dnevnem prometu v dobro ter o končnem stanju sredstev na računu) in tudi podatke za posamične prejete odobritve in izvršene obremenitve – posamične plačilne transakcije) na disketi ali po e-pošti.
Če proračunski uporabnik prevzame izpisek na disketi, dobi skupaj z disketo tudi pisno obvestilo, v katerem so navedeni morebitni tisti popravki podatkov na predloženih plačilnih navodilih na disketi, ki jih UJP sme in jih je popravil.
UJP na enak način zagotovi proračunskim uporabnikom obvestilo o tovrstnih popravkih na plačilnih navodilih predloženih UJP po e_pošti.


### 17. člen

Podatke o prejšnjem stanju, skupnem dnevnem prometu v breme in skupnem dnevnem prometu v dobro ter o novem (končnem) stanju v obliki računalniškega zapisa izpiska, na disketi ali z e_pošto, UJP pripravi v datoteki TKIZP.TXT v naslednji obliki:

Oblika priprave podatkov


### 18. člen

Struktura stavka v računalniškem zapisu podatkov o posameznih plačilnih transakcijah v domačem plačilnem prometu, ki ga UJP pripravi za proračunske uporabnike (datoteka TKDIS.TXT):


### 19. člen

Struktura stavka v računalniškem zapisu podatkov o posameznih plačilnih transakcijah deviznih plačilnih navodil za odlive in prilive, ki ga UJP pripravi za proračunske uporabnike (TKDIS.TXT):


### IV. ZAPIS IN KONTROLA PODATKOV NA MAGNETNEM MEDIJU


### 20. člen

Plačilna navodila in devizna plačilna navodila za odlive, ki jih proračunski uporabnik posreduje UJP v računalniški obliki, morajo vsebovati vse predpisane podatke. Pred predložitvijo/pošiljanjem podatkov UJP mora proračunski uporabnik vse vsebovane podatke preveriti po določbah tega navodila.


### 21. člen

Kontrola številke podračuna plačnika in številke transakcijskega računa ali podračuna prejemnika plačila se opravi v skladu z izračunom kontrolne številke po poenostavljenem modelu ISO 7064, MOD  97-10. Primer izračuna kontrolne številke je v Prilogi 1 tega navodila.
Kontrola  podatkov v sklicevanju na številko obremenitve oziroma odobritve se opravi na način, predpisan za izbrano številko modela v Pregledu in vsebini osnovnih modelov za sklicevanje na številko obremenitve in odobritve ter v pojasnilih za njihovo uporabo, ki je Priloga 2 tega navodila in je sestavni del tega navodila.
Podatki v sklicevanju na številko obremenitve in odobritve se ne kontrolirajo, če je izbrana številka modela 00.


### V. PREHODNA IN KONČNA DOLOČBA


### 22. člen

Do vzpostavitve računalniške podpore v UJP se devizna plačilna navodila za odliv predlagajo v papirni obliki (obrazec DPNO 70).


### 23. člen

To navodilo začne veljati naslednji dan po objavi v Uradnem listu Republike Slovenije, uporablja pa se od 29. junija 2002.

Št. 431-19/02

Ljubljana, dne 19. junija 2002.

mag. Anton Rop l. r.
Minister
za finance

Priloga 1: Izračun kontrolne številke transakcijskega računa oziroma podračuna enotnega zakladniškega računa po poenostavljenem postopku za ISO 7064, MOD 97- 10

Priloga 2: Pregled in vsebina osnovnih modelov za sklicevanje na številko obremenitve in odobritve ter pojasnila za njihovo uporabo
