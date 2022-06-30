# Geometric Shapes

*Geometric Shapes* je aplikace, ve které si uživatel může vytvářet rovinné nebo
prostorové geometrické útvary a přiřazovat hodnoty jejich metrickým veličinám,
přičemž v okamžiku, kdy lze na základě těchto hodnot vypočítat hodnoty dalších
veličin, tak se tento výpočet provede.

Aplikace je koncipována tak, že žádné konkrétní geometrické útvary nejsou
součástí její implementace, ale vytváří se na základě explicitních informací
v textových souborech, které tyto útvary popisují.
Výčet geometrických útvarů, se kterými aplikace může pracovat, je tedy dán
počtem a dostupností příslušných textových souborů. Platí, že jeden textový
soubor odpovídá jednomu geometrickému útvaru (např. obdélník, kruh, kvádr,
jehlan atp.)

Aplikace běží v příkazovém řádku, resp. terminálu, a používá textové uživatelské
rozhraní.

Aplikace je napsána v IDE PyCharm Community s nainstalovaným interpreterem
jazyka Python verze 3.10.

## Cíle projektu

Smyslem projektu *Geometric Shapes* bylo vytvoření aplikace, která dokáže
spočítat hodnoty metrických veličin (délky stran, obvod, obsah, velikosti úhlů,
u prostorových útvarů objem, povrch atd.) geometrických útvarů na základě hodnot
zadaných uživatelem, tak aby splňovala následující cíle:

### 1. Geometrická univerzálnost

Jedná se o odstínění kódu aplikace od vlastností konkrétního geometrického
útvaru.
Aplikace musí být schopna načíst si informace ke konkrétnímu geometrickému
útvaru explicitně z prostého textového souboru a veškeré výpočty provádět na
jejich základě.

To znamená, že příslušný textový soubor musí daný útvar popisovat vyčerpávajícím
způsobem, a zároveň musí jít aplikaci rozšířit o práci s libovolným geometrickým
útvarem vytvořením nového textového souboru dle daných pravidel (viz níže), aniž
by autor tohoto textového souboru musel vědět cokoli o tom, jak aplikace pracuje
či jak je implementována.

### 2. Matematická univerzálnost

Matematickou univerzálností mám na mysli schopnost vypočítat hodnoty ostatních
metrických veličin konkrétního geometrického útvaru na základě libovolné
kombinace hodnot zadaných uživatelem.
Jakmile uživatel zadá dostatečný počet hodnot konkrétních veličin, na jejichž
základě je matematicky možné vypočítat minimálně jednu novou hodnotu, aplikace
tento výpočet provede. Tím se množina známých hodnot rozšíří a aplikace se
pokusí vypočítat další hodnotu či hodnoty dosud neznámých veličin útvaru.

K pokusu o výpočet nových hodnot tedy dojde vždy, když uživatel přiřadí novou
hodnotu konkrétní veličině, nebo alespoň jedna nová hodnota byla vypočítána
v předchozí iteraci příslušného cyklu.
Cyklus pro pokus o výpočet nových hodnot se zastaví buď tehdy, pokud v jeho
předchozí iteraci nedošlo k výpočtu žádné nové hodnoty, nebo hodnoty všech
metrických veličin daného útvaru jsou již známé a není co dále počítat.

### 3. Schopnost pracovat s dostatečným minimem matematických vzorců

Textový soubor popisující vlastnosti konkrétního geometrického útvaru nemusí
obsahovat "úplný seznam" matematických vzorců v tom smyslu, aby bylo možné
vypočítat hodnotu určité veličiny *ihned* po zadání hodnot uživatelem,
na jejichž základě je možné takový výpočet provést.
Stačí, když víme, že tyto zadané hodnoty povedou k výpočtu jiné veličiny,
díky které bude možné vypočítat danou hodnotu později.

Pro lepší představu si uveďme jednoduchý příklad s obdélníkem:
Dejme tomu, že uživatel zadá délku jeho jedné strany a délku úhlopříčky.
Pokud příslušný textový soubor obsahuje vzorec pro výpočet druhé strany tohoto
obdélníku na základě těchto dvou údajů (např. pomocí Pythagorovy věty) a zároveň
vzorec pro výpočet obsahu obdélníku na základě součinu délek jeho stran, pak
vzorec, který by dokázal spočítat tento obsah přímo z délek zadané strany a
úhlopříčky, je nadbytečný, protože víme, že určitě dojde k výpočtu délky druhé
strany obdélníku, což následně umožní vypočítat i jeho obsah.

## Účel projektu

Účelem tvorby aplikace *Geometric Shapes* bylo vyzkoušet si napsat první funkční
aplikaci v jazyce Python, jehož učení se věnuji. Domnívám se, že spolu se
studiem teorie a konstrukcí jazyka z různých zdrojů je nezbytné průběžně
tvořit vlastní funkční aplikace, protože je to jediná cesta, jak se
v programování postupně zdokonalovat, učit se z vlastních chyb a dotahovat věci
do konce.

*Geometric Shapes* je tedy zejména demonstrační projekt, na kterém jsem si
chtěl procvičit základní programové konstrukce, datové struktury apod. jazyka
Python.
Za tímto účelem jsem si stanovil výše popsané cíle, které aplikace
splňuje.

Rovněž jsem chtěl porovnat objektově orientované programování, které jsem použil
v modulu *shape.py* s procedurálním, jež používají moduly *textfiles.py*
a *main.py*.

## Moduly a třídy

Zdrojový kód je rozdělen do tří souborů (modulů):
1. *textfiles.py* - obsahuje funkce pro práci s textovými soubory - zejména
těmi, které popisují vlastnosti konkrétních geometrických útvarů.
Funkce v tomto modulu slouží pro načtení obsahu textového souboru z disku,
odstranění prázdných řádků a komentářů a převod tohoto obsahu do datové
struktury, která je kompatibilní s konstruktorem třídy *GeometricShape* v modulu
*shape.py*.
2. *shape.py* - obsahuje dvě třídy: *GeometricShape* a *UserShape*:
   - *GeometricShape* - třída je instanciována na základě informací
   pocházejících z textového souboru, jež odpovídá konkrétnímu geometrickému
   útvaru.
   Její instance obsahuje **obecné informace** o tomto útvaru, tedy
   takové, které jsou **společné** pro všechny útvary daného geometrického
   "typu" jako např. obdélník, kruh apod.
   Jedná se zejména o vzorce pro výpočet hodnot veličin na základě hodnot jiných
   veličin a podmínky konstruovatelnosti útvaru (viz dále).
   Pokud si uživatel během práce s aplikací vytvoří např. více zmíněných
   obdélníků, pak všechny tyto obdélníky budou sdílet **jedinou** instanci
   této třídy, protože vzorce pro výpočet hodnot veličin i podmínky
   konstruovatelnosti jsou pro všechny obdélníky stejné a nezávislé na
   konkrétních hodnotách těchto veličin.
   - *UserShape* - instance této třídy reprezentuje konkrétní útvar vytvořený
   uživatelem a je pro každý útvar **jedinečná**, protože obsahuje **konkrétní
   hodnoty jeho metrických veličin**.
   Tzn., že pokud si uživatel během práce s aplikací vytvoří např. pět
   obdélníků, pak bude existovat pět instancí této třídy, které budou sdílet
   jednu a tutéž instanci třídy *GeometricShape*, jak jsem již uvedl výše.
   
   V dokumentačních komentářích ve zdrojovém kódu používám pro větší názornost
   a lepší rozlišení mezi instancemi těchto dvou tříd VELKÁ PÍSMENA - u všeho,
   co se týká instance třídy *GeometricShape*, píšu 'GEOMETRICKÝ' a u všeho,
   co se týká instance třídy *UserShape*, píšu 'UŽIVATELSKÝ', resp. jiný tvar
   těchto slov dle daného kontextu.
3. *main.py* - obsahuje funkce pro ovládání aplikace uživatelem pomocí textového
   uživatelského rozhraní.

## Používání aplikace

Pro použití aplikace je třeba mít na daném zařízení nainstalován Python, ideálně
ve verzi 3.10 nebo vyšší. Dále je třeba mít v konkrétním adresáři stažené
soubory s jednotlivými moduly *textfiles.py*, *shape.py* a *main.py*, textovým
souborem *list_of_shapes.txt* a podadresářem *geometric_shapes*, který obsahuje
textové soubory k jednotlivým geometrickým útvarům, s nimiž můžeme v aplikaci
pracovat.

Pokud se v příkazovém řádku nacházíme uvnitř složky se zmíněnými moduly,
aplikaci spustíme příkazem:

```python main.py```

Zobrazí se úvodní informace a textové menu. Ovládání aplikace je jednoduché
a intuitivní.
Aplikace obsahuje též jednoduchou nápovědu.

Prostřednictvím volby 'Vytvořit nový útvar' přístupné zadáním písmene 'v' nebo
'V' nás aplikace provede vytvořením nového geometrického útvaru.
Zobrazí se seznam dostupných útvarů, z nějž si jeden zvolíme zadáním jeho názvu
(bez diakritiky) a v dalším kroku mu přidělíme náš uživatelský název.
Tím je útvar vytvořen a aplikace se vrátí do hlavního menu.

Pokud zvolíme 'Moje útvary', aplikace zobrazí seznam našich útvarů, které jsme
vytvořili - v případě, že máme vytvořen zatím jen jediný, zobrazí se pouze
tento.
Napíšeme název, který jsme útvaru přidělili a potvrdíme klávesou Enter.
Aplikace zobrazí seznam značek veličin útvaru, kterým můžeme začít přiřazovat
hodnoty volbou 'Zadat novou hodnotu veličiny a automaticky přepočítat'.

Hodnoty se zadávají ve formátu:

```značka_veličiny = číslo```

tedy například:

```a = 10```

pokud daný útvar má veličinu se značkou ```a```.

U značek veličin se rozlišují malá a velká písmena.
Například pro zadání obsahu musíme napsat velké S.

Pokud budeme zadávat desetinné číslo, jako oddělovač desetinných míst použijeme
**tečku**, nikoli čárku!
Například:

```a = 7.5```

Mezery kolem znaku ```=``` nejsou nutné - slouží pouze k lepší přehlednosti
zadávaných hodnot. Všechny čtyři následující příklady přiřazení hodnoty
```10``` veličině ```a``` jsou platné a ekvivalentní:

```a=10```, ```a= 10```, ```a =10```, ```a = 10```.

Hodnoty se zadávají bez jednotek.
Záleží na nás, jestli daná čísla budou představovat centimetry, metry, kilometry
nebo cokoli jiného.

Přiřazení hodnoty další veličině provedeme opakováním stejné volby 'Zadat novou
hodnotu veličiny a automaticky přepočítat'.
Takto můžeme pokračovat, dokud aplikace nebude mít dostatek vstupních údajů
k tomu, že hodnoty všech ostatních veličin našeho útvaru dopočítá.

Pokud si nebudeme jistí, kterou veličinu daná značka reprezentuje, použijeme
volbu 'Podrobný výpis veličin včetně jejich popisů'.

V řadě případů nám bude stačit zadat pouze dvě hodnoty - u obdélníku např. délky
stran.
U některých útvarů stačí zadat pouze jedinou hodnotu - např. u kruhu (poloměr,
průměr, obvod nebo obsah) a všechny zbývající se dopočítají ihned poté.

Velikosti úhlů se zadávají ve stupních.
Například:

```alfa = 30```

Vypočítané výsledky všech veličin se zaokrouhlují na 4 desetinná místa.

Kdykoli se můžeme vrátit do hlavního menu, vytvářet útvary nové, nebo se vracet
k těm, které jsme vytvořili dříve.
Aplikace si je bude pamatovat, dokud se nerozhodneme některé vymazat, nebo dokud
práci s aplikací neukončíme.

## Textové soubory s vlastnostmi geometrických útvarů

Každý jeden textový soubor obsahuje informace o jednom konkrétním geometrickém
útvaru.
Název textového souboru odpovídá názvu geometrického útvaru tak, jak se spolu
s ostatními dostupnými geometrickými útvary zobrazí uživateli aplikace, když
si mezi nimi bude vybírat, a jak jej také napíše do příkazového řádku.
Proto by tento název měl být co nejjednodušší, bez diakritiky a velkých písmen.

### Konvence pro tvorbu textových souborů

- Textový soubor musí obsahovat čtyři sekce: DESCRIPTIVE_NAME, QUANTITIES,
FORMULAS a CONDITIONS a to v tomto pořadí.
- Vyjma těchto čtyř oddílů nesmí textový soubor obsahovat nic jiného, kromě
komentářů a prázdných řádků (viz dále).
- Každá sekce musí být uvozena textem 'Section: ' (např. 'Section: FORMULAS').
Tento text musí být na samostatném řádku.
- Každý jednotlivý údaj v libovolné sekci musí být napsán **na jednom řádku**,
tzn. že řádky nesmí být zalamovány.
- Kdekoli v textovém souboru jsou povoleny komentáře a prázdné řádky - program
je bude ignorovat.
- Komentář začíná znakem '#' a sahá po konec řádku, na kterém se tento znak
nachází.

#### Sekce DESCRIPTIVE_NAME

Tato část textového souboru obsahuje jediný údaj, a sice **popisný název
geometrického útvaru** včetně případné diakritiky a mezer.
Tento text aplikace zobrazuje na místech, kde je vhodné poskytnout uživateli
přesnější a přívětivější informaci o typu geometrického útvaru, se kterým
pracuje nebo se chystá pracovat (např. při tvorbě nového útvaru).

#### Sekce QUANTITIES

Tento část textového souboru obsahuje seznam metrických veličin geometrického
útvaru, kterým může uživatel přiřazovat hodnoty nebo jejichž hodnoty budou
aplikací vypočítány.

Každý řádek odpovídá jedné veličině, kde jsou uvedeny její vlastnosti oddělené
znakem '|' v následujícím pořadí:

značka veličiny| krátký popis veličiny| delší popis veličiny| text 'angle',
pokud daná veličina reprezentuje úhel (pokud ne, řádek zde končí).

Mezi jednotlivými položkami řádku oddělenými znakem '|' mohou být pro větší
přehlednost mezery nebo tabulátory.

Příklad:

```alfa| úhel alfa| úhel mezi stranou a a úhlopříčkou u| angle```

UPOZORNĚNÍ: U značek veličin se rozlišují malá a velká písmena!
Toto platí i pro následující oddíly (FORMULAS a CONDITIONS).

#### Sekce FORMULAS

Tento oddíl obsahuje seznam vzorců, které jsou zapotřebí k tomu, aby při
postačujícím počtu libovolné kombinace uživatelem zadaných hodnot veličin bylo
možné "postupným dosazováním" do jejich pravých stran spočítat hodnoty všech
ostatních veličin geometrického útvaru, pokud je to matematicky možné.

Veškeré značky veličin ve vzorcích musí odpovídat značkám z oddílu QUANTITIES.
Operátory a funkce ve vzorcích musí odpovídat konvencím programovacího
jazyka Python - včetně prefixu 'math.' před názvem matematických funkcí nebo
konstant (např. math.sin, math.sqrt, math.pi a podobně). Na tomto místě je
vhodné připomenout, že pro umocňování se v jazyce Python používají dva znaky
hvězdičky po sobě, např. ```a ** 2```.

#### Sekce CONDITIONS

Poslední oddíl textového souboru obsahuje sadu nerovnic a jejich popisů,
které reprezentují **podmínky konstruovatelnosti** útvaru.
Při přiřazení hodnoty určité veličině uživatelem aplikace provede kontrolu, zda
je tato hodnota v souladu s ostatními již zadanými nebo vypočítanými hodnotami
jiných veličin v tom smyslu, aby útvar bylo vůbec možné zkonstruovat.

Podmínky konstruovatelnosti jsou dány sadou nerovnic, kde je každá nerovnice
uvedena na samostatném řádku, přičemž levá strana nerovnice obsahuje vždy pouze
značku jedné konkrétní veličiny.
Za nerovnicí je na témže řádku oddělovací znak '|' následovaný slovním popisem
podmínky.

Například pro pro obdélník platí, že délka jeho úhlopříčky musí být větší než
délka jeho libovolné strany a také naopak - délka jeho libovolné strany musí být
menší než délka úhlopříčky.
Odpovídající řádek týkající se této podmínky pak může vypadat např. takto:

```u > a | Délka úhlopříčky obdélníku musí být větší než délka strany a.```

Pokud se uživatel pokusí přiřadit některé veličině hodnotu, která nesplňuje
některou z podmínek, jež se této veličiny týkají, aplikace ji nepřiřadí
a informuje o této situaci uživatele včetně příslušného slovního popisu této
podmínky.

Je nutné ošetřit všechny situace, které mohou při zadávání hodnot uživatelem
nastat. Uživatel totiž může - v případě našeho zmiňovaného obdélníku - např.
zadat jeho obsah a následně obvod.
Hodnoty těchto dvou veličin jsou dostatečné k výpočtu délek stran obdélníku
a jeho ostatních veličin.
Pro obvod obdélníku ale platí, že musí být větší nebo roven než čtyřnásobek
druhé odmocniny jeho obsahu.
Proto i tento případ musí být ošetřen odpovídající podmínkou.
