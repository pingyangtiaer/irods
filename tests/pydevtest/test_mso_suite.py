import time
import sys
import shutil
import os
if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest
import socket
import commands
import os
import datetime
import time

from resource_suite import ResourceBase
from pydevtest_common import get_irods_top_level_dir, get_irods_config_dir
import pydevtest_common
import pydevtest_sessions


RODSHOME = "/home/irodstest/irodsfromsvn/iRODS"
ABSPATHTESTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
RODSHOME = ABSPATHTESTDIR + "/../../iRODS"

class Test_MSOSuite(ResourceBase, unittest.TestCase):
    def setUp(self):
        super(Test_MSOSuite, self).setUp()
        hostname = pydevtest_common.get_hostname()
        self.admin.assert_icommand("iadmin modresc demoResc name origResc", 'STDOUT', 'rename', stdin_string='yes\n')
        self.admin.assert_icommand("iadmin mkresc demoResc compound", 'STDOUT', 'compound')
        self.admin.assert_icommand("iadmin mkresc cacheResc 'unixfilesystem' " + hostname + ":" + get_irods_top_level_dir() + "/cacheRescVault", 'STDOUT', 'unixfilesystem')
        self.admin.assert_icommand("iadmin mkresc archiveResc mso " + hostname + ":/fake/vault/", 'STDOUT', 'mso')
        self.admin.assert_icommand("iadmin addchildtoresc demoResc cacheResc cache")
        self.admin.assert_icommand("iadmin addchildtoresc demoResc archiveResc archive")

    def tearDown(self):
        super(Test_MSOSuite, self).tearDown()
        with pydevtest_sessions.make_session_for_existing_admin() as admin_session:
            admin_session.assert_icommand("iadmin rmchildfromresc demoResc archiveResc")
            admin_session.assert_icommand("iadmin rmchildfromresc demoResc cacheResc")
            admin_session.assert_icommand("iadmin rmresc archiveResc")
            admin_session.assert_icommand("iadmin rmresc cacheResc")
            admin_session.assert_icommand("iadmin rmresc demoResc")
            admin_session.assert_icommand("iadmin modresc origResc name demoResc", 'STDOUT', 'rename', stdin_string='yes\n')
            shutil.rmtree(get_irods_top_level_dir() + "/cacheRescVault")

    def test_mso_http(self):
        test_file_path = self.admin.session_collection
        self.admin.assert_icommand('ireg -D mso -R archiveResc "//http://people.renci.org/~jasonc/irods/http_mso_test_file.txt" ' +
                   test_file_path + '/test_file.txt')
        self.admin.assert_icommand('iget -f ' + test_file_path + '/test_file.txt')
        self.admin.assert_icommand_fail('ils -L ' + test_file_path + '/test_file.txt', 'STDOUT', ' -99 ')
        os.remove('test_file.txt')
        # unregister the object
        self.admin.assert_icommand('irm -U ' + test_file_path + '/test_file.txt')
        self.admin.assert_icommand('ils -L', 'STDOUT', 'tempZone')

    def test_mso_slink(self):
        test_file_path = self.admin.session_collection
        self.admin.assert_icommand('iput -fR origResc ../zombiereaper.sh src_file.txt')
        self.admin.assert_icommand('ireg -D mso -R archiveResc "//slink:' +
                   test_file_path + '/src_file.txt" ' + test_file_path + '/test_file.txt')
        self.admin.assert_icommand('iget -f ' + test_file_path + '/test_file.txt')

        result = os.system("diff %s %s" % ('./test_file.txt', '../zombiereaper.sh'))
        assert result == 0

        self.admin.assert_icommand('iput -f ../zombiereaper.sh ' + test_file_path + '/test_file.txt')

        # unregister the object
        self.admin.assert_icommand('irm -U ' + test_file_path + '/test_file.txt')

    def test_mso_irods(self):
        hostname = socket.gethostname()
        test_file_path = self.admin.session_collection
        self.admin.assert_icommand('iput -fR pydevtest_AnotherResc ../zombiereaper.sh src_file.txt')
        self.admin.assert_icommand('ireg -D mso -R archiveResc "//irods:' + hostname +
                   ':1247:' + self.admin.username + '@' + self.admin.zone_name + test_file_path + '/src_file.txt" ' + test_file_path + '/test_file.txt')
        self.admin.assert_icommand('iget -f ' + test_file_path + '/test_file.txt')

        result = os.system("diff %s %s" % ('./test_file.txt', '../zombiereaper.sh'))
        assert result == 0

        self.admin.assert_icommand('iput -f ../zombiereaper.sh ' + test_file_path + '/test_file.txt')

        # unregister the object
        self.admin.assert_icommand('irm -U ' + test_file_path + '/test_file.txt')
        self.admin.assert_icommand('irm -f src_file.txt')
