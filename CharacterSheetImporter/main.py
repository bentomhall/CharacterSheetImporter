import template
import xml.etree.ElementTree as xmlTree
import htmlrenderer

def extract_details(xml_details):
    output = {}
    output['character_name'] = xml_details.find("./Details/name").text.strip()
    output['character_race'] = xml_details.find(".//RulesElement[@type='Race']").get("name")
    output['character_class'] = xml_details.find(".//RulesElement[@internal-id='ID_FMP_CLASS_2']").get("name")
    output['character_level'] = xml_details.find('./Details/Level').text.strip()
    return output

def extract_ability_scores(sheet):
    stats = ['STR', 'con', 'DEX', 'INT', 'WIS', 'CHA']
    container_class = "stat-container"
    section_heading = "Ability Scores"
    table_class = "ability-scores"
    row_data = [{'css':'table-header', 'data':["Ability", "Score", "Mod"]}]
    for ability in stats:
        predicate = "./StatBlock/Stat/alias[@name='{}']/..".format(ability)
        element = sheet.find(predicate)
        name = ability.upper()
        score = element.get("value")
        modifier = (int(score) - 10)/2 #integer division intended
        row_data.append({'data':[name, score, modifier]})
    return (row_data, container_class, table_class, section_heading)

def extract_defenses(sheet):
    defenses = ["AC", "Fortitude", "Reflex", "Will"]
    row_data = [{'css':"table-header", 'data':["Defense", "Value", "Notes"]}]
    for d in defenses:
        predicate = "./StatBlock/Stat/alias[@name='{}']/..".format(d)
        element = sheet.find(predicate)
        value = element.get("value")
        try:
            conditional = element.find("./statadd[@conditional]")
            notes = "+{}".format(conditional.get("value"))
            notes += " {}".format(conditional.get("conditional"))
        except ValueError:
            notes = ""
        row_data.append({'data': [d, value, notes]})
    container_class = "stat-container defenses"
    table_class = "defenses"
    section_heading = "Defenses"
    return (row_data, container_class, table_class, section_heading)

def extract_health(sheet):
    hp = sheet.find("./StatBlock/Stat/alias[@name='Hit Points']/..").get("value")
    surges_total = sheet.find("./StatBlock/Stat/alias[@name='Healing Surges']/..").get("value")
    surge_value = int(hp)/4
    bloodied_value = int(hp)/2
    row_data = [
        {'data':["HP: {}".format(hp), "Bloodied: {}".format(bloodied_value)]},
        {'data':["Current HP:         ", "Surges: {}".format(surges_total)]},
        {'data':["Conditions:         ", "Surge Value: {}".format(surge_value)]}]
    return (row_data, 'health-container', 'health', 'Health')

def text_or_empty(element, predicate):
    try:
        output = element.find(predicate).text.strip()
    except AttributeError:
        output = ""
    return output

def extract_powers(sheet):
    predicate = "./PowerStats/Power"
    powers = sheet.findall(predicate)
    output = []
    for p in powers:
        power_data = {}
        power_data['name'] = p.get('name')
        power_data['type'] = text_or_empty(p, './specific[@name="Power Usage"]')
        power_data['keywords'] = text_or_empty(p, './specific[@name="Keywords"]')
        power_data['action'] = text_or_empty(p, './specific[@name="Action Type"]')
        power_data['target'] = text_or_empty(p, './specific[@name="Target"]')
        power_data['range'] = text_or_empty(p, './specific[@name="Attack Type"]').replace('\n', '<br/>')
        power_data['attack_bonus'] = text_or_empty(p, './Weapon/AttackBonus')
        power_data['defense'] = text_or_empty(p, './Weapon/Defense')
        power_data['damage_type'] = text_or_empty(p, './Weapon/DamageType')
        power_data['damage'] = text_or_empty(p, './Weapon/Damage')
        power_data['hit_effects'] = text_or_empty(p, './specific[@name="Hit"]').replace('\n', '<br/>')
        power_data['effects'] = text_or_empty(p, './specific[@name="Effect"]')
        power_data['miss'] = text_or_empty(p, './specific[@name="Miss"]')
        power_data['trigger'] = text_or_empty(p, './specific[@name="Trigger"]')
        output.append(power_data)
    return output
   
def main(filename=None):
    t = template.Template()
    renderer =  htmlrenderer.HTMLRenderer(t)
    if filename is None:
        filename = 'test\deva cleric.xml'
    tree = xmlTree.parse(filename)
    root = tree.getroot()
    character_sheet = root.find("CharacterSheet")
    health_data, health_container, health_table, health_heading = extract_health(character_sheet)
    defense_data, defense_container, defense_table, defense_heading = extract_defenses(character_sheet)
    ability_data, ability_container, ability_table, ability_heading = extract_ability_scores(character_sheet)
    powers = extract_powers(character_sheet)

    with open('test/test_output.html', 'w') as outputfile:
        outputfile.write(renderer.start_html())
        body_header_information = extract_details(character_sheet)
        outputfile.write(renderer.render_top_banner(body_header_information))
        outputfile.write(renderer.open_container("main-content"))
        outputfile.write(renderer.render_table_container(ability_data, ability_container, ability_table, ability_heading))
        outputfile.write(renderer.render_table_container(defense_data, defense_container, defense_table, defense_heading))
        outputfile.write(renderer.render_table_container(health_data, health_container, health_table, health_heading))
        outputfile.write(t.render_page_break())
        for index, p in enumerate(powers):
            if index % 6 == 0 and index != 0:
                outputfile.write(t.render_page_break())
            outputfile.write(t.render_power_card(p))
        outputfile.write(renderer.close_container()) #main-content
        outputfile.write(renderer.end_html())
    return

if __name__ == "__main__":
    main()
