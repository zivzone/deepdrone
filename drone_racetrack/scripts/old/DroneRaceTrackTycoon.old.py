#!/usr/bin/env python
# -*- coding: utf-8 -*-



'____ TO DO ____'

# - Random keyframes [ ]
# - Metrics as input in GUI [ ]

'____ \TO DO ____'



'____ IMPORT MODULES ____'

import numpy as np
import os
dirname = os.path.dirname(__file__)

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

from PIL import Image, ImageTk

from scipy.spatial.transform import Rotation

from trajectory_generation import *

'____ \IMPORT MODULES ____'



'____ GENERIC TKINTER CLASSES ____'

class LabeledFrame:
    # Tkinter class: 
    # Empty Frame with label.
    
    def LabeledFrame(self, master, label):
        
        # Frame
        frame = tk.Frame(master)
        frame.pack()

        # Label
        label = tk.Label(frame, text=label)
        label.pack(anchor=tk.W)
        
        return frame



class SingleSelectionButtonsFrame( LabeledFrame ):
    # Tkinter class: 
    # Frame which contains multiple buttons.
    # Only one button can be selected at one time.

    def __init__( self, master, name, label='Label', sel_but=0, raised_icons=[], sunken_icons=[], icon_size=(10, 10) ):
        
        # For inheritance of this class
        if not hasattr(self, 'ssb_frames'):
            self.ssb_frames = {}
        
        # An own sub dictionary for this frame
        self.ssb_frames[ name ] = {
            'frame'         :   self.LabeledFrame( master, label ),
            'n_but'         :   len(sunken_icons),
            'sel_but'       :   sel_but,
        }

        self.ssb_frames[ name ][ 'icons' ] = self.SSB_Icons( 
            name, 
            raised_icons, 
            sunken_icons, 
            icon_size
        )

        self.ssb_frames[ name ][ 'buts' ] = self.SSB_Buttons( name )


    def SSB_Icons( self, name, raised_icons, sunken_icons, icon_size ):
        # This function loads the icons of the buttons.
        # raised_icons and sunken_icons are lists containing relative path to images
        # icon size for example (100, 100)

        for ind_icon in range( self.ssb_frames[ name ][ 'n_but' ] ):

            # Load image
            loaded_image = Image.open(
                os.path.join( dirname, raised_icons[ ind_icon ] )
            )
            # Scale the image to the righ size
            loaded_image.thumbnail(
                icon_size, 
                Image.ANTIALIAS
            )
            # Overwrite path with corresponding icon
            raised_icons[ ind_icon ] = ImageTk.PhotoImage( loaded_image )
            
            # Load image
            loaded_image = Image.open(
                os.path.join( dirname, sunken_icons[ ind_icon ] )
            )
            # Scale the image to the righ size
            loaded_image.thumbnail(
                icon_size, 
                Image.ANTIALIAS
            )
            # Overwrite path with corresponding icon
            sunken_icons[ ind_icon ] = ImageTk.PhotoImage( loaded_image )

        # dictionary with buttons, true for raised, false for sunken
        icons = {
            True    :   raised_icons,
            False   :   sunken_icons,
        }

        return icons


    def SSB_Buttons( self, name ):

        # Create empty list for the buttons
        buttons = []

        # For every direction button
        for ind_but in range( self.ssb_frames[ name ][ 'n_but' ] ):

            # Each of the Buttons passes its index into the Click function for identification
            button = tk.Button(
                self.ssb_frames[ name ][ 'frame' ], 
                image=self.ssb_frames[ name ][ 'icons' ][ False ][ ind_but ], 
                command=lambda ind_but=ind_but : self.SSB_Click( name, ind_but )
            )
            # Pack Buttons from left to right into the frame
            button.pack( side=tk.LEFT)
            buttons.append(button)

        # Activate the button which is selected as default
        buttons[ self.ssb_frames[ name ][ 'sel_but' ] ].config(
            image=self.ssb_frames[ name ][ 'icons' ][ True ][ self.ssb_frames[ name ][ 'sel_but' ] ],
            relief=tk.SUNKEN
        )
        
        return buttons


    def SSB_Click( self, name, ind_but ):
        
        print("Button #" + str(ind_but) + " is selected.")
        # Turn off previous selected button
        self.ssb_frames[ name ][ 'buts' ][ self.ssb_frames[ name ][ 'sel_but' ] ].config(
            relief=tk.RAISED, 
            image=self.ssb_frames[ name ][ 'icons' ][ False ][ self.ssb_frames[ name ][ 'sel_but' ] ]
        )

        # Update selection
        self.ssb_frames[ name ][ 'sel_but' ] = ind_but

        # Turn on selected button
        self.ssb_frames[ name ][ 'buts' ][ self.ssb_frames[ name ][ 'sel_but' ] ].config(
            relief=tk.SUNKEN, 
            image=self.ssb_frames[ name ][ 'icons' ][ True ][ self.ssb_frames[ name ][ 'sel_but' ] ]
        )



class SingleActionButtonFrame( LabeledFrame ):
    # Tkinter class: 
    # Frame which contains a single button.
    # When being enabled and clicked, this button activates an action.

    def __init__( 
        self, 
        master, 
        name, 
        label='Label', 
        enabled=True, 
        raised_icon=None, 
        sunken_icon=None, 
        icon_size=(10, 10),
        action=None ):

        # standard action
        if action == None:
            action = lambda name=name : self.SAB_Click( name )
        
        # For inheritance of this class
        if not hasattr(self, 'sab_frames'):
            self.sab_frames = {}
        
        # An own sub dictionary for this frame
        self.sab_frames[ name ] = {
            'frame'         :   self.LabeledFrame( master, label ),
            'enabled'       :   enabled
        }

        self.sab_frames[ name ][ 'icons' ] = self.SAB_Icons( 
            raised_icon, 
            sunken_icon, 
            icon_size
        )

        self.sab_frames[ name ][ 'but' ] = self.SAB_Button( name, action )


    def SAB_Icons( self, raised_icon, sunken_icon, icon_size ):
        # This function loads the icons of the button.
        # raised_icon and sunken_icon are relative paths to the image
        # icon size for example (100, 100)

        # Load image
        loaded_image = Image.open(
            os.path.join( dirname, raised_icon )
        )
        # Scale the image to the righ size
        loaded_image.thumbnail(
            icon_size, 
            Image.ANTIALIAS
        )
        # Overwrite path with corresponding icon
        raised_icon = ImageTk.PhotoImage( loaded_image )
        
        # Load image
        loaded_image = Image.open(
            os.path.join( dirname, sunken_icon )
        )
        # Scale the image to the righ size
        loaded_image.thumbnail(
            icon_size, 
            Image.ANTIALIAS
        )
        # Overwrite path with corresponding icon
        sunken_icon = ImageTk.PhotoImage( loaded_image )

        # dictionary with icons, true for raised, false for sunken
        icons = {
            True    :   raised_icon,
            False   :   sunken_icon,
        }

        return icons


    def SAB_Button( self, name, action):

        # Create Button
        button = tk.Button(
            self.sab_frames[ name ][ 'frame' ], 
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ], 
            command=action
        )

        if not self.sab_frames[ name ][ 'enabled' ]:
            button.config( relief=tk.SUNKEN )

        # Pack Button into the frame
        button.pack( side=tk.LEFT )
 
        return button


    def SAB_Click( self, name ):
        
        if self.sab_frames[ name ][ 'enabled' ] == True:
            print("\nAction is activated.")
            # Change the status for visualization
            self.sab_frames[ name ][ 'enabled' ] = False
            self.sab_frames[ name ][ 'but' ].config(
            relief=tk.SUNKEN,
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )
        else:
            print("\nButton is not enabled.")
            # Change the status for visualization
            self.sab_frames[ name ][ 'enabled' ] = True
            self.sab_frames[ name ][ 'but' ].config(
            relief=tk.RAISED,
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )

'____ \GENERIC TKINTER CLASSES ____'



'____ DRONE RACETRACK TKINTER CLASSES ____'

class DRT_DirectionFrame( SingleSelectionButtonsFrame ):
    # Tkinter class:
    # Calls SingleSelectionButtonsFrame with specific arguments
    # Frame containing direction buttons
    
    def __init__(self, master):

        SingleSelectionButtonsFrame.__init__(
            self,
            master,
            'direction',
            label="\n--- Direction ---",
            sel_but=3,
            raised_icons=[
                'img/DirectionFrame/sLeft90.png',
                'img/DirectionFrame/bLeft90.png',
                'img/DirectionFrame/Left45.png',
                'img/DirectionFrame/Straight.png',
                'img/DirectionFrame/Right45.png',
                'img/DirectionFrame/bRight90.png',
                'img/DirectionFrame/sRight90.png'],
            sunken_icons=[
                'img/DirectionFrame/grey_sLeft90.png',
                'img/DirectionFrame/grey_bLeft90.png',
                'img/DirectionFrame/grey_Left45.png',
                'img/DirectionFrame/grey_Straight.png',
                'img/DirectionFrame/grey_Right45.png',
                'img/DirectionFrame/grey_bRight90.png',
                'img/DirectionFrame/grey_sRight90.png'],
            icon_size=(31, 31)
        )



class DRT_SlopeFrame( SingleSelectionButtonsFrame ):
    # Tkinter class:
    # Calls SingleSelectionButtonsFrame with specific arguments
    # Frame containing slope buttons

    def __init__(self, master):

        SingleSelectionButtonsFrame.__init__(
            self,
            master,
            'slope',
            label='\n--- Slope ---',
            sel_but=1,
            raised_icons=[
                'img/SlopeFrame/Downward.png',
                'img/SlopeFrame/Flat.png',
                'img/SlopeFrame/Upward.png'],
            sunken_icons=[
                'img/SlopeFrame/grey_Downward.png',
                'img/SlopeFrame/grey_Flat.png',
                'img/SlopeFrame/grey_Upward.png'],
            icon_size=(80, 80)
        )



class DRT_BuildFrame( SingleActionButtonFrame ):
    # Tkinter class:
    # Calls SingleActionButtonFrame with specific arguments
    # Frame containing build button

    def __init__(self, master):

        name = 'build'

        SingleActionButtonFrame.__init__(
            self,
            master,
            name,
            label='\n--- Build Gate ---',
            enabled=True,
            raised_icon='img/BuildFrame/Gate.png',
            sunken_icon='img/BuildFrame/grey_Gate.png',
            icon_size=(250, 250),
            action=lambda name=name : self.BuildClick( name ) 
        )
        

    def BuildClick( self, name ):

        if self.sab_frames[ name ][ 'enabled' ] == True:
            print("\nGate has been built.")
            # Change the status for visualization
            self.sab_frames[ name ][ 'enabled' ] = False
            self.sab_frames[ name ][ 'but' ].config(
            relief=tk.SUNKEN,
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )
        else:
            print("\nCannot build gate.")
            # Change the status for visualization
            self.sab_frames[ name ][ 'enabled' ] = True
            self.sab_frames[ name ][ 'but' ].config(
            relief=tk.RAISED,
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )



class DRT_WreckFrame( SingleActionButtonFrame ):
    # Tkinter class:
    # Calls SingleActionButtonFrame with specific arguments
    # Frame containing wreck button


    def __init__(self, master):

        name = 'wreck'

        SingleActionButtonFrame.__init__(
            self,
            master,
            name,
            label='\n--- Demolish Gate ---',
            enabled=False,
            raised_icon='img/WreckFrame/WreckingMachine.png',
            sunken_icon='img/WreckFrame/grey_WreckingMachine.png',
            icon_size=(100, 100),
            action=lambda name=name : self.WreckClick( name )
        )
    

    def WreckClick( self, name ):

        if self.sab_frames[ name ][ 'enabled' ] == True:
            print("\nGate has been wrecked.")
            # Change the status for visualization
            self.sab_frames[ name ][ 'enabled' ] = False
            self.sab_frames[ name ][ 'but' ].config(
            relief=tk.SUNKEN,
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )
        else:
            print("\nInitial gate cannot be wrecked.")
            # Change the status for visualization
            self.sab_frames[ name ][ 'enabled' ] = True
            self.sab_frames[ name ][ 'but' ].config(
            relief=tk.RAISED,
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )
    
   

class DRT_TrajectoryFrame( SingleActionButtonFrame ):
    # Tkinter class:
    # Calls SingleActionButtonFrame with specific arguments
    # Frame containing button for trajectory calculation

    def __init__(self, master):

        name = 'traj'

        SingleActionButtonFrame.__init__(
            self,
            master,
            name,
            label='\n--- Compute Trajectory ---',
            enabled=False,
            raised_icon='img/TrajectoryFrame/traj3.png',
            sunken_icon='img/TrajectoryFrame/grey_traj3.png',
            icon_size=(200, 200),
            action=lambda name=name : self.TrajClick( name )
        )

        # self.roundFrame = self.LabeledFrame( self.sab_frames[ 'traj' ][ 'frame' ], 'Number of Rounds: ' )
        # self.roundSpinbox = tk.Spinbox(self.roundFrame, from_=0, to=100, width=3)
        # self.roundSpinbox.pack()
        # self.roundFrame.pack(side=tk.TOP)
    

    def TrajClick( self, name ):

        if self.sab_frames[ name ][ 'enabled' ] == True:
            print("\nTrajectory has been computed.")
            # Change the status for visualization
            self.sab_frames[ name ][ 'enabled' ] = False
            self.sab_frames[ name ][ 'but' ].config(
            relief=tk.SUNKEN,
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )
        else:
            print("\nTrajectory cannot be computed if there is only one gate.")
            # Change the status for visualization
            self.sab_frames[ name ][ 'enabled' ] = True
            self.sab_frames[ name ][ 'but' ].config(
            relief=tk.RAISED,
            image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )



class DRT_CreatorFrame(
    DRT_DirectionFrame, 
    DRT_SlopeFrame, 
    DRT_BuildFrame, 
    DRT_WreckFrame, 
    DRT_TrajectoryFrame):

    def __init__( self, Master ):

        # Initialize GUI
        self.drt_creator_frame = tk.Frame(Master)
        self.drt_creator_frame.pack(side=tk.LEFT)

        DRT_DirectionFrame.__init__(self, self.drt_creator_frame)
        DRT_SlopeFrame.__init__(self, self.drt_creator_frame)
        DRT_BuildFrame.__init__(self, self.drt_creator_frame)
        DRT_WreckFrame.__init__(self, self.drt_creator_frame)
        DRT_TrajectoryFrame.__init__(self, self.drt_creator_frame)

        # Initialize first keyframe at origin
        self.keyframes = {
            'x'         :   [ 0 ],
            'y'         :   [ 0 ],
            'z'         :   [ 0 ],
            'roll'      :   [ 0 ],
            'pitch'     :   [ 0 ],
            'yaw'       :   [ 0 ],
            't'         :   [ 0 ],
            'n'         :     1
        }

        # Relative coordinates to the current keyframe when building a new keyframe         # SET THIS VALUES THROUGH GUI !!!!!
        self.gate_diameter = 1
        self.keyframe_delta = {
            'x'         :   np.array( [   1.50,    3.00,    4.50,    3.00,    4.50,    3.00,    1.50 ] ) * self.gate_diameter,
            'y'         :   np.array( [   0.50,    1.00,    1.50,    0.00,   -1.50,   -1.00,   -0.50 ] ) * self.gate_diameter,
            'z'         :   np.array( [  -1.00,    0.00,    1.00 ] ),
            'roll'      :   np.array( [   0.00 ] ) * self.gate_diameter,
            'pitch'     :   np.array( [   0.00 ] ),
            'yaw'       :   np.array( [   1./6,    1./6,    1./6,    0.00,   -1./6,   -1./6,   -1./6 ] ) * np.pi,
            't'         :   np.array( [   1.00 ] ),
        }

        # Spawn the first keyframe at the origin
        '''
        self.SpawnGateRequest()
        '''
    

    def BuildClick( self, name ):
        # The following happens when the build button is pressed.

        # If the build button is raised
        if self.sab_frames[ name ][ 'enabled' ] == True:

            # Add the next keyframe
            self.AddKeyframe()

            # Now that there is at least one additional keyframe, the wreck button is raised.
            name = 'wreck'
            self.sab_frames[ name ][ 'enabled' ] = True
            self.sab_frames[ name ][ 'but' ].config(
                relief=tk.RAISED,
                image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )

            # Now that there is at least one additional keyframe, the trajectory button is raised.
            name = 'traj'
            self.sab_frames[ name ][ 'enabled' ] = True
            self.sab_frames[ name ][ 'but' ].config(
                relief=tk.RAISED,
                image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
            )

            # Print keyframes on terminal
            print("\nGate has been built.\n\nKeyframes:\n")
            print '\tx:\t', self.keyframes[ 'x' ]
            print '\ty:\t', self.keyframes[ 'y' ]
            print '\tz:\t', self.keyframes[ 'z' ]
            print '\troll:\t', self.keyframes[ 'roll' ]
            print '\tpitch:\t', self.keyframes[ 'pitch' ]
            print '\tyaw:\t', self.keyframes[ 'yaw' ]
            print '\tt:\t', self.keyframes[ 't' ]
            print '\tn:\t', self.keyframes[ 'n' ]
            
        else:
            print("\nCannot build gate.")


    def AddKeyframe( self ):

        # The relative coordinates of the next keyframe
        x_delta = self.keyframe_delta[ 'x' ][ self.ssb_frames[ 'direction' ][ 'sel_but' ] ]
        y_delta = self.keyframe_delta[ 'y' ][ self.ssb_frames[ 'direction' ][ 'sel_but' ] ]
        z_delta = self.keyframe_delta[ 'z' ][ self.ssb_frames[ 'slope' ][ 'sel_but' ] ]

        # Rotate the relative coordinates (x, y, z) of the next keyframe
        # according to the orientation of the current keyframe.
        rot_mat = Rotation.from_euler('xyz', [ self.keyframes[ 'roll' ][ -1 ], self.keyframes[ 'pitch' ][ -1 ], self.keyframes[ 'yaw' ][ -1 ] ]).as_dcm()
        pos_delta = np.matmul( rot_mat, np.array( [x_delta, y_delta, z_delta] )[ :, np.newaxis ] )

        # The absolute coordinates of the next keyframe
        self.keyframes[ 'x' ].append(       self.keyframes[ 'x' ][ -1 ]     +   pos_delta[ 0, 0 ] )
        self.keyframes[ 'y' ].append(       self.keyframes[ 'y' ][ -1 ]     +   pos_delta[ 1, 0 ] )
        self.keyframes[ 'z' ].append(       self.keyframes[ 'z' ][ -1 ]     +   pos_delta[ 2, 0 ] )
        self.keyframes[ 'roll' ].append(    self.keyframes[ 'roll' ][ -1 ]  +   self.keyframe_delta[ 'roll' ][ 0 ]                                          )
        self.keyframes[ 'pitch' ].append(   self.keyframes[ 'pitch' ][ -1 ] +   self.keyframe_delta[ 'pitch' ][ 0 ]                                         )
        self.keyframes[ 'yaw' ].append(     self.keyframes[ 'yaw' ][ -1 ]   +   self.keyframe_delta[ 'yaw' ][ self.ssb_frames[ 'direction' ][ 'sel_but' ] ] )
        self.keyframes[ 't' ].append(       self.keyframes[ 't' ][ -1 ]     +   self.keyframe_delta[ 't' ][ 0 ]                                             )
        self.keyframes[ 'n' ] += 1


    def WreckClick( self, name ):
        # The following happens when the wreck button is pressed:

        # If the wreck button is raised
        if self.sab_frames[ name ][ 'enabled' ] == True:
            
            self.DelKeyframe()
    
            # After wrecking the current gate, if there is only the gate in the
            # origin left, disable the delete button and the trajectory button.
            if self.keyframes[ 'n' ] == 1:

                name = 'wreck'
                self.sab_frames[ name ][ 'enabled' ] = False
                self.sab_frames[ name ][ 'but' ].config(
                    relief=tk.SUNKEN,
                    image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
                )

                name = 'traj'
                self.sab_frames[ name ][ 'enabled' ] = False
                self.sab_frames[ name ][ 'but' ].config(
                    relief=tk.SUNKEN,
                    image=self.sab_frames[ name ][ 'icons' ][ self.sab_frames[ name ][ 'enabled' ] ]
                )

            # Print keyframes on terminal
            print("\nGate has been wrecked.\n\nKeyframes:\n")
            print '\tx:\t', self.keyframes[ 'x' ]
            print '\ty:\t', self.keyframes[ 'y' ]
            print '\tz:\t', self.keyframes[ 'z' ]
            print '\troll:\t', self.keyframes[ 'roll' ]
            print '\tpitch:\t', self.keyframes[ 'pitch' ]
            print '\tyaw:\t', self.keyframes[ 'yaw' ]
            print '\tt:\t', self.keyframes[ 't' ]
            print '\tn:\t', self.keyframes[ 'n' ]

        else:
            print("\nInitial gate cannot be wrecked.")

    
    def DelKeyframe( self ):

        # Delete the coordinates of the current gate
        for coord in [ 'x', 'y', 'z', 'roll', 'pitch', 'yaw', 't' ]:
            del self.keyframes[ coord ][ -1 ]
        self.keyframes[ 'n' ] -= 1


    def TrajClick( self, name ):
        # The following happens when the trajectory button is pressed:

        if self.sab_frames[ name ][ 'enabled' ] == True:
            
            # Initialize trajectory instance
            trajectory = Trajectory(
                x       =   self.keyframes[ 'x'     ],
                y       =   self.keyframes[ 'y'     ],
                z       =   self.keyframes[ 'z'     ],
                roll    =   self.keyframes[ 'roll'  ],
                pitch   =   self.keyframes[ 'pitch' ],
                yaw     =   self.keyframes[ 'yaw'   ],
                t       =   self.keyframes[ 't'     ],
                rounds  =   False
            )

            # Calculate minimum snap trajectory
            trajectory.MinSnapTraj(6, solver='gurobi')
            print("\nTrajectory has been computed.")

        else:
            print("\nTrajectory cannot be computed if there is only one gate.")

'____ \DRONE RACETRACK TKINTER CLASSES ____'



'____ MAIN ____'

if __name__ == '__main__':

    # *** WINDOW ***
    root = tk.Tk()
    #drt_direction_frame = DRT_DirectionFrame(root)
    drt_creator_frame = DRT_CreatorFrame(root)
    # Keep window continuosly open until close button pressed
    root.mainloop()

'____ \MAIN ____'