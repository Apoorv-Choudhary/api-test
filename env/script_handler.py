import os
import sys
import traceback


class ScriptHandler:
    def __init__(self, **kwargs):
        self.feature_dir = kwargs.get("feature_dir", "")
        if not self.feature_dir or not os.path.isdir(
            os.path.join(os.getcwd(), self.feature_dir)
        ):
            raise "feature directory not found."
        self.pre_scripts = self.get_script_names(
            "pre", kwargs.get("pre_scripts", "none")
        )
        self.coincident_scripts = self.get_script_names(
            "coincident", kwargs.get("coincident_scripts", "none")
        )
        self.post_scripts = self.get_script_names(
            "post", kwargs.get("post_scripts", "all")
        )

    def get_script_names(self, script_type, scripts):
        if isinstance(scripts, str) and scripts.lower() == "none":
            return {}
        elif isinstance(scripts, dict):
            return scripts
        elif isinstance(scripts, str) and scripts.lower() == "all":
            script_names = os.listdir(os.path.join(self.feature_dir, script_type))
            return dict(
                (each.replace(".py", ""), [])
                for each in script_names
                if each.endswith(".py")
            )

    def run_script(self, script_name, script_type, args=[]):
        script_path = ".".join(
            self.feature_dir.split(os.sep) + [script_type, script_name]
        )
        m = __import__(script_path)
        for submodule_name in script_path.split(".")[1:]:
            m = getattr(m, submodule_name)

        try:
            if hasattr(m, "main") and callable(getattr(m, "main")):
                main_method = getattr(m, "main")
                main_method(args)
            else:
                raise AttributeError(
                    f"'main' method does not exist in {script_type}/{script_name} script."
                )
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error_obj = traceback.format_exception(exc_obj)
            msg1 = error_obj[-2] if len(error_obj) >= 2 else None
            msg2 = error_obj[-1]
            if msg1:
                root_path = os.getcwd()
                msg1 = (
                    'Traceback:\nFile "'
                    + msg1.split(root_path + os.sep)[-1].split(self.feature_dir)[-1]
                )
                print(msg1)
            print(msg2)
