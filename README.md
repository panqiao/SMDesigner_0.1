SMDesigner - Structure mutation designer

    SMDesigner makes mutation automatic for conserved RNA structure. 
    It makes minimum mutations to district structure which affect RNA's 
    function. SMDesigner work is based on the consences structure feature of RNA.
    SMDesigner selects the base pair to make mutation according to the number
    and position of covariation mutation, the length of the stem. Then it 
    makes two types of mutation for each sequence, one is distript mutation
    another is restory mutation.

------------------------------------------------------------------------
SMDesigner Install

Before installing SMDesigner, make sure you have gcc, if not you can use below
command: 
    xcode-select --install
    xcrun --version 

SMDesigner Install successfully in the Anaconda environment of the Mac OS system
and ......

SMDesigner dependent infernal and R2R. 
    Install infernal using a package manager:
        If you are using Debian, you can install it with:
            sudo apt-get install infernal infernal-doc
        Bioconda package, thanks to Björn Grüning. If you have conda, you can install with:
            conda install -c bioconda infernal
        Homebrew Science package. With homebrew, you can install it with
            brew tap brewsci/bio
            brew install infernal
    R2R install at the same time with SMDesigner. But if there is an error, you need to install
    seperiatlly.

SMDesigner is packed with setup tools, you can use pip to install.
    download SMDesigner-1.0.0.tar.gz
    pip install SMDesigner-1.0.0.tar.gz

------------------------------------------------------------------------
Run test
    
