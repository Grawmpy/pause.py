#!/usr/bin/python3

#  Author: Grawmpy <grawmpy@gmail.com> (CSPhelps)

#  Description: This script allows for the interruption of the current process until either 
#  the timer reaches [00], or the user presses any key. If no timer is used, the process
#  will be stopped indefinitely until the press of any key except [CTRL], [ALT], [Shift]. Using 
#  the timer  (in seconds only) continues the current process without user interaction. The order of the 
#  variables can be passed to the script in any order, doesn't matter, they are processed as they 
#  are read and the result is stored until applied to the final output. 
# 
#  Default prompt: "Press any key to contniue..."
#  
#  Example of code:
#  $ pause
#  $ Press any key to continue...
#  
#  $ pause -t 10 -p "Hello World" -r "Thank you, come again".
#  $ [10] Hello World
#  $ Thank you, come again.
#
#  $ keypress=$(pause -e -p "Enter your selection: ")
#  $ Enter your selection: f (key not echoed to monitor)
#  $ echo $keypress
#  $ f
# 
#  Options include: [-t, --timer] [-p, --prompt] [-r, --response] [-e, --echo]
#  -t, --timer: pause -t 10 (Will display as [00h:00m:00s] before the prompt)
#  -p, --prompt: pause -p "Hello World"
#  -r, --response: pause -r "Thank you, come again."
#  -e, --echo: pause -e (Can be used in conjunction with command substitution keypress=$(pause -e) ) 
#  -q, --quiet: pause -q -t10 [Must be used wit timer]
#  
#  The -e option will echo the single key press to the std out for populating variables to be used in
#  case statements, etc.
#
#  GPL3 License: THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#  SOFTWARE. 
 
import time
import sys
import argparse
import select
import tty
import termios
import os
import signal 

# --- Metadata and Descriptions ---
SCRIPT = os.path.basename(sys.argv[0])
VERSION = '5.0.4' # Updated version number
AUTHOR = 'Grawmpy <Grawmpy@gmail.com> (CSPhelps)'
COPYRIGHT = """
GPL3.0 License. Software is intended as free use and is offered 'is is' 
with no implied guarantees or copyrights."""
DESCRIPTION = """
A simple script that interrupts the current process until optional 
timer reaches zero or the user presses any alphanumeric or [Enter] 
key. 

Command will interrupt process indefinitely until user presses any 
alphanumeric key or optional timer reaches [00].

[ seconds are converted to [00h:00m:00s] style format ]
"""
DEFAULT_PROMPT = "Press any key to continue..."
# ---------------------------------

def format_seconds(seconds):
    """Converts seconds into a [DD:HH:MM:SS] style format string."""
    if seconds is None:
        return ""
    
    parts = []
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    
    if days > 0:
        parts.append(f"{days:02d}")
    if hours > 0 or days > 0:
        parts.append(f"{hours:02d}")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes:02d}")
    
    # Seconds are always present
    parts.append(f"{seconds:02d}")

    return ":".join(parts)
def wait_for_key_or_timer(timeout=None, prompt=DEFAULT_PROMPT, response_text=None, quiet=False, echo_key=False):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'
    ERASE_LINE  = '\r\033[K'
    
    pressed_key = None 
    
    try:
        # Set to cbreak mode immediately for both scenarios (timed and indefinite)
        tty.setcbreak(fd)
        start_time = time.time()
        
        sys.stderr.write(HIDE_CURSOR)
        sys.stderr.flush()
        
        # Determine the initial display text based on quiet mode/timer
        if not quiet:
            initial_output = f"{prompt}\r"
            sys.stderr.write(initial_output)
            sys.stderr.flush()

        while True:
            # Use select to check for input with a small delay
            # We must use select because we are now in cbreak mode constantly
            if select.select([sys.stdin], [], [], 0.1)[0]:
                pressed_key = sys.stdin.read(1) # Read ONE character
                
                # Check if the pressed key is [Enter] (Carriage Return)
                if pressed_key == '\r':
                    pressed_key = '\n' # Normalize CR to NL for consistent handling
                
                break # Exit loop immediately on the first keypress

            # --- Timer logic only runs if a timeout was provided ---
            if timeout is not None:
                elapsed_time = time.time() - start_time
                remaining = int(timeout - elapsed_time)

                if remaining <= 0:
                    break # Timer ran out
                
                timer_display = format_seconds(remaining)
                output = f"{ERASE_LINE}[{timer_display}] {prompt}\r"
            
                # Display output if not quiet
                if not quiet:
                    sys.stderr.write(output)
                    sys.stderr.flush()
            # If timeout is None, the loop simply waits for input via select() and the while condition

        # Clear final prompt line
        sys.stderr.write(ERASE_LINE)
        sys.stderr.flush()

    finally:
        # Restore original terminal settings in all cases
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        # Show the cursor again
        sys.stderr.write(SHOW_CURSOR)
        sys.stderr.flush()

    # --- Handle Post-Exit Logic (Outside the try...finally block) ---
    if response_text:
        sys.stderr.write(f"{response_text}\n")
        sys.stderr.flush()
    
    if echo_key and pressed_key is not None:
        # This now echoes *only* the single character captured, without a prompt echo
        sys.stdout.write(pressed_key)
        sys.stdout.flush()

def main():
    full_epilog = f"""
Default prompt: {DEFAULT_PROMPT}

Usage:
{SCRIPT} [-p|--prompt ] [-t|--timer ] [-r|--response ] [-h|--help] [-q|--quiet] [-e|--echo]

    -p, --prompt    [ input required (string must be in quotes) ]
    -t, --timer     [ number of seconds ]
    -r, --response  [ requires text (string must be in quotes) ]
    -e, --echo      [ echoes the key pressed to stdout if present. ]
    -h, --help      [ this information ]
    -q, --quiet     [ quiets text, requires timer be set. ]

Examples:
Input:  $ {SCRIPT}
Output: $ {DEFAULT_PROMPT}

Input:  $ {SCRIPT} -t <seconds>
Output: $ [timer] {DEFAULT_PROMPT}

Input:  $ {SCRIPT} --prompt "Optional Prompt" --response "Your response"
Output: $ Optional Prompt
        $ Your Response

Input:  $ {SCRIPT} -p "Optional Prompt" -r "Your response"

Author: {AUTHOR}
{COPYRIGHT}
"""

    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=full_epilog
    )

    parser.add_argument('-t', '--timer', type=int, help='Number of seconds to wait.')
    parser.add_argument('-p', '--prompt', type=str, default=DEFAULT_PROMPT, help='Custom prompt message.')
    parser.add_argument('-r', '--response', type=str, help='Requires text to be displayed after interruption.')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiets text, implicitly requires timer be set.')
    parser.add_argument('-e', '--echo', action='store_true', help='Echoes the key pressed to stdout if present.')
    parser.add_argument('--version', action='version', version=f'%(prog)s v{VERSION}')
    
    # FIX: Moved this line up so 'args' is defined before the subsequent logic checks
    args = parser.parse_args() 

    # Logic checks as per original bash script
    if args.quiet and not args.timer:
        print("Error: Timer must be set when using --quiet mode.")
        sys.exit(1)

    wait_for_key_or_timer(
        timeout=args.timer,
        prompt=args.prompt,
        response_text=args.response,
        quiet=args.quiet,
        echo_key=args.echo
    )
    sys.exit(0)

if __name__ == "__main__":
    # Check if we are running interactively, which is required for termios
    if not sys.stdin.isatty():
        print("This script requires an interactive terminal to function properly.")
        sys.exit(1)
        
    main()
