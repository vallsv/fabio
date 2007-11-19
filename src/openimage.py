

"""

Authors: Henning O. Sorensen & Erik Knudsen
         Center for Fundamental Research: Metal Structures in Four Dimensions
         Risoe National Laboratory
         Frederiksborgvej 399
         DK-4000 Roskilde
         email:henning.sorensen@risoe.dk

mods for fabio by JPW

"""

import fabio
from fabio import deconstruct_filename, getnum
from fabio.fabioimage import fabioimage


from fabio import edfimage
from fabio import adscimage
from fabio import tifimage
from fabio import marccdimage
from fabio import mar345image
from fabio import fit2dmaskimage
from fabio import brukerimage
from fabio import bruker100image
from fabio import pnmimage
from fabio import GEimage
from fabio import OXDimage


MAGIC_NUMBERS = [
    # "\42\5a" : 'bzipped'
    # "\1f\8b" : 'gzipped'
    ("FORMAT :        86" , 'bruker'), 
    ("\x4d\x4d\x00\x2a"   , 'tif') ,
    ("\x49\x49\x2a\x00"   , 'tif') ,
    # ADSC must come before edf
    ("{\nHEA"             , 'adsc'),
    ("{"                  , 'edf'),
    ("\r{"                , 'edf'),
    ("ADEPT"              , 'GE'),
    ("OD"                 , 'OXD'),
    # hint : MASK in 32 bit
    ('M\x00\x00\x00A\x00\x00\x00S\x00\x00\x00K\x00\x00\x00' , 'fit2dmask') ,
    ]

def do_magic(byts):
    """ Try to interpret the bytes starting the file as a magic number """
    for magic, format in MAGIC_NUMBERS:
        if byts.find(magic) == 0:
            return format
        if 0: # debugging - bruker needed 18 bytes below
            print "m:",magic,"f:",format,
            print "bytes:",magic,"len(bytes)",len(magic),
            print "found:",byts.find(magic) 
            for i in range(len(magic)):
                print ord(magic[i]),ord(byts[i]),magic[i],byts[i]
    raise Exception("Could not interpret magic string")

def openimage(filename):
    """ Try to open an image """
    try:
        imo = fabioimage()
        byts = imo._open(filename).read(18)
        filetype = do_magic(byts)
        filenumber = getnum(filename)
    except IOError:
        # File probably does not exist
        raise
    except:
        try:
            file_obj = deconstruct_filename(filename)
            if len(file_obj.format) != 1 and \
                    type(file_obj.format) != type(["list"]):
                # one of OXD/ ADSC - should have got in previous
                raise Exception("openimage failed on magic bytes and name guess")
            filetype = file_obj.format
            filenumber = file_obj.num
        except:
            import traceback
            traceback.print_exc()
            raise Exception("Fabio could not identify "+filename)

    
    klass_name = filetype + 'image' 
    #print "looking for",klass_name
    if hasattr(fabio, klass_name):
        module = getattr(fabio, klass_name)
        if hasattr(module, klass_name):
            klass  = getattr(module, klass_name)
        else:
            raise Exception("Module " + module + "has no image class")
    else:
        raise Exception("Filetype not known " + filename + " " +
                        klass_name)
    obj = klass()
    obj.read(filename)
    return obj

        


