.PHONY: format lint test

format:
	yapf --recursive -i --style ./style.ini ./tool ./searchcode

lint:
	pylint --disable=all --enable=E bidder_data_pipeline
