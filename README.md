SMDesigner - Structure mutation designr

    SMDesigner make mutation automatical for conserved rna structure. 
    It make minimum muations to district structure which affect RNA's 
    function. SMDesigner work based on consence structure feature of RNA.
    SMDesigner select the basepair to make mutation according the number
    and position of covariation mutation, the length of stem. Then it 
    make two type of mutation for each sequence, one is distript mutation
    another is restory mutation.

------------------------------------------------------------------------
SMDesigner Install

Before install SMDesigner, make sure you have gcc, if not you can use below
command: 
    xcode-select --install
    xcrun --version 

SMDesigner Install successful in the anaconda enviroment of the mac os system
and ......

SMDesigner dependent infernal and R2R. 
    Install infernal using a package manager:
        If you are using Debian, you can install with:
            sudo apt-get install infernal infernal-doc
        Bioconda package, thanks to Björn Grüning. If you have conda, you can install with:
            conda install -c bioconda infernal
        Homebrew Science package. With homebrew, you can install with
            brew tap brewsci/bio
            brew install infernal
    R2R install at the same time with SMDesigner. But is there is error, you need to install
    seperiatlly.

SMDesigner packed by setup tools, you can use pip to install.
    download SMDesigner-1.0.0.tar.gz
    pip install SMDesigner-1.0.0.tar.gz

------------------------------------------------------------------------
Run test
    