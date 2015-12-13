import string

class Template(object):
    """Contains HTML templates and helper functions for rendering character sheet elements"""

    header = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="../static/main.css">
        <title>Character Sheet</title>
    </head>
"""

    def render_title_bar(self, character_details):
        template_text = "<header>"
        template_text += "    <h1>$character_name</h1> \n"
        template_text += '    <p id="race">Race: $character_race</p> \n'
        template_text += '    <p id="class-level">Class: $character_class $character_level</p> \n'
        template_text += '    <p id="xp">XP:___________________</p> \n'
        template_text += '    <p>Player Name:__________________</p> \n'
        template_text += '</header>'
        t = string.Template(template_text)
        return t.substitute(character_details)

    def render_section_heading(self, text):
        return string.Template('<h2 class="section-heading">$text</h2>').substitute(text=text)
        
    def render_table_row(self, columns, data, with_class=None):
        if with_class is None:
            template_text = '<tr> \n'
        else:
            template_text = '<tr class={}> \n'.format(with_class)
        for i in range(columns):
            template_text += '    <td class="column{0:d}">$value{0:d}</td>\n'.format(i)
        template_text += '</tr> \n'
        if columns == 2:
            return string.Template(template_text).substitute(value0=data[0], value1=data[1])
        elif columns == 3:
            return string.Template(template_text).substitute(value0=data[0], value1=data[1], value2=data[2])
        else:
            raise NotImplementedError("only 2 or 3 columns are allowed")

    def render_table(self, with_class, shouldStart=True):
        if shouldStart:
            return string.Template('<table class="$class_name">').substitute(class_name=with_class)
        else:
            return '</table>'

    def render_container(self, with_class, shouldStart=True):
        if shouldStart:
            return string.Template('<div class="$class_name">').substitute(class_name=with_class)
        else:
            return '</div>'

    def render_closing(self):
        return "</body>\n</html>"

    def render_power_card(self, data):
        output = []
        type = data['type']
        output.append(self.render_container("power-card {}".format(type.lower().replace(' ', '-')))) #0
        output.append(self.render_section_heading('$type (${action})'))
        output.append("<ul class='power-summary'>") #1
        output.append('<li class="name">${name}</li>')
        if data.get('attack_bonus'):
            output.append('<li class="attack"><b>ATK:</b> 1d20 + ${attack_bonus} VS $defense</li>')
        else:
            output.append('<li class="attack"><b>ATK:</b> N/A</li>')
        if data.get('damage'):
            output.append("<li class='damage'><b>DMG:</b> $damage ${damage_type}</li>")
        else:
            output.append("<li class='damage'><b>DMG:</b> None</li>")
        output.append("</ul>") #/1

        output.append("<ul class='power-targeting'>") #2
        if data.get('target'):
            output.append("<li><b>Target(s):</b> $target</li>")
        else:
            output.append("<li><b>Target:</b> Self</li>")
        if data.get('range'):
            output.append("<li><b>Range:</b> $range</li>")
        output.append("</ul>") #/2

        output.append("<ul class='power-effects'>") #3
        if data.get('hit_effects'):
            output.append("<li><b>Effect on Hit:</b> $hit_effects</li>")
        if data.get('miss'):
            output.append("<li><b>Effect on Miss:</b> $miss</li>")
        if data.get('trigger'):
            output.append("<li><b>Trigger:</b> $trigger</li>")
        if data.get('effects'):
            output.append("<li><b>Effects (always):</b> $effects</li>")
        output.append("</ul>") #/4

        if data.get('keywords'):
            output.append("<div class='power-keywords'>") #4
            output.append("<b>Keywords:</b> $keywords")
            output.append("</div>") #/4

        output.append(self.render_container("", False)) #/0
        return string.Template('\n'.join(output)).safe_substitute(data)

    def render_page_break(self):
        return '<div class="page-break"></div>\n'
