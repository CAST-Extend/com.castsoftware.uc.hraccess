# com.castsoftware.uc.hraccess

This extension excludes COBOL quality rules violations that are part of HR Access generated code.

Only COBOL quality rule violation that is part of a non generated code block will be kept: which means only the UTTB paragraphs. 

Example : 

![UTTB Paragraph](/UTTB_paragraph.jpg)

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



CAST dashboard before extension use : 
TBD


CAST dashboard after extension use : 
TBD 



