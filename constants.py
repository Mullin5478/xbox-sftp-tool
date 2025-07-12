from enum import IntEnum

class XEP_DEVICE(IntEnum):
    XDeviceHdd = 0x0000
    XDeviceOdd = 0x0001
    XDeviceFlash = 0x0002
    XDeviceXBlb = 0x0003
    XDeviceXtf = 0x0004
    XDeviceXbox = 0x0005
    XDeviceSra = 0x0006
    XDeviceIndexMax = 0x0007

class XCRD_ID(IntEnum):
    XCrdTemp = 0x0000
    XCrdUserContent = 0x0001
    XCrdSystemSupport = 0x0002
    XCrdSystemUpdate = 0x0003
    XCrdEraLaunch = 0x0004
    XCrdFutureGrowth = 0x0005
    XCrdXtfRemote = 0x0007
    XCrdXBlb = 0x0008
    XCrdOdd = 0x0009
    XCrdEmbeddedXvd = 0x000a
    XCrdTransferStorage0 = 0x000b
    XCrdExternalStorage0 = 0x0013
    XCrdXbox = 0x001b
    XCrdSraFile = 0x001c
    XCrdFlashApps = 0x001d

DEVICE_PATH_MAP = {
    'U:\\': 'XDeviceHdd',
    'D:\\': 'XDeviceOdd',
    'X:\\': 'XDeviceFlash',
    'Y:\\': 'XDeviceFlash',
    'Z:\\': 'XDeviceFlash'
}

XCRD_ID_MAP = {
    'U:\\': 'XCrdUserContent',
    'D:\\': 'XCrdOdd',
    'X:\\': 'XCrdSystemSupport',
    'Y:\\': 'XCrdSystemSupport',
    'Z:\\': 'XCrdSystemSupport'
}
