import serial
from sima import logger
from lxml import etree

class Word:
    """Class that defines a word with :
    - his code
    - his french translation
    - his english translation
    - etc..."""

    def __init__(self, code, word_fr, word_en):
        self.code = code
        self.word_fr = word_fr
        self.word_en = word_en

class Database:
    """Class that defines a database with :
    - wordlist
    - methods"""

    def __init__(self):
        self.wordlist = []

    def LoadDB(self, db):
        """Function that loads the database."""

        tree = etree.parse(db)
        root = tree.getroot()

        codes = []
        words =[]
        count = 0
        i = 0

        for child in root:
            codes.append(child.attrib["id"])
            count += 1

        if count < 1:
            return None

        while i < count:
            words.append(Word(codes[i], root[i][0].text, root[i][1].text))
            i += 1

        self.wordlist = words

    def AddDB(self, code, word_fr, word_en, db):
        """Function that add an entry to the database."""
        tree = etree.parse(db)
        
        new_entry = etree.fromstring('''<word id="{code}">
        <french>{word_fr}</french>
        <english>{word_en}</english>
        </word>'''.format(code=code, word_fr=word_fr, word_en=word_en))

        root = tree.getroot()
        root.append(new_entry)

        f = open(db, 'wb')
        f.write(etree.tostring(root, pretty_print=True))
        f.close()

class Arduino:
    """Class that defines a board with :
    - his port
    - his baudrate
    - his timeout
    - his refreshrate
    - his state
    - the last received lane
    """

    def __init__(self, port, baudrate, timeout, refreshrate):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.refreshrate = refreshrate
        
        self.state = False
        self.ser = None
        self.lastline = ""
        
        self.noglove = False
    def initialize(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            self.state = True
        except:
            self.state = False

    def read(self):
        if self.state:
            try:
                self.lastline = self.ser.readline()
                self.ser.flushInput()
                self.lastline = str(self.lastline.strip())
                self.lastline = self.lastline.replace("b'", "")
                self.lastline = self.lastline.replace("'", "")
            except serial.SerialException:
                return ("Error while reading Arduino data...")
            except KeyboardInterrupt:
                return ("Reading process was interrupted.")
        else:
            return ("The board isn't initialized.")

    def stop(self):
        if self.state:
            self.ser.close()