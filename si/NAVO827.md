---
kratica: NAVO827
naziv: "Navodilo o vsebini in načinu poročanja o medbančnih depozitih"
vrsta: "navodilo"
datum: 2006-10-12
sop: 2006-01-4512
organ: "Banka Slovenije"
zbirka: "Drugi splošni in posamični akti"
status: "Neveljaven predpis"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=2006-01-4512"
---

# Navodilo o vsebini in načinu poročanja o medbančnih depozitih

Na podlagi tretjega odstavka 29. člena Zakona o Banki Slovenije (Uradni list RS, št. 72/06 – uradno prečiščeno besedilo) in 5. točke Sklepa o poročanju o medbančnih depozitih (Uradni list RS, št. 103/06) sprejema guverner Banke Slovenije


## N A V O D I L O
o vsebini in načinu poročanja
o medbančnih depozitih

UVODNA DOLOČBA

1. To navodilo ureja vsebino in način posredovanja podatkov o nezavarovanih medbančnih depozitih, ki jih obvezniki poročanja posredujejo Banki Slovenije v skladu z veljavnim Sklepom o poročanju o medbančnih depozitih.

VSEBINA POROČANJA

2. Za potrebe teh navodil:
– so izrazi medbančni depozit, medbančni kredit, medbančno posojilo in medbančna vloga sinonimi;
– se podaljšanje depozita šteje kot novo odobren oziroma novo prejet depozit;
– obveznik poročanja poroča kot en zapis depozita, sklenjena isti dan, z isto kreditno institucijo, z istim datumom valutacije in datumom vračila depozita in z enako obrestno mero istega tipa (tj. zneske depozitov, kjer so navedeni parametri enaki, sešteje).
3. Obveznik poročanja mora Banki Slovenije najkasneje do 8. ure na delovni dan Banke Slovenije poročati o prejetih in danih nezavarovanih medbančnih depozitih, ki jih je z drugimi kreditnimi institucijami v sodelujočih državah članicah sklenil od vključno dneva, ko je poslal zadnje poročilo o medbančnih depozitih.
V primeru, da v obdobju, za katero mora poročati, obveznik poročanja ni sklenil nezavarovanih medbančnih depozitov, Banki Slovenije ne posreduje poročila o medbančnih depozitih.
Obveznik poročanja posreduje podatke ne glede na ročnost depozita in ne glede na tip uporabljene obrestne mere.
4. Obveznik poročanja posreduje Banki Slovenije naslednje podatke:
– MFI_ID obveznika poročanja
– MFI_ID posojilodajalca
– MFI_ID posojilojemalca
– Datum sklenitve depozita
– Datum valutacije depozita
– Datum vračila depozita
– Znesek depozita v eurih
– Obrestno mero depozita, zaokroženo na dve decimalni mesti
– Tip obrestne mere depozita
– N (nominalna obrestna mera)
– O (ostale vrste obrestnih mer)
Obveznik poročanja uporabi za oznako kreditne institucije MFI_ID kreditnih institucij s seznama kreditnih institucij, ki je objavljen na spletni strani Evropske centralne banke (www.ecb.int).
V primeru uporabe ostalih vrst obrestnih mer obveznik poročanja izračuna in poroča nominalno obrestno mero, ki velja na dan sklenitve depozita, in v polje »tip obrestne mere« vnese oznako »O«.

NAČIN POROČANJA

5. Obveznik poročanja posreduje Banki Slovenije poročilo prek elektronske pošte po omrežju BSNET na naslov: cbomp@bsi.si.
5.1. Definicija zadeve (subject)
Zadeva v elektronskem sporočilu se navede v obliki:
– CBOMP  oznaka aplikacije v Banki Slovenije,
– SINNNNNNN  MFI_ID obveznika poročanja,
– LLLLMMDD  datum poročanja,
– (PGP)  oznaka, da gre za uporabo PGP,
– (CP)  kodna tabela (obvezno, kadar ni uporabljena kodna tabela CP1250, možne vrednosti CP : CP7BIT, CP1250, CP852, CPUNICODE, CPLATIN1, CPLATIN2).
primera:
CBOMPSI555555520060414(PGP)/uporabljena kodna tabela 1250
CBOMPSI555555520060414(PGP)(CP7BIT)/uporabljena 7-bitna kodna tabela
5.2. Zaščita poročil
Vsa sporočila morajo biti elektronsko podpisana s programom PGP. Za podpisovanje obveznik poročanja uporablja javni ključ, ki ga mora poslati Banki Slovenije vsaj en delovni dan Banke Slovenije prej, preden začne poročati v skladu s tem sklepom. Sporočila so lahko tudi šifrirana (neobvezno). Za šifriranje se uporablja javni ključ Banke Slovenije, opisan v točki 5.3.
5.3. Odgovor obvezniku poročanja o prevzemu pošte
Vsi odgovori Banke Slovenije so elektronsko podpisani z javnim ključem »Banka Slovenije – Aplikacija CBOMP«, ki je dostopen na spletni strani: http://www.bsi.si/html/elektronska_posta/pgp/index.html. Odgovor potrjuje sprejem sporočila in sporoča pravilnost oziroma nepravilnost podatkov.
Primer odgovora v primeru, ko je sporočilo sprejeto:
– RE: originalna zadeva, CBOMP-I-OK, tekst

Primer:   RE: CBOMPSI555555520060414 CBOMP-I-OK, Podatki so v redu

Primer odgovora, ko so v sporočilu napake:
– RE: originalna zadeva, CBOMP-E-ERR, tekst
Napaka je opisana v vsebini sporočila in v skrajšani obliki v polju tekst.
5.4. Pravila za formiranje zapisov
Priporočamo uporabo kodne tabele CP1250. Kolikor je uporabljena druga kodna tabela, mora biti obvezno navedena kot zadnji podatek v zadevi (subjectu) (glej točko 5.1).
Vsakemu zapisu je na začetku dodana oznaka aplikacije (CBOMP) in tip zapisa (prvi zapis-00, podatki-11, zadnji zapis-99).
– prvi zapis: CBOMP00, v nadaljevanju:
– MFI_ID obveznika poročanja (9AN),
– datum poročanja (8N),
– status podatkov: N-novi, P-popravki (1AN),
– zaporedna številka popravka (2N).
– podatki: CBOMP11, v nadaljevanju:
– zaporedna številka vrstice (3N)
– MFI_ID posojilodajalca (15AN),
– MFI_ID posojilojemalca (15AN),
– datum sklenitve depozita (8N),
– datum valutacije depozita (8N),
– datum vračila depozita (8N)
– znesek depozita v EUR (9N)
– obrestna mera depozita (4,2N)
– tip obrestne mere depozita (»N« ali »O«)
– zadnji zapis: CBOMP99, v nadaljevanju:
– število zapisov s podatki (3N),
– ime in priimek sestavljavca (40AN),
– telefon sestavljavca (12AN).
Razlaga oznak:
– N pomeni število numeričnih znakov. Prva številka pomeni število vseh cifer, druga število decimalnih mest.
Primer za 4,2N:   3,15   --->  0315
– AN pomeni število alfa numeričnih znakov (zapis znakov od leve proti desni). Kadar podatka ni, je polje prazno (napolnjeno s presledki).
V primeru, da datum vračila depozita ni določen, ga zapišemo kot 31. 12. 9999.
5.5. Pošiljanje popravkov
Poročilo, ki je napačno, je treba čim prej popraviti in še enkrat poslati v Banko Slovenije. Poslati je treba celotno poročilo. Novo, popravljeno poročilo zamenja oziroma prekrije prejšnje poročilo.
Poročilo se šteje kot popravek, če ima v prvem zapisu v polju status podatkov znak P in zaporedno številko popravka 01. Primer: CBOMP00SI555555520060414P01. Popravek popravka ima zaporedno številko popravka enako 02 in tako dalje.
5.6. Ponovno pošiljanje zavrnjenih poročil
Kadar je poročilo zavrnjeno (zaradi napačne strukture zadeve/subjecta, napačnega PGP podpisa ipd.), je treba poročilo čim prej ponovno poslati v celoti. Ponovno poslana poročila, ki so bila predhodno zavrnjena, obveznik poročanja označi kot nova.
5.7. Primer poročila v obliki za pošiljanje prek elektronske pošte

Zadeva: CBOMPSI555555520060414(PGP)
-------------------------------------------------------------------------------
CBOMP00SI555555520060414N00
CBOMP11001SI5555555          SI1247777   2006041320060413200604180120000000325N
CBOMP11002SI5555555          SI1247777   2006041320060414200604180023000000310N
CBOMP11003SI5555555          DE62666666  2006041320060413200604220007500000400N
CBOMP11004AT1211111          SI5555555   2006041320060413200607010400000000325O
CBOMP99004JANEZ NOVAK                    01 999 99 99
-------------------------------------------------------------------------------

6. Z dnem uveljavitve tega navodila preneha veljati Navodilo za izdelavo poročila o medbančnih depozitih (Uradni list RS, št. 43/04, 68/04 in 42/06). Obveznik poročanja pošlje zadnje poročilo v skladu z navodilom iz prejšnjega stavka 3. 1. 2007, in sicer za medbančne depozite, sklenjene 29. 12. 2006 v tolarjih.
7. To navodilo začne veljati 1. 1. 2007. Obveznik poročanja ga prvič uporabi 3. 1. 2007 za poročanje medbančnih depozitov, sklenjenih 2. 1. 2007 v eurih.

Guverner
Banke Slovenije
Mitja Gaspari l.r.
