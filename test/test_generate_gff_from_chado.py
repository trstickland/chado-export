#!/usr/bin/env python3

import sys
import os
import pkg_resources
import unittest

from nose import SkipTest


from generate_gff_from_chado import * 
from nose.tools import assert_equal, assert_not_equal, assert_raises, assert_true

#
# NOTE: This test class relies on the contents of the test orglist file.
# If this is changed then the test will also
# need to be updated.
#
# Author: K. Pepper
#
class TestChadoGffExporter:

	DEFAULT_INI_FILE = '/generate_gff_from_chado.ini'
	DEFAULT_ORG_LIST_FILE = 'generate_gff_from_chado.orglist'
	INI_FILE = os.path.join(sys.path[0]+'/test_generate_gff_from_chado.ini')
	ORGLIST_FILE1= 'test_generate_gff_from_chado.orglist1'
	ORGLIST_FILE2= 'test_generate_gff_from_chado.orglist2'
	
	ORG_FILE1_CHUNKS = [['Bsaltans', 'Bxylophilus', 'Eacervulina', 'Ebrunetti', 'Egranulosus', 'Emaxima', 'Emitis', 'Emultilocularis', 'Enecatrix', 'Epraecox'], \
						['Etenella', 'Gpallida', 'Hmicrostoma', 'Lbraziliensis', 'Ldonovani_BPK282A1', 'Linfantum', 'Lmajor', 'Lmexicana', 'Ncaninum', 'Pberghei'], \
						['Pchabaudi', 'Pfalciparum', 'Pgallinaceum', 'Pknowlesi', 'Pmalariae', 'Povale', 'Preichenowi', 'Prelictum', 'PvivaxP01', 'Pyoelii'], \
						['Sjaponicum', 'Smansoni', 'Tannulata', 'Tbruceibrucei927', 'Tbruceigambiense', 'TbruceiLister427', 'Tcongolense', 'Tcruzi', 'Tsolium', 'Tvivax']]
						
	ORG_FILE2_CHUNKS = [['Bsaltans', 'Bxylophilus', 'Eacervulina'], \
						['Ebrunetti', 'Egranulosus', 'Emaxima'], \
						['Emitis', 'Emultilocularis', 'Enecatrix'], \
						['Epraecox']]
	
	def setup(self):
		args = ['program_name']
		self.chadoGffExporter = ChadoGffExporter(args) 

	def teardown(self):
		self.chadoGffExporter = None

	def checkAutoBuild(self):
		if os.environ.get('TRAVIS_BUILD') and os.getenv('TRAVIS_BUILD') == 'yes':
			raise SkipTest("Test skipped for automatic builds")
			
	
	def test_01_read_program_arguments1(self):
    
		# Given
		args = ['program_name']
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
    		
		# Then
		assert self.chadoGffExporter.configfile_property.endswith(TestChadoGffExporter.DEFAULT_INI_FILE)
		assert self.chadoGffExporter.org_list_file_property == TestChadoGffExporter.DEFAULT_ORG_LIST_FILE
		assert self.chadoGffExporter.dump_all_property == False
		
		
	def test_02_read_program_arguments2(self):
		
		# Given
		args = ['program_name', '-a']
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
    		
		# Then
		assert self.chadoGffExporter.dump_all_property == True
		
	def test_03_read_program_arguments3(self):
		
		# Given
		args = ['program_name', '-i', '/somedirectory/config.ini']
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
    		
		# Then
		assert self.chadoGffExporter.configfile_property == '/somedirectory/config.ini'
		
	def test_04_read_program_arguments4(self):
		
		# Given
		args = ['program_name', '-f', '/somedirectory/organism.list']
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
    		
		# Then
		assert self.chadoGffExporter.org_list_file_property == '/somedirectory/organism.list'
		
	def test_05_read_program_arguments5(self):
	
		# Given
		args = ['program_name', '-a', '-i', '/somedirectory/config.ini', '-f', '/somedirectory/organism.list']
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
    		
		# Then
		assert self.chadoGffExporter.configfile_property == '/somedirectory/config.ini'
		assert self.chadoGffExporter.dump_all_property == True
		assert self.chadoGffExporter.org_list_file_property == '/somedirectory/organism.list'
	
	
	def test_06_read_configuration(self):
    
		# Given
		args = ['program_name', '-i', TestChadoGffExporter.INI_FILE]
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
		self.chadoGffExporter.validate_arguments()
		self.chadoGffExporter.read_configuration()
		self.chadoGffExporter.display_configuration()
    		
		# Then
		assert self.chadoGffExporter.gtbin_property == '/software/pathogen/external/apps/usr/local/genometools-1.5.9/bin/gt'
		assert self.chadoGffExporter.writedbentrypath_property == '/software/pathogen/projects/artemis/current/etc/writedb_entry'
		assert self.chadoGffExporter.slice_size_property == 10
		assert self.chadoGffExporter.queue_property == 'basement'
		assert self.chadoGffExporter.targetpath_property == '/lustre/scratch118/infgen/pathdev/kp11/chado-gff'
		assert self.chadoGffExporter.finalresultpath_property == self.chadoGffExporter.targetpath_property + '/results'
		assert self.chadoGffExporter.scriptpath_property == self.chadoGffExporter.targetpath_property + '/scripts'
		assert self.chadoGffExporter.logpath_property == self.chadoGffExporter.targetpath_property + '/logs'
		assert self.chadoGffExporter.statuspath_property == self.chadoGffExporter.targetpath_property + '/status'
	
	
	def test_07_read_organism_list_from_file(self):
	
		# Given
		args = ['program_name', '-i', TestChadoGffExporter.INI_FILE, '-f', 'test/'+TestChadoGffExporter.ORGLIST_FILE1]
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
		self.chadoGffExporter.read_configuration()
		organisms = self.chadoGffExporter.read_organism_list_from_file()
		
		# Then
		assert len(organisms) == 40

	# Must skip on Travis as no database connection available
	# @unittest.skipIf("TRAVIS_BUILD" in os.environ and os.environ["TRAVIS_BUILD"] == "yes", "Skipping this test on Travis CI.")
	def test_08_get_organism_list_all(self):
	
		# Hack as there's no decent annotation mechanism in nose to conditionally skip tests...
		self.checkAutoBuild()
		
		# Given
		args = ['program_name', '-a', '-i', TestChadoGffExporter.INI_FILE]
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
		self.chadoGffExporter.read_configuration()
		
		# Then - will read from chado!
		i = 0
		for org in self.chadoGffExporter.get_organism_list(10):
			print("organism: %s" % (org))
			
			assert len(org) > 0
			
			i = i + 1

		assert i > 1


	def test_09_get_organism_list_from_file1(self):
	
		# Given
		args = ['program_name', '-i', TestChadoGffExporter.INI_FILE, '-f', 'test/'+TestChadoGffExporter.ORGLIST_FILE1]
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
		self.chadoGffExporter.read_configuration()

		# Then
		i = 0
		for org in self.chadoGffExporter.get_organism_list(10):
		
			print("organism: %s" % (org))
			
			assert TestChadoGffExporter.ORG_FILE1_CHUNKS[i] == org
			i = i + 1

		assert i == 4
	
	def test_10_get_organism_list_from_file2(self):
	
		# Given
		args = ['program_name', '-i', TestChadoGffExporter.INI_FILE, '-f', 'test/'+TestChadoGffExporter.ORGLIST_FILE2]
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
		self.chadoGffExporter.read_configuration()

		# Then - use different chunk size
		i = 0
		for org in self.chadoGffExporter.get_organism_list(3):
		
			print("organism: %s" % (org))
			
			assert TestChadoGffExporter.ORG_FILE2_CHUNKS[i] == org
			i = i + 1

		assert i == 4

	# @unittest.skipIf("TRAVIS_BUILD" in os.environ and os.environ["TRAVIS_BUILD"] == "yes", "Skipping this test on Travis CI.")
	def test_11_create_folder_structure(self):
	
		# Hack as there's no decent annotation mechanism in nose to conditionally skip tests...
		self.checkAutoBuild()
			
		# Given
		args = ['program_name', '-i', TestChadoGffExporter.INI_FILE, '-f', 'test/'+TestChadoGffExporter.ORGLIST_FILE1]
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
		self.chadoGffExporter.read_configuration()
		self.chadoGffExporter.create_folder_structure()
		
		# Then
		assert os.path.isdir(self.chadoGffExporter.targetpath_property + '/results')
		assert os.path.isdir(self.chadoGffExporter.targetpath_property + '/scripts')
		assert os.path.isdir(self.chadoGffExporter.targetpath_property + '/logs')
		assert os.path.isdir(self.chadoGffExporter.targetpath_property + '/status')
		assert os.path.isdir(self.chadoGffExporter.targetpath_property + '/results')
	
	
	# @unittest.skipIf("TRAVIS_BUILD" in os.environ and os.environ["TRAVIS_BUILD"] == "yes", "Skipping this test on Travis CI.")
	def test_12_execute_export(self):
	
		# Hack as there's no decent annotation mechanism in nose to conditionally skip tests...
		self.checkAutoBuild()
			
		# Given
		args = ['program_name', '-i', TestChadoGffExporter.INI_FILE, '-f', 'test/'+TestChadoGffExporter.ORGLIST_FILE1]
		
		# Don't actually run the export..
		self.chadoGffExporter.run_jobs = False
    		
		# When
		self.chadoGffExporter.read_program_arguments(args)
		self.chadoGffExporter.read_configuration()
		self.chadoGffExporter.create_folder_structure()
		
		assert self.chadoGffExporter.run_jobs == False
		
		self.chadoGffExporter.execute_export()
		
		# Then
		# We should now have four generated files [scripts] based on the current test organism list file
		list = os.listdir(self.chadoGffExporter.scriptpath_property) # dir is your directory path
		num_scripts = len(list)
		assert num_scripts == 4
	
		
		