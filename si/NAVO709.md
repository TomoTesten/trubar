---
kratica: NAVO709
naziv: "Navodilo za izdelavo poročila o depozitnem trgu"
vrsta: "navodilo"
datum: 2004-07-13
sop: 2004-01-3370
organ: "Banka Slovenije"
zbirka: "Drugi splošni in posamični akti"
status: "Neveljaven predpis"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=2004-01-3370"
---

# Navodilo za izdelavo poročila o depozitnem trgu

Na podlagi tretjega odstavka 29. člena zakona o Banki Slovenije (Uradni list RS, št. 58/02 in 85/02) in 12. točke sklepa o pošiljanju določenih podatkov bank in hranilnic (Uradni list RS, št. 34/04) sprejema guverner Banke Slovenije


## N A V O D I L O
za izdelavo poročila o depozitnem trgu


### 1

Poročilo o depozitnem trgu sestavlja in posreduje Banki Slovenije osem največjih bank v Republiki Sloveniji po kriteriju bilančne vsote (v nadaljevanju: obvezniki). Izbor obveznikov se opravi dvakrat letno po knjigovodskih podatkih na dan 30. junij in 31. december.
Banka Slovenije do 25. januarja oziroma do 25. julija pisno obvesti tiste banke, ki so po novem izboru obvezniki. Nov izbor obveznikov začne veljati 15. februarja in 15. avgusta.


### 2

Zahtevane podatke obveznikov, metodologijo za poročanje ter način in roke posredovanja podatkov Banki Slovenije določa in ureja to navodilo.


### 3

Obveznik posreduje Banki Slovenije podatke o prejetih nezavarovanih tolarskih depozitih z dospelostjo do enega leta, ki jih je prejel od pravnih oseb, ki niso obvezniki za obvezne rezerve, kot jih določa veljavni sklep o obveznih rezervah (v nadaljevanju: depoziti).


### 4

Depoziti so razvrščeni v osem razredov glede na ročnost in denarno poravnavo, in sicer:

-------------------------------------------------
 Razred    Ročnost              Denarna poravnava
-------------------------------------------------
 01        čez noč              T + 0
 02        1 dan                T + 1 in več
 03        2 do 7 dni           T + 0 in več
 04        8 do14 dni           T + 0 in več
 05        15 do 30 dni         T + 0 in več
 06        31 do 60 dni         T + 0 in več
 07        61 do 180 dni        T + 0 in več
 08        181 dni do 1 leta    T + 0 in več
-------------------------------------------------

V razredih 01 in 02 obveznik upošteva pri ročnosti kriterij delovnih dni, v razredih od 03 do 08 obveznik pri ročnosti upošteva kriterij koledarskih dni.


### 5

Obveznik posreduje dnevno do 11. ure Banki Slovenije podatke o petih največjih depozitih v vsakem razredu, sklenjenih pretekli delovni dan. V primeru depozita, vplačanega na podlagi okvirne pogodbe, obveznik posreduje podatke o depozitu, vplačanem pretekli delovni dan. Če ima obveznik sklenjenih oziroma vplačanih depozitov pet ali manj, posreduje podatke o vseh sklenjenih depozitih. V primeru, da obveznik ne sklene nobenega depozita, pošlje poročilo s prvim in zadnjim zapisom (glej točko 9.4).


### 6

Za vsak depozit obveznik posreduje Banki Slovenije naslednje podatke:
– Oznaka razreda (od 01 do 08);
– Oznaka depozita v razredu (od 01 do 05);
– Datum sklenitve depozita;
– Datum vplačila depozita;
– Datum vračila depozita;
– Znesek depozita, zaokrožen na tisoč SIT;
– Tip obrestne mere depozita:
· N (nominalna obrestna mera),
· D (obrestna mera, vezana na devizno klavzulo),
· O (obrestna mera, vezana na ostale vrste referenčnih obrestnih mer);
– Obrestna mera depozita na letni ravni (nominalna, nad D, nad O), izračunana na linearen način z upoštevanjem 360 dni v letu, zaokrožena na dve decimalni mesti.


### 7

Če obveznik pri sklepanju poslov uporablja drugačen način izračuna obrestne mere, kot je določen v zadnji alinei 6. točke tega navodila, mora pri posredovanju podatkov Banki Slovenije obrestno mero ustrezno preračunati.


### 8

Obveznik mora poleg podatkov o depozitu, ki jih pošlje Banki Slovenije, imeti v svoji evidenci tudi podatek o partiji pogodbe o depozitu, ki ga predloži Banki Slovenije na njeno zahtevo. Te podatke mora obveznik hraniti najmanj tri mesece.


### 9

Način poročanja
Obveznik pošilja Banki Slovenije podatke prek elektronske pošte po omrežju BSNET na naslov cbodt@bsi.si.
9.1. Definicija zadeve (subjecta) sporočila
Zadeva v elektronskem sporočilu se navede v obliki:
– CBODT oznaka aplikacije v Banki Slovenije,
– NNNNNNN matična številka obveznika,
– LLLLMMDD datum poročanja,
– (PGP) oznaka, da gre za uporabo PGP,
– (CP) kodna tabela (obvezno, kadar ni uporabljena kodna tabela CP1250, možne vrednosti CP: CP7BIT, CP1250, CP852, CPUNICODE, CPLATIN1, CPLATIN2).
primera:
CBODT555555520040415(PGP) / uporabljena kodna tabela 1250
CBODT555555520040415(PGP)(CP7BIT) / uporabljena 7 bitna kodna tabela
9.2. Zaščita poročil
Vsa sporočila so elektronsko podpisana s programom PGP. Za podpisovanje banka uporablja javni ključ, ki ga mora poslati Banki Slovenije vsaj en delovni dan prej, preden postane obveznik za poročanje. Sporočila so lahko tudi šifrirana (neobvezno). Za šifriranje se uporablja javni ključ Banke Slovenije opisan v točki 9.3.
9.3. Odgovor obvezniku o prevzemu pošte
Vsi odgovori Banke Slovenije so elektronsko podpisani z javnim ključem "Banka Slovenije – Aplikacija CBODT", ki je dostopen na spletni strani: http://www.bsi.si/html/elektronska_posta/pgp/index.html. Odgovor potrjuje sprejem sporočila in sporoča pravilnost oziroma nepravilnost podatkov.
Primer odgovora v primeru, ko je sporočilo sprejeto:
RE: originalna zadeva, CBODT-I-OK, tekst
Primer: RE: CBODT555555520040315 CBODT-I-OK, Podatki so v redu
Primer odgovora, ko so v sporočilu napake:
RE: originalna zadeva, CBODT-E-ERR, tekst
Napaka je opisana v vsebini sporočila in v skrajšani obliki v polju tekst.
9.4. Pravila za formiranje zapisov
Priporočamo uporabo kodne tabele CP1250. Kolikor je uporabljena druga kodna tabela, mora biti obvezno navedena kot zadnji podatek v zadevi (subjectu) (glej točko 9.1)
Vsak zapis se prične z oznako aplikacije (CBODT) in oznako tipa zapisa (prvi zapis-00, podatki-11, zadnji zapis-99).
– prvi zapis: CBODT00 se nadaljuje z:
– matično številko banke (7N),
– datumom poročanja LLLLMMDD,
– oznako (1AN), ali gre za nove podatke (N) ali popravke (P);
– zapis s podatki: CBODT11 se nadaljuje z:
– oznako razreda (2N),
– oznako depozita v razredu (2N),
– datumom sklenitve depozita LLLLMMDD,
v primeru okvirne pogodbe datum sklenitve zapišemo kot 00000000
– datumom vplačila depozita LLLLMMDD,
– datumom vračila depozita LLLLMMDD,
– zneskom depozita v tisoč SIT (9N),
– tipom obrestne mere (1AN) (N, D ali O),
– predznakom obrestne mere (+ oziroma -),
– obrestno mero depozita (4,2N);
– zadnji zapis: CBODT99 se nadaljuje z:
– imenom in priimkom sestavljalca (40AN) in
– telefonsko številko sestavljalca (12AN).
Razlaga oznak:
– xAN alfa numerični podatek, število znakov je podano s številko
– xN numerični podatek, število cifer je podano s številko
– x,yN numerični podatek, število vseh cifer je podano z 'x', število decimalnih mest z 'y'
Primer: 7,35 se zapiše kot 0735
– LLLLMMDD datum zapisan v obliki leto/mesec/dan
9.5. Pošiljanje popravkov
Poročilo, ki je napačno, je treba popraviti in še enkrat poslati v Banko Slovenije. Poslati je potrebno celotno poročilo. Novo, popravljeno poročilo zamenja oziroma prekrije prejšnje poročilo. Poročilo se smatra kot popravek, če ima v prvem zapisu v polju oznaka znak P. Primer: CBODT00555555520040415P
9.6. Ponovno pošiljanje zavrnjenih poročil
Kadar je poročilo zavrnjeno (zaradi napačne strukture zadeve/subjecta, napačnega PGP podpisa ipd.), je treba poročilo poslati v celoti ponovno. Ponovno poslana predhodno zavrnjena poročila obveznik označi kot nova.
9.7. Primer poročila v elektronski obliki
Zadeva: CBODT555555520040415(PGP)
CBODT00555555520040415N
CBODT110101200404142004041420040415000052000N+0300
CBODT110102200404142004041420040415000049000N+0310
CBODT110103200404142004041420040415010048800N+0310
CBODT110104200404142004041420040415000032000N+0355
CBODT110105200404142004041420040415000031100N+0320
CBODT110201200404142004041520040416000053000N+0320
CBODT110202200404142004041620040417000051000N+0350
CBODT110203200404142004041520040416000035000N+0350
CBODT110204200404142004041520040416000033000N+0320
CBODT110205200404142004041520040416000032000N+0360
CBODT110301200404142004041420040417000090000N+0465
CBODT110302200404142004041420040417000043050N+0465
CBODT110303200404142004041420040418000041000N+0480
CBODT110304200404142004041420040418000040000N+0465
CBODT110305200404142004041420040417000040000N+0475
CBODT110401200404142004041420040424000040000N+0565
CBODT110402200404142004041620040425000036600N+0580
CBODT110403200404142004041420040425000032000N+0565
CBODT110404200404142004041420040424000032000N+0590
CBODT110405200404142004041420040424000026000N+0575
CBODT110501200404142004041420040505000050000N+0615
CBODT110502200404142004041420040505000042000N+0615
CBODT110503200404142004041520040505000035000N+0630
CBODT110504200404142004041420040505000034500N+0620
CBODT110505200404142004041420040506000032000N+0620
CBODT110601200404142004041420040520000062000N+0655
CBODT110602200404142004041420040522000050000N+0690
CBODT110603200404142004041420040522000042000N+0655
CBODT110604200404142004041520040523000034480N+0490
CBODT110605200404142004041420040522000012000N+0495
CBODT110701200404142004041420040722000055500N+0690
CBODT110702200404142004041420040722000044500O+0710
CBODT110703200404142004041420040822000034590O-0100
CBODT110704200404142004041420040822000033500N+0720
CBODT110705200404142004041420040822000031500N+0720
CBODT110801200404142004041420041210000075500D+0700
CBODT110802200404142004041420041111000044000D+0710
CBODT110803200404142004041420041111000024500N+0770
CBODT110804200404142004041420041113000022200N+0840
CBODT110805200404142004041620041111000017000N+0850
CBOMP99PETER POROČNIK                                       013459843


### 10

Z dnem uveljavitve tega navodila preneha veljati navodilo za izdelavo poročila o depozitnem trgu (Uradni list RS, št. 43/04).
Obvezniki za poročanje, izbrani na podlagi navodila za izdelavo poročila o depozitnem trgu (Uradni list RS, št. 43/04), z dnem uveljavitve tega navodila postanejo obvezniki za poročanje po tem navodilu.


### 11

To navodilo začne veljati 1. 9. 2004.

Št. 22-0091

Ljubljana, dne 6. julija 2004.

Guverner
Mitja Gaspari l. r.
