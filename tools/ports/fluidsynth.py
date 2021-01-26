# Copyright 2018 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import logging
from tools import building

TAG = 'v2.1.6-emscripten'
HASH = None
SUBDIR = 'fluidsynth-emscripten-' + TAG

def get(ports, settings, shared):
  if settings.USE_FLUIDSYNTH != 1:
    return []

  ports.fetch_project('fluidsynth', 'https://github.com/devappd/fluidsynth-emscripten/archive/' + TAG + '.zip', SUBDIR, sha512hash=HASH)

  def create():
    logging.info('building port: fluidsynth')
    ports.clear_project_build('fluidsynth')

    source_path = os.path.join(ports.get_dir(), 'fluidsynth', SUBDIR)
    dest_path = os.path.join(ports.get_build_dir(), 'fluidsynth')
    target_path = os.path.join(dest_path, 'libfluidsynth.a')

    configure_args = [
      'cmake',
      '-B' + dest_path,
      '-H' + source_path,
      '-DCMAKE_BUILD_TYPE=Release',
      '-DCMAKE_INSTALL_PREFIX=' + dest_path,
      '-DCMAKE_C_FLAGS_RELEASE=-O2',
      '-Denable-static-emlib=on'
    ]

    if os.name != 'nt': # not windows
      configure_args.extend(['-G', 'Unix Makefiles'])

    building.configure(configure_args)
    building.make(['make', '-j%d' % building.get_num_cores(), '-C' + dest_path, 'install'])
    os.rename(os.path.join(dest_path, 'bin', 'libfluidsynth.a'), target_path)

    ports.install_header_dir(os.path.join(dest_path, 'include'))
    ports.install_header_dir(os.path.join(dest_path, 'include', 'fluidsynth'))

    return target_path

  return [shared.Cache.get('libfluidsynth.a', create, what='port')]


def clear(ports, shared):
  shared.Cache.erase_file('libfluidsynth.a')


def process_dependencies(settings):
  pass


def process_args(ports, args, settings, shared):
  if settings.USE_FLUIDSYNTH == 1:
    get(ports, settings, shared)
    args += ['-I' + os.path.join(ports.get_build_dir(), 'fluidsynth', 'include')]
  return args


def show():
  return 'fluidsynth (USE_FLUIDSYNTH=1; LGPL license)'
