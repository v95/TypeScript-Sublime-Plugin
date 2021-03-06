import collections

from . import json_helpers
from .node_client import CommClient
from .text_helpers import Location


class ServiceProxy:
    def __init__(self, comm=CommClient()):
        self.__comm = comm
        self.seq = 1

    def increase_seq(self):
        temp = self.seq
        self.seq += 1
        return temp

    def exit(self):
        req_dict = self.create_req_dict("exit")
        json_str = json_helpers.encode(req_dict)
        self.__comm.postCmd(json_str)

    def configure(self, host_info="Sublime Text", file=None, format_options=None):
        args = {"hostInfo": host_info, "formatOptions": format_options, "file": file}
        req_dict = self.create_req_dict("configure", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def change(self, path, begin_location=Location(1, 1), end_location=Location(1, 1), insertString=""):
        args = {
            "file": path,
            "line": begin_location.line,
            "offset": begin_location.offset,
            "endLine": end_location.line,
            "endOffset": end_location.offset,
            "insertString": insertString
        }
        req_dict = self.create_req_dict("change", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.postCmd(json_str)

    def completions(self, path, location=Location(1, 1), prefix="", on_completed=None):
        args = {"file": path, "line": location.line, "offset": location.offset, "prefix": prefix}
        req_dict = self.create_req_dict("completions", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.sendCmd(
            lambda json_dict: None if on_completed is None else on_completed(json_dict),
            json_str,
            req_dict["seq"]
        )

    def async_completions(self, path, location=Location(1, 1), prefix="", on_completed=None):
        args = {"file": path, "line": location.line, "offset": location.offset, "prefix": prefix}
        req_dict = self.create_req_dict("completions", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.sendCmdAsync(json_str, req_dict["seq"], on_completed)

    def signature_help(self, path, location=Location(1, 1), prefix="", on_completed=None):
        args = {"file": path, "line": location.line, "offset": location.offset, "prefix": prefix}
        req_dict = self.create_req_dict("signatureHelp", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.sendCmd(
            lambda response_dict: None if on_completed is None else on_completed(response_dict),
            json_str,
            req_dict["seq"]
        )

    def async_signature_help(self, path, location=Location(1, 1), prefix="", on_completed=None):
        args = {"file": path, "line": location.line, "offset": location.offset, "prefix": prefix}
        req_dict = self.create_req_dict("signatureHelp", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.sendCmdAsync(json_str, req_dict["seq"], on_completed)

    def definition(self, path, location=Location(1, 1)):
        args = {"file": path, "line": location.line, "offset": location.offset}
        req_dict = self.create_req_dict("definition", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def format(self, path, begin_location=Location(1, 1), end_location=Location(1, 1)):
        args = {
            "file": path,
            "line": begin_location.line,
            "offset": begin_location.offset,
            "endLine": end_location.line,
            "endOffset": end_location.offset
        }
        req_dict = self.create_req_dict("format", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def format_on_key(self, path, location=Location(1, 1), key=""):
        args = {"file": path, "line": location.line, "offset": location.offset, "key": key}
        req_dict = self.create_req_dict("formatonkey", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def open(self, path):
        args = {"file": path}
        req_dict = self.create_req_dict("open", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.postCmd(json_str)

    def close(self, path):
        args = {"file": path}
        req_dict = self.create_req_dict("close", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.postCmd(json_str)

    def references(self, path, location=Location(1, 1)):
        args = {"file": path, "line": location.line, "offset": location.offset}
        req_dict = self.create_req_dict("references", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def reload(self, path, alternate_path):
        args = {"file": path, "tmpfile": alternate_path}
        req_dict = self.create_req_dict("reload", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def reload_async(self, path, alternate_path, on_completed):
        args = {"file": path, "tmpfile": alternate_path}
        req_dict = self.create_req_dict("reload", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.sendCmdAsync(json_str, req_dict["seq"], on_completed)

    def rename(self, path, location=Location(1, 1)):
        args = {"file": path, "line": location.line, "offset": location.offset}
        req_dict = self.create_req_dict("rename", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def request_get_err(self, delay=0, pathList=[]):
        args = {"files": pathList, "delay": delay}
        req_dict = self.create_req_dict("geterr", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.postCmd(json_str)

    def type(self, path, location=Location(1, 1)):
        args = {"file": path, "line": location.line, "offset": location.offset}
        req_dict = self.create_req_dict("type", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def quick_info(self, path, location=Location(1, 1), onCompleted=None):
        args = {"file": path, "line": location.line, "offset": location.offset}
        req_dict = self.create_req_dict("quickinfo", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.sendCmd(
            lambda json_dict: None if onCompleted is None else onCompleted(json_dict),
            json_str,
            req_dict["seq"]
        )

    def get_event(self):
        event_json_str = self.__comm.getEvent()
        return json_helpers.decode(event_json_str) if event_json_str is not None else None

    def save_to(self, path, alternatePath):
        args = {"file": path, "tmpfile": alternatePath}
        req_dict = self.create_req_dict("saveto", args)
        json_str = json_helpers.encode(req_dict)
        self.__comm.postCmd(json_str)

    def nav_to(self, search_text, file_name):
        args = {"searchValue": search_text, "file": file_name, "maxResultCount": 20}
        req_dict = self.create_req_dict("navto", args)
        json_str = json_helpers.encode(req_dict)
        response_dict = self.__comm.sendCmdSync(json_str, req_dict["seq"])
        return response_dict

    def create_req_dict(self, command_name, args=None):
        req_dict = {
            "command": command_name,
            "seq": self.increase_seq(),
            "type": "request"
        }
        if args:
            req_dict["arguments"] = args
        return req_dict
