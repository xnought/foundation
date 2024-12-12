all: deploy

deploy:
	python3 compile.py --base /foundation
	git add .
	git commit -m "deploy $(uuidgen)"
	git push

dev:
	python3 compile.py