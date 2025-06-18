#START{
import re
#:
def url_fix(url):
    if url.startswith("http://") or url.startswith("https://"):
        url = str(url)
    else:
        url = "http://" + str(url)
    return url
#}END.