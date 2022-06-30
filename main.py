"""
Modul s textovým uživatelským rozhraním

Modul obsahuje funkce pro textové uživatelské rozhraní aplikace.
Aplikace tedy běží v příkazovém řádku nebo terminálu. Uživatel
program ovládá pomocí menu, po jejichž zobrazení je vyzván
k volbě zadáním jednoho písmene, které danou volbu reprezentuje,
s následným potvrzením klávesou ENTER.
Na jiných místech je uživatel vyzván k zadání textového řetězce,
který reprezentuje např. UŽIVATELSKÝ název útvaru nebo výraz,
pomocí nějž se vybrané veličině přiřazuje hodnota.
"""

import math
import textfiles
from shape import GeometricShape, UserShape


# Verze aplikace
VERSION = '1.0.0'

# Zdroj ke stažení zdrojového kódu aplikace
installation_resource = ''  # todo doplnit

# Druhy geometrických útvarů dostupných na tomto zařízení dle
# obsahu textového souboru 'list_of_shapes.txt'
geometric_shapes = dict()

# Slovník s konkrétními geometrickými útvary vytvořenými uživatelem
user_shapes = dict()

# Poslední chybová zpráva pro jakoukoli část modulu
last_error_message = {
    'error': False,
    'text': ''
}

# Počet desetinných míst, na který se budou zaokrouhlovat
# hodnoty veličin útvaru při jejich výpisu
ROUND_DECIMALS = 4

# Proměnná continue_app je kontrolována na začátku hlavní smyčky
# aplikace. Pokud nabude hodnoty False, aplikace se ukončí.
continue_app = True

# Proměnná continue_user_shape_work je kontrolována ve smyčce
# pro práci s vybraným UŽIVATELSKÝM útvarem. Pokud nabude hodnoty
# False, program se vrátí do hlavní smyčky s hlavním menu.
continue_user_shape_work = True

# Proměnná detailed_last bude mít hodnotu True, pokud byl během práce
# s útvarem naposled použit podrobný výpis veličin pomocí funkce
# detailed_last_overview, aby se poté znovu nevypsal běžný výpis
detailed_last = False

# Uvítací text po spuštění aplikace pomocí tohoto textového rozhraní
invitation = f'Vítejte v programu Shapes verze {VERSION}!\n\n' \
             f'Tato verze používá textové uživatelské rozhraní, které ' \
             f'běží v okně příkazového řádku.\n\n' \
             f'Program Shapes slouží k výpočtu hodnot veličin ' \
             f'geometrických útvarů a funguje tak, že z libovolné ' \
             f'kombinace uživatelem zadaných veličin, z níž je ' \
             f'matematicky možné spočítat hodnoty jiných veličin, ' \
             f'program Shapes tyto hodnoty dokáže spočítat. Můžete ' \
             f'zadat například strany obdélníku a program spočítá jeho ' \
             f'obvod, obsah, délku úhlopříčky a úhly mezi stranami a ' \
             f'úhlopříčkami, ale stejně tak můžete zadat například ' \
             f'obvod a délku úhlopříčky a program spočítá délky stran ' \
             f'a rovněž všechny zbývající veličiny.\n\n' \
             f'Podrobnější informace získáte volbou \'Nápověda\' a ' \
             f'v dokumentaci k programu.\n\n' \
             f'Volbou \'Vytvořit nový útvar\', zobrazíte ' \
             f'seznam všech geometrických útvarů, se kterými můžete ' \
             f'pracovat.\n\n' \
             f'Program je vytvořený tak, aby sami uživatelé ' \
             f'(včetně vás) do něj mohli relativně jednoduchým způsobem ' \
             f'doplňovat nové geometrické útvary pomocí prostých ' \
             f'textových souborů a aplikaci tak rozšiřovat. (Více informací ' \
             f'opět naleznete v dokumentaci.) Proto se tento seznam ' \
             f'může na různých počítačích lišit.\n\n' \
             f'Volby každého menu jsou zobrazeny velkými písmeny, ale ' \
             f'můžete používat i písmena malá!\n'


def initialize_geometric_shapes():
    """
    Inicializuje slovník s dostupnými GEOMETRICKÝMI útvary

    Funkce transformuje informace z textového souboru
    list_of_shapes.txt do slovníku, aby aplikace věděla, se kterými
    GEOMETRICKÝMI útvary může pracovat, a mohla vytvářet jejich
    instance.

    :return: None
    """
    lines = textfiles.load_text_file('list_of_shapes.txt')

    clean_lines = textfiles.get_clean_lines(lines)
    for clean_line in clean_lines:
        shape = dict()
        shape_name, full_name, path = [
            item.strip() for item in clean_line.split('|')]
        shape['full_name'] = full_name
        shape['path'] = path
        shape['is_instantiated'] = False
        geometric_shapes[shape_name] = shape

    if check_empty_geometric_shapes():
        return


def check_empty_geometric_shapes():
    """
    Zkontroluje, zda jsou k dispozici GEOMETRICKÉ útvary.

    Funkce ověří, zda jsou má aplikace k dispozici textové soubory,
    na jejichž základě může vytvářet instance GEOMETRICKÝCH a potažmo
    UŽIVATELSKÝCH útvarů.

    :return: zda má aplikace k dispozici textové soubory k vytváření útvarů:
    bool
    """
    if geometric_shapes == {}:
        fixed_width_output(f'Na vašem zařízení nejsou dostupné žádné '
                           f'geometrické útvary.\n\n'
                           f'Můžete zkusit program znovu stáhnout z '
                           f'následujícího zdroje: '
                           f'{installation_resource}.\n\n')
        global continue_app
        continue_app = False
        input('Stiskněte ENTER pro ukončení aplikace... ')
        return True


def main():
    """
    Vstupní bod a hlavní funkce aplikace

    Funkce zavolá inicializační funkce a poté spustí hlavní smyčku,
    ze které se podle uživatelových voleb budou volat jiné funkce
    potřebné pro provádění příslušných akcí.

    :return: None
    """
    initialize_geometric_shapes()
    if check_empty_geometric_shapes():
        return
    fixed_width_output(invitation)

    # volby hlavního menu
    # Hlavními klíči slovníku main_menu_options jsou klávesy, které
    # uživatel může na vstupu zadat. Vnořená položka 'description'
    # je text, který se v menu k dané volbě zobrazí a 'action' pak
    # identifikátor funkce, která se po výběru volby uživatelem zavolá.
    main_menu_options = {
        'V': {
            'description': 'Vytvořit nový útvar',
            'action': create_new_user_shape,
        },
        'M': {
            'description': 'Moje útvary',
            'action': my_shapes,
        },
        'N': {
            'description': 'Nápověda',
            'action': help_app,
        },
        'K': {
            'description': 'Konec',
            'action': quit_app,
        },
    }

    # Hlavní smyčka textového rozhraní aplikace
    while continue_app:
        action = key_command_menu(main_menu_options, 'Hlavní menu')
        if action == help_app:
            help_app('main')
        else:
            action()


def key_command_menu(options, name=''):
    """
    Zobrazí textové menu, které je možno ovládat pomocí klávesnice

    Funkce zobrazí název a volby textového menu na základě parametrů
    name a options. Uživatel bude vyzván k zadání jednopísmenné
    volby a funkce vrátí identifikátor jiné funkce, která této volbě
    odpovídá.

    :param options: volby menu, jejich popisy a odpovídající funkce:
    dict
    :param name: hlavička (název) menu: str
    :return: identifikátor funkce odpovídající uživatelem vybrané volbě:
    function
    """
    if name:
        print(name + ':\n')

    for k, v in options.items():
        print(k + ': ' + v['description'])
    print()

    user_option = ''
    invalid_choice = True

    # žádost o zadání se bude opakovat, dokud uživatel nezadá platnou
    # volbu
    while invalid_choice:
        user_option = input('Zvolte akci a stiskněte ENTER: ') \
            .strip().upper()
        if user_option in options.keys():
            invalid_choice = False
        else:
            print('Neplatná volba, zkuste to prosím znovu.')

    menu_func = options[user_option]['action']

    print()
    return menu_func


def confirm_option(prompt):
    """
    Pomocná funkce k potvrzení předchozí volby uživatelem

    Funkce zobrazí výzvu předanou v parametru prompt bezprostředně
    následovanou textem ' (A/N) ' a v případě, že uživatel zadá 'A'
    (resp. 'a'), vrátí True. V případě, že uživatel zadá 'N' (resp. 'n'),
    vrátí False.

    :param prompt: výzva zobrazená uživateli k potvrzení nebo zamítnutí:
    str
    :return: zda uživatel výzvu potvrdí nebo zamítne: bool
    """
    option = ''
    invalid_option = True

    # Uživatel bude v případě neplatné volby opakovaně vyzýván
    # k další, dokud nezadá volbu platnou
    while invalid_option:
        option = input(prompt + ' (A/N) ').strip().upper()
        if option in ['A', 'N']:
            invalid_option = False
        else:
            print('Neplatná volba, zkuste to prosím znovu.')

    return option == 'A'


def secondary_menu(prompt, crucial_options, assistive_options, capital=False):
    """
    Zobrazí pomocné menu s výzvou a pomocnými volbami

    Funkce zobrazí výzvu předanou parametrem prompt a pod ní
    "jednořádkové" menu s pomocnými kontextovými volbami předanými
    parametrem assistive_options. Platnost uživatelem zadané volby
    se ověřuje pomocí předané kolekce v parametru crucial_options.
    (Pokud může uživatel zadat libovolný text, pak funkci předáme
    v tomto parametru znak '*'.) Funkce vrátí text s platnou hodnotou
    nebo jednopísmennou pomocnou volbou.

    :param prompt: výzva zobrazená uživateli pro zadání hodnoty: str
    :param crucial_options: kolekce s platnými hodnotami, které
    uživatel může zadat: list / tuple
    :param assistive_options: pomocné kontextové menu: dict
    :param capital: zda se v zadané volbě mají ponechat velká písmena
    (tzn. nepřevádět je na malá): bool
    :return: uživatelova volba: str
    """
    fixed_width_output(prompt)

    if assistive_options:
        i = 0
        print('(', end='')
        for k, v in assistive_options.items():
            print(f'{k}: {v}', end='')
            if i < len(assistive_options)-1:
                print(', ', end='')
            else:
                print(')')
            i += 1

    # převod klíčů, které reprezentují jednopísmenné pomocné volby,
    # na malá písmena kvůli porovnávání s uživatelským vstupem, který se
    # v případě zadání pomocné volby rovněž vždy převádí na malá písmena
    assistive_options = {k.lower(): v for k, v in assistive_options.items()}

    user_option = ''
    invalid_choice = True

    # pokud uživatel zadá neplatnou volbu, výzva k zadání platné volby
    # se bude opakovat
    while invalid_choice:
        user_option = input('Vaše volba: ').strip()

        # pokud nezáleží na malých a velkých písmenech v uživatelském
        # vstupu, pak jej převedeme na písmena malá - to platí, pokud
        # to není explicitně zadáno v parametru capital nebo pokud
        # uživatel zvolí pomocnou volbu
        if not capital or user_option in assistive_options:
            user_option = user_option.lower()

        # pokud nejsou omezeny hodnoty, které uživatel může zadat,
        # pak zadanou hodnotu jednoduše vrátíme
        if crucial_options == '*' and user_option != '':
            return user_option

        # uživatelova volba je platná, pokud zadá hodnotu z kolekce
        # předané parametrem crucial_options nebo některou z pomocných
        # voleb
        if user_option in crucial_options \
                or user_option in assistive_options.keys():
            invalid_choice = False
        else:
            print('Zadali jste neplatnou volbu. Zkuste to prosím znovu.')

    return user_option


def create_new_user_shape():
    """
    Provede uživatele procesem vytvoření nového UŽIVATELSKÉHO útvaru

    Funkce nabídne uživateli dostupné GEOMETRICKÉ útvary a vyzve ho
    k volbě. Poté ho vyzve k zadání UŽIVATELSKÉHO jména zvoleného
    GEOMETRICKÉHO útvaru a pokud vše proběhne v rámci stanovených
    podmínek, vytvoří nový UŽIVATELSKÝ útvar, který je instancí
    třídy UserShape a jako instanční proměnnou obsahuje instanci
    odpovídající zvolenému GEOMETRICKÉMU útvaru, jež je instancí třídy
    GeometricShape.

    Instance třídy GeometricShape obsahuje obecné vlastnosti daného
    GEOMETRICKÉHO útvaru, které jsou pro všechny instance odpovídajících
    UŽIVATELSKÝCH útvarů tohoto typu společné a neměnné. Pokud
    instance GEOMETRICKÉHO útvaru dosud nebyla vytvořena, funkce ji
    založí. V opačném případě se do příslušné instanční proměnné
    nově vzniklého UŽIVATELSKÉHO útvaru uloží pouze reference na
    již existující instanci GEOMETRICKÉHO útvaru.

    Díky tomuto přístupu mohou různé UŽIVATELSKÉ útvary stejného
    GEOMETRICKÉHO typu sdílet jedinou instanci třídy GeometricShape.
    Uživatel tak může mít např. vytvořený libovolný počet obdélníků
    s různými názvy a hodnotami geometrických veličin (délky stran,
    velikosti úhlů mezi úhlopříčkami apod.), které budou sdílet pouze
    jednu instanci GEOMETRICKÉHO útvaru obsahující obecné vlastnosti
    všech obdélníků (jako jsou značky, názvy a popisy veličin, vzorce
    pro výpočet hodnot veličin na základě jiných veličin či podmínky
    konstruovatelnosti.)

    :return: None
    """
    fixed_width_output('Seznam dostupných geometrických útvarů na vašem '
                       'zařízení:\n')

    for geom_shape, v in geometric_shapes.items():
        print(f'{geom_shape} ({v["full_name"]})')
    print()

    # výzva uživateli k výběru GEOMETRICKÉHO útvaru
    user_option = secondary_menu(
        'Napište název geometrického útvaru ze seznamu, který chcete '
        'vytvořit.\nNapište pouze název ze začátku řádku, bez diakritiky '
        'a popisu v závorce!',
        geometric_shapes.keys(),
        {'Z': 'Návrat zpět do hlavního menu', }
    )
    if user_option == 'z':
        print()
        return

    print()
    # GEOMETRICKÝ název útvaru
    geom_shape_name = user_option

    # výzva uživateli k zadání jména svého nového UŽIVATELSKÉHO útvaru
    user_option = input_new_user_shape_name()
    if user_option == 'z':
        print()
        return

    # UŽIVATELSKÝ název útvaru
    user_shape_name = user_option

    # Pokud uživatelem zvolený geometrický útvar není instanciovaný,
    # pak se tato instance vytvoří a reference na ni se uloží
    # do globálního slovníku geometric_shapes
    if not geometric_shapes[geom_shape_name]['is_instantiated']:
        # získání inicializačních informací GEOMETRICKÉHO útvaru
        # z příslušného textového souboru
        path = geometric_shapes[geom_shape_name]['path']
        filename = geom_shape_name
        shape_init_data = textfiles.shape_init_list_from_text_file(
            path, filename)

        # destrukturace (unpacking) inicializačních dat pro konstruktor
        geom_full_name, quantities, formulas, conditions = shape_init_data

        # vytvoření instance GEOMETRICKÉHO útvaru
        geometric_shape_instance = GeometricShape(
            geom_shape_name, geom_full_name, quantities, formulas, conditions)

        # označení instance daného GEOMETRICKÉHO útvaru jako vytvořené
        # a uložení reference na ni do globálního slovníku geometric_shapes
        geometric_shapes[geom_shape_name]['is_instantiated'] = True
        geometric_shapes[geom_shape_name][
            'instance'] = geometric_shape_instance

    # Pokud uživatelem zvolený geometrický útvar je instanciovaný,
    # pak jsou všechny jeho vlastnosti (značky a popisy veličin,
    # vzorce i podmínky konzistence) obecné a pro více instancí
    # uživatelských útvarů tohoto geometrického útvaru společné.
    # Více uživatelských instancí stejného geometrického útvaru tedy
    # může sdílet jedinou instanci tohoto geometrického útvaru.
    # Proto se reference na tuto instanci pouze zkopíruje z příslušné
    # položky globálního slovníku geometric_shapes.
    else:
        geometric_shape_instance = geometric_shapes[
            geom_shape_name]['instance']

    # Do globálního slovníku user_shapes se uloží pouze uživatelem zvolené
    # jméno útvaru, které bude klíčem jeho položky. Hodnotou této položky
    # pak bude reference na instanci příslušného UŽIVATELSKÉHO útvaru,
    # která se vytvoří.
    # Instance UŽIVATELSKÉHO útvaru obsahuje referenci na příslušný
    # GEOMETRICKÝ útvar jako svoji instanční proměnnou.
    user_shape_instance = UserShape(user_shape_name, geometric_shape_instance)
    user_shapes[user_shape_name] = user_shape_instance

    fixed_width_output(f'Geometrický útvar {geom_shape_name} s názvem '
                       f'{user_shape_name} byl vytvořen.')
    print()


def input_new_user_shape_name():
    """
    Požádá uživatele o zadání jména nového útvaru, které vrátí

    Pomocná funkce, která se zavolá při tvorbě nového útvaru. Požádá
    uživatele o zadání jména útvaru, zvaliduje jeho platnost,
    a v případě platného a současně unikátního jména ho vrátí.
    V opačném případě vypíše chybové hlášení a proces se bude
    opakovat, dokud uživatel nezadá platnou volbu, což může být
    i příkaz ke zrušení celého procesu tvorby nového útvaru
    a návratu do hlavního menu.

    :return: UŽIVATELSKÉ jméno nového útvaru nebo volba z pomocného
    menu: str
    """
    user_option = ''
    invalid_choice = True

    # smyčka se bude opakovat, dokud uživatel nezadá platnou volbu
    while invalid_choice:
        user_option = secondary_menu(
            'Zadejte vaše uživatelské jméno útvaru.',
            '*', {
                'N': 'Nápověda',
                'Z': 'Návrat zpět do hlavního menu',
            }
        )
        if user_option == 'z':
            return user_option

        if user_option == 'n':
            print()
            help_app('user_shape_name')

        # UŽIVATELSKÉ jméno útvaru musí být unikátní
        elif user_option in user_shapes.keys():
            fixed_width_output('Útvar s tímto uživatelským jménem už existuje. '
                               'Zadejte prosím jiné jméno.')

        # kontrola, zda zadané jméno splňuje příslušné konvence
        elif validate_name(user_option):
            invalid_choice = False
        else:
            print('Zadali jste neplatné jméno. Zkuste to prosím znovu.')

    return user_option


def my_shapes():
    """
    Hlavní funkce pro práci s UŽIVATELSKÝMI útvary

    Funkce ověří, zda má uživatel vytvořeny nějaké útvary, v kladném
    případě zobrazí jejich výpis a požádá ho o výběr útvaru, se kterým
    si přeje pracovat. Poté vypíše seznam veličin a jejich známých
    hodnot v tomto okamžiku a zobrazí menu s volbami pro různé úkony,
    které může uživatel s vybraným útvarem provádět.

    :return: None
    """
    if not user_shapes:
        fixed_width_output('Nemáte vytvořeny žádné útvary. Pomocí volby '
                           '\'Vytvořit Nový útvar\' nejprve nějaký vytvořte.')
        print()
        return

    show_user_shapes()

    # funkci pro pomocné menu předáme jako druhý argument klíče slovníku
    # user_shapes, které jsou tvořeny UŽIVATELSKÝMI názvy dosud
    # vytvořených útvarů; tento argument představuje platné volby,
    # které uživatel (kromě pomocných voleb) může v pomocném menu zadat
    user_option = secondary_menu(
        'Napište uživatelské jméno útvaru, se kterým chcete pracovat.',
        user_shapes.keys(),
        {'Z': 'Návrat zpět do hlavního menu'}
    )
    print()
    if user_option == 'z':
        return

    # uživatel nezvolil pomocnou volbu, takže UŽIVATELSKÉ jméno útvaru
    # bude odpovídat vrácené volbě z pomocného menu
    user_shape = user_shapes[user_option]

    # dokud bude globální proměnná continue_user_shape_work mít hodnotu
    # True, následná hlavní smyčka pro práci s vybraným útvarem se bude
    # opakovat
    global continue_user_shape_work
    continue_user_shape_work = True

    # Hlavní smyčka pro práci s konkrétním uživatelským útvarem
    while continue_user_shape_work:
        global detailed_last

        # běžný výpis hodnot veličin; provedeme ho pouze v případě,
        # nebyl-li v předchozí iteraci použit podrobný výpis veličin
        # pomocí funkce detailed_quantity_overview
        if not detailed_last:
            print_quantity_values(user_shape)
        detailed_last = False

        # do identifikátoru action se přiřadí funkce odpovídající uživatelem
        # zvolené akci, kterou si přeje s útvarem provést
        # funkce se zavolá s argumentem, kterým je reference na instanci
        # UŽIVATELSKÉHO útvaru třídy UserShape, s nímž uživatel právě pracuje
        action = user_shape_menu()
        # funkce zajišťující návrat do hlavního menu nemá žádný parametr
        if action == back_to_main_menu:
            action()
        # pokud smažeme celý UŽIVATELSKÝ útvar, je třeba se poté vrátit
        # do hlavního menu
        elif action == delete_user_shape:
            action(user_shape)
            back_to_main_menu()
        else:
            action(user_shape)


def show_user_shapes():
    """
    Zobrazí seznam UŽIVATELSKÝCH útvarů

    Funkce zobrazí úvodní popisek a vypíše seznam UŽIVATELSKÝCH útvarů
    včetně stručných informací o počtu jejich známých veličin (zadaných
    nebo vypočítaných) a celkovém počtu jejich veličin.

    :return: None
    """
    fixed_width_output('Seznam vašich útvarů. Položky na každém řádku '
                       'jsou vypsány v tomto formátu:\n'
                       '{uživatelské jméno útvaru} ... {geometrický typ} ... '
                       '{počet známých veličin} / {celkový počet veličin}')
    print()

    for k, v in user_shapes.items():
        print(f'{k} ... {v.geom_shape_name} ... '
              f'{v.number_of_known_quantities} / '
              f'{v.total_number_of_quantities}')

    print()


def user_shape_menu():
    """
    Menu pro práci s vybraným UŽIVATELSKÝM útvarem

    :return: identifikátor funkce pro uskutečnění uživatelem zvolené
    akce: function
    """

    # volby menu pro práci s UŽIVATELSKÝM útvarem
    user_shape_options = {
        'H': {
            'description': 'Zadat novou hodnotu veličiny a automaticky '
                           'přepočítat',
            'action': set_new_quantity_value,
        },
        'P': {
            'description': 'Podrobný výpis veličin včetně jejich popisů',
            'action': detailed_quantity_overview,
        },
        'V': {
            'description': 'Vymazat hodnoty všech veličin',
            'action': delete_all_quantity_values,
        },
        'O': {
            'description': 'Odstranit útvar',
            'action': delete_user_shape,
        },
        'Z': {
            'description': 'Návrat zpět do hlavního menu',
            'action': back_to_main_menu,
        },
    }

    user_shape_func = key_command_menu(user_shape_options, 'Menu - Uživatelský '
                                                           'útvar')
    return user_shape_func


def print_quantity_values(user_shape):
    """
    Vypíše seznam veličin UŽIVATELSKÉHO útvaru a jejich hodnot

    Funkce vypíše hlavičku se základními informacemi UŽIVATELSKÉHO
    útvaru následovanou seznamem značek jeho veličin a příslušných
    hodnot. Pokud daná veličina zatím nemá přiřazenou hodnotu, vypíší se
    místo ní tři tečky.

    :param user_shape: reference na instanci příslušného UŽIVATELSKÉHO
    útvaru: UserShape
    :return: None
    """

    # hlavička s názvem a GEOMETRICKÝM typem útvaru
    user_shape_header = (f'Uživatelské jméno útvaru: '
                         f'{user_shape.user_shape_name}')
    geom_shape_header = (f'Geometrický typ útvaru: '
                         f'{user_shape.geom_shape_name} '
                         f'({user_shape.geom_descriptive_name})')

    # oddělující čára
    line_length = max(len(user_shape_header), len(geom_shape_header))
    print('-'*line_length)

    # výpis hlavičky
    fixed_width_output(user_shape_header)
    fixed_width_output(geom_shape_header)
    print()
    fixed_width_output('Veličiny a jejich hodnoty:')
    fixed_width_output('Formát výpisu: {značka veličiny} = {hodnota}')
    fixed_width_output('(Tři tečky za rovnítkem znamenají, že hodnota veličiny '
                       'je zatím neznámá.)')
    print()

    # výpis značek veličin a odpovídajících hodnot
    for k, v in user_shape.quantity_values.items():
        print_symbol_and_value(user_shape, k, v)

    print()


def detailed_quantity_overview(user_shape):
    """
    Vypíše podrobné informace o veličinách UŽIVATELSKÉM útvaru

    Funkce vypíše seznam veličin UŽIVATELSKÉHO útvaru včetně jejich
    hodnot a navíc i popisy těchto veličin.

    :param user_shape: reference na instanci příslušného UŽIVATELSKÉHO
    útvaru: UserShape
    :return: None
    """
    fixed_width_output('Podrobný výpis veličin útvaru včetně jejich popisů:')
    print()

    for k, v in user_shape.quantity_values.items():
        print_symbol_and_value(user_shape, k, v)
        fixed_width_output(f'Stručný popis veličiny: '
                           f'{user_shape.get_property(k, "short_name")}')
        fixed_width_output(f'Podrobný popis veličiny: '
                           f'{user_shape.get_property(k, "description")}')
        print()

        # globální proměnnou detailed_last nastavíme na hodnotu True,
        # aby program po návratu do hlavní smyčky pro práci s UŽIVATELSKÝMI
        # útvary věděl, že právě byl uskutečněn tento podrobný výpis,
        # a nedošlo k bezprostřednímu běžnému výpisu veličin a hodnot
        # tohoto útvaru
        global detailed_last
        detailed_last = True


def back_to_main_menu():
    """
    Provede nastavení, které způsobí návrat programu do hlavního menu

    Funkce se používá během běhu smyčky pro práci s vybraným
    UŽIVATELSKÝM útvarem a nastaví globální proměnnou
    continue_user_shape_work na hodnotu False. Tato proměnná je
    v této smyčce kontrolována a slouží právě k identifikaci, že
    uživatel zvolil volbu pro návrat do hlavního menu programu.

    :return: None
    """
    global continue_user_shape_work
    continue_user_shape_work = False


def set_new_quantity_value(user_shape):
    """
    Přiřadí hodnotu veličině UŽIVATELSKÉHO útvaru

    Funkce vyzve uživatele k zadání rovnice ve tvaru
    'značka veličiny' = 'hodnota' a poté provede všechna nezbytná
    ověření, zda lze tuto hodnotu příslušné veličině přiřadit.
    V případě, že některé z těchto ověření selže, funkce informuje
    uživatele o příčině a provede návrat. Jestliže všechna ověření
    budou v pořádku, funkce provede přiřazení uživatelem zadané
    hodnoty příslušné veličině.

    :param user_shape: reference na instanci příslušného UŽIVATELSKÉHO
    útvaru: UserShape
    :return: None
    """

    # kontrola, zda již všechny veličiny UŽIVATELSKÉHO útvaru nemají
    # přiřazené hodnoty
    if user_shape.number_of_known_quantities \
            == user_shape.total_number_of_quantities:
        fixed_width_output(f'Veškeré veličiny vašeho útvaru '
                           f'{user_shape.user_shape_name} jsou již známé '
                           f'(přiřazené nebo vypočítané).')
        return

    # výzva uživateli k zadání značky veličiny a hodnoty
    user_option = secondary_menu(
        'Napište výraz ve tvaru {značka veličiny} = {hodnota}',
        '*',
        {'Z': 'Návrat zpět do menu Uživatelský útvar'}, True
    )
    print()
    if user_option == 'z':
        return

    # konverze uživatelova zadání na seznam obsahující řetězce
    # reprezentující jednotlivá "slova" tohoto zadání bez přiřazovacího
    # symbolu '='
    parsed_command = parse_command(user_option)

    # konverze seznamu parsed_values na dvoupoložkový tuple
    # (značka veličiny: str, hodnota: float)
    symbol, value = get_assignment_pair(parsed_command)

    # pokud tato konverze selhala z důvodu chybně zadaného uživatelského
    # vstupu, vypíše se informace o příčině selhání a funkce se ukončí
    if last_error_message['error']:
        fixed_width_output(last_error_message['text'])
        return

    # kontrola, zda aktuální UŽIVATELSKÝ útvar má definovánu veličinu
    # se značkou, kterou zadal
    if not user_shape.quantity_exists(symbol):
        fixed_width_output(f'CHYBA: Váš útvar {user_shape.user_shape_name} '
                           f'typu {user_shape.geom_shape_name} '
                           f'nemá definovánu veličinu se značkou {symbol}.')
        return

    # přiřazování úhlů probíhá ve stupních, ale do příslušné datové
    # struktury s UŽIVATELSKÝM útvarem se ukládá v obloukové míře
    # (radiánech) - proto se v případě, že daná veličina reprezentuje
    # úhel, provede převod uživatelem zadané hodnoty ze stupňů do
    # obloukové míry
    if user_shape.get_property(symbol, 'is_angle'):
        value = math.radians(value)

    # kontrola, zda uživatelem zvolená veličina již nemá přiřazenu hodnotu
    if user_shape.quantity_has_value(symbol):
        fixed_width_output(f'CHYBA: Veličina {symbol} již má přiřazenu hodnotu '
                           f'{user_shape.quantity_values[symbol]["value"]}.')
        return

    # kontrola, zda uživatelem zadaná hodnota náleží do rozsahu hodnot,
    # kterých může nabývat v rámci obecných geometrických pravidel
    # i v rámci aktuálního kontextu (tj. vzhledem k hodnotám jiných
    # veličin)
    if not user_shape.value_meets_conditions(symbol, value):
        fixed_width_output(f'CHYBA: {user_shape.last_condition_message}')
        return

    # funkce dosud neprovedla návrat, což znamená, že všechna ověření
    # uživatelova zadání prošla - přiřadíme tedy hodnotu dané veličině
    # a informujeme o tom uživatele; při každém přiřazení se VŽDY
    # automaticky provede pokus o výpočet hodnot dalších veličin
    # UŽIVATELSKÉHO útvaru na základě množiny hodnot, která se právě
    # rozšířila o hodnotu novou, jak napovídá název funkce
    # assign_value_and_recalculate
    user_shape.assign_value_and_recalculate(symbol, value)
    fixed_width_output('Hodnota byla úspěšně přiřazena.')


def parse_command(user_command):
    """
    Rozdělí vstupní text na významové entity včetně znaku '='

    Funkce vrátí seznam stringů reprezentujících souvislé části textu
    bez bílých znaků nebo znak '='. Funkce je používána k rozdělení
    uživatelova vstupu na jednotlivé entity v situaci, kdy se pokouší
    přiřadit hodnotu některé veličině. Např. pro následující vstupy:
    'alfa=30', 'alfa = 30', 'alfa= 30' a 'alfa =30', bude výstupem
    seznam ['alfa', '=', '30'].

    :param user_command: vstup uživatele při přiřazování hodnoty veličině:
    str
    :return: seznam stringů reprezentujících jednotlivé významové entity:
    list
    """
    splitted_command = user_command.split()

    parsed_command = []
    for word in splitted_command:
        if '=' in word and word != '=':
            if word.startswith('='):
                parsed_command.append('=')
                parsed_command.append(word[1:])
            elif word.endswith('='):
                parsed_command.append(word[:len(word) - 1])
                parsed_command.append('=')
            else:
                i = word.index('=')
                parsed_command.append(word[:i])
                parsed_command.append('=')
                parsed_command.append(word[i + 1:])
        else:
            parsed_command.append(word)

    return parsed_command


def get_assignment_pair(parsed_command):
    """
    Vrátí dvoupoložkovou n-tici 'značka veličiny', 'číslo'

    Funkce ověří, zda na vstupu obdržela třípoložkový seznam stringů,
    dále zvaliduje, zda první je platnou značkou veličiny, druhý znak '='
    a třetí číslo. Bude-li vše v pořádku, vrátí dvoupoložkovou n-tici
    'značka veličiny', 'číslo'. V opačném případě vrátí prázdný string
    a číslo -1 a nastaví chybovou zprávu pro následné upozornění
    uživatele.

    :param parsed_command: seznam stringů reprezentujících části
    přiřazovacího příkazu hodnoty veličině
    :return: značka veličiny a přiřazovaná hodnota: tuple
    """
    last_error_message['error'] = False
    if len(parsed_command) != 3 or parsed_command[1] != '=':
        last_error_message['error'] = True
        last_error_message['text'] = 'CHYBA: Nesprávný formát příkazu.'
        return '', -1
    if not validate_name(parsed_command[0], True, 1):
        last_error_message['error'] = True
        last_error_message['text'] = 'CHYBA: Nesprávně zadaná značka ' \
                                     'veličiny na levé straně přiřazovacího ' \
                                     'příkazu.'
        return '', -1
    if not is_convertible_to_float(parsed_command[2]):
        last_error_message['error'] = True
        last_error_message['text'] = 'CHYBA: Nesprávně zadané číslo na pravé ' \
                                     'straně přiřazovacího příkazu.'
        return '', -1

    return parsed_command[0], float(parsed_command[2])


def is_convertible_to_float(value):
    """
    Ověří, zda je vstupní string převoditelný na float

    :param value: vstupní text, který by měl reprezentovat číslo: str
    :return: zda lze vstupní text zkonvertovat na float: bool
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def print_symbol_and_value(user_shape, k, v):
    """
    Vypíše značku veličiny a její hodnotu

    Funkce vypíše na jeden řádek značku veličiny, znaménko '=' a hodnotu
    této veličiny, pokud je známá. Je-li hodnota neznámá, vypíše místo ní
    tři tečky.

    :param user_shape: reference na instanci UŽIVATELSKÉHO útvaru:
    UserShape
    :param k: značka veličiny UŽIVATELSKÉHO útvaru: str
    :param v: hodnota veličiny UŽIVATELSKÉHO útvaru: float
    :return: None
    """
    print(f'{k} = ', end='')
    if v['has_value']:
        if user_shape.get_property(k, 'is_angle'):
            print(round(math.degrees(v['value']), ROUND_DECIMALS))
        else:
            print(round(v['value'], ROUND_DECIMALS))
    else:
        print('...')


def delete_all_quantity_values(user_shape):
    """
    Vymaže hodnoty všech veličin UŽIVATELSKÉHO útvaru

    :param user_shape: reference na instanci příslušného UŽIVATELSKÉHO
    útvaru: UserShape
    :return: None
    """
    user_shape.delete_quantity_values()


def delete_user_shape(user_shape):
    """
    Smaže celý UŽIVATELSKÝ útvar

    Funkce odstraní UŽIVATELSKÝ útvar z globálního slovníku user_shapes.

    :param user_shape: reference na instanci příslušného UŽIVATELSKÉHO
    útvaru: UserShape
    :return: None
    """
    deleted_user_shape_name = user_shape.user_shape_name
    deleted_geom_shape_name = user_shape.geom_shape_name
    del user_shapes[user_shape.user_shape_name]
    fixed_width_output(f'Útvar s názvem {deleted_user_shape_name} typu '
                       f'{deleted_geom_shape_name} byl smazán.')


def quit_app():
    """
    Potvrzení ukončení práce s programem uživatelem

    Vyzve uživatele k potvrzení, zda si opravdu přeje ukončit práci
    s aplikací. Podle jeho volby pak nastaví globální proměnnou
    continue_app na False nebo ji ponechá jako True. Proměnná continue_app
    s nastavenou hodnotou False bude mít za následek ukončení programu.

    :return: None
    """
    if confirm_option('Opravdu si přejete ukončit program?'):
        global continue_app
        continue_app = False


def validate_name(name, capital=False, minimal_length=3):
    """
    Zvaliduje platnost identifikátoru zadaného uživatelem

    Funkce ověří, zda identifikátor zadaný uživatelem splňuje příslušná
    kritéria. Může se jednat například o název UŽIVATELSKÉHO útvaru.

    :param name: validovaný identifikátor: str
    :param capital: zda identifikátor může nebo nemůže obsahovat velká
    písmena: bool
    :param minimal_length: minimální požadovaná délka identifikátoru
    :return: zda identifikátor splňuje nebo nesplňuje daná kritéria: bool
    """
    def is_small_letter(c):
        return (ord(c) >= ord('a')) and (ord(c) <= ord('z'))

    def is_capital_letter(c):
        return (ord(c) >= ord('A')) and (ord(c) <= ord('Z'))

    def is_valid_letter(c):
        return (is_small_letter(c)) or (capital and is_capital_letter(c))

    def is_digit_or_underscore(c):
        return (ord(c) >= ord('0')) and (ord(c) <= ord('9')) or (c == '_')

    if len(name) < minimal_length:
        return False

    if not is_valid_letter(name[0]):
        return False

    for char in name[1:]:
        if not (is_valid_letter(char) or is_digit_or_underscore(char)):
            return False

    return True


def fixed_width_output(text, columns=76):
    """
    Vypíše do konzole text zformátovaný na požadovanou šířku

    Funkce vypíše do konzole text tak, aby jeho šířka nepřekročila
    určitý počet znaků, a aby nedocházelo k nežádoucímu zalamování
    textu uprostřed slov nebo těsně před interpunkčními znaménky.

    :param text: výstupní text: str
    :param columns: maximální počet znaků v jednom řádku: int
    :return: None
    """
    while len(text) > columns:

        # index poslední mezery v rozsahu délky řádku
        space_index = text[:columns].rfind(' ')

        # index prvního znaku konce řádku v rozsahu délky řádku
        nl_index = text[:columns].find('\n')

        if nl_index == -1:
            # v rozsahu délky řádku není znak konce řádku - vypíše se
            # část textu po poslední mezeru na konci tohoto rozsahu
            # a vypsaná část textu se odřízne
            print(text[:space_index + 1])
            text = text[space_index + 1:]
        else:
            # v rozsahu délky řádku je znak konce řádku, vypíše se tedy
            # část textu, která končí těsně před ním, protože odřádkování
            # zajistí samotné volání funkce print(), a vypsaná část textu
            # se odřízne
            print(text[:nl_index])
            text = text[nl_index + 1:]
    else:
        # vypsání zbytku textu
        print(text)


def help_app(topic):
    """
    Nápověda k programu

    :param topic: téma, k němuž si uživatel přeje vypsat nápovědu: str
    :return: None
    """
    content = {
        'main': {
            'header': 'Hlavní nápověda k programu',
            'description': 'Nejjednodušší způsob, jak se naučit s aplikací '
                           'pracovat, je zkoušet si s ní hrát :)\n\n'
                           'Začněte volbou \'Vytvořit nový útvar\'. Zobrazí se '
                           'seznam dostupných geometrických útvarů, z nichž si '
                           'jeden zvolíte a následně mu přidělíte svůj vlastní '
                           'název (např. obdélník si můžete pojmenovat jako '
                           '\'obd1\'). Můžete si vytvořit tolik útvarů, kolik '
                           'chcete. Nezáleží přitom na tom, zda budou mít '
                           'stejné nebo různé geometrické typy - můžete si '
                           'kdykoli vytvořit např. další obdélníky, pouze jim '
                           'musíte přidělit jedinečné názvy (\'obd2\', '
                           '\'obd3\', \'velky_obdelnik\' apod.) Stejně tak si '
                           'můžete vytvořit libovolný počet jiných '
                           'geometrických útvarů. Aplikace si je bude všechny '
                           'pamatovat, dokud se nerozhodnete ji ukončit. Při '
                           'pojmenovávání Vašich útvarů musíte dodržet '
                           'několik pravidel, která jsou popsána v pomocné '
                           'nápovědě přístupné uvnitř této části programu.\n\n'
                           'Jakmile vytvoříte alespoň jeden nový útvar, zvolte '
                           'v hlavním menu volbu \'Moje útvary\'. Zde uvidíte '
                           'seznam vašich dosud vytvořených útvarů. U každého'
                           'z nich se zobrazí i jeho geometrický typ (zda se '
                           'jedná o kruh, obdélník atd.) a rovněž počet jeho '
                           'veličin, které jsou v aktuálním okamžiku známé / '
                           'celkový počet jeho veličin. Dále zadáte název '
                           'útvaru (ten Váš, tzn. uživatelský), s nímž si '
                           'přejete pracovat, a zobrazí se seznam jeho veličin '
                           '(např. délky stran, obsah, obvod apod.) Každá '
                           'veličina má svoji značku a hodnotu. Pokud hodnotu '
                           'zatím ještě nemá, zobrazí se tři tečky.\n\n'
                           'Nyní můžete zvolit možnost \'Zadat novou hodnotu '
                           'veličiny a automaticky přepočítat\'. Následně '
                           'budete vyzváni k zadání značky veličiny '
                           'a hodnoty, kterou jí chcete přidělit. Mezi tyto '
                           'dva údaje napíšete znaménko \'=\' - u obdélníku '
                           'např. můžete zadat \'a = 10\' (mezery okolo znaku '
                           '\'=\' nejsou podstatné a můžete je vynechat - '
                           'slouží pouze pro zvýšení přehlednosti při '
                           'zadávání). Program si Vámi přidělenou hodnotu '
                           'zapamatuje a můžete zadat další. Jakmile bude mít '
                           'program dostatek informací k tomu, aby spočítal '
                           'hodnotu nebo hodnoty jiných veličin tohoto útvaru, '
                           'tak tento výpočet provede a v seznamu se zobrazí '
                           'výsledky.\n\n'
                           'Pokud nevíte, kterou veličinu daná značka '
                           'reprezentuje, zvolte \'Podrobný výpis veličin '
                           'včetně jejich popisů\'.\n\n'
                           'Důležité poznámky:\n'
                           '- Jako oddělovač desetinných čísel používejte '
                           'TEČKU, nikoli čárku.\n'
                           '- Zadávané a vypočítané hodnoty nepoužívají žádné '
                           'jednotky. Veličinám přidělujete pouze čísla. Je na '
                           'Vás, abyste všechny údaje zadali ve stejných '
                           'jednotkách, ať už to budou centimetry, metry '
                           'a podobně.\n'
                           '- U značek veličin se rozlišují malá a velká '
                           'písmena. Např. při zadávání obsahu musíte '
                           'napsat velké S.\n '
                           '- Velikosti úhlů se zadávají i zobrazují ve '
                           'stupních.'
        },
        'user_shape_name': {
            'header': 'Uživatelské jméno útvaru',
            'description': 'Uživatelské jméno útvaru je jméno, které nově '
                           'vytvořenému geometrickému útvaru přidělujete Vy '
                           'jakožto uživatel programu.\n\n'
                           'Uživatelské jméno je tedy důležité zejména pro '
                           'Vás, abyste si mohli různé útvary pojmenovávat '
                           'snadno zapamatovatelnými jmény, které vám pomohou '
                           'si lépe uvědomit, s jakým útvarem pracujete '
                           '(např. \'maly_obdelnik\', \'velky_obdelnik\' '
                           'apod.) a také k rozlišení více geometrických '
                           'útvarů stejného typu, pokud je v průběhu práce '
                           's programem vytvoříte (můžete si např. vytvořit '
                           'několik odlišných obdélníků, kruhů atd. a následně '
                           'se na konkrétní útvar odkazovat právě Vámi '
                           'zvoleným uživatelským jménem tohoto útvaru).\n\n'
                           'Útvary si můžete pojmenovávat libovolně, avšak '
                           'musíte dodržet několik pravidel:\n'
                           '1) Uživatelské jméno útvaru se může skládat pouze '
                           'z malých písmen anglické abecedy (nesmí tedy '
                           'obsahovat diakritiku), číslic a znaku podtržítka '
                           '\'_\'.\n'
                           '2) Jméno musí začínat (malým) písmenem.\n'
                           '3) Jméno musí mít minimální délku tři znaky.\n'
                           '4) Jméno nesmí obsahovat mezery ani žádné jiné '
                           'speciální znaky.\n\n'
                           'Příklady platných jmen uživatelských geometrických '
                           'útvarů:\n'
                           'obd\nobd1\nmuj_obdelnik\nprvni_obd\nvelky_kruh\n'
                           'kr_maly\n\n'
                           'Příklady neplatných jmen uživatelských '
                           'geometrických útvarů:\n'
                           'obdélník1 (obsahuje diakritiku)\n'
                           '2obd (nezačíná písmenem, ale číslicí)\n'
                           'Obd1 (obsahuje velké písmeno)\n'
                           'maly obdelnik (obsahuje mezeru)\n'
                           'kr (nemá minimální požadovanou délku 3 znaky)\n'
                           'muj-kruh (obsahuje speciální znak - pomlčku)'
        },
    }

    if topic in content.keys():
        fixed_width_output(f'{content[topic]["header"]}')
        print()
        fixed_width_output(f'{content[topic]["description"]}')
        print()
    else:
        fixed_width_output('Omlouváme se, nápověda k tomuto tématu není '
                           'k dispozici.')
        print()

    input('Stiskněte ENTER pro návrat zpět...')

    print()
    return


if __name__ == '__main__':
    main()
