# Created by: baodongli <robert.li1@dell.com>
# $FreeBSD: tags/RELEASE_12_2_0/devel/py-ironic-python-agent/Makefile 23455 2021-01-21 19:43:55Z sunpoet $

PORTNAME=	ironic-python-agent
PORTVERSION=	6.5.0

CATEGORIES=	devel python
USE_GITHUB=     yes
GH_ACCOUNT=     Dell-EMC-Cloud
GH_PROJECT=     ironic-python-agent
GH_TAGNAME=     525fa09960696681e7f4a565d03038b0d9677ecc
PKGNAMEPREFIX=	${PYTHON_PKGNAMEPREFIX}

MAINTAINER=	sunpoet@FreeBSD.org
COMMENT=	Openstack Ironic Python Agent

LICENSE=	APACHE20
LICENSE_FILE=	${WRKSRC}/LICENSE


USES=		python:3.6+
USE_PYTHON=	autoplist concurrent distutils

NO_ARCH=	yes

.include <bsd.port.mk>
