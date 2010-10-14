test: clean
	@nosetests --verbose --with-coverage --cover-package=bitly -sd
clean:
	@find . -name "*.pyc" -delete
