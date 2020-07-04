CC = clang
INCPATHS = -I/usr/local/Cellar/openssl@1.1/1.1.1d/include -I/usr/local/Cellar/gmp/6.1.2_2/include
CFLAGS = -g -Wall -O3 $(INCPATHS) -march=native
LDLIBS = -lgmp -lssl -lcrypto
LDPATH = -L/usr/local/Cellar/gmp/6.1.2_2/lib -L/usr/local/Cellar/openssl@1.1/1.1.1d/lib
BUILD = build


SRC = main.c crypto.c ore.c 
OBJPATHS = $(patsubst %.c,$(BUILD)/%.o, $(SRC))


all: $(BUILD) $(OBJPATHS) main


$(BUILD):
	mkdir -p $(BUILD)


$(BUILD)/%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@


main:$(OBJPATHS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDPATH) $(LDLIBS)

clean:
	rm -rf $(BUILD) *~
	rm main