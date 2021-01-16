# -*- coding: utf-8 -*-
help_str = """
Builds statistics from vfr2pg.py log file.

Usage: build_statistics.py [log_file_name]
"""


def convert_file(file_name):
    FILE_PREFIX = "Processing "
    FILE_SUFFIX = "..."
    TIME_PREFIX = "Time elapsed: "

    in_file = open(file_name, "r")
    out_file_name = file_name[:file_name.rfind(".")] + ".csv"
    out_file = open(out_file_name, "w")
    try:
        out_file.write("#,Time [sec],File name\n")
        line_count = 0
        file_count = 0
        file_name = ""
        for line in in_file:
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            if line.startswith(FILE_PREFIX) and line.endswith(FILE_SUFFIX):
                file_count = file_count + 1
                line = line[len(FILE_PREFIX):]
                file_name = line[:line.find(" ")]
            elif line.startswith(TIME_PREFIX):
                timeSec = line[len(TIME_PREFIX):line.rfind(" ")]
                out_file.write("%d,%s,%s\n" % (file_count, timeSec, file_name))

            line_count = line_count + 1

        print line_count, " lines read."
    finally:
        in_file.close()
        out_file.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print help_str
    else:
        convert_file(sys.argv[1])
