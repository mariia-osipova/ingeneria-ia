CC      = clang
CFLAGS  = -Wall -Wextra -Werror -std=c11 -I/usr/local/include
LDLIBS  = /usr/local/lib/libcs50.a

%: %.c
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

clean:
	rm -f hello 1-hello *.o
