FROM ubuntu:20.04 AS builder

LABEL description='Dockerfile for building dynawo docker image'

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
RUN apt-get update && apt-get install -y \
	autoconf \
	automake \
	cmake \
	doxygen \
	doxygen-latex \
	gcc \
	gcovr \
	gettext \
	git \
	g++ \
	gfortran \
	hwloc \
	lcov \
	libblas-dev \
	liblpsolve55-dev \
	libarchive-dev \
	libboost-all-dev \
	liblapack-dev \
	libexpat1-dev \
	libsqlite3-dev \
	libtool \
	libncurses5-dev \
	libreadline-dev \
	libdigest-perl-md5-perl \
	libxml2-utils \
	libcurl4-openssl-dev \
	libopenblas-openmp-dev \
	lsb-release \
	make \
	openjdk-8-jdk \
	pkgconf \
	patch \
	python3-pip \
	python-lxml \
	python-psutil \
	qt5-default \
	rsync \
	unzip \
	wget \
	zlib1g-dev \
	&& apt-get autoclean \
	&& apt-get autoremove \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /vat/tmp/*   
        
RUN git clone https://github.com/dynawo/dynawo.git \
	&& cd dynawo \
	&& echo '#!/bin/bash \n\
	export DYNAWO_HOME=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd) \n\
	\n\
	export DYNAWO_SRC_OPENMODELICA=$DYNAWO_HOME/OpenModelica/Source \n\
	export DYNAWO_INSTALL_OPENMODELICA=$DYNAWO_HOME/OpenModelica/Install \n\
	\n\
	export DYNAWO_LOCALE=en_GB \n\
	export DYNAWO_RESULTS_SHOW=false \n\
	export DYNAWO_BROWSER=firefox \n\
	export DYNAWO_NB_PROCESSORS_USED=4 \n\
	export DYNAWO_BUILD_TYPE=Release \n\
	export DYNAWO_CXX11_ENABLED=YES \n\
	export DYNAWO_PYTHON_COMMAND=python3 \n\
	$DYNAWO_HOME/util/envDynawo.sh $@' > myEnvDynawo.sh \
	&& chmod +x myEnvDynawo.sh \
	&& ./myEnvDynawo.sh build-omcDynawo \
	&& ./myEnvDynawo.sh build-3rd-party \
	&& ./myEnvDynawo.sh build-dynawo \
	&& ./myEnvDynawo.sh deploy-autocompletion --deploy \
	&& rm -rf OpenModelica/Source \
	&& rm -rf build \
	&& rm -rf OpenModelica/Install/share \
	&& rm -f OpenModelica/Install/lib/libipopt.so.0.0.0
	
RUN rm -rf dynawo/dynawo/3rdParty/adept/adept-2.0.8.tar.gz dynawo/dynawo/3rdParty/libxml2/v2.9.4.tar.gz dynawo/dynawo/3rdParty/libiidm/v1.4.0.tar.gz dynawo/dynawo/3rdParty/modelicalib dynawo/dynawo/3rdParty/suitesparse/SuiteSparse-5.4.0.tar.gz dynawo/dynawo/3rdParty/sundials-5.3.0.tar.gz dynawo/dynawo/3rdParty/xercesc/xerces-c-3.2.2.tar.gz dynawo/documentation

FROM ubuntu:20.04 AS runtime

RUN apt-get update && apt-get install -y bash-completion git g++ python3 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /vat/tmp/*

COPY --from=builder dynawo dynawo

COPY --from=builder /usr/lib/x86_64-linux-gnu/libtinfo.so.6 /usr/lib/x86_64-linux-gnu/libdl.so.2 /usr/lib/x86_64-linux-gnu/libc.so.6 /usr/lib/x86_64-linux-gnu/libnss_files.so.2 /usr/lib/x86_64-linux-gnu/libselinux.so.1 /usr/lib/x86_64-linux-gnu/libpcre2-8.so.0 /usr/lib/x86_64-linux-gnu/libpthread.so.0 /usr/lib/x86_64-linux-gnu/libz.so.1 /usr/lib/x86_64-linux-gnu/libarchive.so.13 /usr/lib/x86_64-linux-gnu/libcurl.so.4 /usr/lib/x86_64-linux-gnu/libjsoncpp.so.1 /usr/lib/x86_64-linux-gnu/libm.so.6 /usr/lib/x86_64-linux-gnu/libuv.so.1 /usr/lib/x86_64-linux-gnu/librhash.so.0 /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 /usr/lib/x86_64-linux-gnu/libnettle.so.7 /usr/lib/x86_64-linux-gnu/libacl.so.1 /usr/lib/x86_64-linux-gnu/liblzma.so.5 /usr/lib/x86_64-linux-gnu/libzstd.so.1 /usr/lib/x86_64-linux-gnu/liblz4.so.1 /usr/lib/x86_64-linux-gnu/libbz2.so.1.0 /usr/lib/x86_64-linux-gnu/libxml2.so.2 /usr/lib/x86_64-linux-gnu/libnghttp2.so.14 /usr/lib/x86_64-linux-gnu/libidn2.so.0 /usr/lib/x86_64-linux-gnu/librtmp.so.1 /usr/lib/x86_64-linux-gnu/libssh.so.4 /usr/lib/x86_64-linux-gnu/libpsl.so.5 /usr/lib/x86_64-linux-gnu/libssl.so.1.1 /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1 /usr/lib/x86_64-linux-gnu/libgssapi_krb5.so.2 /usr/lib/x86_64-linux-gnu/libldap_r-2.4.so.2 /usr/lib/x86_64-linux-gnu/libbrotlidec.so.1 /usr/lib/x86_64-linux-gnu/libicuuc.so.66 /usr/lib/x86_64-linux-gnu/libunistring.so.2 /usr/lib/x86_64-linux-gnu/libgnutls.so.30 /usr/lib/x86_64-linux-gnu/libhogweed.so.5 /usr/lib/x86_64-linux-gnu/libgmp.so.10 /usr/lib/x86_64-linux-gnu/libk5crypto.so.3 /usr/lib/x86_64-linux-gnu/libcom_err.so.2 /usr/lib/x86_64-linux-gnu/libkrb5support.so.0 /usr/lib/x86_64-linux-gnu/libresolv.so.2 /usr/lib/x86_64-linux-gnu/libsasl2.so.2 /usr/lib/x86_64-linux-gnu/libgssapi.so.3 /usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 /usr/lib/x86_64-linux-gnu/libicudata.so.66 /usr/lib/x86_64-linux-gnu/libp11-kit.so.0 /usr/lib/x86_64-linux-gnu/libtasn1.so.6 /usr/lib/x86_64-linux-gnu/libkeyutils.so.1 /usr/lib/x86_64-linux-gnu/libheimntlm.so.0 /usr/lib/x86_64-linux-gnu/libkrb5.so.26 /usr/lib/x86_64-linux-gnu/libasn1.so.8 /usr/lib/x86_64-linux-gnu/libhcrypto.so.4 /usr/lib/x86_64-linux-gnu/libroken.so.18 /usr/lib/x86_64-linux-gnu/libffi.so.7 /usr/lib/x86_64-linux-gnu/libwind.so.0 /usr/lib/x86_64-linux-gnu/libheimbase.so.1 /usr/lib/x86_64-linux-gnu/libhx509.so.5 /usr/lib/x86_64-linux-gnu/libsqlite3.so.0 /usr/lib/x86_64-linux-gnu/libcrypt.so.1 /usr/lib/x86_64-linux-gnu/libboost_program_options.so.1.71.0 /usr/lib/x86_64-linux-gnu/libexpat.so.1 /usr/lib/x86_64-linux-gnu/libcolamd.so /usr/lib/x86_64-linux-gnu/libhwloc.so.15 /usr/lib/x86_64-linux-gnu/libopenblas.so.0 /usr/lib/x86_64-linux-gnu/libudev.so.1 /usr/lib/x86_64-linux-gnu/libltdl.so.7 /usr/lib/x86_64-linux-gnu/libgfortran.so.5 /usr/lib/x86_64-linux-gnu/libgomp.so.1 /usr/lib/x86_64-linux-gnu/libquadmath.so.0 /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0 /usr/lib/x86_64-linux-gnu/libboost_serialization.so.1.71.0 /usr/lib/x86_64-linux-gnu/libboost_log.so.1.71.0 /usr/lib/x86_64-linux-gnu/libboost_thread.so.1.71.0 /usr/lib/x86_64-linux-gnu/

COPY --from=builder /usr/lib/x86_64-linux-gnu/openblas-openmp/libopenblas.so.0 /usr/lib/x86_64-linux-gnu/openblas-openmp/
COPY --from=builder /lib64/ld-linux-x86-64.so.2  /lib64/

WORKDIR dynawo

RUN ./myEnvDynawo.sh deploy-autocompletion --deploy && ldconfig

CMD /bin/bash

