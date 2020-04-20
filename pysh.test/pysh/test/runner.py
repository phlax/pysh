#!/usr/bin/env python

import os
import subprocess
import sys
import time

import termcolor


COLORS = (
    ("DEFAULT",
     dict()),
    ("PAGE_TITLE",
     dict(color="white", bg_color="grey")),
    ("SHEBANG",
     dict(color="blue")),
   ("PREFIX",
     dict(color="yellow", bg_color="grey", attrs=["bold"])),
    ("COMMENT",
     dict(attrs=["concealed"])),
    ("HEADING",
     dict(color="cyan", attrs=["bold"])),
    ("SECTION_HEADING",
     dict(color="cyan", attrs=["dark", "bold"])),
    ("FAIL",
     dict(color="white", bg_color="red", attrs=["bold"])),
    ("FAIL_TEXT",
     dict(color="white", bg_color="red")),
    ("ERROR_SUMMARY",
     dict(color="white", bg_color="red", attrs=["reverse"])),
    ("SUCCESS_SUMMARY",
     dict(color="green", bg_color="white")),
)


class PyshRunner(object):
    prev = None
    last = None
    in_wrapper = False
    failing = False
    lines = 0

    def __init__(self):
        self.start = time.time()
        self.last = self.start
        self.colors = dict(COLORS)
        self.errors = []

    def prefix(self, time_taken, line):
        if time_taken < .001:
            time_taken = ""
        else:
            time_taken = "%ss:" % time_taken
        time_taken='{0:>10}'.format(*[time_taken])
        formatter = self.colors.get("PREFIX")
        if formatter:
            color = formatter.get("color")
            bg_color = (
                "on_%s" % formatter["bg_color"]
                if formatter.get("bg_color")
                else None)
            attrs = formatter.get("attrs")
            time_taken = termcolor.colored(
                time_taken, color, bg_color, attrs=attrs)
        return "%s " % time_taken

    def format_line(self, time_taken, line):
        color = None
        bg_color = None
        attrs=[]
        formatter = None
        if self.failing:
            if line.startswith(" "):
                formatter = self.colors["FAIL_TEXT"]
                self.error["lines"].append(line)
            else:
                self.failing = False
        elif line.startswith("FAIL"):
            formatter = self.colors["FAIL"]
            self.error = dict(lines=[])
            self.errors.append(self.error)
            self.failing = True
        if not self.failing:
            if line.startswith("RUNNING"):
                formatter = self.colors["PAGE_TITLE"]
            elif line.startswith("#!"):
                formatter = self.colors["SHEBANG"]
            elif line.startswith("# "):
                formatter = self.colors["COMMENT"]
            elif line.startswith("## "):
                formatter = self.colors["HEADING"]
            elif line.startswith("### "):
                formatter = self.colors["SECTION_HEADING"]
            else:
                formatter = self.colors["DEFAULT"]
        if formatter:
            color = formatter.get("color")
            bg_color = (
                "on_%s" % formatter["bg_color"]
                if formatter.get("bg_color")
                else None)
            attrs = formatter.get("attrs", [])
        if not self.failing and time_taken > .001:
            attrs = []
            attrs.append("bold")
            attrs.append("dark")
        return termcolor.colored(self.prev, color, bg_color, attrs=attrs)

    def handle_line(self, line=None):
        tstamp = time.time()
        time_taken = round(tstamp - self.last, 4)
        if self.in_wrapper:
            if (line or "").rstrip().endswith("}"):
                self.in_wrapper = False
                line = ""
        elif self.prev is not None:
            print(
                "%s%s"
                % (self.prefix(time_taken, self.prev),
                   self.format_line(time_taken, self.prev)),
                end='\n')
        self.prev = (line or "").rstrip()
        self.last = tstamp

    def _run(self, cmd):
        self.handle_line("RUNNING: %s" % (" ".join(cmd[1:])))
        self.handle_line("")
        self.in_wrapper = True
        self.proc = subprocess.Popen(
            cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            universal_newlines = True)
        while self.proc.poll() is None:
            self.handle_line(self.proc.stdout.readline())
        # flush
        self.handle_line()
        return self.proc.returncode

    def get_command(self, command):
        wrapper = os.path.join(os.path.dirname(__file__), "wrapper.sh")
        return [wrapper, command]

    def run(self, command):
        code = self._run(self.get_command(command))
        time_taken = round(time.time() - self.start, 4)
        formatter = self.colors["ERROR_SUMMARY"]
        if not self.errors:
            formatter = self.colors["SUCCESS_SUMMARY"]
            return
        color = formatter.get("color")
        bg_color = (
            "on_%s" % formatter["bg_color"]
            if formatter.get("bg_color")
            else None)
        attrs = formatter.get("attrs")
        if not self.errors:
            message = '{0:<80}'.format(*["SUCCESS: All tests completed successfully"])
            print(
                termcolor.colored(
                    message,
                    color,
                    bg_color,
                    attrs=attrs))
            return
        for error in self.errors:
            message = '{0:<80}'.format(*["ERROR: %s" % error["lines"][0].strip()])
            print(
                termcolor.colored(
                    message,
                    color,
                    bg_color,
                    attrs=attrs))
        message = '{0:<80}'.format(*["FAILED: (%s) tests failed in %ss" % (len(self.errors), time_taken)])
        attrs = attrs and attrs.append("bold") or ["bold"]
        print(
            termcolor.colored(
                message,
                color,
                bg_color,
                attrs=attrs))
        raise SystemExit(1)
