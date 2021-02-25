from setuptools import find_packages, setup

setup(
	name = 'tbcompanion',
	version = '0.0.1',
	package = find_packages(),
	include_package_date = True,
	zip_safe = False,
	install_requires =[
		'flask',
	],
)