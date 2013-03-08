
class HardwareInput:
    
    knob1 = 200
    knob2 = 200
    knob3 = 200
    knob4 = 200
    clear_screen = False
    note_on = False
    note_off = False

    midi_clk = False
    midi_start = False
    midi_stop = False
    midi_clk_count = 0

    quarter_note = False
    eighth_note = False
    eighth_note_triplet = False
    sixteenth_note = False
    thirtysecond_note = False

    half_note = False
    whole_note = False

    midi_clk_count = 0
    whole_note_count = 0

    note_ch = 1
    note_velocity = 0
    note_note = 60

    #patch interface
    next_patch = False
    set_patch = False
    reload_patch = False
    patch = ''

    quit = False

    osd = False
    
    def parse_serial(self, line):
        array = line.split(',')
        #print array
 
        if len (array) == 1:
            if array[0] == "rlp": 
                self.reload_patch = True
  
        if len (array) == 1:
            if array[0] == "osd": 
                if self.osd :
                    self.osd = False
                else :
                    self.osd = True

  
        if len (array) == 1:
            if array[0] == "quit": 
                self.quit = True
 
        if len (array) == 1:
            if array[0] == "cs": 
                self.clear_screen = True
 
        # basic parse sd key (this is supposed to be mapped to shutdowh -h now)
        if len (array) == 1:
            if array[0] == "sd": 
                self.clear_screen = True
      
        # basic parse next command
        if len(array) == 1:
            if array[0] == "n" :
                self.next_patch = True
  
        # basic midi start
        if len(array) == 1:
            if array[0] == "ms" :
                self.midi_start = True
                self.midi_clk_count = 0
                self.whole_note_count = 0
        
        # basic midi syn
        if len(array) == 1:
            if array[0] == "my" :
#                print self.midi_clk_count
                self.clk = True
                
                if self.whole_note_count == 0: self.whole_note = True
                if (self.whole_note_count % 48) == 0: self.half_note = True

                if self.midi_clk_count == 0 : self.quarter_note = True
                if (self.midi_clk_count % 12) == 0 : self.eighth_note = True
                if (self.midi_clk_count % 8) == 0 : self.eighth_note_triplet = True
                if (self.midi_clk_count % 6) == 0 : self.sixteenth_note = True
                if (self.midi_clk_count % 3) == 0 : self.thirty_triplet = True

                self.midi_clk_count += 1
                if self.midi_clk_count == 24 : self.midi_clk_count = 0

                self.whole_note_count += 1
                if self.whole_note_count == 96 : self.midi_clk_count = 0

        if len(array) == 2 :
            if array[0] == "setpatch" :
                self.set_patch = True
                self.patch = array[1]


        # basic parse of knob array
        if len(array) == 5 :
            if array[0] == "k" :
                if array[1].isdigit() :
                    self.knob1 = int(array[1])
                if array[2].isdigit() :
                    self.knob2 = int(array[2])
                if array[3].isdigit() :
                    self.knob3 = int(array[3])
                if array[4].isdigit() :
                    self.knob4 = int(array[4])
      
        # basic parse note on command
        if len(array) == 4:
            if array[0] == "no" :
                self.note_on = True
                if array[1].isdigit() :
                    self.note_ch = int(array[1])
                if array[2].isdigit() :
                    self.note_note = int(array[2])
                if array[3].isdigit() :
                    self.note_velocity = int(array[3])
 
        # basic parse note off command
        if len(array) == 4:
            if array[0] == "nf" :
                self.note_off = True
                if array[1].isdigit() :
                    self.note_ch = int(array[1])
                if array[2].isdigit() :
                    self.note_note = int(array[2])
                if array[3].isdigit() :
                    self.note_velocity = int(array[3])

 

 

    def clear_flags(self):
        self.next_patch = False
        self.clear_screen = False
        self.note_on = False
        self.note_off = False
        self.quarter_note = False
        self.eighth_note = False
        self.eighth_note_triplet = False
        self.sixteenth_note = False
        self.thirtysecond_note = False
        self.half_note = False
        self.whole_note = False
        self.next_patch = False
        self.set_patch = False
        self.reload_patch = False



