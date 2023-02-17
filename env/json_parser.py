class JSONParser:

    def __init__(self, **kwargs):
        self.domain = ""
        self.client_name = ""
        self.controller_name = ""
        self.feature_name = ""
        self.url = kwargs.get("url", "")
        self.method_type = kwargs.get("method_type", "")
        self.arguments = kwargs.get("arguments", {})
        self.body = kwargs.get("body", {})
        # pre_scripts, coincident_scripts, post_scripts accepts "all", "none" or dictionary of script names as key
        # and list of required args as its value.
        self.pre_scripts = kwargs.get("pre_api_methods", "none")
        self.coincident_scripts = kwargs.get("coincident_api_methods", "none")
        self.post_scripts = kwargs.get("post_api_methods", "all")
        self.username = kwargs.get("username", False)
        self.password = kwargs.get("password", False)
        self.parse_data_from_url()

    def validate_json(self):
        # TODO: write logic to validate json input
        pass

    def parse_data_from_url(self):
        """

        :return: parse the url and update all the instance variable of this class
                that are provided by the user.
        """

        url_split = self.url.split("//")
        adaptor = url_split[0]
        temp_url = url_split[1].split("/")
        self.domain = f"{adaptor}//{temp_url[0]}"
        self.client_name = temp_url[1]
        self.controller_name = temp_url[2]
        self.feature_name = temp_url[3]


