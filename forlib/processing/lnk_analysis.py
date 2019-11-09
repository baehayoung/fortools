from datetime import datetime, timedelta
import struct
from bitstring import BitArray
import os

class LnkAnalysis:

    def __init__(self, file, path):
        self.file = file
        self.path = path
        self.lnk_flag = []
        self.locbase_path_uni = None
        self.start_off = None
        self.info_size = None
        self.info_flag = None
        self.extra_off = None
        self.extra_data = None
        self.linkinfo_flag = None

    def __link_flag(self, flags_to_parse):
        flags = {0: "HasLinkTargetIDList",
                 1: "HasLinkInfo",
                 2: "HasName",
                 3: "HasRelativePath",
                 4: "HasWorkingDir",
                 5: "HasArguments",
                 6: "HasIconLocation",
                 7: "IsUnicode",
                 8: "ForceNoLinkInfo",
                 9: "HasExpString",
                 10: "RunInSeparateProcess",
                 11: "Unused1",
                 12: "HasDarwinID",
                 13: "RunAsUser",
                 14: "HasExpIcon",
                 15: "NoPidlAlias",
                 16: "Unused2",
                 17: "RunWithShimLayer",
                 18: "ForceNoLinkTrack",
                 19: "EnableTargetMetadata",
                 20: "DisableLinkPathTracking",
                 21: "DisableKnownFolderTracking",
                 22: "DisableKnownFolderAlias",
                 23: "AllowLinkToLink",
                 24: "UnaliasOnSave",
                 25: "PreferEnvironmentPath",
                 26: "KeepLocalIDListForUNCTarget"
                 }

        for count, items in enumerate(flags_to_parse):
            if int(items) == 1:
                self.lnk_flag.append(format(flags[count]))
            else:
                continue

        return self.lnk_flag

    def __lnk_attrib(self, attrib_to_parse):
        attrib = {0: "FILE_ATTRIBUTE_READONLY",
                  1: "FILE_ATTRIBUTE_HIDDEN",
                  2: "FILE_ATTRIBUTE_SYSTEM",
                  3: "Reserved1",
                  4: "FILE_ATTRIBUTE_DIRECTORY",
                  5: "FILE_ATTRIBUTE_ARCHIVE",
                  6: "Reserved2",
                  7: "FILE_ATTRIBUTE_NORMAL",
                  8: "FILE_ATTRIBUTE_TEMPORARY",
                  9: "FILE_ATTRIBUTE_SPARSE_FILE",
                  10: "FILE_ATTRIBUTE_REPARSE_POINT",
                  11: "FILE_ATTRIBUTE_COMPRESSED",
                  12: "FILE_ATTRIBUTE_OFFLINE",
                  13: "FILE_ATTRIBUTE_NOT_CONTENT_INDEXED",
                  14: "FILE_ATTRIBUTE_ENCRYPTED"
                  }

        lnk_attributes = []
        for count, items in enumerate(attrib_to_parse):
            if int(items) == 1:
                print('Link Attribute: ' + format(attrib[count]))
                lnk_attributes.append(format(attrib[count]))
            else:
                continue

        return lnk_attributes

    def __drive_type_list(self, drive):
        drive_type = {
            0: 'DRIVE_UNKNOWN',
            1: 'DRIVE_NO_ROOT_DIR',
            2: 'DRIVE_REMOVABLE',
            3: 'DRIVE_FIXED',
            4: 'DRIVE_REMOTE',
            5: 'DRIVE_CDROM',
            6: 'DRIVE_RAMDISK'
        }

        drive_type_list = []
        for count, items in enumerate(drive):
            if int(items) == 1:
                print('Drive Type: ' + format(drive_type[count]))
                drive_type_list.append(format(drive_type[count]))
            else:
                continue

        return drive_type_list

    ################ Shell_Link_Header #############################

    # show link flag
    def __link_flags(self):
        self.file.seek(20)
        flags = struct.unpack('<i', self.file.read(4))
        file_flags = BitArray(hex(flags[0]))
        self.__link_flag(file_flags.bin)

    def file_attribute(self):
        self.file.seek(24)
        attributes = struct.unpack('<i', self.file.read(4))
        flag_atributes = BitArray(hex(attributes[0]))
        flag_atributes = self.__lnk_attrib(flag_atributes.bin)

        return flag_atributes

    # Target File time
    def creation_time(self):
        self.file.seek(28)
        c_time = self.file.read(8)
        c_time = struct.unpack('<q', c_time)
        c_time = convert_time(c_time)
        print('Target File Creation Time: ' + str(c_time) + 'UTC+9:00')

        return c_time

    def access_time(self):
        self.file.seek(36)
        a_time = self.file.read(8)
        a_time = struct.unpack_from('<q', a_time)[0]
        a_time = convert_time(a_time)
        print('Target File Access Time: ' + str(a_time) + 'UTC+9:00')

        return a_time

    def write_time(self):
        self.file.seek(44)
        w_time = self.file.read(8)
        w_time = struct.unpack('<q', w_time)[0]
        w_time = convert_time(w_time)
        print('Target File Write Time: ' + str(w_time) + 'UTC+9:00')

        return w_time

    # Link file Time

    def lnk_creation_time(self):
        c_time = datetime.fromtimestamp(os.path.getctime(self.path))
        print('Link File Creation Time: ' + str(c_time) + ' UTC+9:00')

        return c_time

    def lnk_access_time(self):
        a_time = datetime.fromtimestamp(os.path.getatime(self.path))
        print('Link File Last Access Time: ' + str(a_time) + ' UTC+9:00')

        return a_time

    def lnk_write_time(self):
        w_time = datetime.fromtimestamp(os.path.getmtime(self.path))
        print('Link File Write Time: ' + str(w_time) + ' UTC+9:00')

        return w_time

    def file_size(self):
        self.file.seek(52)
        file_size = struct.unpack('<l', self.file.read(4))[0]
        print('Target File Size : ' + str(file_size) + 'bytes')

        return file_size

    def iconindex(self):
        self.file.seek(56)
        iconindex = struct.unpack('<l', self.file.read(4))[0]
        print('Iconindex : ' + str(iconindex))

        return iconindex

    def show_command(self):
        self.file.seek(60)
        showcomand = struct.unpack('<i', self.file.read(4))[0]
        showcomand = hex(showcomand)
        if showcomand == hex(0x1):
            showcomand = 'SW_SHOWNORMAL'
        elif showcomand == hex(0x3):
            showcomand = 'SW_SHOWMAXIMIZED'
        elif showcomand == hex(0x7):
            showcomand = 'SW_SHOWMINNOACTIVE'
        else:
            showcomand = 'SW_SHOWNORMAL(default)'

        print('Showcomand: ' + str(showcomand))

        return showcomand

    ################ Link_Info #############################

    def __linkinfo_off(self):
        self.__link_flags()

        if 'HasLinkInfo' not in self.lnk_flag:
            self.linkinfo_flag = None
        else:
            self.linkinfo_flag = 'True'

        if 'HasLinkTargetIDList' not in self.lnk_flag:
            self.start_off = 76
        else:
            self.file.seek(76)
            items_hex = self.file.read(2)
            b = (b'\x00\x00')
            items_hex = items_hex + b
            idlistsize = struct.unpack('<i', items_hex)[0]
            self.start_off = 78 + idlistsize

        self.file.seek(self.start_off)
        self.info_size = struct.unpack('<i', self.file.read(4))[0]
        info_header_size = self.file.read(4)
        if info_header_size == '\x00\x00\x00\x1C':
            info_option = 'False'
        else:
            info_option = 'True'
        self.info_flag = self.file.read(4)
        if self.info_flag == '\x00\x00\x00\x01':
            self.info_flag = 'A'
            # volume = 'True'
            # locbase_path = 'True'
            # net = None
            if info_option == 'True':
                self.locbase_path_uni = 'True'
            else:
                self.locbase_path_uni = None
        else:
            self.info_flag = 'B'
            # volume = None
            # locbase_path = None
            # net = 'True'
            self.locbase_path_uni = None

    def volume(self):
        self.__linkinfo_off()

        if self.linkinfo_flag != 'True':
            print('link info (X)')
            return [0, 0, 0]
        elif self.info_flag != 'A':
            print('volume id (X)')
            return [0, 0, 0]

        vol_off = self.start_off + 12
        self.file.seek(vol_off)
        volumeid_off = struct.unpack('<i', self.file.read(4))[0]
        volumeid_off = volumeid_off + self.start_off
        self.file.seek(volumeid_off)

        vol_size = struct.unpack('<i', self.file.read(4))[0]

        drive_type = struct.unpack('<i', self.file.read(4))[0]
        drive_type = self.__drive_type_list(drive_type)

        driveserialnumber = struct.unpack('<l', self.file.read(4))[0]
        print('Driveserialnumber: ' + str(driveserialnumber))

        volumelable_off = self.file.read(4)
        if volumelable_off != '0x00000014':
            volumelable_off = struct.unpack('<l', volumelable_off)[0]
            vol_lable_off = volumelable_off
            volumelable_off = volumeid_off + volumelable_off
        else:
            volumelable_off_uni = struct.unpack('<l', self.file.read(4))[0]
            vol_lable_off = volumelable_off_uni
            volumelable_off = volumeid_off + volumelable_off_uni
        self.file.seek(volumelable_off)
        volumelable_size = vol_size - vol_lable_off
        volumelable = self.file.read(volumelable_size)
        volumelable = volumelable.decode('cp1252')
        print('Volumelable: ' + volumelable)

        return [drive_type, driveserialnumber, volumelable]

    def localbase_path(self):
        self.__linkinfo_off()

        if self.linkinfo_flag != 'True':
            print('this file does not have link info')
            return [0, 0]
        elif self.info_flag != 'A':
            print('locabasepath (X), locabasepathunicode (X)')
            return [0, 0]
        elif self.locbase_path_uni != 'True':
            print('locbasepathoffsetunicode : 0\n locbasepathunicode : unknown')
        else:
            locbase_path_off_uni = self.start_off + 28
            self.file.seek(locbase_path_off_uni)
            locbase_path_off_uni = struct.unpack('<l', self.file.read(4))[0]
            self.locbase_path_uni = locbase_path_off_uni + self.start_off
            self.file.seek(self.locbase_path_uni)
            self.locbase_path_uni = self.file.read(100)
            self.locbase_path_uni = self.locbase_path_uni.decode('utf-8', 'ignore')
            self.locbase_path_uni = []
            for i in self.locbase_path_uni.split('\x00\x00'):
                self.locbase_path_uni.append(i)
            print('Localbasepathunicode: ' + self.locbase_path_uni[0])

        locbasepath_off = self.start_off + 16
        self.file.seek(locbasepath_off)
        locbasepath_off = struct.unpack('<l', self.file.read(4))[0]
        locbasepath_off = locbasepath_off + self.start_off

        self.file.seek(locbasepath_off)
        locbasepath = self.file.read(100)
        locbasepath = locbasepath.decode('utf-8', 'ignore')
        locbasepath = []
        for i in locbasepath.split('\x00\x00'):
            locbasepath.append(i)
        print('Localbasepath: ' + locbasepath[0])

        return [self.locbase_path_uni, locbasepath]

    ################ Extra_Data #############################
    def __extradata_size(self, string_off):
        self.file.seek(string_off)
        string_size = self.file.read(2)
        b = (b'\x00\x00')
        string_size = string_size + b
        string_size = struct.unpack('<i', string_size)[0]
        string_off = string_size + string_off + 2
        # if you want to read string, use this
        # relative_path = str(file.read(string_size))
        # relative_path = relative_path.replace('\x00','').encode('utf-8', 'ignore').decode('utf-8')
        return string_off

    def __extradata(self):
        self.__linkinfo_off()

        string_off = self.start_off + self.info_size

        if 'HasName' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        elif 'HasRelativePath' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        elif 'HasWorkingDir' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        elif 'HasArguments' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        elif 'HasIconLocation' in self.lnk_flag:
            string_off = self.__extradata_size(string_off)

        self.extra_off = string_off
        block_signature = self.extra_off + 4
        self.file.seek(block_signature)
        block_signature = self.file.read(4)
        if block_signature == '\xA0\x00\x00\x03':
            self.extra_data = 'True'
        else:
            self.extra_data = None


    def netbios(self):
        self.__extradata()

        if self.extra_data != 'True':
            print('extra data (X)')
            return 0
        netbios = self.extra_off + 16
        self.file.seek(netbios)
        netbios = str(self.file.read(16))
        netbios = netbios.replace('\x00', '').encode('utf-8', 'ignore').decode('utf-8')
        print('NetBios: ' + str(netbios))

        return netbios

    def machine_id(self):
        self.__extradata()

        if self.extra_data != 'True':
            print('extra data (X)')
            return [0, 0]
        droid = self.extra_off + 32
        self.file.seek(droid)
        droid = str(self.file.read(32))
        droid = droid.replace('\x00', '').encode('utf-8', 'ignore').decode('utf-8')
        print('Droid' + str(droid))
        droidbirth = str(self.file.read(32))
        droidbirth = droidbirth.replace('\x00', '').encode('utf-8', 'ignore').decode('utf-8')
        print('DroidBirth' + str(droidbirth))

        return [droid, droidbirth]

    def show_all_info(self):
        info_list = []
        info = dict()
        info["file attributes"] = str(self.file_attribute())
        info["target file creation time"] = str(self.creation_time())
        info["target file access time"] = str(self.access_time())
        info["target file write time"] = str(self.write_time())
        info["link file creation time"] = str(self.lnk_creation_time())
        info["link file access time"] = str(self.lnk_access_time())
        info["link file write time"] = str(self.lnk_write_time())
        info["file size"] = str(self.file_size())
        info["icon index"] = str(self.iconindex())
        info["show command"] = str(self.show_command())
        volume = str(self.volume())
        info["drive type"] = volume[0]
        info["drive serial number"] = volume[1]
        info["volume lable"] = volume[2]
        localbase = str(self.localbase_path())
        info["localbasepathunicode"] = localbase[0]
        info["localbasepath"] = localbase[1]
        info["netbios"] = str(self.netbios())
        machine = str(self.machine_id())
        info["droid"] = machine[0]
        info["droid birth"] = machine[1]

        print(info)
        info_list.append(info)
        return info_list


def convert_time(time):
    time = '%016x' % time
    time = int(time, 16) / 10.
    time = datetime(1601, 1, 1) + timedelta(microseconds=time) + timedelta(hours=9)
    return time        
