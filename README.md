# Fretboard Scale Images

This is a python program that displays color coded musical scales on a fretboard for any fretted stringed instrument. Any scale consisting of any subset of [A, A#, B, C, C#, D, D#, E, F, F#, G, G#] can be input. The number of strings, number of frets, tuning, and color coding are configurable.

## Dependencies:

pycairo 1.18.2
numpy 1.17.4

## Arguments:

### Required:

-s: Number of strings on your fretted instrument

-f: Number of frets on your fretted instrument

-t: A comma separated list of the notes your instrument is tuned to starting from lowest string

-n: A comma separated list of notes in your scale. 

-p: File path to save image to. Can be a .pdf, .png, or .svg file. File type for saving is deduced from this input.

### Optional:

-c: The colors to draw the scale notes in. There are three options for specifying note colors.
                            
1) It can be left blank. All scale notes will be drawn in black by default.
                            
2) A comma separated list of note:color pairs. For example, specifying the following will draw E notes in red, G notes in blue, C notes in teal, and any unspecified notes in black:
    -c e:r,g:b,c:t
                            
3) A comma separated list of colors for each note in your scale in the same order as your scale. A color must be specified for each note if this format is used. 

Duplicate colors are allowed for both options 2 and 3. The following colors are available:
    r - red
    o - orange
    y - yellow
    g - green
    c - cyan
    b - blue
    m - magenta
    t - teal
    k - black # MATLAB haunts me
    p - pink
    l - lavender
    n - navy
    w - white

These colors were chosen because they can be easily abbreviated by 1 letter and supposedly [can be easily distinguished by 95% of population](https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/)
    
-w: Output image width

-e: Output image height

## Examples

E Minor is [E, F#, G, A, B, C, D]. Let's say we want to highlight the root, the minor third, the fifth, and the minor sixth, so [E, G, B, C]. We want to highlight these notes as red, green, blue, and yellow respectively. We will do this for a 6 string guitar with 24 frets in standard tuning. If you do not understand these command line arguments, please scroll up and read the Arguments section.

`python fretboard_scale_image.py -s 6 -f 24 -t e,a,d,g,b,e -n e,f#,g,a,b,c,d -c e:r,g:g,b:b,c:y -p e_minor_standard.svg`

![E Minor Example Image](./docs/e_minor_standard.svg)

This will save an e_minor_standard.svg in your current folder. You can open it in a browser. If you'd prefer, you can change the extension to .pdf or .png and open it with a PDF of PNG viewer. Notice that the notes we did not specify a color for are black by default.

One more example. D Minor is [D, E, F, G, A, A#, C]. This time let's highlight the pentatonic minor scale within D Minor, so [D, F, G, A, C]. We will use the colors cyan, green, yellow, magenta, and orange respectively. We will specify a default color of black for the other notes. We will do this for a 6 string guitar with 17 frets in drop D tuning.

`python fretboard_scale_image.py -s 6 -f 17 -t d,a,d,g,b,e -n d,e,f,g,a,a#,c -c c,k,g,y,m,k,o -p d_minor_drop_d.svg`

![D Minor Example Image](./docs/d_minor_drop_d.svg)

Notice that this time we specified a color for each note in the notes list. These colors are applied in order. Personally, I prefer the note:color pair method, but to each their own. 



