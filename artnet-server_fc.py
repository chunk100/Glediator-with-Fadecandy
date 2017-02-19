# Art-Net protocol for Fadecandy
#Adapted from artnet Unicorn hat implementation

#Fadecandy stuff
import opc, time

#Artnet stuff
from twisted.internet import protocol, endpoints
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

#Initialise Fadecandy stuff
numLEDs = 158#for a 10x15 grid, 2 x 60 LEDs per channel, 1 x 30 LEDs
client = opc.Client('localhost:7890')
black = (0, 0, 0)

#pixel mapping for 10 x 15 grid for Fadecandy
#top left is x=1, y=1, bottom right is x=10, y=15.  NOte that list reference will be (y,x)!

gridarray = [ [0],
            [0, 14, 15, 44, 45, 78, 79, 108, 109, 142, 143],
            [0, 13, 16, 43, 46, 77, 80, 107, 110, 141, 144],
            [0, 12, 17, 42, 47, 76, 81, 106, 111, 140, 145],
            [0, 11, 18, 41, 48, 75, 82, 105, 112, 139, 146],
            [0, 10, 19, 40, 49, 74, 83, 104, 113, 138, 147],
            [0, 9, 20, 39, 50, 73, 84, 103, 114, 137, 148],
            [0, 8, 21, 38, 51, 72, 85, 102, 115, 136, 149],
            [0, 7, 22, 37, 52, 71, 86, 101, 116, 135, 150],
            [0, 6, 23, 36, 53, 70, 87, 100, 117, 134, 151],
            [0, 5, 24, 35, 54, 69, 88, 99, 118, 133, 152],
            [0, 4, 25, 34, 55, 68, 89, 98, 119, 132, 153],
            [0, 3, 26, 33, 56, 67, 90, 97, 120, 131, 154],
            [0, 2, 27, 32, 57, 66, 91, 96, 121, 130, 155],
            [0, 1, 28, 31, 58, 65, 92, 95, 122, 129, 156],
            [0, 0, 29, 30, 59, 64, 93, 94, 123, 128, 157]]

class ArtNet(DatagramProtocol):

    def datagramReceived(self, data, (host, port)):
        if ((len(data) > 18) and (data[0:8] == "Art-Net\x00")):
            rawbytes = map(ord, data)
            opcode = rawbytes[8] + (rawbytes[9] << 8)
            protocolVersion = (rawbytes[10] << 8) + rawbytes[11]
            if ((opcode == 0x5000) and (protocolVersion >= 14)):
                sequence = rawbytes[12]
                physical = rawbytes[13]
                sub_net = (rawbytes[14] & 0xF0) >> 4
                universe = rawbytes[14] & 0x0F
                net = rawbytes[15]
                rgb_length = (rawbytes[16] << 8) + rawbytes[17]
                #print "seq %d phy %d sub_net %d uni %d net %d len %d" % \
                #    (sequence, physical, sub_net, universe, net, rgb_length)
                idx = 18
                #Note my grid runs from x=1-10, y=1-15
                x = 1
                y = 1
                pixels = [ black ] * numLEDs # sets the pixels array to 157 entries of (0,0,0)
                while ((idx < (rgb_length+18)) and (y < 16)):
                    #print(rawbytes[idx])
                    r = rawbytes[idx]
                    idx += 1
                    g = rawbytes[idx]
                    idx += 1
                    b = rawbytes[idx]
                    idx += 1
                    #print("x= " + str(x) + ", y=" + str(y) + " r=" + str(r) + ", g=" + str(g) + "b= " +str(b))
                    pixels[gridarray[y][x]] = (r, g, b)
                    x += 1
                    if (x > 10):
                        x = 1
                        y += 1
                client.put_pixels(pixels)


reactor.listenUDP(6454, ArtNet())
reactor.run()
