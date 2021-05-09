# Maintainer: workonfire <kolucki62@gmail.com>

_pkgname=uno
pkgname=$_pkgname-git
pkgver=ALPHA
pkgrel=1
pkgdesc="A simple Python implementation of the UNO game."
arch=('any')
url=""
license=('GPL')
depends=('python-colorama')
provides=('uno')
conflicts=('uno')
source=("${pkgname}"::git+https://github.com/workonfire/UNO.git)
sha256sums=('SKIP')

build() {
	cd "$srcdir/$pkgname"
	python setup.py build
}

package() {
	cd "$srcdir/$pkgname"
	python setup.py install --root="$pkgdir/" --optimize=1 --skip-build
	install -Dm644 LICENSE "$pkgdir"/usr/share/licenses/$pkgname/LICENSE
}
