"""Harwin LTek Footprint generator



This file can also be imported as a module and contains the following
functions:

    * fileExists - is used to error check for files that already exist
     ask if it should be overwritten 
    * main - Is used to generate the appropriate class members and 
    then print them to a file
"""

import argparse

import io
#example using unix LF f=io.open('file.txt','w', newline='\n')


class HarwinLtekFootprint:
    """
    A class for making Harwin LTek footprints

    '''
    Attributes
    -----------
    pins : int
        An integer number of pins (Default 2)
    rows : int
        Number of Rows (Default 1)
    pitch : double
        Pin pitch in mm (Default 2.00mm)
    vert : bool
        If true then the part is Vertical else Right Angle
    strain : bool
        If true add strain relief clips else don't
    smd : bool
        If true SMD pads will be returned instead of TH pad
    thPinDim : List of doubles 
        Pin Dimensions th
    smdPadDim : List of doubles
        list of doubles defining the SMD Pad dimensions
    strainPinDim = list of doubles
        list of doubles defining the pad dimensions for
    partName : str
        The part name string
    ioFile : io
        The file object where the file is to be saved
    padString : String
        A formated string to fill out the pin information

    Methods
    ----------
    partName()
        returns the formatted partname string
    description()
        returns the descr line of the model
    strainRelief()
        returns the strings for the strain relief if self.strain == true else returns ""
    printPins()
        returns the pad locations for the part
    printFootPrint()
        Returns the footprint file text for the whole footprint
    printOutline()
        returns the outline and silkscreen information
    printModel()
        Returns the model string line
    setPadDim(padDim)
        Sets the pad Dimensions for either SMD or TH
    setStrainPad(padDim)
        Sets Strain pad dimensions
    """

    partName = "Harwin_LTek-Male_{pins}"
    thPinDim = [1.35, 1.35, 0.8]
    smdPadDim = [1.00, 3.20]
    strainPinDim = [1.5, 1.5, 0.95]
    padString = "(pad {padID} {thSMD} {padShape} (at {xCoord} {yCoord}) (size {xSize} {ySize}) {drill} (layers {layers}))"



    def __init__(self, pins=2, rows=1, pitch=2.00, vert = True, strain = True, smd = False ) -> None:
        """
        Parameters
        ----------

        pins : int
            An integer number of pins (Default 2)
        rows : int
            Number of Rows (Default 1)
        pitch : double
            Pin pitch in mm (Default 2.00mm)
        vert : bool
            If true then the part is Vertical else Right Angle
        strain : bool
            If true add strain relief clips else don't
        smd : bool
            If true SMD pads will be returned instead of TH pad
        myFile : str list
            This is a list of strings that would make up the contents of the footprint file
        """
        self.pins = pins
        self.rows = rows
        self.pitch = pitch
        self.vert = vert
        self.strain = strain
        self.smd = smd

    def printPins(self):
        """
        Prints the pin/pad lines for the footprint with Pin 1 at 0,0 and pins folowing the pattern defined by Harwin positive of 0,0
        returns a python list of strings

        Parameters
        ----------
        None

        Raises
        ------
        Non valid connector row configuartions

        Returns
        -------
        myPins
            A list of strings for all of the pads/pins
        """

        i = 0
        myPins = []
        myPadShape = "rect"
        if self.smd:
            myTH = "smd"
            myLayers = "F.Cu F.Paste F.Mask"
            myPinsNum = self.pins
            if self.rows == 2:
                myPinsNum = self.pins/2 #since there are 2 rows each row has half the pins.
                myPins.append(self.padString.format(padID= str(i+1), thSMD=myTH, padShape=myPadShape, xCoord= str(0.00), yCoord= str(0.00), xSize=str(self.thPinDim[0]), ySize=str(self.thPinDim[1]), drill= "(drill " + str(self.thPinDim[2]) + ") ", layers=myLayers))
                myPins.append(self.padString.format(padID= str(myPinsNum+i+1), thSMD=myTH, padShape=myPadShape, xCoord= str(0.00), yCoord= str(self.pitch), xSize=str(self.thPinDim[0]), ySize=str(self.thPinDim[1]), drill= "(drill " + str(self.thPinDim[2]) + ") ", layers=myLayers))
            else:    
                raise Exception('SMD vertical Harwin LTek connectors should only have 2 rows and not have {} row(s)'.format(self.pins))
                
            while i < myPinsNum:  # Populate the pads for SMD Vertical parts
                myXCoord = (float(i) * self.pitch)
                myPins.append(self.padString.format(padID= str(i+1), thSMD=myTH, padShape=myPadShape, xCoord= str(myXCoord), yCoord= str(0.00), xSize=str(self.thPinDim[0]), ySize=str(self.thPinDim[1]), drill= "(drill " + str(self.thPinDim[2]) + ") ", layers=myLayers))
                if self.rows == 2:
                    myPins.append(self.padString.format(padID= str(myPinsNum+i+1), thSMD=myTH, padShape=myPadShape, xCoord= str(0.00), yCoord= str(self.pitch), xSize=str(self.thPinDim[0]), ySize=str(self.thPinDim[1]), drill= "(drill " + str(self.thPinDim[2]) + ") ", layers=myLayers))
                i += 1
            
            if self.strain:
                #add the strain relief for vertical connectors
                myXCoordStrainPlus = mXCoord + 2.25 #myXCoord is still the last pin from the above while loop
                myXCoordStrainMinus = -2.25
                myYCoordStrainPlus = 4.75/2.0
                myYCoordStrainMinus = -1.0*(4.75/2.0)
                myPins.append(self.padString.format(padID= "\"\"", thSMD="thru_hole", padShape=myPadShape, xCoord= str(myXCoordStrainMinus), yCoord= str(myYCoordStrainPlus), xSize=str(self.strainPinDim[0]), ySize=str(self.strainPinDim[1]), drill= "(drill " + str(self.strainPinDim[2]) + ") ", layers=myLayers))
                myPins.append(self.padString.format(padID= "\"\"", thSMD="thru_hole", padShape=myPadShape, xCoord= str(myXCoordStrainMinus), yCoord= str(myYCoordStrainMinus), xSize=str(self.strainPinDim[0]), ySize=str(self.strainPinDim[1]), drill= "(drill " + str(self.strainPinDim[2]) + ") ", layers=myLayers))
                myPins.append(self.padString.format(padID= "\"\"", thSMD="thru_hole", padShape=myPadShape, xCoord= str(myXCoordStrainPlus), yCoord= str(myYCoordStrainPlus), xSize=str(self.strainPinDim[0]), ySize=str(self.strainPinDim[1]), drill= "(drill " + str(self.strainPinDim[2]) + ") ", layers=myLayers))
                myPins.append(self.padString.format(padID= "\"\"", thSMD="thru_hole", padShape=myPadShape, xCoord= str(myXCoordStrainPlus), yCoord= str(myYCoordStrainMinus), xSize=str(self.strainPinDim[0]), ySize=str(self.strainPinDim[1]), drill= "(drill " + str(self.strainPinDim[2]) + ") ", layers=myLayers))
            #End of SMD Vertical Connectors    
        else: #We have a through Hole part and need to treat it accordingly as pins instead of pads
            myTH = "thru_hole"
            myLayers = "*.Cu *.Mask"
            myPinsNum = self.pins
            myPins.append(self.padString.format(padID= str(i+1), thSMD=myTH, padShape=myPadShape, xCoord= str(0.00), yCoord= str(0.00), xSize=str(self.thPinDim[0]), ySize=str(self.thPinDim[1]), drill= "(drill " + str(self.thPinDim[2]) + ") ", layers=myLayers))
            myPadShape  = "circle"
            if self.rows == 2:
                myPinsNum = self.pins/2 #since there are 2 rows each row has half the pins.
                myPins.append(self.padString.format(padID= str(myPinsNum+i+1), thSMD=myTH, padShape=myPadShape, xCoord= str(0.00), yCoord= str(self.pitch), xSize=str(self.thPinDim[0]), ySize=str(self.thPinDim[1]), drill= "(drill " + str(self.thPinDim[2]) + ") ", layers=myLayers))
                

            while i < myPinsNum:  # Populate the pin pads for TH Vertical parts
                myXCoord = (float(i) * self.pitch)
                myPins.append(self.padString.format(padID= str(i+1), thSMD=myTH, padShape=myPadShape, xCoord= str(myXCoord), yCoord= str(0.00), xSize=str(self.thPinDim[0]), ySize=str(self.thPinDim[1]), drill= "(drill " + str(self.thPinDim[2]) + ") ", layers=myLayers))
                if self.rows == 2:
                    myPins.append(self.padString.format(padID= str(myPinsNum+i+1), thSMD=myTH, padShape=myPadShape, xCoord= str(0.00), yCoord= str(self.pitch), xSize=str(self.thPinDim[0]), ySize=str(self.thPinDim[1]), drill= "(drill " + str(self.thPinDim[2]) + ") ", layers=myLayers))
                i += 1
            
            if self.strain:
                #add the strain relief for vertical connectors
                myXCoordStrainPlus = mXCoord + 2.25 #myXCoord is still the last pin from the above while loop
                myXCoordStrainMinus = -2.25
                myYCoordStrainPlus = 4.75/2.0
                myYCoordStrainMinus = -1.0*(4.75/2.0)
                myPins.append(self.padString.format(padID= "\"\"", thSMD="thru_hole", padShape="circle", xCoord= str(myXCoordStrainMinus), yCoord= str(myYCoordStrainPlus), xSize=str(self.strainPinDim[0]), ySize=str(self.strainPinDim[1]), drill= "(drill " + str(self.strainPinDim[2]) + ") ", layers=myLayers))
                myPins.append(self.padString.format(padID= "\"\"", thSMD="thru_hole", padShape="circle", xCoord= str(myXCoordStrainMinus), yCoord= str(myYCoordStrainMinus), xSize=str(self.strainPinDim[0]), ySize=str(self.strainPinDim[1]), drill= "(drill " + str(self.strainPinDim[2]) + ") ", layers=myLayers))
                myPins.append(self.padString.format(padID= "\"\"", thSMD="thru_hole", padShape="circle", xCoord= str(myXCoordStrainPlus), yCoord= str(myYCoordStrainPlus), xSize=str(self.strainPinDim[0]), ySize=str(self.strainPinDim[1]), drill= "(drill " + str(self.strainPinDim[2]) + ") ", layers=myLayers))
                myPins.append(self.padString.format(padID= "\"\"", thSMD="thru_hole", padShape="circle", xCoord= str(myXCoordStrainPlus), yCoord= str(myYCoordStrainMinus), xSize=str(self.strainPinDim[0]), ySize=str(self.strainPinDim[1]), drill= "(drill " + str(self.strainPinDim[2]) + ") ", layers=myLayers))
                


        return myPins





def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input_file',
        type=str,
        help="The spreadsheet file to pring the columns of"
    )
    args = parser.parse_args()
    get_spreadsheet_cols(args.input_file, print_cols=True)


if __name__ == "__main__":
    main()
    

