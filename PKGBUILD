# Maintainer: workonfire <kolucki62@gmail.com>

_pkgname=uno
pkgname=${_pkgname}-git
pkgver=1.0.0a1
pkgrel=1
pkgdesc="A simple CLI implementation of the UNO card game in Python"
arch=('any')
url="https://github.com/workonfire/UNO"
license=('GPL')
depends=('python' 'python-rich')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-hatchling' 'git')
provides=('uno')
conflicts=('uno')
source=("${pkgname}::git+https://github.com/workonfire/UNO.git")
sha256sums=('SKIP')

prepare() {
	mv "$srcdir/$pkgname" "$srcdir/_src"
}

build() {
	cd "$srcdir/_src"
	python -m build --wheel --no-isolation
}

package() {
	cd "$srcdir/_src"
	python -m installer --destdir="$pkgdir" dist/*.whl

	# Licencja
	install -Dm644 LICENSE "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
}
