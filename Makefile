CC = clang
CFLAGS = -Wall -std=c99 -pedantic

all:  _molecule.so

clean:  
	rm -f *.o *.so myprog

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

mol.o:  mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

_molecule.so: libmol.so molecule_wrap.o
	$(CC) molecule_wrap.o -shared -lm -dynamiclib -L/usr/include/python3.7m -lpython3.7m -L. -lmol -o _molecule.so

molecule_wrap.c: molecule.i
	swig -python molecule.i

molecule_wrap.o:  molecule_wrap.c
	$(CC) $(CFLAGS) -c molecule_wrap.c -fPIC -o molecule_wrap.o -I/usr/include/python3.7m

test3.o:  test3.c mol.h
	$(CC) $(CFLAGS) -c test3.c -o test3.o

myprog:  test3.o libmol.so
	$(CC) test3.o -L. -lmol -o myprog

