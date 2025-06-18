#START{
import hashlib
#:
def tomd5(data):
    return hashlib.md5(data.encode('utf-8')).hexdigest()
#}END.