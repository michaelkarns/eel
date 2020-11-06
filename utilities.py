import eel
import jinja2 as jj
import os
import sys
import shutil
import controllers

class EelApp():
    def __init__(self, options):
        """
            kawrgs = {
                'options': {
                    'dst_dir': '',
                    'src_dir': '',
                    '': '',
                    '': '',
                    '': '',
                    '': '',
                    '': '',
                    '': '',
                }
            }
        """
        assert options['dst_dir'], 'You must supply a destination dir'
        assert options['src_dir'], 'You must supply a source dir'

        self.live_dir = os.path.join(options['dst_dir'], 'live')
        self.dst_dir = options['dst_dir']

        # Remove everything at the destination
        try:
            shutil.rmtree(options['dst_dir'])
        except FileNotFoundError:
            pass

        # copy the source directory to the destination directory
        shutil.copytree(options['src_dir'], options['dst_dir'])

        self.template_controller = controllers.TemplateController(f'{os.path.basename(options["src_dir"])}/templates')

        eel.init(self.dst_dir)

    def start(self):
        # initialize eel and launch index.html
        eel.start(os.path.join(self.dst_dir, 'live\\index.html'))

    def write_new_page(self, template_name: str, args: dict):
        """
        Writes to the index.html in the live folder the markup from a template with supplied arguments
        Then it refreshes the page, note that the base template must contain the following for the refresh to work properly:
        <script>
            eel.expose(reload_page)
            function reload_page() {
                location.reload();
            }
        <script>
        """
        # TODO:
        # add authentication
        # verify the user has the ability to load the page before we do it
        # Need to encrypt all of the templates so that they cant be arbitrarily accessed in the program files
        # could test vpn storage of template files
        self.template_controller.build_template('index.html', os.path.join(self.live_dir, 'index.html'), args)
        eel.reload_page()

if __name__=='__main__':
    pass