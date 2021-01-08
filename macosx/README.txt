This folder contains a Mac OS X PackageMaker document, allowing freesteam to be packaged
for use on Mac OS X. This package has not been extensively tested across different OS X
versions.

For this document to work, you need to

cd ~/freesteam
scons INSTALL_PREFIX=/usr/local
scons INSTALL_ROOT=~/freesteam/temp_install install

Then open freesteam.pmdoc using PackageMaker, and build and run.

The package currently contains the Python language bindings but not the ASCEND bindings.

-- 
John Pye
========================================

Following comments from Nicholas Mos detail how SVN r677 freesteam can be got
working on OSX 10.8.2 with some help from the Homebrew package management/SCM
system.
----------------------------------------

In the meantime, here are my notes that show what I did to get this to work. I hope it helps other people to get this to work. Again, this is for OS X 10.8.2 with a Homebrew install and Homebrew Python, and it works with SVN revision 677 of the freesteam directory.

# Be sure to install gtk+, ascend, pkg-config, (and maybe some others; I can't remember) before continuing.

# If swig is installed, uninstall it:
$ brew uninstall swig

$ cd /usr/local

# Now we need to install swig-2.0.4
/usr/local $ git checkout -b swig-2.0.4 0d8d92bfcd00f42d6af777ba8bf548cbd5502638

# pcre is a dependency of swig-2.0.4, but the pcre-8.12 is no longer available on ftp.csx.cam.ac.uk. It is still available on SourceForge:
/usr/local $ wget http://downloads.sourceforge.net/project/pcre/pcre/8.12/pcre-8.12.tar.bz2 -O ~/Library/Caches/Homebrew pcre-8.12.tar.bz2

/usr/local $ brew install swig

$ git checkout master

$ git branch -d swig-2.0.4

$ brew link swig

$ cd ~

# Download freesteam from the SVN trunk:
$ svn co http://freesteam.svn.sourceforge.net/svnroot/freesteam/trunk freesteam-2.1

# Download the patch that I made and patch SConstruct and python/SConscript with it (the patch was for revision 677):
$ wget https://gist.github.com/raw/4661001/3b881864bd3723b44d2864f4a9200efc8e85d47d/freesteam-2.1.patch
$ patch -p0 < freesteam-2.1.patch

$ cd freesteam-2.1

$ export PKG_CONFIG_PATH=/usr/X11/lib/pkgconfig:$PKG_CONFIG_PATH

# Compile:
$ scons gtk python ascend

# Install:
$ mkdir -p /usr/local/Cellar/freesteam/2.1
$ scons install INSTALL_PREFIX=/usr/local/Cellar/freesteam/2.1

# Link it up in Homebrew:
$ brew link freesteam
