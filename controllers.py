import os
import sys
import jinja2 as jj

class BuildController():
    def __init__(self, parent=None):
        pass

    @staticmethod
    def resource_path(relative_path: str):
        """
        Replaces something like.. 'logo.png' with the real path when bundling with pyinstaller. 
        The assets all need to be named and defined as their path so pyinstaller knows where the item is.
        This is pretty much the only workaround except for fetching the assets at a server location
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

class TemplateController():
    def __init__(self, template_dir):
        # Sets the template directory
        file_loader = jj.FileSystemLoader(BuildController.resource_path(template_dir))
        self.env = jj.Environment(loader=file_loader)

    def build_template(self, template_name: str, file_name_with_path: str, args: dict) -> None:
        template = self.env.get_template(template_name)
        self.create_static_file(file_name_with_path, template.render(args=args))

    def create_static_file(self, file_name_with_path: str, markup: str) -> None:
        with open(file_name_with_path, 'w', encoding="utf-8") as f:
            f.write(markup)
            f.close()