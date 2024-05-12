import time
import os
import sys



#cooles Spiel Designs


print("loading")
animation = ["[#"        "]10%","[##"       "]20%","[###"      "]30%","[####"     "]40%","[#####"    "]50%",
             "[######"    "]60%","[#######"  "]70%","[########"  "]80%","[#########" "]90%","[##########]100%"]
for i in range(len(animation)):
    time.sleep(0.6)
    sys.stdout.write("\r" +animation[i % len(animation)])


