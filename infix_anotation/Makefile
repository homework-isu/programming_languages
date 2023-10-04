ifeq ($(OS), Windows_NT)
	RM = del
	TARGET = main.exe

else
	RM = rm
	TARGET = main
endif

run: build
	@$(TARGET)

test:
	@go test -cover ./lib

cover:
	@go test -coverprofile=coverage.out ./lib

cover_html: cover
	@go tool cover -html=coverage.out

build:
	@go build -o $(TARGET) ./cmd/main.go

clear:
	@$(RM) $(TARGET)