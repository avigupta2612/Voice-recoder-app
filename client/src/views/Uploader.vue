<template>
  <div>
    <h1 class="mb-4">UPLOAD</h1>
    <div class="upload-box">
      <CCard class="h-100">
        <CCardBody>
          <div
            v-if="uploadInProgress"
            class="d-flex justify-content-center align-items-center h-100"
          >
            <div>
              <CSpinner color="primary" style="width: 3rem; height: 3rem" class="mb-4" />
              <h4>Processing Audio...</h4>
            </div>
          </div>
          <div
            v-else
            class="upload-boundary d-flex justify-content-center align-items-center h-100"
            @click="selectFile"
          >
            <input
              type="file"
              id="uploader"
              class="d-none"
              accept="audio/*"
              @change="handleUpload"
            />
            <CButton color="primary">CHOOSE FILE</CButton>
          </div>
        </CCardBody>
      </CCard>
    </div>
  </div>
</template>
<script>
import { ajaxCallMixin } from '@/mixins/HttpCommon';
export default {
  name: "Uploader",
  mixins: [ajaxCallMixin],
  data() {
    return {
      fileName: "",
      fields: [],
      uploadInProgress: false,
    };
  },
  methods: {
    selectFile() {
      document.getElementById("uploader").click();
    },
    handleUpload(event) {
      const selectedFile = event.target.files[0];
      this.fileName = selectedFile.name;
      this.fields['audio_data'] = selectedFile;
      this.uploadInProgress = true;
      const url = '/upload_audio';
      const data = {};
      this.ajaxCall(url, data, this.handleUploadResponse, this.fields);
    },
    handleUploadResponse(apiResponse) {
        console.log(apiResponse);
    }
  },
};
</script>
<style scoped>
.upload-box {
  height: 16rem;
}
.upload-boundary {
  border: 1px dashed rgba(0, 0, 0, 0.5);
  cursor: pointer;
}
</style>