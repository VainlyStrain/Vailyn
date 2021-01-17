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
import treelib
import argparse
import requests
import sys
import random
import string
import colorama
import datetime
import time
import os

import core.variables as variables

from itertools import permutations

from math import factorial

from multiprocessing.pool import ThreadPool as Pool

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import (
    QTreeWidgetItem,
    QTableWidgetItem,
    QFileDialog,
)
from scrapy.crawler import CrawlerRunner, CrawlerProcess

from twisted.internet import reactor

from multiprocessing import Process, Queue

from terminaltables import SingleTable

from core.colors import color
from core.config import DESKTOP_NOTIFY
from core.variables import (
    payloadlist,
    nullchars,
    version,
    processes,
    cachedir,
    rce,
    is_windows,
)

from core.methods.parser import build_parser
from core.methods.list import (
    listsplit,
    listperm,
    gensplit,
    filegen,
)
from core.methods.select import select, select_techniques
from core.methods.tree import create_tree
from core.methods.attack import (
    phase1, phase2, lfi_rce, reset_counter
)
from core.methods.cookie import (
    read_cookie, fetch_cookie, cookie_from_file
)
from core.methods.cache import load, save, parse_url
from core.methods.tor import init_check, enable_tor
from core.methods.version import checkUpdate
from core.methods.loot import set_date
from core.methods.notify import notify
from core.methods.print import (
    banner,
    listprint2,
    print_techniques_gui,
    table_print,
    table_entry_print,
)
from core.methods.crawler import (
    UrlSpider,
    arjunEnum,
    crawler_query,
    crawler_path,
    crawler_cookie,
    crawler_post,
)

if not is_windows:
    import setproctitle
    import notify2


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
    permutationLevel = 2
    param = ""
    post = ""
    authcookie = ""
    tor = False
    loot = False
    vlnfile = "/etc/passwd"
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

    attackIndex = 2
    status = ""

    firstiter = True

    def __init__(self):
        super(VailynApp, self).__init__()
        uic.loadUi("core/qt5/Main.ui", self)  # Load the .ui file
        self.attackOption.addItem("query")
        self.attackOption.addItem("path")
        self.attackOption.addItem("cookie")
        self.attackOption.addItem("post")
        self.attackOption.addItem("scraper")
        self.newTargetButton.clicked.connect(self.getVictim)
        self.attackButton.clicked.connect(self.attackGui)
        self.infoButton.clicked.connect(self.showAttackInfo)
        self.fileDictButton.clicked.connect(self.getFileDictionary)
        self.dirDictButton.clicked.connect(self.getDirDictionary)
        self.addCookieButton.clicked.connect(self.getAuthCookie)
        self.shellBox.stateChanged.connect(self.handleShell)
        self.nosploitBox.stateChanged.connect(self.handlePhase2)
        self.attackOption.currentIndexChanged.connect(self.updateAttack)
        self.attack = self.attackOption.currentIndex() + 1
        self.treeView.setHeaderHidden(True)
        self.textBrowser.setMarkdown("""
```
A phased, evasive Path Traversal + LFI scanning & exploitation tool in Python
```

#### Credits & Copyright

> Vailyn: Copyright © <a href="https://github.com/VainlyStrain">VainlyStrain</a>
>
> Arjun:  Copyright © <a href="https://github.com/s0md3v">s0md3v</a>

#### Arjun Modifications

Arjun was slightly modified to fix false negatives with HTTP Basic Auth Sites.

#### Possible Issues

Found some false positives/negatives (or want to point out other bugs/improvements): please leave an issue!
        """)
        if checkUpdate():
            self.status = "latest version"
        else:
            self.status = "update available"
        self.versionLabel.setText("Vailyn {} : {}".format(
            variables.e_version, self.status,
        ))
        self.stackedWidget.setCurrentWidget(self.fileTree)
        self.exitButton.clicked.connect(self.close)
        self.smallQuitBtn.clicked.connect(self.close)
        self.show()

    def updateAttack(self):
        self.attack = self.attackOption.currentIndex() + 1
        if self.attack == 5:
            self.stackedWidget.setCurrentWidget(self.crawlerOutput)
        elif self.shellBox.isChecked():
            self.stackedWidget.setCurrentWidget(self.crawlerOutput)
        else:
            self.stackedWidget.setCurrentWidget(self.fileTree)
        self.show()

    def getFileName(self):
        return QFileDialog.getOpenFileName()

    def getAuthCookie(self):
        self.cookieDisplay.setText(self.getFileName()[0])

    def getFileDictionary(self):
        self.fileDictDisplay.setText(self.getFileName()[0])

    def getDirDictionary(self):
        self.dirDictDisplay.setText(self.getFileName()[0])

    def showAttackInfo(self):
        if self.attack == 1:
            self.showInfo("[GET] http://example.com?file=../../../")
        elif self.attack == 2:
            self.showInfo("[GET] http://example.com/../../../")
        elif self.attack == 3:
            self.showInfo("[GET] http://example.com COOKIE=../../../")
        elif self.attack == 4:
            self.showInfo("[POST] http://example.com POST=../../../")
        elif self.attack == 5:
            self.showInfo("Automatically retreive all links & perform all tests")

    def showInfo(self, message):
        self.infoDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Info.ui", self.infoDialog)
        self.infoDialog.infoMessage.setText(message)
        self.infoDialog.okButton.clicked.connect(self.infoDialog.close)
        self.infoDialog.exec_()

    def guiSelect(self, payloadlist, nullbytes=False, wrappers=False):
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
                except:
                    self.showError("Invalid Selection string.")

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

    def guiSelectTechniques(self):
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
                        self.showError("Invalid Selection string.")
                        self.selection = []
                    else:
                        self.techniqueDialog.close()
                except Exception:
                    self.showError("Invalid Selection string.")

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

    def showPayloads(self, payloadlist, nullbytelist, wrapperlist):
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

    def read_cookieGui(self, target):
        def intern():
            self.selected = self.cookieDialog.cookieSelectInput.text().strip()
            if self.selected == "" or self.selected not in self.cstr:
                self.showError("Invalid Cookie Name.")
            else:
                self.cookieDialog.close()

        cookie = fetch_cookie(target)
        self.cocancel = False
        i = 0
        if len(cookie.keys()) < 1:
            self.showError("Server did not send any cookies.")
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

    def handleShell(self):
        if self.shellBox.isChecked():
            variables.revshell = True
            self.portEdit.setEnabled(True)
            self.ipEdit.setEnabled(True)
        else:
            variables.revshell = False
            self.portEdit.setEnabled(False)
            self.ipEdit.setEnabled(False)

        self.attack = self.attackOption.currentIndex() + 1
        if self.shellBox.isChecked():
            self.stackedWidget.setCurrentWidget(self.crawlerOutput)
        elif self.attack == 5:
            self.stackedWidget.setCurrentWidget(self.crawlerOutput)
        else:
            self.stackedWidget.setCurrentWidget(self.fileTree)
        self.show()

    def handlePhase2(self):
        if self.nosploitBox.isChecked():
            self.nosploit = True
        else:
            self.nosploit = False

    def attackGui(self):
        self.foundfiles = [""]
        self.foundurls = [""]
        self.foundpayloads = []
        self.foundnullbytes = []
        self.attack = self.attackOption.currentIndex() + 1
        self.filedict = self.fileDictDisplay.text().strip()
        self.dirdict = self.dirDictDisplay.text().strip()

        self.timeLabel.setText("")

        variables.precise = self.preciseFlag.isChecked()
        variables.lfi = self.lfiBox.isChecked()

        if (self.victim == "" or (self.attack == 1 and self.param == "")
                or ((self.filedict == "" or self.dirdict == "")
                and self.attack != 5 and not self.nosploit
                and not self.shellBox.isChecked())):
            self.showError("Mandatory argument(s) not specified.")
            return

        try:
            self.depth1 = int(self.phase1Depth.text().strip())
        except ValueError:
            if self.phase1Depth.text().strip() != "":
                self.showError(
                    "Depths must be valid positive integers!",
                )
                return
        try:
            self.depth2 = int(self.phase2Depth.text().strip())
        except ValueError:
            if self.phase2Depth.text().strip() != "":
                self.showError(
                    "Depths must be valid positive integers!",
                )
                return
        try:
            self.permutationLevel = int(self.phase2PLevel.text().strip())
        except ValueError:
            if self.phase2PLevel.text().strip() != "":
                self.showError(
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
                self.showError(
                    "Listening IP and Port needed for attack.",
                )
                return

        timeout = self.timeoutEdit.text().strip()
        if timeout != "":
            try:
                variables.timeout = int(timeout)
                assert(variables.timeout > 0)
            except (ValueError, AssertionError):
                self.showError(
                    "Timeout must be a valid positive integer!",
                )
                return

        self.authcookie = self.cookieDisplay.text().strip()
        self.loot = self.lootBox.isChecked()
        self.tor = self.torBox.isChecked()
        self.vlnfile = self.vlnFileInput.text().strip()

        if self.tor:
            sig = enable_tor(shell=False)
            if sig == 420:
                ans = self.showQuestion(
                    "Do you have the Tor service up and running?",
                )
                if not ans:
                    return
                enable_tor(shell=False, sig_win=True)
            elif sig == 1337:
                ans = self.showQuestion(
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
            self.showError(
                "An attack parameter is required for this attack.",
            )
            return
        elif self.attack == 4 and self.post == "":
            self.showError(
                "A post data string is required for this attack.",
            )
            return

        if self.attack == 4 and "INJECT" not in self.post:
            self.showError(
                "POST Data needs to contain INJECT at injection point",
            )
            return
        if self.attack == 4 and "=" not in self.post:
            self.showError(
                "POST Data needs to be of form P1=V1&P2=V2",
            )
            return

        self.progressBar.setEnabled(True)
        self.treeView.clear()

        if self.attack == 5:
            self.crawlerResultDisplay.setText("")
            variables.viclist.clear()
            crawlcookies = {}
            arjunjar = None
            if self.authcookie != "":
                arjunjar = cookie_from_file(self.authcookie)
                crawlcookies = requests.utils.dict_from_cookiejar(arjunjar)

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
                if result != None:
                    print("Crawler error: {}".format(result))
                    self.showError(
                        "A crawler error has occurred.",
                    )

            self.tabWidget.setCurrentIndex(self.attackIndex)
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

            self.crawlerResultDisplay.append(
                "\n[Info] Arjun GET Scan started.",
            )
            self.timeLabel.setText("Active Phase: 1")
            self.show()
            app.processEvents()
            siteparams = arjunEnum(cookiefile=self.authcookie)

            self.timeLabel.setText("Active Phase: 2")
            self.show()
            app.processEvents()
            queryattack = crawler_query(
                siteparams, self.victim2, variables.verbose,
                self.depth1, self.vlnfile, self.authcookie, gui=self,
            )
            time.sleep(1)

            self.timeLabel.setText("Active Phase: 3")
            self.show()
            app.processEvents()
            pathattack = crawler_path(
                self.victim2, variables.verbose, self.depth1,
                self.vlnfile, self.authcookie, gui=self,
            )
            time.sleep(1)

            self.timeLabel.setText("Active Phase: 4")
            self.show()
            app.processEvents()
            cookieattack = crawler_cookie(
                self.victim2, variables.verbose, self.depth1,
                self.vlnfile, self.authcookie, gui=self,
            )
            time.sleep(1)

            self.crawlerResultDisplay.append(
                "\n[Info] Arjun POST Scan started.",
            )
            self.timeLabel.setText("Active Phase: 5")
            self.show()
            app.processEvents()
            postparams = arjunEnum(
                post=True,
                cookiefile=self.authcookie,
            )

            self.timeLabel.setText("Active Phase: 6")
            self.show()
            app.processEvents()
            postattack = crawler_post(
                postparams, self.victim2, variables.verbose,
                self.depth1, self.vlnfile, self.authcookie,
                gui=self,
            )
            ending_time = time.time()
            total_time = ending_time - starting_time
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
            ) = self.read_cookieGui(self.victim)
            if self.cookie == None or self.selected == None:
                return

        vlnysis = True

        self.tabWidget.setCurrentIndex(self.attackIndex)
        self.show()
        app.processEvents()

        # present option to skip phase 1 if cache from previous attack present
        targetcache = parse_url(self.victim)
        if (os.path.exists(cachedir + targetcache + "payloads.cache")
                and os.path.exists(cachedir + targetcache + "nullbytes.cache")
                and os.path.exists(cachedir + targetcache + "wrappers.cache")):
            choice = self.showQuestion(
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
                    self.vlnfile, self.authcookie, self.post, self,
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
                self.selectedpayloads = self.guiSelect(
                    self.foundpayloads,
                )
                if self.foundnullbytes:
                    self.selectednullbytes = self.guiSelect(
                        self.foundnullbytes,
                        nullbytes=True,
                    )
                else:
                    self.selectednullbytes = []
                if self.foundwrappers:
                    self.selectedwrappers = self.guiSelect(
                        self.foundwrappers,
                        wrappers=True,
                    )
                else:
                    self.selectedwrappers = []
            else:
                self.showPayloads(
                    self.foundpayloads,
                    self.foundnullbytes,
                    self.foundwrappers,
                )
                return
        else:
            self.selectedwrappers = []
            if not self.nosploit:
                cont = self.showQuestion(
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
                self.showInfo("No payload succeeded.")
                return

        if self.nosploit:
            attackphase = False

        if not self.selectedwrappers:
            self.selectedwrappers = [""]

        if attackphase:
            reset_counter()
            self.timeLabel.setText("Active Phase: 2")
            if variables.revshell:
                if is_windows:
                    question = "Are you listening on {}, port {}?".format(
                        variables.LISTENIP, variables.LISTENPORT,
                    )
                    lis = self.showQuestion(question)
                    if not lis:
                        self.showError(
                            "Please start a listener manually"
                            " before starting the attack."
                        )
                        return
                else:
                    with open(os.devnull, "w") as DEVNULL:
                        subprocess.Popen(
                            ["konsole", "--hold", "-e", "nc -lvp {}".format(
                                variables.LISTENPORT
                            )],
                            close_fds=True,
                            stdout=DEVNULL,
                            stderr=subprocess.STDOUT,
                        )
                self.techniques = self.guiSelectTechniques()
                if not self.techniques:
                    return
                starting_time = time.time()
                lfi_rce(
                    self.techniques, self.attack, self.victim,
                    self.victim2, self.param, self.cookie,
                    self.selected, variables.verbose,
                    self.selectedpayloads, self.selectednullbytes,
                    self.selectedwrappers, self.authcookie, self.post,
                    self.depth2, gui=self, app=app,
                )
            else:
                set_date()
                # equally split dictionary entries to all threads
                sdirlen = 0
                with open(self.dirdict, "r") as f:
                    sdirlen = sum(1 for line in f if line.rstrip()) + 1

                if sdirlen > 100:
                    self.showInfo("Preparing dictionaries...")

                dirlen2 = sdirlen
                felems = dirlen2 - 1
                i = 1
                while (i <= self.permutationLevel):
                    if 0 <= i + 1 and i + 1 <= felems:
                        cur = factorial(felems) / factorial(felems - i - 1)
                    else:
                        cur = 0
                    dirlen2 += cur
                    i += 1
                dirlen = int(dirlen2)
                splitted = gensplit(
                    listperm(self.dirdict, self.permutationLevel),
                    round(dirlen / processes),
                )

                starting_time = time.time()
                with Pool(processes=processes) as pool:
                    res = [pool.apply_async(phase2, args=(
                        self.attack, self.victim, self.victim2, self.param,
                        self.cookie, self.selected, self.filedict, splitty,
                        self.depth2, variables.verbose, self.loot,
                        self.selectedpayloads, self.selectednullbytes,
                        self.selectedwrappers, self.authcookie,
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
            self.guiTree(readable_time)

        self.showInfo(
            "Attack done. Found {} files in {}.".format(
                len(self.foundfiles) - 1, readable_time,
            )
        )

        if self.tor and self.unix:
            stop = self.showQuestion(
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

    def getVictim(self):
        def intern():
            vic = self.targetDialog.vicField.text().strip()
            pam = self.targetDialog.paramField.text().strip()
            vic2 = self.targetDialog.vic2Field.text().strip()
            post = self.targetDialog.postInput.text().strip()
            if vic == "":
                self.showError("-v VIC must be specified.")
            elif self.attack == 1 and pam == "":
                self.showError(
                    "-p PAM must be specified for query attack.",
                )
            elif self.attack == 4 and post == "":
                self.showError(
                    "-s DAT must be specified for POST attack.",
                )
            elif "://" not in vic:
                self.showError(
                    "scheme:// must be sepecified in -v VIC.",
                )
            else:
                self.victim = vic
                if self.attack == 1:
                    self.param = pam
                self.victim2 = vic2
                if self.attack == 4:
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
                elif self.attack == 3 or self.attack == 4 or self.attack == 5:
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
                            vic + "/" +  "INJECT" + vic2,
                        )
                        self.victimDisplayLabel.setToolTip(
                            vic + "/" +  "INJECT" + vic2,
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
        if self.attack == 4:
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

    def guiTree(self, atime):
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

    def showError(self, message):
        self.errorDialog = QtWidgets.QDialog()
        uic.loadUi("core/qt5/Error.ui", self.errorDialog)
        self.errorDialog.errorMessage.setText(message)
        self.errorDialog.errorOkButton.clicked.connect(
            self.errorDialog.close,
        )
        self.errorDialog.exec_()

    def showQuestion(self, message):
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

def app_qt5():
    global app
    app = QtWidgets.QApplication(sys.argv)
    window = VailynApp()
    app.setWindowIcon(QtGui.QIcon("core/qt5/icons/Vailyn.png"))
    rcode = app.exec_()
