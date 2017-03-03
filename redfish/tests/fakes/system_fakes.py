# coding=utf-8


def fake_system_data():

    return {
    u'PowerState': u'On',
    u'Processors': {
        u'@odata.id': u'/redfish/v1/Systems/1/Processors'
    },
    u'UUID': u'00000000-0000-0000-0000-000000000000',
    u'SimpleStorage': {
        u'@odata.id': u'/redfish/v1/Systems/1/SimpleStorage'
    },
    u'SerialNumber': u'2M220100SL',
    u'Boot': {
        u'BootSourceOverrideTarget': u'Pxe',
        u'BootSourceOverrideTarget@Redfish.AllowableValues': [
            u'None',
            u'Pxe',
            u'Floppy',
            u'Cd',
            u'Usb',
            u'Hdd',
            u'BiosSetup',
            u'Utilities',
            u'Diags',
            u'UefiTarget'
        ],
        u'BootSourceOverrideEnabled': u'Once',
        u'UefiTargetBootSourceOverride': u'uefidevicepath'
    },
    u'@odata.id': u'/redfish/v1/Systems/1',
    u'IndicatorLED': u'Off',
    u'Status': {
        u'HealthRollUp': u'OK',
        u'State': u'Enabled',
        u'Health': u'OK'
    },
    u'LogServices': {
        u'@odata.id': u'/redfish/v1/Systems/1/Logs'
    },
    u'MemorySummary': {
        u'Status': {
            u'HealthRollUp': u'OK',
            u'State': u'Enabled',
            u'Health': u'OK'
        },
        u'TotalSystemMemoryGiB': 16
    },
    u'Actions': {
        u'#ComputerSystem.Reset': {
            u'ResetType@Redfish.AllowableValues': [
                u'On',
                u'ForceOff',
                u'GracefulRestart',
                u'ForceRestart',
                u'Nmi',
                u'GracefulRestart',
                u'ForceOn',
                u'PushPowerButton'
            ],
            u'target': u'/redfish/v1/Systems/1/Actions/ComputerSystem.Reset'
        },
        u'Oem': {
            u'#Contoso.Reset': {
                u'target': u'/redfish/v1/Systems/1/OEM/Contoso/Actions/Contoso.Reset'
            }
        }
    },
    u'PartNumber': u'',
    u'ProcessorSummary': {
        u'Count': 8,
        u'Status': {
            u'HealthRollUp': u'OK',
            u'State': u'Enabled',
            u'Health': u'OK'
        },
        u'Model': u'Multi-CoreIntel(R)Xeon(R)processor7xxxSeries'
    },
    u'Model': u'ModelName',
    u'Name': u'MyComputerSystem',
    u'@odata.type': u'#ComputerSystem.1.0.0.ComputerSystem',
    u'EthernetInterfaces': {
        u'@odata.id': u'/redfish/v1/Systems/1/EthernetInterfaces'
    },
    u'Description': u'Descriptionofserver',
    u'Links': {
        u'ManagedBy': [
            {
                u'@odata.id': u'/redfish/v1/Managers/1'
            }
        ],
        u'Chassis': [
            {
                u'@odata.id': u'/redfish/v1/Chassis/1'
            }
        ],
        u'Oem': {

        }
    },
    u'SystemType': u'Physical',
    u'HostName': u'web-srv344',
    u'@odata.context': u'/redfish/v1/$metadata#Systems/Members/$entity',
    u'AssetTag': u'freeformassettag',
    u'@Redfish.Copyright': u' Inc.(DMTF).Allrightsreserved.',
    u'Oem': None,
    u'Id': u'1',
    u'Manufacturer': u'ManufacturerName'
}