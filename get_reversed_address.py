##to find a postciode in an address
import re

def reverse_address(address):
    postcodeRegex = (
        '([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})')

    x = re.search(postcodeRegex, address)
    if x is not None:
        return(x.group(0) + ' ' + address.replace(x.group(0), ''))
