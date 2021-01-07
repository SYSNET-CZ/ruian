# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        RUIANDownload
# Purpose:     Downloads VFR data from http://vdp.cuzk.cz/
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

import datetime
import os
import sys
import urllib2
import shared
from htmllog import html_log
from sharedtools import log, RUNS_ON_LINUX, extract_file_name, pathWithLastSlash, getFileExtension, safeMkDir, \
    RUIANDownloadConfig, RUIANDownloadInfoFile, getDataDirFullPath

__author__ = 'raugustyn'

help_str = """
Downloads VFR data from http://vdp.cuzk.cz/

Requires: Python 2.7.5 or later

Usage: download_ruian.py [-DownloadFullDatabase {True | False}] [-DataDir data_dir] [-UncompressDownloadedFiles {True | False}][-help]')

       -DownloadFullDatabase        Set to True to download whole RUIAN state data
       -DataDir                     Path to OSGeo4W.bat supproting VFR format, either relative or absolute
       -UncompressDownloadedFiles   Set to True to uncompress *.xml.gz to *.xml files after download
       -RunImporter                 Set to True to run RUIANImporter.bat after download
       -DownloadURLs                Semicolon separated URL masks for downloading state or update file list from VDP
       -IgnoreHistoricalData        Set to True to download only actual month
       -Help                        Print help
"""

shared.setupPaths()


# from sharedtools import pathWithLastSlash, RUIANDownloadConfig, RUIANDownloadInfoFile, safeMkDir, getFileExtension, extractFileName, getDataDirFullPath, RUNS_ON_LINUX

infoFile = None
config = None


def ___file_percentage_info(file_size, downloaded_size):
    status = r"%10d  [%3.2f%%]" % (downloaded_size, downloaded_size * 100. / file_size)
    log.logger.info(status)


file_percentage_info = ___file_percentage_info


def __file_download_info(file_name, file_size):
    print(file_name, file_size)
    pass


file_download_info = __file_download_info


class DownloadInfo:
    def __init__(self):
        self.file_name = ""
        self.file_size = 0
        self.compressed_file_size = 0
        self.download_time = 0


def clean_directory(folder):
    """ Cleans directory content including subdirectories.

    :param folder: Path to the folder to be cleaned.
    """
    assert isinstance(folder, basestring)

    if os.path.exists(folder):
        for the_file in os.listdir(folder):
            path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    clean_directory(path)
                    os.rmdir(path)

            except Exception, e:
                log.logger.error(e.message, str(e))


def get_file_content(file_name):
    assert isinstance(file_name, basestring)

    log.logger.debug("getFileContent")
    with open(file_name, "r") as f:
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
    assert isinstance(url, basestring)
    assert isinstance(date_str, basestring)

    url = url.replace("vf.cr=U&", "vf.cr=Z&")
    url = url.replace("vf.up=ST&", "")
    url = url.replace("vf.up=OB&", "")
    url = url.replace("vf.vu=Z&", "")
    url = url.replace("vf.uo=A&", "")
    url += "&vf.pd=" + date_str
    return url


class RUIANDownloader:
    def __init__(self, target_dir=""):
        assert isinstance(target_dir, basestring)

        self.data_dir = ""
        self._targetDir = ""
        self.assign_target_dir(target_dir)
        self.download_infos = []
        self.downloadInfo = None
        self._full_download = True
        self.page_urls = config.downloadURLs
        self.ignore_historical_data = config.ignoreHistoricalData

    @property
    def target(self):
        return self._targetDir

    @target.setter
    def target(self, target_dir):
        self.assign_target_dir(target_dir)

    def assign_target_dir(self, target_dir):
        """Assign value to the targetDir property. Creates this directory if not exists, including data sub directory.

        :param target_dir: Target directory path.
        """
        assert isinstance(target_dir, basestring)

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
        assert isinstance(urls, basestring)
        assert isinstance(is_patch_list, bool)

        urls = urls.split(";")
        result = []
        for url in urls:
            url = url.replace("vyhledej", "seznamlinku")
            log.logger.info("Downloading file list from " + url)
            content = urllib2.urlopen(url).read()
            lines = content.splitlines()
            result.extend(lines)

        if self.ignore_historical_data and not is_patch_list:
            newResult = []
            stateMonth = datetime.date.today().month - 1
            stateYear = datetime.date.today().year
            if stateMonth == 0:
                stateYear = stateYear - 1
                stateMonth = 12

            for url in result:
                date = url[url.rfind("/") + 1:]
                date = date[:date.find("_")]
                month = int(date[4:6])
                year = int(date[:4])
                if year == stateYear and month >= stateMonth:
                    newResult.append(url)
            result = newResult

        return result

    def get_update_list(self, from_date=""):
        assert isinstance(from_date, basestring)

        log.logger.debug("RUIANDownloader.getUpdateList since %s", infoFile.validFor())
        self._full_download = False
        if from_date == "" or infoFile.validFor() != "":
            v = infoFile.validFor()
            dateStr = v[8:10] + "." + v[5:7] + "." + v[0:4]
            firstPageURL = self.page_urls.split(";")[0]
            return self.get_list(get_update_url(firstPageURL, dateStr), True)
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
            html_log.addHeader(header_text + " " + v[8:10] + "." + v[5:7] + "." + v[0:4])

        def add_table_header():
            html_log.openTable()
            html_log.htmlCode += "<tr><th align='left' valign='bottom'>Soubor</th><th>Staženo<br>[Bajtů]</th>"
            if config.uncompressDownloadedFiles:
                html_log.htmlCode += "<th></th><th>Rozbaleno<br>[Bajtů]</th>"
            html_log.htmlCode += "<th valign='bottom'>Čas</th></tr>"

        def calc_sum_values():
            calc_info = DownloadInfo()
            calc_info.download_time = 0
            for info in self.download_infos:
                if info.download_time == "":
                    return
                elif info.file_name != "":
                    calc_info.file_size += info.file_size
                    calc_info.compressed_file_size += info.compressed_file_size
                    time = float(info.download_time[:len(info.download_time) - 1])
                    calc_info.download_time = calc_info.download_time + time
                else:
                    info.file_size = calc_info.file_size
                    info.compressed_file_size = calc_info.compressed_file_size
                    info.download_time = calc_info.download_time
                    return

            calc_info.download_time = str(calc_info.download_time) + "s"
            self.download_infos.append(calc_info)

        def int_to_str(int_value):
            if int == 0:
                return ""
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
                html_log.openTableRow(tags)

                add_col(extract_file_name(info.file_name))

                add_col(int_to_str(info.compressed_file_size), 'align="right"')

                if config.uncompressDownloadedFiles and info.file_size != 0:
                    add_col("->")
                else:
                    add_col("")

                if config.uncompressDownloadedFiles:
                    add_col(int_to_str(info.file_size), "align=right")

                add_col(info.download_time, "align=right")
                html_log.closeTableRow()
            html_log.closeTable()

        html_log.clear()
        add_download_header()
        add_table_header()
        calc_sum_values()
        add_table_content()
        html_log.save(config.dataDir + "Index.html")

    def download_url_list(self, url_list):

        def build_download_infos_list():
            self.download_infos = []
            for url_item in url_list:
                self.downloadInfo = DownloadInfo()
                self.downloadInfo.file_name = url_item.split('/')[-1]
                self.download_infos.append(self.downloadInfo)

        log.logger.debug("RUIANDownloader.downloadURLList")
        build_download_infos_list()
        index = 0
        for href in url_list:
            self.downloadInfo = self.download_infos[index]
            index = index + 1
            fileName = self.download_url_to_file(href, index, len(url_list))
            if config.uncompressDownloadedFiles:
                self.uncompress_file(fileName, not config.runImporter)

    def download_url_to_file(self, url, file_index, files_count):
        """ Downloads to temporary file. If suceeded, then rename result. """
        tmp_file_name = pathWithLastSlash(self.data_dir) + "tmpfile.bin"
        log.logger.debug("RUIANDownloader.downloadURLtoFile")
        file_name = self.data_dir + url.split('/')[-1]
        start_time = datetime.datetime.now()

        if os.path.exists(file_name):
            log.logger.info("File " + extract_file_name(file_name) + " is already downloaded, skipping it.")
            file_size = os.stat(file_name).st_size
            sys.stdout.write('.')

        else:
            req = urllib2.urlopen(url)
            meta = req.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            log.logger.info(
                "Downloading file %s [%d/%d %d Bytes]" % (
                    extract_file_name(file_name), file_index, files_count, file_size))
            file_download_info(file_name, file_size)
            CHUNK = 1024 * 1024
            file_size_dl = 0
            with open(tmp_file_name, 'wb') as fp:
                while True:
                    chunk = req.read(CHUNK)
                    if not chunk:
                        break
                    fp.write(chunk)
                    file_size_dl += len(chunk)
                    log.logger.info(r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100.0 / file_size))
                    self.downloadInfo.compressed_file_size = file_size_dl
                    # self.buildIndexHTML()
            fp.close()
            os.rename(tmp_file_name, file_name)
            sys.stdout.write('x')

        self.downloadInfo.download_time = format_time_delta(str(datetime.datetime.now() - start_time)[5:])
        self.downloadInfo.file_name = file_name
        self.downloadInfo.compressed_file_size = file_size
        return file_name

    def uncompress_file(self, file_name, delete_source=True):
        """
        Tato metoda rozbalí soubor s názvem fileName.

        @param file_name: Název souboru k dekompresi
        @param delete_source: Jestliže True, komprimovaný soubor bude vymazán.
        @return: Vrací název expandovaného souboru.
        """
        log.logger.debug("RUIANDownloader.uncompressFile")
        ext = getFileExtension(file_name).lower()
        if ext == ".gz":
            out_file_name = file_name[:-len(ext)]
            log.logger.info("Uncompressing " + extract_file_name(file_name) + " -> " + extract_file_name(out_file_name))
            import gzip

            bufferSize = 1024 * 1024 * 20
            size = 0
            with gzip.open(file_name, 'rb') as inputFile:
                with open(out_file_name, 'wb') as outputFile:
                    while True:
                        data = inputFile.read(bufferSize)
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

        if not infoFile.fullDownloadBroken:
            if was_it_today(infoFile.lastFullDownload):
                log.logger.warning(
                    "Process stopped! Nothing to download. Last full download was done Today " + infoFile.lastFullDownload)
                return
            elif not self._full_download and was_it_today(infoFile.lastPatchDownload):
                log.logger.warning(
                    "Process stopped! Nothing to download. Last patch was downloaded Today " + infoFile.lastPatchDownload)
                return

        # start_time = datetime.datetime.now()

        call_update = False
        if self._full_download or infoFile.lastFullDownload == "":
            log.logger.info("Running in full mode")
            if not infoFile.fullDownloadBroken:
                log.logger.info("Cleaning directory " + config.dataDir)
                clean_directory(config.dataDir)
                infoFile.fullDownloadBroken = True
                infoFile.save()

            safeMkDir(os.path.join(config.dataDir, "data"))
            safeMkDir(os.path.join(config.dataDir, "logs"))

            list1 = self.get_full_set_list()
            d = datetime.date.today()
            infoFile.lastFullDownload = '{:04d}'.format(d.year) + "-" + '{:02d}'.format(d.month) + "-01 14:07:13.084000"
            infoFile.lastPatchDownload = ""
            call_update = True

        else:
            log.logger.info("Running in update mode")
            list1 = self.get_update_list()
            infoFile.lastPatchDownload = str(datetime.datetime.now())

        self.build_index_html()

        if len(list1) > 0:  # stahujeme jedině když není seznam prázdný
            self.download_url_list(list1)
            infoFile.save()
            self.save_file_list(list1)
        else:
            log.logger.warning("Nothing to download, list is empty.")

        self.build_index_html()
        html_log.closeSection(config.dataDir + "Index.html")

        infoFile.fullDownloadBroken = False
        infoFile.save()

        if call_update:
            self._full_download = False
            self.download()

    def save_file_list(self, file_list):
        infoFile.numPatches = infoFile.numPatches + 1
        v = str(datetime.datetime.now())
        fileName = v[0:4] + "." + v[5:7] + "." + v[8:10] + ".txt"
        if self._full_download:
            fileName = "Download_" + fileName
        else:
            fileName = "Patch_" + fileName
        outFile = open(config.dataDir + fileName, "w")
        for line in file_list:
            outFile.write(line + "\n")
        outFile.close()

    def _download_url_to_file(self, url):
        log.logger.debug("RUIANDownloader._downloadURLtoFile")
        log.logger.info("Downloading " + url)
        file_name = url.split('/')[-1]
        log.logger.info(file_name)
        u = urllib2.urlopen(url)
        f = open(self.target + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        log.logger.info("Downloading %s Bytes: %s" % (file_name, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            blockBuffer = u.read(block_sz)
            if not blockBuffer:
                break

            file_size_dl += len(blockBuffer)
            f.write(blockBuffer)
            file_percentage_info(file_size, file_size_dl)
        f.close()


def print_usage_info():
    log.logger.info(help_str)
    sys.exit(1)


if __name__ == '__main__':
    config = RUIANDownloadConfig()
    config.loadFromCommandLine(sys.argv, help_str)

    log.createLogger(os.path.join(config.data_dir, "Download.log"))
    infoFile = RUIANDownloadInfoFile()

    #    if config.downloadFullDatabase:
    #        log.clearLogFile()

    log.logger.info("RUIAN Downloader")
    log.logger.info("#############################################")
    log.logger.info("Data directory : %s", config.data_dir)
    log.logger.info("Data directory full path : %s", getDataDirFullPath())
    log.logger.info("Download full database : %s", str(config.downloadFullDatabase))
    if not config.downloadFullDatabase:
        log.logger.info("Last full download  : %s", infoFile.lastFullDownload)
        log.logger.info("Last patch download : %s", infoFile.lastPatchDownload)
    log.logger.info("---------------------------------------------")

    downloader = RUIANDownloader(config.data_dir)
    downloader._full_download = config.downloadFullDatabase or infoFile.fullDownloadBroken
    downloader.download()

    log.logger.info("Download done.")
    if config.runImporter:
        log.logger.info("Executing importer.importruian.doImport().")
        from importer.import_ruian import doImport

        doImport(sys.argv)
        log.logger.info("Done - importer.import_ruian.doImport().")
