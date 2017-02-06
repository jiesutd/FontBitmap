FontBitMap
======
Giving the characters, it generate the 16x16 binary matrix of the characters shape.

It also provide some tedious demos. 

![alt text](https://github.com/jiesutd/FontBitmap/blob/master/cn_char.map "Character bitmap demo")

* demo_show_string: show the binary maps of the giving string, 
* demo_similar_char: find the similar characters of giving character and the (left,right,up,down) choice with the split position. The demo "demo_similar_char("苟", 3, "up")" mean find all characters which have the same first 3 lines of the char "苟". If will first show the binary map of the given base_character, matched results will be shown after you close the map. (Or just comment out line 172 to jump the show map process)


File SimSun-16.bdf is the font file, which can be found in Windows/Fonts/xx.ttc, then use FontForge to convert into .bdf file.





