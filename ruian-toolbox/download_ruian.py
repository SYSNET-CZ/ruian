# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        RUIANDownload
# Purpose:     Downloads VFR data from http://vdp.cuzk.cz/
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# Contributor: Radim Jäger, 2021. Consolidated for Python 3
# -------------------------------------------------------------------------------

import datetime
import os
import sys
import socket
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from downloader.html_log import html_log
from shared_tools import log, RUNS_ON_LINUX, extract_file_name2, path_with_last_slash, get_file_extension, \
    safe_mk_dir, ruian_download_config, ruian_download_info_file, get_data_dir_full_path, Configuration, shared

__author__ = 'raugustyn'

help_str = """
Downloads VFR data from https://vdp.cuzk.cz/

Requires: Python 3.8 or later

Usage: download_ruian.py [-DownloadFullDatabase {True | False}] [-DataDir data_dir] [-UncompressDownloadedFiles 
{True | False}][-help]')

       -DownloadFullDatabase        Set to True to download whole RUIAN state data
       -DataDir                     Path to OSGeo4W.bat supporting VFR format, either relative or absolute
       -UncompressDownloadedFiles   Set to True to uncompress *.xml.gz to *.xml files after download
       -RunImporter                 Set to True to run RUIANImporter.bat after download
       -DownloadURLs                Semicolon separated URL masks for downloading state or update file list from VDP
       -IgnoreHistoricalData        Set to True to download only actual month
       -Help                        Print help
"""

shared.setup_paths()
# info_file = None
config = Configuration()  # type: Configuration


def ___file_percentage_info(file_size, downloaded_size):
    status = r'%10d  [%3.2f%%]' % (downloaded_size, downloaded_size * 100. / file_size)
    log.logger.info(status)


file_percentage_info = ___file_percentage_info


def __file_download_info(file_name, file_size):
    print(file_name, file_size)
    pass


file_download_info = __file_download_info


class DownloadInfo:
    def __init__(self):
        self.file_name = ''
        self.file_size = 0
        self.compressed_file_size = 0
        self.download_time = 0


def clean_directory(folder):
    """ Cleans directory content including subdirectories.

    :param folder: Path to the folder to be cleaned.
    """
    assert isinstance(folder, (str, bytes))

    if os.path.exists(folder):
        for the_file in os.listdir(folder):
            path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    clean_directory(path)
                    os.rmdir(path)

            except Exception as e:
                log.logger.error(str(e))


def get_file_content(file_name):
    assert isinstance(file_name, (str, bytes))

    log.logger.debug('getFileContent')
    with open(file_name, 'r') as f:
        lines = f.read().splitlines()
        f.close()
    return lines


def format_time_delta(time_delta):
    v = str(time_delta)
    v = v.strip("0")
    if v[0:1] == ".":
        v = "0" + v
    if v == "":
        v = "0"
    return v + "s"


def get_update_url(url, date_str):
    assert isinstance(url, (str, bytes))
    assert isinstance(date_str, (str, bytes))

    url = url.replace("vf.cr=U&", "vf.cr=Z&")
    url = url.replace("vf.up=ST&", "")
    url = url.replace("vf.up=OB&", "")
    url = url.replace("vf.vu=Z&", "")
    url = url.replace("vf.uo=A&", "")
    url += "&vf.pd=" + date_str
    return url


class RUIANDownloader:
    def __init__(self, target_dir=""):
        assert isinstance(target_dir, (str, bytes))

        self.data_dir = ""
        self._targetDir = ""
        self.assign_target_dir(target_dir)
        self.download_infos = []
        self.downloadInfo = None
        self._full_download = True
        self.page_urls = config.downloadURLs
        self.ignore_historical_data = config.ignoreHistoricalData
        self.info_file = ruian_download_info_file()

    @property
    def target(self):
        return self._targetDir

    @target.setter
    def target(self, target_dir):
        self.assign_target_dir(target_dir)

    def get_info_file(self):
        return self.info_file

    def assign_target_dir(self, target_dir):
        """Assign value to the targetDir property. Creates this directory if not exists, including data sub directory.

        :param target_dir: Target directory path.
        """
        assert isinstance(target_dir, (str, bytes))

        if target_dir != "":
            target_dir = os.path.normpath(target_dir)
            if target_dir.rfind(os.sep) != len(target_dir) - 1:
                target_dir += os.sep
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

        self.data_dir = target_dir
        if RUNS_ON_LINUX:
            self.data_dir += "data/"
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)

        self._targetDir = target_dir

    def get_full_set_list(self):
        log.logger.debug("RUIANDownloader.getFullSetList")
        self._full_download = True
        return self.get_list(self.page_urls, False)

    def get_list(self, urls, is_patch_list):
        assert isinstance(urls, (str, bytes))
        assert isinstance(is_patch_list, bool)

        urls = urls.split(';')
        result = []
        for url in urls:
            url = url.replace("vyhledej", "seznamlinku")
            log.logger.info("Downloading file list from " + url)
            content = urlopen(url).read()
            lines = content.splitlines()
            result.extend(lines)

        if self.ignore_historical_data and not is_patch_list:
            new_result = []
            state_month = datetime.date.today().month - 1
            state_year = datetime.date.today().year
            if state_month == 0:
                state_year = state_year - 1
                state_month = 12

            for url in result:
                if isinstance(url, bytes):
                    # print(str(url))
                    date = url[url.rfind(b'/') + 1:]
                    date = date[:date.find(b'_')]
                    month = int(date[4:6])
                    year = int(date[:4])
                    if year == state_year and month >= state_month:
                        new_result.append(url)
                    print(".", end="")
            result = new_result
            print(".")
            print("GET LIST FINISHED")
        return result

    def get_update_list(self, from_date=""):
        assert isinstance(from_date, (str, bytes))

        log.logger.debug("RUIANDownloader.getUpdateList since %s", self.info_file.valid_for())
        self._full_download = False
        if from_date == "" or self.info_file.valid_for() != "":
            v = self.info_file.valid_for()
            date_str = v[8:10] + "." + v[5:7] + "." + v[0:4]
            first_page_url = self.page_urls.split(";")[0]
            return self.get_list(get_update_url(first_page_url, date_str), True)
        else:
            return []

    def build_index_html(self):
        def add_col(value, tags=""):
            html_log.add_col(value, tags)

        def add_download_header():
            if self._full_download:
                header_text = "Stažení stavových dat"
            else:
                header_text = "Stažení aktualizací k "
            v = str(datetime.datetime.now())
            html_log.add_header(header_text + " " + v[8:10] + "." + v[5:7] + "." + v[0:4])

        def add_table_header():
            html_log.open_table()
            html_log.htmlCode += '<tr><th align="left" valign="bottom">Soubor</th><th>Staženo<br>[Bajtů]</th>'
            if config.uncompressDownloadedFiles:
                html_log.htmlCode += '<th></th><th>Rozbaleno<br>[Bajtů]</th>'
            html_log.htmlCode += '<th valign="bottom">Čas</th></tr>'

        def calc_sum_values():
            calc_info = DownloadInfo()
            calc_info.download_time = 0
            for info in self.download_infos:
                if info.download_time == '':
                    return
                elif info.file_name != '':
                    calc_info.file_size += info.file_size
                    calc_info.compressed_file_size += info.compressed_file_size
                    time = float(info.download_time[:len(info.download_time) - 1])
                    calc_info.download_time = calc_info.download_time + time
                else:
                    info.file_size = calc_info.file_size
                    info.compressed_file_size = calc_info.compressed_file_size
                    info.download_time = calc_info.download_time
                    return

            calc_info.download_time = str(calc_info.download_time) + 's'
            self.download_infos.append(calc_info)

        def int_to_str(int_value):
            if int == 0:
                return ''
            else:
                return str(int_value)

        def add_table_content():
            alt_color = True
            for info in self.download_infos:
                if alt_color:
                    tags = 'class="altColor"'
                else:
                    tags = ''
                alt_color = not alt_color
                html_log.open_table_row(tags)
                add_col(extract_file_name2(info.file_name))
                add_col(int_to_str(info.compressed_file_size), 'align="right"')
                if config.uncompressDownloadedFiles and info.file_size != 0:
                    add_col('->')
                else:
                    add_col('')
                if config.uncompressDownloadedFiles:
                    add_col(int_to_str(info.file_size), 'align="right"')
                add_col(info.download_time, 'align="right"')
                html_log.close_table_row()
            html_log.close_table()

        html_log.clear()
        add_download_header()
        add_table_header()
        calc_sum_values()
        add_table_content()
        html_log.save(config.dataDir + 'Index.html')

    def download_url_list(self, url_list):  # stahuje soubory  podle seznamu
        def build_download_infos_list():  # sestaví seznam ke stažení
            self.download_infos = []
            for url_item in url_list:
                if isinstance(url_item, bytes):
                    self.downloadInfo = DownloadInfo()
                    self.downloadInfo.file_name = url_item.split(b'/')[-1]
                    self.download_infos.append(self.downloadInfo)
                print('.', end='')
            print('.')
            print('build_download_infos_list FINISHED')

        log.logger.debug('RUIANDownloader.downloadURLList')
        build_download_infos_list()
        index = 0
        for href in url_list:
            self.downloadInfo = self.download_infos[index]
            index += 1
            file_name = self.download_url_to_file(href, index, len(url_list))
            if config.uncompressDownloadedFiles:
                self.uncompress_file(file_name, not config.runImporter)
            print('.', end='')
        print('.')
        print('download_url_list FINISHED')

    def download_url_to_file(self, url, file_index, files_count):
        """ Downloads to temporary file. If succeeded, then rename result. """
        try:
            tmp_file_name = os.path.join(self.data_dir, 'tmpfile.bin')
            log.logger.info('download_ruian.download_url_to_file - data_dir: {}'.format(self.data_dir))
            file_name = os.path.join(self.data_dir, str(url).split('/')[-1])
            file_name = consolidate_download_file_name(file_name)       # má odstranit apostrof na konci. Kde se vzal?
            start_time = datetime.datetime.now()

            if os.path.exists(file_name):
                log.logger.info('File ' + extract_file_name2(file_name) + " is already downloaded, skipping it.")
                file_size = os.stat(file_name).st_size
                # sys.stdout.write('downloader')
            else:
                if isinstance(url, bytes):
                    url = url.decode('utf-8')
                log.logger.debug('URL: {}'.format(url))
                req = urlopen(url=url, timeout=60)
                file_size = int(req.getheader("Content-Length"))
                log.logger.info(
                    "Downloading file %s [%d/%d %d Bytes]" % (
                        extract_file_name2(file_name), file_index, files_count, file_size))
                file_download_info(file_name, file_size)
                chunk = 1024 * 1024
                file_size_dl = 0
                with open(tmp_file_name, 'wb') as fp:
                    while True:
                        chunk = req.read(chunk)
                        if not chunk:
                            break
                        fp.write(chunk)
                        file_size_dl += len(chunk)
                        log.logger.info(r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100.0 / file_size))
                        self.downloadInfo.compressed_file_size = file_size_dl
                fp.close()
                os.rename(tmp_file_name, file_name)
                sys.stdout.write('x')
            self.downloadInfo.download_time = format_time_delta(str(datetime.datetime.now() - start_time)[5:])
            self.downloadInfo.file_name = file_name
            self.downloadInfo.compressed_file_size = file_size
            return file_name
        except HTTPError as error:
            log.logger.error('Data not retrieved because {0}\nURL: {1}'.format(error, url))
            return None

        except URLError as error:
            if isinstance(error.reason, socket.timeout):
                log.logger.error('Socket timed out - URL %s', url)
            else:
                log.logger.error('Some other error happened {}'.format(str(error)))
            return None

    def uncompress_file(self, file_name, delete_source=True):
        """
        Tato metoda rozbalí soubor s názvem fileName.

        @param file_name: Název souboru k dekompresi
        @param delete_source: Jestliže True, komprimovaný soubor bude vymazán.
        @return: Vrací název expandovaného souboru.
        """
        log.logger.debug("RUIANDownloader.uncompressFile")
        ext = get_file_extension(file_name).lower()
        if ext == ".gz":
            out_file_name = file_name[:-len(ext)]
            log.logger.info(
                "Uncompressing " + extract_file_name2(file_name) + " -> " + extract_file_name2(out_file_name))
            import gzip

            buffer_size = 1024 * 1024 * 20
            size = 0
            with gzip.open(file_name, 'rb') as inputFile:
                with open(out_file_name, 'wb') as outputFile:
                    while True:
                        data = inputFile.read(buffer_size)
                        size = size + len(data)
                        if len(data) == 0:
                            break
                        outputFile.write(data)
                        outputFile.flush()
                    outputFile.close()
                inputFile.close()

            self.downloadInfo.file_size = os.path.getsize(out_file_name)
            if delete_source:
                os.remove(file_name)
            return out_file_name
        else:
            return file_name

    def download(self):
        def was_it_today(date_time_str):
            if date_time_str == "":
                return False
            else:
                return str(datetime.datetime.now().date()) == date_time_str.split(" ")[0]

        if not self.info_file.fullDownloadBroken:
            if was_it_today(self.info_file.lastFullDownload):
                log.logger.warning(
                    "Process stopped! Nothing to download. Last full download was done Today " +
                    self.info_file.lastFullDownload)
                return
            elif not self._full_download and was_it_today(self.info_file.lastPatchDownload):
                log.logger.warning(
                    "Process stopped! Nothing to download. Last patch was downloaded Today " +
                    self.info_file.lastPatchDownload)
                return

        # start_time = datetime.datetime.now()

        call_update = False
        if self._full_download or self.info_file.lastFullDownload == "":
            log.logger.info("Running in full mode")
            if not self.info_file.fullDownloadBroken:
                log.logger.info("Cleaning directory " + config.dataDir)
                clean_directory(config.dataDir)
                self.info_file.fullDownloadBroken = True
                self.info_file.save()

            safe_mk_dir(os.path.join(config.dataDir, "data"))
            safe_mk_dir(os.path.join(config.dataDir, "logs"))

            list1 = self.get_full_set_list()
            d = datetime.date.today()
            self.info_file.lastFullDownload = '{:04d}'.format(d.year) + "-" + '{:02d}'.format(
                d.month) + "-01 14:07:13.084000"
            self.info_file.lastPatchDownload = ""
            call_update = True

        else:
            log.logger.info("Running in update mode")
            list1 = self.get_update_list()
            self.info_file.lastPatchDownload = str(datetime.datetime.now())

        self.build_index_html()

        if len(list1) > 0:  # stahujeme jedině, když není seznam prázdný
            self.download_url_list(list1)
            self.info_file.save()
            self.save_file_list(list1)
        else:
            log.logger.warning("Nothing to download, list is empty.")

        self.build_index_html()
        html_log.close_section(config.dataDir + "Index.html")

        self.info_file.fullDownloadBroken = False
        self.info_file.save()

        if call_update:
            self._full_download = False
            self.download()

    def save_file_list(self, file_list):
        self.info_file.numPatches = self.info_file.numPatches + 1
        v = str(datetime.datetime.now())
        file_name = v[0:4] + "." + v[5:7] + "." + v[8:10] + ".txt"
        if self._full_download:
            file_name = "Download_" + file_name
        else:
            file_name = "Patch_" + file_name
        out_file = open(config.dataDir + file_name, "w")
        for line in file_list:
            out_file.write(line.decode("utf-8") + "\n")
            log.logger.info("save_file_list: {}".format(line.decode("utf-8")))
        out_file.close()

    def _download_url_to_file(self, url):
        log.logger.debug("RUIANDownloader._downloadURLtoFile")
        log.logger.info("Downloading " + url)
        file_name = url.split('/')[-1]
        log.logger.info(file_name)
        u = urlopen(url)
        f = open(self.target + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        log.logger.info("Downloading %s Bytes: %s" % (file_name, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            block_buffer = u.read(block_sz)
            if not block_buffer:
                break

            file_size_dl += len(block_buffer)
            f.write(block_buffer)
            file_percentage_info(file_size, file_size_dl)
        f.close()


def consolidate_download_file_name(file_name):
    if file_name is None:
        return None
    if file_name == '':
        return file_name
    if file_name.endswith("'"):
        return file_name[:-1]
    return file_name


def consolidate_download_names():
    d = config.dataDir
    ld = os.listdir(d)
    out = False
    if ld is None:
        return out
    if not ld:
        return out
    for file_name in ld:
        if file_name.endswith("'"):
            old_name = os.path.join(d, file_name)
            new_name = old_name[:-1]
            os.rename(old_name, new_name)
            out = True
    return out


def print_usage_info():
    log.logger.info(help_str)
    sys.exit(1)


def main(argv):
    global config
    config = ruian_download_config()
    config.load_from_command_line(argv, help_str)
    log.create_logger(os.path.join(config.dataDir, "Download.log"))
    # info_file = ruian_download_info_file()
    downloader = RUIANDownloader(config.dataDir)

    log.logger.info("RUIAN Downloader")
    log.logger.info("#############################################")
    log.logger.info("Data directory : %s", config.dataDir)
    log.logger.info("Data directory full path : %s", get_data_dir_full_path())
    log.logger.info("Download full database : %s", str(config.downloadFullDatabase))
    if not config.downloadFullDatabase:
        log.logger.info("Last full download  : %s", downloader.get_info_file().lastFullDownload)
        log.logger.info("Last patch download : %s", downloader.get_info_file().lastPatchDownload)
    log.logger.info("---------------------------------------------")

    # downloader = RUIANDownloader(config.dataDir)
    downloader._full_download = config.downloadFullDatabase or downloader.get_info_file().fullDownloadBroken
    downloader.download()  # !!! toto je výkonný příkaz !!!

    log.logger.info("Download done.")
    if config.runImporter:
        log.logger.info("Executing importer.import_ruian.doImport().")
        from import_ruian import do_import

        do_import(argv)
        log.logger.info("Done - importer.import_ruian.doImport().")

    pass


if __name__ == '__main__':
    main(sys.argv)
