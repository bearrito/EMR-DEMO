wget http://python.org/ftp/python/2.7.2/Python-2.7.2.tar.bz2
tar jfx Python-2.7.2.tar.bz2
cd Python-2.7.2
./configure --with-threads --enable-shared
make
sudo make install
sudo ln -s /usr/local/lib/libpython2.7.so.1.0 /usr/lib/
sudo ln -s /usr/local/lib/libpython2.7.so /usr/