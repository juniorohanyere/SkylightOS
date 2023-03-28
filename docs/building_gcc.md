# Building GCC for Target Architecture

#### **If you've compiled binutils for one target already, you don't need to recompile it as it doesn't change**

<br>

Prerequsites:
* Latest GDB source
* Latest GCC source
* Latest Binutils source

Setting Targets:
```
export PREFIX="/usr/local/bin/cross"
export TARGET={Set Target Architecture Here (example: i686-elf for 32-bit elf)}
export PATH="$PREFIX/bin:$PATH"
```

Compiling Binutils:
```
tar -xvf bintutils-X.xx.tar.gz
mkdir build-binutils && cd build-binutils
../binutils-X.xx/configure --target=$TARGET --prefix="$PREFIX" --with-sysroot --disable-nls --disable-werror
make
sudo make install
```

Compiling GCC:
```
tar -xvf gcc-XX.x.x.tar.gz
mkdir build-gcc && cd build-gcc
../gcc-XX.x.x/configure --target=$TARGET --prefix="$PREFIX" --disable-nls --enable-languages=c,c++ --without-headers
make all-gcc && make all-target-libgcc
sudo make install-gcc && sudo make install-target-libgcc
```

Compiling GDB:
```
tar -xvf gdb-XX.x.tar.gz
mkdir build-gdb && cd build-gdb
../gdb-XX.x/configure --target=$TARGET --prefix="$PREFIX" --disable-werror
make all-gdb
sudo make install-gdb
```

Test if everything works:
```
/usr/local/bin/cross/bin/$TARGET-gcc --version
/usr/local/bin/cross/bin/$TARGET-gdb --version
/usr/local/bin/cross/bin/$TARGET-ld --version
```
If successful, you should see gcc, gdb and ld (part of binutils) return version information.