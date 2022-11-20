#! /usr/bin/env python3

import common, os, pathlib, sys, zipfile

def parents(path):
  res = []
  parent = path.parent
  while '.' != str(parent):
    res.insert(0, parent)
    parent = parent.parent
  return res

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir, 'skia'))
  
  build_type = common.build_type()
  version = common.version()
  machine = common.machine()
  target = common.target()
  classifier = common.classifier()
  out_bin = 'out/' + build_type + '-' + target + '-' + machine

  globs = [
    '*',
    '**/*'
  ]

  dist = 'Skia-' + target + '-' + build_type + '-' + machine + classifier + '.zip'
  #dist = 'Skia-' + 'source' + '.zip'
  print('> Writing', dist)
  
  with zipfile.ZipFile(os.path.join(os.pardir, dist), 'w', compression=zipfile.ZIP_DEFLATED) as zip:
    dirs = set()
    for glob in globs:
      for path in pathlib.Path().glob(glob):
        if not path.is_dir():
          for dir in parents(path):
            if not dir in dirs:
              zip.write(str(dir))
              dirs.add(dir)
          zip.write(str(path))

  return 0

if __name__ == '__main__':
  sys.exit(main())
