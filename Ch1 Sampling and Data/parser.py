import sys

filename = "1.1 Key Terms in Statistics.html"

# Grab file text
f = open(filename, "r")
text = f.read()
f.close()

# Find the beginning of input divs and the beginning of output_wraper divs
input_div_idx = []
idx = text.find('<div class="input">')
while idx > -1:
    input_div_idx.append(idx)
    idx = text.find('<div class="input">', idx + 1)

output_div_idx = []
idx = text.find('<div class="output_wrapper">')
while idx > -1:
    output_div_idx.append(idx)
    idx = text.find('<div class="output_wrapper">', idx+1)

# Find the start of the next command
beg = text.find('#**') + 3
while beg > 2:

    # Find the end of the command
    end = text.find('**#', beg)
    if end == -1:
        print("ERROR: Missing end code **#")
        sys.exit()

    # Grab the command
    command = text[beg:end]

    # Execute the command
    if command[0:4] == "ALT=":
        alt_text = 'alt="' + command[4:] + '" '
        img_idx = text.find('<img ', end) + 5
        text = text[:img_idx] + alt_text + text[img_idx:]
    elif command == "HIDE_INPUT":
        for input_idx in input_div_idx[::-1]:
            if input_idx < beg:
                break
        for output_idx in output_div_idx:
            if output_idx > end:
                break
        text = text[:input_idx] + text[output_idx:]
    else:
        print("ERROR: Unknown command: " + command)
        sys.exit()

    # Find the start of the next command
    beg = text.find('#**', end) + 3

f = open(filename, 'w')
f.write(text)
f.close()

