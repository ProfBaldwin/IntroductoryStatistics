import sys
import os
import locale


# Define common text elements
CSS_code = """
.videoWrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  height: 0;
}
.videoWrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
"""

videoWrapper = """
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div>
<div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<div class="videoWrapper">
<iframe width="1280" height="720" src="https://www.youtube.com/embed/{YouTubeID}?vq=hd1080" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
</div>
</div>
</div>
"""

cmd_to_html = 'jupyter nbconvert --to html "{notebook}"'

for root, dirs, files in os.walk("."):
    for filename in files:
        if filename.endswith(".ipynb"):
            filepath = os.path.join(root, filename)
            os.system(cmd_to_html.format(notebook = filepath))

for root, dirs, files in os.walk("."):
    for filename in files:
        if filename.endswith(".html"):
            print(filename)
            filepath = os.path.join(root, filename)

            # Grab file text
            f = open(filepath, "r", encoding="utf-8")
            text = f.read()
            f.close()

            # Insert additional CSS
            style_pos = text.find("\n", text.find("<style")) + 1
            text = text[:style_pos] + CSS_code + text[style_pos:]

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
                    cut_start = text.rfind('<span class="c1">', 0, beg)
                    cut_end = text.find('</span>', end) + 8
                    text = text[:cut_start] + text[cut_end:]
                elif command[0:4] == "VID=":
                    vid_id = command[4:]
                    embed_code = videoWrapper.format(YouTubeID = vid_id)
                    cut_start = text.rfind(
                            '<div class="cell border-box-sizing code_cell rendered">', 0, beg)
                    cut_end = text.find('<div', end)
                    text = text[:cut_start] + embed_code + text[cut_end:]
                elif command == "HIDE_INPUT":
                    cut_start = text.rfind('<div class="input">', 0, beg)
                    cut_end = text.find('<div class="output_wrapper">', end)
                    text = text[:cut_start] + text[cut_end:]
                else:
                    print("ERROR: Unknown command: " + command)
                    sys.exit()

                # Find the start of the next command
                beg = text.find('#**') + 3

            f = open(filepath, 'w', encoding="utf-8")
            f.write(text)
            f.close()

