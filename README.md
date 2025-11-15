# pause.py
Python3 script that allows for customization, including replacing the prompt, a response option, quiet mode, timer, and echoing to variable.
The program will echo "Press any key to continue..." indefinitely until either the user presses any key (but [Shift] or arrow keys), or the optional timer [--t | --timer] reaches zero. Timer is shown in [00:00:00] format where hours and minutes hide as it reaches zero until the final count is [00]. The program allows for quiet running with no prompt, just a pause with cursor blink [-q | --quiet] that must have a timer set as well in order to run. There is an option to place an alternative prompt which replaces the default with your own [-p | --prompt ,(Must be within double quotes)] and the ability to also add response text to the output [-r | --response (Must be within double quotes)].I have added the option to send the key press to be able to be used with command substitution in order to populate variables and work with case statements, etc.

When I migrated to Linux from Windows/DOS, I was rather surprised that there wasn't some type of "pause" function of any sort within the basic functioning of Linux, so I thought I would write a program that had the functionality I would have liked the Windows program to have.

The default prompt is "Press any key to continue..."

Usage:
    $ pause.sh [-p|--prompt "<text>"] [-t|--timer <seconds>] [-r|--response "<text>"] [-h|--help] [-q|--quiet ] [-e, --echo]

    -p, --prompt    [ text string required (string must be in quotes)  ]
    -t, --timer     [ number of seconds ]
    -r, --response  [ text string required (string must be in quotes)  ]
    -h, --help      [ help information ]
    -q, --quiet     [ quiets text, requires timer [-t, --timer] be set. ]
    -e, --echo      [ echoes the key press to stdout to use with case statements, etc. ]

    Examples:
    Input:  $ pause.sh
    Output: $ Press any key to continue...
            $
    
    Input:  $ pause.sh --timer <seconds>
    Output: $ [timer] Press any key to continue...
            $
    
    Input:  $ pause --prompt "Optional Prompt" --response "Your response"
    Output: $ Optional Prompt
            $ Your Response
            $
    
    Input:  $ pause -p "Optional Prompt" -r "[ Your response ]" -t <seconds>
    Output: $ [timer] Optional Prompt
            $ [ Your Response ]
            $
    [format of time will be 00:00:00]

    Input:  $ pause -q -t30
    Output: $ 
            $

    Note: Quiet mode (-q|--quiet) will hide all output until the response (-r|--response) text, if given, or until the contiuation of the process.
          Quiet mode must be used in conjunction with a -t, --timer function to operate.

