# CC = clang
CC = g++

CFLAGS = -std=c++14
LDLIBS = -lgmp -lgmpxx  -lcryptoTools
BUILD = build


SRC = Paillier.cpp bloom.cpp functions.cpp alice.cpp bob.cpp

# ALICE_OBJPATHS = $(BUILD)/.o

OBJPATHS = $(patsubst %.cpp,$(BUILD)/%.o, $(SRC))

# BOB_OBJPATHS = $(patsubst %.cpp,$(BUILD)/%.o, $(SRC))


all: $(BUILD) $(OBJPATHS) alice bob


$(BUILD):
	mkdir -p $(BUILD)


$(BUILD)/%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@


alice:$(BUILD)/Paillier.o $(BUILD)/bloom.o $(BUILD)/functions.o $(BUILD)/alice.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDLIBS)


bob:$(BUILD)/Paillier.o $(BUILD)/bloom.o $(BUILD)/functions.o $(BUILD)/bob.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDLIBS)


clean:
	rm -rf $(BUILD) *~
	rm alice
	rm bob