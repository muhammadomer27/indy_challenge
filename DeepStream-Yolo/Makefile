CUDA_VER?=
ifeq ($(CUDA_VER),)
  $(error "CUDA_VER is not set")
endif

APP:= deepstream-app

TARGET_DEVICE = $(shell gcc -dumpmachine | cut -f1 -d -)

NVDS_VERSION:=7.0

LIB_INSTALL_DIR?=/opt/nvidia/deepstream/deepstream-$(NVDS_VERSION)/lib/
# APP_INSTALL_DIR?=/opt/nvidia/deepstream/deepstream-$(NVDS_VERSION)/bin/
APP_INSTALL_DIR?=./

ifeq ($(TARGET_DEVICE),aarch64)
  CFLAGS:= -DPLATFORM_TEGRA
endif

SRCS:= $(wildcard *.c) $(wildcard *.cpp)
SRCS+= $(wildcard apps-common/src/*.c)
SRCS+= $(wildcard apps-common/src/deepstream-yaml/*.cpp)

INCS:= $(wildcard *.h)

PKGS:= gstreamer-1.0 gstreamer-video-1.0 x11 json-glib-1.0

OBJS:= $(SRCS:.c=.o)
OBJS:= $(OBJS:.cpp=.o)

CFLAGS+= -I./ -I apps-common/includes \
		 -I includes -DDS_VERSION_MINOR=1 -DDS_VERSION_MAJOR=5 \
		 -I /usr/local/cuda-$(CUDA_VER)/include

LIBS:= -L/usr/local/cuda-$(CUDA_VER)/lib64/ -lcudart

LIBS+= -L$(LIB_INSTALL_DIR) -lnvdsgst_meta -lnvds_meta -lnvdsgst_helper -lnvdsgst_customhelper \
	  -lnvdsgst_smartrecord -lnvds_utils -lnvds_msgbroker -lm -lyaml-cpp \
    -lcuda -lgstrtspserver-1.0 -ldl -Wl,-rpath,$(LIB_INSTALL_DIR)

CFLAGS+= $(shell pkg-config --cflags $(PKGS))

LIBS+= $(shell pkg-config --libs $(PKGS))

all: $(APP)

%.o: %.c $(INCS) Makefile
	$(CC) -c -o $@ $(CFLAGS) $<

%.o: %.cpp $(INCS) Makefile
	$(CXX) -c -o $@ $(CFLAGS) $<

$(APP): $(OBJS) Makefile
	$(CXX) -o $(APP) $(OBJS) $(LIBS)

install: $(APP)
	cp -rv $(APP) $(APP_INSTALL_DIR)

clean:
	rm -rf $(OBJS) $(APP)
