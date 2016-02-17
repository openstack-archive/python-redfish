# coding=utf-8

import pprint
import re
from urlparse import urljoin
import requests
import simplejson
import tortilla
import config
import mapping
import exception

# Global variable


class Base(object):
    '''Abstract class to manage types (Chassis, Servers etc...).'''
    def __init__(self, url, connection_parameters):
        '''Class constructor'''
        global TORTILLADEBUG
        self.connection_parameters = connection_parameters # Uggly hack to check
        self.url = url
        self.api_url = tortilla.wrap(url, debug=config.TORTILLADEBUG)

        try:
            if connection_parameters.auth_token is None:
                self.data = self.api_url.get(verify=connection_parameters.verify_cert)
            else:
                self.data = self.api_url.get(verify=connection_parameters.verify_cert,
                                             headers={'x-auth-token': connection_parameters.auth_token}
                                             )
        except requests.ConnectionError as e:
            # Log and transmit the exception.
            config.logger.info('Raise a RedfishException to upper level')
            msg = 'Connection error : {}\n'.format(e.message)
            raise exception.ConnectionFailureException(msg)
        except simplejson.scanner.JSONDecodeError as e:
            # Log and transmit the exception.
            config.logger.info('Raise a RedfishException to upper level')
            msg = \
                'Ivalid content : Content does not appear to be a valid ' + \
                'Redfish json\n'
            raise exception.InvalidRedfishContentException(msg)
        except TypeError as e:
            # This happen connecting to a manager using non trusted
            # SSL certificats.
            # The exception is not what could be expected in such case but this
            # is the one provided by Tortilla.
            config.logger.info('Raise a RedfishException to upper level')
            msg = 'Connection error\n'
            raise exception.NonTrustedCertificatException(msg)
        config.logger.debug(self.data)

    def get_link_url(self, link_type):
        '''Need to be explained.

        :param parameter_name: name of the parameter
        :returns:  string -- parameter value
        '''
        self.links = []

        # Manage standard < 1.0
        if float(mapping.redfish_version) < 1.00:
            links = getattr(self.data, mapping.redfish_mapper.map_links())
            if link_type in links:
                return urljoin(self.url, links[link_type][mapping.redfish_mapper.map_links_ref()])
        else:
            links = getattr(self.data, link_type)
            link = getattr(links, mapping.redfish_mapper.map_links_ref())
            return urljoin(self.url, link)

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    def get_parameter(self, parameter_name):
        '''Generic function to get a specific parameter

        :param parameter_name: name of the parameter
        :returns:  string -- parameter value

        '''
        try:
            return self.data[parameter_name]
        except:
            return 'Parameter does not exist'

    def get_parameters(self):
        '''Generic function to get all parameters

        :returns:  string -- parameter value

        '''
        try:
            return self.data
        except:
            return -1

    def set_parameter(self, parameter_name, value):
        '''Generic function to set a specific parameter

        :param parameter_name: name of the parameter
        :param value: value to set
        :returns:   string -- http response of PATCH request

        '''
        # Craft the request
        action = dict()
        action[parameter_name] = value
        config.logger.debug(action)

        # Perform the POST action
        config.logger.debug(self.api_url)
        response = self.api_url.patch(
            verify=self.connection_parameters.verify_cert,
            headers={'x-auth-token': self.connection_parameters.auth_token},
            data=action)
        return response

    def get_name(self):
        '''Get root name

        :returns:  string -- root name or "Not available"

        '''
        try:
            return self.data.Name
        except AttributeError:
            return "Not available"


class BaseCollection(Base):
    '''Abstract class to manage collection (Chassis, Servers etc...).'''
    def __init__(self, url, connection_parameters):
        super(BaseCollection, self).__init__(url, connection_parameters)

        self.links = []

        #linksmembers = self.data.Links.Members
        #linksmembers = self.data.links.Member
        if float(mapping.redfish_version) < 1.00:
            linksmembers = getattr(self.data, mapping.redfish_mapper.map_links())
            linksmembers = getattr(linksmembers, mapping.redfish_mapper.map_members())
        else:
            linksmembers = getattr(self.data, mapping.redfish_mapper.map_members())
        for link in linksmembers:
            #self.links.append(getattr(link,'@odata.id'))
            #self.links.append(getattr(link,'href'))
            self.links.append(urljoin(self.url, getattr(link, mapping.redfish_mapper.map_links_ref())))

        config.logger.debug(self.links)


class Root(Base):
    '''Class to manage redfish Root data.'''
    def get_api_version(self):
        '''Return api version.

        :returns:  string -- version
        :raises: AttributeError

        '''
        try:
            version = self.data.RedfishVersion
        except AttributeError:
            version = self.data.ServiceVersion

        version = version.replace('.', '')
        version = version[0] + '.' + version[1:]
        return(version)

    def get_api_UUID(self):
        '''Return UUID version.

        :returns:  string -- UUID

        '''
        return self.data.UUID

    def get_api_link_to_server(self):
        '''Return api link to server.

        :returns:  string -- path

        '''
        return getattr(self.root.Links.Systems, '@odata.id')


class SessionService(Base):
    '''Class to manage redfish SessionService data.'''
    pass


class Managers(Base):
    '''Class to manage redfish Managers.'''
    def __init__(self, url, connection_parameters):
        super(Managers, self).__init__(url, connection_parameters)
        try:
            # New proliant firmware now respects Redfish v1.00, so seems to correct below statement
            # TODO : better handle exception and if possible support old firmware ?
            self.ethernet_interfaces_collection = \
                EthernetInterfacesCollection(
                    self.get_link_url('EthernetInterfaces'),
                    connection_parameters)

            # Works on proliant, need to treat 095 vs 0.96 differences
            #self.ethernet_interfaces_collection = EthernetInterfacesCollection(
            #                                            self.get_link_url('EthernetNICs'),
            #                                            connection_parameters
            #                                            )
        except exception.InvalidRedfishContentException:
            # This is to avoid invalid content from the mockup
            self.ethernet_interfaces_collection = None

        except AttributeError:
            # This means we don't have EthernetInterfaces
            self.ethernet_interfaces_collection = None

    def get_firmware_version(self):
        '''Get firmware version of the manager

        :returns:  string -- bios version or "Not available"

        '''
        try:
            return self.data.FirmwareVersion
        except AttributeError:
            # We are here because the attribute could be not defined.
            # This is the case with the mockup for manager 2 and 3
            return "Not available"

    def get_type(self):
        '''Get manager type

        :returns:  string -- manager type or "Not available"

        '''
        try:
            return self.data.ManagerType
        except AttributeError:
            return "Not available"

    def get_uuid(self):
        '''Get manager type

        :returns:  string -- manager uuid or "Not available"

        '''
        try:
            return self.data.UUID
        except AttributeError:
            return "Not available"

    def get_status(self):
        '''Get manager status

        :returns:  string -- manager status or "Not available"

        '''
        try:
            return self.data.Status.State
        except AttributeError:
            return "Not available"

    def get_managed_chassis(self):
        '''Get managed chassis ids by the manager

        :returns:  list -- chassis ids or "Not available"

        '''
        chassis_list = []
        links = getattr(self.data, mapping.redfish_mapper.map_links(self.data))

        try:
            for chassis in links.ManagerForChassis:
                result = re.search(r'Chassis/(\w+)', chassis[mapping.redfish_mapper.map_links_ref(chassis)])
                chassis_list.append(result.group(1))
            return chassis_list
        except AttributeError:
            return "Not available"

    def get_managed_systems(self):
        '''Get managed systems ids by the manager

        :returns:  list -- chassis ids or "Not available"

        '''
        systems_list = []
        links = getattr(self.data, mapping.redfish_mapper.map_links(self.data))

        try:
            for systems in links.ManagerForServers:
                result = re.search(r'Systems/(\w+)', systems[mapping.redfish_mapper.map_links_ref(systems)])
                systems_list.append(result.group(1))
            return systems_list
        except AttributeError:
            return "Not available"

    def reset(self):
        '''Reset the manager.

        :returns:  string -- http response of POST request

        '''
        # Craft the request
        link = getattr(self.data.Actions, "#Manager.Reset")
        link = link.target

        reset_url = urljoin(self.url, link)

        response = requests.post(
            reset_url,
            verify=self.connection_parameters.verify_cert,
            headers={'x-auth-token': self.connection_parameters.auth_token,
                     'Content-type': 'application/json'})
        # TODO : treat response.
        return response


class ManagersCollection(BaseCollection):
    '''Class to manage redfish ManagersCollection data.'''
    def __init__(self, url, connection_parameters):
        '''Class constructor'''
        super(ManagersCollection, self).__init__(url, connection_parameters)
        self.managers_dict = {}
        for link in self.links:
            index = re.search(r'Managers/(\w+)', link)
            self.managers_dict[index.group(1)] = Managers(link, connection_parameters)


class Systems(Base):
    '''Class to manage redfish Systems data.'''
    # TODO : Need to discuss with Bruno the required method.
    #        Also to check with the ironic driver requirement.
    def __init__(self, url, connection_parameters):
        '''Class constructor'''
        super(Systems, self).__init__(url, connection_parameters)
        try:
            self.bios = Bios(url + 'Bios/Settings', connection_parameters)
        except:
            pass

    def reset_system(self):
        '''Force reset of the system.

        :returns:  string -- http response of POST request

        '''
        # Craft the request
        action = dict()
        action['Action'] = 'Reset'
        action['ResetType'] = 'ForceRestart'

        #Debug the url and perform the POST action
        #print self.api_url
        response = self.api_url.post(verify=self.connection_parameters.verify_cert,
                                     headers={'x-auth-token': self.connection_parameters.auth_token},
                                     data=action
                                    )
        #TODO : treat response.
        return response

    def get_bios_version(self):
        '''Get bios version of the system.

        :returns:  string -- bios version

        '''
        try:
            # Returned by proliant
            return self.data.Bios.Current.VersionString
        except:
            # Returned by mockup.
            # Hopefully this kind of discrepencies will be fixed with Redfish 1.0 (August)
            return self.data.BiosVersion

    def get_serial_number(self):
        '''Get serial number of the system.

        :returns:  string -- serial number

        '''
        try:
            # Returned by proliant
            return self.data.SerialNumber
        except:
            # Returned by mockup.
            # Hopefully this kind of discrepencies will be fixed with Redfish 1.0 (August)
            return ''

    def get_power(self):
        '''Get power status of the system.

        :returns:  string -- power status or NULL if there is an issue

        '''
        try:
            return self.data.Power
        except:
            return ''

    def set_parameter_json(self, value):
        '''Generic function to set any system parameter using json structure

        :param value: json structure with value to update
        :returns:   string -- http response of PATCH request

        '''
        # perform the POST action
        #print self.api_url.url()
        response = requests.patch(self.api_url.url(),
                                  verify=self.connection_parameters.verify_cert,
                                  headers={'x-auth-token': self.connection_parameters.auth_token, 'Content-type': 'application/json'},
                                  data=value)
        return response.reason

    def set_boot_source_override(self, target, enabled):
        '''Shotcut function to set boot source

        :param target: new boot source. Supported values:
            "None",
            "Pxe",
            "Floppy",
            "Cd",
            "Usb",
            "Hdd",
            "BiosSetup",
            "Utilities",
            "Diags",
            "UefiShell",
            "UefiTarget"
        :param enabled: Supported values:
            "Disabled",
            "Once",
            "Continuous"
        :returns:   string -- http response of PATCH request
        '''
        return self.set_parameter_json('{"Boot": {"BootSourceOverrideTarget": "'+target+'"},{"BootSourceOverrideEnabled" : "'+enabled+'"}}')


class SystemsCollection(BaseCollection):
    '''Class to manage redfish SystemsCollection data.'''
    def __init__(self, url, connection_parameters):
        super(SystemsCollection, self).__init__(url, connection_parameters)

        self.systems_dict = {}

        for link in self.links:
            index = re.search(r'Systems/(\w+)', link)
            self.systems_dict[index.group(1)] = Systems(link, connection_parameters)


class Bios(Base):
    '''Class to manage redfish Bios data.'''
    def __init__(self, url, connection_parameters):
        super(Bios, self).__init__(url, connection_parameters)
        self.boot = Boot(re.findall('.+/Bios', url)[0] + '/Boot/Settings', connection_parameters)


class Boot(Base):
    '''Class to manage redfish Boot data.'''
    def __init__(self, url, connection_parameters):
        super(Boot, self).__init__(url, connection_parameters)


class EthernetInterfacesCollection(BaseCollection):
    '''Class to manage redfish EthernetInterfacesColkection data.'''
    def __init__(self, url, connection_parameters):
        super(EthernetInterfacesCollection,
              self).__init__(url, connection_parameters)

        self.ethernet_interfaces_dict = {}

        # Url returned by the mock up is wrong /redfish/v1/Managers/EthernetInterfaces/1 returns a 404. --> this is not true anymore (2016/01/03)
        # The correct one should be /redfish/v1/Managers/1/EthernetInterfaces/1 --> correct by mockup return invalid content (not json)
        # Check more than 1 hour for this bug.... grrr....
        for link in self.links:
            index = re.search(r'EthernetInterfaces/(\w+)', link)
            self.ethernet_interfaces_dict[index.group(1)] = \
                EthernetInterfaces(link, connection_parameters)


class EthernetInterfaces(Base):
    '''Class to manage redfish EthernetInterfaces.'''
    def get_mac(self):
        '''Get EthernetInterface MacAddress

        :returns:  string -- interface macaddress or "Not available"

        '''
        try:
            return self.data.MacAddress
        except AttributeError:
            return "Not available"

    def get_fqdn(self):
        '''Get EthernetInterface fqdn

        :returns:  string -- interface fqdn or "Not available"

        '''
        try:
            return self.data.FQDN
        except AttributeError:
            return "Not available"

    def get_ipv4(self):
        '''Get EthernetInterface ipv4 address

        :returns:  list -- interface ip addresses or "Not available"

        '''

        ipaddresses = []

        try:
            for ip_settings in self.data.IPv4Addresses:
                address = ip_settings['Address']
                ipaddresses.append(address)

            return ipaddresses
        except AttributeError:
            return "Not available"

    def get_ipv6(self):
        '''Get EthernetInterface ipv6 address

        :returns:  list -- interface ip addresses or "Not available"

        '''

        ipaddresses = []

        try:
            for ip_settings in self.data.IPv6Addresses:
                address = ip_settings['Address']
                ipaddresses.append(address)

            return ipaddresses
        except AttributeError:
            return "Not available"

