# Glediator-with-Fadecandy

There are 3 parts to the Glediator implementation

1.	Fadecandy board, attached to the Raspberry Pi
2.	Raspberry Pi.  Connected to local network and Raspberry Pi.  This acts as an artnet node
3.	Another computer on the same network with Glediator installed and running.  Also needs the .gled file configured for the grid and the IP address of the artnet node (2)

# Raspberry Pi

- Fadecandy files need to be installed and demonstrated to be working with the python examples.  Start the Fadecandy server in a Terminal:

  sudo fcserver
- To set up the Pi as an artnet node, need to work through some of the setup for the [Unicorn Hat example](https://github.com/bbx10/artnet-unicorn-hat) (unicorn hat uses python neopixels library, not Fadecandy).  Install python twisted :

  sudo apt-get install python-twisted

- The artnet-server_fc.py program acts as an artnet node and also a method of transferring the incoming information to fadecandy.  Mine has been set up for a 10x15 grid with Fadecandy  pixels numbers referenced in a list to make it easier.  This will need to be edited to each individuals grid to ensure the x and y values are appropriate

- The following command runs the Art-Net server turning the Pi into an Art-Net node. Many programs can send LED values to an Art-Net node. Glediator is one such program.  In another Terminal, type:

   sudo python artnet-server_fc.py
    
- The Raspberry Pi is now running as an artnet-node, ready to talk to Fadecandy.  You will also need to know the IP address of the Raspberry Pi for the next stage

#Another computer on the same network
This will run Glediator so download it from the website and ensure it will run correctly.  It should just double click on a Windows machine, linux is java –jar Gladiator.jar

Now for the slightly tricky bit.  Again, this was helped by the [Unicorn Hat implementation](https://github.com/bbx10/artnet-unicorn-hat)

- First thing to get right is the Glediator artnet patch.  This needs to be configured for grid size and Raspberry Pi IP address.  It is possible to do this from within Glediator but when I tried, it would not accept my settings.  There is another example [here](https://github.com/bbx10/artnet-unicorn-hat).  I don’t claim to understand all this but it worked.  First of all copy this into a text file and modify the bits in bold

\#GLEDIATOR Patch File

Patch_Matrix_Size_X=**grid x dimension**

Patch_Matrix_Size_Y=**grid y dimension**

Patch_Num_Unis=1

Patch_Uni_ID_0_IP1=**Raspberry Pi IP address part 1**

Patch_Uni_ID_0_IP2=**Raspberry Pi IP address part 2**

Patch_Uni_ID_0_IP3=**Raspberry Pi IP address part 3**

Patch_Uni_ID_0_IP4=**Raspberry Pi IP address part 4**

Patch_Uni_ID_0_Net_Nr=0

Patch_Uni_ID_0_Sub_Net_Nr=0

Patch_Uni_ID_0_Uni_Nr=1

Patch_Uni_ID_0_Num_Ch=**Number which is 3x the number of pixels**

- Then, each pixel needs to be assigned a channel for red green and blue plus another unique line.  I wrote some code to do this as for 150 pixels, that makes 600 entries.  For each pixel add the following, on the next line (modifying the bits in bold)

Patch_Pixel_X_0_Y_0_Ch_R=**Channel no -> start at zero!**

Patch_Pixel_X_0_Y_0_Ch_G=**Channel no +1**

Patch_Pixel_X_0_Y_0_Ch_B=**Channel no+2**

Patch_Pixel_X_0_Y_0_Uni_ID=0

- Repeat for all pixels, ensuring the channel number increases each time.  For my 150 pixels, the last channel number was 449 (as we start at 1).  This numbering is important to ensure the decoding by the Raspberry Pi sends the information to the correct pixel.

- Save the file as something obvious with a .gled extension (it doesn’t matter, just makes it easier to identify it)

- At the Glediator main screen, select Options -> Matrix Size and enter appropriate values for the grid (x is number of horizontal pixels, y is vertical).  NOTE the grid coordinates are (0,0) at the top left.

- Then select Options -> Output
- First select Mapping Mode : Single_Pixels
- Then select Output Mode : Artnet
- Ignore the rest of the screen but in the bottom right click on ‘Patch ArtNet/TMP2.NET
- Select the Load button and open the .gled patch file just created.  This should populate the screen with a map of your grid, showing the unique channels for each RGB of each pixel.  It should also have the correct IP address of the Raspberry Pi.
- Select ‘Apply Changes’
- Stand back, make sure everything is on, take a deep breath and select ‘Open Socket’
- Things should look awesome.

For me, this implementation is a bit clunky as the Pi will happily run Glediator on its own but is being used simply as an Artnet node to drive the Fadecandy.  Having to use another computer is a bit of a pain but at least it works.

Its also tricky if the Pi IP address is not static as having to change the IP address in the Artnet patch file is a bit of a pain.
