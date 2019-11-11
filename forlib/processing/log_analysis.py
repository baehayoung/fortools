import xmltodict
import json
import datetime
import re
import forlib.calc_hash as calc_hash


# analysis part for event file
class EventAnalysis:
    time_cnt = []

    def __init__(self, file, path, hash_v):
        self._result = []
        self.evtx_file = file
        self.evtx_json = self.__make_json()
        self.Favorite = Favorite(self.evtx_json)
        self.hash_value = [hash_v]
        self.path = path

    def show_all_record(self):
        for i in self.evtx_json:
            print(i)
            self._result.append(i)
        return self._result

    def __make_json(self):
        time_cnt = dict()
        json_list = []
        for i in range(0, len(self.evtx_file.records)):
            log_obj = dict()
            log_obj["number"] = i
            log_obj["eventID"] = self.evtx_file.records[i].get_event_identifier()
            log_obj["create Time"] = str(self.evtx_file.records[i].get_creation_time())
            date = log_obj["create Time"][:7]
            if time_cnt.get(date):
                time_cnt[date] = time_cnt[date] + 1
            else:
                time_cnt[date] = 1
            log_obj["level"] = self.evtx_file.records[i].get_event_level()
            log_obj["source"] = self.evtx_file.records[i].get_source_name()
            log_obj["computer Info"] = self.evtx_file.records[i].get_computer_name()
            log_obj["SID"] = self.evtx_file.records[i].get_user_security_identifier()
            json_list.append(log_obj)
        self.time_cnt = time_cnt
        return json_list

    def cal_hash(self):
        self.hash_value.append(calc_hash.get_hash(self.path))

    def get_hash(self):
        return self.hash_value

    def filter(self, filter_list):
        for i in range(0, len(self.evtx_json)):
            for j in range(0, len(filter_list), 3):
                if filter_list[j+2] == 0:  # normal
                    if self.evtx_json[i][filter_list[j]] == filter_list[j+1]:
                        pass
                    else:
                        break
                    '''
                    for k in filter_list[j + 1]:
                        if self.evtx_json[i][filter_list[j]] == k:
                            # if self.evtx_json[i][filter_list[j]] == filter_list[j+1]:
                            pass
                        else:
                            break
                            '''
                elif filter_list[j+2] == 1:  # re
                    result_re = re.search(filter_list[j + 1], str(self.evtx_json[i][filter_list[j]]))
                    if result_re is not None:
                        pass
                    else:
                        break
                if j == len(filter_list) - 3:
                    self._result.append(self.evtx_json[i])
                    print(self.evtx_json[i])
        return self._result

    def date_cnt(self):
        return self.time_cnt

    def get_string(self):
        json_list = []
        if self.evtx_file.number_of_records > 0:
            for i in range(0, len(self.evtx_file.records)):
                dict_type = xmltodict.parse(self.evtx_file.records[i].get_xml_string())
                json_type = json.dumps(dict_type)
                dict2_type = json.loads(json_type)
                try:
                    if dict2_type['Event']['EventData'] is not None:
                        log_obj = dict()
                        log_obj["number"] = i
                        log_obj["string"] = dict2_type['Event']['EventData']['Data']
                        json_list.append(log_obj)
                except Exception as e:
                    pass
                finally:
                    print(log_obj)
        return json_list

    def eventid(self, num):
        for i in range(0, len(self.evtx_json)):
            if self.evtx_json[i]['eventID'] == num:
                self._result.append(self.evtx_json[i])
                print(self.evtx_json[i])
        return self._result

    def level(self, num):
        for i in range(0, len(self.evtx_json)):
            if self.evtx_json[i]['level'] == num:
                print(self.evtx_json[i])
                self._result.append(self.evtx_json[i])
        return self._result

    def date(self, date1, date2):
        for i in range(0, len(self.evtx_json)):
            c_date = self.evtx_json[i]['create Time'].split('.')[0]
            if datetime.datetime.strptime(date1, "%Y-%m-%d") <= datetime.datetime.strptime(c_date, "%Y-%m-%d %H:%M:%S")\
                    <= datetime.datetime.strptime(date2, "%Y-%m-%d")+datetime.timedelta(1):
                print(self.evtx_json[i])
                self._result.append(self.evtx_json[i])
        return self._result

    def xml_with_num(self, num):
        print(self.evtx_file.records[num].get_xml_string())
        return self.evtx_file.records[num].get_xml_string()


# favorite method for evtx log
class Favorite:
    def __init__(self, json):
        self._result = []
        self.evtx_json = json
        self.AccountType = AccountType(self.evtx_json)

    # detect remote logon record
    def remote(self):
        EventAnalysis.eventid(self, 540)
        EventAnalysis.eventid(self, 4776)
        return self._result

    # app error(1000), app hang(1002)
    def app_crashes(self):
        EventAnalysis.eventid(self, 1000)
        EventAnalysis.eventid(self, 1002)
        return self._result

    # windows error reporting(1001)
    def error_report(self):
        EventAnalysis.eventid(self,1001)
        return self._result

    def service_fails(self):
        EventAnalysis.eventid(self, 7022)
        EventAnalysis.eventid(self, 7023)
        EventAnalysis.eventid(self, 7024)
        EventAnalysis.eventid(self, 7026)
        EventAnalysis.eventid(self, 7031)
        EventAnalysis.eventid(self, 7032)
        EventAnalysis.eventid(self, 7034)
        return self._result

    # rule add(2004), rule change(2005), rule deleted(2006, 2033), fail to load group policy(2009)
    def firewall(self):
        EventAnalysis.eventid(self, 2004)
        EventAnalysis.eventid(self, 2005)
        EventAnalysis.eventid(self, 2006)
        EventAnalysis.eventid(self, 2009)
        EventAnalysis.eventid(self, 2033)
        return self._result

    # new device(43), new mass storage installation(400, 410)
    def usb(self):
        EventAnalysis.eventid(self, 43)
        EventAnalysis.eventid(self, 400)
        EventAnalysis.eventid(self, 410)
        return self._result

    # starting a wireless connection(8000, 8011), successfully connected(8001), disconnect(8003), failed(8002)
    def wireless(self):
        EventAnalysis.eventid(self, 8000)
        EventAnalysis.eventid(self, 8001)
        EventAnalysis.eventid(self, 8002)
        EventAnalysis.eventid(self, 8003)
        EventAnalysis.eventid(self, 8011)
        EventAnalysis.eventid(self, 10000)
        EventAnalysis.eventid(self, 10001)
        EventAnalysis.eventid(self, 11000)
        EventAnalysis.eventid(self, 11001)
        EventAnalysis.eventid(self, 11002)
        EventAnalysis.eventid(self, 11004)
        EventAnalysis.eventid(self, 11005)
        EventAnalysis.eventid(self, 11006)
        EventAnalysis.eventid(self, 11010)
        EventAnalysis.eventid(self, 12011)
        EventAnalysis.eventid(self, 12012)
        EventAnalysis.eventid(self, 12013)
        return self._result


# filtering based on logon type
class AccountType:
    def __init__(self, evtx_json):
        self.evtx_json = evtx_json
        self._result = []

    # detect valid logon record
    def logon(self):
        EventAnalysis.eventid(self, 4624)
        return self._result

    # detect failed user account login
    def login_failed(self):
        EventAnalysis.eventid(self, 4625)
        return self._result

    def change_pwd(self):
        EventAnalysis.eventid(self, 4723)
        return self._result

    def delete_account(self):
        EventAnalysis.eventid(self, 4726)
        return self._result

    def verify_account(self):
        EventAnalysis.eventid(self, 4720)
        return self._result

    def add_privileged_group(self):
        EventAnalysis.eventid(self, 4728)
        EventAnalysis.eventid(self, 4732)
        EventAnalysis.eventid(self, 4756)
        return self._result


# analysis for LinuxLog
class LinuxLogAnalysis:
    class AuthLog:
        def __init__(self, file):
            self.file = file
            self.__parse()

        def __parse(self):
            log_parse(self.file)

    class SysLog:
        def __init__(self, file):
            self.file = file
            self.__parse()

        def __parse(self):
            log_parse(self.file)


class ApacheLog:
    class Error:
        def __init__(self, file):
            self.file = file
            self.json = err_parse(self.file)

        def show_info(self):
            for i in range(0, len(self.json)):
                print(self.json[i])

        def date(self, date):
            for i in range(1, len(self.json)):
                if self.json[i]["date"] == date:
                    print(self.json[i])

        def pid(self, pid):
            for i in range(1, len(self.json)):
                if self.json[i]["pid"] == pid:
                    print(self.json[i])

    class Access:
        def __init__(self, file):
            self.file = file
            self.json = access_parse(self.file)

        def show_info(self):
            for i in range(0, len(self.json)):
                print(self.json[i])

        def date(self, date):
            for i in range(1, len(self.json)):
                if self.json[i]["date"] == date:
                    print(self.json[i])

        def ip(self, ip):
            for i in range(1, len(self.json)):
                if self.json[i]["ip"] == ip:
                    print(self.json[i])

        def method(self, method):
            for i in range(1, len(self.json)):
                if self.json[i]["method"] == method:
                    print(self.json[i])

        def respond(self, respond):
            for i in range(1, len(self.json)):
                if int(self.json[i]["respond code"]) == respond:
                    print(self.json[i])


class IIS:
    def __init__(self, file):
        self.file = file
        self.json = iis_parse(self.file)

    def show_info(self):
        for i in self.json:
            print(i)

    def date(self, date):
        for i in range(0, len(self.json)):
            if self.json[i]['no' + str(i)]['date'] == date:
                print(self.json[i])

    def cs_method(self, method):
        for i in range(0, len(self.json)):
            if self.json[i]['no' + str(i)]['cs-method'] == method:
                print(self.json[i])

    def s_port(self, port):
        for i in range(0, len(self.json)):
            if self.json[i]['no' + str(i)]['s-port'] == port:
                print(self.json[i])

    def sc_status(self, status):
        for i in range(0, len(self.json)):
            if self.json[i]['no' + str(i)]['sc-status'] == status:
                print(self.json[i])


def iis_parse(file):
    json_list = []
    fields = None
    while True:
        line = file.readline()
        if line == '':
            break
        elif line[0] == '#' and line[0:7] != '#Fields':
            continue
        if line[0:7] == '#Fields':
            fields = line.split(' ')
            continue
        try:
            log_line = line.split()
            log_obj = dict()
            for i in range(1, len(log_line) - 1):
                log_obj[fields[i]] = log_line[i - 1]
        except:
            print('IIS Log Err, plz check format of file.')
        json_list.append(log_obj)
    return json_list


def err_parse(file):
    date_r = r'\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2}.\d+ \d{4}'
    pid = r'pid +\d+'
    tid = r'tid \d+'
    info = r'AH\d+:.+'
    json_list = []
    while True:
        line = file.readline()
        if line == '':
            break
        try:
            log_obj = dict()
            date = datetime.datetime.strptime(str(re.search(date_r, line).group()), "%a %b %d %H:%M:%S.%f %Y")
            log_obj["date"] = date.strftime('%m/%d')
            log_obj["time"] = date.strftime('%H:%M:%S')
            log_obj["pid"] = re.search(pid, line).group()[4:]
            log_obj["tid"] = re.search(tid, line).group()[4:]
            log_obj["info"] = re.search(info, line).group()
        except:
            continue
        json_list.append(log_obj)
    return json_list


def access_parse(file):
    ip = r'(\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3})|(::1)'
    date_r = r'\d{1,2}/\w{1,3}/\d{1,4}:\d{2}:\d{2}:\d{2} [+]\d{4}'
    method = r'GET|PUSH|PUT|POST|HEAD|OPTIONS|Head|T'
    respond = r' \d{3} '
    uri = r'( /+\S+)|( \*)'
    url = r'(http|https)://\S+'

    json_list = []
    while True:
        line = file.readline()
        if line == '':
            break
        log_obj = dict()
        try:
            log_obj["ip"] = re.search(ip, line).group()
            date = re.search(date_r, line).group()
            date = datetime.datetime.strptime(date, '%d/%b/%Y:%H:%M:%S %z')
            log_obj["date"] = str(date.strftime('%Y/%m/%d'))
            log_obj["time"] = str(date.strftime('%H:%M:%S'))
            log_obj["method"] = re.search(method, line).group()
            log_obj["respond code"] = re.search(respond, line).group()[1:-1]
        except:
            continue
        try:
            log_obj["uri"] = re.search(uri, line).group()[1:]
        except:
            log_obj["uri"] = 'none'
        try:
            log_obj["url"] = re.search(url, line).group()
        except:
            log_obj["url"] = 'none'
        json_list.append(log_obj)
    return json_list


def log_parse(file):
    while True:
        line = file.readline()
        if line == '':
            break
        line_parse = line.split(' ')
        log_obj = dict()
        info = ''
        date = datetime.datetime.strptime(line_parse[0] + line_parse[1] + line_parse[2], "%b%d%H:%M:%S")
        log_obj["date"] = date.strftime('%m/%d')
        log_obj["time"] = date.strftime('%H:%M:%S')
        log_obj["system"] = line_parse[3]
        log_obj["source"] = line_parse[4][:-1]
        for i in range(5, len(line_parse)):
            info = info + line_parse[i] + ' '
        log_obj["info"] = info
        print(log_obj)
    return log_obj
