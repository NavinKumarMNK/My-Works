build:
	docker build . -t megnav-dev

run:
	docker run --rm -it -v -rm .:/workspace megnav-dev 

build-ml:
	docker build -f ml.Dockerfile . -t megnav-dev

run-ml:
	docker run --gpus all -it --rm megnav-ml