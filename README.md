# com.castsoftware.uc.hraccess

This extension excludes COBOL quality rules violations that are part of HR Access generated code.

Only COBOL quality rule violation that is part of a non generated code block will be kept: which means only the UTTB paragraphs. 

Example : 
>	000006 UTTBPUUU-JA0U63IN-FK.                                            TBPUUU 

>	000007           IF    UJA-FLG-PU = 1                                   TBPUUU 
	000008           NEXT SENTENCE ELSE GO TO UTTBPUUU-JA0U63IN-FK-FN.      TBPUUU 
	000009     MOVE        UJA-0-ZYU6-POSADM TO                             TBPUUU 
	000010                 UJA-4-ZYU6-POSADM                                TBPUUU 
	000011     MOVE        UJA-0-ZYU6-CODTRA TO                             TBPUUU 
  	000012                 UJA-4-ZYU6-CODTRA                                TBPUUU 
  	000013     MOVE        UJA-0-ZYU6-CODINC TO                             TBPUUU 
  	000014                 UJA-4-ZYU6-CODINC                                TBPUUU 
  	000015     MOVE        UJA-0-ZYU6-CATEG1 TO                             TBPUUU 
  	000016                 UJA-4-ZYU6-CATEG1                                TBPUUU 
  	000017     MOVE        UJA-0-ZYU6-CATEG2 TO                             TBPUUU 
  	000018                 UJA-4-ZYU6-CATEG2.                               TBPUUU 
  	000019 UTTBPUUU-JA0U63IN-FK-FN.    EXIT.                                TBPUUU 


This only applies to COBOL quality rules with bookmarks so:

* Avoid using HANDLE CONDITION
* Avoid using IGNORE CONDITION
* Avoid using HANDLE ABEND
* Using SEARCH ALL only with sorted data
* Avoid using SORT
* Avoid using MERGE
* Avoid using ALTER
* Avoid using PERFORM ... THROUGH | THRU
* Avoid STOP RUN (use GOBACK instead)
* Avoid DISPLAY ... UPON CONSOLE
* Avoid Procedure Paragraphs that contains no statements
* Avoid Procedure Sections that contain no Paragraphs.
* Avoid using Sections in the PROCEDURE DIVISION (use Paragraphs only)
* Avoid using NEXT SENTENCE
* Include a WHEN OTHER clause when using EVALUATE
* Avoid using MOVE CORRESPONDING ... TO ...
* Avoid undocumented Sections
* Avoid undocumented Paragraphs
* Avoid using GOTO statement
* Avoid OPEN/CLOSE inside loops
* EVALUATE statements must be closed by END-EVALUATE
* Avoid recursive calls with PERFORM statements
* Avoid GOTO jumps out of PERFORM range
* Avoid cyclic calls with PERFORM statements
* Avoid unreferenced Sections and Paragraphs
* Avoid using Pointers
* IF statements must be closed by END-IF
* File descriptor block must be defined with 0 record
* When using binary data items (COMP), then use the SYNCHRONIZED clause
* Avoid using inline PERFORM with too many lines of code
* Subprograms called multiple times should be called statically
* Never use incompatible statements with the CICS environment
* Avoid using nested programs
* Avoid accessing data by using the position and length
* Programs accessing relational databases must include the SQLCA copybook
* Avoid executing multiple OPEN statements
* Never truncate data in MOVE statements
* Avoid unchecked return code (SQLCODE) after EXEC SQL query
* Each opened file must be closed
* Avoid calling the same paragraph with PERFORM and GO TO statements
* Files should be declared with a FILE-STATUS
* Sections and paragraphs should be located after the first statement calling them
* Avoid using COMPUTE statement for elementary arithmetic operation
* Avoid using READ statement without AT END clause
* Check alphanumeric data before moving them into numeric data
* Variables defined in Working-Storage section must be initialized before to be read
