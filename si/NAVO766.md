---
kratica: NAVO766
naziv: "Navodilo za elektronsko posredovanje poročila o kapitalu in kapitalski ustreznosti (obrazcev KAP)"
vrsta: "navodilo"
datum: 2005-04-21
sop: 2005-01-1441
organ: "Banka Slovenije"
zbirka: "Drugi splošni in posamični akti"
status: "Neveljaven predpis"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=2005-01-1441"
---

# Navodilo za elektronsko posredovanje poročila o kapitalu in kapitalski ustreznosti (obrazcev KAP)

Na podlagi tretjega odstavka 29. člena Zakona o Banki Slovenije (Uradni list RS, št. 58/02 in 85/02) in Sklepa o kapitalski ustreznosti bank in hranilnic (Uradni list RS, št. 24/02, 85/02, 22/03, 36/04, 68/04, 103/04 in 124/04) izdaja guverner Banke Slovenije


## N A V O D I L O
za elektronsko posredovanje poročila o kapitalu in kapitalski ustreznosti (obrazcev KAP)


### I. NAMEN NAVODILA

1. To navodilo predpisuje obliko in način izpolnjevanja ter elektronskega posredovanja poročila o kapitalu in kapitalski ustreznosti iz 49. točke Sklepa o kapitalski ustreznosti bank in hranilnic (v nadaljevanju: sklep), in sicer tisti del obrazcev KAP, ki jih je banka oziroma hranilnica (v nadaljevanju: banka) dolžna predlagati po stanju na zadnji dan vsakega četrtletja.
2. Obliko in način elektronskega posredovanja obrazca KAP-8, ki ga je banka dolžna predlagati po stanju na zadnji dan vsakega meseca, ureja posebno navodilo.
3. V skladu z obveznostjo poročanja iz 1. točke tega navodila mora banka predložiti naslednje obrazce:
– KAP – Kapital banke,
– KAP – 1 – Specifikacija temeljnega kapitala,
– KAP – 2 – Specifikacija dodatnega kapitala I,
– KAP – 3 – Izračun kapitalskih zahtev in količnika kapitalske ustreznosti banke,
– KAP – 4 – Izračun tveganju prilagojene aktive,
– KAP – 5 – Izračun tveganju prilagojene zunajbilančne aktive,
– KAP – 6 – Izračun tveganju prilagojenih postavk za izvedene finančne instrumente (metoda tekoče izpostavljenosti),
– KAP – 7 – Izračun tveganju prilagojene postavke za izvedene finančne instrumente (metoda originalne zapadlosti),
– KAP – 9/1 – Posli trgovanja banke (postavke trgovanja),
– KAP – 9/2 – Posli trgovanja banke (celotno poslovanje).
Banka, ki je v skladu z 9. točko sklepa dolžna izračunavati in izpolnjevati tudi kapitalske zahteve za tržna tveganja, dodatno izpolni še naslednje obrazce:
– KAP – trg – Kapital banke (namesto obrazca KAP),
– KAP – trg 1 – Izračun uporabljenega ustreznega dodatnega kapitala II,
– KAP – trg – 2 – Izračun kapitalskih zahtev in količnika kapitalske ustreznosti banke (namesto KAP – 3).


### II. OBLIKA IN NAČIN IZPOLNJEVANJA TER ELEKTRONSKEGA POSREDOVANJA OBRAZCEV KAP

4. Vsebina in zapis podatkov
Vsebina in struktura obrazcev KAP v elektronski obliki ostaja enaka papirnati obliki. Elektronski obrazci KAP, kamor banka vnese poročane podatke, se nahajajo v datoteki BSKAP.XLS (verzija Excel 97 SR-2). Vsi poročani podatki se vpisujejo v tisoč SIT. Izjema so le podatki iz obrazca KAP – 3 oziroma KAP – trg – 2, kamor banka vnese:
– v polje »kapitalske zahteve za kreditno tveganje« oziroma »kapitalske zahteve za valutna tveganja« odstotek zahtevane kapitalske ustreznosti, ki jo mora izpolnjevati (minimalen predpisani odstotek oziroma s strani Banke Slovenije določen višji odstotek kapitalske ustreznosti), in
– v polje »tržnim tveganjem prilagojene postavke« faktor 12,5 (recipročna vrednost od 8%) oziroma drug ustrezen faktor v primeru višjega zahtevanega količnika kapitalske ustreznosti.
Polje »faktor za določanje skupne kapitalske zahteve za tržna tveganja« izpolni banka le v primeru, ko ima s strani Banke Slovenije določen višji količnik kapitalske ustreznosti od minimalno zahtevanega, v nasprotnem primeru banka pusti polje prazno.
Banka mora po dokončnem vnosu podatkov v datoteko BSKAP.XLS, to datoteko zapreti, pri čemer se samodejno ustvari datoteka s podatki (BSKAP_PODATKI.TXT). Po njenem kodiranju banka posreduje datoteko po elektronski pošti v skladu z navodili, podanimi v nadaljevanju.
5. Način pošiljanja
Banka mora datoteko s podatki (BSKAP_PODATKI.TXT) poslati po elektronski pošti. V enem sporočilu se lahko nahaja ena datoteka s podatki za eno obdobje.
5.1. Naslov za dostavljanje podatkov
KAP@BSI.SI

5.2. Definicija zadeve/subjekta sporočila
“ZADEVA”/“SUBJEKT” v elektronskem sporočilu se navede v obliki:
    KAP        oznaka aplikacije v BS
    NNNNNNN    7-mestna šifra poročevalca iz registra
               poslovnih subjektov v RS
    DATUM      datum, zadnji dan obdobja, na katerega se
               nanaša poročilo (LLLLMMDD)
    OZNAKA     'N'
    (PGP)      oznaka, da gre za uporabo PGP
    (CP)       kodna tabela (obvezno, kadar ni
               uporabljena kodna tabela CP1250,
               možne vrednosti CP: CP7BIT, CP1250,
               CP852,
               CPUNICODE, CPLATIN1, CPLATIN2)

Primer zadeve/subjekta sporočila:
KAP586058020041231N(PGP)(CPLATIN2)
5.3.Zaščita poročil
Vsa poročila morajo biti elektronsko podpisana in tudi šifrirana. Za zaščito poročil banka uporabi PGP. Ko se pošilja elektronsko sporočilo, mora biti to zakodirano tako, da je v ASCII obliki, ne pa v binarni.

Primer sporočila:
    -----BEGIN PGP MESSAGE-----
    Version: PGPfreeware 6.5.2 for non-commercial use
MXlly96wYF4DHu9Zsk11t/oHhK1hgqhWieAweGmgi7nMH8fxfAv76efLi7Iy4wQe
    =9i1L
    -----END PGP MESSAGE-----

Banka mora PGP javni ključ poslati po elektronski pošti na naslov PGP@BSI.SI, pri čemer mora biti v sporočilu navedeno, da gre za aplikacijo KAP.
Banka mora parametre javnega ključa (Key ID, Key Name, Fingerprint (hex), Created), potrjene s žigom pošiljatelja in podpisom pooblaščene osebe, posredovati Banki Slovenije tudi v pisni obliki, in sicer na naslov:

Banka Slovenije
       Informacijska tehnologija
       Slovenska 35
       1505 Ljubljana

PGP javni ključ Banke Slovenije za aplikacijo KAP se nahaja na spletnem strežniku Banke Slovenije na naslovu:
http://www.bsi.si/html/elektronska_posta/pgp/BA39266B.asc
5.4. Odgovor pošiljatelju o prevzemu pošte oziroma o rezultatu obdelave njegovih podatkov
Banka po izvedeni obdelavi prejme odgovor od Banke Slovenije, in sicer:

– »RE: originalni subject, KAP-I-OK, besedilo«
v primeru, ko je poročilo v redu
 
– »RE: originalni subject, KAP-E-err, besedilo«
v primerih, ko je v poročilu napaka
 
Možnosti za err:
BADSUBJ
BADDATA

V besedilu odgovora se pri pravilnem poročilu zapiše:

»Vsi podatki OK«

V primeru napak v poročilu se besedilo odgovora glasi:

»Poročilo vsebuje napačne podatke«

Vsi odgovori pošiljatelju morajo biti elektronsko podpisani s ključem Banke Slovenije. V primeru, da se v odgovoru nahajajo tudi podatki, mora biti ta šifriran tudi z javnim ključem pošiljatelja.
5.5. Pošiljanje popravkov
Poročila, ki so bila poslana z napačno vsebino in so bila v Banki Slovenije sprejeta kot pravilna, mora banka popraviti in še enkrat poslati v Banko Slovenije. Poslati je potrebno celotno poročilo. Popravljeno poročilo zamenja oziroma prekrije prejšnje poročilo.
Poročila, na katera pošiljatelj prejme negativen odgovor, se pošljejo ponovno, kot nova.
6. Informacije
Vprašanja, povezana z uporabo sporočilnega sistema, se naslovi na:

Help desk za sistem BSNET:
 
SMTP:          bsnethelpdesk@bsi.si
 
ali administratorja domene BSNET
 
SMTP:          bsnetadmin@bsi.si


### III. PREHODNE IN KONČNE DOLOČBE

7. Banka mora prvo poročilo v skladu s tem navodilom predložiti po stanju na dan 31. 3. 2005, najkasneje do 16. 5. 2005, kasneje pa v rokih predpisanih v 51. točki sklepa.
8. To navodilo začne veljati z dnem objave v Uradnem listu Republike Slovenije.

Ljubljana, dne 15. aprila 2005.

Mitja Gaspari l. r.
Guverner
