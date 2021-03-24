#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

# This file is part of Guadalinex
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__ = "Abraham Macías <amacias@gruposolutia.com>"
__copyright__ = "Copyright (C) 2011, Junta de Andalucía <devmaster@guadalinex.org>"
__license__ = "GPL-2"


###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ######################

import os
import sys
import glob

try:
    import DistUtilsExtra.auto
    from distutils.core import setup, Command
    from DistUtilsExtra.command import build_i18n, build_extra
except ImportError:
    print('To build HelpChannelClient you need https://launchpad.net/python-distutils-extra', file=sys.stderr)
    sys.exit(1)
assert DistUtilsExtra.auto.__version__ >= '2.39', 'needs DistUtilsExtra.auto >= 2.39'

def get_datafiles(datadir):
    source = ''
    datafiles = []
    for root, dirs, files in os.walk(datadir):
        sources = []
        for f in files:
            sources.append(os.path.join(root,f))
        root_s = root.split('/')
        root_s.remove(datadir)
        root = str.join('/', root_s)
        datafiles.append(['share/helpchannel/'+datadir+'/'+root, sources])
    return datafiles

datafiles = get_datafiles('locale')
datafiles.append(('share/applications/', glob.glob('helpchannel.desktop')))
datafiles.append(('share/helpchannel', glob.glob('helpchannel.svg')))
datafiles.append(('/etc', glob.glob('helpchannel.conf')))



def update_desktop_file(datadir):

    try:
        fin = open('helpchannel.desktop', 'r')
        fout = open(fin.name + '.new', 'w')

        for line in fin:
            if 'Icon=' in line:
                line = "Icon=%s\n" % (datadir + 'helpchannel.svg')
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError) as e:
        print ("ERROR: Can't find helpchannel.desktop")
        sys.exit(1)

def update_bin_script(datadir):

    try:
        fin = open('helpchannel', 'r')
        fout = open(fin.name + '.new', 'w')

        for line in fin:
            if 'BASE_DIR =' in line:
                line = "BASE_DIR = '%s'\n" % (datadir)
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError) as e:
        print ("ERROR: Can't find helpchannel script")
        sys.exit(1)

def copy_pages(pages_path):
    pass


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):
    def run(self):
        update_desktop_file(self.prefix + '/share/helpchannel/')
        update_bin_script(self.prefix + '/share/helpchannel')
        DistUtilsExtra.auto.install_auto.run(self)
        os.system('find %s -type f -exec chmod 644 \\{\\} \\;'%(self.prefix + '/share/helpchannel'))
        os.system('find %s -type f -exec chmod 644 \\{\\} \\;'%(self.prefix + '/lib/python3/site-packages/pycos'))
        os.system('find %s -type f -exec chmod 644 \\{\\} \\;'%(self.prefix + '/lib/python3/site-packages/websocket'))
        os.system('mv %s %s'%(self.prefix + '/lib/python3/site-packages/websocket', self.prefix + '/lib/python3/dist-packages/websocket'))
        os.system('mv %s %s'%(self.prefix + '/lib/python3/site-packages/pycos', self.prefix + '/lib/python3/dist-packages/pycos'))
        return True


class Clean(Command):
    description = "custom clean command that forcefully removes dist/build directories and update data directory"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        os.system('rm -rf ./build ./dist')



       
        
##################################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ######################
##################################################################################

DistUtilsExtra.auto.setup(
    name='helpchannel',
    version='1.2.0',
    license='GPL-2',
    author='GECOS Team',
    author_email='gecos@guadalinex.org',
    description='Help Channel client',
    url='https://github.com/gecos-team/gecoshc-client',

    keywords=['python', 'gnome', 'guadalinex', 'gecos', 'help'],

    packages=[
        'pycos',
        'websocket',
    ],

    package_dir={
        },

    scripts=[
        'helpchannel',
        'hctunnel.py'
    ],
    data_files = datafiles,
    cmdclass={
        'install': InstallAndUpdateDataDirectory,
        "build": build_extra.build_extra,
        "build_i18n":  build_i18n.build_i18n
    }
)
