#START{
#:
def del_line_startwith(string,hash):
    lines = string.splitlines()
    if lines and lines[0].startswith(hash):
        lines.pop(0)
    text = "\n".join(lines)
    return text
#}END.