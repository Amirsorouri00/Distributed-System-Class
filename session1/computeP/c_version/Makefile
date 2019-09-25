LDFLAGS := -lm


all: p

p: p.o
	 gcc -o p p.o $(LDFLAGS)

p.o: p.c
	 gcc -c p.c
     
clean:
	 rm p.o p
