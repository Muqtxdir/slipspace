pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'slipspace'
gnome = import('gnome')

gnome.compile_resources('slipspace',
  'slipspace.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'slipspace.in',
  output: 'slipspace',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

slipspace_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(slipspace_sources, install_dir: moduledir)

slipspace_components_sources = [
  'components/__init__.py',
]

install_data(slipspace_components_sources, install_dir: moduledir / 'components')

slipspace_datetime_sources = [
  'components/datetime/__init__.py',
  'components/datetime/clock.py',
  'components/datetime/datetime_label.py',
  'components/datetime/enums.py',
]

install_data(slipspace_datetime_sources,
  install_dir: moduledir / 'components' / 'datetime',
)

slipspace_panel_sources = [
  'components/panel/__init__.py',
  'components/panel/panel.py',
]

install_data(slipspace_panel_sources,
  install_dir: moduledir / 'components' / 'panel',
)
