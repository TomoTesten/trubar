---
kratica: NAVO699
naziv: "Navodilo za izdelavo poročila o depozitnem trgu"
vrsta: "navodilo"
datum: 2004-04-26
sop: 2004-01-1946
organ: ""
zbirka: "Neuradna prečiščena besedila"
status: "Neznano"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=2004-01-1946"
---

# Navodilo za izdelavo poročila o depozitnem trgu

Na podlagi tretjega odstavka 29. člena zakona o Banki Slovenije (Uradni list RS, št. 58/02 in 85/02) in 12. točke sklepa o pošiljanju določenih podatkov bank in hranilnic (Uradni list RS, št. 34/04) sprejema guverner Banke Slovenije


## N A V O D I L O
za izdelavo poročila o depozitnem trgu

1. Poročilo o depozitnem trgu sestavlja in posreduje Banki Slovenije osem največjih bank v Republiki Sloveniji po kriteriju bilančne vsote /v nadaljevanju: obvezniki/. Izbor obveznikov se opravi dvakrat letno po knjigovodskih podatkih na dan 30. junij in 31. december.
Banka Slovenije do 25. januarja oziroma do 25. julija pisno obvesti tiste banke, ki so po novem izboru obvezniki. Nov izbor obveznikov začne veljati 15. februarja in 15. avgusta.
2. Zahtevane podatke obveznikov, metodologijo za poročanje ter način in roke posredovanja podatkov Banki Slovenije določa in ureja to navodilo.
3. Obveznik posreduje Banki Slovenije podatke o prejetih nezavarovanih tolarskih depozitih z dospelostjo do enega leta, ki jih je prejel od pravnih oseb, ki niso obvezniki za obvezne rezerve, kot jih določa veljavni sklep o obveznih rezervah /v nadaljevanju: depoziti/.
4. Depoziti so razvrščeni v devet razredov glede na ročnost in denarno poravnavo, in sicer:

---------------------------------------------------
Razred        Ročnost             Denarna poravnava
---------------------------------------------------
01            čez noč             T + 0
02            1 dan               T + 1 in več
03            2 do 7 dni          T + 0 in več
04            8 do14 dni          T + 0 in več
05            15 do 30 dni        T + 0 in več
06            31 do 60 dni        T + 0 in več
07            61 do 180 dni       T + 0 in več
08            181 dni do 1 leta   T + 0 in več
09            na odpoklic         T + 0 in več
---------------------------------------------------

V razredih 01 in 02 obveznik upošteva pri ročnosti kriterij delovnih dni, v razredih od 03 do 08 obveznik pri ročnosti upošteva kriterij koledarskih dni.
5. Obveznik posreduje dnevno do 11. ure Banki Slovenije podatke o petih največjih depozitih v vsakem razredu, sklenjenih pretekli delovni dan. V primeru depozita, vplačanega na podlagi okvirne pogodbe, obveznik posreduje podatke o depozitu, vplačanem pretekli delovni dan. Če ima obveznik sklenjenih oziroma vplačanih depozitov pet ali manj, posreduje podatke o vseh sklenjenih depozitih. V primeru, da obveznik ne sklene nobenega depozita, pošlje poročilo s prvim in zadnjim zapisom (glej točko 9.4).
6. Za vsak depozit obveznik posreduje Banki Slovenije naslednje podatke:
– Oznaka razreda (od 01 do 09);
– Oznaka depozita v razredu (od 01 do 05);
– Datum sklenitve depozita;
– Datum vplačila depozita;
– Datum vračila depozita;
– Znesek depozita, zaokrožen na tisoč SIT;
– Tip obrestne mere depozita:
– N (nominalna obrestna mera),
– D (obrestna mera, vezana na devizno klavzulo),
– O (obrestna mera, vezana na ostale vrste referenčnih obrestnih mer);
– Obrestna mera depozita na letni ravni (nominalna, nad D, nad O), izračunana na linearen način z upoštevanjem 360 dni v letu, zaokrožena na dve decimalni mesti.
7. Če obveznik pri sklepanju poslov uporablja drugačen način izračuna obrestne mere, kot je določen v zadnji alinei 6. točke tega navodila, mora pri posredovanju podatkov Banki Slovenije obrestno mero ustrezno preračunati.
8. Obveznik mora poleg podatkov o depozitu, ki jih pošlje Banki Slovenije, imeti v svoji evidenci tudi podatek o partiji pogodbe o depozitu, ki ga predloži Banki Slovenije na njeno zahtevo. Te podatke mora obveznik hraniti najmanj tri mesece.
9. Način poročanja
Obveznik pošilja Banki Slovenije podatke prek elektronske pošte po omrežju BSNET na naslov cbodt@bsi.si.
9.1. Definicija zadeve (subjecta) sporočila
Zadeva v elektronskem sporočilu se navede v obliki:
– CBODT oznaka aplikacije v Banki Slovenije,
– NNNNNNN matična številka banke oziroma hranilnice,
– LLLLMMDD datum poročanja,
– (PGP) oznaka, da gre za uporabo PGP,
– (CP) kodna tabela (obvezno, kadar ni uporabljena kodna tabela CP1250, možne vrednosti CP: CP7BIT, CP1250, CP852, CPUNICODE, CPLATIN1, CPLATIN2).
primera:
CBODT555555520030415(PGP) / uporabljena kodna tabela 1250
CBODT555555520030415(PGP)(CP7BIT) / uporabljena 7 bitna kodna tabela
9.2. Zaščita poročil
Vsa sporočila so elektronsko podpisana s programom PGP. Za podpisovanje banka uporablja javni ključ, ki ga mora poslati Banki Slovenije vsaj en delovni dan prej, preden postane obveznik za poročanje. Sporočila so lahko tudi šifrirana (neobvezno). Za šifriranje se uporablja javni ključ Banke Slovenije opisan v točki 9.3.
9.3. Odgovor obvezniku o prevzemu pošte
Vsi odgovori Banke Slovenije so elektronsko podpisani z javnim ključem "Banka Slovenije – Aplikacija CBODT", ki je dostopen na spletni strani: http://www.bsi.si/html/elektronska_posta/pgp/index.html. Odgovor potrjuje sprejem sporočila in sporoča pravilnost oziroma nepravilnost podatkov.
Primer odgovora v primeru, ko je sporočilo sprejeto:
RE: originalna zadeva, CBODT-I-OK, tekst
Primer:  RE: CBODT555555520030315 CBODT-I-OK, Podatki so v redu
Primer odgovora, ko so v sporočilu napake:
RE: originalna zadeva, CBODT-E-ERR, tekst
Napaka je opisana v vsebini sporočila in v skrajšani obliki v polju tekst.
9.4. Pravila za formiranje zapisov
Priporočamo uporabo kodne tabele CP1250. V kolikor je uporabljena druga kodna tabela, mora biti obvezno navedena kot zadnji podatek v zadevi (subjectu) (glej točko 9.1)
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
v primeru depozita na odpoklic datum vračila zapišemo kot 99991231
– zneskom depozita v tisoč SIT (7N),
– tipom obrestne mere (1AN) (N, D ali O),
– obrestno mero depozita (4,2N)
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
Poročilo, ki je napačno, je treba popraviti in še enkrat poslati v Banko Slovenije. Poslati je treba celotno poročilo. Novo, popravljeno poročilo zamenja oziroma prekrije prejšnje poročilo. Poročilo se smatra kot popravek, če ima v prvem zapisu v polju oznaka znak P. Primer: CBODT00555555520030415P
9.6. Ponovno pošiljanje zavrnjenih poročil
Kadar je poročilo zavrnjeno (zaradi napačne strukture zadeve/subjecta, napačnega PGP podpisa ipd.), je treba poročilo poslati v celoti ponovno. Ponovno poslana predhodno zavrnjena poročila obveznik označi kot nova.
9.7. Primer poročila v elektronski obliki
Zadeva: CBODT555555520030415(PGP)
CBODT00555555520030415N
CBODT1101012003041420030414200304150052000N0300
CBODT1101022003041420030414200304150049000N0310
CBODT1101032003041420030414200304150048800N0310
CBODT1101042003041420030414200304150032000N0355
CBODT1101052003041420030414200304150031100N0320
CBODT1102012003041420030415200304160053000N0320
CBODT1102022003041420030416200304170051000N0350
CBODT1102032003041420030415200304160035000N0350
CBODT1102042003041420030415200304160033000N0320
CBODT1102052003041420030415200304160032000N0360
CBODT1103012003041420030414200304170090000N0465
CBODT1103022003041420030414200304170043050N0465
CBODT1103032003041420030414200304180041000N0480
CBODT1103042003041420030414200304180040000N0465
CBODT1103052003041420030414200304170040000N0475
CBODT1104012003041420030414200304240040000N0565
CBODT1104022003041420030416200304250036600N0580
CBODT1104032003041420030414200304250032000N0565
CBODT1104042003041420030414200304240032000N0590
CBODT1104052003041420030414200304240026000N0575
CBODT1105012003041420030414200305050050000N0615
CBODT1105022003041420030414200305050042000N0615
CBODT1105032003041420030415200305050035000N0630
CBODT1105042003041420030414200305050034500N0620
CBODT1105052003041420030414200305060032000N0620
CBODT1106012003041420030414200305200062000N0655
CBODT1106022003041420030414200305220050000N0690
CBODT1106032003041420030414200305220042000N0655
CBODT1106042003041420030415200305230034480N0490
CBODT1106052003041420030414200305220012000N0495
CBODT1107012003041420030414200307220055500N0690
CBODT1107022003041420030414200307220044500O0710
CBODT1107032003041420030414200308220034590N0720
CBODT1107042003041420030414200308220033500N0720
CBODT1107052003041420030414200308220031500N0720
CBODT1108012003041420030414200312100075500D0700
CBODT1108022003041420030414200311110044000D0710
CBODT1108032003041420030414200311110024500N0770
CBODT1108042003041420030414200311130022200N0840
CBODT1108052003041420030416200311110017000N0850
CBODT1109012003041420030414999912310075500N0350
CBODT1109022003041420030414999912310044000N0400
CBODT1109032003041420030414999912310024500N0430
CBODT1109042003041420030414999912310022200N0410
CBODT1109052003041420030416999912310017000N0520
CBOMP99PETER POROČNIK 013459843
10. Z dnem uveljavitve tega navodila preneha veljati navodilo za izdelavo poročila o depozitnem trgu št. 22-0114/03 z dne 16. 7. 2003
11. To navodilo začne veljati 1. 5. 2004.

Št. 22-0050/04

Ljubljana, dne 16. aprila 2004.

Guverner
Mitja Gaspari l. r.
