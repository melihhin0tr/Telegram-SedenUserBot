# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import re

from sre_constants import error as sre_err

from sedenbot import KOMUT
from sedenecem.events import edit, sedenify

DELIMITERS = ('/', ':', '|', '_')

def separate_sed(sed_string):
    if (len(sed_string) > 3 and sed_string[3] in DELIMITERS
            and sed_string.count(sed_string[3]) >= 2):
        delim = sed_string[3]
        start = counter = 4
        while counter < len(sed_string):
            if sed_string[counter] == '\\':
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if (sed_string[counter] == '\\' and counter + 1 < len(sed_string)
                    and sed_string[counter + 1] == delim):
                sed_string = sed_string[:counter] + sed_string[counter + 1:]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ''

        flags = ''
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()
    return None

@sedenify(pattern='^sed')
def sed(message):
    sed_result = separate_sed(message.text)
    textx = message.reply_to_message
    if sed_result:
        if textx:
            to_fix = textx.text
        else:
            edit(message,
                '`Bunun için yeterli zekâya sahip değilim.`')
            return

        repl, repl_with, flags = sed_result

        if not repl:
            edit(message,
                '`Bunun için yeterli zekâya sahip değilim.`')
            return

        try:
            check = re.match(repl, to_fix, flags=re.IGNORECASE)
            if check and check.group(0).lower() == to_fix.lower():
                edit(message, '`Bu bir yanıtlama. Sed kullanma`')
                return

            if 'i' in flags and 'g' in flags:
                text = re.sub(repl, repl_with, to_fix, flags=re.I).strip()
            elif 'i' in flags:
                text = re.sub(repl, repl_with, to_fix, count=1,
                              flags=re.I).strip()
            elif 'g' in flags:
                text = re.sub(repl, repl_with, to_fix).strip()
            else:
                text = re.sub(repl, repl_with, to_fix, count=1).strip()
        except sre_err:
            edit(message, 'Dostum lütfen [regex](https://regexone.com) öğren!')
            return
        if text:
            edit(message, f'Bunu mu demek istedin ? \n\n{text}')

KOMUT.update({
    "sed":
    "sed<sınırlayıcı><eski kelime(ler)><sınırlayıcı><yeni kelime(ler)>\
    \nKullanım: Sed kullanarak bir kelimeyi veya kelimeleri değiştirir.\
    \nSınırlayıcılar: `/, :, |, _`"
})

