---
kratica: NAVO700
naziv: "Navodilo za izdelavo poročila o medbančnih depozitih"
vrsta: "navodilo"
datum: 2004-04-26
sop: 2004-01-1947
organ: ""
zbirka: "Neuradna prečiščena besedila"
status: "Neznano"
vir: "https://www.uradni-list.si/1/objava.jsp?sop=2004-01-1947"
---

# Navodilo za izdelavo poročila o medbančnih depozitih

Na podlagi tretjega odstavka 29. člena zakona o Banki Slovenije (Uradni list RS, št. 58/02 in 85/02) in 8. točke sklepa o pošiljanju določenih podatkov bank in hranilnic (Uradni list RS, št. 34/04) sprejema guverner Banke Slovenije


## N A V O D I L O
za izdelavo poročila o medbančnih depozitih

1. Banke sestavijo in posredujejo Banki Slovenije poročilo o medbančnih depozitih v skladu z veljavnim sklepom o pošiljanju določenih podatkov bank in hranilnic.
Navodilo ureja vsebino, način in roke posredovanja podatkov o medbančnih depozitih.
2. Banka dnevno najkasneje do 11. ure posreduje Banki Slovenije podatke o danih in prejetih nezavarovanih tolarskih depozitih, ki jih je dala oziroma prejela od drugih bank. Banka posreduje podatke o depozitih, sklenjenih pretekli delovni dan.
Banka posreduje podatke ne glede na ročnost depozita in ne glede na tip uporabljene obrestne mere (nominalna, indeksirana).
Za potrebe teh navodil
– so izrazi medbančni depozit, medbančni kredit, medbančno posojilo in medbančna vloga sinonimi;
– podaljšanje depozita šteje kot novo odobren oziroma novo prejet depozit;
– banka poroča kot en zapis depozita sklenjena isti dan, z isto banko, z istim datumom valutacije in datumom vračila depozita, z enako obrestno mero istega tipa (t.j. zneske depozitov, kjer so navedeni parametri enaki, sešteje).
3. Banka posreduje Banki Slovenije v skladu in na način, predpisan s 4. točko tega navodila, za vsak dan oziroma prejet depozit naslednje podatke:
– Matično številko banke poročevalke
– Matično številko banke posojilodajalke
– Matično številko banke posojilojemalke
– Datum sklenitve depozita
– Datum valutacije depozita
– Datum vračila depozita
– Znesek depozita v tisoč SIT
– Obrestno mero depozita, zaokroženo na dve decimalni mesti
– Tip obrestne mere depozita
– N (nominalna obrestna mera)
– D (obrestna mera, vezana na devizno klavzulo)
– T (obrestna mera, vezana na TOM)
– O (obrestna mera, vezana na ostale vrste referenčnih obrestnih mer).
4. Način poročanja
Banka posreduje Banki Slovenije poročilo prek elektronske pošte po omrežju BSNET na naslov:
cbomp@bsi.si.
4.1. Definicija zadeve (subjecta)
Zadeva v elektronskem sporočilu se navede v obliki:
– CBOMP oznaka aplikacije v Banki Slovenije,
– NNNNNNN matična številka banke,
– LLLLMMDD datum poročanja,
– (PGP) oznaka, da gre za uporabo PGP,
– (CP) kodna tabela (obvezno, kadar ni uporabljena kodna tabela CP1250, možne vrednosti CP: CP7BIT, CP1250, CP852, CPUNICODE, CPLATIN1, CPLATIN2).
primera:
CBOMP555555520020304(PGP) / uporabljena kodna tabela 1250
CBOMP555555520020304(PGP)(CP7BIT) / uporabljena 7 bitna kodna tabela
4.2. Zaščita poročil
Vsa sporočila so elektronsko podpisana s programom PGP. Za podpisovanje banka uporablja javni ključ, ki ga mora poslati Banki Slovenije vsaj en delovni dan prej, preden postane obveznik za poročanje. Sporočila so lahko tudi šifrirana (neobvezno). Za šifriranje se uporablja javni ključ Banke Slovenije, opisan v točki 4.3.
4.3. Odgovor banki o prevzemu pošte
Vsi odgovori Banke Slovenije so elektronsko podpisani z javnim ključem "Banka Slovenije – Aplikacija CBOMP", ki je dostopen na spletni strani: http://www.bsi.si/html/elektronska_posta/pgp/index.html. Odgovor potrjuje sprejem sporočila in sporoča pravilnost oziroma nepravilnost podatkov.
Primer odgovora v primeru, ko je sporočilo sprejeto:
– RE: originalna zadeva, CBOMP-I-OK, tekst
Primer: RE: CBOMP555555520020304 CBOMP-I-OK, Podatki so v redu
Primer odgovora, ko so v sporočilu napake:
– RE: originalna zadeva, CBOMP-E-ERR, tekst
Napaka je opisana v vsebini sporočila in v skrajšani obliki v polju tekst.
4.4. Pravila za formiranje zapisov
Priporočamo uporabo kodne tabele CP1250. V kolikor je uporabljena druga kodna tabela, mora biti obvezno navedena kot zadnji podatek v zadevi (subjectu) (glej točko 4.1).
Vsakemu zapisu je na začetku dodana oznaka aplikacije (CBOMP) in tip zapisa (prvi zapis-00, podatki-11, zadnji zapis-99).
– prvi zapis: CBOMP00, v nadaljevanju:
– matična številka banke poročevalke (7N),
– datum poročanja (8N),
– status podatkov: N-novi, P-popravki (1AN),
– zaporedna številka popravka (2N).
– podatki: CBOMP11, v nadaljevanju:
– zaporedna številka vrstice (2N)
– matična številka banke posojilodajalke (7N),
– matična številka banke posojilojemalke (7N),
– datum sklenitve depozita (8N),
– datum valutacije depozita (8N),
– datum vračila depozita (8N)
– znesek depozita v tisoč SIT (9N)
– obrestna mera depozita (4,2N)
– tip obrestne mere depozita (N, D, T ali O)
– zadnji zapis: CBOMP99, v nadaljevanju:
– število zapisov s podatki (2N),
– ime in priimek sestavljalca (40AN),
– telefon sestavljalca (12AN).
Razlaga oznak:
– N pomeni število numeričnih znakov. Prva številka pomeni število vseh cifer, druga število decimalnih mest.
Primer za 4,2N: 9,15 ---> 0915
– AN pomeni število alfa numeričnih znakov (zapis znakov od leve proti desni). Kadar podatka ni, je polje prazno (napolnjeno s presledki).
V primeru, da datum vračila depozita ni določen, ga zapišemo kot 31.12.9999.
4.5. Pošiljanje popravkov
Poročilo, ki je napačno, je treba popraviti in še enkrat poslati v Banko Slovenije. Poslati je treba celotno poročilo. Novo, popravljeno poročilo zamenja oziroma prekrije prejšnje poročilo.
Poročilo se šteje kot popravek, če ima v prvem zapisu v polju status podatkov znak P in zaporedno številko popravka 01. Primer: CBOMP00555555520020304P01. Popravek popravka ima zaporedno številko popravka enako 02 in tako dalje.
4.6. Ponovno pošiljanje zavrnjenih poročil
Kadar je poročilo zavrnjeno (zaradi napačne strukture zadeve/subjecta, napačnega PGP podpisa ipd.), je treba poročilo poslati v celoti ponovno. Ponovno poslana predhodno zavrnjena poročila banka označi kot nova.
4.7. Primer poročila v obliki za pošiljanje prek elektronske pošte
Zadeva: CBOMP555555520020304(PGP)
CBOMP00555555520020304N00
CBOMP1101555555512477772002030120020301200203180120000000725N
CBOMP1102555555512477772002030120020304200203180023000000710N
CBOMP1103555555562666662002030120020301200203220007500000900N
CBOMP1104121111155555552002030120020301200204100400000000325T
CBOMP9904JANEZ NOVAK 01 999 99 99
5. Z dnem uveljavitve tega navodila preneha veljati navodilo za izdelavo poročila o medbančnih depozitih št. 22-0157/02 z dne 25. 11. 2002.
6. To navodilo začne veljati 1. 5. 2004.

Št. 22-0051/04

Ljubljana, dne 16. aprila 2004.

Guverner
Mitja Gaspari l. r.
