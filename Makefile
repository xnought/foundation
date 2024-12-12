all: deploy

deploy:
	python3 compile.py --base /foundation
	git add .
	uuidgen | xargs -Iid git commit -m "deploy id"
	git push

dev:
	python3 compile.py