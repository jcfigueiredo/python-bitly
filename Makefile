test: clean
	@nosetests --verbose --with-coverage --cover-package=bitly -sd
clean:
	@find . -name "*.pyc" -delete
	@rm -rf build/ dist/ *.egg-info/
