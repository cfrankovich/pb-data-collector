# PB Data Collector

## How To Use
Clone the repository, input your email and password in the `YOURPBKEYS.txt` file, input links to scrape in `links.txt`, and run the program. 

The program assumes all links are clothing or fashion related items. There has not been any testing on non-clothing items.

## Options
**--page-sleep-time=[INTEGER]**

Wait time before each action. 
Recommended to set this to a high value if a slower computer is being used. 
Default value is 5 seconds. 
Input value is in seconds.

**--captcha-sleep-time=[INTEGER]**

Wait time before continuing on with login. 
This value allows time to enter captcha so the program can login to continue. 
Default value is 5 seconds. 
Input value is in seconds.

**--list-delimiter=[STRING]**

List delimiter being used for the output. 
List values like color and size are output into one "cell" in the csv file. 
To recognize the start and end of the items, a delimiter is used.
Default is "<>".

**--output=[STRING]**

Changes the output file name.
Default is `output.csv`.

