Download the package file from:
 https://github.com/lilihou/SMDesigner_0.1/blob/main/dist/SMDesigner-1.0.0.tar.gz

System requirements

    Operating system: 
      SMDesigner is written in Python, but it requires the external software R2R, which is written in C and Perl. Therefore, this program needs to be run on UNIX, Linux, or MacOS systems.
     
    Compiler: 
      Since the R2R source code is written in C and Perl, you will need the GNU C compiler (gcc) and the C++ compiler (g++). Ensure your PATH environmental variable includes a directory with a Perl executable.
    
Dependencies:

      R2R (Weinberg and Breaker, 2011) (for marking RNA structure feature),
      the Infernal library package (http://eddylab.org/infernal/), this is required by R2R.

SMDesigner has been test successful UNIX and MacOS system.

Using SMDesigner with R2R Software: 

    if you already have R2R installed on your computer: 
      you could download the package, Unzip the package, and run dirrectly ./SMDesigner/ python SMDsigner3_test.py.
    if you didn't have R2R: 
      There is automatic install program to install r2r in SMDesigner when you first run program. Becaused of the r2r need special environment to install, this may be not work for some computer. if so, you need to install r2r by yourself, you can refer to:
      https://sourceforge.net/projects/weinberg-r2r/


Below are two example to install SMDesigner successful:
MAC os system:

    1.check if system has gcc(GNU Compiler Collection) and g++(GNU C++ Compiler):
        gcc --version
        g++ --version
      if not installed, install using below command:
        open terminal;
        type 'xcode-select --install' and press enter;
        install follow the guide on screen
    2.check if system has autoconf and automake:
        autoconf --version
        automake --version
      if not installed, install using homebrew:
        brew install autoconf
        brew install automake
      if you don't have homebrew, install it first:
        open terminal, copy and past below command:
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    3.In anaconda(conda 23.3.1) environment:
        when you install anaconda(choose one fit Inter chips), when you open terminal, it supposed in base environment, you can did follow below instruction; if not, you can create a new environment: 
          conda create --name myenv
          conda activate myenv
        3.1 install infernal which is needed by r2r if you didn't have:
          conda install -c bioconda infernal
        3.2 install python
          conda install python=3.x
        3.3 install SMDesigner
          cd path(SMDesigner-1.0.0.tar.gz located)
          pip install SMDesigner-1.0.0.tar.gz
            if it show 'Successfully installed SMDesigner-1.0.0':
              type 'SMDesigner'
               this command will test if you have r2r, if not, it will help install; if r2r has been installed, it will start test.
              type'test'
               this will show you if SMDesigner worked and what the output looks like. if it output 'test finished', you can 
              type 'SMDesigner':
               input your sample folder name with path, after runing, you will get your result.

    debug:
    1.if you have problem to install infernal:
        1.1 check if Anaconda installation is optimized for Apple's M1 (ARM architecture) or Intel (x86_64 architecture) chips on macOS:
            conda info | grep platform
            if output is platform : osx-64, that's correct; if not, you will have problem install infernal with conda. You can install infernal by yourself and you can refer: http://eddylab.org/infernal/

Ubuntu 20.04.4 LTS (GNU/Linux 5.15.146.1-microsoft-standard-WSL2 x86_64):

    1.check if system has gcc(GNU Compiler Collection) and g++(GNU C++ Compiler):
        gcc --version
        g++ --version
      if not installed, install using below command:
        open terminal;
        sudo apt update
        sudo apt install build-essential
        
    2.check if system has autoconf and automake:
        autoconf --version
        automake --version
      if not installed, install using sudo apt:
        sudo apt install autoconf
        sudo apt install automake
    3.
      3.1 install python
          conda install python=3.x
      3.2 
      







