################################################################################
 # clips/private_protocol/make.inc
 #
 # History:
 #   2019/04/22 - [Hu GuoHu] Created file
 #
 # Copyright (c) 2019 SimShine, Inc.
 #
 # This file and its contents ( "Software" ) are protected by intellectual
 # property rights including, without limitation, U.S. and/or foreign
 # copyrights. This Software is also the confidential and proprietary
 # information of SimShine, Inc. and its licensors. You may not use, reproduce,
 # disclose, distribute, modify, or otherwise prepare derivative works of this
 # Software or any portion thereof except pursuant to a signed license agreement
 # or nondisclosure agreement with Ambarella, Inc. or its authorized affiliates.
 # In the absence of such an agreement, you agree to promptly notify and return
 # this Software to SimShine, Inc.
 #
 # THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 # INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF NON-INFRINGEMENT,
 # MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 # IN NO EVENT SHALL AMBARELLA, INC. OR ITS AFFILIATES BE LIABLE FOR ANY DIRECT,
 # INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 # (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 # LOSS OF USE, DATA, OR PROFITS; COMPUTER FAILURE OR MALFUNCTION; OR BUSINESS
 # INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 # CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 # ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 # POSSIBILITY OF SUCH DAMAGE.
 #
################################################################################

ifeq ($(BUILD_AMBARELLA_APP_IPCAM_CLIPS), y)

LOCAL_PATH	:= $(call my-dir)
CUR_PATH	= $(CLIPS_DIR)/cv
include $(CLEAR_VARS)

LOCAL_TARGET	:= fdet.a
LOCAL_SRCS	:= $(wildcard $(LOCAL_PATH)/*.c)
#LOCAL_SRCS	+= $(LOCAL_PATH)/cmd_parse.c
LOCAL_CFLAGS	:= -I$(AMB_TOPDIR)/packages/cavalry_mem/inc -I$(LOCAL_PATH)/mtcnn/arch_$(AMBARELLA_ARCH)/ \
		-I$(AMB_TOPDIR)/include/cavalry \
		-I$(AMB_TOPDIR)/packages/vproc/inc \
		#-I$(AMB_TOPDIR)/packages/smartfb

include $(BUILD_APP)
#$(warning $(LOCAL_CFLAGS)) #print
INSTALL_BIN_DIR  = $(FAKEROOT_DIR)/usr/bin

.PHONY: $(LOCAL_TARGET)

$(LOCAL_TARGET): $(LOCAL_MODULE)
	@cp -dpRf $< $(CLIPS_OUT_LIB)/
	@cp $(CUR_PATH)/*.h $(CLIPS_OUT_INC)
	@echo "Build $@ Done."

$(call add-target-into-build, $(LOCAL_TARGET))
endif
