import sys
import logging
import re
import os

from optparse import OptionParser

SCRIPT = os.path.basename(__file__)

def GetEventIdsFromFile(file):
    event_ids = None
    
    #get eventids from file and strip the newline chars
    with open(file) as f:
        event_ids = f.readlines()
        
    return [id.strip() for id in event_ids]

def AddPrefix(event_ids, prefix):
    return [('{0}{1}'.format(prefix,id)) for id in event_ids]
 
def AddSuffix(event_ids, suffix):
    return [('{0}{1}'.format(id,suffix)) for id in event_ids]

def AssertRegexMatch(pattern, id):
    if re.search(pattern, id) is None:
        return False
        
    return True
    
def GetRawId(data, prefix, suffix):
    raw_id = data
    
    if prefix:
        raw_id = raw_id.lstrip(prefix)
    if suffix:
        raw_id = raw_id.rstrip(suffix)
        
    return raw_id

#GetTestedEvents: returns (passed,failed) list tuple
#can be used by outside callers in case of use as non-independent tool
def GetTestedEvents(event_ids, expr, prefix=None,suffix=None):
    passed = [] #list of passed event ids
    failed = [] #list of failed event ids
    
    for id in event_ids:
        raw_id = GetRawId(id, prefix, suffix)
        
        if AssertRegexMatch(expr, id):
            #test passed in here
            passed.append(raw_id)
        else:
            #test failed in here
            failed.append(raw_id)
    
def main(args):
    if args[0].debug:
        logging.EnableDebug(True)
        logging.Message('DEBUG', 'Debugging has been enabled')

    expr = args[0].regex
    file = args[0].file
    
    logging.Message('DEBUG', 'Using file:\n\t%s' % file)
    logging.Message('DEBUG', 'Using regex:\n\t%s' % expr)
    logging.Message('DEBUG', 'Using prefix:\n\t"%s"' % args[0].prefix)
    logging.Message('DEBUG', 'Using suffix:\n\t"%s"' % args[0].suffix)
    
    event_ids = GetEventIdsFromFile(file) 
    
    if event_ids is None:
        logging.Message('ERROR', 'Error - file could not be opened')
        sys.exit(-1)
    else:    
        logging.Message('STATUS', 'Loaded [%s] event ids to test' % len(event_ids))
        
    #if we have a prefix, let's add it
    if args[0].prefix:
        logging.Message('PROGRESS', 'Prefix detected - adding: "%s"' % args[0].prefix)
        event_ids = AddPrefix(event_ids, args[0].prefix)
        logging.Message('STATUS', 'Prefix added to event ids')
        
    if args[0].suffix:
        logging.Message('PROGRESS', 'Suffix detected - adding: "%s"' % args[0].suffix)
        event_ids = AddSuffix(event_ids, args[0].suffix)
        logging.Message('STATUS', 'Suffix added to event ids')

    logging.Message('PROGRESS', 'Running assertion test against regex...')
        
    logging.Message('PROGRESS','{0:12}{1}'.format('Event ID', 'Status'))
    logging.Message('PROGRESS','{0:12}{1}'.format('--------', '------'))
    
    passed = 0
    failed = 0
    
    for id in event_ids:
        raw_id = GetRawId(id, args[0].prefix, args[0].suffix)
        
        if AssertRegexMatch(expr, id):
            #test passed in here
            if not args[0].fail:
                logging.Message('STATUS', '{0:12}{1}'.format(raw_id, 'TEST PASSED'))
            passed += 1
        else:
            #test failed in here
            logging.Message('STATUS', '{0:12}{1}'.format(raw_id, 'TEST FAILED'))
            failed += 1
    
    logging.Message('PROGRESS', '') #just for the new line
    logging.Message('PROGRESS', '{0:<14}{1}'.format('Total Tests:', (passed + failed)))
    logging.Message('PROGRESS', '{0:<14}{1}'.format('Passed:', passed))
    logging.Message('PROGRESS', '{0:<14}{1}'.format('Failed:', failed))
    logging.Message('PROGRESS', '') #just for the new line
        
# This is to modify the behaviour of the OptParser to make it check arguments
# more strictly
class NonCorrectingOptionParser(OptionParser):

    def _match_long_opt(self, opt):
        # Is there an exact match?
        if opt in self._long_opt:
            return opt
        else:
            self.error('"{0}" is not a valid command line option.'.format(opt))
    
# This method return the parser to parse our command line arguments.
USAGE_MESSAGE = ("Type 'python %s --help' for usage." % SCRIPT)

def get_parser():
    parser = NonCorrectingOptionParser(add_help_option=False)

    parser.add_option('-h', '--help', help='Show help message',
                      action='store_true')
    parser.add_option('-r', '--regex',
                      help='Regex required to test. Required',
                      action='store')
    parser.add_option('-f','--file',
                      help='File containting lines that are to be tested. Required',
                      action='store')
    parser.add_option('-p','--prefix',
                      help='Prefix to put infront of each line to be tested.',
                      action='store')
    parser.add_option('-s','--suffix',
                      help='Suffix to put after each line to be tested.',
                      action='store')
    parser.add_option('--fail',
                    help='Show only when a test fails. Default False',
                    action='store_true')
    parser.add_option('-d', '--debug',
                      help='Enable debugger print messages. Default False',
                      action='store_true')
                      
    return parser
    
def print_help(parser):
    print(parser.format_help().strip())
    print('\nExample query:\n python %s --regex "(?:4656|466[03])" ' % SCRIPT +
          '--file "eventids.txt" --prefix " EventID=" --suffix " "')
          
def ValidateInput(args):
    #if we have regex and a file, we can go
    if args[0].regex and args[0].file:
        return True

    #no matches passed above
    return False

def ArgEntry():
    #setup/parse the command line input
    parser = get_parser()
    args = parser.parse_args()

    if args[0].debug:
        logging.EnableDebug()
    
    if args[0].help:
        print_help(parser)
    elif not sys.argv[1:] or not ValidateInput(args):
        print(USAGE_MESSAGE + '\n')
    else:
        main(args)
        ExitMessage()

def ExitMessage():
    logging.Message('STATUS', '{0:<10}{1}'.format('Author:', 'Steven Bremner'))
    logging.Message('STATUS', '{0:<10}{1}'.format('Date:', 'May 13, 2015'))
    logging.Message('STATUS', 'Thank you for using %s by SteveInternals' % SCRIPT)
        
if __name__ == '__main__':
    try:
        ArgEntry()
    except KeyboardInterrupt:
        # quit
        print()
        logging.Message('ERROR', 'User sent keyboard interrupt - exiting')
        ExitMessage()
        sys.exit()