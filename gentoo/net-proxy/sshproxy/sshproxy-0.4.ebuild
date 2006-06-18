# Copyright 1999-2006 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

inherit distutils

DESCRIPTION="sshproxy is an ssh gateway to apply ACLs on ssh connections"
HOMEPAGE="http://penguin.fr/sshproxy/"
SRC_URI="http://penguin.fr/sshproxy/download/${P}.tar.gz"

LICENSE="GPL"
SLOT="0"
KEYWORDS="~alpha ~amd64 ~ia64 ~ppc ~sparc ~x86"
IUSE="mysql"

DEPEND=">=dev-lang/python-2.4.0
		>=dev-python/paramiko-1.6
		mysql? ( >=dev-python/mysql-python-1.2.0 )"
RDEPEND=""
