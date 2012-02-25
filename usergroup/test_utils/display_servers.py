#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 et sts=4 ai:

"""Classes which represent the user's display."""

import os
import subprocess


class RealDisplay(object):
    """Use the users display."""

    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        pass


class VNCDisplay(object):
    """Use a VNCServer for display."""

    def __init__(self, viewer=False):
        self.display = ':10'
        self.original = os.getenv('DISPLAY')

        self.vncserver = None

        self.viewer = viewer

    def __enter__(self):
        # Start the VNCServer
        p = subprocess.Popen(
            ' '.join(['vncserver', self.display, '-SecurityTypes', 'None']),
            shell=True,
            stdout=file('vncserver.stdout', 'w'),
            stderr=subprocess.STDOUT,
            )
        p.wait()
        self.vncserver = 'RUNNING'

        # Set the environment
        os.environ['DISPLAY'] = ':10'

        # Start a window manager
        winman = subprocess.Popen(
            ' '.join(['metacity']),
            shell=True,
            )

        # Start a viewer if needed
        if self.viewer:
            viewer = subprocess.Popen(
                ' '.join(['vncviewer', self.display]),
                shell=True,
                stdout=file('vncviewer.stdout', 'w'),
                stderr=subprocess.STDOUT,
                env={'DISPLAY': self.original},
                )

    def __exit__(self, exc_type, exc_value, traceback):
        if self.vncserver == 'RUNNING':
            os.putenv('DISPLAY', self.original)

            p = subprocess.Popen(
                ' '.join(['vncserver', '-kill', self.display]),
                shell=True,
                )
            p.wait()

            self.vncserver = 'TERMINATED'
