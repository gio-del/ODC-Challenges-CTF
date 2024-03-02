# Compiler and Compiler Flags
CC 		:=	gcc
CFLAGS 	:=	-g -fPIE -pie

# Target binary
TARGET	:=	santas_letter

# Source and Object Files
SRC 	:=	santas_letter.c

# Default target
all: $(TARGET)

# Rule to link the object file to create the executable
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $^

# Clean target
clean:
	rm -f $(TARGET) $(OBJ)

# Phony targets
.PHONY: all clean
