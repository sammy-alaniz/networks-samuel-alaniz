# HELO¤<screen_name>¤<IP>¤<Port>\n

import messages
import tcp

if "__main__" == __name__:
    tcp.send_message(messages.hello_message("John","localhost","50123"),61616)