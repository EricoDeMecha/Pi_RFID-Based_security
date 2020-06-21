## Safe-Laptop

This project uses RFID technology to track and record student's laptop
at both entry and exit of school autonomously, and paperless,at the shortest
time possible.

### Hardware
 RFID-Key Ring ![Key ring Image](https://github.com/EricoDeMecha/Pi_RFID-Based_security/blob/master/data/img/key_ring.jpg)
  125KHz
  
 RFID card ![card](https://github.com/EricoDeMecha/Pi_RFID-Based_security/blob/master/data/img/RFID_tags.png)
 13Mhz
 
 RFID reader ![reader](https://github.com/EricoDeMecha/Pi_RFID-Based_security/blob/master/data/img/card_reader.jpg)
 
 Raspbery pi ![pi](https://github.com/EricoDeMecha/Pi_RFID-Based_security/blob/master/data/img/Raspberry_pi.jpg)
 
 A breadboard and just a bunch of jumper wires
 
 ### Detailed project description 
 
 * Students register their details 
 ![write App](https://github.com/EricoDeMecha/Pi_RFID-Based_security/blob/master/data/img/writeApp.jpg)
 
 * All the information from the above interface is saved in the main database.
 
 * Key and card names are written digitally to the key ring and the card tag respectively.
 
 * Student carries the key ring and the card tag is attached permanently to the student's laptop
 
 * At the gate, scanner_1 which only detect cards, automatically detects student's laptop
 even while in the bag. 
            ![display](https://github.com/EricoDeMecha/Pi_RFID-Based_security/blob/master/data/img/displayApp.jpg)
           
 * The system's program pulls students data from the main database based on data from the detected card
 and stores the data in a temporary database. If the card_data isn't recognized and card is
 displayed as unrecognized.
 
 * Student then swipes the low frequency key ring on scanner_2. The system's program then
 matches the key data with the data in the temporary database. 
 
 * If found, the verification is complete, else the key data is displayed as unrecognized.