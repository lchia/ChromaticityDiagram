import cv2
import os
import numpy as np 
import colour


class Structure(dict):
    """
    Defines a dict-like object allowing to access key values using dot syntax.
    Other Parameters
    ----------------
    \\*args : list, optional
        Arguments.
    \\**kwargs : dict, optional
        Key / Value pairs.
    Methods
    -------
    -   :meth:`~colour.utilities.Structure.__init__`
    References
    ----------
    :cite:`Mansencald`
    Examples
    --------
    >>> person = Structure(first_name='John', last_name='Doe', gender='male')
    >>> person.first_name
    'John'
    >>> sorted(person.keys())
    ['first_name', 'gender', 'last_name']
    >>> person['gender']
    'male'
    """

    def __init__(self, *args, **kwargs):
        super(Structure, self).__init__(*args, **kwargs)
        self.__dict__ = self


def process(frame, filename):
    """
    Color Equations: 
        https://blog.csdn.net/lxw907304340/article/details/46437953

    Colour-science:
        https://github.com/colour-science/colour
    """
 

    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    settings = Structure(
        **{
        'standalone': True, 
        'filename': filename
         })

    colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(
        RGB, 'ITU-R BT.709',
        colourspaces=['ACEScg', 'S-Gamut', 'Pointer Gamut'], 
        **settings)

 
def ChromaticityDiagram(video_file):
 
    rst_dir = './ChromaticityDiagram'
    os.makedirs(rst_dir, exist_ok=True)
 
    cap1 = cv2.VideoCapture(video_file)
  
    frame_idx = 0
    start_idx = 10
    stop_idx = 60
    while 1:
        if not cap1.isOpened():
            print('\t>> ChromaticityDiagram: Cannot open video %s\n'%(video_file))
        else:
            # get a frame
            flag, frame = cap1.read()  
 
            if not flag: 
                print('\t>> ChromaticityDiagram: Video opened, no frame was captured, frame_idx = %d'%(frame_idx))
                break
            else:
                # process  
                filename = '%s/%d.png'%(rst_dir, frame_idx) 
                process(frame, filename) 
 
                keyvalue = cv2.waitKey(1)
                if keyvalue == ord('q'):
                    break 

                # write result 
                frame_idx += 1
     
    cap1.release()




if __name__ == '__main__':
    # test
    video_file = "./huoguo.mp4"

    ChromaticityDiagram(video_file) 

