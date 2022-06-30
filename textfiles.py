"""
Modul s funkcemi pro inicializaci dat z textových souborů

Obsahuje funkce pro načtení a úvodní zpracování obsahu textových
souborů s obecně platnými informacemi o konkrétních GEOMETRICKÝCH
útvarech za účelem výpočtu jejich metrických veličin na základě
vstupních hodnot zadaných uživatelem.
"""


def shape_init_list_from_text_file(path, filename):
    """
    Provede konverzi textového souboru s informacemi o GEOMETRICKÉM útvaru.

    Vrácená n-tice bude tvořena textovým řetězcem a třemi vnořenými seznamy,
    které odpovídají jednotlivým oddílům inicializačního souboru.
    Seznamy z oddílů QUANTITIES a CONDITIONS budou tvořeny ještě o jednu úroveň
    hlouběji vnořenými seznamy.

    :param path: relativní cesta k inicializačnímu souboru konkrétního
    útvaru bez názvu tohoto souboru: str
    :param filename: název textového inicializačního souboru útvaru bez přípony:
    str
    :return: datová struktura s informacemi o GEOMETRICKÉM útvaru: tuple

    Schéma vrácené n-tice:
     tuple
     |-- popisný název geometrického útvaru (k uživatelským výpisům): str
     |-- veličiny: list
     |             |-- veličina 1: list
     |             |               |-- značka veličiny: str
     |             |               |-- krátký popis veličiny: str
     |             |               |-- delší popis veličiny: str
     |             |               |-- [is_angle: str]
     |             |
     |             |-- veličina 2: list
     |             .
     |             .
     |             .
     |             |-- veličina n: list
     |
     |-- vzorce: list
     |            |-- vzorec 1: str
     |            |-- vzorec 2: str
     |            .
     |            .
     |            .
     |            |-- vzorec m: str
     |
     |-- podmínky konstruovatelnosti: list
                                      |-- podmínka 1: list
                                      |               |-- nerovnice: str
                                      |               |-- popis: str
                                      |
                                      |-- podmínka 2: list
                                      .
                                      .
                                      |-- podmínka k: list
    """
    lines = load_text_file(path + filename + '.txt')
    clean_lines = get_clean_lines(lines)

    geom_descriptive_name_list = get_section(clean_lines, 'DESCRIPTIVE_NAME')

    # protože popisný název GEOMETRICKÉHO útvaru je pouze jednopoložkový seznam,
    # převedeme jej rovnou na string
    geom_descriptive_name = geom_descriptive_name_list[0]

    quantity_lines = get_section(clean_lines, 'QUANTITIES')
    quantities = split_items(quantity_lines)

    formulas = get_section(clean_lines, 'FORMULAS')

    condition_lines = get_section(clean_lines, 'CONDITIONS')
    conditions = split_items(condition_lines)

    return geom_descriptive_name, quantities, formulas, conditions


def load_text_file(full_path):
    """
    Načte obsah textového souboru a vrátí ho jako seznam řádků.

    :param full_path: relativní cesta k souboru včetně jeho názvu a přípony: str
    :return: řádky textového souboru: list
    """
    try:
        with open(f'{full_path}', 'r', encoding='utf8') as file:
            lines = file.readlines()
            return lines
    except IOError:
        print('Chyba při načítání inicializačního souboru {path}.')


def get_clean_lines(lines):
    """
    Vrátí "očištěný" seznam řádků textu.

    Funkce odstraní z textu komentáře, prázdné řádky a bílé znaky na začátcích
    a koncích řádků.

    :param lines: řádky textu ke zpracování: list
    :return: zpracované řádky: list
    """

    # odstranění komentářů
    clean_list = []
    for item in lines:
        comment_index = item.find('#')
        if comment_index == -1:
            clean_list.append(item)
        else:
            clean_list.append(item[:comment_index])

    # odstranění bílých znaků
    clean_list = [item.strip() for item in clean_list]

    # odstranění prázdných řádků
    clean_list = [item for item in clean_list if item]

    return clean_list


def get_section(lines, section_name):
    """
    Vrátí seznam řádků textu patřících pouze do konkrétního oddílu.

    Funkce vrátí řádky textu, které patří do oddílu určeného parametrem
    section_name (bez řádku s názvem tohoto oddílu).

    :param lines: řádky textu: list
    :param section_name: název oddílu, jehož řádky chceme vybrat a vrátit: str
    :return: řádky textu z vybraného oddílu: list
    """

    # nalezení začátku oddílu
    # 1. položka nového seznamu je o 1 prvek dále, než položka s názvem sekce
    start_index = lines.index(f'Section: {section_name}') + 1

    # nalezení konce oddílu
    for i in range(start_index, len(lines)):
        if lines[i].startswith('Section: '):
            # nalezen začátek dalšího oddílu, hledaný oddíl končí těsně před ním
            end_index = i
            break  # můžeme tedy opustit cyklus
    else:
        # Další sekce již není - hledaný oddíl končí poslední položkou seznamu
        end_index = len(lines)

    # indexy hranic oddílu nalezeny - můžeme provést slicing
    section = lines[start_index:end_index]
    return section


def split_items(lines):
    """
    Rozdělí řádky textu podle znaku '|' a vrátí příslušnou datovou strukturu.

    Funkce přijme v parametru lines seznam řádků textu, každý řádek rozdělí do
    samostatných textových řetězců podle znaku '|', odstraní bílé znaky na
    jejich začátcích a koncích a vrátí seznam s vnořenými seznamy obsahujícími
    takto získané výsledné řetězce.

    :param lines: řádky textu: list
    :return: rozdělené řádky textu jako řetězce ve vnořených seznamech: list
    """

    splitted_text = []
    for line in lines:
        items = line.split('|')
        items = [item.strip() for item in items]
        splitted_text.append(items)

    return splitted_text
