CC = g++

INCPATHS = -I/usr/local/opt/openssl@1.1/include
CFLAGS = -std=c++14 $(INCPATHS)
LDLIBS = -lgmp -lgmpxx  -lcryptoTools -llibOTe -lrelic_s -lssl -lcrypto
LDPATH = -L/usr/local/opt/openssl@1.1/lib
BUILD = build

SRC = alice.cpp bob.cpp cJSON.cpp functions.cpp

OBJPATHS = $(patsubst %.cpp,$(BUILD)/%.o, $(SRC))

all: $(BUILD) $(OBJPATHS) alice bob

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

alice:$(BUILD)/alice.o $(BUILD)/cJSON.o $(BUILD)/bloom.o $(BUILD)/functions.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDPATH) $(LDLIBS)

bob:$(BUILD)/bob.o $(BUILD)/cJSON.o $(BUILD)/bloom.o $(BUILD)/functions.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDPATH) $(LDLIBS)

clean:
	rm -rf $(BUILD) *~
	rm alice
	rm bob