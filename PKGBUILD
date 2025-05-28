# Maintainer: workonfire <kolucki62@gmail.com>

pkgname=uno
pkgver=1.0.0a1
pkgrel=1
pkgdesc="A simple CLI implementation of the UNO card game in Python"
arch=('any')
url="https://github.com/workonfire/UNO"
license=('GPL')
depends=('python' 'python-rich')
makedepends=('python-build' 'python-installer' 'python-wheel' 'python-hatchling')
source=("uno-${pkgver}.tar.gz")
sha256sums=('SKIP')

build() {
	cd "$srcdir/${pkgname}-${pkgver}"
	python -m build --wheel --no-isolation
}

package() {
	cd "$srcdir/${pkgname}-${pkgver}"
	python -m installer --destdir="$pkgdir" dist/*.whl
	install -Dm644 LICENSE "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
}
