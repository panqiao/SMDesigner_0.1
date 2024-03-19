SMDesigner - Structure mutation designer

    SMDesigner automates mutation for conserved RNA structures, ensuring minimal 
    alterations to disrupt the structure, which can affect RNA function. SMDesigner 
    work is based on the consences structure feature of RNA. SMDesigner chooses 
    base pairs for mutation based on the number and position of covariation mutations, 
    as well as the stem's length. Then it makes two types of mutation for each 
    sequence, one is disruptive mutation another is restorative mutation.

------------------------------------------------------------------------
SMDesigner Install

SMDesigner comes with setup tools and can be installed using pip:

    Download the package SMDesigner-1.0.0.tar.gz.
    Install it using pip with the command: pip install SMDesigner-1.0.0.tar.gz.
    
For more details, refer to the README_INSTALL.md file.

------------------------------------------------------------------------
SMDesigner test running

To run a test after installing SMDesigner using the command pip install SMDesigner-1.0.0.tar.gz, 
follow these steps:

    1. Open your command line interface.
    2. Type 'SMDesigner' to launch the program.
    3. Then, type 'test' to run a default test.
------------------------------------------------------------------------
SMDesigner running the sample

After successfully running a test in SMDesigner and seeing the output "test finished," 
you can proceed to run your own sample data by following these steps:

    1. Type 'SMDesigner' to launch the program again.
    2. Type the path to your sample folder to run your sample data. For example, if your sample
    data is located in a folder named sample_data in the directory 
    'C:\Users\YourName\Documents', 
    you should type 
    'C:\Users\YourName\Documents\sample_data'.

Drawing the secondary structure for each sequence with flag --–run-r2r.
    1. Type 'SMDesigner --run-r2r' to launch the program with flag function
    2. Type the 'test' or '<the path to your sample folder>'


    
    
