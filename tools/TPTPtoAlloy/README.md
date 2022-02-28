# TPTPtoAlloy

The purpose of this utility is to translate tptp files to Alloy.  
Note that it cannot translate files containing quoted identifiers. Neither single-quoted strings used as identifiers nor double-quoted strings used as distinct objects.

## Usage

It can be run with "./gradlew run path_to_tptp_file scope".  
For example, "./gradlew run ../TPTP-v7.4.0/Problems/HWV/HWV083+1.p 15" translates HWV083+1.p into the Alloy language and adds a command with domain size 15.

## Acknowledgement

Some TPTP files publicly available on the TPTP Problem Library(http://www.tptp.org/) are used for unit tests.
