import simplejson as json


class HSProperty:

    def __init__(self, name, **kwargs):

        self.name = name.replace(" ", "_").tolower()
        self.label = kwargs.get("label", name)
        self.description = kwargs.get("description")
        self.groupName = kwargs.get("groupName", "contactinformation")
        self.type = kwargs.get("type", "string")
        self.fieldType = kwargs.get("fieldType")
        self.formField = kwargs.get("formField", True)
        self.displayOrder = kwargs.get("displayOrder", 6),
        self.options = kwargs.get("options", [])

        if not self.fieldType:
            if self.type == "string":
                self.fieldType = "text"
            elif self.type == "number":
                self.fieldType = "number"
            elif self.type == "bool":
                self.property_type = "enumeration"
                self.fieldType = "booleancheckbox"
                self.options = [
                    {
                        "displayOrder": -1,
                        "label": "Yes",
                        "value": "true"
                    },
                    {
                        "displayOrder": -1,
                        "label": "No",
                        "value": "false"
                    }
                ]
            elif self.type == "datetime":
                self.fieldType = "date"
            elif self.type == "enumeration":
                self.fieldType = "checkbox"

    def update(self, **kwargs):
        for item, value in kwargs.iteritems():
            setattr(self, item, value)

    def add_option(self, option, value):
        new_option = {
            "label": option,
            "value": value,
        }
        self.options.append(new_option)

    def add_options(self, options):
        for option in options:
            self.add_option(option=option[0], value=option[1])

    def remove_option(self, target):
        self.options = [option for option in self.options if option["label"] != target]

    def remove_options(self, targets):
        self.options = [option for option in self.options if option["label"] not in targets]

    def to_json(self):
        json_data = {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "groupName": self.groupName,
            "displayOrder": self.displayOrder,
            "formField": self.formField,
            "type": self.type,
            "fieldType": self.fieldType,
            "options": self.options,
        }
        return json.dumps(json_data)

    @classmethod
    def from_json(cls, data):
        hsproperty = HSProperty()
        try:
            hsproperty.name = data["name"]
            hsproperty.label = data["label"]
            hsproperty.description = data["description"]
            hsproperty.groupName = data["groupName"]
            hsproperty.displayOrder = data["displayOrder"]
            hsproperty.type = data["type"]
            hsproperty.fieldType = data["fieldType"]
            hsproperty.options = data["options"]
        except Exception as exc:
            raise SyntaxError(
                "There is an error in the property data you submitted to this function. "
                "Expected to find a fully formed property object, and instead found missing data. "
                "Refer to the original exception message for details: {exc}".format(exc=exc)
            )
        else:
            return hsproperty
