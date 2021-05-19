import cv2
import os
import numpy as np
import time

import matplotlib.pyplot as plt
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


def process(frame, rst_dir, frame_idx):
    """
    Color Equations: 
        https://blog.csdn.net/lxw907304340/article/details/46437953

    Colour-science:
        https://github.com/colour-science/colour
    """
 

    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    filename = '%s/%03d_CIE.png'%(rst_dir, frame_idx)
    print('\t\tsave CIE: ', filename)

    settings = Structure(
        **{
        'standalone': True, 
        'filename': filename
         })

    colour.plotting.plot_RGB_chromaticities_in_chromaticity_diagram_CIE1931(
        RGB, 'ITU-R BT.709',
        colourspaces=['ACEScg', 'S-Gamut', 'Pointer Gamut'], 
        **settings)

    result = cv2.imread(filename)

    return result
  
    
 
def main():
    video_file = "./data/huoguo.mp4"

    rst_dir = os.path.splitext(video_file)[0]
    os.makedirs(rst_dir, exist_ok=True)
 
    cap1 = cv2.VideoCapture(video_file)

    # get size and fps of video
    width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 2#cap1.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2') 


    # create VideoWriter for saving 
    video_name = os.path.splitext(os.path.split(video_file)[1])[0]
    result_video = '%s/%s.avi'%(rst_dir, video_name)
    print('\tsave to : ', result_video)
    outVideo = cv2.VideoWriter(result_video, fourcc, fps, (640, 640)) 
 
 
    frame_idx = 0
    start_idx = 10
    stop_idx = 60
    while 1:
        if not cap1.isOpened():
            print('cannot open video %s\n'%(video_file))
        else:
            # get a frame
            flag, frame = cap1.read() 
            #show_img(frame, 'frame')

            
            if not flag: 
                print('->No frame was captured.')
                break
            else:  
                print('->frame: ', frame_idx)
                # process
                if frame_idx > start_idx and frame_idx < stop_idx:
                    t0 = time.time()
                    result = process(frame, rst_dir, frame_idx)
                    td = time.time() - t0 
 
                    # show  
                    cv2.imshow('origin', frame)
                    cv2.imshow('CIE', result)

                    # save 
                    filename = '%s/%03d_bgr.png'%(rst_dir, frame_idx)
                    print('\t\tsave BGR: ', filename)
                    cv2.imwrite(filename, frame)

                    keyvalue = cv2.waitKey(1)
                    if keyvalue == ord('q'):
                        break 

                    # write result
                    outVideo.write(result)
                    frame_idx += 1
   
                else:
                    # index ++
                    frame_idx += 1
                    continue

 
    cap1.release() 
    outVideo.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main() 
