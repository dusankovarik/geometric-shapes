"""
Modul obsahující třídy pro výpočty veličin útvarů

Modul obsahuje třídy:
- GeometricShape. Tato slouží k tvorbě instancí konkrétních GEOMETRICKÝCH
  útvarů, jako např. kruh, obdélník, krychle, koule apod. Třída je
  instanciována na základě textového souboru, který obsahuje popisný název
  útvaru, značky, názvy a popisy metrických veličin útvaru, vzorce pro
  výpočet hodnot veličin na základě jiných veličin, podmínky konstruovatelnosti
  útvaru a jejich popisy. Název GEOMETRICKÉHO útvaru je shodný s názvem
  příslušného textového souboru.
  Instance třídy GeometricShape bude tedy obsahovat obecné vlastnosti,
  které jsou shodné pro všechny GEOMETRICKÉ útvary stejného typu (např.
  "obdelnik") a jsou nezávislé na konkrétních hodnotách metrických veličin
  tohoto útvaru.
- UserShape. Instance této třídy jsou tvořeny na základě vstupů od uživatele
  programu. Jedná se tedy o UŽIVATELSKÉ útvary, které jsou v průběhu práce
  s programem jedinečné - uživatel si může vytvořit např. více útvarů typu
  "obdelnik", z nichž každý bude mít jiné UŽIVATELSKÉ jméno a (pravděpodobně)
  jiné hodnoty metrických veličin.
  Všechny instance UŽIVATELSKÝCH útvarů stejného typu (např. zmíněný "obdelnik")
  budou sdílet tutéž instanci třídy GeometricShape s obecnými vlastnostmi
  tohoto útvaru.
"""

import math


class GeometricShape:
    """
    Třída reprezentující rovinný nebo prostorový GEOMETRICKÝ útvar
    """

    def __init__(self, geom_shape_name, geom_descriptive_name, quantities,
                 formulas, conditions):
        """
        Konstruktor GEOMETRICKÉHO útvaru

        :param geom_shape_name: geometrický název útvaru bez diakritiky: str
        :param geom_descriptive_name: popisný název útvaru včetně případné
        diakritiky a mezer
        :param quantities: veličiny útvaru: list
        :param formulas: vzorce pro výpočet hodnot veličin: list
        :param conditions: podmínky konstruovatelnosti útvaru: list
        """

        # geometrický název útvaru - slouží v programu jako jeho identifikátor
        self.geom_shape_name = geom_shape_name

        # popisný název útvaru včetně případné diakritiky a mezer -
        # vhodný pro uživatelské výpisy
        self.geom_descriptive_name = geom_descriptive_name

        # datová struktura s veškerými obecnými vlastnostmi útvaru
        # (značky, názvy a popisy veličin, vzorce pro výpočet veličin,
        # podmínky konstruovatelnosti)
        self.general_properties = dict()

        # inicializace obecných vlastností geometrických veličin útvaru
        self._initialize_general_properties(quantities)

        # příprava a vložení vzorců pro výpočet hodnot veličin útvaru do datové
        # struktury general_properties
        self._insert_formulas(formulas)

        # příprava a vložení podmínek pro kontrolu vzájemné konzistence veličin
        # (podmínek konstruovatelnosti útvaru) do datové struktury
        # general_properties
        self._insert_conditions(conditions)

        # celkový počet geometrických veličin útvaru
        self.total_number_of_quantities = len(self.general_properties)

    def _initialize_general_properties(self, quantities):
        """
        Inicializuje hlavní datovou strukturu (seznam) general_properties.

        Geometrická značka každé veličiny bude klíčem vnořeného slovníku,
        jehož položky budou reprezentovat obecné vlastnosti této veličiny.
        K některým těmto vlastnostem metoda rovnou přiřadí hodnoty a k ostatním
        pouze prázdné seznamy, jejichž obsah bude připraven a vložen jinými
        metodami.

        :param quantities: matematické veličiny útvaru: list
        :return: None
        """

        for quantity_symbol, short_name, description, *is_angle in quantities:
            quantity = dict()

            quantity['short_name'] = short_name
            quantity['description'] = description
            quantity['is_angle'] = is_angle == ['angle']
            quantity['countable_by'] = []
            quantity['conditions'] = []

            self.general_properties[quantity_symbol] = quantity

    def _insert_formulas(self, formulas):
        """
        Zpracuje a vloží do general_properties vzorce pro výpočet veličin

        :param formulas: seznam vzorců pro výpočet veličin útvaru
        :return: None
        """

        processed_formulas = self._process_expressions(formulas, '=')

        for symbol, expression, variables in processed_formulas:
            item = dict()

            item['variables'] = variables
            item['expression'] = expression

            self.general_properties[symbol]['countable_by'].append(item)

    def _insert_conditions(self, conditions):
        """
        Zpracuje a vloží do general_properties podmínky konstruovatelnosti

        :param conditions: podmínky konstruovatelnosti útvaru: list
        :return: None
        """

        inequalities = []
        descriptions = []
        for inequality, description in conditions:
            inequalities.append(inequality.strip())
            descriptions.append(description.strip())

        processed_inequalities = self._process_expressions(inequalities, ' ')

        counter = 0
        for symbol, expression, variables in processed_inequalities:
            item = dict()

            item['variables'] = variables
            item['expression'] = expression
            item['description'] = descriptions[counter]

            self.general_properties[symbol]['conditions'].append(item)
            counter += 1

    def _process_expressions(self, expressions, split_char):
        """
        Vrátí seznam zpracovaných výrazů

        Výrazem se myslí vzorec (rovnice) pro výpočet některé veličiny útvaru
        nebo podmínka (nerovnice) pro kontrolu konstruovatelnosti útvaru.

        Výsledný seznam se bude skládat z vnořených seznamů ve formátu:
        [značka veličiny na levé straně výrazu: string,
        pravá strana výrazu se značkami veličin vnořených do složených
        závorek: string,
        množina značek veličin na pravé straně výrazu: set of strings].

        :param expressions: výrazy ke zpracování: list
        :param split_char: znak, podle jehož prvního výskytu se každý výraz
        v seznamu bude splitovat na levou a pravou stranu
        :return: zpracované výrazy: list
        """

        processed_expressions = []

        for left_side, right_side in [expression.split(split_char, 1)
                                      for expression in expressions]:
            # založíme nový seznam tím, že do něj rovnou vložíme značku
            # veličiny z levé strany výrazu
            processed_expression = [left_side.strip()]

            stripped_right_side = right_side.strip()
            processed_right_side = self._process_expression(stripped_right_side)

            # přidáme do seznamu zpracovanou pravou stranu výrazu
            processed_expression.append(processed_right_side)

            variables = self._parse_quantities(processed_right_side)

            # nakonec přidáme do seznamu množinu se značkami veličin
            # z pravé strany výrazu
            processed_expression.append(variables)

            # seznam vložíme jako vnitřní položku do seznamu všech
            # zpracovávaných veličin
            processed_expressions.append(processed_expression)

        return processed_expressions

    def _process_expression(self, expression):
        """
        Ohraničí značky veličin ve výrazu složenými závorkami

        Např. pro výraz:
        'b / math.tan(alfa)'
        vrátí:
        '{b} / math.tan({alfa})'

        :param expression: výraz ke zpracování: str
        :return: výraz s proměnnými ohraničenými složenými závorkami: str
        """

        # znaky, které mohou následovat za názvem proměnné nebo mu předcházet
        valid_neighbor_chars = ' +-*/%=!<>()'

        # vložení mezery před a za řetězec expression kvůli snadnějšímu
        # zpracování (nemusíme na okrajích řetězce hlídat překročení
        # hranic indexu znaku)
        expression = ' ' + expression + ' '

        # řetězec se zpracovaným výrazem
        processed_expression = ''

        # začínáme od indexu 1, protože na okraje jsme přidali znaky mezery
        i = 1
        while i < len(expression) - 1:  # na pravém okraji je též mezera
            if self._valid_char(expression[i], True):  # možný začátek názvu
                start = i
                quantity_name = expression[i]
                i += 1
                while self._valid_char(expression[i], False):
                    quantity_name += expression[i]
                    i += 1
                end = i  # jsme na konci potenciálního názvu proměnné

                # kontrola, zda nejde například o název funkce z knihovny
                # math apod. - aby nalezený substring reprezentoval
                # proměnnou, musí mít před i za sebou některý ze znaků
                # z řetězce valid_neighbor_chars
                if (expression[start - 1] in valid_neighbor_chars) \
                        and (expression[end] in valid_neighbor_chars):
                    processed_expression += '{' + expression[start:end] + '}'
                else:
                    processed_expression += expression[start:end]
            else:
                processed_expression += expression[i]
                i += 1

        return processed_expression

    @staticmethod
    def _valid_char(char, is_first_char):
        """
        Zvaliduje znak, který je součástí názvu veličiny

        :param char: znak, který validujeme: str
        :param is_first_char: jde o znak na začátku názvu veličiny?: bool
        :return: může validovaný znak být součástí názvu veličiny?: bool
        """

        o = ord(char)
        # znak v názvu veličiny může být malé nebo velké písmeno anglické
        # abecedy nebo znak podtržítka
        is_letter = (o >= ord('a')) and (o <= ord('z')) or \
                    (o >= ord('A')) and (o <= ord('Z')) or (char == '_')
        if is_first_char:
            return is_letter

        # znak v názvu veličiny může být číslice, pokud není na jeho začátku
        is_digit = (o >= ord('0')) and (o <= ord('9'))
        return is_letter or is_digit

    @staticmethod
    def _parse_quantities(expression):
        """
        Vrátí množinu se značkami veličin, které jsou obsaženy ve výrazu

        Výraz musí mít značky veličin ohraničeny složenými závorkami.

        :param expression: výraz se značkami veličin: str
        :return: značky těchto veličin: set of strings
        """

        quantities = set()
        parse = False
        quantity_symbol = ''
        for char in expression:
            if char == '{':
                # aktivuje režim parsování
                parse = True
            elif char == '}':
                # deaktivuje režim parsování a právě naparsovanou značku
                # veličiny přidá do množiny, kterou metoda vrací
                parse = False
                quantities.add(quantity_symbol)
                quantity_symbol = ''
            elif parse:
                # je-li aktivní režim parsování, přidá znak do názvu značky
                # veličiny
                quantity_symbol += char

        return quantities


class UserShape:
    """
    Třída reprezentující UŽIVATELSKÝ útvar, který obsahuje instanci
    GEOMETRICKÉHO útvaru třídy GeometricShape.
    """

    def __init__(self, user_shape_name, geom_shape_instance):
        """
        Konstruktor konkrétního UŽIVATELSKÉHO útvaru

        :param user_shape_name: UŽIVATELSKÝ název geometrického útvaru
        :param geom_shape_instance: odkaz na instanci příslušného GEOMETRICKÉHO
        útvaru
        """
        self.user_shape_name = user_shape_name
        self.geom_shape_instance = geom_shape_instance

        # název GEOMETRICKÉHO útvaru zkopírovaný z instance třídy
        # GeometricShape, aby byl jednodušeji přístupný i jako atribut instance
        # této třídy
        self.geom_shape_name = geom_shape_instance.geom_shape_name

        # popisný název útvaru včetně případné diakritiky a mezer -
        # vhodný pro uživatelské výpisy, rovněž zkopírovaný z instance třídy
        # GeometricShape kvůli snadnější přístupnosti ve zdejší třídě
        self.geom_descriptive_name = geom_shape_instance.geom_descriptive_name

        # slovník, do kterého se budou postupně ukládat konkrétní hodnoty
        # geometrických veličin UŽIVATELSKÉHO útvaru v okamžiku, kdy budou známé
        # (zadané nebo vypočítané)
        self.quantity_values = dict()

        # provede inicializaci slovníku quantity_values tím, že nastaví
        # vnořené položky na výchozí hodnoty
        # metoda se používá i zvnějšku, když se uživatel rozhodne smazat
        # všechny veličiny svého útvaru
        self.delete_quantity_values()

        # počet známých hodnot veličin UŽIVATELSKÉHO útvaru, který bude stoupat
        # spolu s tím, jak bude uživatel tyto hodnoty zadávat a jak se na
        # základě těchto zadaných hodnot budou dopočítávat ostatní
        self.number_of_known_quantities = 0

        # celkový počet geometrických veličin, které jsou definovány
        # v odpovídajícím GEOMETRICKÉM útvaru - jde o zkopírovanou hodnotu
        # z instance tohoto GEOMETRICKÉHO útvaru, aby byla jednodušeji
        # přístupná i přímo z instance této třídy
        self.total_number_of_quantities \
            = geom_shape_instance.total_number_of_quantities

        # poslední zpráva s textem popisujícím výsledek pokusu, resp. příčinu
        # neúspěchu, při přiřazení hodnoty některé veličině uživatelem
        self.last_condition_message = ''

    def delete_quantity_values(self):
        """
        Vymaže všechny hodnoty veličin UŽIVATELSKÉHO útvaru

        Metoda uvede slovník s hodnotami veličin UŽIVATELSKÉHO útvaru
        quantity_values do výchozího stavu. Používá se při první inicializaci
        tohoto slovníku při založení instance UŽIVATELSKÉHO útvaru nebo
        zvnějšku, pokud se uživatel rozhodne všechny veličiny svého útvaru
        smazat.

        Metoda též vynuluje počitadlo známých hodnot veličin tohoto útvaru.

        :return: None
        """
        self.quantity_values = dict()

        for quantity_symbol in self.geom_shape_instance.general_properties:
            quantity = dict()

            quantity['has_value'] = False
            quantity['value'] = None

            self.quantity_values[quantity_symbol] = quantity

        self.number_of_known_quantities = 0

    def quantity_exists(self, quantity_symbol):
        """
        Ověří, zda UŽIVATELSKÝ útvar obsahuje danou veličinu

        Metoda se pokusí vyhledat značku veličiny z parametru quantity_symbol
        ve slovníku s hodnotami veličin UŽIVATELSKÉHO útvaru quantity_values.

        :param quantity_symbol: značka veličiny útvaru: str
        :return: zda útvar obsahuje veličinu s touto značkou: bool
        """
        return quantity_symbol in self.geom_shape_instance.general_properties

    def quantity_has_value(self, quantity_symbol):
        """
        Ověří, zda daná veličina již má přiřazenou hodnotu

        Metoda ověří, zda veličina UŽIVATELSKÉHO útvaru, jejíž značka je
        předána parametrem quantity_symbol, již má přiřazenou (nebo vypočítanou)
        hodnotu.

        :param quantity_symbol: značka veličiny útvaru: str
        :return: zda odpovídající veličina již má přiřazenou hodnotu: bool
        """
        return self.quantity_values[quantity_symbol]['has_value']

    def value_meets_conditions(self, quantity_symbol, value):
        """
        Ověří, zda zadaná hodnota splňuje podmínky konstruovatelnosti

        Metoda ověří, jestli hodnota, kterou se uživatel pokouší přiřadit
        veličině určené značkou z parametru quantity_symbol, splňuje podmínky
        konstruovatelnosti útvaru. To znamená, že každá nově zadaná hodnota
        některé veličiny uživatelova útvaru musí být v souladu s obecnými
        matematickými pravidly (například délkové veličiny musí být kladné,
        úhly se musí pohybovat u určitých mezích apod.), ale také s hodnotami
        ostatních veličin útvaru, které jsou již známé (zadané nebo vypočítané).
        Například není možné zkonstruovat (sestrojit) obdélník, jehož strana
        má délku větší nebo rovnu, než kolik tvoří polovina jeho obvodu apod.

        :param quantity_symbol: značka veličiny útvaru: str
        :param value: přiřazovaná hodnota: float
        :return: zda je přiřazovaná hodnota v souladu s podmínkami: bool
        """
        if value <= 0.0:
            self.last_condition_message = 'Hodnota musí být větší než nula.'
            return False

        is_angle = self.get_property(quantity_symbol, 'is_angle')
        if is_angle and value >= math.pi:
            self.last_condition_message \
                = 'Hodnota úhlu musí být menší než 180 stupňů.'
            return False

        conditions = self.get_property(quantity_symbol, 'conditions')
        if not conditions:
            self.last_condition_message = 'Implicitní podmínky pro zadanou ' \
                                          'hodnotu jsou splněny, explicitní ' \
                                          'podmínky nejsou definovány.'
            return True

        return self._check_explicit_conditions(value, conditions)

    def _check_explicit_conditions(self, value, conditions):
        """
        Ověří, zda přiřazovaná hodnota splňuje explicitní podmínky

        Metoda je volána z metody value_meets_conditions a ověřuje, zda
        hodnota, kterou se pokoušíme přiřadit určité veličině, splňuje
        právě ty podmínky, které vyplývají z jiných - již přiřazených nebo
        vypočítaných - hodnot jiných veličin útvaru. Tyto podmínky zde
        označujeme jako explicitní.

        :param value: přiřazovaná hodnota: float
        :param conditions: explicitní podmínky konstruovatelnosti útvaru: list
        :return: zda je přiřazovaná hodnota v souladu s explicitními podmínkami:
        bool
        """
        for condition in conditions:
            if self._quantities_have_values(condition['variables']):
                expression = condition['expression']
                substituted_expression = self._substitute_expression(expression)
                inequality = str(value) + ' ' + substituted_expression
                if not eval(inequality):
                    self.last_condition_message = condition['description']
                    return False

        self.last_condition_message = 'Implicitní i explicitní podmínky pro ' \
                                      'zadanou hodnotu jsou splněny.'
        return True

    def assign_value_and_recalculate(self, quantity_symbol, value):
        """
        Přiřadí hodnotu veličině útvaru a vypočítá hodnoty dalších veličin

        Metoda přiřadí uživatelem zadanou hodnotu veličině, jejíž značka
        je dána parametrem quantity_symbol, a následně vypočítá hodnoty
        těch veličin útvaru, které dosud žádnou neměly, a které na základě
        sady známých veličin rozšířené právě o tuto novou hodnotu vypočítat lze.
        Pokud se podaří spočítat minimálně jednu novou hodnotu dosud neznámé
        veličiny, sada známých veličin se opět rozšíří a cyklus s pokusem
        o výpočet dalších hodnot se opakuje. Toto opakování se děje až do
        okamžiku, kdy již není možné spočítat žádnou novou hodnotu, nebo kdy
        jsou hodnoty všech veličin útvaru známé.

        :param quantity_symbol: značka veličiny útvaru: str
        :param value: přiřazovaná hodnota: float
        :return: None
        """

        # přiřadíme hodnotu příslušné veličině a označíme ji jako známou
        self.quantity_values[quantity_symbol]['value'] = value
        self.quantity_values[quantity_symbol]['has_value'] = True
        self.number_of_known_quantities += 1

        new_calculated_values = -1
        # cyklus počítající nové hodnoty na základě právě přiřazené uživatelem
        # nebo vypočítaných právě v průběhu cyklu
        # cyklus bude běžet, pokud se během jeho předchozí iterace podařilo
        # spočítat minimálně jednu novou hodnotu, a zároveň pokud všechny
        # hodnoty veličin útvaru nejsou spočítané
        while new_calculated_values != 0 and \
                self.number_of_known_quantities \
                != self.total_number_of_quantities:
            new_calculated_values = 0
            for quantity_symbol, properties in self.quantity_values.items():
                if not properties['has_value']:
                    if self._try_to_calculate_value(quantity_symbol):
                        new_calculated_values += 1

    def get_property(self, quantity_symbol, property_name):
        """
        Vrátí hodnotu vnořené položky slovníku general_properties

        Jedná se o pomocnou metodu sloužící ke snadnějšímu získání vnořené
        hodnoty ze slovníku general_properties, což je instanční proměnná třídy
        GeometricShape obsahující všechny obecné informace o veličinách
        GEOMETRICKÉHO útvaru, na nějž instance UŽIVATELSKÉHO útvaru (instanční
        proměnná této třídy) obsahuje odkaz.

        Metoda vrátí hodnotu položky vnořeného slovníku ve slovníku
        general_properties, který odpovídá veličině útvaru dané parametrem
        quantity_symbol.

        :param quantity_symbol: značka veličiny útvaru: str
        :param property_name: klíč položky vnořeného slovníku odpovídajícího
        veličině dané parametrem quantity_symbol: str
        :return: hodnota položky vnořeného slovníku odpovídajícího veličině
        dané parametrem quantity_symbol
        """
        return self.geom_shape_instance. \
            general_properties[quantity_symbol][property_name]

    def _try_to_calculate_value(self, quantity_symbol):
        """
        Pokusí se spočítat hodnotu konkrétní veličiny útvaru

        Metoda spočítá a přiřadí hodnotu veličině útvaru určené parametrem
        quantity_symbol, pokud je to možné na základě jiných veličin
        s již přiřazenou hodnotou. V případě úspěchu vrátí True, v případě
        neúspěchu False.

        :param quantity_symbol: značka veličiny útvaru: str
        :return: zda se podařilo spočítat příslušnou hodnotu: bool
        """
        countable_by = self.get_property(quantity_symbol, 'countable_by')

        # pokud hodnota vnořeného slovníku GEOMETRICKÉHO útvaru náležícího
        # veličině určené parametrem quantity_symbol s klíčem 'countable_by'
        # je prázdný seznam, potom ji není možné spočítat na základě hodnot
        # jiných veličin, ale může být pouze zadána uživatelem
        if not countable_by:
            return False

        # cyklus projde všechny způsoby, kterými je možné hodnotu veličiny
        # spočítat na základě jiných známých hodnot (nebo na základě hodnot,
        # u kterých lze předpokládat, že dojde k jejich výpočtu v jiné
        # iteraci cyklu uvnitř metody assign_value_and_recalculate())
        for way in countable_by:
            if self._quantities_have_values(way['variables']):
                self._calculate_value(quantity_symbol, way['expression'])
                return True

        return False

    def _calculate_value(self, quantity_symbol, input_expression):
        """
        Vypočítá hodnotu veličiny na základě předaného výrazu

        Metoda vypočítá a přiřadí hodnotu veličiny útvaru určené parametrem
        quantity_symbol, označí ji jako známou (...['has_value'] = True)
        a inkrementuje instanční proměnnou number_of_known_quantities.
        Výpočet se provede na základě předaného matematického výrazu
        input_expression, získaného z hlavního slovníku GEOMETRICKÉHO
        útvaru general_properties, jež je instanční proměnnou třídy
        GeometricShape. Do tohoto výrazu se dosadí hodnoty příslušných
        veličin a poté se vyhodnotí.

        :param quantity_symbol: značka veličiny útvaru: str
        :param input_expression: výraz pro výpočet hodnoty této veličiny:
        str
        :return: None
        """

        # symboly veličin ve výrazu nahradíme jejich hodnotami
        substituted_expression = self._substitute_expression(input_expression)

        # takto substituovaný výraz vyhodnotíme a získanou hodnotu přiřadíme
        self.quantity_values[quantity_symbol]['value'] \
            = eval(substituted_expression)
        self.quantity_values[quantity_symbol]['has_value'] = True

        self.number_of_known_quantities += 1

    def _quantities_have_values(self, variables):
        """
        Ověří, zda množina veličin má přiřazené hodnoty

        Metoda ověří, zda množina veličin potřebných k výpočtu hodnoty jiné
        veličiny útvaru, nebo ke kontrole konzistence (konstruovatelnosti)
        útvaru, již má přiřazené (nebo vypočítané) hodnoty. Tato množina
        pochází z některé vnořené položky slovníku general_properties, která
        je instanční proměnnou třídy GeometricShape, a náleží právě té
        veličině, kterou lze na základě hodnot veličin uvnitř množiny spočítat,
        nebo ověřit, zda může nabýt uživatelem zadané hodnoty.

        :param variables: množina značek veličin: set of strings
        :return: zda mají všechny veličiny v množině variables přiřazené
        hodnoty: bool
        """

        # pokud je množina variables prázdná, potom z matematického hlediska
        # nelze říci, že by některý z jejích prvků neměl přiřazenou hodnotu;
        # z praktického hlediska to znamená, že hodnotu jiné veličiny, která
        # se k této množině vztahuje, lze spočítat, nebo lze ověřit podmínky
        # konstruovatelnosti útvaru, nezávisle na jiných veličinách, a proto
        # můžeme vrátit True
        if not variables:
            return True

        for variable in variables:
            if not self.quantity_values[variable]['has_value']:
                return False

        return True

    def _substitute_expression(self, expression):
        """
        Nahradí značky veličin hodnotami veličin útvaru

        Metoda přijme string s matematickým výrazem, v němž jsou značky
        veličin útvaru ohraničeny složenými závorkami, a vytvoří nový string,
        kde budou tyto značky (včetně jejich ohraničujících složených závorek)
        nahrazeny hodnotami odpovídajících veličin útvaru, který vrátí.

        :param expression: matematický výraz se značkami veličin ohraničených
        složenými závorkami: string
        :return: matematický výraz s hodnotami příslušných veličin místo jejich
        značek a složených závorek: string
        """
        substituted_expression = ''
        substitute = False
        substituted_variable = ''
        for char in expression:
            if char == '{':
                # aktivuje režim substituce
                substitute = True
            elif char == '}':
                # deaktivuje režim substituce a do substituovaného výrazu
                # dosadí hodnotu příslušné veličiny
                substitute = False
                substituted_expression \
                    += str(self.quantity_values[substituted_variable]['value'])
                substituted_variable = ''
            elif substitute:
                # je-li aktivní režim substituce, přidá znak do názvu proměnné
                substituted_variable += char
            else:
                substituted_expression += char

        return substituted_expression
