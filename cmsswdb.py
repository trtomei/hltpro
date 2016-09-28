#! /usr/bin/env python

import os,sys,socket
import shutil
import optparse             # use optparse instead of argarse to maintain compatibility with python 2.6
import ConfigParser
import cx_Oracle


class CmsswDB(object):

    def __init__(self, database = None):
        self.command = os.path.basename(sys.argv[0])
        self.config  = os.path.expanduser('/nfshome0/hltpro/.cmsswdb')
        try:
            config = ConfigParser.SafeConfigParser()
            config.readfp(open(self.config))
            user     = config.get('cmsswdb', 'user')
            password = config.get('cmsswdb', 'password')
            dsn      = config.get('cmsswdb', 'dsn')
            if database == 'INT2R':
                dsn = config.get('cmsswdb', 'INT2Rdsn')
        except:
            print '%(command)s: error reading the configuration from %(config)s: %(error)s' % { 'command': self.command, 'config': self.config, 'error': str(sys.exc_value) }
            sys.exit(1)
        try:
            self.connection = cx_Oracle.connect(user, password, dsn)
        except cx_Oracle.DatabaseError as e:
            print '%(command)s: error connecting to database for writing: %(error)s' % { 'command': self.command, 'error': str(e) }
            sys.exit(1)


    def list_releases(self, subsystem = None):
        cursor = self.connection.cursor()
        if not subsystem:
            query = "select DAQ_TYPE,ARCH,CMSSW_REL from CMS_HLT_GDR.HLT_CMSSW_ARCH"
        else:
            query = "select DAQ_TYPE,ARCH,CMSSW_REL from CMS_HLT_GDR.HLT_CMSSW_ARCH where DAQ_TYPE='%(subsystem)s'" % { 'subsystem': subsystem }

        cursor.execute(query)
        releases = cursor.fetchall()
        cursor.close()

        for (subsystem, architecture, release) in sorted(releases):
            print '%-24s%-24s%-24s' % (subsystem, architecture, release)


    def check_release(self, subsystem, architecture, release):
        cursor = self.connection.cursor()
        query = "select DAQ_TYPE,ARCH,CMSSW_REL from CMS_HLT_GDR.HLT_CMSSW_ARCH where DAQ_TYPE='%(subsystem)s' and ARCH='%(architecture)s' and CMSSW_REL='%(release)s'" % \
                { 'release': release, 'architecture': architecture, 'subsystem': subsystem }

        cursor.execute(query)
        releases = cursor.fetchall()
        cursor.close()

        if not releases:
            return False
        else:
            return True


    def add_release(self, subsystem, architecture, release):
        if self.check_release(subsystem, architecture, release):
            print 'Warning: the release "%(release)s" is already listed for the software architecture "%(architecture)s" on the subsystem "%(subsystem)s"' % \
                { 'release': release, 'architecture': architecture, 'subsystem': subsystem }
            return True

        cursor = self.connection.cursor()
        query = "insert into CMS_HLT_GDR.HLT_CMSSW_ARCH values('%(subsystem)s', '%(release)s', '%(architecture)s')" % \
                { 'release': release, 'architecture': architecture, 'subsystem': subsystem }
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

        if self.check_release(subsystem, architecture, release):
            return True
        else:
            print '%(command)s: error: failed to add the release "%(release)s" for the software architecture "%(architecture)s" from the subsystem "%(subsystem)s"' % \
                { 'command': self.command, 'release': release, 'architecture': architecture, 'subsystem': subsystem }
            return False


    def remove_release(self, subsystem, architecture, release):
        if not self.check_release(subsystem, architecture, release):
            print 'Warning: the release "%(release)s" is not listed for the software architecture "%(architecture)s" on the subsystem "%(subsystem)s"' % \
                { 'release': release, 'architecture': architecture, 'subsystem': subsystem }
            return True

        cursor = self.connection.cursor()
        query = "delete from CMS_HLT_GDR.HLT_CMSSW_ARCH where DAQ_TYPE='%(subsystem)s' and CMSSW_REL='%(release)s' and ARCH='%(architecture)s'" % \
                { 'release': release, 'architecture': architecture, 'subsystem': subsystem }
        cursor.execute(query)
        self.connection.commit()
        cursor.close()

        if not self.check_release(subsystem, architecture, release):
            return True
        else:
            print '%(command)s: error: failed to remove the release "%(release)s" for the software architecture "%(architecture)s" from the subsystem "%(subsystem)s"' % \
                { 'command': self.command, 'release': release, 'architecture': architecture, 'subsystem': subsystem }
            return False


def print_help():
    command = os.path.basename(sys.argv[0])
    print """Maintain the list of CMSSW releases in the database for the various subsystems and software architectures.

Usage:
    %(command)s [-s SUBSYSTEM] list 

        Print all releases listed in the database. If a SUBSYSTEM is specified, print the releases for that SUBSYSTEM,
        otherwise print the releases for all SUBSYSTEMs.


    %(command)s -s SUBSYSTEM -a SCRAM_ARCH check CMSSW_VERSION

        Check if the release CMSSW_VERSION is available for the architecture SCRAM_ARCH on the given SUBSYSTEM.


    %(command)s -s SUBSYSTEM -a SCRAM_ARCH add CMSSW_VERSION

        Try to add release CMSSW_VERSION for the architecture SCRAM_ARCH on the given SUBSYSTEM to the database.


    %(command)s -s SUBSYSTEM -a SCRAM_ARCH remove CMSSW_VERSION

        Try to remove release CMSSW_VERSION for the architecture SCRAM_ARCH on the given SUBSYSTEM from the database.


    %(command)s [--help]

        Print this message, and exit.

""" % {'command': command}


def main():
    command = os.path.basename(sys.argv[0])

    parser = optparse.OptionParser(add_help_option = False)
    parser.enable_interspersed_args()
    parser.add_option('-s', '--subsystem')
    parser.add_option('-a', '--architecture')
    parser.add_option('-h', '--help')
    parser.add_option('-d', '--database')
    parser.set_usage(optparse.SUPPRESS_USAGE)   # suppress the default usage message
    (options, args) = parser.parse_args()

    actions = {
        'list': 0,
        'check': 1,
        'add': 1,
        'remove' : 1,
    }

    if options.help:
        print_help()
        sys.exit(0)

    if len(args) == 0 or len(args) > 2:
        print_help()
        sys.exit(2)

    db = CmsswDB(options.database)

    action = args[0]
    if action not in actions:
        print '%(command)s: error: invalid action "%(action)s"' % { 'command': command, 'action': action }
        sys.exit(2)

    if len(args) == 1:
        if actions[action] != 0:
            print '%(command)s: error: "%(action)s" action requires a RELEASE argument' % { 'command': command, 'action': action }
            sys.exit(2)
        if action == 'list':
            if options.architecture:
                print '%(command)s: error: the "list" action does not support the "-a" or "--architecture" option' % { 'command': command }
                sys.exit(2)
            if options.subsystem:
                db.list_releases(options.subsystem)
                sys.exit(0)
            else:
                db.list_releases()
                sys.exit(0)

    if len(args) == 2:
        if actions[action] != 1:
            print '%(command)s: error: the "%(action)s" action does not support a RELEASE argument' % { 'command': command, 'action': action }
            sys.exit(2)
        if not options.subsystem:
            print '%(command)s: error: the "%(action)s" action requires a "-s" or "--subsystem" option' % { 'command': command, 'action': action }
            sys.exit(2)
        if not options.subsystem:
            print '%(command)s: error: the "%(action)s" action requires a "-a" or "--architecture" option' % { 'command': command, 'action': action }
            sys.exit(2)
        
        release = args[1]

        if action == 'check':
            ret = db.check_release(options.subsystem, options.architecture, release)
        elif action == 'add':
            ret = db.add_release(options.subsystem, options.architecture, release)
        elif action == 'remove':
            ret = db.remove_release(options.subsystem, options.architecture, release)

        if ret:
            sys.exit(0)
        else:
            sys.exit(1)
            


if __name__ == '__main__':
    main()
