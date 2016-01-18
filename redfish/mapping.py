# coding=utf-8

redfish_mapper = None
redfish_version = None
redfish_root_name = None

class RedfishVersionMapping(object):
    '''Implements basic url path mapping beetween Redfish versions.'''

    def __init__(self, version, rootname):
        self.__version = version
        self.__rootname = rootname

    def map_sessionservice(self):
        if self.__version == '0.95':
            return 'Sessions'
        return 'SessionService'

    def map_links(self, data_dict=None):
        if data_dict == None:
            if self.__version == '0.95':
                return 'links'
        else:
            # Checking if we have Links or links.
            # This is to deal with proliant firmware 2.40 bug that reports
            # incorrectly links instead of Links (Redfish standard)
            try:
                data_dict.links
                return 'links'
            except AttributeError:
                pass
        return 'Links'

    def map_links_ref(self, data_dict=None):
        if data_dict == None:
            if self.__version == '0.95':
                return 'href'
        else:
            # Checking if we have @odata.id or href.
            # This is to deal with proliant firmware 2.40 bug that reports
            # incorrectly href instead of @odata.id (Redfish standard)
            try:
                data_dict.href
                return 'href'
            except AttributeError:     
                pass       
        return '@odata.id'
    
    def map_members(self):
        if self.__version == '0.95':
            return 'Member'
        return 'Members'