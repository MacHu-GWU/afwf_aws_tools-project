# -*- coding: utf-8 -*-

from . import paths


def setup_test_config_and_credential_file():
    paths.PATH_TEST_BACKUP_CONFIG_FILE.copyto(
        new_abspath=paths.PATH_TEST_CONFIG_FILE.abspath, overwrite=True)
    paths.PATG_TEST_BACKUP_CREDENTIALS_FILE.copyto(
        new_abspath=paths.PATH_TEST_CREDENTIALS_FILE.abspath, overwrite=True)
