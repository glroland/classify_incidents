""" List of Actions supported in web page """

class WebsiteActions():
    """ List of website actions """

    # Action Key Values
    HOME = "home"
    CREATE_EVALUATION = "create"
    VIEW_EVALUATION = "view"
    PLAYGROUND = "playground"

    class ViewPageSubactions():
        """ List of view page actions """

        HOME = "home"
        IMPORT = "import"

    view_subactions = ViewPageSubactions()

actions = WebsiteActions()
