---
kratica: NAVO269
naziv: "Navodilo za dostavljanje dnevnih podatkov o odkupu in prodaji tuje gotovine po elektronski pošti"
vrsta: "navodilo"
datum: 2000-02-04
sop: 2000-01-0475
organ: "Banka Slovenije"
zbirka: "Drugi splošni in posamični akti"
status: "Veljaven predpis"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=2000-01-0475"
---

# Navodilo za dostavljanje dnevnih podatkov o odkupu in prodaji tuje gotovine po elektronski pošti

Na podlagi tretjega odstavka 49. člena zakona o deviznem poslovanju (Uradni list RS, št. 23/99), tretjega odstavka 17. točke sklepa o opravljanju menjalniških poslov (Uradni list RS, št. 50/99) in 23. člena zakona o Banki Slovenije (Uradni list RS, št. 1/91-I) izdaja guverner Banke Slovenije


## N A V O D I L O
za dostavljanje dnevnih podatkov o odkupu  in prodaji tuje gotovine po elektronski pošti

Navedeno navodilo ureja način dostavljanja dnevnih podatkov o odkupu in prodaji tuje gotovine po elektronski pošti.
1. Naslov za dostavljanje podatkov
1.1 Poročevalci, ki so integrirani v omrežje BSNET, preko X400 mail-a pošljejo poročila na naslov:

Country (C)               =     SI
Administrative_domain (A) =     MAIL
Private_domain (P)        =     BSLO
Organization (O)          =     BS
Organization_unit (OU1)   =     APPSRVR
Surname (S)               =     EKM

1.2 Poročevalci, ki so integrirani v omrežje BSNET, preko internet maila pošljejo poročila na naslov:
EKM@APPSRVR.BS.BSI.SI
1.3 Poročevalci, ki niso integrirani v omrežje BSNET, preko internet maila pošljejo poročila na naslov:
EKM@BSI.SI
2. Definicija subjecta
»ZADEVA«/»SUBJECT« v elektronskem sporočilu se navede v obliki:

EKM         oznaka aplikacije v BS
NNNNNNN     7-mestna šifra poročevalca – menjalca iz registra 
            poslovnih subjektov v RS
LLLLMMDD    datum, na katerega se nanaša poročilo (LLLLMMDD)
(PGP)       oznaka, da gre za uporabo PGP (obvezno za 
            poročevalce, ki niso integrirani v omrežje BSNET)
(CP)        kodna tabela (obvezno, kadar ni uporabljena kodna 
            tabela CP1250, možne vrednosti CP: CP7BIT, CP1250, 
            CP852, CPUNICODE, CPLATIN1, CPLATIN2)

primer:
EKM555057719990930(PGP)(CP7BIT) / uporabljena 7-bitna kodna tabela
EKM555057719990930(PGP) / uporabljena kodna tabela 1250
3. Zaščita poročil
Vsa sporočila so elektronsko podpisana in tudi šifrirana, če so poslana po Internetu. Za zaščito poročil uporabljamo PGP.
Prosimo, da PGP javne ključe pošljete do 15. 5. 2000 po elektronski pošti na naslov:
bsnetadmin@bsi.si
istočasno pa še z dopisom, na katerem so PGP informacije:
– identifikacijska številka ključa (KeyID)
– datum generiranja ključa (Date)
– uporabniško ime ključa (User ID)
na oddelek Informacijska tehnologija, potrjeno s podpisom pooblaščene osebe in žigom pošiljatelja na naslov:
Banka Slovenije
Informacijska tehnologija
Slovenska 35
1505 Ljubljana
PGP javni ključi Banke Slovenije za posamezne aplikacije se nahajajo na WEB strežniku Banke Slovenije na naslovu:

http://www.bsi.si/html/elektronska_posta/pgp/index.html

4. Informacije
Vprašanja, povezana z uporabo sporočilnega sistema, lahko pošiljatelji pošljejo na naslov:
Help desk za sistem BSNET:

x.400:                  c=si/a=mail/p=bslo/o=bs/s=
                        x400helpdesk/ou1=bses
SMTP/Internet naslov:   bsnethelpdesk@bsi.si

ali administratorja domene BSNET in sistema X.400

x.400:                   c=si/a=mail/p=bslo/o=bs/s=
                         bsnetadmin/ou1=bses.
SMTP/Internet naslov:    bsnetadmin@bsi.si

5. Odgovor pošiljatelju o prevzemu pošte oziroma o rezultatu obdelave njegovih podatkov.
Odgovor se lahko pošlje takoj po prevzemu ali pa šele po obdelavi podatkov.

RE:    originalni subject, APL-I-OK, tekst
       v primeru, ko je poročilo v redu
       originalni subject, APL-E-err, tekst
       v primeru, ko so napake v poročilu

možne vrednosti err:

BADSUBJ
BADDATA – N      (dnevno poročilo sprejeto, vendar
                 napake)
BADDATA – Z      (dnevno poročilo zavrnjeno v celoti)
BADPACKET–N      (zbirno dnevno poročilo delno
                 sprejeto, vendar napake v vsaj enem
                 paketu)
BADPACKET – Z    (zbirno dnevno poročilo zavrnjeno
                 v celoti – vsi paketi)

Možne so še druge sistemske napake, ki jih bomo po potrebi dopolnili. O tekstu in izgledu odgovorov bodo menjalci obveščeni po pošti oziroma bo dostopen na Internet strani Banke Slovenije:

http://www.bsi.si/html/porocanje_banki/ekm/index.html

Vsi odgovori pošiljatelju so elektronsko podpisani s ključem Banke Slovenije. V primeru, da se v odgovoru nahajajo tudi podatki, so le-ti tudi šifrirani s pomočjo javnega ključa pošiljatelja.
6. Pošiljanje popravkov dnevnih poročil
Dnevna poročila, ki so napačna, je treba popraviti in popravljena še enkrat poslati v Banko Slovenije. Vsakič je potrebno poslati celotno dnevno poročilo za menjalno mesto. Novo, popravljeno poročilo zamenja oziroma prekrije prejšnje dnevno poročilo za menjalno mesto.
Pošiljatelj, ki pošilja zbirno dnevno poročilo za več menjalnih mest lahko pošlje popravke za eno menjalno mesto, vendar za to menjalno mesto v celoti.
7. Pravila za formiranje zapisov
7.1 Priporočamo uporabo kodne tabele CP1250. Kolikor je uporabljena druga kodna tabela, mora biti obvezno navedena kot zadnji podatek v subjectu (zadevi).
7.2 Vsakemu zapisu je na začetku dodana oznaka aplikacije v BS in tip zapisa (prvi zapis-00, podatki-11, zadnji zapis-99)

prvi zapis:     EKM00     (v nadaljevanju: matična številka
                          menjalca (7N), zaporedna številka menjalnega mesta 
                          (3N), zaporedna številka poročila (5N), status 
                          podatkov: N-novi, P-popravki (1AN), številka sprejema: 
                          za novo poročilo 0000000000, za popravke sporočena 
                          številka sprejema (10N))
podatki:                  EKM11 (v nadaljevanju: zahtevani podatki – glej 
                          strukturo zapisa (8. točka), začetek podatkov)
zadnji zapis:   EKM99     (v nadaljevanju: matična številka menjalca (7N), 
                          zaporedna številka menjalnega mesta (3N) in število 
                          zapisov s podatki znotraj paketa za menjalno mesto 
                          (3N))

V primeru, ko poročevalec (banka ali hranilnica) pošilja zbirno dnevno poročilo za več menjalnih mest, vrstici, ki se začne z EKM99 in zaključuje podatke za eno menjalno mesto, sledi nova vrstica, ki se začne z EKM00 in vsebuje podatke za novo menjalno mesto.
7.3 Dolžine polj so fiksne (število znakov za posamezno polje je razvidno iz tabele).
7.4 N pomeni število numeričnih znakov (števila z vodilnimi ničlami, brez decimalnih pik oziroma vejic.
7.5 Predznačeni zneski imajo na prvem mestu znak + ali –, nato odgovarjajoče število vodilnih ničel in številk). Kadar podatka ni oziroma je njegova vrednost 0, ga napolnimo z ničlami (in predznakom).

Primer:   format        vrednost       način zapisa
          10N              2.500         0000002500
          10,2N         2.540,45         0000254045
          S10,2N        2.545,45         +000254045
          S10,2N       –2.545,45         –000254045

7.6 AN pomeni število alfa numeričnih znakov (zapis znakov od leve proti desni). Kadar podatka ni, je polje prazno (napolnjeno s presledki).
7.7 Datumi – vedno pišemo v obliki LLLLMMDD, LLLLMM, LLLL
7.8 Kadar imamo v podatkih vrednosti DA, NE, jih numerično prikažemo z: 1 – DA, 0 – NE
8. Struktura zapisa (vrstica s podatki):

-----------------------------------------------------------------------------
Atribut                    Dolžina   Vrednost      Primer
-----------------------------------------------------------------------------
Začetek vrstice s
podatki
-----------------------------------------------------------------------------
Ime aplikacije v BS        3 AN      EKM
Identifikacija zapisa
podatkov                   2 N       11
-----------------------------------------------------------------------------
Začetek podatkov
-----------------------------------------------------------------------------
Šifra valute (numerična)   3 N                     nemška marka = 276
                                                   avstrijski šiling = 040
Začetno stanje             14,2 N                  130.750,00 = 0000013075000
                                                   12.000,95 = 00000001200095
Odkup tuje gotovine
(rezidenti)                14,2 N
Odkup tuje gotovine
(nerezidenti)              14,2 N
Odkup tujih čekov          14,2 N
Ponderirani nakupni
tečaj                      13,6 N
Ostali prejemki            14,2 N
Prodaja tuje gotovine
(rezidenti)                14,2 N
Prodaja tuje gotovine
(nerezidenti)              14,2 N
Ponderirani prodajni
tečaj                      13,6 N
Ostali izdatki             14,2 N
Končno stanje              14,2 N
-----------------------------------------------------------------------------

To navodilo stopi v veljavo z dnem objave v Uradnem listu RS, uporablja pa se od   1. 7. 2000 dalje.

Ljubljana, dne 18. januarja 2000.

Guverner
Banke Slovenije
dr. France Arhar l. r.
