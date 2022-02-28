
import subprocess
import urllib
import os

import urllib.request

ANTLR_JAR = "antlr-4.9.3-complete.jar"
ANTLR_URL = 'https://www.antlr.org/download/' + ANTLR_JAR

if not os.path.isfile(ANTLR_JAR):
    jar = urllib.request.urlopen(ANTLR_URL)
    with open(ANTLR_JAR, 'wb') as output:
        output.write(jar.read())

subprocess.run(["java", "-Xmx500M", "-cp", ANTLR_JAR, "org.antlr.v4.Tool", "-Dlanguage=Python3",
                "-o", "../src/destables/cparser", "-no-listener", "-visitor", "C11.g4"])
