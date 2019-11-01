import os
import sys
from forlib.processing.internal import check

class Thumbnail_analysis:
    def __init__(self):
        self.os = None
        self.analysis = None

    def check_os(self, os):
        if os == "win":
            self.analysis = Thumbnail_analysis_windows()

        if self.analysis == None:
            return False

class Thumbnail_analysis_windows:
    def __init__(self, file):
        self.window_version = { "Windows_7": 0x15,
                               "Windows_8": 0x1A,
                               "Windows_8v2": 0x1C,
                               "Windows_8v3": 0x1E,
                               "Windows_8_1": 0x1F,
                               "Windows_10": 0x20}

    def get_data(self, path):
        file = open(path, "rb")

        db_header = {"signature": None,
                     "version": None,
                     "type": None}

        entry_info = {"first_cache_entry": None,        # Windows Vista, 7, 8, 8v2, 8v3, 8_1, 10
                      "available_cache_entry": None,    # Windows Vista, 7, 8, 8v2, 8v3, 8_1, 10
                      "number_of_cache_entries": None}  # Windows Vista, 7, 8, 8v2

        entry = {"signature": None,
                 "cache_entry_size": None,
                 "entry_hash": None,
                 "filename_length": None,
                 "padding_size": None,
                 "data_size": None,
                 "width": None,
                 "height": None,
                 "unknown": None,
                 "data_checksum": None,
                 "header_checksum": None}

        db_header.update({"signature": check.convert_endian(file.read(4), 4,False, 's')})
        db_header.update({"version": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
        db_header.update({"type": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})

        if None in db_header.values():
            return None
        elif db_header.get("signature") != "CMMM":
            return None

        try:
            version = db_header.get("version")
            if version == self.window_version.get("Windows_7") or \
                version == self.window_version.get("Windows_8"):
                entry_info.update({"first_cache_entry": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                entry_info.update({"available_cache_entry": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                entry_info.update({"number_of_cache_entries": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})

            elif version == self.window_version.get("Windows_8v2"):
                file.seek(4, 1)
                entry_info.update({"first_cache_entry": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                entry_info.update({"available_cache_entry": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                entry_info.update({"number_of_cache_entries": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})

            elif version == self.window_version.get("Windows_8v3") or \
                version == self.window_version.get("Windows_8_1") or \
                version == self.window_version.get("Windows_10"):
                file.seek(4, 1)
                entry_info.update({"first_cache_entry": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                entry_info.update({"available_cache_entry": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})

            else:
                return None
        except:
            return None

        if list(entry_info.values()).count(None) >= 2 or \
                entry_info.get("first_cache_entry") == None:
            return None


        if version == self.window_version.get("Windows_8v2"):
            start_offset = 28
        else:
            start_offset = 24

        num = 0

        while True:

            try:
                file.seek(start_offset)
                entry.clear()

                if version == self.window_version.get("Windows_7"):
                    entry.update({"signature": check.convert_endian(file.read(4), 4, False, 's')})
                    entry.update({"entry_size": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    entry.update({"entry_hash": check.convert_endian(file.read(8), 8, True, 's')})
                    entry.update({"name_length": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    entry.update({"padding_size": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    entry.update({"data_size": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    file.seek(4, 1)
                    entry.update({"data_checksum": check.convert_endian(file.read(8), 8, True, 'x')})
                    entry.update({"header_checksum": check.convert_endian(file.read(8), 8, True, 'x')})

                elif version == self.window_version.get("Windows_8") or \
                    version == self.window_version.get("Windows_8v2") or \
                    version == self.window_version.get("Windows_8v3") or \
                    version == self.window_version.get("Windows_8_1") or \
                    version == self.window_version.get("Windows_10"):
                    entry.update({"signature": check.convert_endian(file.read(4), 4, False, 's')})
                    entry.update({"entry_size": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    entry.update({"entry_hash": check.convert_endian(file.read(8), 8, True, 'x')})
                    entry.update({"name_length": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    entry.update({"padding_size": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    entry.update({"data_size": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    entry.update({"width": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    entry.update({"height": int(check.convert_endian(file.read(4), 4, True, 'd'), 10)})
                    file.seek(4, 1)
                    entry.update({"data_checksum": check.convert_endian(file.read(8), 8, True, 'x')})
                    entry.update({"header_checksum": check.convert_endian(file.read(8), 8, True, 'x')})

                else:
                    break
            except Exception as e:
                break

            if entry.get("signature") != "CMMM":
                start_offset = check.find_signature(path, start_offset, 32768, b'CMMM')
                if start_offset != -1:
                    continue
                else:
                    break

            if int(entry.get("entry_hash"), 16) == 0:
                start_offset = file.tell()
                continue

            start_offset += entry.get("entry_size")

            try:
                file_name = check.convert_endian(file.read(entry.get("name_length")), entry.get("name_length"), False, 'unicode')
                file.seek(entry.get("padding_size"), 1)

                if entry.get("data_size") == 0:
                    continue
                else:
                    data = file.read(entry.get("data_size"))

                if check.check_signature(data, "bmp") == True:
                    file_name += ".bmp"
                elif check.check_signature(data, "jpg") == True:
                    file_name += ".jpg"
                elif check.check_signature(data, "png") == True:
                    file_name += ".png"

            except Exception as e:
                break

            num += 1

            cache_file = {"file_name": None,
                          "entry_hash": None,
                          "size": None,
                          "dimension": None,
                          "header_checksum": None,
                          "data_checksum": None,
                          "system": None,
                          "location": None}
            system_version = None
            cache_file.update({"file_name": file_name})
            cache_file.update({"entry_hash": entry.get("entry_hash")})
            cache_file.update({"size": entry.get("data_size")})
            cache_file.update({"dimension": "%sx%s" % (entry.get("width"), entry.get("height"))})
            cache_file.update({"header_checksum": entry.get("header_checksum")})
            cache_file.update({"data_checksum": entry.get("data_checksum")})

            if db_header.get("version") == 32:
                system_version = "Windows 10"
            elif db_header.get("version") == 31 or db_header.get("version") == 30 or db_header.get("version") == 28 or db_header.get("version") == 26:
                system_version = "Windows 8"
            elif db_header.get("version") == 21:
                system_version = "Windows 7"

            cache_file.update({"system": "%s" % system_version})
            cache_file.update({"location": "%s" % (path)})
            print({num:cache_file})

        file.close()











