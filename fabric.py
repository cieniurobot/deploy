#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
from fabric.api import task, env, local, run
from ftpsync.targets import FsTarget
from ftpsync.ftp_target import FtpTarget
from ftpsync.synchronizers import BiDirSynchronizer


#
# Configuration 
#

DEPLOY_FOLDER = "deploy"
SOURCE_FOLDER = "src"
FTP_HOST = "example.com"
FTP_TARGET = "/domains/xxx/public_html"


def build_html():
    print "running gulp..."
    run("gulp deploy")

def make_temp():
    if os.path.exists(DEPLOY_FOLDER):
        shutil.rmtree(DEPLOY_FOLDER)
    shutil.copy2(SOURCE_FOLDER, DEPLOY_FOLDER)
    return False


def make_config(env):
    print "Making prod config file..."
    shutil.copy2('{0}/protected/config/main.php-{1}'.format(SOURCE_FOLDER, env), '{0}/protected/config/main.php'.format(DEPLOY_FOLDER))
    return False


def synchronize(user, password):
    print "syncing..."
    try:
        local = FsTarget(DEPLOY_FOLDER)
        remote = FtpTarget(FTP_TARGET, FTP_HOST, user, password, tls=True)
        opts = {"resolve": "skip", "verbose": 1, "dry_run" : False}
        s = BiDirSynchronizer(local, remote, opts)
        s.run()
        print "sync complete..."
    except Exception as e:
        print type(e)
        print e.args
        print e


@task
def deploy(env="test", user, password):
    print "deploying..."
    make_temp()
    make_config(env)
    synchronize(user, password)