class HTMLRenderer(object):
    """description of class"""
    is_container_open = False
    is_table_open = False
    css_classes = ""

    def __init__(self, template_instance):
        self._t = template_instance
        return

    def close_table(self):
        self.is_table_open = False
        return self._t.render_table("", shouldStart=False)
      
    def close_container(self):
        self.is_container_open = False
        return self._t.render_container("", shouldStart=False)
    
    def open_table(self, css_class):
        self.is_table_open = True
        return  self._t.render_table(css_class, shouldStart=True)
    
    def open_container(self, css_class):
        self.is_container_open = True
        return self._t.render_container(css_class, shouldStart=True) 

        """Renders a table from provided rows.
        row_data format: [{'css': string, 'data': [row elements]}, {...}]
    """
    def render_table(self, row_data, table_class=""):
        #close any open tables (failsafe)
        output = []
        if self.is_table_open:
            output.append(self.close_table())
            
        output.append(self.open_table(table_class))
        for row_dict in row_data:
            css = row_dict.get('css')
            data = row_dict['data'] #should throw if improperly constructed
            columns = len(data)
            output.append(self._t.render_table_row(columns, data, with_class=css))
        output.append(self.close_table())
        return '\n'.join(output) +'\n'

    def render_table_container(self, table_data, container_class, table_class="", section_heading=""):
        output = []
        output.append(self.open_container(container_class))
        if section_heading:
            output.append(self._t.render_section_heading(section_heading))
        output.append(self.render_table(table_data, table_class=table_class))
        output.append(self.close_container())
        return '\n'.join(output) + '\n'

    def render_text_container(self, contents, container_class):
        output = []
        output.append(self.open_container(container_class))
        output.append(contents)
        output.append(self.close_container())
        return '\n'.join(output) + '\n'

    def render_top_banner(self, data):
        return self._t.render_title_bar(data) + '\n'

    def start_html(self):
        return self._t.header +'\n'

    def end_html(self):
        return self._t.render_closing()





