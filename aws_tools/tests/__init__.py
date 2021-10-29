# -*- coding: utf-8 -*-

from . import paths


def setup_test_config_and_credential_file():
    paths.P_TEST_BACKUP_CONFIG_FILE.copyto(
        new_abspath=paths.P_TEST_CONFIG_FILE.abspath, overwrite=True)
    paths.P_TEST_BACKUP_CREDENTIALS_FILE.copyto(
        new_abspath=paths.P_TEST_CREDENTIALS_FILE.abspath, overwrite=True)
