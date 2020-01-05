import cairo
import argparse
import numpy as np

def make_fretboard(num_strings, num_frets, tuning):
    """
    Constructs a 2d list representing a fretboard.
    The 0-th element is your lowest string (i.e. low E on six string)
    Each string is a list of num_frets elements.
    Each element is the note at that fret.

    inputs:
        tuning: array specifying the note of the 0-th fret of each string, 
            starting from lowest string 
            
        num_frets: number of frets on your guitar
    
    outputs:
        fretboard: 2d list representing a fretboard.
    """
    notes = {'a': 0, 'a#': 1, 'b': 2, 'c': 3, 'c#': 4, 'd': 5, 
         'd#': 6, 'e': 7, 'f': 8, 'f#': 9, 'g': 10, 'g#': 11}

    # {1: 'a', 2: 'b', etc.}
    inverted_notes = dict([[v,k] for k, v in notes.items()])

    # numerical value of 0-th fret notes given input tuning
    current_notes = [notes[note] for note in tuning]
    
    fretboard = [[] for _ in range(num_strings)]
    for i in range(num_strings):
        for _ in range(num_frets+1):
            # fretboard[i][j] == note on i-th string at j-th fret given input tuning
            fretboard[i].append(inverted_notes[current_notes[i]])
            
            # increment note for next fret on i-th string, mod 12 because notes are cyclic
            # 
            # Its Z_12!
            # https://www.math.drexel.edu/~dp399/musicmath/algebraicmusictheory.html
            # https://codedot.github.io/tonnetz/
            current_notes[i] = (current_notes[i] + 1) % 12
        
    return fretboard


def print_fretboard(fretboard):
    """
    Prints a text representation of the input fretboard.
    
    inputs:
        fretboard: a 2d list representing a fretboard returned by make_fretboard().
    """
    # even spacing is frustrating
    notes_per_string = len(fretboard[0])
    num_strings = len(fretboard)
    initial_fret_string = ""
    fret_string = initial_fret_string
    for i in range(notes_per_string):
        num_trailing_spaces = 3
        if i >= 10:
            num_trailing_spaces -= 1
        fret_string += ('%d' % i) + (" " * num_trailing_spaces)
    print(fret_string)
    
    for i in range(num_strings-1, -1, -1):
        string_string = " " * len(initial_fret_string)
        for j in range(notes_per_string):
            num_trailing_spaces = 1
            
            # if note is 2 characters long, add 1 more trailing space
            # if note is 1 character long, add 2 more trailing spaces
            num_trailing_spaces += (len(fretboard[i][j]) % 2) + 1
            string_string += fretboard[i][j] + (" " * num_trailing_spaces)
            
        print(string_string)


def get_note_locations(fretboard):
    """
    Constructs a dictionary of note locations on an input fretboard.
    
    inputs:
        fretboard: a 2d list representing a fretboard returned by make_fretboard().
        
    outputs:
        note_locations: a dictionary of note locations on the input fretboard.
    """
    note_locations = {'a': [], 'a#': [], 'b': [], 'c': [], 'c#': [], 'd': [], 
                      'd#': [], 'e': [], 'f': [], 'f#': [], 'g': [], 'g#': []}
    
    # go through fretboard, record each possible (string, fret) pair for every note 
    for i in range(len(fretboard)):
        for j in range(len(fretboard[i])):
            note_locations[fretboard[i][j]].append((i, j))
            
    return note_locations


def draw_guitar_scale(fretboard, note_locations, 
                      scale_notes, note_highlights={}, 
                      save_name='scale.svg', im_width=792,
                      im_height=612):
    """
    Draws a vector graphic image of a fretboard with highlighted input notes to 
    a pdf, png or svg file.
    
    inputs:
        fretboard: a 2d list representing a fretboard returned by make_fretboard().
        note_locations: a dictionary of note locations on the input fretboard.
        scale_notes: a list of notes from any scale on your instrument.
        note_highlights: an optional dictionary specifying colors for notes. 
            if a dictionary is not specified, all notes are drawn in black.
        save_name: a file path to save your graphic to.
    """
    
    # im_width and im_height default value explanation:
    # 1 point == 1/72.0 inch
    # For 8.5 x 11 printable pdf we have:
    # 72 * 11 = 792 points
    # 72 * 8.5 = 612 points
    
    # deduce surface from input file extension
    # SVG's render great in browsers by the way, definitely my favorite.
    ext = save_name.split('.')[-1]
    if ext == 'svg':
        ps = cairo.SVGSurface(save_name, im_width, im_height)
    elif ext == 'pdf':
        ps = cairo.PDFSurface(save_name, im_width, im_height)
    elif ext == 'png':
        ps = cairo.ImageSurface(cairo.FORMAT_ARGB32, im_width, im_height)
    else:
        raise ValueError('Input extension %s unrecognized. Use .pdf, .png, or .svg.' % ext)
        
    cr = cairo.Context(ps)
    
    num_strings = len(fretboard)
    notes_per_string = len(fretboard[0])
    
    # You'll see a lot of these weird numbers being multipled by width and height
    # throughout this function. I initially went through with some fixed width height 
    # and found exact values that made the graphic look exactly like I wanted it to. 
    # Then, I divided each value by the fixed width or height (depending on the value) 
    # I was using to find out the ratio of it to the width/height. That ratio can be 
    # multipled by any width or height to achieve an appropriately scaled image, so feel 
    # free to mess with the im_width or im_height values if you want bigger images
    initial_x_point = 0.074 * im_width
    final_x_point = 0.981 * im_width
    
    # I really wanted this to be spaced like a real fret board, but every
    # solution I can think of to solve for x's that still fit to the 
    # page for any number of frets involves a term with a log-sum 
    # and solving a nonlinear optimization problem just to make the 
    # image look like a real guitar feels like overkill so this guitar
    # has evenly spaced frets
    fret_x = np.linspace(initial_x_point, final_x_point, notes_per_string)
    
    initial_y_point = 0.277 * im_height # this is the high string
    fret_height = 0.555 * im_height
    string_distance = fret_height / (num_strings - 1)
    
    # 0-th element is lowest string
    fret_y = np.linspace(initial_y_point+fret_height, initial_y_point, num_strings)

    # set up text and line parameters
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(2)
    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    font_size = 0.019 * im_width
    cr.set_font_size(font_size)
    x_text_offset = font_size / 2
    y_top_text_offset = font_size
    y_bottom_text_offset = 2 * font_size
    
    # draw each fret from the highest string to the lowest string
    # label each fret with its fret number
    for i, x in enumerate(fret_x):
        cr.move_to(x-x_text_offset, fret_y[-1]-y_top_text_offset)
        cr.show_text('%d' % i)
        cr.move_to(x, fret_y[-1])
        cr.line_to(x, fret_y[0])
        cr.stroke()
        cr.move_to(x-x_text_offset, fret_y[0]+y_bottom_text_offset)
        cr.show_text('%d' % i)
        
    # set up font for labeling string tuning
    font_size = 0.042 * im_width
    cr.set_font_size(font_size)
    x_text = 0.009 * im_width # starting x for each string label
    y_text_offset = font_size / 4
    
    # draw strings from 0-th fret to n-th fret
    # label each string with its open string note
    for i, y in enumerate(fret_y):
        cr.move_to(x_text, y+y_text_offset)
        cr.show_text(fretboard[i][0].upper())
        cr.move_to(fret_x[0], y)
        cr.line_to(fret_x[-1], y)
        cr.stroke()
    
    # draw scale notes on fretboard as circles
    # color circles according to input color_highlights
    # default color is black
    radius = 0.009 * im_width
    for note in scale_notes:
        for loc in note_locations[note]:
            i, j = loc
            x_c = fret_x[j]
            y_c = fret_y[i]
            cr.arc(x_c, y_c, radius, 0, 2*np.pi)
            
            cr.set_source_rgb(0, 0, 0)
            if note in note_highlights:
                r, g, b = note_highlights[note]
                cr.set_source_rgb(r, g, b)
            
            cr.fill()
    
    # set up font for legend
    font_size = 0.042 * im_width
    cr.set_font_size(font_size)
    y_text_offset = font_size / 4
    
    # create legend
    leg_spacing = font_size * 2
    leg_width = leg_spacing * (len(scale_notes)-1)
    leg_center_x = im_width / 2
    leg_y = fret_y[-1] / 2
    leg_initial_x = leg_center_x - (leg_width / 2) - (font_size / 2)
    leg_x = np.linspace(leg_initial_x, leg_initial_x + leg_width, len(scale_notes))
    
    for i, note in enumerate(scale_notes):
        cr.set_source_rgb(0, 0, 0)
        
        # color legend appropriately
        if note in note_highlights:
            r, g, b = note_highlights[note]
            cr.set_source_rgb(r, g, b)
        
        cr.move_to(leg_x[i], leg_y)
        cr.show_text(note.upper())

    if ext == 'pdf' or ext == 'svg':    
        cr.show_page()
    else:
        ps.write_to_png(save_name)

def main():
    parser = argparse.ArgumentParser(description='Fretboard scale creator')
    parser.add_argument('-s', '--num-strings', 
                        help='Number of strings on your fretted instrument',
                        type=int,
                        required=True)
    parser.add_argument('-f', '--num-frets',
                        help='Number of frets on your fretted instrument',
                        type=int,
                        required=True)
    parser.add_argument('-t', '--tuning',
                        help='Comma separated list of notes your instrument is tuned to starting from lowest string',
                        type=str,
                        required=True)
    parser.add_argument('-n', '--scale-notes',
                        help='Comma separated list of notes in your scale',
                        type=str,
                        required=True)
    parser.add_argument('-c', '--note-colors',
                        help="""
                            There are three options for specifying note colors.
                            
                            1) It can be left black. All scale notes will be drawn in black by default.
                            
                            2) A comma separated list of note:color pairs. For example, specifying the following will
                            draw E notes in red, G notes in blue, C notes in teal, and any unspecified notes in black: 
                            -c e:r,g:b,c:t
                            
                            3) A comma separated list of colors for each note in your scale in the same order as your
                            scale. A color must be specified for each note if this format is used. Duplicates are allowed.
                            The following colors are available:
                                r - red, 
                                o - orange, 
                                y - yellow, 
                                g - green, 
                                c - cyan, 
                                b - blue, 
                                m - magenta, 
                                t - teal, 
                                k - black,
                                p - pink,
                                l - lavender, 
                                n - navy,
                                w - white
                            """,
                        type=str,
                        required=False)
    parser.add_argument('-p', '--save-path',
                        help='File path to save image to. Can be a .pdf, .png, or .svg file.',
                        type=str)
    parser.add_argument('-w', '--im-width', 
                        help='Output image width',
                        type=int,
                        required=False,
                        default=792)
    parser.add_argument('-e', '--im-height',
                        help='Output image height',
                        type=int,
                        required=False,
                        default=612)
    args = parser.parse_args()
    
    # ridiculous that argparse doesn't support CSV input lists
    args.tuning = [n.lower() for n in args.tuning.split(',')]
    args.scale_notes = [n.lower() for n in args.scale_notes.split(',')]
    
    # 13 colors that can be easily abbreviated by 1 letter and supposedly can be
    # easily distinguished by 95% of population
    # https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
    colors_to_rgb = {'r': (230, 25, 75),
                     'o': (245, 130, 48),
                     'y': (255, 225, 25),
                     'g': (60, 180, 75),
                     'c': (70, 240, 240),
                     'b': (0, 130, 200),
                     'm': (240, 50, 230),
                     't': (0, 128, 128), 
                     'k': (0, 0, 0), # MATLAB haunts me
                     'p': (250, 190, 190),
                     'l': (230, 190, 255),
                     'n': (0, 0, 128),
                     'w': (255, 255, 255)}

    for k, v in colors_to_rgb.items():
        colors_to_rgb[k] = [c/255 for c in v]
    
    # populate note_highlights dictionary based on user input choice
    note_highlights = {}
    if args.note_colors is not None:
        note_color_pairs = False
        if ':' in args.note_colors:
            note_color_pairs = True
            
        args.note_colors = [c.lower() for c in args.note_colors.split(',')]

        # handle note color input appropriately
        if note_color_pairs:
            for pair in args.note_colors:
                try:
                    n, c = pair.split(':')
                except ValueError:
                    print('If note:color pair format is used for note_color input, each string in the comma separated list must be a note:color pair.')
                note_highlights[n] = colors_to_rgb[c]
        else:
            if len(args.note_colors) != len(args.scale_notes):
                raise ValueError("""
                    note_colors input must be same length as scale Notes input if 
                    comma separated note:color pairs are not used. See -h for details.
                    """)
            for i, n in enumerate(args.scale_notes):
                note_highlights[n] = colors_to_rgb[args.note_colors[i]]

    # make badass images
    fretboard = make_fretboard(args.num_strings, args.num_frets, args.tuning)
    note_locations = get_note_locations(fretboard)
    draw_guitar_scale(fretboard, note_locations, args.scale_notes, note_highlights,
                      save_name=args.save_path, im_width=args.im_width, 
                      im_height=args.im_height)
    
if __name__ == "__main__":
    main()
