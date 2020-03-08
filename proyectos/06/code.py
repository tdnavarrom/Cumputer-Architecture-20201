class Code:

    """Translates Hack assembly language mnemonics into binary codes."""

    @staticmethod
    def dest(mnemonic):

        """Returns the binary code of the dest mnemonic."""

        if 'A' not in mnemonic and 'M' not in mnemonic and 'D' not in mnemonic and mnemonic != "":
            raise KeyError

        if 'A' in mnemonic:
            A = '1'
        else:
            A = '0'

        if 'D' in mnemonic:
            D = '1'
        else:
            D = '0'

        if 'M' in mnemonic:
            M = '1'
        else:
            M = '0'

        return A + D + M


    @staticmethod
    def comp(mnemonic):

        """Returns the binary code of the comp mnemonic.
           table{'typeOfOperations':'Binary Code'}"""

        if "M" in mnemonic:
            a='1'
        else:
            a='0'

        table = {
            '0':   '101010',
            '1':   '111111',
            '-1':  '111010',
            'D':   '001100',
            'A':   '110000',
            'M':   '110000',
            '!D':  '001101',
            '!A':  '110001',
            '!M':  '110001',
            '-D':  '001111',
            '-A':  '110011',
            '-M':  '110011',
            'D+1': '011111',
            'A+1': '110111',
            'M+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'M-1': '110010',
            'D+A': '000010',
            'D+M': '000010',
            'D-A': '010011',
            'D-M': '010011',
            'A-D': '000111',
            'M-D': '000111',
            'D&A': '000000',
            'D&M': '000000',
            'D|A': '010101',
            'D|M': '010101'
        }

        return a + table[mnemonic]


    @staticmethod
    def jump(mnemonic):

        """Returns the binary code of the jump mnemonic,
           table{'typeOfJump':'Binary Code'}"""

        table = {
            '':    '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111'
        }

        return table[mnemonic]
