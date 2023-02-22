Pseudorange, Doppler, and carrier phase observables produced by processing the
TEXBAT data sets via the UT GRID/pprx receiver are available in the
subdirectories of this directory.  The format for each type of Matlab .mat
file is described in the .txt files available here:

http://radionavlab.ae.utexas.edu/datastore/satNavCourse/

For example, the format of channel.mat is described by channeldef.txt.

Note that when loading the data into Matlab, you must take the transpose of
the matrix that gets loaded; e.g., 

channelData = load('channel.mat');
channelData = channelData';

Then the columns of channelData will be as described in channeldef.txt.
