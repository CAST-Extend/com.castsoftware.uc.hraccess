import cast_upgrade_1_5_9 # @UnusedImport
from cast.application import ApplicationLevelExtension, open_source_file, Bookmark #@UnresolvedImport
import logging
import re


def is_begin(line):
    """
    Return true if the line is the beginning of a user code section
    """
    filter1 = re.compile("[0-9]{6}[ \*]UTTB[A-Z0-9]{4}\-[A-Z0-9]{8}\-[A-Z0-9]{2}\.")
    # example : 000323 UTTBPUUU-JA029Z3B-HD.  
    return filter1.match(line) 

def is_end(line):
    """
    Return true if the line is the end of a user code section
    """
    filter1 = re.compile("[0-9]{6}[ \*]UTTB[A-Z0-9]{4}\-[A-Z0-9]{8}\-[A-Z0-9]{2}\-FN")  
    # example : 000331 UTTBPUUU-JA029Z3B-HA-FN 
    return filter1.match(line) 


def get_properties(application):
    """
    Gives all Cobol properties corresponding to bookmarked quality rules
    
    @todo : should probably depend on CAIP version by using : application.get_caip_version()
    """

    properties = [138954, 138955, 138953, 138951, 138910, 138901,
                  138899, 138906, 138911, 138947, 139222, 138904, 138909,
                  138948, 138959, 138902, 139323, 139322, 138900,
                  139020, 138950, 139139, 138589, 139122, 139335,
                  139166, 138949, 138991, 139045, 139321, 139320,
                  138994, 138997, 138907, 139258, 138903, 138594,
                  138995, 139171, 139369, 138998, 139145,
                  138996, 138908, 139405, 139414, 
                  ]
    
    #properties = [138995,]   # diag 5690 

    
    return properties


class FilterViolations(ApplicationLevelExtension):

    def end_application(self, application):
        
        logging.info("Filtering violations")
        
        # All Cobol properties corresponding to bookmarked quality rules
        properties = get_properties(application)
        
        # 1. register each property as handled by this plugin : we will rewrite them
        for prop in properties:
            application.declare_property_ownership(prop, 'CAST_COBOL_SavedProgram')
        
        number_of_programs = 0
        number_of_cobol_programs = 0 
        number_of_cobol_copybooks = 0 
        number_of_hra_programs = 0
        number_of_violations = 0
        number_of_kept_violations = 0
        hra_LOC = 0 
        total_LOC = 0 
        
        for program in application.objects().has_type('CAST_COBOL_SavedProgram').load_violations(properties):
            
            # 1. get the violations for that program
            
            # a Cobol violation can be in a copybook, we group violations per file
            violations_per_file = {}
            number_of_programs += 1
            is_hra = False
            
            for prop in properties:
                
                for violation in program.get_violations(prop):
                    
                    _file = violation[1].file
                    if _file not in violations_per_file:
                        violations_per_file[_file] = []
                    
                    violations_per_file[_file].append(violation)
            
            # 2. filter the violations  that are in user code
            user_code_violations = []
            
            for _file, violations in violations_per_file.items():
                
                if program != _file: 
                    #CobolFileType = 'CopyBook'     # we are in a Copybook 
                    number_of_cobol_copybooks += 1 
                else: 
                    #CobolFileType = 'Program'    # we are not in the program not a Copybook 
                    number_of_cobol_programs += 1

                # open the file, get the 'user code bookmarks'
                # those are the 'bookmarks' that represent the user code  
                bookmarks = []
                
                with open_source_file(_file.get_path()) as f:

                    #logging.info('current file (%s) =[ %s ] ' % (CobolFileType, _file.get_path()))

                    begin_line = 0
                    current_line = 0
                    number_of_hra_LOC_in_current_file = 0 
                    
                    for line in f:
                        current_line += 1
                        
                        if is_begin(line):
                            # store current portion begin
                            #logging.info('begin_line =[ %s ] ' % (line))
                            begin_line = current_line
                        elif is_end(line):
                            # add a user code bookmark
                            end_line = current_line 
                            bookmark = Bookmark(_file, 
                                                begin_line,
                                                1,
                                                current_line, -1)
                            
                            #logging.info('end_line =[ %s ] ' % (line))
                            #logging.info('bookmark file =[ %s ], begin_line = %s end_line = %s ' % (_file, begin_line, end_line))
                            
                            bookmarks.append(bookmark)
                            is_hra = True
                            number_of_hra_LOC_in_current_file += (end_line - begin_line +1) 

                # filter the violations that reside in at least one 'user code bookmark'
                for violation in violations:
                    
                    number_of_violations += 1
                    
                    for bookmark in bookmarks:
                        # use of contains operator
                        if bookmark.contains(violation[1]):
                            user_code_violations.append(violation)
                            break
                    if not bookmarks:
                        # case where we do not have any marker : keep all violations : maybe we are not in HR Access environment
                        user_code_violations.append(violation)
            
                if (number_of_hra_LOC_in_current_file != 0):
                    logging.info('Number of customer code LOC in current file [%s]: %s on a total of %s LOC' % (_file.get_path(), number_of_hra_LOC_in_current_file, current_line))
                    total_LOC += current_line
                    hra_LOC += number_of_hra_LOC_in_current_file
                else: 
                    logging.info('File [%s] does not contain any customer code, file LOC = %s' % (_file.get_path(), current_line))
                    total_LOC += current_line

            if is_hra:
                number_of_hra_programs += 1             
            
            # 3. save back user_code_violations
            for violation in user_code_violations:
                
                number_of_kept_violations += 1
                
                # violation 'format' is almost directly usable as parameter   
                program.save_violation(violation[0], violation[1], violation[2])
                
            # et hop !
            
        if (total_LOC > 0): 
            logging.info('Found %s HR Access programs out of %s programs and %s copybooks' % (number_of_hra_programs, number_of_programs, number_of_cobol_copybooks))
            logging.info('Kept %s violation bookmarks out of %s' % (number_of_kept_violations, number_of_violations))
            logging.info('Number of HR Access LOC : %s on a total of %s LOC, which means %s percent of generated LOC' % (hra_LOC, total_LOC, round(hra_LOC*100/total_LOC,2)))
            logging.info("Done filtering violations")
        else: 
            logging.info('*** No Cobol files analyzed, so no HR Access code to filter')        
        
        
